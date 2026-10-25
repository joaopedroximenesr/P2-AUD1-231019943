"""
Dados transcritos das Notas Explicativas da DFP 2025 da PRIO S.A. (valores em R$ mil).

Documento-fonte: DFP 31/12/2025, versão 1, protocolo CVM nº 155241, entregue em 10/03/2026.
Link: https://www.rad.cvm.gov.br/ENETCONSULTA/frmDownloadDocumento.aspx?Tela=ext&numSequencia=155241&numVersao=1&numProtocolo=&descTipo=DFP&CodigoInstituicao=1
Paginação citada = "PÁGINA: X de 108" impressa no rodapé do PDF da CVM.
Data de acesso: 23/10/2026.

As tabelas estruturadas (BP, DRE, DFC, DVA) NÃO estão aqui: vêm do Portal de Dados Abertos da CVM
(05_Codigo/00_extrair_dados_publicos.py). Aqui ficam apenas as quebras que só existem nas notas.
Cada bloco tem a página de origem para referência cruzada (PT 500).
"""

FONTE_DFP = {
    "documento": "DFP - Demonstrações Financeiras Padronizadas 31/12/2025 (v1)",
    "protocolo": "155241",
    "entrega": "10/03/2026",
    "url": "https://www.rad.cvm.gov.br/ENETCONSULTA/frmDownloadDocumento.aspx?Tela=ext&numSequencia=155241&numVersao=1&numProtocolo=&descTipo=DFP&CodigoInstituicao=1",
    "acesso": "23/10/2026",
}

# NE 8 - Imobilizado (Consolidado) - PÁGINA 67 de 108 (composição) e 68 (movimentação)
# (classe, grupo, método, taxa a.a., custo, depreciação acumulada, ajuste de conversão, saldo 31/12/2025, saldo 31/12/2024)
NE8_IMOBILIZADO = [
    ("Plataforma e Sonda - Polvo A", "Em operação", "UOP", None, 111_236, -100_530, 13_148, 23_854, 16_700),
    ("Plataforma Peregrino", "Em operação", "UOP", None, 6_889_483, -1_182_996, -257_530, 5_448_957, 4_179_633),
    ("FPSO Valente - Frade", "Em operação", "UOP", None, 2_016_456, -1_011_863, 10_498, 1_015_091, 1_124_728),
    ("FPSO Bravo - Tubarão Martelo", "Em operação", "UOP", None, 972_447, -494_984, 26_041, 503_504, 619_663),
    ("FPSO Forte - Albacora Leste", "Em operação", "UOP", None, 1_833_925, -642_726, 110_123, 1_301_322, 1_715_458),
    ("Sonda Hunter Queen", "Em operação", "UOP", None, 825_923, -93_117, 61_479, 794_285, 954_624),
    ("Ativos de Óleo e Gás - Frade", "Em operação", "UOP", None, 2_953_170, -1_103_380, 144_071, 1_993_861, 2_412_888),
    ("Ativos de Óleo e Gás - Polvo & TBMT", "Em operação", "UOP", None, 1_167_710, -653_768, -10_656, 503_286, 826_986),
    ("Ativos de Óleo e Gás - Peregrino", "Em operação", "UOP", None, 9_729_254, -1_269_060, -248_672, 8_211_522, 3_236_104),
    ("Ativos de Óleo e Gás - Albacora Leste", "Em operação", "UOP", None, 338_782, -5_032, -1_016, 332_734, 0),
    ("Revitalização de Poços (workover)", "Em operação", "Linear", 0.3333, 565_405, -490_670, 11_244, 85_979, 251_956),
    ("Embarcação Gênesis I", "Em operação", "Linear", 0.05, 230_908, -14_750, 22_097, 238_255, 245_808),
    ("Máquinas e equipamentos", "Em operação", "Linear", 0.10, 8_009, -8_009, 0, 0, 0),
    ("Móveis e utensílios", "Em operação", "Linear", 0.10, 2_361, -1_846, -8, 507, 751),
    ("Equipamentos de comunicação", "Em operação", "Linear", 0.10, 3_367, -1_021, 14, 2_360, 2_230),
    ("Equipamentos de informática", "Em operação", "Linear", 0.20, 36_551, -14_142, 1_731, 24_140, 12_371),
    ("Benfeitorias em imóveis de terceiros", "Em operação", "Linear", 0.04, 49_236, -3_327, 2_332, 48_241, 46_201),
    ("Imobilizado em andamento", "Em andamento", "Não deprecia", None, 96_796, 0, 1_028, 97_824, 34_519),
    ("Revitalização de Poços (workover) - andamento", "Em andamento", "Não deprecia", None, 356_401, 0, 54, 356_455, 138_779),
    ("Revitalização da Plataforma - Polvo A", "Em andamento", "Não deprecia", None, 73_108, 0, 1_103, 74_211, 0),
    ("Gastos com Desenvolvimento", "Em andamento", "Não deprecia", None, 6_481_048, 0, 84_988, 6_566_036, 4_440_618),
    ("Sobressalentes", "Em andamento", "Não deprecia", None, 378_355, 0, -13_136, 365_219, 15_345),
    ("Material poços", "Em andamento", "Não deprecia", None, 2_570_780, 0, -26_019, 2_544_761, 2_600_898),
]
NE8_TOTAL = {"custo": 37_690_711, "depreciacao": -7_091_221, "ajuste": -67_086, "saldo2025": 30_532_404, "saldo2024": 22_876_260, "pagina": 67}
# NE 8 b) Movimentação 2025 - PÁGINA 68
NE8_MOVIMENTACAO_2025 = {"saldo_inicial": 22_876_260, "adicoes": 14_189_924, "depreciacao": -3_273_407,
                         "transferencias": -874_566, "ajuste_conversao": -2_385_807, "saldo_final": 30_532_404,
                         "pagina": 68}
