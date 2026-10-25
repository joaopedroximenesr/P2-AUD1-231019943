"""Conteúdo dos papéis de trabalho - parte B (PT 330 a PT 600, base simulada, anexos e conclusão)."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notas_dfp2025 as ne  # noqa: E402
from cobertura import FONTES, MATRIZ  # noqa: E402
from dossie_base import RAIZ, badge, br, carregar_json, csv, fig, pt, ref, tab, ul  # noqa: E402
from parametros import conta  # noqa: E402

RT = carregar_json("resumo_testes.json")
RA = carregar_json("resumo_analiticos.json")
IND = RA["indicadores"]
MUS, MUS2, ATR = RT["mus"], RT["mus_pos_ajustes"], RT["atributos"]


def pt330():
    linhas = [
        ["Receita - corte/ocorrência (fraude)", "Controles de faturamento e transferência de controle (Incoterms)", "Corte de cargas ±10 dias; confirmação de recebíveis; analítico volume x Brent x PTAX", "Final (31/12 e jan/26)", "100% das cargas no corte; analítico em 100%", badge("R") + " analítico; " + badge("P") + " corte"],
        ["Burla de controles", "-", "Testes de lançamentos por critérios de risco em 100%; revisão de estimativas; transações incomuns", "Final", "100% da população", badge("S") + " (base); " + badge("R") + " NE 25"],
        ["Imobilizado - existência", "Inventário rotativo; conciliação do subledger com o razão", "MUS (n=" + str(MUS["tamanho_amostra_calculado"]) + ") com documento-suporte; inspeção física nos FPSOs", "Intermediária + final", "MUS 95%, TM R$ 93 mi", badge("S") + " MUS; " + badge("P") + " inspeção"],
        ["Imobilizado - classificação capex/opex", "Aprovação de AFE/capex e alçadas", "CAATs T07-T09; exame de adições e transferências (R$ 874,6 mi)", "Intermediária + final", "100% (CAAT)", badge("S")],
        ["Imobilizado/intangível - avaliação (UOP, impairment)", "Revisão gerencial das reservas D&M", "Recálculo de UOP por campo; avaliação da D&M (NBC TA 500 item 8); teste do ágio (taxa de 9,61%)", "Final", "Todos os campos", badge("R") + " analítico D&A; " + badge("P") + " recálculo"],
        ["Aquisição +40% Peregrino", "Aprovação do CA; revisão da alocação", "Contrato SPA; alocação (NE 9.d); teste de concentração CPC 15 B7A; ARO complementar", "Dez/2025-fev/2026", "100% da transação", badge("R") + " leitura; " + badge("P") + " contrato"],
        ["ARO (PAA)", "Revisão de premissas", "Sensibilidade; comparação das taxas com mercado; prazos x concessão", "Final", "Todos os campos", badge("R")],
        ["IR diferido (PAA)", "Revisão das projeções", "Aderência das projeções ao orçamento/D&M; limite de 30%; Pillar 2", "Final", "Todas as entidades", badge("R") + " leitura; " + badge("P") + " projeções"],
        ["Empréstimos/covenants", "Monitoramento trimestral do covenant", "Confirmação com credores; recálculo do covenant; teste de hedge accounting", "Final", "100% dos contratos", badge("R") + " recálculo; " + badge("P") + " confirmação"],
        ["Estoques", "Contagens e medição de tanques", "Observação em 31/12; NRV x Brent dez/2025; realização em 2026 (ITR)", "31/12 e final", "Locais > 5% do saldo", badge("P") + "; " + badge("R") + " ITR"],
        ["Contingências", "Controle jurídico de processos", "Cartas de advogados; leitura de atas; conciliação NE 30 x BP", "Final", "Processos > R$ 7,75 mi", badge("R") + " conciliação; " + badge("P") + " cartas"],
        ["Caixa", "Conciliações bancárias", "Confirmação bancária (14 instituições - NE 3)", "Final", "100% das contas", badge("P") + " (modelo no PT 505)"],
        ["Controles gerais de TI", "Acesso, mudanças, operação", "Teste de perfis (autoaprovação), usuários genéricos", "Intermediária", "População de usuários", badge("S") + " (T07)"],
    ]
    corpo = tab(["Risco (PT 315)", "Teste de controle", "Procedimento substantivo", "Época", "Extensão", "Situação"], linhas,
                larg=["16%", "16%", "30%", "10%", "12%", "16%"])
    r = csv("PT330_resumo_caat.csv")
    caat = tab(["Teste (100% da base sintética)", "Itens sinalizados", "Valor contábil sinalizado (R$)"],
               [[x.teste, br(x.itens_sinalizados), br(x.valor_contabil_sinalizado_brl, 2)] for x in r.itertuples()], num_cols=(1, 2))
    return pt("PT 330", "Respostas aos riscos avaliados", "NBC TA 330 (R1) itens 5-30, A1-A73",
              "Relacionar cada risco aos testes de controles e procedimentos substantivos; definir natureza, época e extensão; distinguir testes executados de planejados.",
              "Riscos significativos e altos do PT 315.", "Conforme o risco.", "Respostas não proporcionais; testes apenas planejados apresentados como executados.",
              "Matriz de riscos (PT 315) e base sintética de 518.405 registros para os CAATs.",
              [("Mapear risco → resposta com natureza, época e extensão", "R", "Tabela"),
               ("Executar 12 CAATs na base sintética (T01-T12)", "S", "05_Codigo/02_testes_base.py"),
               ("Executar analíticos substantivos com dados reais", "R", "PT 520"),
               ("Executar testes de controles reais (walkthrough, reexecução)", "P", "Sem acesso")],
              ul(["06_Resultados/PT330_resumo_caat.csv; PT330_excecoes_caat.csv.gz", f"Amostragem → {ref('PT 530')}; exceções → {ref('PT 450')}; programas → {ref('A')}"]),
              "<h3>Resultados dos testes em 100% da população [DADOS SINTÉTICOS]</h3>" + caat +
              "<p>T01-T10 identificaram 100% dos erros inseridos (655 de 655), sem falsos positivos. T11 (89.510 itens de materiais sem movimento há mais de 12 meses, R$ 1,24 bi) e T12 (40 itens estatisticamente atípicos) são <i>indicadores</i> para teste de avaliação (obsolescência/NRV), não erros.</p>",
              "Cada risco tem resposta definida. As respostas executáveis com dados públicos foram realizadas; as demais estão planejadas e identificadas.",
              "A detecção de 100% reflete testes desenhados conhecendo as tipologias inseridas; em ambiente real, a eficácia seria menor e haveria falsos positivos.", corpo)


def pt402():
    corpo = tab(["Organização / serviço", "Relevância para as DFs", "Controles complementares da usuária (CUEC)", "Relatório esperado", "Procedimento alternativo"], [
        ["Equinor - operadora de Peregrino até 11/11/2025 (cash calls e billing statements de 40%)", "Custos e capex de Peregrino de jan-nov/2025; receita até o fechamento", "Revisão e aprovação dos billing statements; conciliação de cash calls (NE 2.11.2)", "SOC 1 tipo 2 do operador (raro) ou relatório de auditoria do JOA", "Exercer o direito de auditoria do JOA; testar billing statements contra faturas; analíticos de custo por barril"],
        ["Operador de Pitangola (PRIO não operadora)", "Custos proporcionais (80%)", "Idem", "Relatório de auditoria do consórcio", "Idem"],
        ["Prestador de comercialização/trader (intermediário das vendas - NE 29)", "Receita, recebíveis, risco de crédito", "Conferência de contratos, B/L e faturas; aprovação de clientes", "SOC 1 tipo 2", "Confirmação de clientes; vouching de B/L"],
        ["Itaú Corretora - escriturador de ações (FCA)", "Capital, tesouraria (59,5 mi ações), opções", "Conciliação da posição acionária", "SOC 1 tipo 1 ou 2", "Confirmação da posição com o escriturador"],
        ["Bancos/fundo cambial BTG (custódia)", "Caixa (R$ 3,4 bi)", "Conciliação diária", "Não aplicável (confirmação)", "Confirmação bancária (PT 505)"],
        ["Provedores de TI/nuvem (hipótese)", "Processamento contábil", "Gestão de acessos da usuária", "SOC 1/SOC 2 tipo 2", "Testes diretos de controles gerais de TI"],
    ], larg=["22%", "18%", "22%", "16%", "22%"])
    return pt("PT 402", "Organizações prestadoras de serviços", "NBC TA 402 itens 9-22, A1-A44",
              "Identificar serviços terceirizados relevantes e controles complementares; planejar a análise de relatórios tipo 1 ou tipo 2 e procedimentos alternativos.",
              "Custos e capex de JOA (Peregrino/Pitangola), comercialização, escrituração de ações, custódia.",
              "Ocorrência e exatidão (custos JOA); existência (caixa, ações); ocorrência (receita).",
              "Custos de Peregrino de jan-nov/2025 processados pela Equinor sem visibilidade dos controles; integração dos sistemas após o fechamento.",
              "NE 2.11 (JOA), NE 29 (trader), FCA (escriturador), NE 3 (bancos).",
              [("Identificar serviços terceirizados nas fontes públicas", "R", "Tabela"),
               ("Avaliar se o serviço faz parte do sistema de informação relevante (item 12)", "R", "Tabela"),
               ("Obter e avaliar relatórios tipo 2: período, exceções, CUECs, subprestadores", "P", "Sem acesso"),
               ("Planejar procedimentos alternativos (direito de auditoria do JOA)", "R", "Tabela")],
              ul([f"Risco de controle → {ref('PT 315')}; confirmações → {ref('PT 505')}"]),
              "<p>Seis prestadoras relevantes foram identificadas; a mais crítica é a operadora de Peregrino até 11/11/2025. Com relatório tipo 1, o auditor não obteria evidência de eficácia operacional e teria de ampliar os testes substantivos.</p>",
              "O uso de prestadoras não impede a auditoria, desde que haja tipo 2 ou procedimentos alternativos substantivos.",
              "Nenhum relatório SOC foi obtido.", corpo)


def pt450():
    comp = csv("PT450_inseridos_x_detectados.csv")
    imp = csv("PT450_impacto_erros_inseridos.csv")
    mapa = tab(["Ref.", "Origem", "Descrição", "Valor (R$ mil)", "Situação"], [
        ["D01", "Pública", "Provisões cíveis: abertura da NE 30 x BP - diferença de divulgação", "43.003", "Não corrigida - divulgação"],
        ["D02", "Pública", "Ausência de nota de estoques (saldo R$ 3.109.940 mil)", "n/a", "Não corrigida - omissão"],
        ["D03", "Pública", "Remissões incorretas entre notas (NE 2.16)", "n/a", "Não corrigida - qualitativa"],
        ["D04", "Pública", "Reclassificação no PL comparativo sem nota", "29.885", "Não corrigida - apresentação"],
        ["D05", "Pública", "MTM de swap de empréstimo apresentado em debêntures", "11.020", "Não corrigida - classificação"],
        ["D06", "Pública", "D&A DFC x DVA (1.035) e CPV x NE 15 (5.147)", "6.182", "Trivial"],
        ["S01-S04", "SIMULADA", "E09 OPEX capitalizado; E06 x10; E01 duplicidade; E02 corte", br((imp.set_index('tipo_erro').loc[['E09-Lançamento manual suspeito', 'E06-Digitação x10', 'E01-Duplicidade', 'E02-Corte'], 'impacto_valor_contabil_brl'].sum()) / 1000), "Corrigidas (simulação)"],
        ["S05-S07", "SIMULADA", "E03 VC negativo; E04 depreciação em andamento; E05 taxa linear", br(-(imp.set_index('tipo_erro').loc[['E03-VC negativo', 'E04-Depreciação em andamento', 'E05-Taxa incorreta'], 'impacto_valor_contabil_brl'].sum()) / 1000), "Não corrigidas: ajuste líquido proposto (+) no ativo"],
    ], larg=["8%", "10%", "52%", "14%", "16%"], num_cols=(3,))
    det = tab(["Erro inserido", "Teste", "Inseridos", "Detectados", "Taxa", "Falsos positivos"],
              [[x.tipo_erro_inserido, x.teste, x.inseridos, x.detectados, br(x.taxa_deteccao, 0, pct=True), x.falsos_positivos] for x in comp.itertuples()],
              num_cols=(2, 3, 4, 5))
    return pt("PT 450", "Avaliação das distorções identificadas e simuladas", "NBC TA 450 (R1) itens 5-15, A1-A30",
              "Elaborar o mapa de distorções identificadas ou simuladas, corrigidas e não corrigidas; avaliar os efeitos quantitativos e qualitativos.",
              "Todas as contas; ênfase em imobilizado (base) e divulgações.", "Todas.", "Acúmulo de distorções não corrigidas acima da materialidade; distorções qualitativamente relevantes (fraude).",
              "Reconciliações públicas (PT 500) e resultados da base sintética (PT 330/530).",
              [("Acumular distorções acima do limite trivial (R$ 7,75 mi)", "R", "Mapa"),
               ("Classificar em factuais, de julgamento e projetadas", "R", "X-PT450"),
               ("Solicitar correção à administração e avaliar as não corrigidas (item 8-11)", "S", "Correções simuladas"),
               ("Reaplicar o MUS após os ajustes", "S", "PT 530"),
               ("Comparar erros inseridos com exceções identificadas (registro exigido)", "S", "Tabela")],
              ul(["03_Planilhas/PT450_PT600_Distorcoes_Componentes.xlsx", "02_Base_Simulada/registro_erros_inseridos.csv", f"Comunicação → {ref('PT 260')}; representações → {ref('PT 580')}"]),
              mapa + "<h3>Registro comparativo: erros inseridos x detectados [DADOS SINTÉTICOS]</h3>" + det + fig("g07_deteccao.png", "Figura 4 - Erros inseridos x detectados por tipologia (gabarito x testes)."),
              f"Distorções públicas: todas de apresentação/divulgação, sem efeito no resultado; D01 e D02 seriam comunicadas para correção. Simuladas: o total inserido foi de R$ {br(RT['superavaliacao_real_brl']/1e6,1)} mi de superavaliação e R$ {br(-RT['subavaliacao_real_brl']/1e6,1)} mi de subavaliação; após as correções simuladas, as não corrigidas somam R$ 6,96 mi (líquido), abaixo do limite trivial, e o LSD do MUS cai para R$ {br(MUS2['limite_superior_distorcao_brl']/1e6,1)} mi, abaixo da distorção tolerável. A fraude simulada (E09) é relevante por natureza, independentemente do valor.",
              "As correções da administração são simuladas; as distorções públicas não puderam ser discutidas com a companhia.")


def pt500():
    rec = csv("PT500_reconciliacao_notas_x_demonstracoes.csv")
    linhas = [[x.item, x.ref_demonstracao, br(x.valor_demonstracao), x.ref_nota, br(x.valor_nota), br(x.diferenca), x.situacao] for x in rec.itertuples()]
    aval = tab(["Fonte de evidência", "Relevância", "Confiabilidade", "Observação"], [
        ["DFP auditada (CVM/ENET)", "Alta", "Alta - documento oficial, auditado", "Evidência gerada pela própria entidade; o auditor real obteve evidência externa"],
        ["Dados abertos CVM (CSV)", "Alta", "Alta - mesma origem; conferido 100% contra o PDF nas contas testadas", "Sem notas explicativas estruturadas"],
        ["RA e apresentações de resultados", "Média", "Média - não auditados (marcados (*) na DFP)", "Usados só para expectativas/corroboração"],
        ["Fatos relevantes 2026", "Alta para PT 560/570", "Alta - divulgação regulatória", "Posteriores à data do relatório"],
        ["BCB (PTAX) e EIA (Brent)", "Alta para analíticos", "Alta - fontes externas independentes", "Série EIA obtida por espelho público (limitação de acesso ao site original)"],
        ["Base sintética", "Didática", "Nula como evidência real", "Usada exclusivamente para demonstrar procedimentos"],
    ], larg=["26%", "14%", "30%", "30%"])
    return pt("PT 500", "Evidência de auditoria - avaliação e reconciliações", "NBC TA 500 (R1) itens 6-11, A1-A57",
              "Avaliar relevância, confiabilidade e suficiência das evidências; reconciliar saldos com as demonstrações; explicitar limitações das fontes públicas e dos dados simulados.",
              "Saldos das notas x demonstrações; base simulada x NE 8/15.", "Exatidão, integridade, apresentação.", "Divergências entre notas e demonstrações; evidência inadequada.",
              "19 reconciliações cobrindo 100% das principais contas; base simulada por classe (27 classes).",
              [("Reconciliar notas explicativas x demonstrações (CVM dados abertos)", "R", "Tabela"),
               ("Conferir os CSV da CVM contra o PDF da DFP (amostra de contas)", "R", "BP p. 12-16"),
               ("Conciliar a base simulada com a NE 8/NE 15 e explicar diferenças", "S", "Seção BS"),
               ("Avaliar a confiabilidade de cada fonte", "R", "Tabela"),
               ("Obter evidência externa (confirmações) e avaliar especialistas (D&M)", "P", "PT 505")],
              ul(["03_Planilhas/PT500_PT510_Conciliacoes.xlsx", f"Diferenças → {ref('PT 450')}; base → {ref('BS')}"]),
              tab(["Item", "Ref. DF", "DF", "Ref. nota", "Nota", "Dif.", "Situação"], linhas, num_cols=(2, 4, 5), larg=["24%", "16%", "11%", "15%", "11%", "8%", "15%"]) +
              "<p><b>Diferenças acima do trivial:</b> (1) debêntures: R$ 11.020 mil, explicada pelo MTM do swap do empréstimo XP; (2) D&A da DFC x movimentações: R$ 151.210 mil, com hipótese de conversão por taxa média x histórica (PT 520). Adicionalmente, a abertura das provisões cíveis da NE 30 não fecha com o BP por R$ 43.003 mil (D01).</p>" + aval,
              "Para o objetivo didático, a evidência pública é relevante e confiável; não é suficiente para uma opinião, porque faltam evidências externas e internas.",
              "Fontes públicas são, em grande parte, produzidas pela própria entidade; a base sintética não tem valor probatório.")


def pt501():
    corpo = "<h3>Estoques</h3>" + tab(["Aspecto", "Análise"], [
        ["Saldo e variação", f"R$ {br(conta('BPA','1.01.04'))} mil em 31/12/2025 (2024: R$ {br(conta('BPA','1.01.04','PENÚLTIMO'))} mil; +158%)."],
        ["Divulgação", "Não há nota específica; constam apenas as políticas 2.7 (óleo) e 2.8 (consumíveis) - CPC 16 item 36 exige valor por classificação → D02."],
        ["Explicação provável", "Fechamento de Peregrino com R$ 877.125 mil de \"materiais em almoxarifado\" (NE 9.d) e óleo produzido não vendido no fim de dez/2025 (produção de 155,8 mil bpd em dez)."],
        ["Evidência posterior", "ITR: estoques de R$ 2,32 bi (31/03/2026) e R$ 1,61 bi (30/06/2026) → realização posterior que corrobora existência e valor (realizado)."],
        ["NRV", "Brent em 31/12/2025: US$ 61,35 (EIA), abaixo da média do ano; óleo pesado de Peregrino com desconto maior (RA) → teste de NRV planejado."],
    ], larg=["20%", "80%"])
    lit = tab(["Processo (NE 30)", "Classificação", "R$ mil"], [[n, "Possível", br(v)] for n, v in ne.NE30_POSSIVEIS] + [
        ["Conteúdo local - Prio Forte (ANP)", "Provável - provisionado", br(ne.NE30["conteudo_local_forte"])],
        ["IRRF remessas 2013 - Prio Forte", "Provável - provisionado", br(ne.NE30["irrf_forte_2013"])]], num_cols=(2,))
    seg = tab(["Requisito CPC 22 / IFRS 8", "Situação na DFP", "Avaliação"], [
        ["Identificação de segmentos (item 5)", "Segmento único: E&P (NE 28)", "Plausível: os campos têm características econômicas semelhantes (agregação permitida, item 12), mas o RA gerencia por campo (receita e lifting cost por campo) → indagar o CODM (planejado)"],
        ["Informações por área geográfica (item 33)", "Ativo Brasil x exterior; receita 100% \"exterior\"", "Ativo não circulante no exterior caiu de R$ 12,5 bi para R$ 0,18 bi sem explicação (liquidação da Stellina?) → a esclarecer"],
        ["Principais clientes (item 34)", "Repsol 29% e Unipec 15% das vendas - NE 29, não na NE 28", "Divulgado em outra nota - aceitável, com recomendação de remissão"],
    ], larg=["24%", "30%", "46%"])
    return pt("PT 501", "Itens específicos - estoques, litígios e informações por segmento", "NBC TA 501 itens 4-13, A1-A26",
              "Planejar procedimentos sobre estoques, litígios e informações por segmento; executar os permitidos pelas fontes disponíveis.",
              "Estoques (BP 1.01.04); provisões e contingências (NE 30); segmentos (NE 28).",
              "Existência e avaliação (estoques); integridade e avaliação (litígios); apresentação (segmentos).",
              "Estoques sem nota e com crescimento atípico; litígios relevantes como possíveis (R$ 4,03 bi); segmento único questionável.",
              "BP, NE 2.7-2.8, 9.d, 28, 29, 30; ITR 2026. Critério: saldos > ME e processos > limite trivial.",
              [("Observar a contagem física e a medição de tanques nos FPSOs e almoxarifados em 31/12/2025 (item 4)", "P", "Não realizada - simulação proibida"),
               ("Analisar realização subsequente dos estoques pelo ITR 2026", "R", "F05"),
               ("Conciliar provisões da NE 30 com o BP e avaliar classificação provável/possível", "R", "D01"),
               ("Enviar cartas aos assessores jurídicos (item 10) e ler atas", "P", "Modelo no PT 505"),
               ("Avaliar a identificação de segmentos e as divulgações exigidas", "R", "Tabela"),
               ("Indagar o CODM sobre os relatórios gerenciais por campo", "P", "Sem acesso")],
              ul([f"Distorções D01/D02 → {ref('PT 450')}; ARO e contingências → {ref('PT 540')}; leis → {ref('PT 250')}"]),
              corpo + "<h3>Litígios - maiores causas (NE 30)</h3>" + lit + "<h3>Informações por segmento</h3>" + seg,
              "Estoques: existência corroborada pela realização em 2026, com deficiência de divulgação. Litígios: a provisão de R$ 758 mi reconcilia com o BP no total, mas não na abertura (diferença de R$ 43 mi). Segmentos: divulgação aceitável, com pontos a esclarecer.",
              "Sem observação física, cartas jurídicas nem acesso aos relatórios gerenciais.")


def pt505():
    clientes = [("BP", 542_451, 542_451, "Confirmado", "-"), ("Mercuria", 288_670, 279_955, "Diferença", "Fatura de 30/12 registrada pelo cliente em jan/26 (corte) - conciliada"),
                ("Repsol", 229_569, 229_569, "Confirmado", "-"), ("Cathay", 205_635, None, "Sem resposta", "Procedimento alternativo: recebimento em jan/26 + B/L"),
                ("Petrochina", 160_995, 160_995, "Confirmado", "-")]
    ctrl = tab(["Destinatário", "Saldo contábil (R$ mil - real)", "Resposta (R$ mil - SIMULADA)", "Status [SIMULADO]", "Tratamento"],
               [[c, br(s), br(r) if r else "-", st, t] for c, s, r, st, t in clientes], num_cols=(1, 2), larg=["16%", "18%", "18%", "14%", "34%"])
    modelos = """<div class="letter"><div class="wm">MODELO - NÃO ENVIADO</div>
