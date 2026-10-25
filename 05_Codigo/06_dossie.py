"""
Monta o dossiê (HTML) e imprime em PDF com o Microsoft Edge/Chrome headless.
Uso: python 05_Codigo/06_dossie.py          Saída: 01_Dossie/Dossie_Auditoria_PRIO_2025.html e .pdf
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dossie_pts_a as a  # noqa: E402
import dossie_pts_b as b  # noqa: E402
from dossie_base import CSS  # noqa: E402

DOSSIE = Path(__file__).resolve().parents[1] / "01_Dossie"
NAVEGADORES = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
               r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
               r"C:\Program Files\Google\Chrome\Application\chrome.exe", "msedge", "google-chrome", "chromium", "chrome"]

INDICE = [("ID", "Identificação da companhia e visão financeira", "-"),
          ("PT EC", "Estrutura conceitual - caracterização do trabalho", "NBC TA Estrutura Conceitual"),
          ("PT 200", "Objetivos gerais, ética, ceticismo e risco", "NBC TA 200 (R1)"), ("PT 210", "Termos do trabalho", "NBC TA 210 (R1)"),
          ("PT 220", "Gestão da qualidade", "NBC TA 220 (R3)"), ("PT 230", "Documentação", "NBC TA 230 (R1)"),
          ("PT 240", "Fraude", "NBC TA 240 (R1)"), ("PT 250", "Leis e regulamentos", "NBC TA 250"),
          ("PT 260", "Comunicação com a governança", "NBC TA 260 (R2)"), ("PT 265", "Deficiências de controle", "NBC TA 265"),
          ("PT 300", "Planejamento", "NBC TA 300 (R1)"), ("PT 315", "Identificação e avaliação dos riscos", "NBC TA 315 (R2)"),
          ("PT 320", "Materialidade", "NBC TA 320 (R1)"), ("PT 330", "Respostas aos riscos", "NBC TA 330 (R1)"),
          ("PT 402", "Organização prestadora de serviços", "NBC TA 402"), ("PT 450", "Distorções", "NBC TA 450 (R1)"),
          ("PT 500", "Evidência", "NBC TA 500 (R1)"), ("PT 501", "Itens específicos", "NBC TA 501"),
          ("PT 505", "Confirmações externas", "NBC TA 505"), ("PT 510", "Saldos iniciais", "NBC TA 510 (R1)"),
          ("PT 520", "Procedimentos analíticos", "NBC TA 520"), ("PT 530", "Amostragem", "NBC TA 530"),
          ("BS", "Base de dados simulada obrigatória (imobilizado)", "Instruções item 3"),
          ("PT 540", "Estimativas contábeis", "NBC TA 540 (R2)"), ("PT 550", "Partes relacionadas", "NBC TA 550"),
          ("PT 560", "Eventos subsequentes", "NBC TA 560 (R1)"), ("PT 570", "Continuidade operacional", "NBC TA 570"),
          ("PT 580", "Representações formais", "NBC TA 580 (R1)"), ("PT 600", "Auditoria de grupos", "NBC TA 600 (R2)"),
          ("CONC", "Conclusão integrada", "-"), ("A", "Anexo A - Programas de auditoria por ciclo", "NBC TA 300/330"),
          ("B", "Anexo B - Matriz de cobertura das normas", "-"), ("C", "Anexo C - Relação das fontes", "NBC TA 230/500")]


def montar() -> str:
    partes = [a.capa(), a.sumario(INDICE), a.identificacao(), a.pt_ec(), a.pt200(), a.pt210(), a.pt220(), a.pt230(), a.pt240(),
              a.pt250(), a.pt260(), a.pt265(), a.pt300(), a.pt315(), a.pt320(), b.pt330(), b.pt402(), b.pt450(), b.pt500(),
              b.pt501(), b.pt505(), b.pt510(), b.pt520(), b.pt530(), b.secao_base(), b.pt540(), b.pt550(), b.pt560(), b.pt570(),
              b.pt580(), b.pt600(), b.conclusao(), b.anexo_programas(), b.anexo_cobertura(), b.anexo_fontes()]
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Dossiê de Auditoria PRIO S.A. 2025</title>
<style>{CSS}</style></head><body>{''.join(partes)}</body></html>"""


def navegador() -> str | None:
    for n in NAVEGADORES:
        if Path(n).exists() or shutil.which(n):
            return n if Path(n).exists() else shutil.which(n)
    return None


def main() -> None:
    html_path = DOSSIE / "Dossie_Auditoria_PRIO_2025.html"
    html_path.write_text(montar(), encoding="utf-8")
    print("HTML:", html_path)
    nav = navegador()
    if not nav:
        print("Navegador Chromium não encontrado - abra o HTML e imprima em PDF manualmente.")
        return
    pdf = DOSSIE / "Dossie_Auditoria_PRIO_2025.pdf"
    cmd = [nav, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--print-to-pdf-no-header",
           f"--print-to-pdf={pdf}", "--virtual-time-budget=15000", html_path.as_uri()]
    subprocess.run(cmd, check=True, timeout=300, capture_output=True)
    print("PDF:", pdf, f"{pdf.stat().st_size/1e6:.1f} MB")


if __name__ == "__main__":
    main()
