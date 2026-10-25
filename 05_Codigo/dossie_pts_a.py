"""Conteúdo dos papéis de trabalho - parte A (identificação, PT EC a PT 320)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notas_dfp2025 as ne  # noqa: E402
from dossie_base import br, carregar_json, csv, fig, pt, ref, tab, ul  # noqa: E402
from parametros import bases_materialidade, conta  # noqa: E402

RT = carregar_json("resumo_testes.json")
RA = carregar_json("resumo_analiticos.json")
M = RA["mercado"]
IND = RA["indicadores"]


def mil(v):
    return br(v)


def capa():
    return f"""
<div class="capa">
  <div>
    <div class="sup">UNIVERSIDADE DE BRASÍLIA - UnB &nbsp;|&nbsp; Auditoria 1 - CCA0024 - Turma 02 - 2026.2 &nbsp;|&nbsp; Prof. Lucas Oliveira Gomes Ferreira</div>
    <div class="tit">Dossiê de Auditoria<br>PRIO S.A.</div>
    <div class="sub">Demonstrações contábeis individuais e consolidadas de 31/12/2025<br>
    NBC TA Estrutura Conceitual e NBC TA 200 a 600 - avaliação P2</div>
    <div class="box">
      <b>Companhia:</b> PRIO S.A. (antiga Petro Rio S.A. e HRT Participações em Petróleo S.A.) - CNPJ 10.629.105/0001-68 - Código CVM 022187 - B3: PRIO3 (Novo Mercado)<br>
      <b>Exercício examinado:</b> 2025, com comparativos de 2024 &nbsp;|&nbsp; <b>Data-base:</b> 31/12/2025<br>
      <b>Preparador:</b> Matrícula 231019943 &nbsp;|&nbsp; <b>Data de preparação:</b> 23/10/2026 &nbsp;|&nbsp; <b>Data de corte da pesquisa:</b> 23/10/2026<br>
      <b>Moeda:</b> R$ mil, salvo indicação (base simulada em R$)
    </div>
  </div>
  <div class="aviso">
    <b>Natureza do documento.</b> Trabalho acadêmico individual. Não constitui opinião profissional de auditoria independente, não foi
    emitido por firma de auditoria e não substitui o relatório da KPMG Auditores Independentes Ltda. de 10/03/2026. Nenhuma empresa,
    auditor, cliente ou fornecedor foi contatado. Confirmações, entrevistas, inspeções físicas e acessos a sistemas <b>não</b> foram
    realizados; aparecem apenas como procedimentos <i>planejados</i> ou <i>simulados</i>, sempre identificados. Os dados da base de
    imobilizado ({br(RT['base_linhas'])} registros) são <b>sintéticos</b>, gerados para fins didáticos, e não são registros reais da companhia.
  </div>
</div>"""


def sumario(itens):
    linhas = [[f'<a href="#{c.replace(" ", "")}">{c}</a>', t, n] for c, t, n in itens]
    return f"""<section class="sec" id="SUM"><h1>Índice do dossiê</h1>
<p>Convenção de códigos e de referências cruzadas em {ref('PT 230')}. Cada papel de trabalho segue a estrutura mínima exigida:
código, título, norma e itens; objetivo e conta; afirmações e riscos; população, fontes e critérios; procedimentos com classificação;
evidências e referências cruzadas; resultados, exceções, conclusão e limitações; preparador e campo de revisão.</p>
<p class="legend"><span class="badge b-r">Realizado com evidência pública</span> <span class="badge b-p">Planejado por falta de acesso</span>
<span class="badge b-s">Simulado para fins didáticos</span></p>
{tab(['Código', 'Papel de trabalho', 'Norma'], linhas, cls='toc', larg=['12%', '58%', '30%'])}</section>"""


def identificacao():
    dre = [("Receita líquida", "3.01"), ("Resultado bruto", "3.03"), ("EBIT", "3.05"), ("Resultado financeiro", "3.06"),
           ("Resultado antes dos tributos", "3.07"), ("IR e CS (diferido positivo)", "3.08"), ("Lucro líquido", "3.11")]
    bp = [("Ativo total", "BPA", "1"), ("Ativo circulante", "BPA", "1.01"), ("Imobilizado", "BPA", "1.02.03"),
          ("Intangível", "BPA", "1.02.04"), ("IR/CS diferido ativo", "BPA", "1.02.01.07"), ("Passivo circulante", "BPP", "2.01"),
          ("Empréstimos, debêntures e arrendamentos (circ. + não circ.)", None, None), ("Provisão para abandono", "BPP", "2.02.04.02.03"),
          ("Patrimônio líquido", "BPP", "2.03")]
    linhas_bp = []
    for nome, d, c in bp:
        if d is None:
            v25 = conta("BPP", "2.01.04") + conta("BPP", "2.02.01")
            v24 = conta("BPP", "2.01.04", "PENÚLTIMO") + conta("BPP", "2.02.01", "PENÚLTIMO")
        else:
            v25, v24 = conta(d, c), conta(d, c, "PENÚLTIMO")
        linhas_bp.append([nome, mil(v24), mil(v25), br((v25 - v24) / abs(v24), 1, pct=True) if v24 else "-"])
    linhas_dre = []
    for nome, c in dre:
        v25, v24 = conta("DRE", c), conta("DRE", c, "PENÚLTIMO")
        linhas_dre.append([nome, mil(v24), mil(v25), br((v25 - v24) / abs(v24), 1, pct=True) if v24 else "-"])
    kp = f"""<div class="kpis">
<div class="kpi"><div class="v">R$ {br(conta('DRE','3.01')/1e6,2)} bi</div><div class="l">Receita líquida 2025 (+{br(conta('DRE','3.01')/conta('DRE','3.01','PENÚLTIMO')-1,1,pct=True)})</div></div>
<div class="kpi"><div class="v">R$ {br(conta('DRE','3.11')/1e6,2)} bi</div><div class="l">Lucro líquido 2025 (2024: R$ {br(conta('DRE','3.11','PENÚLTIMO')/1e6,2)} bi)</div></div>
<div class="kpi"><div class="v">R$ {br(IND['ebitda_aj']/1e6,2)} bi</div><div class="l">EBITDA ajustado recalculado (margem {br(IND['ebitda_aj']/conta('DRE','3.01'),1,pct=True)})</div></div>
<div class="kpi"><div class="v">{br(IND['alavancagem'],2)}x</div><div class="l">Dívida líquida / EBITDA aj. sem pró-forma (covenant 2,5x)</div></div>
<div class="kpi"><div class="v">106,4 mil bpd</div><div class="l">Produção média 2025 (recorde; RA p. 27)</div></div>
<div class="kpi"><div class="v">US$ {br(M['brent_medio_2025'],2)}</div><div class="l">Brent médio 2025 (2024: US$ {br(M['brent_medio_2024'],2)}; EIA)</div></div>
<div class="kpi"><div class="v">R$ {br(M['ptax_media_2025'],4)}</div><div class="l">PTAX média 2025 (fim: {br(M['ptax_fim_2025'],4)}; BCB)</div></div>
<div class="kpi"><div class="v">757,3 MMbbl</div><div class="l">Reservas 1P D&M em 01/01/2026 (811,3 com +20% Peregrino)</div></div></div>"""
    return f"""<section class="sec" id="ID"><h1>Identificação da companhia e visão financeira</h1>
<h3>Identidade, alterações de nome empresarial e de código de negociação</h3>
{tab(['Atributo', 'Informação verificada', 'Fonte'], [
        ['Denominação atual', 'PRIO S.A. desde 12/05/2023', 'FCA 2026 (CVM), campo Data_Nome_Empresarial'],
        ['Denominação anterior', 'PETRO RIO S.A. (renomeada PRIO S.A. em 12/05/2023)', 'FCA 2026, campo Nome_Empresarial_Anterior'],
        ['Denominação de origem', 'HRT Participações em Petróleo S.A. (ex-controladora da HRT Walvis, Namíbia - NE 2.3)', 'NE 2.3 da DFP 2025 (subsidiárias "HRT Walvis"); histórico corporativo - ver nota abaixo'],
        ['Código de negociação', 'PRIO3 - ações ordinárias, B3, Novo Mercado; início de negociação/listagem registrado em 25/10/2010', 'FCA 2026, item valor mobiliário'],
        ['CNPJ / Código CVM', '10.629.105/0001-68 / 022187 (registro CVM 21/10/2010, categoria A)', 'FCA 2026'],
        ['Data de constituição', 'FCA: 13/10/2008 | NE 1: "constituída em 17 de julho de 2009" - <b>divergência</b>', 'FCA 2026 x DFP 2025 p. 43'],
        ['Atividade', 'Exploração e produção (E&P) de petróleo e gás natural, Bacia de Campos; holding operacional', 'NE 1 (p. 43)'],
        ['Auditor 2025', 'KPMG Auditores Independentes Ltda. (desde 2025) - opinião sem ressalva de 10/03/2026', 'DFP 2025 p. 99-102; FCA 2026'],
        ['Auditor 2020-2024', 'Ernst & Young Auditores Independentes S/S Ltda. - relatório sem modificação de 12/03/2025', 'DFP 2024 (dados abertos, pareceres)'],
        ['Moeda funcional', 'Dólar norte-americano (todas as entidades); apresentação em reais', 'NE 2.4 (p. 47-48)'],
    ], larg=['20%', '50%', '30%'])}