<p><b>Confirmação positiva de saldo - cliente.</b> [Papel timbrado da PRIO] Prezados, nossos auditores [nome do auditor], [endereço],
estão examinando nossas demonstrações contábeis. Solicitamos confirmar <u>diretamente a eles</u> o saldo devido por V.Sas. em 31/12/2025:
<b>US$ [valor] / R$ [valor]</b>, referente às faturas [nºs] de venda de óleo dos campos [campos]. Se o saldo divergir, informe os detalhes.
[Assinatura da administração]. Resposta: ( ) concorda ( ) diverge - detalhes: ____ - Assinatura/cargo/data.</p>
<p><b>Confirmação bancária.</b> Saldos de contas correntes, time deposits, fundos (BTG fundo cambial), empréstimos (PPE/ACC/NCE),
garantias, derivativos (swaps de debêntures e da NCE XP), cartas de crédito e assinaturas autorizadas em 31/12/2025.</p>
<p><b>Credores/trustee.</b> Saldo de principal e juros dos bonds 2026/2030 e das debêntures; cumprimento de covenants; garantias (FPSO Bravo e FPSO Frade).</p>
<p><b>Assessores jurídicos (carta de circularização).</b> Lista de processos, avaliação de probabilidade e valor estimado; processos não listados pela administração.</p>
<p><b>Parceiros de JOA (Repsol Sinopec, Equinor).</b> Saldo de adiantamentos de parceiros (NE 18: R$ 240.064 mil) e cash calls em aberto.</p></div>"""
    return pt("PT 505", "Confirmações externas", "NBC TA 505 itens 7-16, A1-A25",
              "Preparar modelos, controle de circularização, tratamento de diferenças e procedimentos alternativos, sem enviar solicitações reais.",
              "Contas a receber (NE 4), caixa (NE 3), empréstimos (NE 13-14), contingências (NE 30), parceiros (NE 18).",
              "Existência, direitos e obrigações, integridade (passivos).",
              "Recebíveis concentrados (5 clientes = 84%); 14 bancos; 12 credores com covenant.",
              "Saldos reais por contraparte das NE 3, 4 e 13. Seleção: clientes > 5% do saldo; 100% de bancos e credores.",
              [("Selecionar contrapartes e preparar modelos", "R", "Modelos abaixo"),
               ("Manter controle sobre envio e recebimento (item 7)", "S", "Controle SIMULADO"),
               ("Enviar e obter respostas", "P", "Proibido pelas instruções - não realizado"),
               ("Investigar diferenças e aplicar procedimentos alternativos às não respostas", "S", "Tabela"),
               ("Avaliar a confiabilidade das respostas (risco de interceptação)", "P", "-")],
              ul([f"Cartas jurídicas → {ref('PT 501')}; covenants → {ref('PT 570')}"]),
              "<p>Controle de circularização com respostas <b>sintéticas</b>, para demonstrar o tratamento:</p>" + ctrl,
              "Os modelos e o controle permitem executar o procedimento no caso real. As respostas apresentadas são fictícias e não constituem evidência.",
              "Nenhuma solicitação foi enviada; as respostas são simuladas e estão identificadas.", modelos)


def pt510():
    si = csv("PT510_saldos_iniciais.csv", dtype={"cd_conta": str})
    dif = si[si["situacao"] != "Igual"]
    t = tab(["Conta", "Descrição", "DFP 2024 original", "Comparativo DFP 2025", "Diferença"],
            [[x.cd_conta, x.ds_conta, br(x.dfp2024_original), br(x.comparativo_dfp2025), br(x.diferenca)] for x in dif.itertuples()], num_cols=(2, 3, 4))
    paa = ul(ne.AUDITOR["anterior_paa"])
    return pt("PT 510", "Trabalhos iniciais - saldos iniciais", "NBC TA 510 (R1) itens 3-13, A1-A11",
              "Tratar o caso como auditoria inicial: examinar saldos de abertura, políticas contábeis e efeitos de modificações na opinião do auditor anterior.",
              "Saldos de 31/12/2024 (abertura de 2025) - BP consolidado.", "Existência, integridade, avaliação e classificação dos saldos iniciais; consistência das políticas.",
              "Distorções nos saldos iniciais que afetam 2025; mudança de políticas não divulgada. Caso real: 2025 é o 1º ano da KPMG, sucedendo a EY.",
              f"DFP 2024 original (F03) x comparativos da DFP 2025 (F02): {len(si)} contas comparadas (100%).",
              [("Comparar 100% das contas do BP de 31/12/2024 publicado x comparativo de 2025", "R", "X-PT510"),
               ("Ler o relatório do auditor anterior (EY, 12/03/2025): tipo de opinião e PAA", "R", "F03"),
               ("Verificar a consistência das políticas (moeda funcional, esforços bem-sucedidos, UOP, ARO)", "R", "NE 2"),
               ("Revisar os papéis do auditor antecessor (A3) e comunicação (NBC PG 100)", "P", "Sem acesso"),
               ("Testar movimentações de 2025 que corroboram saldos iniciais (recebimentos, pagamentos)", "R", "DFC/ITR")],
              ul([f"Riscos herdados dos PAA da EY → {ref('PT 315')}", "07_Dados_Publicos/dfp2024_*; 06_Resultados/PT510_saldos_iniciais.csv"]),
              f"<p>Auditor anterior: {ne.AUDITOR['anterior']}. PAA de 2024:</p>{paa}<p><b>Comparação de saldos:</b> {len(dif)} diferenças encontradas, todas no PL:</p>{t}" +
              "<p>Trata-se de uma reclassificação de R$ 29.885 mil de \"Ações em Tesouraria\" para \"Lucro na venda de Ações em Tesouraria\", sem efeito no PL total e sem nota de reapresentação (CPC 23 item 49 / CPC 26 item 41) → D04 no PT 450. Políticas consistentes; a mudança de estimativa (vida de Peregrino 2031 → 2034) é prospectiva a partir de 2026 e está divulgada (NE 2.22.1).</p>",
              "Saldos iniciais consistentes com a DFP 2024 auditada sem modificação, exceto uma reclassificação imaterial no PL sem divulgação. Opinião anterior não modificada → sem efeito na opinião de 2025.",
              "Sem acesso aos papéis da EY. As notas da DFP 2024 estão em formato não pesquisável (F04), o que impediu extrair as taxas de ARO de 2024.")


def pt520():
    an = csv("PT520_procedimentos_analiticos.csv")
    linhas = [[x.conta, x.expectativa_metodo, br(x.valor_esperado), br(x.valor_registrado), br(x.diferenca_pct, 1, pct=True),
               br(x.limite_investigacao), "Sim" if x.investigar else "Não"] for x in an.itertuples()]
    dec = csv("PT520_decomposicao_da.csv")
    t2 = tab(["Ativo", "D&A 2025 (R$ mil)"], [[x.ativo, br(x.depreciacao_2025)] for x in dec.itertuples()], num_cols=(1,))
    hv = csv("PT520_analise_horizontal_vertical.csv", dtype={"CD_CONTA": str})
    hv = hv[hv["acima_limite"]].head(14)
    t3 = tab(["Conta", "2024", "2025", "Var. %"], [
        [f"{x.CD_CONTA} {x.DS_CONTA}", br(x._4), br(x._5), br(x.var_pct, 0, pct=True)] for x in hv.itertuples()], num_cols=(1, 2, 3))
    return pt("PT 520", "Procedimentos analíticos", "NBC TA 520 itens 5-7, A1-A19",
              "Construir expectativas, definir precisão e limites de investigação, calcular relações e variações e investigar diferenças, com cálculos reproduzíveis.",
              "Receita, D&A, despesas financeiras, ARO (atualização), royalties; BP/DRE (horizontal/vertical).",
              "Ocorrência, exatidão, integridade, avaliação.", "Variações inesperadas não explicadas; expectativas pouco precisas usadas como evidência suficiente.",
              "Dados independentes: Brent (EIA), PTAX (BCB), volumes (RA - não auditados), notas da DFP.",
              [("Desenvolver expectativas independentes com dados externos (Brent, PTAX)", "R", "X-PT520"),
               ("Definir precisão e limite de investigação; comparar com a ME", "R", "Tabela"),
               ("Investigar diferenças de D&A e ARO por decomposição das notas", "R", "Tabela"),
               ("Indagar a administração e obter corroboração das explicações", "P", "Sem acesso"),
               ("Benford e análise horizontal/vertical", "R", "Abaixo")],
              ul(["03_Planilhas/PT520_Analiticos.xlsx; 05_Codigo/03_analiticos.py", f"Riscos → {ref('PT 315')}; ARO → {ref('PT 540')}"]),
              tab(["Conta", "Expectativa (método)", "Esperado", "Registrado", "Dif. %", "Limite", "Investigar"], linhas, num_cols=(2, 3, 4, 5),
                  larg=["16%", "38%", "10%", "10%", "8%", "10%", "8%"]) +
              "<p><b>Receita:</b> diferença de +1,5%, dentro da precisão de 5%; o preço implícito realizado (US$ 66,09/bbl) é coerente com o Brent médio menos um desconto de cerca de US$ 3. Como o limite (R$ 688 mi) supera a ME, o analítico <i>não</i> basta sozinho e é combinado com testes de corte (PT 330). <b>Juros e royalties:</b> dentro da precisão. <b>D&A (+41,5%):</b> investigada pela decomposição abaixo. Peregrino responde por R$ 2,995 bi (51%), pois a UOP usa reservas provadas desenvolvidas até o fim da concessão então vigente (2031) e uma base a valor justo; o RA corrobora (D&A +112% em US$). Resíduo de R$ 151 mi entre DFC e movimentações (hipótese de conversão). <b>ARO (+37,8%):</b> não explicada com dados públicos; hipótese: taxas de desconto de abertura maiores que as de fim de ano (a atualização das taxas elevou a provisão em R$ 722,5 mi). Procedimento planejado: obter as taxas de 2024.</p>"
              + "<h3>Decomposição da D&A 2025 (NE 8, 9, 15)</h3>" + t2 + "<h3>Variações acima do limite (> ME e > 10%) - análise horizontal</h3>" + t3 +
              "<p class='small'>Explicações das variações: aquisição de Peregrino (imobilizado, intangível, ARO, estoques); emissões de bonds e debêntures (empréstimos); capitalização da reserva de investimentos (capital social); conversão USD/BRL de 6,19 para 5,50 (ajustes de conversão); fornecedores +210% (operação de Peregrino assumida em nov/2025).</p>" +
              fig("g06_benford.png", "Figura 5 - Benford na base sintética (indicador de manipulação - NBC TA 240)."),
              "Receita, juros e royalties são coerentes com as expectativas. D&A foi explicada qualitativamente por Peregrino, com resíduo de conversão. A diferença da ARO segue como ponto em aberto para o PT 540.",
              "Volumes vêm do RA (não auditado); a expectativa de D&A é aproximada (linear até a concessão), porque as reservas PD por campo não são públicas.")


def pt530():
    par = tab(["Parâmetro", "Base entregue", "Após ajustes simulados"], [
        ["População (itens com VC > 0)", br(MUS["populacao_itens"]), br(MUS2["populacao_itens"])],
        ["Valor contábil da população (R$)", br(MUS["valor_contabil_populacao_brl"], 2), br(MUS2["valor_contabil_populacao_brl"], 2)],
        ["Confiança / fator", "95% / 3,0", "95% / 3,0"],
        ["Distorção tolerável / esperada (R$)", "93.000.000 / 9.300.000", "93.000.000 / 9.300.000"],
        ["Tamanho n = VC x 3 / (DT - DE x 1,6)", br(MUS["tamanho_amostra_calculado"]), br(MUS2["tamanho_amostra_calculado"])],
        ["Intervalo amostral J (R$)", br(MUS["intervalo_amostral_brl"], 2), br(MUS2["intervalo_amostral_brl"], 2)],
        ["Itens distintos selecionados / estrato topo", f"{br(MUS['itens_selecionados'])} / {MUS['itens_topo']}", f"{br(MUS2['itens_selecionados'])} / {MUS2['itens_topo']}"],
        ["Cobertura de valor", br(MUS["cobertura_valor"], 1, pct=True), br(MUS2["cobertura_valor"], 1, pct=True)],
        ["Distorções encontradas (itens)", MUS["distorcoes_encontradas"], MUS2["distorcoes_encontradas"]],
        ["Distorção projetada (R$)", br(MUS["distorcao_projetada_brl"], 2), br(MUS2["distorcao_projetada_brl"], 2)],
        ["Precisão básica + provisão incremental (R$)", br(MUS["precisao_basica_brl"] + MUS["provisao_incremental_brl"], 2), br(MUS2["precisao_basica_brl"], 2)],
        ["<b>Limite superior de distorção (R$)</b>", f"<b>{br(MUS['limite_superior_distorcao_brl'], 2)}</b>", f"<b>{br(MUS2['limite_superior_distorcao_brl'], 2)}</b>"],
        ["Conclusão", "Rejeitar - LSD > tolerável", "Aceitar - LSD ≤ tolerável"],
    ], larg=["44%", "28%", "28%"], num_cols=(1, 2))
    return pt("PT 530", "Amostragem em auditoria - base simulada obrigatória", "NBC TA 530 itens 6-15, A1-A23 e Apêndices 2-4",
              "Aplicar amostragem à base simulada: população, unidade amostral, método, tamanho, seleção, risco amostral, tratamento e projeção de erros.",
              "Imobilizado - base sintética de " + br(RT["base_linhas"]) + " registros.", "Existência e avaliação (MUS); eficácia do controle de aprovação (atributos).",
              "Risco amostral (aceitação incorreta); risco não amostral (erro na avaliação do item).",
              "<b>População:</b> registros com valor contábil positivo (os negativos são tratados em 100% pelo T03). <b>Unidade amostral:</b> cada real de valor contábil (MUS). <b>Seleção:</b> sistemática com início aleatório (semente 231019943); itens ≥ J pertencem ao estrato topo e são testados em 100%.",
              [("Definir população, unidade amostral e parâmetros", "S", "X-PT530"), ("Calcular tamanho e selecionar por PPS sistemático", "S", "Amostra_MUS"),
               ("Testar cada item contra a documentação-suporte simulada", "S", "documentacao_suporte_simulada"),
               ("Projetar distorções (taint x J) e calcular o LSD (Stringer/Poisson)", "S", "Avaliacao_MUS"),
               ("Amostragem por atributos do controle de aprovação (n=93)", "S", "Atributos_Controle"),
               ("Reaplicar após as correções da administração", "S", "PT 450")],
              ul(["03_Planilhas/PT530_Amostragem.xlsx (fórmulas verificadas)", "06_Resultados/PT530_amostra_mus.csv; PT530_amostra_atributos.csv", f"Distorções → {ref('PT 450')}"]),
              par + f"<p><b>Atributos:</b> n=93, {ATR['desvios_encontrados']} desvios; limite superior de {br(ATR['limite_superior_desvio'],1,pct=True)} ≤ 5% tolerável → controle considerado efetivo para fins de amostragem. Isso é coerente com a taxa real de desvios na população (0,05%), mesmo havendo deficiência de configuração (PT 265): o controle falha raramente, mas falha em itens de alto risco. Por isso o teste em 100% (CAAT) é complementar à amostragem.</p>" +
              f"<p><b>Eficácia da projeção:</b> distorção projetada de R$ {br(MUS['distorcao_projetada_brl']/1e6,1)} mi contra distorção real conhecida (gabarito) de R$ {br((RT['superavaliacao_real_brl']+RT['subavaliacao_real_brl'])/1e6,1)} mi líquida. O MUS estimou bem a magnitude.</p>" +
              fig("g08_mus.png", "Figura 6 - Composição do LSD antes e depois das correções simuladas."),
              "Base entregue: saldo rejeitado (LSD de R$ 535 mi contra tolerável de R$ 93 mi). Após as correções simuladas, saldo aceito (LSD de R$ 78 mi).",
              "Dados sintéticos; o \"valor auditado\" é a documentação-suporte simulada; no caso real haveria risco não amostral na avaliação de documentos.")


def pt540():
    s = csv("PT540_sensibilidade_aro.csv")
    tot = s[s["campo"].str.startswith("TOTAL")].set_index("cenario")
    por = s[(s["cenario"] == "Base") & s["ano_abandono"].notna()][["campo", "ano_abandono", "taxa", "custo_futuro_estimado", "valor_presente"]]
    t1 = tab(["Campo", "Ano abandono", "Taxa", "Custo futuro implícito (R$ mil)", "VP = saldo NE 17 (R$ mil)"],
             [[x.campo, int(x.ano_abandono), br(x.taxa, 2, pct=True), br(x.custo_futuro_estimado), br(x.valor_presente)] for x in por.itertuples()], num_cols=(1, 2, 3, 4))
    t2 = tab(["Cenário", "Provisão (R$ mil)", "Variação (R$ mil)", "Variação / MG"],
             [[c, br(r.valor_presente), br(r.variacao), br(r.variacao / 155_000, 1) + "x"] for c, r in tot.iterrows()], num_cols=(1, 2, 3))
    vies = tab(["Indicador de viés (item 32, A133)", "Observação", "Direção"], [
        ["Atualização das taxas em 31/12/2025", "+R$ 722,5 mi na provisão (contra o ativo)", "Conservadora (aumenta passivo)"],
        ["Extensão da vida de Peregrino (2031 → 2034)", "Reduz o VP do ARO e a taxa de D&A a partir de 2026; baseada em redução de OPEX pela PRIO", "Otimista - julgamento a desafiar"],
        ["Albacora Leste - abandono em 2031 (fim da concessão)", "Prazo limitado pelo contrato, não pela economicidade", "Neutro"],
        ["Ausência de divulgação de sensibilidade na NE 17", "CPC 26 item 125 (fontes de incerteza)", "Divulgação insuficiente"],
        ["IR diferido: realização de prejuízos até 2041", "Depende de Brent e reservas; o Brent subiu em 2026 (EIA: média de US$ 95 até out)", "Evidência posterior favorável"],
    ], larg=["34%", "44%", "22%"])
    return pt("PT 540", "Estimativas contábeis - provisão para abandono (ARO)", "NBC TA 540 (R2) itens 13-39, A1-A152",
              "Selecionar estimativa relevante e avaliar método, premissas, dados, incerteza e possível viés da administração; executar análise de sensibilidade.",
              "Provisão para abandono de instalações - R$ 5.447.438 mil (NE 17) - PAA da KPMG. Complementar: IR diferido de R$ 8.121.172 mil (NE 16).",
              "Avaliação; integridade; divulgação.", "Incerteza de estimativa alta (prazos de 2026 a 2041; custos offshore; taxa); complexidade; subjetividade; possível viés.",
              "NE 17 (saldos, taxas, prazos), NE 9.d (complemento de R$ 1,32 bi), NE 2.22.1 (vida de Peregrino), certificação D&M (F08). Polvo excluído (líquido do fundo).",
              [("Entender o método (VP do custo em USD inflacionado a 2% e descontado a 7,41%-8,12%)", "R", "NE 17"),
               ("Derivar o custo futuro implícito por campo e sensibilizar taxa, custo e prazo", "R", "X-PT540"),
               ("Avaliar indicadores de viés", "R", "Tabela"),
               ("Avaliar os especialistas (D&M; engenharia de custos): competência, objetividade (NBC TA 500 item 8)", "P", "Sem acesso aos laudos"),
               ("Comparar custos unitários de abandono com benchmarks/contratos", "P", "Sem dados"),
               ("Desenvolver estimativa pontual/intervalo do auditor (item 29)", "R", "Intervalo abaixo")],
              ul(["03_Planilhas/PT540_PT570_Estimativas_Continuidade.xlsx (fórmulas)", f"Analítico de ARO → {ref('PT 520')}; IR diferido → {ref('PT 570')}"]),
              t1 + t2 + fig("g05_tornado_aro.png", "Figura 7 - Tornado: +20% no custo eleva a provisão em R$ 1,09 bi (7x a MG).") + vies,
              f"A estimativa é altamente sensível: ±1 p.p. na taxa produz de R$ {br(tot.loc['Taxa +1 p.p.','variacao'])} a R$ +{br(tot.loc['Taxa -1 p.p.','variacao'])} mil; +10% no custo, R$ +{br(tot.loc['Custo +10%','variacao'])} mil. O intervalo razoável do auditor (custo ±10%, taxa ±0,5 p.p.) é muito mais amplo que a MG, o que confirma o PAA. Não há evidência pública de viés sistemático (as revisões vão nos dois sentidos). Recomenda-se divulgar a sensibilidade (CPC 26 item 125).",
              "Custos futuros não são públicos; o custo implícito foi derivado do VP. O prazo de Tubarão Azul é premissa didática.")


def pt550():
    rp = tab(["Parte relacionada / vínculo", "Saldo 2025 (R$ mil)", "Saldo 2024 (R$ mil)", "Natureza"],
             [[n, br(a), br(b), "Intragrupo (eliminado no consolidado)"] for n, a, b in ne.NE21_PARTES], num_cols=(1, 2))
    ext = tab(["Vínculo", "Informação", "Fonte", "Avaliação"], [
        ["Administração (pessoal-chave)", "Remuneração de R$ 34.932 mil (2024: 27.185); 84% em ações", "NE 21 (p. 88)", "Acima da materialidade específica (R$ 1.750 mil) → testar a totalidade"],
        ["Acionistas > 5%", "FMR 5% e Schroder 5% (dez/2025); BlackRock 7,52% (abr/2026); Orbis 5,05% (out/2026); Goldman Sachs 4,91% em derivativos (mar/2026)", "NE 20; F07", "Sem controlador; FCA classifica o controle como \"Privado Holding\" - divergência terminológica a esclarecer"],
        ["Controladas e mútuos", "Mútuos Lux Holding (7,03% a.a.) e Forte (6,125% a.a.); juros de R$ 48.345 mil", "NE 21", "Eliminados; taxas próximas ao custo de dívida (6,36%)"],
        ["Plano de opções", "Programas XIII-3; aumento de capital jan/2026 (exercício)", "NE 20.2; F07", "Transações com administradores - divulgadas"],
        ["Parceiros de JOA", "Repsol Sinopec (10% ABL), Equinor (20% Peregrino)", "NE 1, 18", "Não são partes relacionadas (CPC 05) - operações conjuntas"],
    ], larg=["20%", "36%", "14%", "30%"])
    return pt("PT 550", "Partes relacionadas", "NBC TA 550 itens 11-27, A1-A50; CPC 05 (R1)",
              "Mapear vínculos, saldos e transações; avaliar completude e divulgações; planejar a identificação de operações não informadas.",
              "Transações e saldos com partes relacionadas; remuneração do pessoal-chave.", "Integridade, ocorrência, divulgação.",
              "Operações não identificadas (por exemplo, fornecedores ligados a administradores); a NE 21 cobre só a controladora.",
              "NE 20, 21, Formulário de Referência (seção 11 - planejado), fatos relevantes de participação acionária (F07).",
              [("Mapear vínculos e saldos divulgados", "R", "Tabelas"), ("Confirmar eliminação no consolidado dos mútuos intragrupo", "R", "NE 2.3, 7"),
               ("Cruzar o cadastro de fornecedores (base) com CNPJ/QSA de empresas de administradores", "P", "Base de fornecedores real necessária"),
               ("Ler atas do CA e do Comitê; Formulário de Referência item 11.2", "P", "-"),
               ("Indagar a administração sobre partes relacionadas e transações fora do curso normal", "P", "-"),
               ("Testar remuneração do pessoal-chave contra a proposta da AGO (17/04/2026)", "P", "F07 - assembleia")],
              ul([f"Materialidade específica → {ref('PT 320')}; representações → {ref('PT 580')}"]),
              rp + ext,
              "As divulgações públicas são coerentes; não há controlador. A completude não pode ser concluída sem os procedimentos planejados.",
              "Sem acesso ao cadastro de fornecedores e às atas.")


def pt560():
    ev = [
        ["02/01/2026 (FR, versão 2 em 09/01)", "Aumento de capital por exercício de opções (3.137.840 ações / R$ 95,1 mi; reapresentado com 3.039.475 ações / R$ 91,0 mi)", "Tipo 2 - não ajusta", "Não divulgado na NE 31; abaixo da MG. Ceticismo: duas versões com números diferentes - verificar retificação"],
        ["03/03/2026 (FR)", "Licença de Operação de Wahoo (IBAMA)", "Tipo 2 - não ajusta", "Divulgado na NE 31.1 ✓; corrobora a recuperabilidade de R$ 6,57 bi em desenvolvimento"],
        ["10/03/2026 (FR)", "Certificação de reservas D&M (data-base 01/01/2026): 1P de 757,3 MMbbl", "Tipo 1 - evidência de condições em 31/12", "Usada no impairment (NE 19) e na ARO ✓"],
        ["10/03/2026", "<b>Data do relatório do auditor e da aprovação das DFs</b>", "Marco", "Eventos posteriores: NBC TA 560 itens 10-17"],
        ["16/03/2026 (FR)", "Licença de perfuração de 14 poços em Frade", "Após o relatório", "Nenhuma ação; positivo para a continuidade"],
        ["19/03 a 16/06/2026 (FR)", "Início de produção de Wahoo; 4 poços; 40 kbpd", "Após o relatório", "Corrobora a avaliação do imobilizado em andamento"],
        ["05/05/2026 (FR)", "Renúncia do Diretor de Operações; eleição de sucessor", "Após o relatório", "Nenhum efeito contábil"],
        ["1T26 / 2T26 (ITR)", "Lucro do 1S26 de R$ 4,37 bi; PL de R$ 28,2 bi; bond 2026 quitado (US$ 168,7 mi); alavancagem de 1,5x", "Após o relatório", "Nenhuma dúvida de continuidade (PT 570)"],
        ["Ago/2026", "Fechamento dos 20% restantes de Peregrino ainda pendente (apresentação 2T26)", "Após o relatório", "Compromisso divulgado na NE 9.d ✓"],
        ["07/10/2026 (FR)", "Leilão ANP: blocos Magnetita e Hematita (bônus de R$ 94,6 mi)", "Após o relatório", "Compromisso futuro; não ajusta"],
        ["Jan-out/2026", "Brent médio de US$ 95,34 (até out); US$ 115 em 20/10/2026", "Após o relatório", "Prospectivo - favorável ao IR diferido e ao impairment"],
    ]
    return pt("PT 560", "Eventos subsequentes", "NBC TA 560 (R1) itens 6-17, A1-A18; CPC 24",
              "Fixar a data de corte, examinar publicações posteriores ao encerramento e distinguir eventos que exigem ajuste dos que exigem divulgação.",
              "Período de 01/01/2026 até a data de corte (23/10/2026); relatório de 10/03/2026.", "Integridade, avaliação, divulgação.",
              "Evento de tipo 1 não ajustado; evento de tipo 2 relevante não divulgado; fato descoberto após o relatório.",
              "Data de corte: <b>23/10/2026</b>. População: 44 documentos IPE de 2026 da PRIO (fatos relevantes, comunicados, assembleias), ITR 1T26 e 2T26, Brent EIA.",
              [("Fixar a data de corte e listar todos os fatos relevantes e comunicados de 2026", "R", "07_Dados_Publicos/ipe2026_prio.csv"),
               ("Ler a NE 31 e comparar com os eventos até 10/03/2026", "R", "p. 98"),
               ("Classificar eventos em tipo 1 (ajuste) e tipo 2 (divulgação)", "R", "Tabela"),
               ("Analisar ITR 2026 como evidência posterior (realização de estoques, dívida, PL)", "R", "F05"),
               ("Indagar a administração e ler atas até a data do relatório (item 7)", "P", "-"),
               ("Avaliar fatos conhecidos após o relatório (itens 14-17)", "R", "Nenhum exige reemissão")],
              ul([f"Continuidade → {ref('PT 570')}; estoques → {ref('PT 501')}; representações datadas → {ref('PT 580')}"]),
              tab(["Data", "Evento", "Classificação", "Tratamento / avaliação"], ev, larg=["16%", "38%", "16%", "30%"]),
              "Não há evento de tipo 1 não ajustado. O único evento de tipo 2 até a data do relatório (LO de Wahoo) está divulgado. O aumento de capital de jan/2026 (≈R$ 95 mi) não foi divulgado, mas está abaixo da MG. Nenhum fato posterior ao relatório exigiria reemissão.",
              "Sem indagações e atas; a pesquisa limita-se a divulgações públicas.")


def pt570():
    ind = csv("PT570_indicadores.csv")
    t = tab(["Indicador", "2025", "2024", "Referência"],
            [[x.indicador, br(x._2, 2) if abs(x._2) < 100 else br(x._2), (br(x._3, 2) if abs(x._3) < 100 else br(x._3)) if pd.notna(x._3) else "-", x.referencia] for x in ind.itertuples()],
            num_cols=(1, 2))
    return pt("PT 570", "Continuidade operacional", "NBC TA 570 itens 10-24, A1-A35 (versão vigente para 2025; a (R1) do DOU de 25/09/2026 foi consultada e não aplicada)",
              "Analisar liquidez, endividamento, cláusulas contratuais, fluxos de caixa e eventos adversos; avaliar incertezas relevantes e divulgações.",
              "Base de continuidade (NE 2.2); dívida e covenants (NE 13-14); liquidez (NE 29).", "Apresentação e divulgação (base contábil); classificação da dívida.",
              "Descumprimento de covenant (vencimento antecipado/restrição); concentração de vencimentos; dependência do Brent.",
              "BP, DRE, DFC, NE 13, 14, 29; ITR e apresentações de 2026 (evidência posterior).",
              [("Calcular indicadores de liquidez, endividamento e cobertura", "R", "X-PT570"),
               ("Recalcular o covenant (dívida líquida/EBITDA ajustado ≤ 2,5x) com e sem pró-forma de Peregrino", "R", "Gráfico"),
               ("Analisar vencimentos (NE 29) contra caixa e FCO", "R", "Gráfico"),
               ("Obter o certificado de covenant enviado aos credores e o cálculo da administração", "P", "Sem acesso"),
               ("Avaliar a projeção de caixa da administração por 12 meses (item 13)", "P", "Sem acesso"),
               ("Examinar evidência posterior: 2T26 (1,5x), bond 2026 quitado, lucro do 1S26", "R", "F10, F05")],
              ul(["03_Planilhas/PT540_PT570_Estimativas_Continuidade.xlsx", f"Eventos → {ref('PT 560')}"]),
              t + fig("g04_alavancagem.png", "Figura 8 - Alavancagem: sem pró-forma (2,91x) acima de 2,5x; com o EBITDA LTM de +40% de Peregrino (premissa de US$ 35/bbl) cai para 2,15x; a companhia divulgou 1,5x no 2T26.") +
              fig("g09_vencimentos.png", "Figura 9 - Vencimentos: R$ 6,0 bi em 12 meses contra caixa de R$ 3,4 bi e FCO de R$ 8,2 bi."),
              f"<p>Sem o pró-forma, a dívida líquida de R$ {br(IND['divida_liquida'])} mil sobre EBITDA ajustado de R$ {br(IND['ebitda_aj'])} mil dá 2,91x. O contrato inclui o EBITDA LTM da participação adquirida (RA p. 40), o que exige ≥ R$ 1,33 bi de pró-forma; a premissa didática gera R$ 2,85 bi. A consequência contratual de excesso é <b>restrição a novas dívidas</b>, não vencimento antecipado (NE 13). Não há incerteza relevante sobre a continuidade: FCO de R$ 8,2 bi, liquidez corrente de 1,82, acesso a mercado (bond de US$ 700 mi em out/2025) e evidência posterior favorável. Recomenda-se divulgar o cálculo do covenant com o ajuste pró-forma.</p>",
              "O uso da base de continuidade é apropriado; não há incerteza relevante a divulgar.",
              "O cálculo contratual exato (definições, câmbio, IFRS 16) não é público; o pró-forma é premissa didática.")


def pt580():
    carta = """<div class="letter"><div class="wm">MINUTA DIDÁTICA - NÃO ASSINADA - SEM VALIDADE</div>
