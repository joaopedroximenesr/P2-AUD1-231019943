"""Utilitários de HTML para o dossiê (layout padronizado dos papéis de trabalho)."""
from __future__ import annotations

import html
import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
RES = RAIZ / "06_Resultados"
PREP = "Matrícula 231019943"
DATA = "23/10/2026"

TIPOS = {
    "R": ("Realizado com evidência pública", "b-r"),
    "P": ("Planejado por falta de acesso", "b-p"),
    "S": ("Simulado para fins didáticos", "b-s"),
}


def br(v, dec=0, pct=False):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "-"
    if pct:
        return f"{v*100:,.{dec}f}%".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def esc(t):
    return html.escape(str(t))


def tab(cab, linhas, cls="", larg=None, num_cols=()):
    th = "".join(f"<th{f' style=width:{larg[i]}' if larg else ''}>{c}</th>" for i, c in enumerate(cab))
    corpo = []
    for ln in linhas:
        tds = []
        for j, v in enumerate(ln):
            a = ' class="n"' if j in num_cols else ""
            tds.append(f"<td{a}>{v}</td>")
        corpo.append("<tr>" + "".join(tds) + "</tr>")
    return f'<div class="tw"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{"".join(corpo)}</tbody></table></div>'


def badge(t):
    nome, cls = TIPOS[t]
    return f'<span class="badge {cls}">{nome}</span>'


def ul(itens):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in itens) + "</ul>"


def ref(code):
    alvo = code.replace(" ", "")
    return f'<a class="xr" href="#{alvo}">{code}</a>'


def fig(arquivo, legenda):
    return f'<figure><img src="graficos/{arquivo}" alt="{esc(legenda)}"><figcaption>{legenda}</figcaption></figure>'


def pt(codigo, titulo, norma, objetivo, conta, afirmacoes, riscos, populacao, procedimentos, evidencias, resultados,
       conclusao, limitacoes, corpo=""):
    """Papel de trabalho com a estrutura mínima exigida (item 4 das instruções)."""
    ancora = codigo.replace(" ", "")
    procs = tab(["#", "Procedimento", "Classificação", "Ref. / evidência"],
                [[i + 1, p[0], badge(p[1]), p[2] if len(p) > 2 else ""] for i, p in enumerate(procedimentos)],
                cls="procs", larg=["4%", "58%", "18%", "20%"])
    return f"""
<section class="pt" id="{ancora}">
  <div class="pt-head">
    <div class="pt-code">{codigo}</div>
    <div class="pt-title"><h2>{titulo}</h2><div class="pt-norma">{norma}</div></div>
  </div>
  <div class="meta">
    <div><b>Objetivo</b>{objetivo}</div>
    <div><b>Conta, processo ou divulgação examinada</b>{conta}</div>
  </div>
  <div class="meta">
    <div><b>Afirmações relevantes</b>{afirmacoes}</div>
    <div><b>Riscos identificados</b>{riscos}</div>
  </div>
  <div class="meta one"><div><b>População, fontes e critérios de seleção</b>{populacao}</div></div>
  {corpo}
  <h3>Procedimentos planejados ou executados</h3>
  {procs}
  <h3>Evidências e referências cruzadas</h3>
  {evidencias}
  <h3>Resultados e exceções</h3>
  {resultados}
  <div class="fecho">
  <div class="conc"><b>Conclusão.</b> {conclusao}</div>
  <div class="lim"><b>Limitações.</b> {limitacoes}</div>
  <div class="sign">
    <div><b>Preparado por:</b> {PREP} &nbsp;|&nbsp; <b>Data:</b> {DATA}</div>
    <div><b>Revisado por:</b> ______________________ &nbsp;|&nbsp; <b>Data:</b> ____/____/______ <span class="muted">(campo de revisão em branco; nenhuma revisão de terceiros foi simulada)</span></div>
  </div></div>
</section>"""


def carregar_json(nome):
    return json.loads((RES / nome).read_text(encoding="utf-8"))


def csv(nome, **kw):
    return pd.read_csv(RES / nome, **kw)