<div class="note"><b>Nota de ceticismo sobre a identidade.</b> A companhia atribuída foi mantida durante todo o trabalho (mesmo CNPJ e código CVM).
O FCA registra o código PRIO3 com início em 25/10/2010, data da listagem original; a negociação sob o código HRTP3 no período HRT
(2010-2015) é informação histórica que <b>não</b> consta dos documentos primários consultados e, por isso, é registrada apenas como
referência a confirmar no histórico de códigos da B3. A divergência sobre a data de constituição (FCA x NE 1) foi levada ao {ref('PT 265')}.</div>
<h3>Indicadores-chave (dados reais públicos)</h3>{kp}
<h3>Balanço patrimonial consolidado resumido (R$ mil) - CVM Dados Abertos (F02), DFP p. 12-16</h3>
{tab(['Conta', '31/12/2024', '31/12/2025', 'Var.'], linhas_bp, num_cols=(1, 2, 3))}
<h3>Demonstração do resultado consolidada resumida (R$ mil) - DFP p. 17-18</h3>
{tab(['Conta', '2024', '2025', 'Var.'], linhas_dre, num_cols=(1, 2, 3))}
{fig('g01_composicao_ativo.png', 'Figura 1 - Composição do ativo em 31/12/2025. O imobilizado (48,5%) é a conta de maior materialidade e é a base simulada obrigatória (PT 530).')}
{fig('g03_receita_campos.png', 'Figura 2 - Receita líquida por campo (NE 22, p. 89). Peregrino, adquirido em etapas (dez/2024 e nov/2025), passa a ser o maior campo.')}
<h3>Leitura do exercício</h3>
<p>Em 2025 a PRIO aumentou a produção em 27% (recorde de 106,4 mil bpd), principalmente pelas aquisições em Peregrino: 40% via
combinação de negócios Stellina (dez/2024) e mais 40%, com a operação, comprados da Equinor em 11/11/2025 por US$ 1.564 milhões no
fechamento (NE 9.d). Mesmo com o Brent médio 14,1% menor (US$ 69,14 contra US$ 80,52), a receita cresceu 8,5%. O lucro líquido caiu 78%,
para R$ 2,25 bi, por três motivos: depreciação, amortização e exaustão 135% maior (Peregrino a valor justo); resultado financeiro de
R$ -2,04 bi (dívida bruta de R$ 27,1 bi); e um crédito de IR diferido menor do que o de 2024, quando foi reconhecido o prejuízo
fiscal da Forte. O LAIR foi <b>negativo</b> (R$ -232,6 mi) e o lucro só é positivo por causa do IR diferido (R$ +2,9 bi), ponto que
orienta materialidade, fraude e estimativas ({ref('PT 320')}, {ref('PT 240')}, {ref('PT 540')}).</p>
</section>"""


def pt_ec():
    corpo = tab(["Elemento (NBC TA EC)", "Aplicação ao trabalho sobre a PRIO"], [
        ["Relacionamento de três partes", "Auditor independente (no caso real, KPMG; aqui, o aluno em caráter didático); parte responsável = administração da PRIO S.A. (Diretoria e Conselho de Administração); usuários previstos."],
        ["Usuários previstos", "Acionistas (capital pulverizado: FMR 5%, Schroder 5%, BlackRock 7,5% em abr/2026), detentores de bonds 2030 (US$ 700 mi) e de debêntures locais (R$ 9,9 bi), 12 bancos credores sujeitos a covenant de 2,5x, ANP (royalties/PE), CVM, B3, Receita Federal e parceiros de JOA (Repsol Sinopec, Equinor)."],
        ["Objeto", "Demonstrações contábeis individuais e consolidadas de 31/12/2025 (BP, DRE, DRA, DMPL, DFC, DVA como informação suplementar) e notas explicativas."],
        ["Critérios", "Práticas contábeis adotadas no Brasil (Lei 6.404/1976, pronunciamentos CPC aprovados pela CVM) e IFRS Accounting Standards (NE 2.1). Critérios adequados: relevantes, completos, confiáveis, neutros e compreensíveis."],
        ["Evidência", "No caso real: inspeção, observação, confirmação, recálculo, reexecução, procedimentos analíticos e indagação. Neste dossiê: somente documentos públicos (CVM, B3, RI) e uma base sintética (ver PT 500)."],
        ["Relatório", "Opinião em forma positiva (\"apresentam adequadamente, em todos os aspectos relevantes\") - modelo NBC TA 700/701 com PAA. Este dossiê não emite opinião."],
        ["Nível de asseguração", "Razoável (alto, mas não absoluto) - auditoria. Contraste: limitada na revisão das ITR (NBC TR 2410) e na asseguração do inventário de GEE contratada pela PRIO com a KPMG (Relatório do Comitê de Auditoria, DFP p. 104-106)."],
    ], larg=["24%", "76%"])
    corpo += "<h3>Auditoria x outros trabalhos de asseguração e serviços correlatos</h3>" + tab(
        ["Trabalho", "Norma", "Asseguração", "Forma da conclusão", "Exemplo na PRIO"], [
            ["Auditoria de demonstrações contábeis", "NBC TA 200-810", "Razoável", "Positiva (opinião)", "DFP 2025 - KPMG, 10/03/2026"],
            ["Revisão de informações intermediárias", "NBC TR 2410", "Limitada", "Negativa (\"nada chegou ao nosso conhecimento\")", "ITR 1T26 e 2T26 (F05)"],
            ["Asseguração de informação não histórica", "NBC TO 3000 / 3410", "Limitada ou razoável", "Conforme o trabalho", "Inventário de GEE 2024 e 2025 (KPMG)"],
            ["Procedimentos previamente acordados", "NBC TSC 4400", "Nenhuma", "Relato de constatações", "Ex.: certificação de covenants para credores (hipótese)"],
            ["Compilação", "NBC TSC 4410", "Nenhuma", "Relatório de compilação", "Não aplicável a companhia aberta"],
            ["Este dossiê acadêmico", "Instruções P2", "Nenhuma", "Conclusão integrada sem opinião", "-"],
        ], larg=["24%", "14%", "12%", "24%", "26%"])
    return pt("PT EC", "Estrutura conceitual - caracterização do trabalho", "NBC TA Estrutura Conceitual para Trabalhos de Asseguração (DOU 25/11/2015), itens 5-11, 20-60",
              "Caracterizar o trabalho, os usuários, o objeto, os critérios, as responsabilidades, a evidência e o nível de asseguração, e distinguir auditoria de outros trabalhos.",
              "Demonstrações contábeis individuais e consolidadas da PRIO S.A. em 31/12/2025.",
              "Todas as afirmações ao nível das demonstrações como um todo (NBC TA 315 A190).",
              "Usar critérios inadequados; confundir o nível de asseguração; usuários com interesses diversos (credores sensíveis a covenants e acionistas a lucro e reservas).",
              "DFP 2025 (F01), FCA 2026 (F06) e relatório do Comitê de Auditoria (DFP p. 104-106). Critério: identificar cada elemento da estrutura conceitual na documentação pública.",
              [("Identificar parte responsável, usuários previstos e objeto com base na DFP e no FCA", "R", "F01, F06"),
               ("Avaliar a adequação dos critérios (CPC/IFRS) - declaração de conformidade NE 2.1", "R", "NE 2.1, p. 46"),
               ("Comparar o relatório da KPMG (razoável) com as revisões de ITR (limitada) e o serviço de GEE", "R", "p. 99-106; F05"),
               ("Confirmar com a administração os usuários e o uso pretendido do relatório", "P", "Requer acesso à administração")],
              ul([f"Relatório do auditor (p. 99-102): opinião sem ressalva, PAA = ARO e IR diferido → {ref('PT 540')}",
                  f"Comitê de Auditoria: contratação da KPMG em 09/04/2025 e serviços de GEE → {ref('PT 220')}, {ref('PT 200')}"]),
              corpo and "<p>Todos os elementos de um trabalho de asseguração razoável estão presentes no caso real. O objeto é auditável e os critérios são adequados e estão disponíveis aos usuários (publicados por CPC e IASB).</p>",
              "O trabalho real é uma auditoria (asseguração razoável) de propósito geral. Este dossiê reproduz o raciocínio do auditor sem asseguração, o que é coerente com a limitação de acesso.",
              "Sem acesso à carta de contratação real e à documentação do auditor.", corpo)


def pt200():
    corpo = "<h3>Modelo de risco de auditoria aplicado</h3>" + tab(
        ["Componente", "Avaliação PRIO 2025", "Justificativa"], [
            ["Risco inerente (RI)", "Alto em imobilizado/estimativas; moderado em caixa", "Aquisições complexas, UOP dependente de reservas, ARO de longo prazo, moeda funcional USD, IR diferido de R$ 8,1 bi"],
            ["Risco de controle (RC)", "Moderado (não testado - premissa)", "Companhia do Novo Mercado com Comitê de Auditoria, auditoria interna e compliance (DFP p. 104-106); integração de Peregrino em nov/2025 aumenta o RC no 4T"],
            ["Risco de distorção relevante (RDR = RI x RC)", "Alto nas áreas significativas", "Ver matriz no PT 315"],
            ["Risco de detecção (RD)", "Baixo nas áreas significativas", "Resposta: testes substantivos extensos e especialistas (PT 330)"],
            ["Risco de auditoria (RA)", "Aceitavelmente baixo", "Segurança razoável (item 5)"],
        ], larg=["22%", "28%", "50%"])
    corpo += "<h3>Ceticismo profissional - situações reais identificadas nas fontes públicas</h3>" + ul([
        "NE 30: a abertura das provisões cíveis (352.598 + 221.458 + 25.111) não fecha com o BP (642.170). Diferença de R$ 43.003 mil, sendo que 2024 fechava → " + ref("PT 450"),
        "Não há nota explicativa específica para Estoques (R$ 3,11 bi, +158%) → " + ref("PT 501"),
        "Lucro líquido positivo apesar de LAIR negativo, sustentado por IR diferido (R$ +2,9 bi), uma estimativa sensível → " + ref("PT 540"),
        "Alavancagem recalculada de 2,91x (sem pró-forma), acima do covenant de 2,5x; o atendimento depende do EBITDA pró-forma de Peregrino → " + ref("PT 570"),
        "Data de constituição divergente (FCA 13/10/2008 x NE 1 17/07/2009) e responsável técnico no FCA diferente do sócio signatário → " + ref("PT 265"),
        "Reclassificação de R$ 29.885 mil no PL comparativo, sem nota de reapresentação → " + ref("PT 510"),
        "Diferença de R$ 151.210 mil entre D&A da DFC e as movimentações das notas → " + ref("PT 520"),
    ])
    return pt("PT 200", "Objetivos gerais, ética, independência, ceticismo e risco de auditoria",
              "NBC TA 200 (R1) itens 3-24, A20-A57; NBC PG 01 (Código de Ética); NBC PA 400 (independência)",
              "Documentar ética, independência, ceticismo, julgamento profissional, risco de auditoria e condições para obter segurança razoável.",
              "Trabalho como um todo.", "Todas.",
              "Ameaças de interesse próprio e de autorrevisão por serviços não relacionados à auditoria; viés de confirmação diante de narrativa de crescimento.",
              "Relatório do Comitê de Auditoria (serviços da KPMG: GEE e KPMG LLP), FCA (auditor), DFP. Critério: todas as fontes que afetam ética e risco.",
              [("Avaliar a independência: serviços de asseguração de GEE (2024 e 2025) e serviços da KPMG LLP aprovados pelo Comitê em 27/10/2025", "R", "DFP p. 104-106"),
               ("Declaração de independência da equipe e da rede KPMG", "P", "Documento interno da firma"),
               ("Aplicar ceticismo: cruzar notas x demonstrações x FCA x fatos relevantes", "R", "PT 500, PT 450"),
               ("Documentar julgamentos relevantes: base de materialidade, componentes, estimativa selecionada", "R", "PT 320, PT 600, PT 540"),
               ("Avaliar limitações inerentes: estimativas de reservas, fraude com conluio", "R", "PT 240, PT 540")],
              ul([f"Independência: o Comitê concluiu que os serviços não comprometem a objetividade, e o auditor deve fazer avaliação própria (NBC PA 400) → {ref('PT 220')}",
                  f"Segurança razoável depende de evidência suficiente e apropriada → {ref('PT 500')}"]),
              corpo and "<p>Nenhuma ameaça impeditiva foi identificada nas fontes públicas. Os serviços de GEE são asseguração (não geram autorrevisão das DFs), mas devem constar do PT de independência. Sete situações de ceticismo foram registradas e encaminhadas.</p>",
              "As condições para segurança razoável existem no caso real: critérios adequados, administração que reconhece suas responsabilidades e acesso a evidências. Neste dossiê, a segurança obtida é apenas didática.",
              "Não houve indagação à equipe nem às salvaguardas da firma; o risco de controle não foi testado (premissa moderada).", corpo)


def pt210():
    carta = """<div class="letter"><div class="wm">MINUTA DIDÁTICA - NÃO ENVIADA - SEM VALIDADE JURÍDICA - NÃO REPRESENTA DOCUMENTO DA KPMG OU DA PRIO</div>