<p>[Local], [data = data do relatório do auditor]. Ao [auditor]. Em conexão com sua auditoria das DFs individuais e consolidadas da PRIO S.A. em 31/12/2025, declaramos:</p>
<ol class="small">
<li>Cumprimos nossa responsabilidade pela elaboração das DFs conforme CPC/IFRS, conforme os termos do trabalho (NBC TA 580 item 10).</li>
<li>Fornecemos acesso a todas as informações, registros e pessoas, inclusive dos componentes no exterior (item 11).</li>
<li>Todas as transações foram registradas e refletidas nas DFs.</li>
<li>As premissas significativas das estimativas - provisão para abandono (taxas, custos, prazos), IR diferido (projeções de Brent, CAPEX, OPEX, reservas D&M), UOP e alocação do preço de Peregrino - são razoáveis (NBC TA 540 item 37).</li>
<li>Divulgamos todas as partes relacionadas e transações conhecidas (NBC TA 550 item 26).</li>
<li>Todos os eventos subsequentes que exigem ajuste ou divulgação foram tratados (NBC TA 560 item 9).</li>
<li>Os efeitos das distorções não corrigidas (anexo) são imateriais, individualmente e em conjunto (NBC TA 450 item 14).</li>
<li>Divulgamos os resultados de nossa avaliação de risco de fraude e todo conhecimento de fraude ou suspeita (NBC TA 240 item 39).</li>
<li>Divulgamos todos os casos conhecidos de descumprimento de leis, inclusive a interdição do FPSO Peregrino pela ANP (NBC TA 250 item 16).</li>
<li>Cumprimos os covenants contratuais em 31/12/2025 e em todas as medições trimestrais, com o cálculo informado aos credores.</li>
<li>Os litígios e as reclamações foram avaliados e contabilizados/divulgados conforme o CPC 25 (NBC TA 501 item 12).</li>
<li>A base de continuidade operacional é apropriada (NBC TA 570 item 16).</li></ol>
<p>Diretor-Presidente: __________ &nbsp; Diretor Financeiro: __________ (campos em branco)</p></div>"""
    return pt("PT 580", "Representações formais - minuta e limites", "NBC TA 580 (R1) itens 9-20, A1-A26 e Apêndices",
              "Preparar minuta didática da carta de representações da administração e explicar por que ela não substitui outras evidências.",
              "Representações da Diretoria (CEO e CFO).", "Todas (complementar).",
              "Representações contraditórias com outras evidências; recusa da administração.",
              "Requisitos de representação das NBC TA 240, 250, 450, 501, 540, 550, 560, 570.",
              [("Redigir a minuta com representações gerais e específicas", "S", "Minuta"),
               ("Datar na data do relatório e obter as assinaturas", "P", "-"),
               ("Avaliar a consistência com as evidências (item 16)", "R", "Covenant x PT 570; NE 30 x D01")],
              ul([f"Distorções não corrigidas anexadas → {ref('PT 450')}"]),
              "<p><b>Por que não substitui outras evidências:</b> (i) é evidência gerada pela própria administração, de menor confiabilidade (NBC TA 500 A31); (ii) por si só não fornece evidência suficiente sobre nenhum assunto (item 4); (iii) não comprova existência, valor ou ocorrência; por exemplo, declarar o cumprimento do covenant não substitui o recálculo (PT 570), e declarar a razoabilidade da ARO não substitui a sensibilidade e a avaliação dos especialistas (PT 540); (iv) se contradisser outras evidências, como a divergência da NE 30, reduz a confiança nas demais representações (item 17).</p>",
              "A minuta cobre as representações exigidas; seu valor é complementar.", "Minuta não assinada.", carta)


def pt600():
    grupo = tab(["Entidade", "Função", "Participação", "País"], [list(g) for g in ne.GRUPO], larg=["36%", "34%", "18%", "12%"])
    co = csv("PT600_componentes.csv")
    t = tab(["Componente", "Receita (R$ mil)", "% receita", "% ativo (imob.+intang.)", "Significativo?", "Materialidade do componente"],
            [[x.componente, br(x.receita_liquida), br(x.pct_receita, 1, pct=True), br(x.pct_ativo_longo, 1, pct=True), x.significativo, br(x.materialidade_componente)]
             for x in co.itertuples()], num_cols=(1, 2, 3, 5), larg=["28%", "12%", "9%", "11%", "26%", "14%"])
    soc = tab(["Evento societário 2025", "Data"], [list(e) for e in ne.EVENTOS_SOCIETARIOS_2025])
    return pt("PT 600", "Auditoria de grupos - componentes e consolidação", "NBC TA 600 (R2) itens 12-49, A1-A160",
              "Mapear o grupo, seus componentes e o processo de consolidação; avaliar riscos, materialidade dos componentes, envolvimento de auditores de componentes e suficiência das evidências.",
              "Consolidação de 12+ entidades (Brasil, Luxemburgo, Áustria, Holanda, EUA, Namíbia).", "Integridade da consolidação; eliminações; conversão; classificação entre componentes.",
              "Eliminações incompletas de mútuos (por exemplo, empréstimos Stellina/Contina de R$ 16 bi na aquisição); conversão USD/BRL; incorporações em 2025; ativos no componente errado.",
              "NE 2.3, 2.4, 7, 9.c, 22, 28; base sintética (teste T10). Critério de significância: >15% da receita ou do ativo total.",
              [("Mapear a estrutura do grupo e os eventos societários", "R", "Tabelas"), ("Determinar componentes significativos e suas materialidades", "R", "X-PT600"),
               ("Entender o processo de consolidação: moeda funcional USD, conversão, eliminações", "R", "NE 2.3-2.4"),
               ("Conferir a reconciliação controladora x consolidado (PL e resultado)", "R", "Abaixo"),
               ("Instruções aos auditores de componentes (Lux, Áustria) e avaliação de competência/independência", "P", "-"),
               ("Testar a alocação de ativos por entidade (T10)", "S", "40 exceções")],
              ul(["03_Planilhas/PT450_PT600_Distorcoes_Componentes.xlsx", f"Materialidade de grupo → {ref('PT 320')}"]),
              grupo + soc + t +
              f"<p><b>Consolidação:</b> PL da controladora = PL consolidado (R$ {br(conta('BPP','2.03'))} mil; sem não controladores). Resultado da controladora (R$ 2.251.479 mil) = consolidado ✓. Investimento: PrioOG de R$ 26.139.413 + PrioIntl de R$ 149.469 = R$ 26.288.882 mil (NE 7). Eliminações relevantes: mútuos Lux/Forte com a controladora (R$ 446.361 mil) e a dívida da Tigris com a Lux (origem Stellina). <b>Simulação:</b> o T10 encontrou 40 ativos de Peregrino lançados na Prio Bravo. Não altera o consolidado, mas distorceria os componentes e o IR por entidade.</p>",
              "Três componentes significativos (Tigris/Peregrino, Forte/Frade-Wahoo, Forte/ABL) exigem auditoria completa. Bravo e as entidades de trading recebem procedimentos específicos. A evidência seria suficiente com o envolvimento planejado dos auditores de componentes.",
              "Sem demonstrações individuais das controladas nem comunicação com auditores de componentes.")


def secao_base():
    dic = pd.read_csv(RAIZ / "02_Base_Simulada" / "dicionario_variaveis.csv")
    td = tab(["Variável", "Tipo", "Descrição", "Exemplo"], dic.values.tolist(), larg=["20%", "10%", "50%", "20%"])
    conc = csv("PT500_conciliacao_base_x_notas.csv", index_col=0)
    tc = tab(["Classe", "Saldo nota (R$ mil)", "Saldo base (R$ mil)", "Diferença", "Explicada por erros inseridos", "Não explicada"],
             [[i, br(r.saldo_nota_rmil), br(r.saldo_base_rmil, 2), br(r.diferenca_rmil, 2), br(r.explicado_erros_inseridos_rmil, 2), br(r.diferenca_nao_explicada_rmil, 2)]
              for i, r in conc.iterrows()], num_cols=(1, 2, 3, 4, 5), cls="small")
    return f"""<section class="pt" id="BS"><div class="pt-head"><div class="pt-code">BS</div><div class="pt-title"><h2>Base de dados simulada obrigatória - Imobilizado</h2>