CSS = """
@page { size: A4; margin: 16mm 14mm 16mm 14mm;
  @bottom-right { content: "Página " counter(page) " de " counter(pages); font: 8pt 'Segoe UI', Arial, sans-serif; color: #6b6a65; }
  @bottom-left { content: "Dossiê de Auditoria PRIO S.A. 2025 - trabalho acadêmico UnB CCA0024 - Matrícula 231019943"; font: 8pt 'Segoe UI', Arial, sans-serif; color: #6b6a65; } }
@page :first { @bottom-right { content: none; } @bottom-left { content: none; } }
:root { --ink:#16181d; --ink2:#4b4f58; --muted:#7a7d85; --line:#d9dce2; --brand:#1f3a5f; --brand2:#2a78d6; --bg2:#f4f6f9;
  --r:#1baf7a; --p:#eda100; --s:#e34948; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', Arial, sans-serif; color: var(--ink); font-size: 9.2pt; line-height: 1.42; margin: 0; background: #fff; }
h1 { font-size: 22pt; margin: 0 0 6px; color: var(--brand); }
h2 { font-size: 13.5pt; margin: 0; color: var(--brand); }
h3 { font-size: 10.2pt; margin: 14px 0 6px; color: var(--brand); border-bottom: 1px solid var(--line); padding-bottom: 2px; }
h4 { font-size: 9.6pt; margin: 10px 0 4px; }
p { margin: 4px 0 6px; text-align: justify; }
a { color: var(--brand2); text-decoration: none; }
ul { margin: 3px 0 6px 18px; padding: 0; } li { margin: 1px 0; }
.capa { height: 262mm; display: flex; flex-direction: column; justify-content: space-between; page-break-after: always;
  border-left: 10px solid var(--brand); padding: 10mm 0 0 12mm; }
.capa .sup { font-size: 10pt; color: var(--ink2); letter-spacing: .5px; }
.capa .tit { font-size: 30pt; font-weight: 700; color: var(--brand); line-height: 1.1; margin-top: 30mm; }
.capa .sub { font-size: 14pt; color: var(--ink2); margin-top: 6mm; }
.capa .box { border: 1px solid var(--line); background: var(--bg2); padding: 10px 14px; margin-top: 14mm; font-size: 9.5pt; width: 92%; }
.capa .aviso { border-left: 4px solid var(--s); background: #fdf0ef; padding: 8px 12px; font-size: 8.8pt; width: 92%; }
.sec { page-break-before: always; }
.pt { page-break-before: always; }
.pt-head { display: flex; gap: 10px; align-items: stretch; border-bottom: 3px solid var(--brand); padding-bottom: 6px; margin-bottom: 8px; }
.pt-code { white-space: nowrap; background: var(--brand); color: #fff; font-weight: 700; font-size: 13pt; padding: 6px 10px; min-width: 70px; text-align: center; display: flex; align-items: center; justify-content: center; }
.pt-norma { color: var(--ink2); font-size: 8.6pt; margin-top: 2px; }
.meta { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin: 6px 0; }
.meta.one { grid-template-columns: 1fr; }
.meta > div { background: var(--bg2); border: 1px solid var(--line); padding: 6px 8px; font-size: 8.7pt; }
.meta b { display: block; color: var(--brand); font-size: 8pt; text-transform: uppercase; letter-spacing: .3px; margin-bottom: 2px; }
.tw { overflow-x: auto; margin: 4px 0 8px; }
table { border-collapse: collapse; width: 100%; font-size: 8.2pt; page-break-inside: auto; }
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
th { background: var(--brand); color: #fff; text-align: left; padding: 4px 5px; font-weight: 600; vertical-align: bottom; }
td { border-bottom: 1px solid var(--line); padding: 3px 5px; vertical-align: top; }
td.n { text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }
tbody tr:nth-child(even) td { background: #fafbfc; }
.badge { display: inline-block; font-size: 7.4pt; font-weight: 600; padding: 1px 6px; border-radius: 9px; white-space: nowrap; }
.b-r { background: #e3f6ee; color: #0d6b48; border: 1px solid #9fdcc3; }
.b-p { background: #fff4d6; color: #7a5300; border: 1px solid #f1d27e; }
.b-s { background: #fde4e3; color: #9c1f1e; border: 1px solid #f3aaa9; }
.conc { border-left: 4px solid var(--r); background: #eefaf5; padding: 6px 9px; margin: 8px 0 4px; }
.lim { border-left: 4px solid var(--p); background: #fffaeb; padding: 6px 9px; margin: 4px 0; }
.alert { border-left: 4px solid var(--s); background: #fdf0ef; padding: 6px 9px; margin: 6px 0; }
.note { border-left: 4px solid var(--brand2); background: #eef4fc; padding: 6px 9px; margin: 6px 0; }
.sign { margin-top: 10px; border-top: 1px dashed var(--line); padding-top: 6px; font-size: 8.4pt; color: var(--ink2); }
.muted { color: var(--muted); font-size: 7.8pt; }
figure { margin: 6px 0 10px; text-align: center; page-break-inside: avoid; }
figure img { max-width: 100%; width: 172mm; }
figcaption { font-size: 7.8pt; color: var(--ink2); margin-top: 2px; }
.kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin: 8px 0; }
.kpi { border: 1px solid var(--line); padding: 7px 9px; background: var(--bg2); }
.kpi .v { font-size: 13pt; font-weight: 700; color: var(--brand); }
.kpi .l { font-size: 7.8pt; color: var(--ink2); }
.toc a { color: var(--ink); } .toc td { padding: 2px 5px; }
.heat td.h0 { background: #e3f6ee !important; } .heat td.h1 { background: #fff4d6 !important; }
.heat td.h2 { background: #fde0c9 !important; } .heat td.h3 { background: #f8c9c8 !important; font-weight: 600; }
.heat td { text-align: center; } .heat td:first-child { text-align: left; }
.letter { border: 1px solid var(--line); padding: 10px 14px; background: #fff; font-size: 8.8pt; }
.letter .wm { color: var(--s); font-weight: 700; font-size: 8pt; letter-spacing: .5px; }
.xr { font-weight: 600; }
.fecho { page-break-inside: avoid; break-inside: avoid; }
table.fixed { table-layout: fixed; }
table.fixed td { word-wrap: break-word; }
.small { font-size: 8pt; }
.legend span { margin-right: 10px; }
"""