NE8_DESENVOLVIMENTO_ADICOES_2025 = {"Peregrino": 784_531, "Wahoo": 1_226_851, "Frade": 488_594,
                                    "Albacora Leste": 611_147, "Polvo & TBMT": 227_446}

# NE 15 - Direito de uso (CPC 06 R2) - PÁGINA 80
NE15_DIREITO_USO = [
    ("Embarcações de Apoio", 218_986, -85_124, 8_275, 142_137),
    ("Helicópteros", 701_123, -347_976, 16_992, 370_139),
    ("Edificações/Bases de Apoio", 88_384, -35_580, 2_843, 55_647),
    ("Equipamentos", 72_406, -35_872, 5_943, 42_477),
]
NE15_TOTAL = {"custo": 1_080_899, "depreciacao": -504_552, "ajuste": 34_053, "saldo": 610_400,
              "passivo": 644_854, "passivo_circ": 299_266, "passivo_nc": 345_588, "pagina": 80}

# NE 9 - Intangível - PÁGINA 69
NE9_INTANGIVEL = [
    ("Ativos de Óleo e Gás - Frade", 284_158, 361_510),
    ("Ativos de Óleo e Gás - Albacora Leste", 7_033_798, 9_374_246),
    ("Ativos de Óleo e Gás - Polvo & TBMT", 284_218, 378_275),
    ("Ativos de Óleo e Gás - Wahoo", 833_949, 938_510),
    ("Ativos de Óleo e Gás - Itaipu", 431, 485),
    ("Ativos de Óleo e Gás - Peregrino", 4_542_886, 3_722_532),
    ("Bônus de assinatura - FZA-M-254", 5_990, 6_075),
    ("Bônus de assinatura - FZA-Z-539", 8_051, 8_165),
    ("Softwares e outros", 274, 276),
    ("Ágio na aquisição do controle da Forte", 1_521_607, 1_712_388),
    ("Adiantamento para aquisição Peregrino", 523_278, 0),
]

# NE 9 d) Alocação da aquisição de +40% de Peregrino (11/11/2025) - PÁGINAS 71-72
NE9D_PEREGRINO_40 = {"adiantamento": 1_264_969, "complemento": 8_246_237, "imobilizado": 6_794_400,
                     "intangivel": 1_928_710, "almoxarifado": 877_125, "adiant_fornecedor": 20_442,
                     "cash_balance": -109_471, "aro_complemento": 1_322_571, "valor_base_usd_mi": 3_350}

