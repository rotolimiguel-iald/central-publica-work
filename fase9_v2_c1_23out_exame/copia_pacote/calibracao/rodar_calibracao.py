# -*- coding: utf-8 -*-
"""rodar_calibracao.py -- CALIBRACAO DE CAUDA por simulacao sob as nulas + PODER ESPERADO da V2-c1 (so incertezas; nenhum centro observado).
Gera: calibracao/CALIBRACAO_CAUDA_RECIBO.json, calibracao/MC_VALIDACAO.json, poder/PODER_ESPERADO_V2C1.json e .md.
Rodar:  python -P -E -X utf8 calibracao/rodar_calibracao.py [--n-por-cenario 100000] [--workers 40]"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import math
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "testes"))
sys.path.insert(0, os.path.join(ROOT, "runner"))
import numpy as np  # noqa: E402
from scipy import stats as sps  # noqa: E402

import f9v2_calibration as CAL  # noqa: E402
import f9v2_stats as ST  # noqa: E402
import simlib as SL  # noqa: E402

MODES = ("bruto", "proprio", "sup_caixa")
CORNERS = {"indep(0,0)": (0.0, 0.0), "max_sigma(1,0.25)": (1.0, 0.25), "pior_caixa(1,1)": (1.0, 1.0)}
CHUNK = 5000


def sha(b):
    return hashlib.sha256(b).hexdigest()


def worker(args):
    null, corner, n, seed = args
    c = SL.ctx()
    rng = np.random.default_rng(seed)
    lam = CORNERS[corner]
    C_true = SL.covariance_at(c, *lam)
    Y = SL.draw_y(c, null, C_true, rng, n)
    zd = np.full(n, np.nan)
    zq = np.zeros(n)
    counts = {m: {k: 0 for k in SL.CLASS_NAMES + ["OUTRO"]} for m in MODES}
    counts["_dispersao"] = {"chi2_gt2_min": 0, "chi2_gt2_max": 0, "p_lt_001_min": 0, "p_lt_001_max": 0, "qualquer_regra": 0, "so_p_lt_001": 0}
    for j in range(n):
        y = Y[j]
        st_min = ST.endpoint_statistics(y, c["ids"], c["ep"]["minimum"]["covariance"], c["law"], c["bgfree"], fast=True)
        st_max = ST.endpoint_statistics(y, c["ids"], c["ep"]["maximum"]["covariance"], c["law"], c["bgfree"], fast=True)
        dm, dM = st_min["dispersao"], st_max["dispersao"]
        cd = counts["_dispersao"]
        cd["chi2_gt2_min"] += dm["chi2_por_gl"] > 2
        cd["chi2_gt2_max"] += dM["chi2_por_gl"] > 2
        cd["p_lt_001_min"] += dm["p"] < 0.01
        cd["p_lt_001_max"] += dM["p"] < 0.01
        cd["qualquer_regra"] += (dm["chi2_por_gl"] > 2) or (dM["chi2_por_gl"] > 2) or (dm["p"] < 0.01) or (dM["p"] < 0.01)
        cd["so_p_lt_001"] += (dm["p"] < 0.01) or (dM["p"] < 0.01)
        zd[j] = np.nan if st_min["z_delta"] is None else st_min["z_delta"]
        zq[j] = st_max["z_disc"]
        for m in MODES:
            tok = SL.assemble_and_verdict(c, y, m, st_min, st_max)[0]
            counts[m][SL.classify(tok)] += 1
    return null, corner, zd, zq, counts


def tail_table(zd, zq, c, mode_tau):
    ts_d = [1.0, 2.0, 3.0, 3.5, 4.0, 4.5]
    ts_q = [-3.0, 0.0, 1.0, 2.0, 3.0]
    ok = np.isfinite(zd)
    out = {"n": int(len(zd)), "z_delta_indefinido_frac": float(1 - ok.mean()), "z_delta": {}, "z_disc": {}}
    for t in ts_d:
        k = int(np.sum(np.abs(zd[ok]) >= t))
        out["z_delta"][str(t)] = {"mc_frac": k / len(zd), "mc_k": k}
    for t in ts_q:
        k = int(np.sum(zq >= t))
        out["z_disc"][str(t)] = {"mc_frac": k / len(zq), "mc_k": k}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-por-cenario", type=int, default=100000)
    ap.add_argument("--workers", type=int, default=40)
    a = ap.parse_args()
    t0 = time.time()
    c = SL.ctx()
    spec, law, ep, tau = c["spec"], c["law"], c["ep"], c["tau"]
    mode_spec = spec["calibracao_de_cauda"]["modo"]
    # ---- analitico
    zmap, zdm = c["zmap"], c["zdm"]
    analytic = {"tau": tau, "z_delta_p_cal": {}, "z_disc_p_cal": {}}
    for t in (1, 2, 3, 4, 5, 6, 7):
        analytic["z_delta_p_cal"][str(t)] = {
            "gauss_bilateral": float(2 * sps.norm.sf(t)),
            "proprio": zmap.p_two_sided(t, tau["tau_f_proprio"])[0], "z_cal_proprio": zmap.z_cal(t, tau["tau_f_proprio"]),
            "sup_caixa": zmap.p_two_sided(t, tau["tau_f_sup"])[0], "z_cal_sup_caixa": zmap.z_cal(t, tau["tau_f_sup"])}
        analytic["z_disc_p_cal"][str(t)] = {
            "gauss_unilateral": float(sps.norm.sf(t)),
            "proprio": zdm.p_one_sided(t, tau["tau_d_proprio"]), "z_cal_proprio": zdm.z_cal(t, tau["tau_d_proprio"]),
            "sup_caixa": zdm.p_one_sided(t, tau["tau_d_sup"]), "z_cal_sup_caixa": zdm.z_cal(t, tau["tau_d_sup"])}
    thr = {m: CAL.threshold_equivalents(zmap, zdm, tau["tau_f_sup" if m == "sup_caixa" else "tau_f_proprio"], tau["tau_d_sup" if m == "sup_caixa" else "tau_d_proprio"])
           for m in ("proprio", "sup_caixa")}
    print("analitico pronto", round(time.time() - t0, 1), "s", flush=True)
    # ---- simulacao sob as nulas (full pipeline) -- tarefas em paralelo
    tasks = []
    seed = 20261023
    for null in ("TGL", "LCDM"):
        for corner in CORNERS:
            for k in range(a.n_por_cenario // CHUNK):
                seed += 1
                tasks.append((null, corner, CHUNK, seed))
    agg = {}
    with cf.ProcessPoolExecutor(max_workers=a.workers) as ex:
        for null, corner, zd, zq, counts in ex.map(worker, tasks):
            e = agg.setdefault((null, corner), {"zd": [], "zq": [], "counts": {m: {} for m in MODES}, "disp": {}})
            for k, v in counts["_dispersao"].items():
                e["disp"][k] = e["disp"].get(k, 0) + int(v)
            e["zd"].append(zd)
            e["zq"].append(zq)
            for m in MODES:
                for k, v in counts[m].items():
                    e["counts"][m][k] = e["counts"][m].get(k, 0) + v
    print("simulacao pronta", round(time.time() - t0, 1), "s", flush=True)
    mc = {}
    classes = {}
    disp_rates = {}
    for (null, corner), e in sorted(agg.items()):
        zd = np.concatenate(e["zd"])
        zq = np.concatenate(e["zq"])
        tt = tail_table(zd, zq, c, None)
        # taxas calibradas por LUT (vetorizado)
        for mode, tk in (("proprio", tau["tau_f_proprio"]), ("sup_caixa", tau["tau_f_sup"])):
            raw, cal = c["lut"][mode]
            ok = np.isfinite(zd)
            zc = np.sign(zd[ok]) * np.interp(np.abs(zd[ok]), raw, cal)
            tt["z_delta_calibrado_" + mode] = {str(t): float(np.mean(np.abs(zc) >= t)) for t in (1.0, 2.0, 3.0, 3.5, 4.0)}
        key = "%s_verdadeira__C_verdadeira=%s" % (null, corner)
        mc[key] = tt
        n = len(zd)
        classes[key] = {m: {k: v / n for k, v in e["counts"][m].items() if v} for m in MODES}
        disp_rates[key] = {k: v / n for k, v in e["disp"].items()}
    # comparar MC x analitico nos limiares simulaveis
    cmp = {}
    for corner in CORNERS:
        key = "TGL_verdadeira__C_verdadeira=%s" % corner
        cmp[key] = {}
        # tau verdadeiro desse canto: Var(w_min' C_true w_min) + V_T
        w = ep["minimum"]["weights"]
        Ct = SL.covariance_at(c, *CORNERS[corner])
        tau_t = math.sqrt(float(w @ Ct @ w) + tau["V_T"])
        for t in (1.0, 2.0, 3.0, 3.5, 4.0, 4.5):
            pa = zmap.p_two_sided(t, tau_t)[0]
            cmp[key][str(t)] = {"analitico": pa, "mc": mc[key]["z_delta"][str(t)]["mc_frac"], "mc_k": mc[key]["z_delta"][str(t)]["mc_k"]}
        key2 = "LCDM_verdadeira__C_verdadeira=%s" % corner
        cmp[key2] = {}
        w2 = ep["maximum"]["weights"]
        tau_t2 = math.sqrt(float(w2 @ Ct @ w2) + tau["V_L"])
        for t in (0.0, 1.0, 2.0, 3.0):
            pa = zdm.p_one_sided(t, tau_t2)
            cmp[key2][str(t)] = {"analitico": pa, "mc": mc[key2]["z_disc"][str(t)]["mc_frac"], "mc_k": mc[key2]["z_disc"][str(t)]["mc_k"]}
    # reducao exata: pipeline completo x mapa (m)
    rng = np.random.default_rng(7)
    red = []
    for _ in range(400):
        y = SL.draw_y(c, "TGL", SL.covariance_at(c, 0.0, 0.0), rng, 1)[0]
        st = ST.endpoint_statistics(y, c["ids"], ep["minimum"]["covariance"], law, c["bgfree"], fast=True)
        m = float(ep["minimum"]["weights"] @ y)
        zr = CAL.zdelta_of_m(m, ep["minimum"]["sigma_comb"], law)
        stm = ST.endpoint_statistics(y, c["ids"], ep["maximum"]["covariance"], law, c["bgfree"], fast=True)
        xm = float(ep["maximum"]["weights"] @ y) - law.mu
        red.append([abs(st["z_delta"] - zr) if (zr is not None and st["z_delta"] is not None) else 0.0, abs(stm["z_disc"] - zdm.z_raw(xm))])
    red = np.array(red)
    # ---- poder so com sigma (pinado) e fundo
    pw = {}
    for fam in spec["familias"]:
        ids = spec["familias"][fam]["ids"]
        e2 = ST.grid_endpoints(c["amps"], c["sig"], ids, c["grid"]["lambda_N"], c["grid"]["lambda_T"])
        pw[fam] = {s: {"sigma_comb": e2[s]["sigma_comb"], "D_BG1_S5_fundo_de_qualificacao": ST.power_sigma_only(law.K, law.mu, e2[s]["sigma_comb"], law.V(law.beta)),
                       **{"D_" + b + "_formula_pinada": ST.power_sigma_only(law.K, spec["fundos"][b]["H0"], e2[s]["sigma_comb"], (law.K * spec["fundos"][b]["sigma"]) ** 2) for b in ("BG1", "BG2", "BG3")}}
                   for s in ("minimum", "maximum")}
    # ---- gravacao
    qraw = open(SL.QUAL_PATH, "rb").read()
    mod_hash = {f: sha(open(os.path.join(ROOT, "runner", f), "rb").read())[:16] for f in sorted(os.listdir(os.path.join(ROOT, "runner"))) if f.endswith(".py")}
    receipt = {
        "schema": "F9V2C1_CALIBRACAO_CAUDA_RECIBO_V1", "quando": time.strftime("%Y-%m-%d %H:%M:%S"), "modo_do_spec": mode_spec,
        "entradas": {"spec_canonico_sha256": json.load(open(SL.SPEC_PATH, encoding="utf-8"))["spec_sha256"], "qualificacao_fundo_sha256": sha(qraw),
                     "modulos_do_runner_sha16": mod_hash, "simulacao": {"n_por_cenario": a.n_por_cenario, "cantos": CORNERS, "workers": a.workers}},
        "taus": tau,
        "limiares_equivalentes_P_primaria_BG1": thr[mode_spec] if mode_spec in thr else {},
        "limiares_equivalentes_todos_os_modos": thr,
        "leitura": ("limiar BRUTO que corresponde a um p gaussiano de 3 e 5 sigma. 'proprio' = covariancia do ponto de analise; 'sup_caixa' = pior covariancia da caixa. "
                    "A regra bruta |z_delta| >= 5 corresponde a z calibrado %.2f (sup_caixa) / %.2f (proprio)." % (
                        analytic["z_delta_p_cal"]["5"]["z_cal_sup_caixa"], analytic["z_delta_p_cal"]["5"]["z_cal_proprio"])),
        "analitico": analytic, "reducao_exata_pipeline_completo_x_mapa": {"n": int(len(red)), "max_abs_diff_z_delta": float(red[:, 0].max()), "max_abs_diff_z_disc": float(red[:, 1].max())},
    }
    rb = json.dumps(receipt, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
    open(os.path.join(ROOT, "calibracao", "CALIBRACAO_CAUDA_RECIBO.json"), "wb").write(rb)
    mcj = {"mc_x_analitico": cmp, "mc_tabelas": mc}
    open(os.path.join(ROOT, "calibracao", "MC_VALIDACAO.json"), "wb").write(json.dumps(mcj, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8"))
    pj = {"nota": "PODER ESPERADO pelas incertezas; nenhum centro observado; fundo de qualificacao (Planck comprimido + DESI DR2). Probabilidades por simulacao sob a nula indicada, pipeline completo e funcao pinada.",
          "D_so_sigma": pw, "D_pinado_no_spec": spec["poder_previo"]["primary_five"], "p_calibrado_analitico": analytic,
          "probabilidade_da_classe_do_veredito": classes, "taxa_de_INCONCLUSIVE_pela_dispersao_sob_a_nula": disp_rates, "modos": {"bruto": "a funcao le o escore bruto (equivale a R5.2)", "proprio": "z de p calibrado, covariancia do ponto", "sup_caixa": "z de p calibrado, pior covariancia da caixa (padrao do spec)"},
          "n_por_cenario": a.n_por_cenario}
    open(os.path.join(ROOT, "poder", "PODER_ESPERADO_V2C1.json"), "wb").write(json.dumps(pj, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8"))
    print("tempo", round(time.time() - t0, 1), "s | receipt", sha(rb)[:16])
    print(json.dumps(receipt["limiares_equivalentes_todos_os_modos"], indent=1))
    print("reducao", receipt["reducao_exata_pipeline_completo_x_mapa"])


if __name__ == "__main__":
    main()