<div class="pt-norma">Instruções item 3 | NBC TA 500, 520, 530 | <b>*** DADOS SINTÉTICOS PARA FINS DIDÁTICOS - NÃO SÃO REGISTROS REAIS DA PRIO ***</b></div></div></div>
<h3>1. Escolha da conta e materialidade</h3>
<p>Imobilizado consolidado (BP 1.02.03): <b>R$ 31.142.804 mil = 48,5% do ativo total</b>. É a maior conta do ativo, à frente de intangível (23,4%) e IR diferido (12,7%) - Figura 1.
Equivale a 201 vezes a materialidade global e concentra riscos significativos (Peregrino, UOP, capitalização). Composição: NE 8 (23 classes, R$ 30.532.404 mil) + NE 15 (direito de uso, 4 classes, R$ 610.400 mil).</p>
<h3>2. Premissas e método de geração (05_Codigo/01_gerar_base.py)</h3>
<ul>
<li>Cada linha = um registro analítico do subledger: componente patrimonial (FPSO, plataforma, poço, equipamento submarino), lote de material de poço, sobressalente, gasto capitalizado de desenvolvimento (OS/NF), item administrativo ou contrato de arrendamento. Não há repetição artificial: 518.200 registros distintos antes dos erros.</li>
<li>Número de linhas por classe proporcional à natureza (ex.: 190.000 gastos de desenvolvimento, 165.000 lotes de material e 9.000 componentes da plataforma de Peregrino). Valores por distribuição log-normal (cauda longa típica de ativos), alocados em centavos inteiros para fechar <b>exatamente</b> com custo, depreciação, ajuste de conversão e saldo de cada classe da NE 8/15.</li>
<li>Depreciação: UOP distribuída por maturidade do item; linear coerente com taxa e data de entrada em operação (permite recálculo exato - T05); itens em andamento sem depreciação (CPC 27 item 55).</li>
<li>Datas e origens compatíveis com os fatos: Peregrino em 05/12/2024 (Stellina) e 11/11/2025 (Equinor +40%); ARO de Albacora Leste em 2025; FPSO Valente desde 2019 etc. Entidade e campo seguem a NE 1/7.</li>
<li>Controles simulados: usuários USR001-030, gerentes APR01-08 (alçada até R$ 5 mi) e diretores DIR01-03.</li>
<li>Semente 231019943: reprodução idêntica. Arquivo <code>base_imobilizado_sintetica.csv.gz</code> ({br(RT['base_linhas'])} linhas, ~26 MB) e <code>documentacao_suporte_simulada.csv.gz</code> (valores corretos, usados só para os itens amostrados).</li>
<li>Erros inseridos (655 registros, 10 tipologias) documentados em <code>registro_erros_inseridos.csv</code>, com valor original e inserido - gabarito para comparar com as exceções identificadas (PT 450).</li></ul>
{fig('g10_base_classes.png', 'Figura 10 - Distribuição dos registros sintéticos por classe.')}
<h3>3. Dicionário das variáveis</h3>{td}
<h3>4. Conciliação da base com o saldo contábil (R$ mil)</h3>
<p>Base limpa = BP 1.02.03 centavo a centavo (assert no script). Base entregue: R$ {br(RT['base_total_brl']/1000, 2)} mil; diferença de R$ {br(RT['diferenca_conciliacao_brl']/1000, 2)} mil, <b>100% explicada</b> pelos erros inseridos (não explicada: R$ {br(RT['diferenca_nao_explicada_rmil'], 2)}).</p>{tc}
<h3>5. Procedimentos executados com a base</h3>
<p>CAATs em 100% ({ref('PT 330')}); amostragem MUS e por atributos ({ref('PT 530')}); Benford e indicadores ({ref('PT 520')}); mapa de distorções e comparação inseridos x detectados ({ref('PT 450')}); deficiências simuladas ({ref('PT 265')}); componente errado ({ref('PT 600')}).</p>
<div class="lim"><b>Limitações.</b> A base reproduz totais reais, mas a distribuição interna (quantidade de itens, datas, usuários, fornecedores) é inventada. Nenhuma conclusão sobre a PRIO real decorre dela.</div>
<div class="sign"><div><b>Preparado por:</b> Matrícula 231019943 | <b>Data:</b> 23/10/2026</div><div><b>Revisado por:</b> ______________________ | <b>Data:</b> ____/____/______</div></div></section>"""


def anexo_programas():
    progs = {
        "A.1 Receitas": [("Analítico: volume vendido x Brent x PTAX x desconto; por campo e mês", "R"), ("Corte: cargas de 20/12/2025 a 10/01/2026 - B/L, fatura, Incoterm, data de transferência de controle", "P"),
                         ("Trading: contratos de compra e venda back-to-back; apresentação bruta x líquida (CPC 47 B34-B38)", "P"), ("Royalties/PE: recálculo sobre receita e preço de referência ANP", "R"),
                         ("Confirmação de recebíveis dos 5 maiores clientes", "S"), ("Deduções e despesas de comercialização reclassificadas para CPV em 2025 (NE 22)", "R")],
        "A.2 Disponibilidades": [("Confirmação bancária das 14 instituições (NE 3)", "P"), ("Conciliações bancárias de 31/12 e itens em trânsito", "P"),
                                 ("Classificação como equivalente de caixa (fundo cambial BTG R$ 439 mi; CPC 03 item 7)", "R"), ("Conversão de saldos em USD/EUR à PTAX de 31/12/2025 (5,5024)", "R")],
        "A.3 Estoques": [("Observação da contagem e da medição de tanques nos FPSOs em 31/12/2025", "P"), ("Custo médio ponderado e NRV (Brent de 31/12 de US$ 61,35)", "P"),
                         ("Realização subsequente (ITR 1T26/2T26)", "R"), ("Composição (óleo x consumíveis) e divulgação ausente - D02", "R")],
        "A.4 Imobilizado": [("Conciliação subledger x razão x NE 8 (base simulada)", "S"), ("MUS de existência/avaliação (n=1.209) e inspeção física de amostra", "S"),
                            ("Adições: AFE aprovada, capex x opex, juros capitalizados (CPC 20)", "S"), ("Transferências de R$ 874,6 mi para CPV - critério de capitalização", "P"),
                            ("Recálculo de UOP por campo com reservas PD da D&M", "P"), ("Indicadores de impairment (Brent, reservas, custos) e teste do ágio da Forte (9,61%)", "R"),
                            ("Alocação da aquisição de +40% de Peregrino (NE 9.d) e teste de concentração CPC 15 B7A", "R"), ("Direito de uso: novos contratos e encerramentos (ganho na NE 15)", "R")],
        "A.5 Passivos": [("Empréstimos: confirmação, cronograma, juros, covenants, classificação circulante", "R"), ("Debêntures e swaps: hedge accounting (CPC 48 6.4.1), MTM em ORA", "R"),
                         ("Fornecedores: busca de passivos não registrados (pagamentos de jan-fev/2026)", "P"), ("Provisões e contingências: cartas jurídicas; conciliação NE 30 x BP (D01)", "R"),
                         ("Adiantamentos de parceiros (NE 18) e cash calls", "P"), ("Tributos a pagar: royalties/PE, IRPJ/CSLL, Pillar 2", "R")],
        "A.6 Estimativas": [("ARO: sensibilidade de taxa, custo e prazo; especialistas", "R"), ("IR diferido: projeções x orçamento/D&M; limite de 30%; expectativa de realização até 2041", "R"),
                            ("UOP/reservas: competência e objetividade da D&M", "P"), ("Impairment do ágio: taxa de 9,61%, Brent e reservas", "P"),
                            ("Opções de ações (Black-Scholes, NE 20.2)", "P"), ("Valor justo de swaps (nível 2)", "P")],
    }
    html = '<section class="sec" id="A"><h1>Anexo A - Programas de auditoria por ciclo</h1><p>Programas exigidos no item 6 das instruções, vinculados ao ' + ref("PT 300") + " e ao " + ref("PT 330") + ".</p>"
    for k, v in progs.items():
        html += f"<h3>{k}</h3>" + tab(["#", "Procedimento", "Classificação"], [[i + 1, p, badge(c)] for i, (p, c) in enumerate(v)], larg=["5%", "73%", "22%"])
    return html + "</section>"


def anexo_cobertura():
    return '<section class="sec" id="B"><h1>Anexo B - Matriz de cobertura das normas</h1><p>Versões consultadas na tabela do CFC (F15), acessada em 23/10/2026. Para 2025 aplicaram-se as versões vigentes no exercício auditado.</p>' + tab(
        ["Norma", "Versão", "Requisito principal", "PT", "Evidência/arquivo", "Status"],
        [[f'<a href="#{m["pt"].split(";")[0].replace(" ", "")}">{m["norma"]}</a>', m["versao"], m["requisito"], m["pt"], m["evidencias"], m["status"]] for m in MATRIZ],
        larg=["13%", "17%", "25%", "11%", "22%", "12%"], cls="small fixed") + "</section>"


def anexo_fontes():
    return '<section class="sec" id="C"><h1>Anexo C - Relação das fontes utilizadas</h1>' + tab(
        ["ID", "Documento", "Emissor", "Endereço eletrônico", "Acesso", "Exercício", "Página/uso"],
        [[f["id"], f["documento"], f["emissor"], f'<a href="{f["url"]}" style="word-break:break-all">{f["url"]}</a>', f["acesso"], f["exercicio"], f["paginas"]] for f in FONTES],
        larg=["4%", "22%", "9%", "37%", "8%", "8%", "12%"], cls="small fixed") + "</section>"


def conclusao():
    return f"""<section class="sec" id="CONC"><h1>Conclusão integrada</h1>
