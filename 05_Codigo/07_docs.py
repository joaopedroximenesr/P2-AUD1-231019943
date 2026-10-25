"""Gera 04_Matriz_Normas_e_Fontes/matriz_cobertura_normas.md e 04_Matriz_Normas_e_Fontes/fontes.md a partir de 05_Codigo/cobertura.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cobertura import FONTES, MATRIZ  # noqa: E402

DOCS = Path(__file__).resolve().parents[1] / "04_Matriz_Normas_e_Fontes"


def md(linhas, cab):
    out = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    out += ["| " + " | ".join(str(c).replace("|", "/") for c in ln) + " |" for ln in linhas]
    return "\n".join(out)


DOCS.mkdir(exist_ok=True)
(DOCS / "matriz_cobertura_normas.md").write_text(
    "# Matriz de cobertura das normas - Dossiê PRIO S.A. 2025\n\nVersões conforme a tabela do CFC acessada em 23/10/2026. "
    "Para o exercício de 2025 aplicaram-se as versões vigentes no período auditado.\n\n"
    + md([[m["norma"], m["versao"], m["requisito"], m["pt"], m["evidencias"], m["status"]] for m in MATRIZ],
         ["Norma", "Versão consultada", "Requisito", "Papel de trabalho", "Evidência / arquivo", "Status"]) + "\n", encoding="utf-8")
(DOCS / "fontes.md").write_text(
    "# Relação das fontes utilizadas\n\nTodas as fontes são públicas. Data de acesso: 23/10/2026.\n\n"
    + md([[f["id"], f["documento"], f["emissor"], f["url"], f["acesso"], f["exercicio"], f["paginas"]] for f in FONTES],
         ["ID", "Documento", "Emissor", "Endereço eletrônico", "Acesso", "Exercício", "Página / uso"]) + "\n", encoding="utf-8")
print("docs gerados")
