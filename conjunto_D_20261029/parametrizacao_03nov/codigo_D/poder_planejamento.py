# -*- coding: utf-8 -*-
"""poder_planejamento.py -- RASCUNHO do PODER_RAMO_B_ANTES_DE_ABRIR para o conjunto D, SEM NENHUM DADO de deformacao ou de strain.
Entradas (todas ja fixadas/lidas por hash): SNR de rede e delta_pred por evento (tabela 'informacao cega' do V1), ajuste sigma_tau(SNR) da bancada nos 31 eventos
do GWTC-5.0 (E0_SNR_INFORMATION_FIT.json; NOT_BLIND; so planejamento), sigma_sys da familia declarada do V1 (0,029 e 0,038), as constantes da Fase 6.
Reproduz o numero do plano de 29/10 (D10: 3,73-3,93 sigma; D14: 4,39-4,64) e ACRESCENTA o que o plano deixou como [OPEN]: o efeito da incerteza do vies c(sigma)
medido pelas injecoes C2 (J por classe) sobre o poder.  Estatuto: [DERIVED] sobre entradas [DECLARADO]; nao e poder medido; as sigma_i reais nascem na PE.
"""
import hashlib
import json
import math
import time
from pathlib import Path

import numpy as np

import estimador_ramo_b_v1 as E
import v1_ramo_b as V

FIT = "C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E0_SNR_INFORMATION_FIT.json"
SIGMA_SYS = (0.0,) + E.SIGMA_SYS_FAMILIA


def _sigma_med(b0, b1, snr):
    return math.exp(b0 + b1 * math.log(snr))


def _w(sig, ss, modo, s_ln):
    if modo == "esperada":
        info = (1.0 / sig ** 2) * math.exp(2 * s_ln ** 2)
        return 1.0 / (1.0 / info + ss ** 2)
    return 1.0 / (sig ** 2 + ss ** 2)


def _escolha_c2(sigmas_por_evento, ordem_snr, m):
    idx = sorted({round(i * (len(ordem_snr) - 1) / (m - 1)) for i in range(m)}) if m > 1 else [0]
    return [ordem_snr[i] for i in idx]


def sigma_do_vies(sig_eventos, w, eventos_ordem_snr, J_classe):
    """sigma do vies c(sigma_i) propagado na media ponderada (g' Cov g), para J_classe injecoes por classe, cada uma com espalhamento = sigma do seu evento;
    ajuste linear c0 + k_c*sigma (como o V1)."""
    base = _escolha_c2(sig_eventos, eventos_ordem_snr, 5 if J_classe <= 5 else 10)
    pts = []
    for j in range(J_classe):
        ev = base[j % len(base)]
        pts.append({"sigma": sig_eventos[ev], "vies": 0.0, "sigma_vies": sig_eventos[ev]})
    fit = E.ajustar_vies(pts)
    s = np.array([sig_eventos[e] for e in eventos_ordem_snr])
    g = np.array([1.0, float((w * s).sum() / w.sum())])
    return math.sqrt(float(g @ np.asarray(fit["cov"]) @ g)), fit["modo"]