# NE 3 - Caixa (PÁGINA 62) e instituições (PÁGINA 63)
NE3_BANCOS = [
    ("Time Deposit/Conta Remunerada", "USD", "Citi, BTG, Itaú, Santander, Safra", 2_146_568),
    ("Fundo Cambial", "USD", "BTG", 439_067),
    ("Conta Corrente", "USD", "Standard Bank, Millennium BCP", 579),
    ("Time Deposit/Conta Remunerada", "EUR", "Citi", 2_500),
    ("CDI/Compromissadas", "BRL", "Bradesco, Citi, Itaú, Santander", 808_575),
    ("Conta Corrente", "BRL", "BB, BTG, CEF, Rendimento", 908),
]
NE3_CAIXA_ESPECIE = 94

# NE 4 - Contas a receber por cliente - PÁGINA 63
NE4_CLIENTES = [("BP", 542_451, 0), ("Mercuria", 288_670, 0), ("Repsol", 229_569, 116_054),
                ("Cathay", 205_635, 0), ("Petrochina", 160_995, 0), ("CMM Cyprus", 75_729, 22_939),
                ("Navig8", 45_759, 55_731), ("Unipec", 80_369, 132_563), ("Equinor", 30_488, 0),
                ("Phillips 66", 6_884, 47_234), ("Exxon Mobil", 0, 5_827), ("Shell", 0, 111),
                ("Vitol", 0, 267_275), ("Sinochem London", 0, 249_407), ("Petrobras", 0, 13_948),
                ("Valero", 0, 5_771), ("Total", 0, 9_466), ("Trafigura", 0, 278), ("Outros", 23_551, 5_166)]

# NE 13 - Empréstimos (saldo 31/12/2025) - PÁGINA 73
NE13_EMPRESTIMOS = [("Citibank", 1_677_509), ("BTG", 2_221_792), ("Itaú", 1_795_199), ("Safra", 423_652),
                    ("Santander", 1_660_659), ("Bank of China", 276_831), ("HSBC", 1_401_109),
                    ("Bradesco", 552_899), ("JP Morgan", 562_993), ("Morgan Stanley", 278_038),
                    ("ABC", 165_445), ("Sumitomo Mitsui", 849_312), ("Bond 2026/2030", 4_837_598),
                    ("Gastos com captação - Bond", -95_174), ("XP S/A (NCE c/ swap)", 559_758)]
NE13_TOTAL = {"total": 17_167_620, "circulante": 1_253_614, "nao_circulante": 15_914_006, "pagina": 73}
NE14_DEBENTURES = {"total": 9_943_197, "mtm_swap": 671_595, "total_com_mtm": 10_614_792,
                   "circulante": 220_444, "nao_circulante": 10_394_348, "pagina": 79}
COVENANT_LIMITE = 2.5   # Dívida líquida / EBITDA ajustado LTM - NE 13 e 14 (PÁGINAS 77 e 79)

# NE 16 - Prejuízos fiscais e IR diferido - PÁGINAS 82-83
NE16_IR_DIFERIDO = {"ativo": 8_121_172, "passivo": 94_113, "prejuizos_reconhecidos": 8_090_896,
                    "credito_nao_reconhecido": 1_295_642, "pagina": 83}
NE16_REALIZACAO_PREJUIZOS = {2026: 1_195_466, 2027: 1_092_512, 2028: 1_241_280, 2029: 1_199_134,
                             2030: 1_178_218, 2031: 1_065_213, 2032: 839_684, "2033-2041": 279_389}

# NE 17 - Provisão para abandono (ARO) - PÁGINA 84
# (campo, saldo 31/12/2025, saldo 31/12/2024, ano previsto de abandono, taxa de desconto a.a.)
NE17_ARO = [
    ("Polvo", -11_099, -44_087, 2033, 0.0759),          # líquido do fundo de abandono
    ("Tubarão Martelo", 238_335, 201_213, 2033, 0.0759),
    ("Frade", 350_213, 227_860, 2041, 0.0812),
    ("Albacora Leste", 1_805_585, 1_515_053, 2031, 0.0741),
    ("Peregrino", 2_978_159, 1_385_554, 2034, 0.0741),
    ("Tubarão Azul", 86_245, 102_173, 2026, 0.0759),    # campo em descomissionamento (premissa didática de prazo)
]
NE17_TOTAL = {"saldo2025": 5_447_438, "saldo2024": 3_387_766, "atualizacao_monetaria": 371_394,
              "aumento_taxa": 722_504, "inflacao_usd": 0.02, "pagina": 84}

