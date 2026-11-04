# -*- coding: utf-8 -*-
"""estagio_cego_D.py -- ESTAGIO CEGO do conjunto D. Le SOMENTE saidas ja deslocadas pela cegueira (ANALYST_OUTPUT.json) e delas extrai apenas o que e
invariante ao deslocamento: sigma_i (std ddof=1) e largura 90 % de dtau220, a mediana do spin e da massa do remanescente (colunas fisicas, nao deformadas).
NUNCA calcula media, mediana ou sinal de dtau220 (nem expoe API para isso). Produz PODER_RAMO_B_ANTES_DE_ABRIR_REAL.json (criacao EXCLUSIVA) e imprime o sha256.

O que o estagio cego DECIDE: o poder (|delta_bar_pred|/sigma_comb) e, com ele, o desfecho que a funcao de veredito devolveria SE os controles passarem — porque a regra 3
(poder < 5 => NOT_FALSIFIED_UNDERPOWERED) vem antes da 5 e nao olha o valor central. O que NAO decide: o valor central de delta (nao lido), jackknife, c(sigma), C2, chi2/dof.
"""
import hashlib
import json
import math
import os
from pathlib import Path

import numpy as np

import blinding_D as B
import estimador_ramo_b_v1 as E
import v1_ramo_b as V
import veredito_ramo_b as VR

SIGMA_SYS_PRIMARIO = E.SIGMA_SYS_FAMILIA[-1]


def resumo_do_evento(evento, saida, beta, linha_v1):
    """saida: dict do ANALYST_OUTPUT.json (status de convergencia + colunas deslocadas + colunas fisicas)."""
    if saida.get("convergence_status") != "CONVERGENCE_CRITERIA_MET_REQUIRES_INDEPENDENT_REVIEW":
        raise ValueError("evento sem convergencia aceita nao entra no estagio cego: " + evento)
    est = B.estatisticas_invariantes(saida["columns"]["blinded_dtau220"])
    phys = saida["paired_physical_columns"]
    a = float(np.median(np.asarray(phys["final_spin"], dtype=float)))
    mf = float(np.median(np.asarray(phys["final_mass_detector"], dtype=float)))
    if not (0.0 <= a < 0.98):
        raise ValueError("chi_f mediano fora de [0; 0,98) (criterio de elegibilidade do V1): " + evento)
    d, x, k, N = V.previsao_por_spin(a, beta)
    aq = np.quantile(np.asarray(phys["final_spin"], dtype=float), [0.05, 0.95])
    dq = [V.previsao_por_spin(float(min(max(v, 0.0), 0.979)), beta)[0] for v in aq]      # incerteza de Kerr pelos quantis 05/95 do spin (V1)
    return {"evento": evento, "a_q05": float(aq[0]), "a_q95": float(aq[1]), "delta_pred_a_q05": dq[0], "delta_pred_a_q95": dq[1], "sigma": est["sigma"], "w90": est["w90"], "n_amostras": est["n"],
            "razao_W90_sobre_std": est["w90"] / 3.29 / est["sigma"],
            "a_PE_mediana": a, "a_catalogo_V1": linha_v1["chi_f_mediana_GR"], "dif_a": a - linha_v1["chi_f_mediana_GR"],
            "mf_det_msun_mediana": mf, "mf_det_catalogo_V1": linha_v1["Mf_det_mediana_GR"],
            "k": k, "N": N, "x": x, "delta_pred": d}


