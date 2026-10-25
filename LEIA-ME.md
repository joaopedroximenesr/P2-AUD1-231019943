# Dossiê de Auditoria - PRIO S.A. - Exercício 2025

**Universidade de Brasília (UnB)** · Auditoria 1 · CCA0024 · Turma 02 · 2026.2
**Prof. Lucas Oliveira Gomes Ferreira** · Avaliação P2 · Trabalho individual
**Identificação: Matrícula 231019943** · Versão 1.0 · 23/10/2026

**Companhia:** PRIO S.A. (antiga Petro Rio S.A.) · CNPJ 10.629.105/0001-68 · Código CVM 022187 · B3: PRIO3 (Novo Mercado)
**Objeto:** demonstrações contábeis individuais e consolidadas de 31/12/2025, com comparativos de 2024, notas explicativas e relatório do auditor independente (KPMG, 10/03/2026)

> Trabalho acadêmico. Não constitui opinião profissional de auditoria. Nenhuma empresa, auditor, cliente ou fornecedor foi contatado.
> A base de imobilizado é **sintética** (gerada para fins didáticos) e não representa registros reais da companhia.

---

## Onde está cada item exigido (item 6 das instruções)

| # | Exigência do professor | Pasta / arquivo |
|:-:|---|---|
| 1 | **Dossiê em PDF**: papéis de trabalho organizados e com referências cruzadas | `01_Dossie/Dossie_Auditoria_PRIO_2025.pdf` |
| 2 | **Base simulada** com ≥ 500.000 linhas + dicionário de variáveis | `02_Base_Simulada/base_imobilizado_sintetica.csv.gz` (518.405 linhas) · `dicionario_variaveis.csv` |
| 3 | **Planilhas editáveis**: materialidade, amostras, analíticos e conciliações | `03_Planilhas/` (7 arquivos Excel com fórmulas) |
| 4 | **Matriz de cobertura das normas** | `04_Matriz_Normas_e_Fontes/matriz_cobertura_normas.md` (também no Anexo B do dossiê) |
| 5 | **Relação das fontes** com documentos e links | `04_Matriz_Normas_e_Fontes/fontes.md` (também no Anexo C do dossiê) |
| 6 | **Código de geração e análise** (base, testes e resultados) | `05_Codigo/` |
| 7 | **Registro de erros inseridos x exceções identificadas** | `02_Base_Simulada/registro_erros_inseridos.csv` · `06_Resultados/PT450_inseridos_x_detectados.csv` |
| 8 | **Leia-me** com identificação, organização e reprodução | este arquivo |

Material de apoio: `06_Resultados/` (saídas de todos os testes, em CSV/JSON) e `07_Dados_Publicos/` (extratos da CVM, do BCB e da EIA usados no trabalho).

---

## Roteiro de leitura sugerido

1. **Dossiê (PDF)**: capa → índice clicável → identificação da companhia → PT EC a PT 600 → base simulada (BS) → conclusão integrada → Anexos A (programas por ciclo), B (matriz) e C (fontes).
2. Em cada papel de trabalho, os procedimentos vêm identificados por cor:
   - 🟢 **Realizado com evidência pública**
   - 🟡 **Planejado por falta de acesso**
   - 🔴 **Simulado para fins didáticos**
3. **Planilhas:** células amarelas são premissas editáveis; as demais são fórmulas.

### Conteúdo das planilhas (`03_Planilhas/`)

| Arquivo | Papel de trabalho |
|---|---|
| `PT320_Materialidade.xlsx` | Bases, percentuais, materialidade global, de execução, trivial e específicas |
| `PT530_Amostragem.xlsx` | MUS: parâmetros, amostra selecionada, avaliação e LSD; amostragem por atributos |
| `PT520_Analiticos.xlsx` | Expectativas, precisão e limites; decomposição da D&A; análise horizontal/vertical; Benford |
| `PT500_PT510_Conciliacoes.xlsx` | Notas x demonstrações; base simulada x NE 8; saldos iniciais 2024 |
| `PT540_PT570_Estimativas_Continuidade.xlsx` | Sensibilidade da provisão para abandono; indicadores e covenant |
| `PT450_PT600_Distorcoes_Componentes.xlsx` | Mapa de distorções; inseridos x detectados; componentes do grupo |
| `Matriz_Cobertura_e_Fontes.xlsx` | Matriz de normas e relação de fontes |

---

## Resumo dos resultados

| Tema | Resultado |
|---|---|
| Conta da base simulada | Imobilizado: R$ 31.142.804 mil, 48,5% do ativo (maior conta) |
| Materialidade | Global R$ 155 mi (1% da receita) · execução R$ 93 mi · trivial R$ 7,75 mi |
| Conciliação da base | Base sem erros = NE 8 + NE 15 centavo a centavo; diferença da base entregue (R$ 325 mi) 100% explicada pelos erros inseridos |
| Testes em 100% da base | 655 de 655 erros inseridos identificados (10 tipologias) |
| Amostragem (MUS, 95%) | LSD de R$ 535 mi antes dos ajustes (saldo rejeitado) e R$ 78 mi depois (aceito) |
| Constatações com evidência pública | Diferença de R$ 43 mi na abertura das provisões cíveis (NE 30); ausência de nota de estoques; reclassificação no PL comparativo sem nota; covenant atendido apenas com EBITDA pró-forma; provisão para abandono muito sensível (+20% no custo ≈ +R$ 1,1 bi) |

---

## Como reproduzir

Requisitos: Python 3.11 ou superior, Microsoft Edge ou Google Chrome (para gerar o PDF) e acesso à internet.

```bash
pip install -r requirements.txt
python 05_Codigo/run_all.py
```

O processo baixa os dados públicos, gera a base simulada (semente fixa 231019943, resultados idênticos a cada execução), executa os testes e recria planilhas, gráficos, dossiê e documentos. Tempo aproximado: 2 minutos.

| Script | Função |
|---|---|
| `00_extrair_dados_publicos.py` | Baixa e filtra os dados da CVM (DFP 2025/2024, ITR 2026, FCA, IPE), a PTAX (BCB) e o Brent (EIA) |
| `01_gerar_base.py` | Gera a base sintética de imobilizado e insere os erros controlados |
| `02_testes_base.py` | Conciliação, testes em 100% da população, MUS, atributos, inseridos x detectados |
| `03_analiticos.py` | Reconciliações, saldos iniciais, analíticos, sensibilidade, covenants, componentes |
| `04_graficos.py` · `05_planilhas.py` · `06_dossie.py` · `07_docs.py` | Gráficos, planilhas, dossiê em PDF e documentos |

---

## Registro de versões

| Versão | Data | Descrição |
|---|---|---|
| 1.0 | 23/10/2026 | Versão entregue para avaliação P2 |
