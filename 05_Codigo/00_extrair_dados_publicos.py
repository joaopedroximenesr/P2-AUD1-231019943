"""
PT 500 / PT 510 / PT 560 - Extração reproduzível de dados públicos da PRIO S.A.

Fontes (todas públicas, sem login):
  * CVM - Portal de Dados Abertos (DFP 2025, DFP 2024, ITR 2026, FCA 2026, IPE 2025/2026)
  * Banco Central do Brasil - SGS série 1 (PTAX venda diária)
  * EIA (via espelho datasets/oil-prices) - Brent diário

Uso:  python 05_Codigo/00_extrair_dados_publicos.py
Saída: 07_Dados_Publicos/*.csv  (os .zip brutos ficam em 07_Dados_Publicos/brutos/, não acompanham a entrega)

Identificação da companhia: CNPJ 10.629.105/0001-68 | Código CVM 022187 | PRIO3 (B3)
"""
from __future__ import annotations

import io
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "07_Dados_Publicos"
BRUTOS = SAIDA / "brutos"
CNPJ = "10.629.105/0001-68"
CD_CVM = "022187"

CVM = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC"
ARQUIVOS = {
    "dfp2025": f"{CVM}/DFP/DADOS/dfp_cia_aberta_2025.zip",
    "dfp2024": f"{CVM}/DFP/DADOS/dfp_cia_aberta_2024.zip",
    "itr2026": f"{CVM}/ITR/DADOS/itr_cia_aberta_2026.zip",
    "fca2026": f"{CVM}/FCA/DADOS/fca_cia_aberta_2026.zip",
    "ipe2026": f"{CVM}/IPE/DADOS/ipe_cia_aberta_2026.zip",
}
PTAX = ("https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json"
        "&dataInicial=01/01/2024&dataFinal=31/12/2025")
BRENT = "https://raw.githubusercontent.com/datasets/oil-prices/main/data/brent-daily.csv"


def baixar(nome: str, url: str, ext: str = "zip") -> Path:
    BRUTOS.mkdir(parents=True, exist_ok=True)
    destino = BRUTOS / f"{nome}.{ext}"
    if not destino.exists():
        print(f"  baixando {url}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=180) as r:
            destino.write_bytes(r.read())
    return destino


def ler_zip(caminho: Path, membro: str) -> pd.DataFrame:
    with zipfile.ZipFile(caminho) as z:
        with z.open(membro) as f:
            return pd.read_csv(io.TextIOWrapper(f, encoding="latin1"), sep=";", dtype=str)


def demonstracoes(zip_path: Path, prefixo: str, ano: int, saida_prefixo: str) -> None:
    """Extrai BPA, BPP, DRE, DFC_MI e DVA (consolidado e individual) da companhia."""
    for dem in ["BPA", "BPP", "DRE", "DFC_MI", "DVA"]:
        for esc in ["con", "ind"]:
            df = ler_zip(zip_path, f"{prefixo}_cia_aberta_{dem}_{esc}_{ano}.csv")
            df = df[df["CD_CVM"] == CD_CVM].copy()
            if df.empty:
                continue
            df["VL_CONTA"] = df["VL_CONTA"].astype(float)
            cols = [c for c in ["DT_REFER", "VERSAO", "DT_INI_EXERC", "DT_FIM_EXERC", "ORDEM_EXERC",
                                "CD_CONTA", "DS_CONTA", "ESCALA_MOEDA", "VL_CONTA"] if c in df.columns]
            df[cols].to_csv(SAIDA / f"{saida_prefixo}_{dem}_{esc}.csv", index=False, encoding="utf-8-sig")


def main() -> None:
    SAIDA.mkdir(exist_ok=True)
    print("1) CVM - DFP 2025 (exercício auditado e comparativo 2024)")
    z = baixar("dfp2025", ARQUIVOS["dfp2025"])
    demonstracoes(z, "dfp", 2025, "dfp2025")
    for membro, nome in [("dfp_cia_aberta_2025.csv", "dfp2025_documento"),
                         ("dfp_cia_aberta_parecer_2025.csv", "dfp2025_pareceres"),
                         ("dfp_cia_aberta_composicao_capital_2025.csv", "dfp2025_capital")]:
        df = ler_zip(z, membro)
        col = "CNPJ_CIA"
        df[df[col] == CNPJ].to_csv(SAIDA / f"{nome}.csv", index=False, encoding="utf-8-sig")

    print("2) CVM - DFP 2024 (saldos de abertura conforme publicados originalmente - PT 510)")
    z = baixar("dfp2024", ARQUIVOS["dfp2024"])
    demonstracoes(z, "dfp", 2024, "dfp2024")
    df = ler_zip(z, "dfp_cia_aberta_parecer_2024.csv")
    df[df["CNPJ_CIA"] == CNPJ].to_csv(SAIDA / "dfp2024_pareceres.csv", index=False, encoding="utf-8-sig")

    print("3) CVM - ITR 2026 (eventos subsequentes / continuidade - PT 560 e PT 570)")
    z = baixar("itr2026", ARQUIVOS["itr2026"])
    demonstracoes(z, "itr", 2026, "itr2026")

    print("4) CVM - FCA 2026 (nome empresarial, auditor, valores mobiliários)")
    z = baixar("fca2026", ARQUIVOS["fca2026"])
    for parte in ["geral", "auditor", "valor_mobiliario", "escriturador"]:
        df = ler_zip(z, f"fca_cia_aberta_{parte}_2026.csv")
        df[df["CNPJ_Companhia"] == CNPJ].to_csv(SAIDA / f"fca2026_{parte}.csv", index=False, encoding="utf-8-sig")

    print("5) CVM - IPE 2026 (fatos relevantes e comunicados após o encerramento)")
    z = baixar("ipe2026", ARQUIVOS["ipe2026"])
    df = ler_zip(z, "ipe_cia_aberta_2026.csv")
    df = df[df["CNPJ_Companhia"] == CNPJ]
    df.sort_values("Data_Entrega").to_csv(SAIDA / "ipe2026_prio.csv", index=False, encoding="utf-8-sig")

    print("6) BCB - PTAX diária 2024-2025 | 7) Brent diário (EIA)")
    try:
        ptax = json.loads(baixar("ptax", PTAX, "json").read_text())
        p = pd.DataFrame(ptax)
        p["data"] = pd.to_datetime(p["data"], dayfirst=True)
        p["valor"] = p["valor"].astype(float)
        p.to_csv(SAIDA / "mercado_ptax_diaria.csv", index=False)
    except Exception as exc:  # fonte externa pode estar indisponível
        print("  PTAX indisponível:", exc, file=sys.stderr)
    try:
        b = pd.read_csv(baixar("brent", BRENT, "csv"))
        b.columns = ["data", "brent_usd"]
        b = b[b["data"] >= "2023-01-01"]
        b.to_csv(SAIDA / "mercado_brent_diario.csv", index=False)
    except Exception as exc:
        print("  Brent indisponível:", exc, file=sys.stderr)
    print("Concluído. Arquivos em", SAIDA)


if __name__ == "__main__":
    main()