# NE 19 - Impairment - PÁGINA 85
NE19 = {"taxa_desconto_agio": 0.0961, "certificadora": "DeGolyer and MacNaughton (D&M)", "pagina": 85}

# NE 21 - Partes relacionadas (Controladora) - PÁGINAS 87-88
NE21_PARTES = [("Contas a receber Prio S.A x Comercializadora", 94, 0),
               ("Contas a receber Prio S.A x Forte", 1_484, 10_892),
               ("Contas a receber Prio S.A x Bravo", 1_768, 6_414),
               ("Rateio despesas administrativas Forte", 5_067, 0),
               ("Rateio despesas administrativas Bravo", 921, 0),
               ("Rateio despesas administrativas Tigris", 9_210, 0),
               ("Mútuo passivo Lux Holding x Prio S.A (7,03% a.a.)", -273_807, -273_676),
               ("Mútuo passivo Prio S.A x Coral (3% a.a.)", 0, -16_384),
               ("Mútuo passivo Prio S.A x Forte (6,125% a.a.)", -172_526, -375_051)]
NE21_RESULTADO = {"juros_mutuo": 48_345, "variacao_cambial": 48_112}
NE21_REMUNERACAO = {"curto_prazo": 5_556, "acoes": 29_376, "total": 34_932, "total_2024": 27_185}

# NE 22 - Receita líquida por campo (2025) - PÁGINA 89
NE22_RECEITA = [("Polvo/TBMT", 1_765_815, -14_052, 1_751_763), ("Frade", 4_218_789, -29_656, 4_189_133),
                ("Albacora Leste", 3_468_791, -56_989, 3_411_802), ("Peregrino", 4_500_706, -23_705, 4_477_001),
                ("Trading", 1_754_261, 0, 1_754_261)]
NE22_RECEITA_2024 = [("Polvo/TBMT", 1_671_158), ("Frade", 6_554_471), ("Albacora Leste", 3_774_570),
                     ("Peregrino", 248_155), ("Trading", 2_112_299)]

# NE 23 - CPV - PÁGINA 89
NE23_CPV = [("Depreciação e Amortização", -5_405_313, -2_205_033), ("Compra de óleo para revenda", -1_610_875, -2_088_361),
            ("Royalties e participação especial", -1_533_652, -1_232_820), ("Operação e Manutenção", -1_063_389, -335_887),
            ("Consumíveis", -625_186, -564_534), ("Pessoal", -553_542, -255_427),
            ("Depreciação de arrendamento", -298_515, -182_841), ("Outros Custos", -227_910, -111_458),
            ("Logística", -221_711, -109_515), ("Despesas de comercialização", -928_960, 0)]

# NE 25 - Outras receitas e despesas (consolidado) - PÁGINA 90
NE25_OUTRAS = [("Provisão contingências trabalhistas", -9_630), ("Provisão contingências fiscais", -4_978),
               ("Reversão contingências cíveis", 5_532), ("Impostos sobre JSCP", -125_997),
               ("Indirect Overhead - Parcerias", 1_033), ("Acordo desmobilização FPSO Polvo", -142_919),
               ("Perda parada de produção Peregrino", -194_765), ("Fee de aquisição de Peregrino", -35_786),
               ("Outras", 15_642)]

# NE 28 - Segmentos - PÁGINA 92
NE28_SEGMENTO = {"ac_brasil": 6_490_179, "ac_exterior": 3_083_086, "anc_brasil": 54_421_782, "anc_exterior": 184_558,
                 "ac_brasil_2024": 3_689_240, "ac_exterior_2024": 4_263_332, "anc_brasil_2024": 35_248_375,
                 "anc_exterior_2024": 12_545_218, "receita_exterior": 15_583_960}