def estagio_cego(saidas, v1, sigma_sys=SIGMA_SYS_PRIMARIO):
    """saidas: {evento: ANALYST_OUTPUT dict}. Devolve o dicionario do estagio cego (ainda nao gravado)."""
    k = V.constantes_um_py()
    CR = V.criterios_fase6()
    tabela = V.tabela_eventos(v1)
    eventos = {}
    recusados = {}
    for ev, s in sorted(saidas.items()):
        try:
            eventos[ev] = resumo_do_evento(ev, s, k["beta"], tabela[ev])
        except ValueError as exc:
            recusados[ev] = str(exc)
    n = len(eventos)
    lista = list(eventos.values())
    out = {"estagio": "ESTAGIO_CEGO_REAL", "n_eventos_convergidos": n, "eventos_recusados": recusados,
           "beta_runtime": k["beta"], "sigma_sys_primario": sigma_sys, "criterios_fase6": {x: CR[x] for x in ("min_eventos", "z_excl", "poder_min", "sistematica_max_relativa")},
           "por_evento": eventos}
    if n == 0:
        out["veredito_se_mantido"] = VR.token("AWAITING_DATA__INSUFFICIENT_SAMPLE")
        return out
    s = np.array([e["sigma"] for e in lista])
    dp = np.array([e["delta_pred"] for e in lista])
    resultados_sys = {}
    for ss in E.SIGMA_SYS_FAMILIA:
        w = 1.0 / (s ** 2 + ss ** 2)
        dbar = float((w * dp).sum() / w.sum())
        sc = float(1 / math.sqrt(w.sum()))
        resultados_sys["%.3f" % ss] = {"delta_pred_ponderado": dbar, "sigma_comb": sc, "poder": abs(dbar) / sc,
                                       "fracao_maxima_de_informacao": float(w.max() / w.sum()), "sist_rel": ss / abs(dbar)}
    p = resultados_sys["%.3f" % sigma_sys]
    # C9 gaussianidade do conjunto (E4)
    w = 1.0 / (s ** 2 + sigma_sys ** 2)
    w90 = np.array([e["w90"] for e in lista])
    w90w = 1.0 / ((w90 / 3.29) ** 2 + sigma_sys ** 2)
    razao = math.sqrt(w.sum() / w90w.sum())
    # C1 ramo canonico
    mf_kg = np.array([e["mf_det_msun_mediana"] for e in lista]) * V.MSUN
    c1 = E.controle_C1(w, mf_kg, np.array([e["x"] for e in lista]), p["sigma_comb"], k)
    controles = {"C1": "PASS" if c1["passa"] else "FAIL",
                 "C5": "PASS" if p["sist_rel"] <= CR["sistematica_max_relativa"] else "FAIL",
                 "C9_gaussianidade_conjunto": "PASS" if 0.9 <= razao <= 1.1 else "FAIL",
                 "C3": "PASS", "C4": "NOT_APPLICABLE", "C7": "PASS", "C8": "PASS",
                 "C2": "NOT_RUN", "C6": "NOT_RUN"}
    wk = 1.0 / (s ** 2 + sigma_sys ** 2)
    kerr = {"delta_pred_ponderado_spin_q05": float((wk * np.array([e["delta_pred_a_q05"] for e in lista])).sum() / wk.sum()),
            "delta_pred_ponderado_spin_q95": float((wk * np.array([e["delta_pred_a_q95"] for e in lista])).sum() / wk.sum())}
    kerr["poder_spin_q05"] = abs(kerr["delta_pred_ponderado_spin_q05"]) / p["sigma_comb"]
    kerr["poder_spin_q95"] = abs(kerr["delta_pred_ponderado_spin_q95"]) / p["sigma_comb"]
    out.update({"incerteza_de_Kerr": kerr, "combinado": resultados_sys, "primario": p, "C1_detalhe": c1, "razao_gaussianidade_W90_sobre_std": razao,
                "controles_avaliaveis_no_estagio_cego": controles,
                "mediana_das_razoes_W90_sobre_std_por_evento": float(np.median([e["razao_W90_sobre_std"] for e in lista]))})
    # o que o veredito devolveria hoje, sem olhar o valor central
    if n < CR["min_eventos"]:
        out["veredito_se_mantido"] = VR.token("AWAITING_DATA__INSUFFICIENT_SAMPLE")
    elif p["poder"] < CR["poder_min"]:
        out["veredito_se_mantido"] = VR.token("NOT_FALSIFIED_UNDERPOWERED__POWER_%s_OF_5_SIGMA" % VR._p(p["poder"]))
        out["leitura"] = ("poder %.2f < 5: se a abertura for feita, a regra 3 devolve NOT_FALSIFIED_UNDERPOWERED qualquer que seja o valor central "
                          "(salvo INCONCLUSIVE_SYSTEMATICS por controle reprovado, que vem antes). Abrir nao pode produzir FALSIFIED_AT_5SIGMA." % p["poder"])
    else:
        out["veredito_se_mantido"] = "ABERTURA_PODE_DECIDIR (poder >= 5); o desfecho depende do valor central, ainda nao lido"
    return out


def publicar_estagio_cego(dado, caminho):
    """Criacao EXCLUSIVA (nunca sobrescreve); devolve o sha256 do arquivo (para registrar no Mapa ANTES da abertura)."""
    raw = (json.dumps(dado, indent=2, allow_nan=False, ensure_ascii=False, sort_keys=True) + "\n").encode()
    p = Path(caminho)
    with open(p, "xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    return hashlib.sha256(raw).hexdigest()