<p><b>Ao Conselho de Administração e ao Comitê de Auditoria da PRIO S.A.</b> - Rio de Janeiro, [data da contratação]</p>
<p><b>1. Objetivo e alcance.</b> Auditar as demonstrações contábeis individuais e consolidadas da PRIO S.A. em 31/12/2025, conforme as normas
brasileiras e internacionais de auditoria, para expressar opinião sobre se apresentam adequadamente, em todos os aspectos relevantes,
a posição patrimonial e financeira, o desempenho e os fluxos de caixa, segundo as práticas contábeis adotadas no Brasil e as IFRS.
Inclui a DVA (informação suplementar), a leitura do Relatório da Administração (NBC TA 720) e a revisão das ITR de 2025 (NBC TR 2410).</p>
<p><b>2. Responsabilidades do auditor.</b> Planejar e executar a auditoria para obter segurança razoável; manter ceticismo; comunicar
deficiências significativas, PAA e assuntos de independência à governança; manter independência (NBC PA 400 e regras da CVM).
Por limitações inerentes, há risco inevitável de que distorções relevantes não sejam detectadas.</p>
<p><b>3. Responsabilidades da administração (precondição).</b> (a) elaborar as DFs conforme CPC/IFRS; (b) manter controles internos
necessários; (c) fornecer acesso irrestrito a registros, documentos, pessoal e componentes do grupo, inclusive Lux Holding (Luxemburgo)
e PrioAustria; (d) fornecer representações formais (NBC TA 580); (e) disponibilizar laudos de especialistas: D&M (reservas) e avaliadores
de ARO e de alocação de preço de compra.</p>
<p><b>4. Estrutura do relatório.</b> Opinião; base para opinião; PAA (NBC TA 701); outros assuntos (DVA e auditoria anterior pela EY);
outras informações; responsabilidades. A forma e o conteúdo poderão mudar conforme as constatações.</p>
<p><b>5. Outros termos.</b> Equipe e especialistas (PT 220); cronograma (PT 300); honorários [não divulgados - não simular];
acesso aos papéis do auditor antecessor (NBC TA 510); auditores de componentes (NBC TA 600).</p>
<p>De acordo: ____________________ (Administração) &nbsp;&nbsp; ____________________ (Auditor) - <i>campos em branco</i></p></div>"""
    precond = tab(["Precondição (NBC TA 210 item 6)", "Avaliação", "Evidência"], [
        ["Estrutura de relatório financeiro aceitável", "Atendida - CPC/IFRS, estrutura de propósito geral prescrita por lei e pela CVM", "NE 2.1 (p. 46)"],
        ["Administração reconhece a responsabilidade pela elaboração", "Atendida (evidência indireta)", "Declaração dos Diretores, DFP p. 107-108"],
        ["Responsabilidade pelos controles internos", "Atendida (evidência indireta)", "Relatório do Comitê; auditoria interna e compliance"],
        ["Acesso irrestrito a informações e pessoas", "Não verificável publicamente → condição contratual", "Planejado"],
        ["Ausência de limitação de alcance imposta", "Nenhuma indicação; o Comitê registrou que a KPMG não reportou restrições no 2T25", "DFP p. 104"],
        ["Mudança de auditor (rodízio)", "Troca EY → KPMG aprovada pelo Comitê em 09/04/2025; comunicação com antecessor exigida", "DFP p. 104; PT 510"],
    ], larg=["34%", "44%", "22%"])
    return pt("PT 210", "Termos do trabalho - carta de contratação didática e precondições",
              "NBC TA 210 (R1) itens 6-12, A20-A28 e Apêndice 1",
              "Preparar carta de contratação didática (objetivo, alcance, responsabilidades, estrutura do relatório) e avaliar as precondições da auditoria.",
              "Aceitação do trabalho - exercício de 2025 (primeiro ano da KPMG).", "Não se aplica a afirmações específicas; diz respeito ao trabalho como um todo.",
              "Precondições ausentes; termos ambíguos sobre componentes no exterior e especialistas; risco de primeiro ano.",
              "DFP 2025, relatório do Comitê de Auditoria, FCA 2026.",
              [("Avaliar a estrutura de relatório financeiro e a declaração de conformidade", "R", "NE 2.1"),
               ("Verificar o reconhecimento de responsabilidades pela administração em documentos públicos", "R", "p. 107-108"),
               ("Redigir carta de contratação didática (anexa)", "S", "Minuta abaixo"),
               ("Obter a carta assinada e o acordo sobre honorários e acesso aos componentes", "P", "Documento contratual")],
              ul([f"Precondições → tabela abaixo; responsabilidades refletidas na minuta da carta de representações → {ref('PT 580')}",
                  f"Comunicação com o auditor antecessor → {ref('PT 510')}"]),
              precond, "As precondições verificáveis estão atendidas; o acesso irrestrito depende de cláusula contratual. A minuta contém todos os elementos do item 10 da NBC TA 210.",
              "A carta é uma minuta acadêmica; não foram simulados honorários, assinaturas nem aceite.", carta)


def pt220():
    corpo = "<h3>Plano de gestão da qualidade do trabalho</h3>" + tab(["Elemento", "Planejamento"], [
        ["Direção", "Sócio do trabalho com experiência em E&P e em IFRS 3/IFRS 11; reunião de abertura sobre riscos significativos (Peregrino, ARO, IR diferido, moeda funcional)."],
        ["Equipe (didática)", "Sócio, gerente, 2 seniores, 4 assistentes; especialistas em reservas/engenharia (ARO e UOP), avaliação/finanças corporativas (taxas de desconto, alocação de preço), tributário (IR diferido, Pillar 2) e TI (ERP, CAATs). Sem nomes - não se simulam pessoas reais."],
        ["Supervisão", "Gerente revisa 100% dos PTs de áreas significativas; sócio revisa PT 315, 320, 330, 450, 540, 570 e 600."],
        ["Revisão de qualidade do trabalho (EQR)", "Obrigatória para companhia aberta (NBC PA 02); revisor independente da equipe antes da data do relatório."],
        ["Consultas", "Departamento técnico: (i) aquisição de +40% em Peregrino como aquisição de ativos x combinação de negócios (CPC 15 item B7, teste de concentração); (ii) ARO; (iii) diferença de base tributária por moeda funcional (CPC 32 item 41)."],
        ["Recursos tecnológicos", "Ferramenta de análise de dados para 100% dos lançamentos (no dossiê, scripts Python reproduzíveis - 05_Codigo/)."],
        ["Cronograma de revisão", "Planejamento até set/2025; intermediária out-nov/2025; final jan-mar/2026 (PT 300)."],
    ], larg=["24%", "76%"])
    corpo += "<h3>Conflitos e riscos à qualidade</h3>" + tab(["Risco à qualidade", "Origem", "Resposta"], [
        ["Primeiro ano do auditor", "Troca EY → KPMG em 2025", "Mais tempo no entendimento; revisão dos papéis do antecessor (PT 510)"],
        ["Pressão de prazo", "Fechamento de Peregrino em 11/11/2025, a 50 dias do encerramento", "Procedimentos de alocação antecipados para dez/2025; especialistas reservados"],
        ["Serviços não-auditoria", "GEE (KPMG Brasil) e serviços da KPMG LLP (out/2025)", "Avaliação de ameaças e salvaguardas; pré-aprovação pelo Comitê (realizada)"],
        ["Especialização setorial", "UOP, reservas, JOA, ANP", "Especialistas internos e avaliação dos especialistas da administração (D&M) - NBC TA 500 item 8"],
        ["Componentes no exterior", "Lux Holding (Luxemburgo), PrioAustria (Áustria)", "Instruções de grupo e avaliação de auditores de componente (PT 600)"],
    ], larg=["24%", "36%", "40%"])
    return pt("PT 220", "Gestão da qualidade do trabalho", "NBC TA 220 (R3) itens 13-38, A1-A110; NBC PA 01 (R1) e NBC PA 02",
              "Planejar direção, supervisão, revisão, consultas e recursos; documentar conflitos e riscos à qualidade.",
              "Execução do trabalho de auditoria 2025.", "Não se aplica a afirmações; refere-se ao trabalho.",
              "Equipe sem competência setorial; prazo apertado após aquisições; ameaças de independência.",
              "Relatório do Comitê de Auditoria (DFP p. 104-106), NE 1 e 9.d, FCA.",
              [("Mapear riscos à qualidade decorrentes de eventos públicos (troca de auditor, Peregrino, serviços não-auditoria)", "R", "p. 104-106"),
               ("Definir composição da equipe, especialistas e plano de revisão", "S", "Tabela acima (didática)"),
               ("Documentar consultas técnicas sobre Peregrino e moeda funcional", "P", "Consulta interna da firma"),
               ("Executar EQR antes da emissão do relatório", "P", "NBC PA 02")],
              ul([f"Riscos significativos que exigem supervisão do sócio → {ref('PT 315')}", f"Cronograma → {ref('PT 300')}"]),
              corpo and "<p>Cinco riscos à qualidade foram identificados, cada um com resposta definida. Nenhum conflito impeditivo.</p>",
              "O plano de gestão da qualidade é proporcional ao risco do trabalho (alto em áreas significativas).",
              "A equipe é fictícia e didática; nenhuma revisão de terceiros foi simulada.", corpo)


def pt230():
    corpo = "<h3>Índice do arquivo e convenção de códigos</h3>" + tab(["Código", "Conteúdo", "Pasta / arquivo"], [
        ["PT EC a PT 600", "Papéis de trabalho por norma (ordem do roteiro)", "01_Dossie/Dossie_Auditoria_PRIO_2025.pdf"],
        ["BS", "Base simulada: geração, dicionário, conciliação", "02_Base_Simulada/, 05_Codigo/01_gerar_base.py"],
        ["A", "Programas de auditoria por ciclo", "Anexo A do dossiê"],
        ["B / C", "Matriz de cobertura e fontes", "04_Matriz_Normas_e_Fontes/, 03_Planilhas/Matriz_Cobertura_e_Fontes.xlsx"],
        ["R-xxx", "Resultados reproduzíveis (CSV/JSON)", "06_Resultados/"],
        ["X-xxx", "Planilhas editáveis com fórmulas", "03_Planilhas/"],
    ], larg=["14%", "46%", "40%"])
    corpo += "<h3>Referências cruzadas e marcas</h3>" + tab(["Marca", "Significado"], [
        ["→ PT 320", "Remete ao papel de trabalho citado (link clicável no PDF)"],
        ["F01...F17", "Fonte pública na relação de fontes (Anexo C), com URL, data de acesso, página e exercício"],
        ["NE x, p. y", "Nota explicativa x, \"PÁGINA y de 108\" da DFP 2025 (CVM)"],
        ["✓ / Σ / ⓡ", "Conferido com documento / somado / reconciliado (aplicado nas planilhas)"],
        ["[DADOS SINTÉTICOS]", "Informação gerada pela base simulada - nunca representa registro real"],
    ], larg=["20%", "80%"])
    corpo += "<h3>Controle de versões, montagem e guarda</h3>" + ul([
        "Controle de versões: a versão entregue é a v1.0 (23/10/2026); cada arquivo gerado traz data e preparador; alterações posteriores devem ser registradas no LEIA-ME com data, motivo e responsável, sem sobrescrever a versão entregue.",
        "Reprodutibilidade: <code>python 05_Codigo/run_all.py</code> regenera dados públicos, base, testes, planilhas, gráficos e este PDF. A semente aleatória 231019943 garante resultados idênticos.",
        "Montagem do arquivo final: até 60 dias após a data do relatório (NBC TA 230 item 14 e A21). Depois disso, nada é excluído; adições são datadas e justificadas (item 16).",
        "Guarda: mínimo de 5 anos (NBC TA 230 A23 e regulamentação CVM aplicável a auditores), com acesso restrito; no trabalho acadêmico, a pasta entregue e o registro de versões formam a trilha de auditoria.",
        "Dados brutos baixados (zip CVM) ficam em <code>07_Dados_Publicos/brutos/</code>, não acompanham a entrega e são reobtidos pelo script 00.",
    ])
    return pt("PT 230", "Documentação de auditoria", "NBC TA 230 (R1) itens 7-16, A1-A24",
              "Criar índice, convenção de códigos, referências cruzadas, controle de versões e procedimentos de montagem e guarda do arquivo.",
              "Arquivo de auditoria (pastas 01 a 07 desta entrega).", "Não se aplica.",
              "Documentação insuficiente para que um auditor experiente entenda o trabalho; perda de rastreabilidade; alteração posterior não registrada.",
              "Estrutura de pastas da entrega e scripts.",
              [("Definir índice e convenção de códigos", "R", "Tabela acima"), ("Implantar referências cruzadas clicáveis no PDF", "R", "Todo o dossiê"),
               ("Registrar a versão entregue e as regras de alteração", "R", "LEIA-ME"),
               ("Fechar o arquivo em 60 dias e bloquear alterações", "P", "Procedimento da firma")],
              ul([f"Índice geral → {ref('SUM')}", "LEIA-ME.md (organização e instruções de reprodução)"]),
              corpo and "<p>O arquivo atende ao teste do \"auditor experiente\" (item 8): cada conclusão aponta a fonte (Fxx), a página e o script que a reproduz.</p>",
              "A documentação está organizada, rastreável e reproduzível.", "A guarda de 5 anos não é aplicável a um trabalho acadêmico; foi descrita como seria feita no caso real.", corpo)


def pt240():
    corpo = "<h3>Fatores de risco de fraude (triângulo) - PRIO 2025</h3>" + tab(["Fator", "Indício observado em fonte pública", "Fonte"], [
        ["Incentivo/pressão", "Covenant de 2,5x dívida líquida/EBITDA em 12 contratos e nas debêntures; recálculo sem pró-forma de 2,91x", "NE 13-14 (p. 77, 79); PT 570"],
        ["Incentivo/pressão", "Remuneração variável relevante: 84% da remuneração da administração é baseada em ações (R$ 29.376 de 34.932 mil)", "NE 21 (p. 88)"],
        ["Incentivo/pressão", "LAIR negativo; lucro dependente de IR diferido; meta pública de política de dividendos em 2026", "DRE; RA p. 27"],
        ["Oportunidade", "Estimativas complexas (ARO, UOP/reservas, alocação de preço de Peregrino, IR diferido por moeda funcional)", "NE 8, 9, 16, 17"],
        ["Oportunidade", "Trading de óleo de terceiros (R$ 1,75 bi) e vendas no fim do ano (BP: R$ 542 mi a receber de vendas de dez/2025)", "NE 4, 22"],
        ["Oportunidade", "Capitalização de gastos: R$ 874,6 mi de materiais capitalizados levados a CPV em 2025 (\"reparos de emergência\")", "NE 8 (p. 68)"],
        ["Oportunidade", "Integração de Peregrino (operação assumida em 11/11/2025) e JOA com cash calls/billing statements", "NE 1, 2.11"],
        ["Atitude/racionalização", "Nenhum indício público (sem histórico de reapresentação); ambiente de governança do Novo Mercado; canal de integridade reformulado em 2025", "DFP p. 104-106"],
    ], larg=["16%", "62%", "22%"])
    corpo += "<h3>Testes de lançamentos contábeis (burla de controles) - aplicados à base sintética</h3>" + tab(
        ["Critério de seleção (100% da população)", "Itens sinalizados", "Resultado [SIMULADO]"], [
            ["Valor redondo ≥ R$ 1 mi + fim de semana + usuário genérico + documento AJ- + sem fornecedor (score ≥ 3)", "25", "25 lançamentos fictícios de OPEX capitalizado (R$ 282 mi) - todos detectados"],
            ["Lançador = aprovador", "175", "150 inseridos (E07) + 25 do usuário USR_TEMP"],
            ["Valor > R$ 5 mi aprovado por gerente", "82", "60 inseridos (E08) + 22 entre os itens E09/duplicatas"],
            ["Benford - 1º dígito do custo", "MAD " + br(csv('PT520_benford_custo.csv')['desvio_abs'].mean(), 4), "Conformidade próxima; sem desvio sistemático"],
        ], larg=["50%", "14%", "36%"])
    return pt("PT 240", "Fraude - avaliação de riscos e respostas", "NBC TA 240 (R1) itens 16-44, A1-A50 (versão vigente para 2025; a (R2) publicada no DOU de 25/09/2026 foi consultada e não aplicada)",
              "Avaliar fatores de risco de fraude, inclusive reconhecimento de receita e burla de controles pela administração; planejar testes de lançamentos e respostas.",
              "Receita (venda de óleo próprio e trading); imobilizado (capitalização); estimativas; lançamentos manuais.",
              "Ocorrência e corte (receita); existência e classificação CAPEX/OPEX (imobilizado); avaliação (estimativas).",
              "<b>Riscos significativos de fraude:</b> (1) receita - corte de cargas em dez/2025 e trading (presunção do item 26, não refutada); (2) burla de controles pela administração (item 31, sempre presente); (3) capitalização indevida de OPEX para melhorar o EBITDA do covenant.",
              "DFP 2025; base sintética (518.405 registros) para os testes de lançamentos. Critério: todos os lançamentos com características de risco.",
              [("Discussão da equipe (brainstorming) sobre onde as DFs são suscetíveis a fraude", "S", "Fatores acima"),
               ("Indagar administração, Comitê de Auditoria e auditoria interna sobre fraudes conhecidas ou suspeitas", "P", "Sem acesso"),
               ("Analisar receita por campo/mês x volumes ANP e preços Brent (analítico)", "R", "PT 520"),
               ("Testar corte: cargas embarcadas de 20/12/2025 a 10/01/2026 (B/L x fatura x data de transferência de controle)", "P", "Documentos de embarque"),
               ("Testar lançamentos manuais e de fim de período por critérios de risco em 100% da população", "S", "PT 330 T07-T09"),
               ("Revisar estimativas para viés da administração (ARO, IR diferido, UOP)", "R", "PT 540"),
               ("Avaliar a razão de negócio de transações fora do curso normal: acordo do FPSO Polvo (R$ -142,9 mi), perda pela parada de Peregrino (R$ -194,8 mi)", "R", "NE 25 (p. 90)")],
              ul([f"Testes de lançamentos → {ref('PT 330')}; projeção → {ref('PT 530')}; comunicação → {ref('PT 260')}",
                  "06_Resultados/PT450_inseridos_x_detectados.csv"]),
              corpo and "<p>Nas fontes públicas não foi identificado indício de fraude real. Na simulação, os 25 lançamentos fraudulentos inseridos (R$ 282 mi, acima da MG) foram 100% detectados pelos critérios de risco. Se fosse um caso real, a matéria seria comunicada ao Comitê de Auditoria (item 40) e avaliada quanto a outros efeitos (item 36).</p>",
              "Os riscos presumidos de receita e de burla de controles se mantêm significativos; as respostas planejadas e simuladas são adequadas. Não há evidência pública de fraude.",
              "Indagações, testes de corte com documentos de embarque e acesso ao diário contábil real não foram possíveis.", corpo)


def pt250():
    corpo = "<h3>Mapa de obrigações legais e regulatórias relevantes</h3>" + tab(
        ["Norma/regulador", "Obrigação", "Efeito nas DFs", "Indício / risco 2025"], [
            ["Lei 9.478/1997 e Decreto 2.705/1998 (ANP)", "Royalties (até 10%) e participação especial", "CPV R$ 1.533.652 mil (NE 23); a pagar R$ 225.851 mil (NE 12)", "Analítico de royalties dentro da precisão (PT 520)"],
            ["Contratos de concessão ANP - conteúdo local", "Percentuais mínimos de conteúdo local", "Provisão provável de R$ 224.872 mil (multas, Prio Forte)", "Indício de descumprimento já provisionado (NE 30)"],
            ["ANP - segurança operacional (SGSO)", "Gestão de segurança de instalações", "Perda pela parada de Peregrino de R$ 194.765 mil (NE 25)", "<b>Interdição do FPSO Peregrino pela ANP (ago/2025)</b>, retomada em 17/10/2025 (NE 1)"],
            ["IBAMA - licenciamento ambiental", "LP/LI/LO; Foz do Amazonas", "Capitalização de Wahoo (R$ 6,57 bi em andamento)", "LO de Wahoo emitida em 03/03/2026; blocos da Foz suspensos desde 2023"],
            ["Lei 6.404/1976 e Resoluções CVM 80/2022 e 44/2021", "Elaboração, divulgação e fatos relevantes", "DFP, fatos relevantes", "Inconsistências de divulgação (PT 450)"],
            ["Tributária: IRPJ/CSLL, PIS/COFINS, ICMS, IRRF; Pillar 2 (Lei 15.079/2024); Reforma Tributária (EC 132/2023, LC 214/2025)", "Apuração e recolhimento", "IR diferido R$ 8,1 bi; contingências fiscais possíveis R$ 1,43 bi", "Autos de IRRF (R$ 346,5 mi possível; R$ 91,5 mi provável)"],
            ["Lei 12.846/2013 (anticorrupção)", "Programa de integridade", "Passivos contingentes", "Sem indício; programa revisado em 2025 (DFP p. 105)"],
            ["Ambiental/cível - pesca", "Responsabilidade por danos", "Possíveis: R$ 1,31 bi (zona de exclusão de Frade) e R$ 451,6 mi (FEPERJ)", "Litígios relevantes não provisionados (PT 501)"],
            ["Trabalhista/NR (NR-1, NR-37)", "Saúde e segurança offshore", "Provisões trabalhistas R$ 23.455 mil", "Baixo"],
        ], larg=["24%", "20%", "28%", "28%"])
    return pt("PT 250", "Leis e regulamentos", "NBC TA 250 itens 12-30, A6-A26",
              "Mapear obrigações relevantes e riscos de descumprimento; definir procedimentos e comunicações diante de indícios.",
              "Provisões, contingências, royalties, tributos, licenças (premissa de continuidade de campos).",
              "Completude e avaliação de provisões; divulgação de passivos contingentes; ocorrência de multas.",
              "Descumprimento regulatório (ANP/IBAMA) com efeito direto (multas, royalties) ou indireto (interdição, perda de licença).",
              "NE 1, 12, 23, 25, 30; fatos relevantes de 2026. Critério: leis com efeito direto nos valores ou fundamentais para a operação.",
              [("Mapear leis com efeito direto e leis fundamentais à operação", "R", "Tabela acima"),
               ("Ler a NE 30 e a NE 25 em busca de indícios (multas de conteúdo local, interdição ANP)", "R", "p. 90, 96-98"),
               ("Indagar a administração e ler correspondências com ANP e IBAMA", "P", "Sem acesso"),
               ("Obter cartas dos assessores jurídicos (modelo no PT 505)", "P", "PT 505"),
               ("Diante de indício: entender a natureza, avaliar o efeito e comunicar ao Comitê (itens 18-23)", "S", "Interdição ANP - tratamento abaixo")],
              ul([f"Contingências → {ref('PT 501')}; comunicação → {ref('PT 260')}; ANP/Peregrino → {ref('PT 560')}"]),
              corpo and "<p><b>Indício identificado:</b> a interdição do FPSO Peregrino pela ANP (ago/2025) apontou deficiências de documentação de gestão de riscos e do sistema de dilúvio. Tratamento: (i) confirmar que a perda operacional (R$ 194,8 mi) foi reconhecida (sim, NE 25); (ii) avaliar multas potenciais não provisionadas (planejado); (iii) comunicar à governança como assunto de descumprimento (minuta no PT 260).</p>",
              "Os descumprimentos conhecidos estão refletidos (provisão de conteúdo local e perda de Peregrino). Não há indício público de descumprimento não registrado com efeito relevante.",
              "Sem acesso a correspondências regulatórias e sem confirmação jurídica.", corpo)


def pt260():
    carta = f"""<div class="letter"><div class="wm">MINUTA DIDÁTICA - NÃO ENVIADA - SEM VALIDADE JURÍDICA</div>