<div class="alert">Esta conclusão é acadêmica e <b>não</b> constitui opinião profissional independente sobre as demonstrações contábeis da PRIO S.A.</div>
<h3>Riscos identificados</h3>
<p>Seis riscos significativos: receita (corte/trading - fraude presumida), burla de controles, aquisição de +40% de Peregrino, avaliação do imobilizado/intangível (UOP, impairment), provisão para abandono e IR diferido. Os dois últimos coincidem com os PAA da KPMG e os quatro com os da EY em 2024. Também foram avaliados como altos: estoques (+158%, sem nota) e covenants (2,91x sem pró-forma).</p>
<h3>Procedimentos realizados e evidências disponíveis</h3>
<ul>
<li><b>Com evidência pública:</b> 19 reconciliações notas x demonstrações (15 conciliadas, 2 diferenças triviais, 2 acima do trivial: 1 explicada e 1 com hipótese de conversão); comparação de 100% dos saldos de abertura (1 reclassificação no PL); 5 analíticos com dados independentes (receita, juros e royalties dentro da precisão; D&A explicada por Peregrino; ARO em aberto); sensibilidade da ARO (±1 p.p. ≈ R$ 0,4 bi); recálculo do covenant; eventos subsequentes até 23/10/2026; componentes e consolidação.</li>
<li><b>Simulados (base de {br(RT['base_linhas'])} registros):</b> conciliação exata com a NE 8/15; 12 CAATs com 655/655 erros detectados; MUS rejeitando a base entregue (LSD de R$ 535 mi) e aceitando-a após as correções (LSD de R$ 78 mi); atributos (controle efetivo pela amostra, mas com deficiência significativa revelada pelo teste em 100%).</li>
<li><b>Planejados por falta de acesso:</b> confirmações, inventário físico, cartas jurídicas, papéis do antecessor, SOC reports, recálculo da UOP, projeções de IR diferido, indagações e atas.</li></ul>
<h3>Constatações a comunicar (com evidência pública)</h3>
<ol><li>Diferença de R$ 43.003 mil entre a abertura das provisões cíveis (NE 30) e o BP.</li><li>Ausência de nota de estoques (R$ 3,11 bi).</li>
<li>Reclassificação de R$ 29.885 mil no PL comparativo sem divulgação.</li><li>Remissões incorretas entre notas; divergência da data de constituição (FCA x NE 1).</li>
<li>Atendimento do covenant dependente do EBITDA pró-forma, não divulgado - recomenda-se transparência.</li><li>NE 17 sem análise de sensibilidade apesar da alta incerteza.</li></ol>
<p>Nenhuma delas altera o resultado ou o PL; são deficiências de apresentação e divulgação e de controle de revisão das demonstrações.</p>
<h3>Limitações do trabalho</h3>
<p>Uso exclusivo de documentos públicos, majoritariamente produzidos pela própria entidade; ausência de evidência externa direta (confirmações), física (inventário) e de sistemas; RA e apresentações não auditados; notas da DFP 2024 não pesquisáveis; base de imobilizado sintética, sem valor probatório; premissas didáticas (pró-forma de Peregrino, desconto de qualidade, prazo de Tubarão Azul). Com essas limitações, o trabalho <b>não</b> obtém evidência suficiente e apropriada para opinião. O que ele faz é demonstrar o raciocínio, os procedimentos e a documentação que uma auditoria conforme as NBC TA 200-600 exigiria. As constatações públicas são consistentes com a opinião sem ressalva emitida pela KPMG em 10/03/2026, porque são de natureza qualitativa e de divulgação.</p>
<div class="sign"><div><b>Preparado por:</b> Matrícula 231019943 | <b>Data:</b> 23/10/2026</div><div><b>Revisado por:</b> ______________________ | <b>Data:</b> ____/____/______</div></div></section>"""
