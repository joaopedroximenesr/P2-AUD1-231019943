"""
Procedimentos sobre DADOS REAIS PÚBLICOS (DFP 2025, DFP 2024, ITR 2026, BCB, EIA).

  PT 500  - Reconciliação notas explicativas x balanço (CVM dados abertos)
  PT 510  - Saldos iniciais: DFP 2024 original x comparativos apresentados na DFP 2025
  PT 520  - Procedimentos analíticos substantivos (expectativas, precisão, limites, diferenças)
  PT 540  - Sensibilidade da provisão para abandono (ARO)
  PT 570  - Indicadores de liquidez, endividamento e covenants
  PT 600  - Significância dos componentes (campos/UGC e entidades)
  PT 315/320 - análise horizontal e vertical

Uso: python 05_Codigo/03_analiticos.py         Saídas: 06_Resultados/*.csv e 06_Resultados/resumo_analiticos.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notas_dfp2025 as ne  # noqa: E402
from parametros import (DADOS, LIMITE_TRIVIAL, MATERIALIDADE_EXECUCAO, MATERIALIDADE_GLOBAL, RESULTADOS, bases_materialidade,  # noqa: E402
                        conta, demonstracao)

R = RESULTADOS


def mercado() -> dict:
    p = pd.read_csv(DADOS / "mercado_ptax_diaria.csv", parse_dates=["data"])
    b = pd.read_csv(DADOS / "mercado_brent_diario.csv", parse_dates=["data"])
    out = {}
    for ano in (2024, 2025):
        out[f"ptax_media_{ano}"] = round(p.loc[p["data"].dt.year == ano, "valor"].mean(), 4)
        out[f"ptax_fim_{ano}"] = round(p.loc[p["data"].dt.year == ano].sort_values("data")["valor"].iloc[-1], 4)
        out[f"brent_medio_{ano}"] = round(b.loc[b["data"].dt.year == ano, "brent_usd"].mean(), 2)
    return out


def reconciliacoes() -> pd.DataFrame:
    linhas = [
        ("Caixa e equivalentes", "BP 1.01.01", conta("BPA", "1.01.01"), "NE 3 (p. 62)", ne.NE3_CAIXA_ESPECIE + sum(x[3] for x in ne.NE3_BANCOS)),
        ("Contas a receber", "BP 1.01.03", conta("BPA", "1.01.03"), "NE 4 (p. 63)", sum(x[1] for x in ne.NE4_CLIENTES)),
        ("Imobilizado (NE 8 + direito de uso NE 15)", "BP 1.02.03", conta("BPA", "1.02.03"), "NE 8 e 15 (p. 67 e 80)",
         ne.NE8_TOTAL["saldo2025"] + ne.NE15_TOTAL["saldo"]),
        ("Direito de uso", "BP 1.02.03.02", conta("BPA", "1.02.03.02"), "NE 15 (p. 80)", ne.NE15_TOTAL["saldo"]),
        ("Imobilizado em andamento", "BP 1.02.03.03", conta("BPA", "1.02.03.03"), "NE 8 (p. 67)",
         sum(x[7] for x in ne.NE8_IMOBILIZADO if x[1] == "Em andamento")),
        ("Intangível", "BP 1.02.04", conta("BPA", "1.02.04"), "NE 9 (p. 69)", sum(x[1] for x in ne.NE9_INTANGIVEL)),
        ("IR/CS diferido ativo", "BP 1.02.01.07", conta("BPA", "1.02.01.07"), "NE 16 (p. 83)", ne.NE16_IR_DIFERIDO["ativo"]),
        ("Empréstimos (circ. + não circ., sem debêntures e arrend.)", "BP 2.01.04.01 + 2.02.01.01",
         conta("BPP", "2.01.04.01") + conta("BPP", "2.02.01.01"), "NE 13 (p. 73)", ne.NE13_TOTAL["total"]),
        ("Debêntures (inclui MTM swap)", "BP 2.01.04.02 + 2.02.01.02", conta("BPP", "2.01.04.02") + conta("BPP", "2.02.01.02"),
         "NE 14 (p. 79)", ne.NE14_DEBENTURES["total_com_mtm"]),
        ("Passivo de arrendamento", "BP 2.01.04.03 + 2.02.01.03", conta("BPP", "2.01.04.03") + conta("BPP", "2.02.01.03"),
         "NE 15 (p. 80)", ne.NE15_TOTAL["passivo"]),
        ("Provisão para abandono", "BP 2.02.04.02.03", conta("BPP", "2.02.04.02.03"), "NE 17 (p. 84)", ne.NE17_TOTAL["saldo2025"]),
        ("Provisões para contingências", "BP 2.02.04.01", conta("BPP", "2.02.04.01"), "NE 30 (p. 96)", ne.NE30["provisao"]),
        ("Receita líquida", "DRE 3.01", conta("DRE", "3.01"), "NE 22 (p. 89)", sum(x[3] for x in ne.NE22_RECEITA)),
        ("Custo dos produtos vendidos", "DRE 3.02", conta("DRE", "3.02"), "NE 23 (p. 89)", sum(x[1] for x in ne.NE23_CPV)),
        ("Outras receitas/despesas", "DRE 3.04.04 + 3.04.05", conta("DRE", "3.04.04") + conta("DRE", "3.04.05"), "NE 25 (p. 90)",
         sum(x[1] for x in ne.NE25_OUTRAS)),
        ("Depreciação/amortização (DFC x DVA)", "DFC 6.01.01.02", conta("DFC_MI", "6.01.01.02"), "DVA 7.04.01",
         -conta("DVA", "7.04.01")),
        ("Depreciação/amortização (DFC x movimentação NE 8+9+15)", "DFC 6.01.01.02", conta("DFC_MI", "6.01.01.02"),
         "NE 8, 9, 15 (p. 68, 69, 80)", 3_273_407 + 2_137_933 + 293_368),
        ("Depreciação de arrendamento (CPV x NE 15)", "NE 23 (p. 89)", 298_515, "NE 15 (p. 80)", 293_368),
        ("Ativo por região (NE 28) x Ativo total", "BP 1", conta("BPA", "1"), "NE 28 (p. 92)",
         ne.NE28_SEGMENTO["ac_brasil"] + ne.NE28_SEGMENTO["ac_exterior"] + ne.NE28_SEGMENTO["anc_brasil"] + ne.NE28_SEGMENTO["anc_exterior"]),
    ]
    df = pd.DataFrame(linhas, columns=["item", "ref_demonstracao", "valor_demonstracao", "ref_nota", "valor_nota"])
    df["diferenca"] = df["valor_demonstracao"] - df["valor_nota"]
    df["situacao"] = np.select([df["diferenca"].abs() < 1, df["diferenca"].abs() <= LIMITE_TRIVIAL],
                               ["Conciliado", "Diferença trivial - registrar"], "Diferença acima do trivial - investigar")
    explic = {"Debêntures (inclui MTM swap)": "Explicada: MTM do swap do empréstimo XP (R$ 11.027 mil, NE 13 p. 76) apresentado "
                                              "na linha de debêntures do BP; resíduo de R$ 7 mil = arredondamento",
              "Depreciação/amortização (DFC x movimentação NE 8+9+15)": "Hipótese: movimentações das notas a taxas históricas e DFC a "
                                                                       "taxa média (NE 2.4); não comprovável com dados públicos",
              "Depreciação/amortização (DFC x DVA)": "Diferença de R$ 1.035 mil entre DFC e DVA - trivial; registrar no PT 450",
              "Depreciação de arrendamento (CPV x NE 15)": "Diferença de R$ 5.147 mil - trivial; possível efeito de PIS/COFINS sobre arrendamentos (NE 15)"}
    df["explicacao"] = df["item"].map(explic).fillna("")
    return df


def saldos_iniciais() -> pd.DataFrame:
    out = []
    for dem in ["BPA", "BPP"]:
        orig = pd.read_csv(DADOS / f"dfp2024_{dem}_con.csv", dtype={"CD_CONTA": str})
        orig = orig[orig["ORDEM_EXERC"] == "ÚLTIMO"].set_index("CD_CONTA")
        comp = pd.read_csv(DADOS / f"dfp2025_{dem}_con.csv", dtype={"CD_CONTA": str})
        comp = comp[comp["ORDEM_EXERC"] == "PENÚLTIMO"].set_index("CD_CONTA")
        idx = sorted(set(orig.index) | set(comp.index), key=lambda c: [int(x) for x in c.split(".")])
        for c in idx:
            v1 = float(orig["VL_CONTA"].get(c, 0) or 0)
            v2 = float(comp["VL_CONTA"].get(c, 0) or 0)
            ds = comp["DS_CONTA"].get(c, orig["DS_CONTA"].get(c, ""))
            if v1 == 0 and v2 == 0:
                continue
            out.append({"demonstracao": dem, "cd_conta": c, "ds_conta": ds, "dfp2024_original": v1,
                        "comparativo_dfp2025": v2, "diferenca": v2 - v1})
    df = pd.DataFrame(out)
    df["situacao"] = np.where(df["diferenca"].abs() < 1, "Igual", "Reclassificação/reapresentação - examinar")
    return df


def horizontal_vertical() -> pd.DataFrame:
    partes = []
    for dem, base_cod in [("BPA", "1"), ("BPP", "2"), ("DRE", "3.01")]:
        d = demonstracao(dem, nivel=3)
        tot = d.loc[d["CD_CONTA"] == base_cod, ["2024", "2025"]].iloc[0]
        d["AV_2025"] = d["2025"] / tot["2025"]
        d["AV_2024"] = d["2024"] / tot["2024"]
        d["var_abs"] = d["2025"] - d["2024"]
        d["var_pct"] = np.where(d["2024"] != 0, d["var_abs"] / d["2024"].abs(), np.nan)
        d["acima_limite"] = (d["var_abs"].abs() > MATERIALIDADE_EXECUCAO) & (d["var_pct"].abs() > 0.10)
        d.insert(0, "demonstracao", dem)
        partes.append(d)
    return pd.concat(partes, ignore_index=True)


def analiticos(m: dict) -> pd.DataFrame:
    """PT 520 - expectativas independentes, precisão e investigação."""
    receita_propria_bruta = sum(x[1] for x in ne.NE22_RECEITA if x[0] != "Trading")
    vendas = ne.OPERACIONAL["vendas_2025_mmbbl"] * 1e6
    desconto_premissa = 4.00   # US$/bbl - premissa: média histórica de descontos de qualidade divulgados (RA)
    esperado_receita = vendas * (m["brent_medio_2025"] - desconto_premissa) * m["ptax_media_2025"] / 1000
    prod25 = ne.OPERACIONAL["producao_media_2025_bpd"] * 365 / 1e6
    prod24 = ne.OPERACIONAL["producao_media_2025_bpd"] / (1 + ne.OPERACIONAL["crescimento_producao"]) * 365 / 1e6
    da25, da24 = conta("DFC_MI", "6.01.01.02"), conta("DFC_MI", "6.01.01.02", "PENÚLTIMO")
    # Expectativa D&A (duas parcelas):
    #  (a) ativos legados: taxa R$/bbl de 2024 sem Peregrino (D&A Peregrino 2024 = 53.285 + 38.555 + 11.416, NE 8/9)
    #      x barris legados de 2025 (barris de Peregrino estimados pela participação na receita própria, NE 22);
    #  (b) Peregrino: valor contábil de abertura (NE 8/9: 4.179.633 + 3.236.104 + 3.722.532) amortizado de forma
    #      aproximadamente linear até o fim da concessão então vigente (2031 = 6 anos) + parcela de +40% adquirida
    #      em 11/11/2025 (NE 9.d: 6.794.400 + 1.928.710 + ARO 1.322.571) pro rata de 50 dias.
    prod_pere = ne.NE22_RECEITA[3][1] / receita_propria_bruta * prod25
    taxa_legado = (da24 - (53_285 + 38_555 + 11_416)) / prod24
    esperado_da = (taxa_legado * (prod25 - prod_pere)
                   + (4_179_633 + 3_236_104 + 3_722_532) / 6.0
                   + (6_794_400 + 1_928_710 + 1_322_571) / 6.14 * 50 / 365)
    divida24 = 11_936_077 + 6_465_871   # NE 13 e 14 - saldos de 31/12/2024
    divida25 = ne.NE13_TOTAL["total"] + ne.NE14_DEBENTURES["total"]
    esperado_juros = (divida24 + divida25) / 2 * ne.OPERACIONAL["custo_medio_divida"]
    juros = 1_344_905
    aro_ini = ne.NE17_TOTAL["saldo2024"]
    taxa_media_aro = 0.0755
    esperado_aro = (aro_ini + ne.NE9D_PEREGRINO_40["aro_complemento"] * 50 / 365) * taxa_media_aro
    royalties = 1_533_652
    linhas = [
        ("Receita de venda de óleo próprio (bruta)", "Volume vendido (37,8 MMbbl, RA p. 27) x (Brent médio EIA - desconto premissa US$ 4/bbl) x PTAX média BCB",
         esperado_receita, receita_propria_bruta, 0.05),
        ("Depreciação, amortização e exaustão", "Taxa R$/bbl 2024 (sem Peregrino) x barris legados 2025 + VC de abertura de Peregrino / 6 anos até 2031 + aquisição +40% pro rata",
         esperado_da, da25, 0.15),
        ("Juros sobre empréstimos e debêntures", "Dívida bruta média (NE 13+14) x custo médio da dívida 6,36% (RA p. 39)",
         esperado_juros, juros, 0.10),
        ("Atualização monetária da provisão de abandono", "Saldo inicial NE 17 + complemento Peregrino pro rata (50 dias) x taxa média 7,55%",
         esperado_aro, ne.NE17_TOTAL["atualizacao_monetaria"], 0.10),
        ("Royalties e participação especial", "10% (alíquota de royalties ANP) x receita bruta de óleo próprio",
         0.10 * receita_propria_bruta, royalties, 0.15),
    ]
    df = pd.DataFrame(linhas, columns=["conta", "expectativa_metodo", "valor_esperado", "valor_registrado", "precisao_pct"])
    df["diferenca"] = df["valor_registrado"] - df["valor_esperado"]
    df["diferenca_pct"] = df["diferenca"] / df["valor_esperado"]
    df["limite_investigacao"] = df["precisao_pct"] * df["valor_esperado"].abs()
    df["investigar"] = df["diferenca"].abs() > df["limite_investigacao"]
    # Se o limite supera a materialidade para execução, o analítico isolado não dá segurança suficiente (NBC TA 520 A13-A16)
    df["precisao_suficiente_isolada"] = df["limite_investigacao"] <= MATERIALIDADE_EXECUCAO
    return df


def decomposicao_da() -> pd.DataFrame:
    """PT 520 - investigação da diferença de D&A: decomposição por ativo a partir das movimentações (NE 8, 9 e 15)."""
    itens = [("Peregrino - plataforma (NE 8)", 1_076_933), ("Peregrino - ativos O&G (NE 8)", 1_185_119),
             ("Peregrino - concessão (NE 9)", 733_130), ("Albacora Leste - concessão (NE 9)", 1_314_370),
             ("Albacora Leste - FPSO Forte e O&G (NE 8)", 238_204 + 4_328), ("Frade - FPSO, O&G e concessão (NE 8/9)", 118_003 + 249_891 + 37_916),
             ("Polvo/TBMT - FPSO, O&G, plataforma e concessão (NE 8/9)", 90_432 + 92_018 + 4_663 + 52_517),
             ("Workover (NE 8)", 139_953), ("Sonda Hunter Queen (NE 8)", 57_324), ("Embarcação e demais (NE 8)", 10_226 + 227 + 267 + 4_083 + 1_736),
             ("Direito de uso (NE 15)", 293_368)]
    df = pd.DataFrame(itens, columns=["ativo", "depreciacao_2025"])
    df.loc[len(df)] = ["Soma das movimentações (moeda de apresentação, taxas históricas)", df["depreciacao_2025"].sum()]
    df.loc[len(df)] = ["D&A na DFC (6.01.01.02)", conta("DFC_MI", "6.01.01.02")]
    df.loc[len(df)] = ["Diferença (conversão por taxa média x histórica - hipótese)", df.iloc[-1, 1] - df.iloc[-2, 1]]
    return df


def indicadores() -> tuple[pd.DataFrame, dict]:
    ac, pc = conta("BPA", "1.01"), conta("BPP", "2.01")
    caixa = conta("BPA", "1.01.01")
    estoque = conta("BPA", "1.01.04")
    emprest = ne.NE13_TOTAL["total"] + ne.NE14_DEBENTURES["total"]
    arrend = ne.NE15_TOTAL["passivo"]
    ebit = conta("DRE", "3.05")
    da = conta("DFC_MI", "6.01.01.02")
    outras = -(conta("DRE", "3.04.05") + conta("DRE", "3.04.04"))
    ebitda_aj = ebit + da + outras
    dl = emprest - caixa
    juros_pagos = -(conta("DFC_MI", "6.03.04") + conta("DFC_MI", "6.03.13"))
    fco = conta("DFC_MI", "6.01")
    capex = -(conta("DFC_MI", "6.02.01") + conta("DFC_MI", "6.02.02"))
    pl = conta("BPP", "2.03")
    receita = conta("DRE", "3.01")
    # Pró-forma de covenant: EBITDA LTM da participação adicional de 40% em Peregrino (premissa didática)
    ebitda_pere_40 = 40_000 * 365 * 35 * 5.5855 / 1000   # 40 kbpd x US$ 35/bbl de margem EBITDA x PTAX média
    ind = [
        ("Liquidez corrente", ac / pc, conta("BPA", "1.01", "PENÚLTIMO") / conta("BPP", "2.01", "PENÚLTIMO"), "> 1,0"),
        ("Liquidez seca", (ac - estoque) / pc, (conta("BPA", "1.01", "PENÚLTIMO") - conta("BPA", "1.01.04", "PENÚLTIMO"))
         / conta("BPP", "2.01", "PENÚLTIMO"), "> 1,0"),
        ("Dívida bruta (empréstimos + debêntures) R$ mil", emprest, 11_936_077 + 6_465_871, "-"),
        ("Dívida líquida R$ mil", dl, 11_936_077 + 6_465_871 - conta("BPA", "1.01.01", "PENÚLTIMO"), "-"),
        ("EBITDA ajustado R$ mil", ebitda_aj, conta("DRE", "3.05", "PENÚLTIMO") + conta("DFC_MI", "6.01.01.02", "PENÚLTIMO")
         - conta("DRE", "3.04.04", "PENÚLTIMO"), "-"),
        ("Dívida líquida / EBITDA ajustado (sem pró-forma)", dl / ebitda_aj, None, "<= 2,5x (covenant)"),
        ("Dívida líquida / EBITDA ajustado pró-forma Peregrino 40% (premissa)", dl / (ebitda_aj + ebitda_pere_40), None,
         "<= 2,5x (covenant)"),
        ("EBITDA mínimo para atender 2,5x (sem pró-forma) R$ mil", dl / 2.5, None, "-"),
        ("Cobertura de juros (EBITDA aj. / juros pagos)", ebitda_aj / juros_pagos, None, "> 3,0x"),
        ("FCO / dívida bruta", fco / emprest, None, "-"),
        ("FCO - capex (fluxo livre antes de aquisições) R$ mil", fco - capex, None, "> 0"),
        ("Endividamento (passivo total / PL)", (conta("BPP", "2.01") + conta("BPP", "2.02")) / pl, None, "-"),
        ("Margem EBITDA ajustado", ebitda_aj / receita, None, "-"),
        ("Prazo médio de recebimento (dias)", conta("BPA", "1.01.03") / receita * 365,
         conta("BPA", "1.01.03", "PENÚLTIMO") / conta("DRE", "3.01", "PENÚLTIMO") * 365, "30 dias (NE 2.6)"),
    ]
    df = pd.DataFrame(ind, columns=["indicador", "2025", "2024", "referencia"])
    extra = {"divida_liquida": dl, "ebitda_aj": ebitda_aj, "alavancagem": dl / ebitda_aj,
             "alavancagem_proforma": dl / (ebitda_aj + ebitda_pere_40), "ebitda_pere_40_premissa": ebitda_pere_40,
             "liquidez_corrente": ac / pc, "fco": fco, "capex": capex}
    return df, extra


def sensibilidade_aro() -> pd.DataFrame:
    linhas = []
    for campo, saldo, _s24, ano, taxa in ne.NE17_ARO:
        if saldo <= 0:   # Polvo: saldo líquido do fundo de abandono - não sensibilizado (limitação)
            continue
        t = max(ano - 2025, 0.5)
        fv = saldo * (1 + taxa) ** t
        for cen, dt, dc, dano in [("Base", 0, 0, 0), ("Taxa -1 p.p.", -0.01, 0, 0), ("Taxa +1 p.p.", 0.01, 0, 0),
                                  ("Custo +10%", 0, 0.10, 0), ("Custo +20%", 0, 0.20, 0), ("Custo -10%", 0, -0.10, 0),
                                  ("Abandono 2 anos antes", 0, 0, -2), ("Abandono 2 anos depois", 0, 0, 2)]:
            tt = max(t + dano, 0.5)
            pv = fv * (1 + dc) / (1 + taxa + dt) ** tt
            linhas.append({"campo": campo, "cenario": cen, "ano_abandono": ano + dano, "taxa": taxa + dt,
                           "custo_futuro_estimado": fv * (1 + dc), "valor_presente": pv, "variacao": pv - saldo})
    df = pd.DataFrame(linhas)
    tot = df.groupby("cenario")[["valor_presente", "variacao"]].sum().reset_index()
    tot["campo"] = "TOTAL (exceto Polvo)"
    return pd.concat([df, tot], ignore_index=True)


def componentes() -> pd.DataFrame:
    receita = {x[0]: x[3] for x in ne.NE22_RECEITA}
    imob = {
        "Peregrino (Prio Tigris)": 5_448_957 + 8_211_522,
        "Frade + Wahoo (Prio Forte/Bravo)": 1_015_091 + 1_993_861 + 794_285 + 238_255,
        "Albacora Leste (Prio Forte)": 1_301_322 + 332_734,
        "Polvo & TBMT (Prio Bravo / Lux)": 23_854 + 503_504 + 503_286,
    }
    intang = {"Peregrino (Prio Tigris)": 4_542_886 + 523_278, "Frade + Wahoo (Prio Forte/Bravo)": 284_158 + 833_949,
              "Albacora Leste (Prio Forte)": 7_033_798, "Polvo & TBMT (Prio Bravo / Lux)": 284_218}
    rec = {"Peregrino (Prio Tigris)": receita["Peregrino"], "Frade + Wahoo (Prio Forte/Bravo)": receita["Frade"],
           "Albacora Leste (Prio Forte)": receita["Albacora Leste"], "Polvo & TBMT (Prio Bravo / Lux)": receita["Polvo/TBMT"],
           "Trading (Lux Holding / PrioAustria / PrioOG)": receita["Trading"]}
    aro = {"Peregrino (Prio Tigris)": 2_978_159, "Frade + Wahoo (Prio Forte/Bravo)": 350_213,
           "Albacora Leste (Prio Forte)": 1_805_585, "Polvo & TBMT (Prio Bravo / Lux)": 238_335 - 11_099}
    nomes = list(rec)
    df = pd.DataFrame({"componente": nomes, "receita_liquida": [rec[n] for n in nomes],
                       "imobilizado_operacao_ne8": [imob.get(n, 0) for n in nomes],
                       "intangivel_ne9": [intang.get(n, 0) for n in nomes], "aro_ne17": [aro.get(n, 0) for n in nomes]})
    df["pct_receita"] = df["receita_liquida"] / conta("DRE", "3.01")
    df["pct_ativo_longo"] = (df["imobilizado_operacao_ne8"] + df["intangivel_ne9"]) / conta("BPA", "1")
    df["significativo"] = np.where((df["pct_receita"] > 0.15) | (df["pct_ativo_longo"] > 0.15), "Sim - auditoria completa",
                                   "Não - procedimentos analíticos de grupo / específicos")
    df["materialidade_componente"] = np.where(df["significativo"].str.startswith("Sim"),
                                              np.minimum(MATERIALIDADE_EXECUCAO * 0.75, MATERIALIDADE_GLOBAL * np.maximum(df["pct_receita"], 0.4)),
                                              MATERIALIDADE_EXECUCAO * 0.5).round(-3)
    return df


def main() -> None:
    R.mkdir(exist_ok=True)
    m = mercado()
    pd.DataFrame(bases_materialidade()).to_csv(R / "PT320_bases_materialidade.csv", index=False, encoding="utf-8-sig")
    rec = reconciliacoes()
    rec.to_csv(R / "PT500_reconciliacao_notas_x_demonstracoes.csv", index=False, encoding="utf-8-sig")
    si = saldos_iniciais()
    si.to_csv(R / "PT510_saldos_iniciais.csv", index=False, encoding="utf-8-sig")
    hv = horizontal_vertical()
    hv.to_csv(R / "PT520_analise_horizontal_vertical.csv", index=False, encoding="utf-8-sig")
    an = analiticos(m)
    an.to_csv(R / "PT520_procedimentos_analiticos.csv", index=False, encoding="utf-8-sig")
    decomposicao_da().to_csv(R / "PT520_decomposicao_da.csv", index=False, encoding="utf-8-sig")
    ind, extra = indicadores()
    ind.to_csv(R / "PT570_indicadores.csv", index=False, encoding="utf-8-sig")
    sens = sensibilidade_aro()
    sens.to_csv(R / "PT540_sensibilidade_aro.csv", index=False, encoding="utf-8-sig")
    comp = componentes()
    comp.to_csv(R / "PT600_componentes.csv", index=False, encoding="utf-8-sig")
    resumo = {"mercado": m, "indicadores": extra,
              "reconciliacao_itens": len(rec), "reconciliacao_diferencas": int((rec["situacao"] != "Conciliado").sum()),
              "saldos_iniciais_diferencas": int((si["situacao"] != "Igual").sum()),
              "analiticos_investigar": int(an["investigar"].sum())}
    (R / "resumo_analiticos.json").write_text(json.dumps(resumo, indent=2, ensure_ascii=False, default=float), encoding="utf-8")
    pd.set_option("display.width", 250)
    pd.set_option("display.max_colwidth", 60)
    print(json.dumps(m, indent=1))
    print(rec[["item", "valor_demonstracao", "valor_nota", "diferenca", "situacao"]].to_string(index=False))
    print(si[si["situacao"] != "Igual"].to_string(index=False))
    print(an[["conta", "valor_esperado", "valor_registrado", "diferenca_pct", "limite_investigacao", "investigar"]].to_string(index=False))
    print(ind.to_string(index=False))
    print(sens[sens["campo"].str.startswith("TOTAL")].to_string(index=False))
    print(comp.to_string(index=False))


if __name__ == "__main__":
    main()