# NE 29 - Liquidez (fluxos não descontados) - PÁGINA 95
NE29_LIQUIDEZ = [("Empréstimos e financiamentos", 17_167_620, 2_406_529, 21_312_820),
                 ("Fornecedores", 2_350_166, 2_350_166, 0), ("Debêntures locais", 9_943_197, 647_290, 16_983_327),
                 ("Arrendamentos", 644_854, 337_593, 360_634), ("Adiantamento de parceiros", 240_064, 240_064, 0)]
NE29_SENSIB_SOFR = {"provavel": -87_668, "cenario_25": -101_194, "cenario_50": -114_720}

# NE 30 - Contingências - PÁGINAS 96-98
NE30 = {"provisao": 758_162, "provisao_2024": 758_036, "depositos_judiciais": 189_277,
        "provavel_trab": 23_455, "provavel_fiscal": 92_537, "provavel_civel": 352_598,
        "conteudo_local_forte": 224_872, "irrf_forte_2013": 91_503,
        "passivo_contingente_pp_forte": 221_458, "passivo_contingente_pp_stellina": 25_111,
        "possivel_total": 4_029_942, "possivel_fiscal": 1_426_339, "possivel_civel": 2_598_906,
        "possivel_trab": 4_697}
NE30_POSSIVEIS = [("Confederação Nacional de Pescadores - zona de exclusão Frade", 1_314_970),
                  ("FEPERJ - derramamentos Frade 2011/2012 (operado pela Chevron)", 451_590),
                  ("RFB - IRRF sobre juros de PPE da Forte", 346_486),
                  ("PGFN - preço de transferência Jaguar 2010", 221_374),
                  ("RFB - ressarcimento antecipado PIS/COFINS", 179_948),
                  ("Fazenda Nacional - antecipação PIS/COFINS", 109_271),
                  ("Arbitragem Tuscany - sondas", 107_948),
                  ("Fazenda Nacional - IRRF Forte", 98_401)]

# NE 1 e 7 - Portfólio de concessões - PÁGINAS 43 e 65
CONCESSOES = [("Polvo", "BM-C-8", "Bravo", "100%", "Operador", "Produção"),
              ("Tubarão Martelo", "C-M-466", "Bravo e Forte", "100%", "Operador", "Produção"),
              ("Frade", "Frade", "Bravo e Forte", "100%", "Operador", "Produção"),
              ("Albacora Leste", "Albacora Leste", "Forte", "90%", "Operador", "Produção"),
              ("Peregrino", "BM-C-7", "Tigris", "80%", "Operador", "Produção"),
              ("Pitangola", "BM-C-47", "Tigris", "80%", "Não operador", "Produção"),
              ("Wahoo", "BM-C-30", "Forte", "64%", "Operador", "Desenvolvimento"),
              ("Itaipu", "BM-C-32", "Forte", "100%", "Operador", "Exploração"),
              ("FZA-M-254", "Foz do Amazonas", "Forte", "100%", "Operador", "Exploração (suspenso)"),
              ("Pirapema", "FZA-M-539", "Forte", "100%", "Operador", "Exploração (suspenso)")]

# NE 2.3 - Estrutura societária consolidada - PÁGINA 47
GRUPO = [("Prio S.A.", "Controladora (holding)", "-", "Brasil"),
         ("Prio Comercializadora Ltda. (PrioOG)", "Trading de gás / holding", "100% direta", "Brasil"),
         ("Prio Internacional Ltda. (PrioIntl)", "Holding", "0,57% direta / 99,43% indireta", "Brasil"),
         ("Prio Luxembourg Holding Sarl (Lux Holding)", "Trading de petróleo; dona da plataforma Polvo A", "100% indireta", "Luxemburgo"),
         ("Prio Forte S.A. (Forte)", "Produção: Frade, Albacora Leste, Wahoo, Itaipu", "100% indireta", "Brasil"),
         ("Prio Bravo Ltda. (Bravo)", "Produção: Polvo e Tubarão Martelo", "100% indireta", "Brasil"),
         ("Prio Tigris Ltda. (Tigris)", "Produção: Peregrino e Pitangola (80%)", "100% indireta", "Brasil"),
         ("Prio O&G International GmbH / Prio O&G Trading & Shipping GmbH", "Holding / Trading", "100% indireta", "Áustria"),
         ("Dommo Netherlands Holding BV / Dommo Netherlands BV", "Inativas", "100% indireta", "Holanda"),
         ("Prio North America LLC / Prio GOM LLC", "Inativas", "100% indireta", "EUA"),
         ("HRT Walvis / Kunene Energy / Orange Petroleum", "Em liquidação", "100% indireta", "Namíbia"),
         ("Prio Energia Ltda.", "Inativa", "100% indireta", "Brasil")]
