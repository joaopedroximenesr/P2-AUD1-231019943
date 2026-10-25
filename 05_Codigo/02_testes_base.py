"""
Procedimentos de auditoria sobre a BASE SIMULADA de imobilizado (*** dados sintéticos ***).

  PT 500  - Conciliação da base com a NE 8 / NE 15 / BP 1.02.03 e explicação das diferenças
  PT 330  - Testes em 100% da população (CAATs) T01 a T12
  PT 530  - Amostragem estatística: MUS (unidade monetária) para existência/avaliação e
            amostragem por atributos para o controle de aprovação
  PT 450  - Projeção de distorções e comparação "erros inseridos x erros detectados"

Uso: python 05_Codigo/02_testes_base.py      (requer base gerada por 01_gerar_base.py)
Saídas em 06_Resultados/ (csv + resumo_testes.json)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from notas_dfp2025 import NE8_IMOBILIZADO, NE15_DIREITO_USO  # noqa: E402
from parametros import MATERIALIDADE_EXECUCAO, RESULTADOS, SEMENTE, LIMITE_TRIVIAL  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
BASE = RAIZ / "02_Base_Simulada"
DATA_BASE = pd.Timestamp("2025-12-31")
ALCADA = 5_000_000.0
rng = np.random.default_rng(SEMENTE + 530)

# Fatores de confiabilidade (Poisson) para MUS - 95% de confiança (k = nº de distorções)
FATOR_95 = [3.00, 4.75, 6.30, 7.76, 9.16, 10.52, 11.85, 13.15, 14.44, 15.71, 16.97, 18.21, 19.45, 20.67, 21.89,
            23.10, 24.31, 25.50, 26.70, 27.88, 29.07]
CAMPO_ENTIDADE_VALIDO = {
    "Peregrino": {"Prio Tigris"}, "Frade": {"Prio Forte", "Prio Bravo"}, "Albacora Leste": {"Prio Forte", "Prio Bravo"},
    "Wahoo": {"Prio Forte"}, "Polvo & TBMT": {"Prio Bravo", "Lux Holding"}, "Corporativo": {"PrioOG"},
}


def fator(k: int) -> float:
    return FATOR_95[k] if k < len(FATOR_95) else FATOR_95[-1] + 1.2 * (k - len(FATOR_95) + 1)


def carregar() -> pd.DataFrame:
    tipos = {"quantidade": "float64", "unidade": "string"}
    b = pd.read_csv(BASE / "base_imobilizado_sintetica.csv.gz", dtype=tipos,
                    parse_dates=["data_aquisicao", "data_capitalizacao", "data_lancamento", "data_ultima_movimentacao"])
    assert (b["flag_dado"] == "SINTETICO - fins didaticos").all()
    return b


# ------------------------------------------------------------------------------------- PT 500
def conciliar(b: pd.DataFrame, log: pd.DataFrame) -> pd.DataFrame:
    livro = {n: s for (n, *_r, s, _s24) in NE8_IMOBILIZADO}
    livro.update({f"Direito de uso - {n}": s for (n, _c, _d, _a, s) in NE15_DIREITO_USO})
    base = b.groupby("classe_ne")["valor_contabil_brl"].sum() / 1000
    lg = log.merge(b[["id_registro", "classe_ne"]], on="id_registro", how="left")
    erros = lg.groupby("classe_ne")["impacto_valor_contabil_brl"].sum() / 1000
    t = pd.DataFrame({"saldo_nota_rmil": pd.Series(livro), "saldo_base_rmil": base}).fillna(0)
    t["diferenca_rmil"] = t["saldo_base_rmil"] - t["saldo_nota_rmil"]
    t["explicado_erros_inseridos_rmil"] = erros.reindex(t.index).fillna(0)
    t["diferenca_nao_explicada_rmil"] = (t["diferenca_rmil"] - t["explicado_erros_inseridos_rmil"]).round(2)
    t.loc["TOTAL"] = t.sum(numeric_only=True)
    return t.round(2)


# ------------------------------------------------------------------------------------- PT 330
def caats(b: pd.DataFrame) -> pd.DataFrame:
    f = pd.DataFrame({"id_registro": b["id_registro"]})
    chave = ["id_bem", "documento_origem", "custo_historico_brl", "data_aquisicao"]
    f["T01_duplicidade"] = b.sort_values("id_registro").duplicated(chave, keep="first").reindex(b.index)
    f["T02_corte"] = (b["data_aquisicao"] > DATA_BASE) | (b["data_lancamento"] > DATA_BASE)
    f["T03_vc_negativo"] = (b["valor_contabil_brl"] < 0) | (-b["depreciacao_acumulada_brl"] > b["custo_historico_brl"] + 0.01)
    f["T04_deprec_andamento"] = (b["grupo"] == "Em andamento") & (b["depreciacao_acumulada_brl"] != 0)
    lin = b["metodo_depreciacao"] == "Linear"
    anos = (DATA_BASE - b["data_capitalizacao"]).dt.days / 365.25
    esperado = (b["custo_historico_brl"] * np.minimum(1, b["taxa_depreciacao_anual"] * anos)).where(lin)
    dif = (-b["depreciacao_acumulada_brl"] - esperado).abs()
    f["T05_recalculo_linear"] = lin & (dif > np.maximum(1000, 0.02 * esperado))
    conv = (b["custo_historico_brl"] - b["custo_usd"] * b["taxa_cambio_historica"]).abs()
    f["T06_inconsistencia_conversao"] = conv > (1 + 0.001 * b["custo_historico_brl"])
    f["T07_segregacao"] = b["aprovador"] == b["usuario_lancamento"]
    f["T08_alcada"] = (b["custo_historico_brl"] > ALCADA) & (~b["aprovador"].str.startswith("DIR"))
    score = ((b["custo_historico_brl"] % 100_000 == 0) & (b["custo_historico_brl"] >= 1_000_000)).astype(int) \
        + (b["data_lancamento"].dt.weekday >= 5).astype(int) \
        + (~b["usuario_lancamento"].str.match(r"^USR\d{3}$")).astype(int) \
        + b["documento_origem"].str.startswith("AJ-").astype(int) \
        + b["descricao"].str.contains("Ajuste manual", case=False).astype(int) \
        + (b["fornecedor_id"] == "SEM-FORNECEDOR").astype(int)
    f["T09_score_lancamento"] = score
    f["T09_lancamento_suspeito"] = score >= 3
    valido = b.apply(lambda r: r["grupo"] == "Direito de uso"
                     or r["entidade"] in CAMPO_ENTIDADE_VALIDO.get(r["campo_ugc"], {r["entidade"]}), axis=1)
    f["T10_entidade_ugc"] = ~valido
    # Indicadores (não são "erros"): obsolescência e atipicidade estatística
    mat = b["classe_ne"].isin(["Material poços", "Sobressalentes"])
    f["T11_sem_movimento_12m"] = mat & (b["data_ultima_movimentacao"] < DATA_BASE - pd.Timedelta(days=365))
    lc = np.log10(b["custo_historico_brl"].clip(lower=1))
    g = lc.groupby([b["classe_ne"], b["descricao"]])
    med, mad = g.transform("median"), g.transform(lambda s: (s - s.median()).abs().median())
    f["T12_atipico_estatistico"] = ((lc - med) / (1.4826 * mad.replace(0, np.nan))).abs() > 4
    return f


def benford(b: pd.DataFrame) -> pd.DataFrame:
    v = b.loc[b["custo_historico_brl"] >= 10, "custo_historico_brl"]
    d1 = v.astype(str).str.lstrip("0.").str[0].astype(int)
    obs = d1.value_counts(normalize=True).sort_index()
    esp = pd.Series({d: math.log10(1 + 1 / d) for d in range(1, 10)})
    t = pd.DataFrame({"digito": range(1, 10), "observado": obs.reindex(range(1, 10)).fillna(0).values, "esperado_benford": esp.values})
    t["desvio_abs"] = (t["observado"] - t["esperado_benford"]).abs()
    return t


def comparar(f: pd.DataFrame, log: pd.DataFrame) -> pd.DataFrame:
    mapa = {"E01-Duplicidade": "T01_duplicidade", "E02-Corte": "T02_corte", "E03-VC negativo": "T03_vc_negativo",
            "E04-Depreciação em andamento": "T04_deprec_andamento", "E05-Taxa incorreta": "T05_recalculo_linear",
            "E06-Digitação x10": "T06_inconsistencia_conversao", "E07-Segregação de funções": "T07_segregacao",
            "E08-Alçada": "T08_alcada", "E09-Lançamento manual suspeito": "T09_lancamento_suspeito",
            "E10-Entidade/UGC incoerente": "T10_entidade_ugc"}
    erros_ids = set(log["id_registro"])
    linhas = []
    for tipo, teste in mapa.items():
        ids_tipo = set(log.loc[log["tipo_erro"] == tipo, "id_registro"])
        sinalizados = set(f.loc[f[teste], "id_registro"])
        vp = len(ids_tipo & sinalizados)
        outros_erros = len((sinalizados - ids_tipo) & erros_ids)
        fp = len(sinalizados - erros_ids)
        linhas.append({"tipo_erro_inserido": tipo, "teste": teste, "inseridos": len(ids_tipo), "detectados": vp,
                       "nao_detectados": len(ids_tipo) - vp, "taxa_deteccao": round(vp / len(ids_tipo), 4),
                       "sinalizados_total": len(sinalizados), "sinalizados_outros_erros_inseridos": outros_erros,
                       "falsos_positivos": fp})
    return pd.DataFrame(linhas)


# ------------------------------------------------------------------------------------- PT 530
def mus(b: pd.DataFrame, suporte: pd.DataFrame):
    pop = b[b["valor_contabil_brl"] > 0].reset_index(drop=True)
    bv = pop["valor_contabil_brl"].sum()
    tm = MATERIALIDADE_EXECUCAO * 1000.0
    em = 0.10 * tm
    n = math.ceil(bv * FATOR_95[0] / (tm - em * 1.6))
    j = bv / n
    inicio = rng.uniform(0, j)
    acum = pop["valor_contabil_brl"].cumsum().to_numpy()
    pontos = inicio + j * np.arange(n)
    idx = np.unique(np.searchsorted(acum, pontos, side="left"))
    amostra = pop.iloc[idx].copy()
    amostra["estrato"] = np.where(amostra["valor_contabil_brl"] >= j, "Topo (>= intervalo)", "Amostral")
    amostra = amostra.merge(suporte[["id_registro", "valor_contabil_brl"]].rename(columns={"valor_contabil_brl": "valor_auditado_brl"}),
                            on="id_registro", how="left")
    amostra["valor_auditado_brl"] = amostra["valor_auditado_brl"].fillna(0.0)  # sem documento-suporte = inexistente
    amostra["distorcao_brl"] = (amostra["valor_contabil_brl"] - amostra["valor_auditado_brl"]).round(2)
    amostra["taint"] = (amostra["distorcao_brl"] / amostra["valor_contabil_brl"]).clip(upper=1.0)
    amostra["distorcao_projetada_brl"] = np.where(amostra["estrato"].str.startswith("Topo"), amostra["distorcao_brl"],
                                                  amostra["taint"] * j)
    sup_ = amostra[amostra["distorcao_brl"] > 0.01]
    amostral = sup_[~sup_["estrato"].str.startswith("Topo")].sort_values("taint", ascending=False)
    topo = sup_[sup_["estrato"].str.startswith("Topo")]
    precisao_basica = FATOR_95[0] * j
    incremento = sum((fator(k + 1) - fator(k) - 1) * t * j for k, t in enumerate(amostral["taint"]))
    projetada = amostral["distorcao_projetada_brl"].sum() + topo["distorcao_brl"].sum()
    lsd = precisao_basica + projetada + incremento
    parametros = {"populacao_itens": int(len(pop)), "valor_contabil_populacao_brl": round(bv, 2), "confianca": 0.95,
                  "fator_confiabilidade": FATOR_95[0], "distorcao_toleravel_brl": tm, "distorcao_esperada_brl": em,
                  "fator_expansao": 1.6, "tamanho_amostra_calculado": n, "intervalo_amostral_brl": round(j, 2),
                  "inicio_aleatorio_brl": round(inicio, 2), "itens_selecionados": int(len(amostra)),
                  "itens_topo": int((amostra["estrato"] != "Amostral").sum()),
                  "valor_selecionado_brl": round(amostra["valor_contabil_brl"].sum(), 2),
                  "cobertura_valor": round(amostra["valor_contabil_brl"].sum() / bv, 4),
                  "distorcoes_encontradas": int(len(sup_)), "distorcao_conhecida_amostra_brl": round(sup_["distorcao_brl"].sum(), 2),
                  "distorcao_projetada_brl": round(projetada, 2), "precisao_basica_brl": round(precisao_basica, 2),
                  "provisao_incremental_brl": round(incremento, 2), "limite_superior_distorcao_brl": round(lsd, 2),
                  "conclusao": "LSD > distorção tolerável: rejeitar a hipótese de saldo não distorcido de forma relevante"
                  if lsd > tm else "LSD <= distorção tolerável: aceitar o saldo testado"}
    return amostra, parametros


def atributos(b: pd.DataFrame):
    n, tdr, edr = 93, 0.05, 0.005   # tabela AICPA: 95% confiança, desvio tolerável 5%, esperado 0,5%
    am = b.sample(n=n, random_state=SEMENTE).copy()
    am["desvio_segregacao"] = am["aprovador"] == am["usuario_lancamento"]
    am["desvio_alcada"] = (am["custo_historico_brl"] > ALCADA) & (~am["aprovador"].str.startswith("DIR"))
    am["desvio"] = am["desvio_segregacao"] | am["desvio_alcada"]
    k = int(am["desvio"].sum())
    lim = fator(k) / n
    par = {"populacao": int(len(b)), "tamanho_amostra": n, "confianca": 0.95, "desvio_toleravel": tdr, "desvio_esperado": edr,
           "desvios_encontrados": k, "taxa_desvio_amostra": round(k / n, 4), "limite_superior_desvio": round(lim, 4),
           "conclusao": "Controle pode ser considerado efetivo (LSD <= taxa tolerável)" if lim <= tdr else
           "Controle NÃO pode ser considerado efetivo: ampliar testes substantivos"}
    return am, par


def main() -> None:
    RESULTADOS.mkdir(exist_ok=True)
    b = carregar()
    log = pd.read_csv(BASE / "registro_erros_inseridos.csv")
    suporte = pd.read_csv(BASE / "documentacao_suporte_simulada.csv.gz")
    print(f"Base: {len(b):,} linhas | R$ {b['valor_contabil_brl'].sum():,.2f}")

    conc = conciliar(b, log)
    conc.to_csv(RESULTADOS / "PT500_conciliacao_base_x_notas.csv", encoding="utf-8-sig")

    f = caats(b)
    excecoes = f[f.drop(columns=["id_registro", "T09_score_lancamento"]).any(axis=1)]
    excecoes = excecoes.merge(b[["id_registro", "classe_ne", "entidade", "campo_ugc", "descricao", "valor_contabil_brl",
                                 "usuario_lancamento", "aprovador", "data_lancamento"]], on="id_registro")
    excecoes.to_csv(RESULTADOS / "PT330_excecoes_caat.csv.gz", index=False, encoding="utf-8", compression="gzip")
    resumo_t = []
    for c in [c for c in f.columns if c.startswith("T") and c != "T09_score_lancamento"]:
        m = f[c].fillna(False).astype(bool)
        resumo_t.append({"teste": c, "itens_sinalizados": int(m.sum()),
                         "valor_contabil_sinalizado_brl": round(b.loc[m.values, "valor_contabil_brl"].sum(), 2)})
    resumo_t = pd.DataFrame(resumo_t)
    resumo_t.to_csv(RESULTADOS / "PT330_resumo_caat.csv", index=False, encoding="utf-8-sig")

    comp = comparar(f.fillna(False), log)
    comp.to_csv(RESULTADOS / "PT450_inseridos_x_detectados.csv", index=False, encoding="utf-8-sig")
    benford(b).to_csv(RESULTADOS / "PT520_benford_custo.csv", index=False, encoding="utf-8-sig")

    amostra, par_mus = mus(b, suporte)
    amostra.to_csv(RESULTADOS / "PT530_amostra_mus.csv", index=False, encoding="utf-8-sig")
    # Reaplicação após ajustes simulados da administração (PT 450): exclui duplicidades, itens de 2026 e lançamentos
    # fictícios identificados em 100% da população (E01, E02, E09) e corrige os custos digitados x10 (E06).
    excluir = set(log.loc[log["tipo_erro"].isin(["E01-Duplicidade", "E02-Corte", "E09-Lançamento manual suspeito"]), "id_registro"])
    corr = b[~b["id_registro"].isin(excluir)].copy()
    ids06 = log.loc[log["tipo_erro"] == "E06-Digitação x10", "id_registro"]
    s06 = suporte.set_index("id_registro").loc[ids06]
    m06 = corr["id_registro"].isin(ids06)
    corr.loc[m06, "valor_contabil_brl"] = corr.loc[m06, "id_registro"].map(s06["valor_contabil_brl"]).values
    amostra2, par_mus2 = mus(corr, suporte)
    amostra2.to_csv(RESULTADOS / "PT530_amostra_mus_pos_ajustes.csv", index=False, encoding="utf-8-sig")
    par_mus2["base_apos_ajustes_brl"] = round(corr["valor_contabil_brl"].sum(), 2)
    am_attr, par_attr = atributos(b)
    am_attr.to_csv(RESULTADOS / "PT530_amostra_atributos.csv", index=False, encoding="utf-8-sig")

    # Distorção real (conhecida pelo gabarito) para avaliar a eficácia da projeção
    impacto = log.groupby("tipo_erro")["impacto_valor_contabil_brl"].agg(["count", "sum"]).reset_index()
    impacto.columns = ["tipo_erro", "registros", "impacto_valor_contabil_brl"]
    impacto.to_csv(RESULTADOS / "PT450_impacto_erros_inseridos.csv", index=False, encoding="utf-8-sig")
    superavaliacao_real = log.loc[log["impacto_valor_contabil_brl"] > 0, "impacto_valor_contabil_brl"].sum()
    subavaliacao_real = log.loc[log["impacto_valor_contabil_brl"] < 0, "impacto_valor_contabil_brl"].sum()
    obsoleto = b.loc[f["T11_sem_movimento_12m"].values, "valor_contabil_brl"].sum()

    resumo = {
        "base_linhas": int(len(b)), "base_total_brl": round(b["valor_contabil_brl"].sum(), 2),
        "saldo_bp_brl": 31_142_804_000.0, "diferenca_conciliacao_brl": round(b["valor_contabil_brl"].sum() - 31_142_804_000.0, 2),
        "diferenca_nao_explicada_rmil": float(conc.loc["TOTAL", "diferenca_nao_explicada_rmil"]),
        "erros_inseridos": int(len(log)), "superavaliacao_real_brl": round(superavaliacao_real, 2),
        "subavaliacao_real_brl": round(subavaliacao_real, 2), "limite_trivial_brl": LIMITE_TRIVIAL * 1000,
        "mus": par_mus, "mus_pos_ajustes": par_mus2, "atributos": par_attr, "obsolescencia_valor_brl": round(obsoleto, 2),
        "obsolescencia_itens": int(f["T11_sem_movimento_12m"].sum()),
        "atipicos_estatisticos": int(f["T12_atipico_estatistico"].fillna(False).sum()),
        "deteccao_total": round(comp["detectados"].sum() / comp["inseridos"].sum(), 4),
        "falsos_positivos_total": int(comp["falsos_positivos"].sum()),
    }
    (RESULTADOS / "resumo_testes.json").write_text(json.dumps(resumo, indent=2, ensure_ascii=False, default=float), encoding="utf-8")
    print(conc.tail(3).to_string())
    print(resumo_t.to_string(index=False))
    print(comp.to_string(index=False))
    print(json.dumps(par_mus, indent=1, ensure_ascii=False))
    print(json.dumps(par_mus2, indent=1, ensure_ascii=False))
    print(json.dumps(par_attr, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