def gerar():
    v1, info = V.carregar_v1()
    rows = V.tabela_eventos(v1)
    d10 = V.eventos_d10(v1)
    d14 = list(rows.keys())
    fit = json.loads(Path(V.native(FIT)).read_text(encoding="utf-8"))
    f31 = [f for f in fit["fits"] if f["population"] == "GWTC5_31"][0]
    b0, b1 = f31["coefficients_log_intercept_slope"]
    s_ln = f31["residual_sigma_ln_ddof_N"]
    CR = V.criterios_fase6()
    k = V.constantes_um_py()

    def projetar(evs, ss, modo):
        sig = {e: _sigma_med(b0, b1, rows[e]["SNR_rede_GWOSC"]) for e in evs}
        w = np.array([_w(sig[e], ss, modo, s_ln) for e in evs])
        dp = np.array([rows[e]["delta_pred_exato"] for e in evs])
        dbar = float((w * dp).sum() / w.sum())
        sc = float(1 / math.sqrt(w.sum()))
        return sig, w, dbar, sc

    out = {"estagio": "RASCUNHO_DE_PLANEJAMENTO__SEM_DADO__NAO_E_O_ESTAGIO_CEGO",
           "gerado": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
           "aviso": "PLANEJAMENTO [DERIVED]. sigma_tau(SNR) ajustado em 31 eventos pSEOBNRv5PHM publicados (NOT_BLIND), com SNR de REDE (nao de ringdown); sem jackknife "
                    "(so pode piorar), sem a diferenca de familia v4HM-PA x v5PHM. Nenhum valor central de deformacao e lido ou impresso. O estagio cego REAL usa as sigma_i da PE "
                    "e se grava em PODER_RAMO_B_ANTES_DE_ABRIR_REAL.json.",
           "entradas": {"V1_json_sha256": info["PREREGISTRO_RAMO_B_RINGDOWN_V1.json"], "fit_sigma_SNR_sha256": V.sha256_file(FIT),
                        "coef_ln_sigma": [b0, b1], "residuo_ln_ddof_N": s_ln, "criterios_fase6": {x: CR[x] for x in ("min_eventos", "z_excl", "poder_min", "sistematica_max_relativa")},
                        "beta_runtime": k["beta"]},
           "por_evento_D10": {e: {"SNR_rede": rows[e]["SNR_rede_GWOSC"], "sigma_mediana_projetada": _sigma_med(b0, b1, rows[e]["SNR_rede_GWOSC"]),
                                  "delta_pred": rows[e]["delta_pred_exato"], "chi_f": rows[e]["chi_f_mediana_GR"]} for e in d10},
           "poder_sem_incerteza_do_vies": {}, "poder_com_incerteza_do_vies_D10": {}}
    for nome, evs in (("D10_sem_hold", d10), ("D14_com_holds", d14)):
        for ss in SIGMA_SYS:
            for modo in ("mediana", "esperada"):
                sig, w, dbar, sc = projetar(evs, ss, modo)
                out["poder_sem_incerteza_do_vies"]["%s__sigma_sys_%.3f__info_%s" % (nome, ss, modo)] = {
                    "n": len(evs), "delta_pred_ponderado": dbar, "sigma_comb": sc, "poder": abs(dbar) / sc,
                    "fracao_maxima_de_informacao": float(w.max() / w.sum()), "sist_rel": (ss / abs(dbar))}
    # com incerteza do vies (D10; sigma_sys 0,038; info mediana)
    ordem = sorted(d10, key=lambda e: rows[e]["SNR_rede_GWOSC"])
    for ss in E.SIGMA_SYS_FAMILIA:
        for modo in ("mediana", "esperada"):
            sig, w, dbar, sc = projetar(d10, ss, modo)
            ws = np.array([_w(sig[e], ss, modo, s_ln) for e in d10])
            sig_ord = {e: sig[e] for e in d10}
            bloco = {"sem_vies": {"sigma_tot": sc, "poder": abs(dbar) / sc}}
            for J, rot in ((5, "C2_minima_10PE_J5_por_classe"), (10, "C2_media_20PE_J10_por_classe"), (25, "C2_ampla_50PE_J25_por_classe"), (10 ** 6, "C2_infinita_limite")):
                if J > 100:
                    sv = 0.0
                    modo_fit = "limite"
                else:
                    # as injecoes de uma classe cobrem os eventos escolhidos: o ajuste linear c0 + kc*sigma
                    sv, modo_fit = sigma_do_vies(sig_ord, ws, ordem, J)
                st = math.sqrt(sc ** 2 + sv ** 2)
                bloco[rot] = {"sigma_vies": sv, "sigma_tot": st, "poder": abs(dbar) / st, "ajuste": modo_fit,
                              "informacao_extra_necessaria_para_poder_5": (st / (abs(dbar) / 5)) ** 2}
            out["poder_com_incerteza_do_vies_D10"]["sigma_sys_%.3f__info_%s" % (ss, modo)] = bloco
    d10_ref = out["poder_sem_incerteza_do_vies"]["D10_sem_hold__sigma_sys_0.000__info_mediana"]
    out["sigma_comb_maximo_para_poder_5_D10"] = abs(d10_ref["delta_pred_ponderado"]) / 5.0
    out["fator_de_informacao_necessario_D10_sem_vies"] = (d10_ref["sigma_comb"] / (abs(d10_ref["delta_pred_ponderado"]) / 5.0)) ** 2
    out["leitura"] = ("Com os 10 eventos de D o poder de planejamento e < 5 sigma em todas as leituras; pela ordem do V1 (regra 3 antes da 5) o veredito, se os controles passarem, "
                      "e NOT_FALSIFIED_UNDERPOWERED qualquer que seja o valor central. Com o vies do instrumento medido por poucas injecoes C2, o poder cai ainda mais.")
    raw = (json.dumps(out, indent=2, allow_nan=False, ensure_ascii=False, sort_keys=True) + "\n").encode()
    return out, raw


if __name__ == "__main__":
    import sys
    out, raw = gerar()
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if dest:
        with open(dest, "xb") as f:
            f.write(raw)
        print("gravado", dest, hashlib.sha256(raw).hexdigest())
    p = out["poder_sem_incerteza_do_vies"]
    for kk, v in p.items():
        print("%-52s poder=%.2f sigma_comb=%.4f" % (kk, v["poder"], v["sigma_comb"]))
    for kk, b in out["poder_com_incerteza_do_vies_D10"].items():
        print(kk, {r: round(x["poder"], 2) for r, x in b.items()})
