"""
Gráficos do dossiê (PNG, 200 dpi) - dados reais (CVM/BCB/EIA) e dados SINTÉTICOS (identificados no título).
Uso: python 05_Codigo/04_graficos.py      Saída: 01_Dossie/graficos/*.png
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notas_dfp2025 as ne  # noqa: E402
from parametros import RESULTADOS, conta  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "01_Dossie" / "graficos"
AZUL, LARANJA, AQUA, CINZA, TXT, TXT2 = "#2a78d6", "#eb6834", "#1baf7a", "#b9b8b3", "#0b0b0b", "#52514e"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": "#d6d5d0", "axes.labelcolor": TXT2,
                     "xtick.color": TXT2, "ytick.color": TXT2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#ecebe7", "grid.linewidth": 0.6, "axes.axisbelow": True,
                     "axes.titleweight": "bold", "axes.titlesize": 10.5, "axes.titlelocation": "left",
                     "figure.facecolor": "white", "savefig.facecolor": "white"})


def bi(v):
    return f"R$ {v/1e6:,.1f} bi".replace(",", "X").replace(".", ",").replace("X", ".")


def salvar(fig, nome):
    fig.tight_layout()
    fig.savefig(OUT / nome, dpi=200)
    plt.close(fig)


def composicao_ativo():
    itens = [("Imobilizado", "1.02.03"), ("Intangível", "1.02.04"), ("IR/CS diferido", "1.02.01.07"),
             ("Caixa e equivalentes", "1.01.01"), ("Estoques", "1.01.04"), ("Contas a receber", "1.01.03")]
    v = [conta("BPA", c) for _, c in itens]
    outros = conta("BPA", "1") - sum(v)
    nomes = [n for n, _ in itens] + ["Demais ativos"]
    v = v + [outros]
    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    cores = [AZUL] + [CINZA] * (len(v) - 1)
    y = np.arange(len(v))[::-1]
    ax.barh(y, [x / 1e6 for x in v], color=cores, height=0.62)
    for yi, x in zip(y, v):
        ax.text(x / 1e6 + 0.4, yi, f"{bi(x)}  ({x/conta('BPA','1'):.1%})".replace(".", ","), va="center", color=TXT, fontsize=8)
    ax.set_yticks(y, nomes)
    ax.set_xlabel("R$ bilhões")
    ax.set_xlim(0, 40)
    ax.grid(axis="y", visible=False)
    ax.set_title("Composição do ativo consolidado em 31/12/2025 (BP CVM)")
    salvar(fig, "g01_composicao_ativo.png")


def imobilizado_classes():
    df = pd.DataFrame(ne.NE8_IMOBILIZADO, columns=["classe", "grupo", "m", "t", "c", "d", "a", "s25", "s24"])
    df = pd.concat([df, pd.DataFrame([{"classe": "Direito de uso (NE 15)", "s25": 610_400, "s24": 2_421_249}])])
    df = df.sort_values("s25").tail(11)
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    y = np.arange(len(df))
    ax.barh(y + 0.2, df["s24"] / 1e6, height=0.38, color=CINZA, label="31/12/2024")
    ax.barh(y - 0.2, df["s25"] / 1e6, height=0.38, color=AZUL, label="31/12/2025")
    ax.set_yticks(y, df["classe"], fontsize=7.5)
    ax.set_xlabel("R$ bilhões")
    ax.grid(axis="y", visible=False)
    ax.legend(frameon=False, loc="lower right")
    ax.set_title("Imobilizado por classe (NE 8 e NE 15) - 11 maiores saldos")
    salvar(fig, "g02_imobilizado_classes.png")


def receita_campos():
    c25 = {n: v for n, _b, _d, v in ne.NE22_RECEITA}
    c24 = dict(ne.NE22_RECEITA_2024)
    nomes = list(c25)
    x = np.arange(len(nomes))
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    ax.bar(x - 0.2, [c24[n] / 1e6 for n in nomes], 0.38, color=CINZA, label="2024")
    ax.bar(x + 0.2, [c25[n] / 1e6 for n in nomes], 0.38, color=AZUL, label="2025")
    for xi, n in zip(x, nomes):
        ax.text(xi + 0.2, c25[n] / 1e6 + 0.1, f"{c25[n]/1e6:.1f}".replace(".", ","), ha="center", fontsize=7.5, color=TXT)
    ax.set_xticks(x, nomes)
    ax.set_ylabel("R$ bilhões")
    ax.grid(axis="x", visible=False)
    ax.legend(frameon=False)
    ax.set_title("Receita líquida por campo (NE 22) - Peregrino substitui a queda de Frade")
    salvar(fig, "g03_receita_campos.png")


def alavancagem():
    r = json.loads((RESULTADOS / "resumo_analiticos.json").read_text(encoding="utf-8"))["indicadores"]
    nomes = ["Sem pró-forma\n(DFP 2025)", "Pró-forma Peregrino 40%\n(premissa didática)", "Divulgado 2T26\n(apresentação 05/08/2026)"]
    v = [r["alavancagem"], r["alavancagem_proforma"], 1.5]
    fig, ax = plt.subplots(figsize=(7.2, 2.8))
    b = ax.bar(nomes, v, color=[LARANJA, AZUL, AQUA], width=0.5)
    ax.axhline(2.5, color=TXT, lw=1.2, ls="--")
    ax.text(2.45, 2.56, "limite do covenant 2,5x", ha="right", fontsize=8, color=TXT)
    for rect, val in zip(b, v):
        ax.text(rect.get_x() + rect.get_width() / 2, val + 0.06, f"{val:.2f}x".replace(".", ","), ha="center", fontsize=9, color=TXT)
    ax.set_ylim(0, 3.4)
    ax.set_ylabel("Dívida líquida / EBITDA aj.")
    ax.grid(axis="x", visible=False)
    ax.set_title("PT 570 - Alavancagem recalculada x covenant (NE 13/14)")
    salvar(fig, "g04_alavancagem.png")


def tornado_aro():
    s = pd.read_csv(RESULTADOS / "PT540_sensibilidade_aro.csv")
    s = s[s["campo"].str.startswith("TOTAL") & (s["cenario"] != "Base")].sort_values("variacao", key=abs)
    fig, ax = plt.subplots(figsize=(7.2, 2.9))
    cores = [LARANJA if v > 0 else AZUL for v in s["variacao"]]
    ax.barh(s["cenario"], s["variacao"] / 1e3, color=cores, height=0.55)
    for yi, v in enumerate(s["variacao"]):
        ax.text(v / 1e3 + (15 if v > 0 else -15), yi, f"{v/1e3:+,.0f}".replace(",", "."), va="center",
                ha="left" if v > 0 else "right", fontsize=8, color=TXT)
    ax.axvline(0, color=TXT2, lw=0.8)
    ax.axvline(155, color=TXT, lw=0.8, ls=":")
    ax.axvline(-155, color=TXT, lw=0.8, ls=":")
    ax.text(160, -0.6, "MG ±155", fontsize=7, color=TXT2)
    ax.set_xlabel("Variação da provisão (R$ milhões) - laranja aumenta / azul reduz")
    ax.grid(axis="y", visible=False)
    ax.set_xlim(-1000, 1300)
    ax.set_title("PT 540 - Sensibilidade da provisão para abandono (exceto Polvo)")
    salvar(fig, "g05_tornado_aro.png")


def benford():
    b = pd.read_csv(RESULTADOS / "PT520_benford_custo.csv")
    fig, ax = plt.subplots(figsize=(7.2, 2.6))
    ax.bar(b["digito"], b["observado"] * 100, color=AZUL, width=0.6, label="Observado (base sintética)")
    ax.plot(b["digito"], b["esperado_benford"] * 100, color=LARANJA, marker="o", lw=2, ms=5, label="Esperado (Lei de Benford)")
    ax.set_xticks(range(1, 10))
    ax.set_ylabel("% dos registros")
    ax.set_xlabel("Primeiro dígito do custo histórico")
    ax.legend(frameon=False)
    ax.grid(axis="x", visible=False)
    mad = b["desvio_abs"].mean()
    ax.set_title(f"[DADOS SINTÉTICOS] Teste de Benford - MAD {mad:.4f} (conformidade próxima)".replace(".", ","))
    salvar(fig, "g06_benford.png")


def deteccao():
    c = pd.read_csv(RESULTADOS / "PT450_inseridos_x_detectados.csv")
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    y = np.arange(len(c))[::-1]
    ax.barh(y + 0.18, c["inseridos"], 0.34, color=CINZA, label="Inseridos (gabarito)")
    ax.barh(y - 0.18, c["detectados"], 0.34, color=AQUA, label="Detectados pelos testes")
    ax.set_yticks(y, c["tipo_erro_inserido"], fontsize=7.5)
    ax.legend(frameon=False, loc="lower right")
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Registros")
    ax.set_title("[DADOS SINTÉTICOS] Erros inseridos x detectados (CAATs em 100% da base)")
    salvar(fig, "g07_deteccao.png")


def mus():
    r = json.loads((RESULTADOS / "resumo_testes.json").read_text(encoding="utf-8"))
    a, d = r["mus"], r["mus_pos_ajustes"]
    nomes = ["Base entregue", "Após ajustes simulados"]
    proj = [a["distorcao_projetada_brl"] / 1e6, d["distorcao_projetada_brl"] / 1e6]
    prec = [a["precisao_basica_brl"] / 1e6, d["precisao_basica_brl"] / 1e6]
    inc = [a["provisao_incremental_brl"] / 1e6, d["provisao_incremental_brl"] / 1e6]
    fig, ax = plt.subplots(figsize=(7.2, 2.8))
    ax.bar(nomes, prec, 0.45, color=CINZA, label="Precisão básica")
    ax.bar(nomes, proj, 0.45, bottom=prec, color=LARANJA, label="Distorção projetada")
    ax.bar(nomes, inc, 0.45, bottom=np.add(prec, proj), color=AZUL, label="Provisão incremental")
    ax.axhline(93, color=TXT, ls="--", lw=1.2)
    ax.text(0.5, 100, "distorção tolerável R$ 93 mi", fontsize=8, ha="center")
    for i in range(2):
        tot = prec[i] + proj[i] + inc[i]
        ax.text(i, tot + (10 if i == 0 else 45), f"LSD R$ {tot:,.0f} mi".replace(",", "."), ha="center", fontsize=9)
    ax.set_ylabel("R$ milhões")
    ax.set_ylim(0, 620)
    ax.legend(frameon=False, fontsize=7.5)
    ax.grid(axis="x", visible=False)
    ax.set_title("[DADOS SINTÉTICOS] PT 530 - Limite superior de distorção (MUS, 95%)")
    salvar(fig, "g08_mus.png")


def vencimentos():
    nomes = [x[0] for x in ne.NE29_LIQUIDEZ]
    ate12 = [x[2] / 1e6 for x in ne.NE29_LIQUIDEZ]
    acima = [x[3] / 1e6 for x in ne.NE29_LIQUIDEZ]
    fig, ax = plt.subplots(figsize=(7.2, 2.8))
    y = np.arange(len(nomes))[::-1]
    ax.barh(y, ate12, color=LARANJA, height=0.55, label="Até 12 meses")
    ax.barh(y, acima, left=ate12, color=AZUL, height=0.55, label="Acima de 12 meses")
    ax.axvline(conta("BPA", "1.01.01") / 1e6, color=TXT, ls=":", lw=1)
    ax.text(conta("BPA", "1.01.01") / 1e6 + 0.2, 4.35, "caixa 31/12/2025", fontsize=7.5)
    ax.set_yticks(y, nomes, fontsize=8)
    ax.set_xlabel("Fluxos não descontados (R$ bilhões) - NE 29")
    ax.legend(frameon=False, loc="lower right")
    ax.grid(axis="y", visible=False)
    ax.set_title("PT 570 - Perfil de vencimento dos passivos financeiros")
    salvar(fig, "g09_vencimentos.png")


def base_classes():
    b = pd.read_csv(Path(__file__).resolve().parents[1] / "02_Base_Simulada" / "base_imobilizado_sintetica.csv.gz",
                    usecols=["classe_ne", "valor_contabil_brl"])
    g = b.groupby("classe_ne").agg(linhas=("valor_contabil_brl", "size"), valor=("valor_contabil_brl", "sum"))
    g = g.sort_values("linhas").tail(8)
    fig, ax = plt.subplots(figsize=(7.2, 2.9))
    y = np.arange(len(g))
    ax.barh(y, g["linhas"] / 1000, color=AZUL, height=0.6)
    for yi, (n, v) in enumerate(zip(g["linhas"], g["valor"])):
        ax.text(n / 1000 + 2, yi, f"{n:,} linhas | R$ {v/1e9:.2f} bi".replace(",", "."), va="center", fontsize=7.5)
    ax.set_yticks(y, g.index, fontsize=7.5)
    ax.set_xlim(0, 270)
    ax.set_xlabel("Milhares de registros")
    ax.grid(axis="y", visible=False)
    ax.set_title(f"[DADOS SINTÉTICOS] Base de imobilizado: {len(b):,} registros - 8 classes com mais linhas".replace(",", "."))
    salvar(fig, "g10_base_classes.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for f in [composicao_ativo, imobilizado_classes, receita_campos, alavancagem, tornado_aro, benford, deteccao, mus,
              vencimentos, base_classes]:
        f()
        print("ok", f.__name__)
