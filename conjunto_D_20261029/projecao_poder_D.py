# -*- coding: utf-8 -*-
# Projecao de PLANEJAMENTO do poder do conjunto D (sem NENHUM dado de deformacao):
#   entradas: SNR_rede GWOSC e delta_pred_exato por evento (ambos ja no V1 congelado, "informacao cega"),
#             ajuste sigma_tau(SNR) da bancada (E0_SNR_INFORMATION_FIT.json, GWTC5_31, NAO-CEGO, planejamento),
#             sigma_sys DECLARADO do V1 (0.029 e 0.038).
# Estatuto: [DERIVED] sobre entradas [DECLARADO]; nao e poder medido; sigma_i reais nascem na PE.
import json, math, hashlib, time

W = "C:/IALD/Central de Patentes/work/conjunto_D_20261029"
V1 = "C:/IALD/Bancada_Um/investigacao/preregistro_ramo_b_05out/PREREGISTRO_RAMO_B_RINGDOWN_V1.json"
FIT = "C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/bis/E0_SNR_INFORMATION_FIT.json"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


v1 = json.load(open(V1, encoding="utf-8"))
fit = json.load(open(FIT, encoding="utf-8"))
f31 = [f for f in fit["fits"] if f["population"] == "GWTC5_31"][0]
b0, b1 = f31["coefficients_log_intercept_slope"]
s_ln = f31["residual_sigma_ln_ddof_N"]
rows = {r["evento"]: r for r in v1["spec"]["conjuntos"]["D"]["previsao_da_hipotese_por_evento_INFORMACAO_CEGA"]}
D10 = [e for e, r in rows.items() if not r["data_quality_hold"]]
D14 = list(rows.keys())
assert len(D10) == 10 and len(D14) == 14


def sigma_med(snr):
    return math.exp(b0 + b1 * math.log(snr))


def proj(evs, sig_sys, info_mode):
    w = []
    d = []
    for e in evs:
        r = rows[e]
        sm = sigma_med(r["SNR_rede_GWOSC"])
        # informacao esperada E[1/sigma^2] = exp(-2mu + 2 s^2) / ... ; modo 'med' usa 1/mediana^2
        if info_mode == "esperada":
            info = (1.0 / sm ** 2) * math.exp(2 * s_ln ** 2)
            wi = 1.0 / (1.0 / info + sig_sys ** 2)
        else:
            wi = 1.0 / (sm ** 2 + sig_sys ** 2)
        w.append(wi)
        d.append(r["delta_pred_exato"])
    sw = sum(w)
    dbar = sum(wi * di for wi, di in zip(w, d)) / sw
    scomb = 1.0 / math.sqrt(sw)
    wmax = max(w) / sw
    return dict(n=len(evs), delta_pred_ponderado=dbar, sigma_comb=scomb, poder=abs(dbar) / scomb, fracao_max_informacao=wmax)


out = dict(gerado=time.strftime("%Y-%m-%dT%H:%M:%S%z"), script_sha256=sha(__file__), v1_sha256=sha(V1), fit_sha256=sha(FIT),
           coef_ln_sigma=[b0, b1], s_ln_ddof_N=s_ln,
           aviso="PLANEJAMENTO [DERIVED]. Usa sigma_tau(SNR) ajustado em 31 eventos pSEOBNRv5PHM publicados (NOT_BLIND) e SNR de REDE (nao SNR de ringdown); "
                 "nao inclui jackknife (sigma_usado = max(sigma_comb, sigma_jack) so pode piorar), nem a diferenca de familia v4HM-PA x v5PHM. "
                 "Nenhum valor central de deformacao e lido ou impresso.",
           por_evento={e: dict(SNR=rows[e]["SNR_rede_GWOSC"], sigma_mediana_proj=sigma_med(rows[e]["SNR_rede_GWOSC"]), delta_pred=rows[e]["delta_pred_exato"]) for e in D14},
           projecao={})
for nome, evs in [("D10_sem_hold", D10), ("D14_com_holds", D14)]:
    for ss in (0.0, 0.029, 0.038):
        for mode in ("mediana", "esperada"):
            out["projecao"]["%s__sigma_sys_%.3f__info_%s" % (nome, ss, mode)] = proj(evs, ss, mode)
# necessidade: sigma_comb maximo para poder>=5
d10 = out["projecao"]["D10_sem_hold__sigma_sys_0.000__info_mediana"]["delta_pred_ponderado"]
out["sigma_comb_maximo_para_poder_5_D10"] = abs(d10) / 5.0
out["fator_de_informacao_necessario_D10"] = (out["projecao"]["D10_sem_hold__sigma_sys_0.000__info_mediana"]["sigma_comb"] / (abs(d10) / 5.0)) ** 2
json.dump(out, open(W + "/PROJECAO_PODER_D_planejamento.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for k, v in out["projecao"].items():
    print("%-52s n=%2d delta_pred=%+.4f sigma_comb=%.4f poder=%.2f maxinfo=%.3f" % (k, v["n"], v["delta_pred_ponderado"], v["sigma_comb"], v["poder"], v["fracao_max_informacao"]))
print("sigma_comb maximo p/ poder>=5 (D10):", out["sigma_comb_maximo_para_poder_5_D10"], "fator de informacao necessario:", out["fator_de_informacao_necessario_D10"])
print("sigma_i proj:", {e: round(v["sigma_mediana_proj"], 3) for e, v in out["por_evento"].items() if e in D10})