EVENTOS_SOCIETARIOS_2025 = [("Petro Rio Jaguar incorporada pela Prio Forte", "jan/2025"),
                            ("Prio Contina B.V. incorporada pela Lux Holding", "abr/2025"),
                            ("Prio Coral incorporada pela Prio Forte", "30/04/2025"),
                            ("Prio Stellina Netherlands liquidada", "dez/2025")]

# NE 7 a) - investidas (controladora) - PÁGINA 66
NE7_INVESTIDAS = {"PrioOG_PL": 26_139_413, "PrioOG_resultado": 2_363_273, "PrioOG_ativos": 26_354_711,
                  "PrioIntl_PL": 26_050_418, "PrioIntl_resultado": 2_519_887, "investimento_total": 26_288_882}

# NE 20 - Patrimônio líquido - PÁGINAS 85-87
NE20 = {"capital_subscrito": 15_733_747, "acoes": 869_455_788, "tesouraria_acoes": 59_533_057,
        "tesouraria_custo": 1_905_611, "canceladas_17dez2025": 26_890_385,
        "acionistas": [("FMR LLC", 44_727_674), ("Schroder Investment Management Brasil", 43_741_218)],
        "dividendo_minimo": 0.00001, "reserva_investimentos": 2_138_884}

# Relatório da Administração (não auditado) - PÁGINAS 27-42
OPERACIONAL = {"producao_media_2025_bpd": 106_400, "producao_dez_2025_bpd": 155_800,
               "vendas_2025_mmbbl": 37.8, "crescimento_producao": 0.27, "lifting_cost_4t25_usd": 12.5,
               "brent_realizado_4t25": 63.22, "desconto_4t25": 7.73, "ebitda_aj_usd_bi": 1.4,
               "lucro_ex_ifrs16_usd_mi": 405, "da_usd_mi": 980, "custo_medio_divida": 0.0636}

# Fato Relevante 10/03/2026 e apresentação 4T25 (11/03/2026) - reservas D&M (MMbbl, 1P)
RESERVAS = {"1P_2025": 764.9, "producao_2025": 47.8, "1P_2026": 757.3, "1P_2026_pos_closing_20pct": 811.3,
            "1P_mais_1C": 919.3, "reposicao": 40.3}

# Relatório do auditor (PÁGINAS 99-102)
AUDITOR = {"firma": "KPMG Auditores Independentes Ltda.", "crc": "CRC SP-014428/O-6 F-RJ",
           "socio": "Bruno Bressan Marcondes (CRC RJ-112835/O-7)", "data": "10/03/2026", "opiniao": "Sem ressalva",
           "paa": ["Avaliação da estimativa de provisão para abandono de instalações (NE 17)",
                   "Recuperabilidade do IR e CS diferido ativo (NE 16)"],
           "anterior": "Ernst & Young Auditores Independentes S/S Ltda. - relatório de 12/03/2025, sem modificação",
           "anterior_paa": ["Combinação de negócios e aquisição de ativos (Stellina/Peregrino) - NE 1 e 9",
                            "Perda por redução ao valor recuperável dos ativos (impairment) - NE 2, 8, 9, 15 e 19",
                            "Provisão para abandono de instalações - NE 2 e 17",
                            "Recuperabilidade do IR e CS diferidos - NE 2 e 16"],
           "fca_responsavel_tecnico": "Leandro Pereira (FCA 2026, item auditor)"}
