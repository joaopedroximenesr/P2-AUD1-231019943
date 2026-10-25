"""
Parâmetros centrais do trabalho (PT 320 - Materialidade) e leitura das demonstrações da CVM.
Todos os scripts importam daqui para garantir consistência entre papéis de trabalho.
Valores em R$ mil, salvo indicação.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / "07_Dados_Publicos"
RESULTADOS = RAIZ / "06_Resultados"
PREPARADOR = "Matrícula 231019943"
DATA_PREPARO = "23/10/2026"
DATA_BASE = "31/12/2025"
SEMENTE = 231019943


def conta(dem: str, codigo: str, exercicio: str = "ÚLTIMO", escopo: str = "con", ano: int = 2025) -> float:
    """Valor (R$ mil) de uma conta CVM. exercicio: 'ÚLTIMO' (2025) ou 'PENÚLTIMO' (2024)."""
    df = pd.read_csv(DADOS / f"dfp{ano}_{dem}_{escopo}.csv", dtype={"CD_CONTA": str})
    linha = df[(df["CD_CONTA"] == codigo) & (df["ORDEM_EXERC"] == exercicio)]
    return float(linha["VL_CONTA"].iloc[0]) if len(linha) else 0.0


def demonstracao(dem: str, escopo: str = "con", ano: int = 2025, nivel: int = 4) -> pd.DataFrame:
    df = pd.read_csv(DADOS / f"dfp{ano}_{dem}_{escopo}.csv", dtype={"CD_CONTA": str})
    df = df[df["CD_CONTA"].str.count(r"\.") < nivel]
    p = df.pivot_table(index=["CD_CONTA", "DS_CONTA"], columns="ORDEM_EXERC", values="VL_CONTA", aggfunc="first")
    p = p.reset_index().rename(columns={"ÚLTIMO": "2025", "PENÚLTIMO": "2024"})
    p = p[(p["2025"] != 0) | (p["2024"] != 0)]
    return p[["CD_CONTA", "DS_CONTA", "2024", "2025"]]


# ------------------------------------------------------------------ PT 320 - Materialidade
def bases_materialidade() -> list[dict]:
    receita = conta("DRE", "3.01")
    ebit = conta("DRE", "3.05")
    lair = conta("DRE", "3.07")
    da = conta("DFC_MI", "6.01.01.02")
    outras = -conta("DRE", "3.04.05") - conta("DRE", "3.04.04")
    ebitda_aj = ebit + da + outras
    ativo = conta("BPA", "1")
    pl = conta("BPP", "2.03")
    return [
        {"base": "Receita líquida (DRE 3.01)", "valor": receita, "pct_min": 0.005, "pct_max": 0.01, "pct": 0.01, "escolhida": True},
        {"base": "EBITDA ajustado (3.05 + D&A DFC 6.01.01.02 + outras desp. líquidas)", "valor": ebitda_aj, "pct_min": 0.01,
         "pct_max": 0.02, "pct": 0.02, "escolhida": False},
        {"base": "Ativo total (BP 1)", "valor": ativo, "pct_min": 0.0025, "pct_max": 0.005, "pct": 0.0025, "escolhida": False},
        {"base": "Patrimônio líquido (BP 2.03)", "valor": pl, "pct_min": 0.005, "pct_max": 0.01, "pct": 0.005, "escolhida": False},
        {"base": "Lucro antes dos tributos (DRE 3.07) - descartada: negativo/volátil", "valor": lair, "pct_min": 0.05,
         "pct_max": 0.05, "pct": 0.05, "escolhida": False},
    ]


MATERIALIDADE_GLOBAL = 155_000          # R$ mil - 1% da receita líquida (R$ 155.840 mil) arredondado para baixo
PCT_EXECUCAO = 0.60                     # auditoria inicial + aquisições relevantes + 1º ano do auditor
MATERIALIDADE_EXECUCAO = 93_000         # R$ mil
PCT_TRIVIAL = 0.05
LIMITE_TRIVIAL = 7_750                  # R$ mil - distorções claramente triviais
MATERIALIDADE_ESPECIFICA = {
    "Remuneração da administração e transações com partes relacionadas (NE 21)": 1_750,   # 5% de R$ 34.932 mil
    "Divulgação de passivos contingentes possíveis (NE 30)": 77_500,                       # 50% da MG
}
