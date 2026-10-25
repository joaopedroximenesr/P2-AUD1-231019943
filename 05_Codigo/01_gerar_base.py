"""
BASE DE DADOS SIMULADA OBRIGATÓRIA - IMOBILIZADO PRIO S.A. 31/12/2025
=====================================================================
*** DADOS SINTÉTICOS PARA FINS DIDÁTICOS - NÃO SÃO REGISTROS REAIS DA COMPANHIA ***

Conta escolhida: Imobilizado consolidado (BP 1.02.03) = R$ 31.142.804 mil, 48,5% do ativo total
(maior conta do ativo). Composição: NE 8 (R$ 30.532.404 mil, 23 classes) + NE 15 direito de uso
(R$ 610.400 mil, 4 classes).

Cada linha = um registro analítico do subledger de ativo imobilizado (componente patrimonial,
lote de material de poço, item sobressalente, gasto capitalizado de desenvolvimento, contrato
de arrendamento etc.). A base "limpa" reconcilia centavo a centavo, por classe, com custo,
depreciação, ajuste de conversão e saldo das notas. Em seguida são inseridos erros
controlados (registro em registro_erros_inseridos.csv) para testar os procedimentos.

Uso:  python 05_Codigo/01_gerar_base.py
Saídas (pasta 02_Base_Simulada/):
  base_imobilizado_sintetica.csv.gz      -> base "entregue pela entidade" (com erros inseridos)
  documentacao_suporte_simulada.csv.gz   -> valores corretos (simula documentos-suporte; usada
                                            somente para os itens selecionados nos testes)
  registro_erros_inseridos.csv           -> log dos erros inseridos (gabarito)
  dicionario_variaveis.csv               -> dicionário das variáveis
Semente aleatória: 231019943 (matrícula do preparador) -> reprodução idêntica.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notas_dfp2025 import NE8_IMOBILIZADO, NE15_DIREITO_USO  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "02_Base_Simulada"
SEMENTE = 231019943
DATA_BASE = pd.Timestamp("2025-12-31")
FLAG = "SINTETICO - fins didaticos"
rng = np.random.default_rng(SEMENTE)

# PTAX média anual (premissa didática para taxa histórica; 2024-2025 = média BCB SGS 1)
PTAX_ANO = {2014: 2.35, 2015: 3.33, 2016: 3.49, 2017: 3.19, 2018: 3.65, 2019: 3.95, 2020: 5.16,
            2021: 5.40, 2022: 5.16, 2023: 5.00, 2024: 5.392, 2025: 5.586, 2026: 5.40}

# ----------------------------------------------------------------------------------------------
# Parâmetros por classe: n linhas, dispersão (sigma lognormal), entidade(s), campo, período de
# aquisição, catálogo de descrições, local, origem, moeda.
# ----------------------------------------------------------------------------------------------
FPSO = ["Casco e estrutura naval", "Planta de processo - separador trifásico", "Turbogerador principal",
        "Compressor de gás", "Sistema de ancoragem - linha", "Turret/swivel", "Sistema de injeção de água",
        "Guindaste offshore", "Sistema de tratamento de óleo", "Sistema de flare", "Módulo de utilidades",
        "Módulo de acomodações", "Bomba de transferência de carga", "Instrumentação e automação",
        "Sistema de combate a incêndio (dilúvio)", "Tanque de carga", "Válvula de segurança (SDV)",
        "Trocador de calor", "Sistema de medição fiscal", "Painel elétrico de média tensão"]
OG = ["Poço produtor - perfuração", "Poço produtor - completação", "Poço injetor - perfuração",
      "Árvore de natal molhada (ANM)", "Linha flexível de produção", "Umbilical eletro-hidráulico",
      "Manifold submarino", "Riser flexível", "Bomba centrífuga submersa (BCS)", "Sistema de gas lift",
      "Custo de abandono capitalizado (ARO)", "Duto de exportação de gás", "Jumper submarino",
      "Equipamento de controle submarino (SCM)"]
SONDA = ["Torre de perfuração", "Top drive", "BOP - preventor de erupção", "Guincho de perfuração",
         "Bomba de lama", "Sistema de controle de poço", "Mesa rotativa", "Tubos de perfuração (lote)"]
MATERIAL = ['Tubo de revestimento 9 5/8" (lote)', 'Tubo de produção 4 1/2" (lote)', 'Broca PDC 12 1/4"',
            "Cimento classe G (lote)", "Fluido de perfuração base sintética (lote)", "Packer de produção",
            "Válvula DHSV", "Suspensor de coluna", "Cabeça de poço submarina", "Conector submarino",
            "Motor de BCS (estoque)", "Telas de contenção de areia", "Liner de produção (lote)",
            "Mandril de gas lift"]
SOBRES = ["Rotor de bomba", "Selo mecânico", "Kit de vedação", "Rolamento especial",
          "Módulo eletrônico de controle submarino", "Peças de turbogerador", "Filtro coalescedor",
          'Válvula esfera 6"', "Atuador hidráulico", "Inversor de frequência", "Sensor de pressão e temperatura"]
DESENV = ["Serviço de perfuração - diária de sonda", "Serviço de completação", "Instalação de linhas (PLSV)",
          "Engenharia de projeto (FEED/detalhamento)", "Interligação submarina (tieback)", "Fornecimento de ANM",
          "Serviços de ROV e mergulho", "Embarcação de apoio - logística offshore",
          "Juros capitalizados (CPC 20)", "Licenciamento ambiental e estudos", "Fluidos e cimentação",
          "Materiais aplicados em poço"]
WORK = ["Intervenção em poço - troca de BCS", "Workover com sonda", "Estimulação ácida",
        "Reabertura de poço hidratado", "Substituição de coluna de produção"]
INFO = ["Notebook", "Servidor", "Switch de rede", "Estação de trabalho", "Storage", "Firewall", "Monitor",
        "Rádio enlace"]
MOVEIS = ["Mesa de escritório", "Cadeira ergonômica", "Armário", "Estação de trabalho - mobiliário",
          "Mesa de reunião"]
COMUNIC = ["Rádio VHF marítimo", "Sistema VSAT", "Telefone satelital", "Antena", "Sistema de CFTV"]
MAQ = ["Gerador diesel auxiliar", "Compressor de ar", "Empilhadeira", "Máquina de solda"]
BENF = ["Reforma escritório sede - Praia de Botafogo", "Adequação base de apoio Macaé", "Instalações elétricas",
        "Climatização"]
EMB = ["Casco - Gênesis I", "Sistema de lançamento de linhas", "Guindaste - Gênesis I",
       "Revitalização de motores", "Sistema de posicionamento dinâmico (DP)"]
ANDAM = ["Instalações administrativas - obra", "Implantação de sistemas", "Infraestrutura de TI - projeto"]
REVPA = ["Revitalização estrutural da jaqueta", "Reforma do módulo de processo", "Recuperação de conveses"]

#            classe NE 8                                  n      sig  entidades (p)                             campo              ano_ini ano_fim catálogo local            origem padrão
CLASSES = {
    "Plataforma e Sonda - Polvo A":                (2_500, 1.5, {"Lux Holding": 1.0}, "Polvo & TBMT", 2014, 2025, FPSO, "Plataforma Polvo A", "Aquisição BP/Maersk"),
    "Plataforma Peregrino":                        (9_000, 1.7, {"Prio Tigris": 1.0}, "Peregrino", 2024, 2025, FPSO, "FPSO/Plataformas Peregrino", "Aquisição Peregrino"),
    "FPSO Valente - Frade":                        (6_000, 1.6, {"Prio Forte": 0.8, "Prio Bravo": 0.2}, "Frade", 2019, 2025, FPSO, "FPSO Valente", "Aquisição Frade"),
    "FPSO Bravo - Tubarão Martelo":                (4_000, 1.6, {"Prio Bravo": 1.0}, "Polvo & TBMT", 2020, 2025, FPSO, "FPSO Bravo", "Aquisição Dommo"),
    "FPSO Forte - Albacora Leste":                 (5_000, 1.6, {"Prio Forte": 1.0}, "Albacora Leste", 2023, 2025, FPSO, "FPSO Forte", "Aquisição Albacora Leste"),
    "Sonda Hunter Queen":                          (2_500, 1.4, {"Prio Forte": 1.0}, "Frade", 2023, 2025, SONDA, "Sonda Hunter Queen", "Aquisição própria"),
    "Ativos de Óleo e Gás - Frade":                (14_000, 1.5, {"Prio Forte": 0.75, "Prio Bravo": 0.25}, "Frade", 2019, 2025, OG, "Campo de Frade - submarino", "Aquisição própria"),
    "Ativos de Óleo e Gás - Polvo & TBMT":         (8_000, 1.5, {"Prio Bravo": 1.0}, "Polvo & TBMT", 2014, 2025, OG, "Cluster Polvo/TBMT - submarino", "Aquisição própria"),
    "Ativos de Óleo e Gás - Peregrino":            (22_000, 1.6, {"Prio Tigris": 1.0}, "Peregrino", 2024, 2025, OG, "Campo de Peregrino - submarino", "Aquisição Peregrino"),
    "Ativos de Óleo e Gás - Albacora Leste":       (1_500, 1.2, {"Prio Forte": 1.0}, "Albacora Leste", 2025, 2025, OG, "Campo de Albacora Leste", "Provisão de abandono (ARO)"),
    "Revitalização de Poços (workover)":           (6_000, 1.2, {"Prio Forte": 0.6, "Prio Bravo": 0.4}, "Albacora Leste", 2022, 2025, WORK, "Poços em produção", "Aquisição própria"),
    "Embarcação Gênesis I":                        (1_800, 1.4, {"Prio Forte": 1.0}, "Wahoo", 2024, 2025, EMB, "Embarcação Gênesis I", "Aquisição própria"),
    "Máquinas e equipamentos":                     (300, 0.8, {"PrioOG": 1.0}, "Corporativo", 2012, 2015, MAQ, "Base Macaé", "Aquisição própria"),
    "Móveis e utensílios":                         (1_200, 0.7, {"PrioOG": 1.0}, "Corporativo", 2015, 2025, MOVEIS, "Sede Rio de Janeiro", "Aquisição própria"),
    "Equipamentos de comunicação":                 (900, 0.8, {"PrioOG": 1.0}, "Corporativo", 2019, 2025, COMUNIC, "Sede Rio de Janeiro", "Aquisição própria"),
    "Equipamentos de informática":                 (4_500, 0.7, {"PrioOG": 1.0}, "Corporativo", 2020, 2025, INFO, "Sede Rio de Janeiro", "Aquisição própria"),
    "Benfeitorias em imóveis de terceiros":        (600, 1.0, {"PrioOG": 1.0}, "Corporativo", 2023, 2025, BENF, "Sede Rio de Janeiro", "Aquisição própria"),
    "Imobilizado em andamento":                    (3_000, 1.0, {"PrioOG": 1.0}, "Corporativo", 2024, 2025, ANDAM, "Sede Rio de Janeiro", "Aquisição própria"),
    "Revitalização de Poços (workover) - andamento": (8_000, 1.2, {"Prio Forte": 0.7, "Prio Bravo": 0.3}, "Albacora Leste", 2024, 2025, WORK, "Poços em intervenção", "Aquisição própria"),
    "Revitalização da Plataforma - Polvo A":       (2_000, 1.1, {"Lux Holding": 1.0}, "Polvo & TBMT", 2025, 2025, REVPA, "Plataforma Polvo A", "Aquisição própria"),
    "Gastos com Desenvolvimento":                  (190_000, 1.4, {"Prio Forte": 0.62, "Prio Tigris": 0.25, "Prio Bravo": 0.13}, "Wahoo", 2021, 2025, DESENV, "Projetos de desenvolvimento", "Aquisição própria"),
    "Sobressalentes":                              (60_000, 1.2, {"Prio Tigris": 0.7, "Prio Forte": 0.2, "Prio Bravo": 0.1}, "Peregrino", 2023, 2025, SOBRES, "Almoxarifado offshore", "Aquisição própria"),
    "Material poços":                              (165_000, 1.25, {"Prio Forte": 0.55, "Prio Tigris": 0.3, "Prio Bravo": 0.15}, "Frade", 2022, 2025, MATERIAL, "Almoxarifado Macaé", "Aquisição própria"),
}
CAMPO_POR_ENTIDADE = {  # usado nas classes com mais de uma entidade/campo
    "Gastos com Desenvolvimento": {"Prio Forte": ["Wahoo", "Frade", "Albacora Leste"], "Prio Tigris": ["Peregrino"], "Prio Bravo": ["Polvo & TBMT"]},
    "Sobressalentes": {"Prio Tigris": ["Peregrino"], "Prio Forte": ["Frade", "Albacora Leste"], "Prio Bravo": ["Polvo & TBMT"]},
    "Material poços": {"Prio Forte": ["Frade", "Wahoo", "Albacora Leste"], "Prio Tigris": ["Peregrino"], "Prio Bravo": ["Polvo & TBMT"]},
    "Revitalização de Poços (workover)": {"Prio Forte": ["Albacora Leste"], "Prio Bravo": ["Polvo & TBMT"]},
    "Revitalização de Poços (workover) - andamento": {"Prio Forte": ["Albacora Leste"], "Prio Bravo": ["Polvo & TBMT"]},
}
DIREITO_USO = {  # NE 15
    "Embarcações de Apoio": (120, "Contrato de afretamento - embarcação de apoio", "Prio Forte"),
    "Helicópteros": (150, "Contrato de transporte aéreo - helicóptero", "Prio Bravo"),
    "Edificações/Bases de Apoio": (60, "Locação de edificação/base de apoio", "PrioOG"),
    "Equipamentos": (70, "Locação de equipamento operacional", "Prio Tigris"),
}
CONTA = {"Em operação": "1.02.03.01", "Direito de uso": "1.02.03.02", "Em andamento": "1.02.03.03"}
USUARIOS = [f"USR{i:03d}" for i in range(1, 31)]
APROVADORES = [f"APR{i:02d}" for i in range(1, 9)]
DIRETORES = ["DIR01", "DIR02", "DIR03"]
ALCADA_GERENTE = 5_000_000.00  # R$ - acima disso exige aprovação de diretor (premissa de controle)


def alocar_centavos(total_reais_mil: int, pesos: np.ndarray) -> np.ndarray:
    """Distribui um total (R$ mil) em centavos inteiros proporcional aos pesos; soma exata."""
    total = int(round(total_reais_mil * 1000 * 100))
    if total == 0:
        return np.zeros(len(pesos), dtype=np.int64)
    sinal = 1 if total > 0 else -1
    total = abs(total)
    p = pesos / pesos.sum()
    bruto = p * total
    base = np.floor(bruto).astype(np.int64)
    resto = total - base.sum()
    if resto > 0:
        idx = np.argsort(-(bruto - base))[:resto]
        base[idx] += 1
    return sinal * base


def datas_uniformes(n: int, ano_ini: int, ano_fim: int) -> pd.DatetimeIndex:
    ini = pd.Timestamp(f"{ano_ini}-01-01").value // 86_400_000_000_000
    fim = pd.Timestamp(f"{ano_fim}-12-20").value // 86_400_000_000_000
    dias = rng.integers(ini, fim + 1, n)
    return pd.to_datetime(dias, unit="D")


def dia_util(d: pd.Series) -> pd.Series:
    """Empurra lançamentos de sábado/domingo para segunda (mantém ~0,3% em fim de semana)."""
    d = pd.to_datetime(d)
    wd = d.dt.weekday
    ajuste = np.where(wd == 5, 2, np.where(wd == 6, 1, 0))
    manter = rng.random(len(d)) < 0.003
    ajuste = np.where(manter, 0, ajuste)
    return d + pd.to_timedelta(ajuste, unit="D")


def depreciacao_uop(custo: np.ndarray, idade_meses: np.ndarray, alvo_centavos: int) -> np.ndarray:
    """Distribui depreciação acumulada (UOP) proporcional ao custo x maturidade, limitada a 97% do custo."""
    if alvo_centavos == 0:
        return np.zeros_like(custo)
    g = np.clip(idade_meses / 120.0, 0.02, None) * rng.uniform(0.7, 1.3, len(custo))
    lo, hi = 0.0, 50.0
    for _ in range(80):
        a = (lo + hi) / 2
        s = (custo * np.minimum(a * g, 0.97)).sum()
        lo, hi = (a, hi) if s < alvo_centavos else (lo, a)
    d = np.floor(custo * np.minimum(lo * g, 0.97)).astype(np.int64)
    resto = alvo_centavos - d.sum()
    folga = (custo * 0.97).astype(np.int64) - d
    ordem = np.argsort(-folga)
    i = 0
    while resto != 0:  # ajuste de centavos residual nos itens com maior folga
        j = ordem[i % len(ordem)]
        passo = int(np.sign(resto) * min(abs(resto), max(folga[j], 1)))
        d[j] += passo
        resto -= passo
        i += 1
    return d


def depreciacao_linear(custo: np.ndarray, taxa: float, alvo_centavos: int):
    """Gera frações depreciadas f_i com soma exata e devolve (depreciação, anos em uso) coerentes,
    de modo que o recálculo custo x taxa x anos reproduza o saldo (teste PT 330/PT 530)."""
    if alvo_centavos >= custo.sum():  # totalmente depreciado
        anos = 1 / taxa + rng.uniform(0.2, 3.0, len(custo))
        return custo.copy(), anos
    base = rng.beta(2.0, 2.5, len(custo))
    lo, hi = 0.0, 20.0
    for _ in range(80):
        a = (lo + hi) / 2
        s = (custo * np.minimum(a * base, 1.0)).sum()
        lo, hi = (a, hi) if s < alvo_centavos else (lo, a)
    f = np.minimum(lo * base, 1.0)
    d = np.floor(custo * f).astype(np.int64)
    resto = alvo_centavos - d.sum()
    idx = np.argsort(-(custo - d))[: abs(resto)]
    d[idx] += np.sign(resto)
    f = d / custo
    anos = np.where(f >= 0.999999, 1 / taxa + rng.uniform(0.2, 2.0, len(custo)), f / taxa)
    return d, anos


def gerar_classe(nome: str, grupo: str, metodo: str, taxa, custo_mil, depr_mil, ajuste_mil) -> pd.DataFrame:
    n, sig, ents, campo, a0, a1, catalogo, local, origem = CLASSES[nome]
    pesos = rng.lognormal(0.0, sig, n)
    custo = alocar_centavos(custo_mil, pesos)
    # entidade e campo
    nomes_ent = list(ents)
    entidade = rng.choice(nomes_ent, n, p=list(ents.values()))
    if nome in CAMPO_POR_ENTIDADE:
        mapa = CAMPO_POR_ENTIDADE[nome]
        campo_arr = np.array([rng.choice(mapa[e]) for e in entidade])
    else:
        campo_arr = np.full(n, campo)
    # datas
    data_aq = datas_uniformes(n, a0, a1)
    origem_arr = np.full(n, origem, dtype=object)
    if nome in ("Plataforma Peregrino", "Ativos de Óleo e Gás - Peregrino"):
        # 2024: combinação de negócios Stellina (40%) | 2025: aquisição Equinor +40% (11/11/2025)
        lote2025 = rng.random(n) < (0.39 if nome == "Plataforma Peregrino" else 0.58)
        data_aq = pd.DatetimeIndex(np.where(lote2025, pd.Timestamp("2025-11-11"), pd.Timestamp("2024-12-05")))
        origem_arr = np.where(lote2025, "Aquisição de ativos Equinor +40% (NE 9.d)", "Combinação de negócios Stellina (NE 9.c)")
    if nome == "Ativos de Óleo e Gás - Albacora Leste":
        data_aq = pd.DatetimeIndex(np.full(n, pd.Timestamp("2025-12-31")))
    if nome == "Gastos com Desenvolvimento":
        data_aq = datas_uniformes(n, 2023, 2025)
    data_cap = pd.Series(data_aq + pd.to_timedelta(rng.integers(0, 60, n), unit="D"))
    data_cap = data_cap.where(data_cap <= DATA_BASE, DATA_BASE)
    taxa_arr = np.full(n, np.nan)
    vida = np.full(n, np.nan)
    depr = np.zeros(n, dtype=np.int64)
    alvo_depr = int(round(-depr_mil * 1000 * 100))
    if grupo == "Em andamento":
        data_cap = pd.Series([pd.NaT] * n)
    elif metodo == "Linear":
        depr, anos = depreciacao_linear(custo, taxa, alvo_depr)
        data_cap = pd.Series(DATA_BASE - pd.to_timedelta(np.round(anos * 365.25), unit="D"))
        data_aq = pd.DatetimeIndex(data_cap - pd.to_timedelta(rng.integers(0, 30, n), unit="D"))
        taxa_arr[:] = taxa
        vida[:] = round(1 / taxa, 1)
    else:  # UOP
        idade = ((DATA_BASE - data_cap).dt.days / 30.44).to_numpy()
        depr = depreciacao_uop(custo, idade, alvo_depr)
    vc_pre = custo - depr
    pesos_aj = np.where(vc_pre > 0, vc_pre, 0).astype(float)
    ajuste = alocar_centavos(ajuste_mil, pesos_aj) if pesos_aj.sum() > 0 else np.zeros(n, dtype=np.int64)
    ano = pd.DatetimeIndex(data_aq).year
    tx_hist = np.array([PTAX_ANO.get(a, 5.0) for a in ano]) * rng.uniform(0.97, 1.03, n)
    moeda = "BRL" if nome in ("Equipamentos de informática", "Móveis e utensílios", "Benfeitorias em imóveis de terceiros",
                              "Equipamentos de comunicação", "Imobilizado em andamento") else "USD"
    df = pd.DataFrame({
        "classe_ne": nome, "grupo": grupo, "conta_contabil": CONTA[grupo], "entidade": entidade,
        "campo_ugc": campo_arr, "descricao": rng.choice(catalogo, n), "localizacao": local,
        "origem_registro": origem_arr, "metodo_depreciacao": metodo, "taxa_depreciacao_anual": taxa_arr,
        "vida_util_anos": vida, "data_aquisicao": pd.DatetimeIndex(data_aq).normalize(),
        "data_capitalizacao": pd.to_datetime(data_cap).dt.normalize(),
        "moeda_original": moeda, "taxa_cambio_historica": np.round(tx_hist, 4),
        "custo_historico_brl_c": custo, "depreciacao_acumulada_brl_c": -depr, "ajuste_conversao_brl_c": ajuste,
    })
    if nome in ("Material poços", "Sobressalentes"):
        df["quantidade"] = rng.integers(1, 400, n)
        df["unidade"] = np.where(df["descricao"].str.contains("lote"), "LT", "UN")
        df["data_ultima_movimentacao"] = (pd.to_datetime(df["data_aquisicao"])
                                          + pd.to_timedelta(rng.integers(0, 900, n), unit="D")).clip(upper=DATA_BASE)
    return df


def gerar_direito_uso() -> list[pd.DataFrame]:
    partes = []
    for (nome, custo_mil, depr_mil, aj_mil, _saldo) in NE15_DIREITO_USO:
        n, desc, ent = DIREITO_USO[nome]
        pesos = rng.lognormal(0, 0.9, n)
        custo = alocar_centavos(custo_mil, pesos)
        idade = rng.uniform(3, 60, n)
        depr = depreciacao_uop(custo, idade, int(round(-depr_mil * 1000 * 100)))
        vc = custo - depr
        aj = alocar_centavos(aj_mil, np.where(vc > 0, vc, 0).astype(float))
        inicio = pd.to_datetime(DATA_BASE - pd.to_timedelta(np.round(idade * 30.44), unit="D")).normalize()
        partes.append(pd.DataFrame({
            "classe_ne": f"Direito de uso - {nome}", "grupo": "Direito de uso", "conta_contabil": CONTA["Direito de uso"],
            "entidade": ent, "campo_ugc": rng.choice(["Frade", "Albacora Leste", "Polvo & TBMT", "Peregrino"], n),
            "descricao": desc, "localizacao": "Contrato de arrendamento", "origem_registro": "CPC 06 (R2)/IFRS 16",
            "metodo_depreciacao": "Linear (prazo do contrato)", "taxa_depreciacao_anual": np.nan, "vida_util_anos": np.nan,
            "data_aquisicao": inicio, "data_capitalizacao": inicio, "moeda_original": "USD",
            "taxa_cambio_historica": np.round([PTAX_ANO.get(a, 5.0) for a in inicio.year], 4),
            "custo_historico_brl_c": custo, "depreciacao_acumulada_brl_c": -depr, "ajuste_conversao_brl_c": aj,
        }))
    return partes


def finalizar_campos(df: pd.DataFrame) -> pd.DataFrame:
    n = len(df)
    df = df.reset_index(drop=True)
    df.insert(0, "id_registro", [f"IMB{i:07d}" for i in range(1, n + 1)])
    codigos = df.groupby("classe_ne").cumcount() + 1
    sigla = df["classe_ne"].str.replace(r"[^A-Za-zÀ-ú]", "", regex=True).str.upper().str[:4]
    df.insert(1, "id_bem", sigla + "-" + codigos.astype(str).str.zfill(6))
    df["valor_contabil_brl_c"] = df["custo_historico_brl_c"] + df["depreciacao_acumulada_brl_c"] + df["ajuste_conversao_brl_c"]
    df["custo_usd"] = np.round(df["custo_historico_brl_c"] / 100 / df["taxa_cambio_historica"], 2)
    df["fornecedor_id"] = np.where(df["grupo"] == "Direito de uso", "ARRENDADOR-" + pd.Series(rng.integers(1, 40, n)).astype(str),
                                   "FORN-" + pd.Series(rng.zipf(1.6, n) % 4000 + 1).astype(str).str.zfill(5))
    df["documento_origem"] = np.where(df["grupo"] == "Direito de uso", "CTR-", np.where(
        df["classe_ne"] == "Gastos com Desenvolvimento", "OS-", "NF-")) + pd.Series(rng.integers(10**7, 10**8, n)).astype(str)
    base_lanc = df["data_capitalizacao"].fillna(df["data_aquisicao"]) + pd.to_timedelta(rng.integers(0, 6, n), unit="D")
    df["data_lancamento"] = dia_util(base_lanc.clip(upper=DATA_BASE)).clip(upper=DATA_BASE).dt.normalize()
    df["usuario_lancamento"] = rng.choice(USUARIOS, n)
    custo_reais = df["custo_historico_brl_c"] / 100
    df["aprovador"] = np.where(custo_reais > ALCADA_GERENTE, rng.choice(DIRETORES, n), rng.choice(APROVADORES, n))
    df["flag_dado"] = FLAG
    return df


def inserir_erros(df: pd.DataFrame):
    """Insere erros controlados e devolve (base com erros, log)."""
    log = []
    novos = []
    ref = df.copy()

    def registrar(idx_or_id, tipo, desc, impacto_c, campo="", antes="", depois=""):
        log.append({"id_registro": idx_or_id, "tipo_erro": tipo, "descricao": desc, "campo_alterado": campo,
                    "valor_original": antes, "valor_inserido": depois, "impacto_valor_contabil_brl": impacto_c / 100})

    proximo = [len(df) + 1]

    def novo_id():
        i = proximo[0]
        proximo[0] += 1
        return f"IMB{i:07d}"

    ativos = df.index[(df["grupo"] != "Direito de uso")]
    # E01 - Duplicidade de registro (existência)
    for i in rng.choice(ativos, 120, replace=False):
        r = df.loc[i].copy()
        r["id_registro"] = novo_id()
        novos.append(r)
        registrar(r["id_registro"], "E01-Duplicidade", f"Duplicata de {df.at[i, 'id_registro']} (mesmo bem, documento e valor)",
                  r["valor_contabil_brl_c"])
    # E02 - Corte: aquisições de jan-fev/2026 registradas em 2025 (existência/corte)
    for i in rng.choice(df.index[df["grupo"] == "Em andamento"], 60, replace=False):
        r = df.loc[i].copy()
        r["id_registro"] = novo_id()
        d = pd.Timestamp("2026-01-05") + pd.Timedelta(days=int(rng.integers(0, 50)))
        r["data_aquisicao"] = d
        r["data_lancamento"] = pd.Timestamp("2025-12-31")
        r["documento_origem"] = "NF-" + str(rng.integers(10**7, 10**8))
        novos.append(r)
        registrar(r["id_registro"], "E02-Corte", f"NF emitida em {d.date()} lançada na competência 2025", r["valor_contabil_brl_c"],
                  "data_aquisicao", "", str(d.date()))
    # E03 - Depreciação acumulada maior que o custo (valor contábil negativo)
    cand = df.index[(df["grupo"] == "Em operação") & (df["custo_historico_brl_c"] > 0) & (df["metodo_depreciacao"] == "UOP")]
    for i in rng.choice(cand, 40, replace=False):
        antes = df.at[i, "depreciacao_acumulada_brl_c"]
        depois = -int(df.at[i, "custo_historico_brl_c"] * 1.15)
        df.at[i, "depreciacao_acumulada_brl_c"] = depois
        registrar(df.at[i, "id_registro"], "E03-VC negativo", "Depreciação acumulada superior ao custo", depois - antes,
                  "depreciacao_acumulada_brl", antes / 100, depois / 100)
    # E04 - Depreciação registrada em ativo em andamento (ainda não disponível para uso - CPC 27 item 55)
    for i in rng.choice(df.index[df["grupo"] == "Em andamento"], 50, replace=False):
        depois = -int(df.at[i, "custo_historico_brl_c"] * rng.uniform(0.05, 0.30))
        df.at[i, "depreciacao_acumulada_brl_c"] = depois
        registrar(df.at[i, "id_registro"], "E04-Depreciação em andamento", "Depreciação em ativo não disponível para uso", depois,
                  "depreciacao_acumulada_brl", 0, depois / 100)
    # E05 - Taxa de depreciação aplicada pela metade (classes lineares, valor relevante)
    cand = df.index[(df["metodo_depreciacao"] == "Linear") & (df["depreciacao_acumulada_brl_c"] < -1_000_000)
                    & (df["depreciacao_acumulada_brl_c"] > -df["custo_historico_brl_c"])]
    for i in rng.choice(cand, 80, replace=False):
        antes = df.at[i, "depreciacao_acumulada_brl_c"]
        depois = int(antes / 2)
        df.at[i, "depreciacao_acumulada_brl_c"] = depois
        registrar(df.at[i, "id_registro"], "E05-Taxa incorreta", "Depreciação calculada com metade da taxa", depois - antes,
                  "depreciacao_acumulada_brl", antes / 100, depois / 100)
    # E06 - Erro de digitação: custo x10 (avaliação)
    cand = df.index[(df["grupo"] == "Em andamento") & (df["custo_historico_brl_c"].between(5_000_000, 50_000_000))]
    for i in rng.choice(cand, 30, replace=False):
        antes = df.at[i, "custo_historico_brl_c"]
        df.at[i, "custo_historico_brl_c"] = antes * 10
        registrar(df.at[i, "id_registro"], "E06-Digitação x10", "Custo lançado com um zero a mais", antes * 9,
                  "custo_historico_brl", antes / 100, antes * 10 / 100)
    # E07 - Segregação de funções: lançador = aprovador (controle, sem efeito monetário)
    for i in rng.choice(df.index, 150, replace=False):
        antes = df.at[i, "aprovador"]
        df.at[i, "aprovador"] = df.at[i, "usuario_lancamento"]
        registrar(df.at[i, "id_registro"], "E07-Segregação de funções", "Lançamento aprovado pelo próprio usuário", 0,
                  "aprovador", antes, df.at[i, "aprovador"])
    # E08 - Aprovação acima da alçada (controle)
    cand = df.index[df["custo_historico_brl_c"] > ALCADA_GERENTE * 100]
    for i in rng.choice(cand, 60, replace=False):
        antes = df.at[i, "aprovador"]
        df.at[i, "aprovador"] = rng.choice(APROVADORES)
        registrar(df.at[i, "id_registro"], "E08-Alçada", "Valor acima de R$ 5 mi aprovado por gerente", 0, "aprovador", antes,
                  df.at[i, "aprovador"])
    # E09 - Capitalização indevida de OPEX via lançamento manual suspeito (fraude simulada)
    for k in range(25):
        r = df.loc[rng.choice(df.index[df["classe_ne"] == "Gastos com Desenvolvimento"])].copy()
        r["id_registro"] = novo_id()
        valor = int(rng.choice([5, 8, 10, 12, 15, 20])) * 1_000_000 * 100
        sab = pd.Timestamp("2025-12-27") if k % 2 == 0 else pd.Timestamp("2025-12-28")
        r[["custo_historico_brl_c", "depreciacao_acumulada_brl_c", "ajuste_conversao_brl_c"]] = [valor, 0, 0]
        r["descricao"] = "Ajuste manual - reclassificação de custo operacional"
        r["data_lancamento"] = sab
        r["usuario_lancamento"] = "USR_TEMP"
        r["aprovador"] = "USR_TEMP"
        r["documento_origem"] = "AJ-" + str(rng.integers(1000, 9999))
        r["fornecedor_id"] = "SEM-FORNECEDOR"
        r["valor_contabil_brl_c"] = valor
        novos.append(r)
        registrar(r["id_registro"], "E09-Lançamento manual suspeito", "OPEX capitalizado: valor redondo, fim de semana, usuário genérico",
                  valor)
    # E10 - Ativo de Peregrino registrado em entidade incorreta (classificação entre componentes)
    cand = df.index[df["campo_ugc"] == "Peregrino"]
    for i in rng.choice(cand, 40, replace=False):
        antes = df.at[i, "entidade"]
        df.at[i, "entidade"] = "Prio Bravo"
        registrar(df.at[i, "id_registro"], "E10-Entidade/UGC incoerente", "Ativo de Peregrino lançado na Prio Bravo", 0,
                  "entidade", antes, "Prio Bravo")
    if novos:
        df = pd.concat([df, pd.DataFrame(novos)], ignore_index=True)
    df["valor_contabil_brl_c"] = df["custo_historico_brl_c"] + df["depreciacao_acumulada_brl_c"] + df["ajuste_conversao_brl_c"]
    return df, pd.DataFrame(log), ref


def para_reais(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in [c for c in out.columns if c.endswith("_brl_c")]:
        out[c[:-2]] = (out[c] / 100).round(2)
        out = out.drop(columns=c)
    ordem = ["id_registro", "id_bem", "classe_ne", "grupo", "conta_contabil", "entidade", "campo_ugc", "descricao",
             "localizacao", "origem_registro", "metodo_depreciacao", "taxa_depreciacao_anual", "vida_util_anos",
             "data_aquisicao", "data_capitalizacao", "data_lancamento", "moeda_original", "taxa_cambio_historica",
             "custo_usd", "custo_historico_brl", "depreciacao_acumulada_brl", "ajuste_conversao_brl",
             "valor_contabil_brl", "quantidade", "unidade", "data_ultima_movimentacao", "fornecedor_id",
             "documento_origem", "usuario_lancamento", "aprovador", "flag_dado"]
    return out[ordem]


DICIONARIO = [
    ("id_registro", "texto", "Identificador único do registro no subledger (chave primária)", "IMB0000001"),
    ("id_bem", "texto", "Número patrimonial do bem/componente (sigla da classe + sequência)", "PLAT-000123"),
    ("classe_ne", "texto", "Classe do imobilizado conforme NE 8 (ou NE 15 para direito de uso)", "Material poços"),
    ("grupo", "texto", "Em operação | Em andamento | Direito de uso", "Em andamento"),
    ("conta_contabil", "texto", "Conta do plano CVM: 1.02.03.01 operação, .02 direito de uso, .03 andamento", "1.02.03.03"),
    ("entidade", "texto", "Entidade do grupo detentora do registro (componente - PT 600)", "Prio Forte"),
    ("campo_ugc", "texto", "Campo/cluster = unidade geradora de caixa (NE 2.13)", "Peregrino"),
    ("descricao", "texto", "Descrição sintética do bem ou do gasto capitalizado", "Árvore de natal molhada (ANM)"),
    ("localizacao", "texto", "Local físico de referência (para inspeção planejada)", "FPSO Valente"),
    ("origem_registro", "texto", "Forma de ingresso: aquisição própria, combinação de negócios, ARO etc.", "Combinação de negócios Stellina (NE 9.c)"),
    ("metodo_depreciacao", "texto", "UOP (unidades produzidas) | Linear | Não deprecia | Linear (prazo do contrato)", "UOP"),
    ("taxa_depreciacao_anual", "decimal", "Taxa linear anual (somente classes lineares, NE 8)", "0.20"),
    ("vida_util_anos", "decimal", "Vida útil implícita = 1/taxa (classes lineares)", "5.0"),
    ("data_aquisicao", "data", "Data do documento de aquisição", "2025-03-14"),
    ("data_capitalizacao", "data", "Data de entrada em operação (vazia para itens em andamento)", "2025-04-02"),
    ("data_lancamento", "data", "Data do lançamento contábil no sistema", "2025-04-03"),
    ("moeda_original", "texto", "Moeda do documento de origem (moeda funcional do grupo = USD, NE 2.4)", "USD"),
    ("taxa_cambio_historica", "decimal", "Taxa R$/US$ histórica do registro (premissa didática)", "5.3920"),
    ("custo_usd", "decimal", "Custo histórico em US$ = custo R$ / taxa histórica", "1250000.00"),
    ("custo_historico_brl", "decimal (R$)", "Custo histórico em reais", "6740000.00"),
    ("depreciacao_acumulada_brl", "decimal (R$)", "Depreciação acumulada (valor negativo)", "-1234567.89"),
    ("ajuste_conversao_brl", "decimal (R$)", "Parcela do ajuste acumulado de conversão alocada ao registro", "15000.10"),
    ("valor_contabil_brl", "decimal (R$)", "Custo + depreciação + ajuste de conversão (saldo em 31/12/2025)", "5520432.21"),
    ("quantidade", "inteiro", "Quantidade física (materiais de poço e sobressalentes)", "120"),
    ("unidade", "texto", "UN = unidade | LT = lote", "LT"),
    ("data_ultima_movimentacao", "data", "Última movimentação física (materiais) - teste de obsolescência", "2023-08-30"),
    ("fornecedor_id", "texto", "Código do fornecedor/arrendador", "FORN-00012"),
    ("documento_origem", "texto", "NF-, OS- (ordem de serviço), CTR- (contrato), AJ- (ajuste manual)", "NF-48213377"),
    ("usuario_lancamento", "texto", "Usuário que registrou o lançamento", "USR014"),
    ("aprovador", "texto", "Usuário que aprovou (APRxx gerentes até R$ 5 mi; DIRxx diretores)", "DIR02"),
    ("flag_dado", "texto", "Marca obrigatória: dado sintético para fins didáticos", FLAG),
]


def main() -> None:
    SAIDA.mkdir(exist_ok=True)
    partes = []
    for (nome, grupo, metodo, taxa, custo, depr, aj, _s25, _s24) in NE8_IMOBILIZADO:
        partes.append(gerar_classe(nome, grupo, metodo, taxa, custo, depr, aj))
        print(f"  {nome:<48} {len(partes[-1]):>8,} linhas")
    partes += gerar_direito_uso()
    base = finalizar_campos(pd.concat(partes, ignore_index=True))

    # Verificação: base limpa = notas explicativas, centavo a centavo
    tot = base.groupby("classe_ne")[["custo_historico_brl_c", "depreciacao_acumulada_brl_c", "ajuste_conversao_brl_c",
                                     "valor_contabil_brl_c"]].sum()
    for (nome, _g, _m, _t, c, d, a, s, _) in NE8_IMOBILIZADO:
        assert tot.loc[nome].tolist() == [c * 100_000, d * 100_000, a * 100_000, s * 100_000], nome
    assert base["valor_contabil_brl_c"].sum() == 31_142_804 * 100_000
    print(f"Base limpa: {len(base):,} linhas | total R$ {base['valor_contabil_brl_c'].sum()/100:,.2f} (= BP 1.02.03)")

    suja, log, limpa = inserir_erros(base)
    print(f"Erros inseridos: {len(log)} registros | base final: {len(suja):,} linhas")

    para_reais(suja).to_csv(SAIDA / "base_imobilizado_sintetica.csv.gz", index=False, compression="gzip",
                            date_format="%Y-%m-%d", encoding="utf-8")
    sup = para_reais(limpa)[["id_registro", "custo_historico_brl", "depreciacao_acumulada_brl", "ajuste_conversao_brl",
                              "valor_contabil_brl", "entidade", "aprovador", "flag_dado"]]
    sup.to_csv(SAIDA / "documentacao_suporte_simulada.csv.gz", index=False, compression="gzip", encoding="utf-8")
    log.to_csv(SAIDA / "registro_erros_inseridos.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(DICIONARIO, columns=["variavel", "tipo", "descricao", "exemplo"]).to_csv(
        SAIDA / "dicionario_variaveis.csv", index=False, encoding="utf-8-sig")
    print("Arquivos gravados em", SAIDA)


if __name__ == "__main__":
    main()
