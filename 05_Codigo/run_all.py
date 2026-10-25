"""Executa todo o pipeline na ordem: dados públicos -> base -> testes -> analíticos -> gráficos -> planilhas -> dossiê -> docs."""
import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
ETAPAS = ["00_extrair_dados_publicos.py", "01_gerar_base.py", "02_testes_base.py", "03_analiticos.py", "04_graficos.py",
          "05_planilhas.py", "06_dossie.py", "07_docs.py"]

for etapa in ETAPAS:
    print(f"\n=== {etapa} ===", flush=True)
    subprocess.run([sys.executable, str(SRC / etapa)], check=True)
print("\nPipeline concluído.")