<p><b>Ao Comitê de Auditoria e ao Conselho de Administração da PRIO S.A.</b></p>
<p><b>1. Alcance e época planejados.</b> Auditoria das DFs individuais e consolidadas de 31/12/2025, com materialidade global de R$ 155 mi
(1% da receita) e materialidade de execução de R$ 93 mi. Componentes significativos: Tigris (Peregrino), Forte (Frade/Wahoo e Albacora Leste);
procedimentos específicos em Bravo e nas entidades de trading (PT 600). Fases: intermediária out-nov/2025; final jan-fev/2026; relatório previsto para 10/03/2026.</p>
<p><b>2. Riscos significativos.</b> (i) receita - corte e trading (fraude presumida); (ii) burla de controles; (iii) provisão para abandono;
(iv) recuperabilidade do IR diferido; (v) contabilização da aquisição de +40% de Peregrino; (vi) UOP/reservas e impairment do ágio da Forte.</p>
<p><b>3. Independência.</b> Declaramos atender aos requisitos éticos. Comunicamos os serviços de asseguração do inventário de GEE e os
serviços da KPMG LLP aprovados pelo Comitê, avaliados como não impeditivos (salvaguarda: pré-aprovação e equipes distintas).</p>
<p><b>4. Constatações e dificuldades (até a data desta minuta).</b> (a) divulgação das provisões cíveis (NE 30) com diferença de R$ 43 mi; (b) ausência de nota
de estoques; (c) reclassificação no PL comparativo sem divulgação; (d) dependência do EBITDA pró-forma para atender o covenant; (e) deficiências de
controle em ambiente simulado (PT 265); (f) dificuldade: prazo curto entre o fechamento de Peregrino (11/11/2025) e o encerramento.</p>
<p><b>5. Distorções.</b> Distorções não corrigidas abaixo do limite trivial na simulação (PT 450). Solicitamos correção das divulgações listadas.</p>
<p><b>6. Assuntos regulatórios.</b> Interdição do FPSO Peregrino (ANP, ago/2025) - avaliação de multas e controles de segurança operacional.</p></div>"""
    return pt("PT 260", "Comunicação com os responsáveis pela governança", "NBC TA 260 (R2) itens 9-23, A1-A52; NBC TA 701",
              "Preparar comunicação sobre alcance, época, riscos significativos, independência e principais dificuldades.",
              "Governança: Conselho de Administração, Comitê de Auditoria estatutário (3 membros, 9 reuniões em 2025) e Conselho Fiscal.",
              "Não se aplica.", "Falha na comunicação tempestiva de constatações significativas e de independência.",
              "Relatório do Comitê de Auditoria (DFP p. 104-106) e parecer do Conselho Fiscal (p. 103).",
              [("Identificar os responsáveis pela governança e o calendário de reuniões do Comitê", "R", "p. 104-106"),
               ("Redigir minuta de comunicação de planejamento e constatações", "S", "Minuta abaixo"),
               ("Apresentar e discutir com o Comitê; obter a ata", "P", "Sem acesso"),
               ("Avaliar a adequação da comunicação bidirecional (item 22)", "P", "-")],
              ul([f"Riscos significativos → {ref('PT 315')}; deficiências → {ref('PT 265')}; distorções → {ref('PT 450')}"]),
              "<p>A minuta cobre os requisitos dos itens 14-17 (responsabilidades, alcance e época, constatações significativas, independência). O Comitê se reuniu 9 vezes em 2025, o que permite comunicação tempestiva.</p>",
              "A comunicação planejada é suficiente e tempestiva. A versão aqui é didática.", "Minuta não enviada; sem ata nem resposta da governança.", carta)


def pt265():
    m = tab(["#", "Natureza", "Condição", "Critério", "Causa", "Efeito", "Recomendação"], [
        ["1", '<span class="badge b-r">Constatação - evidência pública</span>', "NE 30 não reconcilia provisões cíveis com o BP (diferença de R$ 43.003 mil); remissões incorretas (NE 2.16); reclassificação no PL sem nota", "CPC 26 itens 38-41; CPC 25 item 84", "Revisão insuficiente do processo de divulgação (checklist)", "Risco de divulgação incorreta e perda de confiabilidade", "Checklist de divulgação com conciliação nota x BP aprovada pelo controller"],
        ["2", '<span class="badge b-r">Constatação - evidência pública</span>', "Ausência de nota específica de estoques (R$ 3,11 bi)", "CPC 16 item 36", "Possível julgamento de imaterialidade inadequado", "Usuário não conhece composição (óleo x materiais) nem provisões", "Incluir nota com composição, critério de NRV e baixas"],
        ["3", '<span class="badge b-r">Constatação - evidência pública</span>', "Data de constituição divergente (FCA 13/10/2008 x NE 1 17/07/2009); responsável técnico do auditor no FCA diferente do sócio signatário", "Res. CVM 80/2022 (consistência cadastral)", "Atualização cadastral sem conferência", "Informação cadastral inconsistente aos usuários", "Conciliar FCA x DFP antes do arquivamento"],
        ["4", '<span class="badge b-s">Constatação - SIMULADA</span>', "175 lançamentos do imobilizado aprovados pelo próprio lançador; 82 acima de R$ 5 mi aprovados por gerente; usuário genérico USR_TEMP com 25 lançamentos manuais", "Política de alçadas e segregação de funções (premissa)", "Perfis de acesso do ERP mal configurados (simulado)", "Capitalização fictícia de R$ 282 mi não prevenida (detectada só por teste)", "Bloquear autoaprovação; workflow de alçada; eliminar usuários genéricos; revisão periódica de acessos"],
        ["5", '<span class="badge b-p">Hipótese</span>', "Transferência de R$ 874,6 mi de materiais do imobilizado para CPV (\"reparos de emergência\")", "CPC 27 itens 7-8 e CPC 16", "Critério de capitalização de sobressalentes e materiais pouco preciso", "Possível superavaliação do imobilizado ou oscilação do CPV", "Testar a política de capitalização (planejado)"],
        ["6", '<span class="badge b-p">Hipótese</span>', "Interdição do FPSO Peregrino (ANP) por documentação de gestão de riscos, ainda sob operação da Equinor", "SGSO/ANP", "Controles operacionais do operador anterior", "Perdas operacionais (R$ 194,8 mi); risco regulatório", "Avaliar os controles assumidos na transição da operação (planejado)"],
    ], larg=["3%", "13%", "22%", "13%", "15%", "16%", "18%"])
    return pt("PT 265", "Deficiências de controle interno - matriz", "NBC TA 265 itens 7-11, A1-A30",
              "Preparar matriz com condição, critério, causa, efeito e recomendação, distinguindo hipóteses de constatações sustentadas por evidências.",
              "Controles sobre divulgação, cadastro, imobilizado (aprovação/segregação) e operações.", "Apresentação e divulgação; existência e classificação (imobilizado).",
              "Deficiências significativas não comunicadas; confundir hipóteses com constatações.",
              "Fontes públicas (DFP, FCA) e base sintética (para as constatações simuladas).",
              [("Comparar notas x BP x FCA para detectar falhas de controle de divulgação", "R", "PT 500"),
               ("Testar segregação e alçadas em 100% da base sintética", "S", "PT 330 T07/T08"),
               ("Indagar e fazer walkthrough dos controles de capitalização e de alçadas", "P", "Sem acesso"),
               ("Classificar a gravidade: deficiência x deficiência significativa (item A5-A7)", "S", "Matriz")],
              ul([f"Comunicação por escrito à governança → {ref('PT 260')}", "06_Resultados/PT330_resumo_caat.csv"]),
              "<p>3 constatações com evidência pública (divulgação/cadastro - deficiências, não significativas isoladamente); 1 constatação simulada classificada como <b>deficiência significativa</b> (permitiu capitalização fictícia acima da MG); 2 hipóteses que dependem de acesso interno.</p>",
              "As constatações públicas são deficiências de controle de divulgação, a comunicar à administração. A simulada seria comunicada por escrito à governança (item 9).",
              "Sem walkthroughs nem testes de controles reais; as hipóteses não foram confirmadas.", m)


def pt300():
    crono = tab(["Fase", "Período (didático)", "Atividades", "Marcos reais"], [
        ["Aceitação/contratação", "abr/2025", "Independência, carta, comunicação com a EY", "Comitê aprova a KPMG em 09/04/2025"],
        ["Revisões trimestrais", "mai, jul, out/2025", "ITR 1T, 2T, 3T (NBC TR 2410)", "Comitê: 05/05, 31/07 e 31/10/2025"],
        ["Planejamento e entendimento", "jun-set/2025", "PT 315, 320; walkthroughs; TI", "Contrato de Peregrino com a Equinor em 01/05/2025"],
        ["Revisão do plano", "ago-nov/2025", "Interdição ANP; fechamento de Peregrino; bond 2030", "Interdição ago/2025; bond 15/10/2025; fechamento 11/11/2025"],
        ["Intermediária", "out-nov/2025", "Testes de controles; capex; JOA", "-"],
        ["Inventário/observação", "31/12/2025", "Óleo nos FPSOs (medição de tanques), almoxarifados de Macaé", "-"],
        ["Final", "jan-fev/2026", "Substantivos, circularizações, estimativas, consolidação", "Certificação D&M (data-base 01/01/2026)"],
        ["Conclusão e relatório", "mar/2026", "PT 450, 560, 580; EQR; comunicação", "Relatório de 10/03/2026; DFP entregue em 10/03/2026"],
    ], larg=["20%", "16%", "36%", "28%"])
    estrategia = tab(["Elemento", "Estratégia global (NBC TA 300 item 7-8)"], [
        ["Alcance", "DFs individuais e consolidadas; 4 componentes significativos/relevantes; DVA; leitura do RA; ITR."],
        ["Prioridades (justificativa)", "1º Peregrino (aquisição e UOP) - 29% da receita e do ativo de longo prazo; 2º ARO e IR diferido (PAA, julgamento alto); 3º receita/corte (fraude presumida); 4º dívida/covenants (continuidade); 5º estoques (+158% e sem nota)."],
        ["Materialidade", "MG R$ 155 mi; ME R$ 93 mi; trivial R$ 7,75 mi (PT 320)."],
        ["Abordagem", "Combinada: testes de controles nos ciclos de receita e capex; substantiva nas estimativas; analíticos de suporte; CAATs em 100% dos lançamentos."],
        ["Recursos", "Especialistas em reservas/ARO, avaliação, tributos e TI (PT 220)."],
        ["Alterações do plano", "(i) Ago/2025, interdição de Peregrino: incluídos testes da perda operacional e de multas; (ii) nov/2025, fechamento de +40%: novo risco significativo de alocação de preço e ARO complementar de R$ 1,32 bi; (iii) LAIR negativo identificado no 4T: troca da base de materialidade para receita."],
    ], larg=["20%", "80%"])
    return pt("PT 300", "Planejamento - estratégia global, plano, cronograma e programas", "NBC TA 300 (R1) itens 7-13, A8-A15 e Apêndice",
              "Elaborar estratégia global, plano, cronograma e programas por ciclo; justificar prioridades e alterações.",
              "Todas as áreas.", "Todas.", "Planejamento que não responde aos riscos; plano não atualizado diante de eventos (Peregrino, ANP).",
              "DFP 2025, relatório do Comitê, fatos relevantes de 2025-2026.",
              [("Definir estratégia global e prioridades", "R", "Tabela"), ("Elaborar cronograma com marcos reais", "R", "Cronograma"),
               ("Elaborar programas de auditoria por ciclo (receitas, disponibilidades, estoques, imobilizado, passivos, estimativas)", "R", "Anexo A"),
               ("Documentar alterações do plano e suas razões (item 10)", "R", "Tabela"),
               ("Reunião de planejamento com a administração e o Comitê", "P", "Sem acesso")],
              ul([f"Programas detalhados → {ref('A')}; respostas → {ref('PT 330')}; materialidade → {ref('PT 320')}"]),
              estrategia + "<h3>Cronograma</h3>" + crono,
              "O plano é proporcional aos riscos, com prioridades justificadas e alterações documentadas diante de eventos do exercício.",
              "Cronograma didático; datas de campo não são reais. Os marcos reais vêm das fontes públicas.")


def pt315():
    niv = {0: "Baixo", 1: "Moderado", 2: "Alto", 3: "Significativo"}
    contas = [
        ("Receita de venda de óleo e trading", [3, 3, 2, 1, "-", 1], "Corte de cargas em dez; trading; fraude presumida"),
        ("Contas a receber (R$ 1,69 bi)", ["-", 1, 1, 1, 2, 1], "Concentração BP/Mercuria; prazo médio de 39,6 dias contra a política de 30"),
        ("Caixa e equivalentes (R$ 3,40 bi)", ["-", 0, 0, 0, 1, 1], "63% em contas remuneradas USD no exterior"),
        ("Estoques (R$ 3,11 bi)", ["-", 2, 1, 2, 2, 2], "+158%, sem nota; óleo em FPSO; materiais de Peregrino"),
        ("Imobilizado (R$ 31,14 bi)", ["-", 2, 2, 2, 3, 2], "Capex x opex; UOP; Peregrino a valor justo; impairment"),
        ("Intangível/ágio (R$ 15,04 bi)", ["-", 1, 1, 1, 3, 1], "Ágio da Forte R$ 1,52 bi; concessão ABL R$ 7,03 bi"),
        ("Aquisição +40% Peregrino", [3, 1, "-", 1, 3, 2], "Aquisição de ativos x combinação; alocação de R$ 9,5 bi"),
        ("IR/CS diferido ativo (R$ 8,12 bi)", ["-", 2, "-", 1, 3, 2], "PAA; projeções de Brent/reservas até 2041"),
        ("Provisão para abandono (R$ 5,45 bi)", ["-", "-", 2, 1, 3, 2], "PAA; custo, prazo e taxa"),
        ("Empréstimos e debêntures (R$ 27,1 bi)", ["-", 1, 2, 1, 1, 2], "Covenants; hedge accounting; classificação circulante"),
        ("Contingências (R$ 0,76 bi provisão / R$ 4,0 bi possíveis)", ["-", "-", 2, 1, 2, 2], "Completude; julgamento jurídico"),
        ("Partes relacionadas", [1, "-", 2, 1, "-", 2], "Completude; capital pulverizado"),
        ("Conversão USD → BRL (ajustes de conversão)", [1, "-", "-", 2, 2, 1], "Moeda funcional; base tributária"),
    ]
    cab = ["Conta / transação", "Ocorrência", "Existência", "Integridade", "Exatidão / corte", "Avaliação", "Apresentação/ divulgação", "Fator de risco principal"]
    linhas = []
    for n, vals, f in contas:
        tds = [n] + [f'<span class="h{v}">{niv[v]}</span>' if v != "-" else "-" for v in vals] + [f]
        linhas.append(tds)
    html_rows = []
    for ln in linhas:
        cells = [f"<td>{ln[0]}</td>"]
        for c in ln[1:7]:
            k = c.split('"h')[1][0] if 'class="h' in c else None
            cells.append(f'<td class="h{k}">{c}</td>' if k else f"<td>{c}</td>")
        cells.append(f'<td style="text-align:left">{ln[7]}</td>')
        html_rows.append("<tr>" + "".join(cells) + "</tr>")
    th = "".join(f"<th>{c}</th>" for c in cab)
    matriz = f'<div class="tw"><table class="heat"><thead><tr>{th}</tr></thead><tbody>{"".join(html_rows)}</tbody></table></div>'
    entend = tab(["Dimensão (item 19)", "Entendimento obtido"], [
        ["Setor e ambiente", "E&P offshore na Bacia de Campos; preço do Brent (-14% em 2025; recuperação para US$ 95 de média em 2026 até out, EIA); câmbio; regulação ANP/IBAMA; Pillar 2 e Reforma Tributária."],
        ["Natureza da entidade", "Maior independente de óleo e gás do Brasil; estratégia de aquisição e redesenvolvimento de campos maduros; 7 campos/clusters; 17 clientes, sendo Repsol 29% e Unipec 15% das vendas (NE 29)."],
        ["Estrutura e financiamento", "Holding com controladas no Brasil, Luxemburgo e Áustria; dívida bruta de R$ 27,1 bi (bonds, PPE/ACC/NCE, debêntures com swap para USD)."],
        ["Estrutura contábil", "CPC/IFRS; moeda funcional USD; esforços bem-sucedidos; UOP sobre reservas provadas desenvolvidas; JOA proporcional; hedge accounting de fluxo de caixa."],
        ["Mudanças contábeis/estimativas", "Vida econômica de Peregrino: 2031 → 2034 a partir de jan/2026 (NE 2.22.1); atualização das taxas de ARO (+R$ 722,5 mi); IFRS 18 a partir de 2027."],
        ["Ambiente de controle", "Novo Mercado; Comitê de Auditoria estatutário; auditoria interna; compliance e canal de integridade (DFP p. 104-106)."],
        ["Processo de avaliação de riscos", "Gestão de riscos de mercado, crédito e liquidez pelo CA (NE 29); política de derivativos que admite fins especulativos (NE 29) - ponto de atenção."],
        ["TI", "ERP e sistemas não divulgados publicamente (hipótese a confirmar: ERP integrado para contabilidade, suprimentos e ativo fixo); interfaces críticas com billing statements de JOA, sistemas de medição fiscal ANP e trading. Controles gerais de TI (acesso, mudança, operação) planejados - PT 330."],
        ["Atividades de controle relevantes", "Aprovação de capex e alçadas; conciliação de cash calls; medição fiscal; corte de cargas; revisão de estimativas pelo Comitê."],
    ], larg=["22%", "78%"])
    return pt("PT 315", "Identificação e avaliação dos riscos de distorção relevante", "NBC TA 315 (R2) itens 13-38, A1-A240; Apêndices 1-6",
              "Compreender a entidade, seu ambiente, a estrutura contábil, a TI e os controles; elaborar matriz de riscos por conta e afirmação; identificar riscos significativos.",
              "Todas as contas relevantes.", "Ocorrência, existência, integridade, exatidão/corte, avaliação, apresentação/divulgação.",
              "<b>Riscos significativos (nível mais alto do espectro):</b> receita (corte/fraude); aquisição de Peregrino (alocação); imobilizado e intangível (avaliação: UOP/impairment); IR diferido; ARO; burla de controles.",
              "DFP 2025 (notas 1-31), RA, fatos relevantes, análise horizontal/vertical (06_Resultados/PT520_analise_horizontal_vertical.csv). Critério: contas acima da ME ou com fatores de risco qualitativos.",
              [("Ler a DFP integralmente e o RA; mapear o portfólio e o grupo", "R", "NE 1, 2.3, 7"),
               ("Executar análise horizontal/vertical e identificar variações > ME e > 10%", "R", "PT 520"),
               ("Avaliar fatores de risco inerente (complexidade, subjetividade, mudança, incerteza, viés)", "R", "Matriz"),
               ("Entender a TI e fazer walkthrough dos controles relevantes", "P", "Sem acesso"),
               ("Comparar riscos com os PAA da KPMG (2025) e da EY (2024)", "R", "p. 99-102; F03")],
              ul([f"Respostas → {ref('PT 330')}; PAA reais: ARO e IR diferido (KPMG); combinação de negócios, impairment, ARO e IR diferido (EY 2024) → {ref('PT 510')}"]),
              entend + "<h3>Matriz de riscos por conta e afirmação (risco inerente - espectro)</h3>" + matriz +
              f"<p>Os riscos avaliados como significativos coincidem com os 2 PAA da KPMG e com os 4 PAA da EY de 2024, o que corrobora a avaliação. Acrescentamos <b>estoques</b> e <b>covenants</b> como riscos altos por fatores identificados no exame público.</p>{fig('g02_imobilizado_classes.png', 'Figura 3 - Imobilizado por classe: Peregrino (plataforma e ativos O&G) e gastos de desenvolvimento (Wahoo) concentram o crescimento.')}",
              "Foram identificados 6 riscos significativos; a matriz orienta natureza, época e extensão dos testes.",
              "TI e controles não foram observados; o risco de controle não foi avaliado com evidência.")


def pt320():
    b = bases_materialidade()
    linhas = [[x["base"], br(x["valor"]), f"{br(x['pct_min']*100,2)}% - {br(x['pct_max']*100,2)}%", br(x["valor"] * x["pct"]), "SIM" if x["escolhida"] else "-"] for x in b]
    return pt("PT 320", "Materialidade", "NBC TA 320 (R1) itens 10-14, A1-A14; NBC TA 450 item A2",
              "Calcular e justificar a materialidade global, a de execução e as específicas; fundamentar bases, percentuais e revisões.",
              "Demonstrações consolidadas 2025.", "Todas.",
              "Base volátil (LAIR negativo); materialidade alta demais para áreas sensíveis (partes relacionadas, remuneração).",
              "DRE/BP/DFC consolidados (CVM). Critério: base estável e relevante para os usuários.",
              [("Calcular faixas para 5 bases de referência", "R", "X-PT320"), ("Selecionar a base e justificar", "R", "Abaixo"),
               ("Definir materialidade de execução e limite trivial", "R", "X-PT320"), ("Definir materialidades específicas", "R", "X-PT320"),
               ("Reavaliar no encerramento (item 12-13)", "R", "Sem alteração necessária")],
              ul(["03_Planilhas/PT320_Materialidade.xlsx (fórmulas)", f"Uso em amostragem → {ref('PT 530')}; avaliação → {ref('PT 450')}; componentes → {ref('PT 600')}"]),
              tab(["Base", "Valor 2025 (R$ mil)", "Faixa usual", "Calculada", "Escolhida"], linhas, num_cols=(1, 3)) +
              tab(["Parâmetro", "Valor (R$ mil)", "Fundamento"], [
                  ["Materialidade global (MG)", "155.000", "1% da receita líquida (R$ 155.840 mil), arredondada para baixo"],
                  ["Materialidade para execução (ME)", "93.000", "60% da MG: auditoria inicial, aquisições relevantes e controles não testados → risco maior"],
                  ["Limite claramente trivial", "7.750", "5% da MG"],
                  ["Específica - remuneração da administração e partes relacionadas", "1.750", "5% de R$ 34.932 mil; sensibilidade qualitativa dos usuários"],
                  ["Específica - divulgação de contingências possíveis", "77.500", "50% da MG - relevância para credores"],
              ], larg=["40%", "16%", "44%"], num_cols=(1,)),
              "MG de R$ 155 mi; ME de R$ 93 mi; trivial de R$ 7,75 mi. Validação cruzada: 2% do EBITDA ajustado (R$ 163 mi) e 0,25% do ativo (R$ 160 mi) caem na mesma faixa.",
              "Percentuais por julgamento; não se conhece a materialidade efetiva da KPMG.")
