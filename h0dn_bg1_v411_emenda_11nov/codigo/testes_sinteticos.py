# -*- coding: utf-8 -*-
"""Testes T1-T8 da emenda v411, SO' com vetores SINTETICOS gerados aqui com semente fixa. Nenhum dado observado e' aberto.
Saida: artefatos/TESTES_SINTETICOS.json (cada teste: ok + numeros). Teste que falha NAO e' ajustado: e' reportado."""
import ast
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import traceback
import types
from pathlib import Path

import numpy as np
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import abertura_v411 as ab                     # noqa: E402
from estimator_v411 import evaluate as evaluate_v411  # noqa: E402
from veredito_v411 import veredito_h0dn_v411   # noqa: E402

OUT = HERE.parent / "artefatos"
B = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
NETWORK, FROZEN, BG1 = B / "network" / "network.npz", B / "estimator_frozen.npz", B / "background" / "BG1.json"
README = B / "network" / "upstream" / "h0_constrainer" / "README.md"
S0NPZ = OUT / "estimador_s0_v411.npz"
SEEDS = {"gerador": 20261111, "T5_ruido": 411001, "T5_fundo": 411002, "T5_nuis": 411003}
N_MC = 20000


def fl(x):
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, np.ndarray):
        return x.tolist()
    return x


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ------------------------------------------------------------------ insumos de DESENHO
rede = ab.carregar_rede(NETWORK)
congelado = ab.carregar_congelado(FROZEN)
s0 = ab.carregar_s0(S0NPZ)
bg = ab.carregar_bg(BG1)
A, C, h = rede["A"], rede["C"], rede["h_index"]
H0_bg = float(bg["H0"])
keep = np.asarray(s0["keep"], int)
N255 = congelado["null_basis"]
est255 = {k: congelado[k] for k in ("weights", "null_basis", "gradient_h", "gradient_k", "sd_null", "sd_tgl", "logK", "H0")}
est0 = ab._pack_estimator(s0)
vals_C, U_C = np.linalg.eigh((C + C.T) / 2)
kp = vals_C > 1e-10
assert int(kp.sum()) == 183
SQ = U_C[:, kp] * np.sqrt(vals_C[kp])[None, :]       # 255 x 183: eps = SQ @ z


def x_ref_255():
    x = np.zeros(A.shape[1]); x[h] = np.log10(H0_bg)
    return x


def gerar_x(h_true, seed):
    rng = np.random.default_rng(seed)
    x = 25.0 + 5.0 * rng.standard_normal(A.shape[1])      # nuisance sintetico fixo (escala de magnitudes)
    x[h] = h_true
    return x


def gerar_y(seed, h_true, null_amp=0.0):
    """y = A x + ruido no suporte (C^{1/2}) + componente no nulo (max|u| = null_amp)."""
    rng = np.random.default_rng(seed)
    x = gerar_x(h_true, seed + 1)
    eps = SQ @ rng.standard_normal(SQ.shape[1])
    y = A @ x + eps
    u = np.zeros(N255.shape[1])
    if null_amp:
        u = rng.standard_normal(N255.shape[1]); u *= null_amp / np.max(np.abs(u))
        y = y + N255 @ u
    return y, x, u


def ramos_teste():
    return {"limiar": 5.0, "compat_95": 1.959963984540054,
            "vereditos": {"inconclusivo": "T_INCONCLUSIVE", "lei_falsificada": "T_FALSIFIED", "subpotente": "T_UNDERPOWERED_%s",
                          "tensao": "T_TENSION_%dSIGMA", "nao_discriminado": "T_NOT_DISCRIMINATED_%s",
                          "faixas": ("T_F0", "T_F1", "T_F2"), "sufixo": "__T_SUF",
                          "leitura_partes": ["T_READ_A_", "%dSIGMA_", "T_READ_C"]}}


RAMOS_PROD = json.loads((OUT / "RAMOS_V410.json").read_text(encoding="utf-8"))


def alvos_do_vetor(y):
    nc = ab.numeros_colaboracao(y, A, C, h)
    return {"H0": nc["H0"], "sig": nc["sig"], "chi2": nc["chi2"], "ndof": nc["ndof"], "fp": ab.impressao_digital(y, N255)}


def rodar_abrir(y, alvos, rede_=None, congelado_=None, s0_=None, bg_=None, ramos_=None):
    return ab.abrir(y, rede if rede_ is None else rede_, congelado if congelado_ is None else congelado_,
                    s0 if s0_ is None else s0_, bg if bg_ is None else bg_, alvos, ramos_teste() if ramos_ is None else ramos_)


H_TRUE_SINT = float(np.log10(H0_bg * 1.07))      # verdade sintetica: 7 % acima do fundo (so' para o gerador)
Y_RAW, X_RAW, U_RAW = gerar_y(SEEDS["gerador"], H_TRUE_SINT, null_amp=0.09)
Y_SEM, _, _ = gerar_y(SEEDS["gerador"], H_TRUE_SINT, null_amp=0.0)
LOC_RAW = Y_RAW - A @ x_ref_255()
LOC_SEM = Y_SEM - A @ x_ref_255()
RESULT = {"seeds": SEEDS, "N_MC": N_MC, "nota": "Todos os vetores sao sinteticos (semente fixa). Nenhum dado observado foi aberto.",
          "insumos_de_desenho": {k: {"sha256": sha_file(p)} for k, p in (("network.npz", NETWORK), ("estimator_frozen.npz", FROZEN),
                                                                         ("BG1.json", BG1), ("estimador_s0_v411.npz", S0NPZ),
                                                                         ("estimator_v411.py", HERE / "estimator_v411.py"),
                                                                         ("veredito_v411.py", HERE / "veredito_v411.py"),
                                                                         ("abertura_v411.py", HERE / "abertura_v411.py"),
                                                                         ("executar_abertura_v411.py", HERE / "executar_abertura_v411.py"),
                                                                         ("extrair_ramos_v410.py", HERE / "extrair_ramos_v410.py"),
                                                                         ("gerar_ramos_v411.py", HERE / "gerar_ramos_v411.py"),
                                                                         ("RAMOS_V410.json", OUT / "RAMOS_V410.json"))}}


def teste(nome, tipo="teste"):
    """tipo: 'teste' (pode falhar) ou 'conferencia_de_consistencia' (verifica coerencia interna; nao pode falhar por construcao)."""
    def deco(f):
        try:
            r = f()
        except Exception as e:  # falha de execucao do teste e' falha visivel
            r = {"ok": False, "erro": "%s: %s" % (type(e).__name__, e), "traceback": traceback.format_exc()}
        r["tipo"] = tipo
        RESULT[nome] = r
        print(nome, "OK" if r.get("ok") else "FALHA")
        return f
    return deco


# ------------------------------------------------------------------ T1
@teste("T1_t_igual_com_e_sem_componente_nula")
def _():
    nomes = list(s0["model_names"])
    out = {"por_estimador": {}}
    ok = True
    for nome_est, est, loc_a, loc_b in (("rede255", est255, LOC_RAW, LOC_SEM),
                                        ("S0", est0, LOC_RAW[keep], LOC_SEM[keep])):
        ea = evaluate_v411({"local": loc_a[None, :], "background": np.zeros((1, 3))}, est)
        eb = evaluate_v411({"local": loc_b[None, :], "background": np.zeros((1, 3))}, est)
        dif = np.abs(np.asarray(ea["t"]) - np.asarray(eb["t"]))[0]
        o = {"dif_t": dif.tolist(), "t_com_nulo": np.asarray(ea["t"])[0].tolist(), "t_sem_nulo": np.asarray(eb["t"])[0].tolist(),
             "support_l2_com": float(np.asarray(ea["support_l2"])[0]), "support_l2_sem": float(np.asarray(eb["support_l2"])[0]),
             "support_max_abs_com": float(ea["support_max_abs"]), "ok": bool(np.all(dif < 1e-12))}
        ok = ok and o["ok"] and o["support_l2_com"] > 0.05
        out["por_estimador"][nome_est] = o
    # S0 e rede255 compartilham o mesmo nulo (projetores iguais)
    N0 = s0["null_basis"]; Nk = N255[keep]
    out["dif_projetor_nulo_S0_vs_recorte255"] = float(np.max(np.abs(N0 @ N0.T - Nk @ Nk.T)))
    out["modelos"] = nomes
    out["max_abs_u"] = float(np.max(np.abs(U_RAW)))
    out["fp_do_vetor_com_nulo"] = ab.impressao_digital(Y_RAW, N255)
    out["ok"] = bool(ok and out["dif_projetor_nulo_S0_vs_recorte255"] < 1e-10)
    return out


# ------------------------------------------------------------------ T2
@teste("T2_guarda_congelada_recusa_v411_aceita")
def _():
    spec = importlib.util.spec_from_file_location("estimator_congelado", B / "estimator.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    out = {}
    ok = True
    for nome_est, est, loc_a, loc_b in (("rede255", est255, LOC_RAW, LOC_SEM), ("S0", est0, LOC_RAW[keep], LOC_SEM[keep])):
        d_a = {"local": loc_a[None, :], "background": np.zeros((1, 3))}; d_b = {"local": loc_b[None, :], "background": np.zeros((1, 3))}
        try:
            mod.evaluate(d_a, est); rec = None
        except ValueError as e:
            rec = str(e)
        try:
            mod.evaluate(d_b, est); aceita_sem = True
        except ValueError as e:
            aceita_sem = False
        try:
            evaluate_v411(d_a, est); v_a = True
        except Exception:
            v_a = False
        try:
            evaluate_v411(d_b, est); v_b = True
        except Exception:
            v_b = False
        o = {"congelado_recusa_com_nulo": rec, "congelado_aceita_sem_nulo": aceita_sem, "v411_aceita_com_nulo": v_a, "v411_aceita_sem_nulo": v_b}
        o["ok"] = bool(rec == "data_outside_support" and aceita_sem and v_a and v_b)
        ok = ok and o["ok"]
        out[nome_est] = o
    out["ok"] = ok
    return out


# ------------------------------------------------------------------ T3
@teste("T3_cilada_da_centragem")
def _():
    alvos = alvos_do_vetor(Y_RAW)
    base = rodar_abrir(Y_RAW, alvos)
    nc = ab.numeros_colaboracao(Y_RAW, A, C, h)
    x_pub = np.zeros(A.shape[1]); x_pub[h] = nc["logh"]
    variantes = {"y_menos_A_xpub (x_pub so' em h)": Y_RAW - A @ x_pub,
                 "y_menos_A_xhat (todos os parametros ajustados)": Y_RAW - A @ nc["params"],
                 "y_menos_A_xref (local do fundo)": Y_RAW - A @ x_ref_255()}
    out = {"controle_vetor_cru_passa": bool(base["portao_1_ok"]), "variantes": {}}
    ok = bool(base["portao_1_ok"]) and base["estatistica"] is not None
    for nome, yc in variantes.items():
        r = rodar_abrir(yc, alvos)
        b1 = r["portao_1"]["1b"]
        o = {"1b_ok": b1["ok"], "H0_reproduzido": b1["H0"], "alvo_H0": alvos["H0"], "motivos": r["portao_1"]["motivos"],
             "ramo": r["veredito"]["ramo"], "outcome": r["veredito"]["outcome"],
             "estatistica_None": r["estatistica"] is None, "estresse_None": r["estresse"] is None, "coerencia_None": r["coerencia"] is None,
             "1c_avaliado(esperado False: so' se avalia com 1b.reproduz)": r["portao_1"]["1c"] is not None,
             "pesos_consistentes_avaliado(esperado False)": b1["pesos_consistentes"] is not None}
        o["ok"] = bool((not b1["ok"]) and "falhou_1b" in o["motivos"] and o["ramo"] == 1 and o["estatistica_None"] and o["estresse_None"]
                       and o["coerencia_None"] and not o["1c_avaliado(esperado False: so' se avalia com 1b.reproduz)"]
                       and not o["pesos_consistentes_avaliado(esperado False)"])
        ok = ok and o["ok"]
        out["variantes"][nome] = o
    out["ok"] = ok
    return out


# ------------------------------------------------------------------ T4
@teste("T4_portao_com_alvos_do_proprio_vetor_e_perturbacoes")
def _():
    alvos = alvos_do_vetor(Y_RAW)
    out = {"alvos_do_vetor": {k: fl(v) for k, v in alvos.items()}}
    # conferencia independente por whitener da rede (nao usa a pinv)
    with np.load(NETWORK, allow_pickle=False) as d:
        Wh = d["whitener"].copy()
    Aw, yw = Wh @ A, Wh @ Y_RAW
    xw, *_r = np.linalg.lstsq(Aw, yw, rcond=None)
    chi2_w = float(np.sum((yw - Aw @ xw) ** 2))
    out["independente_whitener"] = {"dif_H0": float(abs(10 ** xw[h] - alvos["H0"])), "dif_chi2": float(abs(chi2_w - alvos["chi2"]))}
    ind_ok = out["independente_whitener"]["dif_H0"] < 1e-9 and out["independente_whitener"]["dif_chi2"] < 1e-8
    r = rodar_abrir(Y_RAW, alvos)
    out["passa_com_alvos_proprios"] = bool(r["portao_1_ok"])
    out["margens_dos_difs"] = {"1b_dif_H0": r["portao_1"]["1b"]["dif_H0"], "1b_dif_sig": r["portao_1"]["1b"]["dif_sig"],
                               "1b_dif_chi2": r["portao_1"]["1b"]["dif_chi2"],
                               "1b_dif_pesos_congelados_logh(tol 1e-10)": r["portao_1"]["1b"]["dif_pesos_congelados_logh"],
                               "1c_dif(tol 1e-10)": r["portao_1"]["1c"]["dif"], "1d_dif(tol 1e-9)": r["portao_1"]["1d"]["dif"],
                               "max_abs_y": float(np.max(np.abs(Y_RAW)))}
    pert = {}
    ok_p = True
    for nome, chave, delta, gate in (("H0+1e-3", "H0", 1e-3, "falhou_1b"), ("sig+1e-3", "sig", 1e-3, "falhou_1b"),
                                     ("chi2+1e-3", "chi2", 1e-3, "falhou_1b"), ("fp+1e-3", "fp", 1e-3, "falhou_1d"),
                                     ("ndof+1", "ndof", 1, "falhou_1b")):
        al = dict(alvos); al[chave] = al[chave] + delta
        rr = rodar_abrir(Y_RAW, al)
        o = {"portao_1_ok": rr["portao_1_ok"], "motivos": rr["portao_1"]["motivos"], "ramo": rr["veredito"]["ramo"]}
        o["ok"] = bool((not rr["portao_1_ok"]) and gate in o["motivos"] and o["ramo"] == 1 and rr["estatistica"] is None)
        ok_p = ok_p and o["ok"]
        pert[nome] = o
    out["perturbacoes_uma_de_cada_vez"] = pert
    # bordas da tolerancia (extra): 0,4e-4 passa, 0,6e-4 falha
    borda = {}
    for nome, delta in (("H0+0.4e-4", 0.4e-4), ("H0+0.6e-4", 0.6e-4)):
        al = dict(alvos); al["H0"] += delta
        borda[nome] = bool(rodar_abrir(Y_RAW, al)["portao_1_ok"])
    out["bordas_H0"] = borda
    borda_ok = borda["H0+0.4e-4"] is True and borda["H0+0.6e-4"] is False
    # dimensao errada, nao finito, alvos incompletos
    y_nan = Y_RAW.copy(); y_nan[3] = np.nan
    def msg(f):
        try:
            f(); return None
        except ValueError as e:
            return str(e)
    m_nan = msg(lambda: rodar_abrir(y_nan, alvos)); m_dim = msg(lambda: rodar_abrir(Y_RAW[:-1], alvos))
    m_inc = msg(lambda: rodar_abrir(Y_RAW, {k: v for k, v in alvos.items() if k != "fp"}))
    out["extras"] = {"nan_ValueError": m_nan, "dim_ValueError": m_dim, "alvos_incompletos_ValueError": m_inc,
                     "nota": "desde a rodada de conserto, vetor mal formado e' recusa dura (ValueError), nao ramo (1)"}
    ex_ok = bool(m_nan and m_nan.startswith("vetor:") and m_dim and m_dim.startswith("vetor:") and m_inc)
    out["ok"] = bool(out["passa_com_alvos_proprios"] and ok_p and ind_ok and borda_ok and ex_ok)
    return out


# ------------------------------------------------------------------ T5
def mc():
    rng_r = np.random.default_rng(SEEDS["T5_ruido"]); rng_f = np.random.default_rng(SEEDS["T5_fundo"])
    cb = np.asarray(bg["covariance"], float); gh = np.asarray(bg["gradient_h"], float); gk = np.asarray(bg["gradient_k"], float)
    logK = float(bg["logK"])
    Lb = np.linalg.cholesky(cb)
    eps = rng_r.standard_normal((N_MC, SQ.shape[1])) @ SQ.T                       # N x 255, no suporte
    delta = rng_f.standard_normal((N_MC, 3)) @ Lb.T                               # delta ~ N(0, Cb)
    x_nuis = gerar_x(0.0, SEEDS["T5_nuis"])
    base = (A[:, :h] @ x_nuis[:h])[None, :]
    xr = x_ref_255()
    res = {}
    for hip, h_true in (("nulo", np.log10(H0_bg) + delta @ gh), ("lei_K", np.log10(H0_bg) + logK + delta @ (gh + gk))):
        y = base + h_true[:, None] * A[:, h][None, :] + eps
        loc = y - (A @ xr)[None, :]
        for nome_est, est, cols in (("rede255", est255, slice(None)), ("S0", est0, keep)):
            ev = evaluate_v411({"local": loc[:, cols], "background": np.zeros((N_MC, 3))}, est)
            res[(hip, nome_est)] = ev
    return res, logK


@teste("T5_monte_carlo")
def _():
    res, logK = mc()
    models = list(s0["model_names"])
    out = {"N": N_MC, "tolerancia": "4 erros-padrao", "combos": {}}
    ok = True
    for nome_est, est in (("rede255", est255), ("S0", est0)):
        for i, m in enumerate(models):
            sdn, sdt = float(est["sd_null"][i]), float(est["sd_tgl"][i])
            D = logK / sdn
            zn0 = np.asarray(res[("nulo", nome_est)]["z_null"])[:, i]
            znK = np.asarray(res[("lei_K", nome_est)]["z_null"])[:, i]
            ztK = np.asarray(res[("lei_K", nome_est)]["z_tgl"])[:, i]
            ztN = np.asarray(res[("nulo", nome_est)]["z_tgl"])[:, i]
            n = N_MC
            p_spec = float(norm.sf(5 - D))
            p_exato = float(norm.cdf((logK - 5 * sdn) / sdt))      # P(t >= 5 sd_null), t ~ N(logK, sd_tgl^2)
            frac = float(np.mean(znK >= 5.0))
            se_frac = float(np.sqrt(p_spec * (1 - p_spec) / n))
            c = {"D": D, "sd_tgl_sobre_sd_null": sdt / sdn,
                 "nulo": {"media_z_null": float(zn0.mean()), "se_media": 1 / np.sqrt(n), "desvio_z_null": float(zn0.std(ddof=1)), "se_desvio": 1 / np.sqrt(2 * n)},
                 "lei_K": {"media_z_tgl": float(ztK.mean()), "desvio_z_tgl": float(ztK.std(ddof=1)),
                           "media_z_null": float(znK.mean()), "se_media_z_null": float(sdt / sdn / np.sqrt(n)), "D": D,
                           "frac_z_null_ge_5": frac, "esperado_spec_Phi(D-5)": p_spec, "esperado_exato_Phi((logK-5sd_null)/sd_tgl)": p_exato,
                           "se_frac": se_frac}}
            checks = {
                "nulo_media": abs(c["nulo"]["media_z_null"]) < 4 * c["nulo"]["se_media"],
                "nulo_desvio": abs(c["nulo"]["desvio_z_null"] - 1) < 4 * c["nulo"]["se_desvio"],
                "K_media_z_tgl": abs(c["lei_K"]["media_z_tgl"]) < 4 / np.sqrt(n),
                "K_desvio_z_tgl": abs(c["lei_K"]["desvio_z_tgl"] - 1) < 4 / np.sqrt(2 * n),
                "K_media_z_null_vs_D": abs(c["lei_K"]["media_z_null"] - D) < 4 * c["lei_K"]["se_media_z_null"],
                "K_fracao_vs_Phi(D-5)_spec": abs(frac - p_spec) < 4 * se_frac,
                "K_fracao_vs_exato": abs(frac - p_exato) < 4 * se_frac}
            c["checks"] = {k: bool(v) for k, v in checks.items()}
            c["ok"] = all(c["checks"].values())
            c["dif_spec_vs_exato"] = abs(p_spec - p_exato)
            c["media_z_tgl_sob_nulo_(informativo)"] = float(ztN.mean())
            ok = ok and c["ok"]
            out["combos"]["%s/%s" % (nome_est, m)] = c
    out["ok"] = bool(ok)
    return out


# ------------------------------------------------------------------ T6
def _t6_com(R):
    V = R["vereditos"]
    casos = [
        ("1 portao falso (z grande)", (6.0, 0.0, 6.7, False), V["inconclusivo"] + V["sufixo"], "INCONCLUSIVE", 1),
        ("1 portao falso vence |z_tgl|>=5", (6.0, 9.0, 6.7, False), V["inconclusivo"] + V["sufixo"], "INCONCLUSIVE", 1),
        ("1 portao falso com z nan", (float("nan"), float("nan"), 6.7, False), V["inconclusivo"] + V["sufixo"], "INCONCLUSIVE", 1),
        ("2 lei K falsificada (z_tgl=-5.5)", (6.0, -5.5, 6.7, True), V["lei_falsificada"] + V["sufixo"], "FALSIFIED", 2),
        ("2 borda |z_tgl|=5.0", (6.0, 5.0, 6.7, True), V["lei_falsificada"] + V["sufixo"], "FALSIFIED", 2),
        ("3 subpotente D=4.0", (6.0, 0.0, 4.0, True), V["subpotente"] % "4_00" + V["sufixo"], "INCONCLUSIVE", 3),
        ("4 leitura z_null=5.7", (5.7, 1.0, 6.7, True), "".join(V["leitura_partes"]) % 5, "NOT_FALSIFIED", 4),
        ("4 borda |z_tgl|=compat_95", (5.2, 1.959963984540054, 6.7, True), "".join(V["leitura_partes"]) % 5, "NOT_FALSIFIED", 4),
        ("5 tensao z_null=5.2 z_tgl=3", (5.2, 3.0, 6.7, True), V["tensao"] % 5 + V["sufixo"], "NOT_FALSIFIED", 5),
        ("5 borda compat_95+", (7.4, 1.96, 6.7, True), V["tensao"] % 7 + V["sufixo"], "NOT_FALSIFIED", 5),
        ("6 nao discriminado faixa0", (2.0, 0.5, 6.7, True), V["nao_discriminado"] % V["faixas"][0] + V["sufixo"], "NOT_FALSIFIED", 6),
        ("6 nao discriminado faixa1", (2.0, 2.0, 6.7, True), V["nao_discriminado"] % V["faixas"][1] + V["sufixo"], "NOT_FALSIFIED", 6),
        ("6 nao discriminado faixa2", (2.0, 4.0, 6.7, True), V["nao_discriminado"] % V["faixas"][2] + V["sufixo"], "NOT_FALSIFIED", 6),
        ("6 borda z_null=4.999", (4.999, 0.0, 6.7, True), V["nao_discriminado"] % V["faixas"][0] + V["sufixo"], "NOT_FALSIFIED", 6)]
    out = {"casos": []}
    ok = True
    ramos_vistos = set()
    for nome, (zn, zt, D, p1), cab, outc, ramo in casos:
        got = veredito_h0dn_v411(zn, zt, D, p1, R)
        o = {"caso": nome, "obtido": list(got), "esperado": [cab, outc, ramo], "ok": got == (cab, outc, ramo)}
        ok = ok and o["ok"]; ramos_vistos.add(got[2]); out["casos"].append(o)
    out["ramos_alcancados"] = sorted(ramos_vistos)
    out["ok"] = bool(ok and ramos_vistos == {1, 2, 3, 4, 5, 6})
    return out


@teste("T6_seis_ramos_do_veredito")
def _():
    a = _t6_com(ramos_teste())
    b = _t6_com(RAMOS_PROD)
    cabecas = {}
    for c in b["casos"]:
        cabecas.setdefault(str(c["obtido"][2]), []).append(c["obtido"][0])
    try:
        ab.conferir_integridade(rede, congelado, s0, bg, RAMOS_PROD); integ = True
    except ValueError:
        integ = False
    return {"ok": bool(a["ok"] and b["ok"] and integ), "ramos_de_teste": a, "ramos_de_producao": b,
            "cabecas_de_producao_por_ramo(ramo 6 tem tres faixas)": {k: sorted(set(v)) for k, v in cabecas.items()},
            "integridade_aceita_ramos_de_producao": integ,
            "ramos_v410_json_sha256": sha_file(OUT / "RAMOS_V410.json")}


# ------------------------------------------------------------------ T7
@teste("T7_estresses_finitos_caso_que_passa_o_portao", tipo="conferencia_de_consistencia")
def _():
    alvos = alvos_do_vetor(Y_RAW)
    r = rodar_abrir(Y_RAW, alvos)
    out = {"portao_1_ok": r["portao_1_ok"]}
    if not r["portao_1_ok"]:
        out["ok"] = False; return out
    e = r["estresse"]; st = r["estatistica"]
    def fin(x):
        return bool(np.all(np.isfinite(np.asarray(x, float))))
    i_ = e["i_tau_por_linha"]; ii = e["ii_ancora_unica"]; iii = e["iii_vies_por_hospedeira"]
    finitos = {"i": all(fin(i_[k]) for k in i_ if k != "modelo"), "ii": all(fin(v[k]) for v in ii["ancoras"].values() if "recusada" not in v for k in ("t", "z_null", "z_tgl", "D")) and fin(ii["dispersao_t"]),
               "iii": all(fin(v[k]) for kb, v in iii.items() if kb.startswith("b_") for k in v)}
    # recomputo direto
    L255 = LOC_RAW
    ta_direto = {a: np.asarray(s0["weights_" + a]) @ L255[np.asarray(s0["keep_" + a], int)] for a in s0["anchor_names"]}
    dif_a = max(float(np.max(np.abs(ta_direto[a] - np.asarray(ii["ancoras"][a]["t"])))) for a in s0["anchor_names"])
    tau_ref = st["support_l2"] / np.sqrt(s0["null_basis"].shape[1])
    s2 = np.asarray(s0["sum_w2_touched"]); sdn = np.asarray(s0["sd_null"])
    sdp_ref = np.sqrt(sdn ** 2 + tau_ref ** 2 * s2)
    larg = {k: float(np.max(np.abs((np.asarray(v["z_null_max"]) - np.asarray(v["z_null_min"])) / 2 - np.asarray(v["delta_t"]) / sdn))) for k, v in iii.items() if k.startswith("b_")}
    out.update({"finitos": finitos, "tau_hat": i_["tau_hat"], "tau_hat_ref": float(tau_ref), "dif_sd_linha": float(np.max(np.abs(np.asarray(i_["sd_null_linha"]) - sdp_ref))),
                "D_linha_menor_ou_igual_D": bool(np.all(np.asarray(i_["D"]) <= np.asarray(st["D_s0"]) + 1e-15)),
                "ancoras": {a: {"D": v.get("D"), "t": v.get("t")} for a, v in ii["ancoras"].items()}, "dispersao_t": ii["dispersao_t"],
                "dif_t_ancora_vs_direto": dif_a, "dif_largura_faixa_iii": larg,
                "z_null": st["z_null"], "z_tgl": st["z_tgl"], "t": st["t"], "support_l2": st["support_l2"],
                "veredito": r["veredito"], "linha_ao_lado": r["linha_ao_lado_cefeidas_livres"],
                "iii": {k: {"z_null_min": v["z_null_min"], "z_null_max": v["z_null_max"]} for k, v in iii.items() if k.startswith("b_")}})
    pares = ab.pares_de_coerencia(rede, congelado, s0)
    coer = r["coerencia"]
    dif_coer = max(abs(coer[k]["dif"] - float(Y_RAW @ p["d"])) for k, p in pares.items())
    out["coerencia"] = {k: {kk: vv for kk, vv in v.items()} for k, v in coer.items()}
    out["dif_coerencia_vs_recomputo"] = float(dif_coer)
    coer_ok = set(coer) == {"primario_vs_rede_completa", "cefeidas_livres_vs_primario", "ancora_N4258_vs_primario", "ancora_LMC_vs_primario", "ancora_MW_vs_primario", "ancora_N4258_vs_LMC", "ancora_N4258_vs_MW", "ancora_LMC_vs_MW"}         and dif_coer < 1e-12 and all(v["z_dif"] is not None and np.isfinite(v["z_dif"]) for v in coer.values())
    MODELO_I = ("ruido adicional independente e homoscedastico nas 111 linhas brutas (R_extra = tau^2 I_111); pesos mantidos; "
                "tau_hat = RMS em torno de zero da projecao nula (norma / raiz de 72); estimado depois de observar o vetor: pos-observacao, nao cego")
    D90 = float(5 - norm.ppf(0.10)); soma_a = np.asarray(s0["s_host"], float).sum(axis=1)
    tira, fab = iii["vies_comum_que_tira_do_portao_90"], iii["vies_comum_que_fabrica_5_sigma"]
    tira_ref = (float(s0["logK"]) - D90 * sdn[0]) / abs(soma_a[0]); fab_ref = 5 * sdn[0] / abs(soma_a[0])
    out["campos_novos"] = {"i_modelo_texto_exato": i_["modelo"] == MODELO_I, "iii_formula_texto_exato": iii["formula"] == "delta = B * soma_g | soma_{i em g} w_i c_i |",
                           "soma_g_a_g": soma_a.tolist(), "vies_comum_que_tira_do_portao_90": tira, "vies_comum_que_fabrica_5_sigma": fab,
                           "ref_tira_modelo0": float(tira_ref), "ref_fabrica_modelo0": float(fab_ref), "D90": D90}
    novos_ok = bool(i_["modelo"] == MODELO_I and iii["formula"] == "delta = B * soma_g | soma_{i em g} w_i c_i |" and abs(tira[0] - tira_ref) < 1e-15
                    and abs(fab[0] - fab_ref) < 1e-15 and tira[1] is None and fab[1] is None)
    out["ok"] = bool(novos_ok and coer_ok and all(finitos.values()) and abs(i_["tau_hat"] - tau_ref) < 1e-15 and out["dif_sd_linha"] < 1e-15
                     and out["D_linha_menor_ou_igual_D"] and dif_a < 1e-12 and max(larg.values()) < 1e-15 and len(ii["ancoras"]) == 3
                     and all("recusada" not in v for v in ii["ancoras"].values()))
    return out


# ------------------------------------------------------------------ T8
@teste("T8_geometry_identica")
def _():
    def seg(path):
        txt = Path(path).read_text(encoding="utf-8")
        tree = ast.parse(txt)
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "geometry")
        return ast.get_source_segment(txt, fn)
    a, b = seg(B / "estimator.py"), seg(HERE / "estimator_v411.py")
    return {"ok": a == b, "sha256_congelado": hashlib.sha256(a.encode("utf-8")).hexdigest(), "sha256_v411": hashlib.sha256(b.encode("utf-8")).hexdigest(),
            "bytes": len(a.encode("utf-8"))}


# ------------------------------------------------------------------ auxiliar: leitor do README
@teste("AUX_leitor_do_README", tipo="conferencia_de_consistencia")
def _():
    sha = sha_file(README)
    al = ab.ler_alvos_readme(README, sha)
    try:
        ab.ler_alvos_readme(README, "0" * 64); levanta = False
    except ValueError:
        levanta = True
    man = json.loads((OUT / "MANIFESTO_S0.json").read_text(encoding="utf-8"))
    iguais = all(man["base_da_colaboracao_README"][k] == al[k] for k in ("H0", "sig", "chi2", "ndof"))
    try:
        ab.ler_alvos_readme(README, None); none_levanta = False
    except ValueError:
        none_levanta = True
    return {"ok": bool(levanta and none_levanta and iguais and al["ndof"] == man["conferencia_ndof"]["rank_C_menos_colunas_de_A_na_rede_completa"]),
            "sha256_None_levanta_ValueError(preparar_estimador_s0.py chama assim)": none_levanta,
            "pino_errado_levanta": levanta, "ndof_readme_igual_rank_menos_colunas": al["ndof"] == man["conferencia_ndof"]["rank_C_menos_colunas_de_A_na_rede_completa"]}


# ------------------------------------------------------------------ rodada de conserto: T9-T18 e F
def msg_de(f):
    """Texto do ValueError levantado por f() (None se nao levantar)."""
    try:
        f()
        return None
    except ValueError as e:
        return str(e)


def simular_locais(n, seed_r, seed_f, seed_n, hip, tau=0.0, seed_t=None):
    """Vetores CRUS sinteticos (N x 255) do modelo publicado: nuisance fixo + h verdadeiro (fundo e, se lei_K, logK) + ruido no suporte
    (+ ruido independente tau nas linhas tocadas pelo nulo)."""
    rng_r, rng_f = np.random.default_rng(seed_r), np.random.default_rng(seed_f)
    gh, gk = np.asarray(bg["gradient_h"], float), np.asarray(bg["gradient_k"], float)
    Lb = np.linalg.cholesky(np.asarray(bg["covariance"], float))
    eps = rng_r.standard_normal((n, SQ.shape[1])) @ SQ.T
    delta = rng_f.standard_normal((n, 3)) @ Lb.T
    x_nuis = gerar_x(0.0, seed_n)
    base = (A[:, :h] @ x_nuis[:h])[None, :]
    h_true = np.log10(H0_bg) + delta @ gh + ((float(bg["logK"]) + delta @ gk) if hip == "lei_K" else 0.0)
    y = base + h_true[:, None] * A[:, h][None, :] + eps
    if tau:
        t255 = keep[np.asarray(s0["touched"], int)]
        y[:, t255] += tau * np.random.default_rng(seed_t).standard_normal((n, len(t255)))
    return y


XREF = x_ref_255()


def BG0(n):
    return np.zeros((n, 3))


@teste("T9_keep_desalinhado_de_weights")
def _():
    al = alvos_do_vetor(Y_RAW)
    perm = np.random.default_rng(SEEDS["gerador"] + 9).permutation(len(keep))
    variantes = {}
    sa = dict(s0); sa["keep"] = np.asarray(s0["keep"]) + 1
    variantes["keep_deslocado_de_1"] = {"s0_": sa}
    sb = dict(s0); sb["weights"] = np.asarray(s0["weights"])[:, perm]
    variantes["pesos_permutados_nas_colunas"] = {"s0_": sb}
    sc = dict(s0); sc["weights"] = np.asarray(s0["weights"])[::-1].copy()
    variantes["linhas_de_pesos_trocadas_(modelos)"] = {"s0_": sc}
    sd_ = dict(s0); k2 = np.asarray(s0["keep"]).copy(); k2[[10, 11]] = k2[[11, 10]]
    sd_["keep"] = k2
    variantes["keep_nao_crescente"] = {"s0_": sd_}
    sn_idx = [i for i, r_ in enumerate(rede["row_names"]) if r_.startswith("SNe Ia equation")]
    se_ = dict(s0); se_["keep"] = np.array([i for i in range(255) if i not in set(sn_idx[:13])], dtype=int)   # 242 validos, mas tira as 13 PRIMEIRAS SN
    variantes["keep_valido_mas_complemento_nas_13_primeiras_SN"] = {"s0_": se_}
    out = {"variantes": {}}
    ok = True
    for nome, kw in variantes.items():
        m = msg_de(lambda: rodar_abrir(Y_RAW, al, **kw))
        o = {"mensagem": m, "ok": bool(m and m.startswith("integridade:"))}
        ok = ok and o["ok"]
        out["variantes"][nome] = o
    # a outra metade do portao: 1b reproduz mas os pesos congelados nao reproduzem logh -> integridade (nao veredito)
    cg = dict(congelado); w = congelado["weights"].copy(); w[0] = w[0] + 1e-12; cg["weights"] = w
    m1 = msg_de(lambda: rodar_abrir(Y_RAW, al, congelado_=cg))
    old = ab.TOL_W
    ab.TOL_W = 0.0
    try:
        m2 = msg_de(lambda: rodar_abrir(Y_RAW, al))
    finally:
        ab.TOL_W = old
    out["pesos_congelados_corrompidos_1e-12_por_entrada"] = {"mensagem": m1, "ok": bool(m1 and m1.startswith("integridade:"))}
    out["tolerancia_W_zero_(caminho pesos_consistentes/1c)"] = {"mensagem": m2, "ok": bool(m2 and m2.startswith("integridade:"))}
    controle = rodar_abrir(Y_RAW, al)
    out["controle_sem_defeito_passa"] = bool(controle["portao_1_ok"])
    out["ok"] = bool(ok and out["pesos_congelados_corrompidos_1e-12_por_entrada"]["ok"] and out["tolerancia_W_zero_(caminho pesos_consistentes/1c)"]["ok"]
                     and out["controle_sem_defeito_passa"])
    return out


@teste("T10_escalas_adulteradas")
def _():
    al = alvos_do_vetor(Y_RAW)
    casos = {}
    s1 = dict(s0); s1["logK"] = float(s0["logK"]) * 1.5; casos["s0.logK x1.5"] = {"s0_": s1}
    s2 = dict(s0); s2["sd_null"] = np.asarray(s0["sd_null"]) * 1.01; casos["s0.sd_null x1.01"] = {"s0_": s2}
    s3 = dict(s0); s3["sd_tgl"] = np.asarray(s0["sd_tgl"]) * 1.01; casos["s0.sd_tgl x1.01 (extra)"] = {"s0_": s3}
    s4 = dict(s0); s4["sd_null_LMC"] = np.asarray(s0["sd_null_LMC"]) * 1.01; casos["s0.sd_null_LMC x1.01 (extra)"] = {"s0_": s4}
    c1 = dict(congelado); c1["logK"] = float(congelado["logK"]) * 1.5; casos["congelado.logK x1.5 (extra)"] = {"congelado_": c1}
    out = {"casos": {}}
    ok = True
    for nome, kw in casos.items():
        m = msg_de(lambda: rodar_abrir(Y_RAW, al, **kw))
        o = {"mensagem": m, "ok": bool(m and m.startswith("integridade:"))}
        ok = ok and o["ok"]
        out["casos"][nome] = o
    out["ok"] = ok
    return out


@teste("T11_modelos_invertidos")
def _():
    al = alvos_do_vetor(Y_RAW)
    s1 = dict(s0); s1["model_names"] = list(reversed(s0["model_names"]))
    c1 = dict(congelado); c1["model_names"] = list(reversed(congelado["model_names"]))
    m1 = msg_de(lambda: rodar_abrir(Y_RAW, al, s0_=s1))
    m2 = msg_de(lambda: rodar_abrir(Y_RAW, al, congelado_=c1))
    return {"s0_invertido": m1, "congelado_invertido": m2, "ok": bool(m1 and m1.startswith("integridade:") and m2 and m2.startswith("integridade:"))}


@teste("T12_vetor_mal_formado")
def _():
    al = alvos_do_vetor(Y_RAW)
    y_nan = Y_RAW.copy(); y_nan[7] = np.nan
    casos = {"float32": Y_RAW.astype(np.float32), "um_NaN": y_nan, "um_inf (extra)": np.where(np.arange(255) == 5, np.inf, Y_RAW),
             "shape_254 (extra)": Y_RAW[:-1].copy(), "lista_python (extra)": Y_RAW.tolist(), "int64 (extra)": np.round(Y_RAW).astype(np.int64)}
    out = {"casos": {}}
    ok = True
    for nome, yy in casos.items():
        m = msg_de(lambda: rodar_abrir(yy, al))
        o = {"mensagem": m, "ok": bool(m == "vetor: float64 (255,) finito exigido")}
        ok = ok and o["ok"]
        out["casos"][nome] = o
    out["ok"] = ok
    return out


@teste("T13_ramos_adulterados")
def _():
    al = alvos_do_vetor(Y_RAW)
    r1 = ramos_teste(); r1["limiar"] = 4.0
    r2 = ramos_teste(); r2["compat_95"] = 1.96
    r3 = ramos_teste(); del r3["vereditos"]["tensao"]
    casos = {"limiar 4.0": r1, "compat_95 1.96 (extra)": r2, "sem chave 'tensao' (extra)": r3}
    out = {"casos": {}}
    ok = True
    for nome, rr in casos.items():
        m = msg_de(lambda: rodar_abrir(Y_RAW, al, ramos_=rr))
        o = {"mensagem": m, "ok": bool(m and m.startswith("integridade:"))}
        ok = ok and o["ok"]
        out["casos"][nome] = o
    out["ok"] = ok
    return out


@teste("T14_ancora_unica_coerente_no_lugar_do_S0")
def _():
    al = alvos_do_vetor(Y_RAW)
    out = {"casos": {}}
    ok = True
    for a in s0["anchor_names"]:
        sx = dict(s0)
        for k in ("keep", "colmask", "weights", "null_basis", "sd_null", "sd_tgl", "D"):
            sx[k] = s0[k + "_" + a]
        sx["h_index_s0"] = s0["h_index_" + a]
        m = msg_de(lambda: rodar_abrir(Y_RAW, al, s0_=sx))
        o = {"mensagem": m, "ok": bool(m and m.startswith("integridade:"))}
        ok = ok and o["ok"]
        out["casos"][a] = o
    out["ok"] = ok
    return out


def exec_ctx(td):
    """Ambiente sintetico do executor num diretorio temporario: vetor, README e pre-registro SINTETICOS; pinos montados a cada chamada."""
    exe = HERE / "executar_abertura_v411.py"
    ARQ = ("abertura_v411.py", "estimator_v411.py", "veredito_v411.py", "executar_abertura_v411.py")
    np.savez(td / "y_sint.npz", y=Y_RAW)
    al = alvos_do_vetor(Y_RAW)
    readme = td / "README_sint.md"
    readme.write_text("# README sintetico\n\nH0=%.4f+/-%.4f km/s/Mpc | Chi-squared=%.4f | ndof=%d | Reduced Chi-squared=0.9 | MB=-19.252+/-0.022\n"
                      % (al["H0"], al["sig"], al["chi2"], al["ndof"]), encoding="utf-8")
    (td / "PRE_REGISTRO_sint.txt").write_text("texto selado SINTETICO do pre-registro (so' para o teste)\n", encoding="utf-8")
    cont = [0]

    def pin(p):
        return {"path": str(p), "sha256": sha_file(p)}

    def pinos_base(saida=None):
        cont[0] += 1
        sd = saida if saida is not None else td / ("saida_%d.json" % cont[0])
        return {"rede": pin(NETWORK), "congelado": pin(FROZEN), "s0": pin(S0NPZ), "bg": pin(BG1), "readme": pin(readme),
                "ramos": pin(OUT / "RAMOS_V410.json"), "pre_registro": pin(td / "PRE_REGISTRO_sint.txt"),
                "vetor": dict(pin(td / "y_sint.npz"), chave="y", convencao="raw_MAS"), "saida": {"path": str(sd)},
                "emenda": {"rotulo": "EMENDA_SINTETICA_T", "regra_antiga": "regra antiga sintetica", "data": "2026-11-11", "motivo": "motivo sintetico"},
                "alvo_fp": repr(float(al["fp"])), "codigo": {n: sha_file(HERE / n) for n in ARQ}}

    def run(pinos, ensaio=False, extra=()):
        cont[0] += 1
        pj = td / ("pinos_%d.json" % cont[0])
        pj.write_text(json.dumps(pinos), encoding="utf-8")
        cmd = [sys.executable, "-X", "utf8", "-B", str(exe), "--pinos", str(pj)] + (["--ensaio"] if ensaio else []) + list(extra)
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=600)
        return p.returncode, p.stdout, p.stderr

    return types.SimpleNamespace(al=al, pin=pin, pinos_base=pinos_base, run=run, readme=readme)


def sha_arq_de(p):
    return Path(str(p) + ".sha256")


@teste("T15_executor_ponta_a_ponta")
def _():
    out = {"casos": {}}
    estado = {"ok": True}

    def reg(nome, cond, **info):
        info["ok"] = bool(cond)
        estado["ok"] = estado["ok"] and info["ok"]
        out["casos"][nome] = info

    with tempfile.TemporaryDirectory(prefix="h0dn_v411_t15_") as td_:
        td = Path(td_)
        cx = exec_ctx(td)
        al, pin, pinos_base, run = cx.al, cx.pin, cx.pinos_base, cx.run
        # 1. ensaio
        pb = pinos_base(); sd = Path(pb["saida"]["path"])
        rc, so, se = run(pb, ensaio=True)
        reg("1_ensaio_passa_sem_gravar_saida", rc == 0 and "vetor NAO aberto" in so and not sd.exists() and not sha_arq_de(sd).exists(), rc=rc, stdout=so.strip(), stderr=se.strip()[:300])
        # 2. execucao real
        pb = pinos_base(); sd2 = Path(pb["saida"]["path"])
        rc, so, se = run(pb)
        gravou = sd2.exists()
        res_json = json.loads(sd2.read_text(encoding="utf-8")) if gravou else {}
        z_proc = ab.abrir(Y_RAW, rede, congelado, s0, bg, dict(al), RAMOS_PROD)["estatistica"]["z_null"]
        z_exe = (res_json.get("resultado", {}).get("estatistica") or {}).get("z_null")
        sha_saida = sha_file(sd2) if gravou else None
        reg("2_execucao_real_grava_saida", rc == 0 and gravou and (res_json["resultado"]["portao_1_ok"] is True) and z_exe is not None
            and max(abs(a - b) for a, b in zip(z_exe, z_proc)) < 1e-12 and (sha_saida in so),
            rc=rc, stdout=so.strip()[:300], stderr=se.strip()[:300], portao_1_ok=res_json.get("resultado", {}).get("portao_1_ok"),
            ramo=(res_json.get("resultado", {}).get("veredito") or {}).get("ramo"), z_null_executor=z_exe, z_null_em_processo=z_proc,
            chaves_da_saida=sorted(res_json), coerencia_presente=bool((res_json.get("resultado") or {}).get("coerencia")),
            decomposicao_presente=bool((res_json.get("resultado") or {}).get("decomposicao")))
        # 3. segunda execucao com os mesmos pinos
        rc3, so3, se3 = run(pb)
        reg("3_segunda_execucao_recusa_saida_existente", rc3 == 4 and "ja existe" in se3 and sha_file(sd2) == sha_saida, rc=rc3, stderr=se3.strip()[:300])
        # 4. um byte do BG1 (copia) alterado
        raw = BG1.read_bytes()
        s = repr(float(bg["H0"])).encode()
        assert raw.count(s) >= 1
        raw_b = raw.replace(s, s[:-1] + (b"5" if s[-1:] != b"5" else b"6"), 1)
        assert len(raw_b) == len(raw) and sum(1 for x, y2 in zip(raw, raw_b) if x != y2) == 1
        (td / "BG1_1byte.json").write_bytes(raw_b)
        pb = pinos_base(); pb["bg"] = dict(pb["bg"], path=str(td / "BG1_1byte.json"))
        rc, so, se = run(pb)
        reg("4_um_byte_do_BG1_recusa_por_sha", rc == 2 and "sha256 diferente" in se and not Path(pb["saida"]["path"]).exists(), rc=rc, stderr=se.strip()[:300])
        # 5. H0 alterado coerentemente nas tres copias, pinos NAO atualizados
        bgd = json.loads(raw.decode("utf-8")); bgd["H0"] = bgd["H0"] * 1.01
        (td / "BG1_H0.json").write_text(json.dumps(bgd), encoding="utf-8")
        for nome, src in (("estimator_frozen_H0.npz", FROZEN), ("estimador_s0_H0.npz", S0NPZ)):
            with np.load(src, allow_pickle=False) as d:
                arr = {k: d[k] for k in d.files}
            arr["H0"] = np.array(float(arr["H0"]) * 1.01)
            np.savez(td / nome, **arr)
        pc = pinos_base()
        pc["bg"] = dict(pc["bg"], path=str(td / "BG1_H0.json")); pc["congelado"] = dict(pc["congelado"], path=str(td / "estimator_frozen_H0.npz"))
        pc["s0"] = dict(pc["s0"], path=str(td / "estimador_s0_H0.npz"))
        rc, so, se = run(pc)
        reg("5_H0_alterado_coerentemente_em_tres_copias_sem_atualizar_pinos_recusa_por_sha", rc == 2 and "sha256 diferente" in se and not Path(pc["saida"]["path"]).exists(), rc=rc, stderr=se.strip()[:300])
        # 5b (informativo): mesmas copias COM pinos atualizados -> a integridade nao pega alteracao coerente; so' os pinos pegam
        pc2 = pinos_base()
        pc2["bg"] = pin(td / "BG1_H0.json"); pc2["congelado"] = pin(td / "estimator_frozen_H0.npz"); pc2["s0"] = pin(td / "estimador_s0_H0.npz")
        rc, so, se = run(pc2)
        out["informativo_5b_pinos_atualizados_com_H0_coerente"] = {"rc": rc, "stdout": so.strip()[:200], "stderr": se.strip()[:300],
                                                                    "leitura": "rc 0 = a integridade NAO barra alteracao coerente de H0; so' o pino sha256 barra"}
        # 6. campo ausente; sha de codigo errado; codigo sem o executor
        pm = pinos_base(); del pm["alvo_fp"]
        rc, so, se = run(pm)
        reg("6a_campo_ausente_alvo_fp_recusa", rc == 2 and "alvo_fp" in se and not Path(pm["saida"]["path"]).exists(), rc=rc, stderr=se.strip()[:300])
        pm = pinos_base(); pm["codigo"] = dict(pm["codigo"], **{"veredito_v411.py": "0" * 64})
        rc, so, se = run(pm)
        reg("6b_sha_de_codigo_errado_recusa", rc == 2 and "codigo" in se and not Path(pm["saida"]["path"]).exists(), rc=rc, stderr=se.strip()[:300])
        pm = pinos_base(); pm["codigo"] = {k: v for k, v in pm["codigo"].items() if k != "executar_abertura_v411.py"}
        rc, so, se = run(pm)
        reg("6c_codigo_sem_o_executor_recusa", rc == 2 and not Path(pm["saida"]["path"]).exists(), rc=rc, stderr=se.strip()[:300])
        # 7. integridade falha com pinos corretos -> rc 3, nada gravado
        with np.load(S0NPZ, allow_pickle=False) as d:
            arr = {k: d[k] for k in d.files}
        arr["logK"] = np.array(float(arr["logK"]) * 1.5)
        np.savez(td / "s0_logK.npz", **arr)
        pi = pinos_base(); pi["s0"] = pin(td / "s0_logK.npz")
        rc, so, se = run(pi)
        reg("7_integridade_falha_rc3_nada_gravado", rc == 3 and "integridade" in se and not Path(pi["saida"]["path"]).exists(), rc=rc, stderr=se.strip()[:300])
        # 8. vetor float32 com pinos corretos -> rc 3 (vetor:)
        np.savez(td / "y_f32.npz", y=Y_RAW.astype(np.float32))
        pv = pinos_base(); pv["vetor"] = dict(pin(td / "y_f32.npz"), chave="y", convencao="raw_MAS")
        rc, so, se = run(pv)
        reg("8_vetor_float32_rc3_nada_gravado", rc == 3 and "vetor:" in se and not Path(pv["saida"]["path"]).exists(), rc=rc, stderr=se.strip()[:300])
        # 9. portao falha (alvo_fp errado) -> rc 0, ramo (1) gravado, sem t/z/estresse/coerencia/decomposicao
        pf = pinos_base(); pf["alvo_fp"] = repr(float(al["fp"]) + 1e-3)
        rc, so, se = run(pf)
        sd9 = Path(pf["saida"]["path"])
        r9 = json.loads(sd9.read_text(encoding="utf-8"))["resultado"] if sd9.exists() else {}
        reg("9_portao_falha_grava_ramo1_sem_estatistica", rc == 0 and r9.get("veredito", {}).get("ramo") == 1 and r9.get("estatistica") is None
            and r9.get("estresse") is None and r9.get("coerencia") is None and r9.get("decomposicao") is None,
            rc=rc, ramo=(r9.get("veredito") or {}).get("ramo"), motivos=(r9.get("portao_1") or {}).get("motivos"))
    out["ok"] = bool(estado["ok"])
    return out


@teste("T22_executor_pre_registro_convencao_emenda_saida")
def _():
    out = {"casos": {}}
    estado = {"ok": True}

    def reg(nome, cond, **info):
        info["ok"] = bool(cond)
        estado["ok"] = estado["ok"] and info["ok"]
        out["casos"][nome] = info

    with tempfile.TemporaryDirectory(prefix="h0dn_v411_t22_") as td_:
        td = Path(td_)
        cx = exec_ctx(td)
        pin, pinos_base, run = cx.pin, cx.pinos_base, cx.run
        # pre_registro ausente / sha errado / arquivo inexistente
        pm = pinos_base(); del pm["pre_registro"]
        rc, so, se = run(pm)
        reg("pre_registro_ausente_recusa", rc == 2 and "pre_registro" in se and not Path(pm["saida"]["path"]).exists(), rc=rc, stderr=se.strip()[:200])
        pm = pinos_base(); pm["pre_registro"] = dict(pm["pre_registro"], sha256="0" * 64)
        rc, so, se = run(pm)
        reg("pre_registro_com_sha_errado_recusa", rc == 2 and "pre_registro" in se and "sha256 diferente" in se and not Path(pm["saida"]["path"]).exists(), rc=rc, stderr=se.strip()[:200])
        # convencao
        for rot, val in (("diferente_de_raw_MAS", "centered"), ("vazia", ""), ("caixa_diferente", "RAW_MAS")):
            pm = pinos_base(); pm["vetor"] = dict(pm["vetor"], convencao=val)
            rc, so, se = run(pm)
            reg("convencao_%s_recusa" % rot, rc == 2 and "convencao" in se and not Path(pm["saida"]["path"]).exists(), rc=rc, stderr=se.strip()[:200])
        pm = pinos_base(); del pm["vetor"]["convencao"]
        rc, so, se = run(pm)
        reg("convencao_ausente_recusa", rc == 2 and "convencao" in se, rc=rc, stderr=se.strip()[:200])
        # emenda: campo vazio, ausente, so' espacos, emenda ausente
        for rot, mod in (("campo_vazio", lambda e: e.update(motivo="")), ("campo_so_espacos", lambda e: e.update(data="   ")),
                         ("campo_ausente", lambda e: e.pop("regra_antiga"))):
            pm = pinos_base(); mod(pm["emenda"])
            rc, so, se = run(pm)
            reg("emenda_%s_recusa" % rot, rc == 2 and "emenda" in se and not Path(pm["saida"]["path"]).exists(), rc=rc, stderr=se.strip()[:200])
        pm = pinos_base(); del pm["emenda"]
        rc, so, se = run(pm)
        reg("emenda_ausente_recusa", rc == 2 and "emenda" in se, rc=rc, stderr=se.strip()[:200])
        # saida: campo ausente e --saida na linha de comando (removido)
        pm = pinos_base(); del pm["saida"]
        rc, so, se = run(pm)
        reg("saida_ausente_nos_pinos_recusa", rc == 2 and "saida" in se, rc=rc, stderr=se.strip()[:200])
        pm = pinos_base()
        rc, so, se = run(pm, extra=("--saida", str(td / "x.json")))
        reg("argumento_--saida_foi_removido", rc != 0 and not (td / "x.json").exists() and not Path(pm["saida"]["path"]).exists(), rc=rc, stderr=se.strip()[:200])
        # execucao boa: saida + .sha256 que confere; bloco emenda, pino do pre_registro e convencao na saida
        pb = pinos_base(); sd = Path(pb["saida"]["path"]); sh = sha_arq_de(sd)
        rc, so, se = run(pb)
        res = json.loads(sd.read_text(encoding="utf-8")) if sd.exists() else {}
        linha = sh.read_text(encoding="utf-8") if sh.exists() else ""
        reg("execucao_boa_grava_saida_e_sha256_que_confere", rc == 0 and sd.exists() and sh.exists() and linha == "%s  %s\n" % (sha_file(sd), sd.name),
            rc=rc, linha_sha256=linha.strip(), sha256_real=sha_file(sd) if sd.exists() else None, stdout=so.strip()[:300], stderr=se.strip()[:200])
        reg("saida_traz_emenda_pre_registro_e_convencao", res.get("emenda") == pb["emenda"] and res.get("pre_registro") == pb["pre_registro"]
            and res.get("vetor_convencao") == "raw_MAS" and (res.get("resultado") or {}).get("emenda") == pb["emenda"] and res.get("pinos_de_entrada", {}).get("vetor", {}).get("convencao") == "raw_MAS",
            chaves=sorted(res))
        # segunda execucao recusa; so' o .sha256 existindo tambem recusa; ensaio com saida existente tambem recusa
        rc, so, se = run(pb)
        reg("segunda_execucao_recusa", rc == 4 and "ja existe" in se and sha_file(sd) == linha.split()[0], rc=rc, stderr=se.strip()[:200])
        pr = pinos_base(); sdr = Path(pr["saida"]["path"])
        sha_arq_de(sdr).write_text("x  y\n", encoding="utf-8")
        rc, so, se = run(pr)
        reg("so_o_dot_sha256_existindo_recusa", rc == 4 and not sdr.exists(), rc=rc, stderr=se.strip()[:200])
        rc, so, se = run(pb, ensaio=True)
        reg("ensaio_com_saida_existente_recusa(decisao: a execucao real seria recusada)", rc == 4, rc=rc, stderr=se.strip()[:200])
    out["ok"] = bool(estado["ok"])
    return out


@teste("T16_ancoras_unicas_monte_carlo")
def _():
    n = 5000
    out = {"N": n, "ancoras": {}}
    ok = True
    for idx, a in enumerate(s0["anchor_names"]):
        ea = ab._pack_estimator(s0, "_" + a)
        ka = np.asarray(s0["keep_" + a], int)
        o = {"D": np.asarray(s0["D_" + a]).tolist()}
        sub = {}
        for hip, k in (("nulo", 0), ("lei_K", 1)):
            y = simular_locais(n, 416000 + 10 * idx + k, 416100 + 10 * idx + k, 416200 + idx, hip)
            loc = y - (A @ XREF)[None, :]
            ev = evaluate_v411({"local": loc[:, ka], "background": BG0(n)}, ea)
            zs = np.asarray(ev["z_null"] if hip == "nulo" else ev["z_tgl"])
            for i, m in enumerate(s0["model_names"]):
                mean, sd = float(zs[:, i].mean()), float(zs[:, i].std(ddof=1))
                chk = abs(mean) < 4 / np.sqrt(n) and abs(sd - 1) < 4 / np.sqrt(2 * n)
                sub["%s/%s/%s" % (hip, "z_null" if hip == "nulo" else "z_tgl", m)] = {"media": mean, "desvio": sd, "se_media": 1 / np.sqrt(n),
                                                                                    "se_desvio": 1 / np.sqrt(2 * n), "ok": bool(chk)}
                ok = ok and bool(chk)
        o["checks"] = sub
        out["ancoras"][a] = o
    r = rodar_abrir(Y_RAW, alvos_do_vetor(Y_RAW)); e = r["estresse"]
    campos = {"i.modelo": "modelo" in e["i_tau_por_linha"], "iii.formula": "formula" in e["iii_vies_por_hospedeira"],
              "iii.vies_comum_que_tira_do_portao_90": "vies_comum_que_tira_do_portao_90" in e["iii_vies_por_hospedeira"],
              "iii.vies_comum_que_fabrica_5_sigma": "vies_comum_que_fabrica_5_sigma" in e["iii_vies_por_hospedeira"],
              "ii.tres_ancoras": sorted(e["ii_ancora_unica"]["ancoras"]) == ["LMC", "MW", "N4258"]}
    out["campos_novos_do_estresse_via_abrir"] = campos
    out["ok"] = bool(ok and all(campos.values()))
    return out


@teste("T17_calibracao_do_tau")
def _():
    from scipy.special import gammaln
    tau = 0.10
    sdn = np.asarray(s0["sd_null"], float); s2 = np.asarray(s0["sum_w2_touched"], float)
    nn = s0["null_basis"].shape[1]
    esp_tau = float(tau * np.sqrt(2.0 / nn) * np.exp(gammaln((nn + 1) / 2.0) - gammaln(nn / 2.0)))   # E[tau_hat] analitico
    out = {"tau": tau, "E_tau_hat_analitico": esp_tau, "rodadas": {}}
    ok = True
    for rot, n, sr, sf, sn_, st in (("spec_N2000", 2000, 417001, 417002, 417003, 417004), ("extra_N20000", 20000, 417011, 417012, 417003, 417014)):
        y = simular_locais(n, sr, sf, sn_, "nulo", tau=tau, seed_t=st)
        loc = (y - (A @ XREF)[None, :])[:, keep]
        ev = evaluate_v411({"local": loc, "background": BG0(n)}, est0)
        th = np.asarray(ev["support_l2"]) / np.sqrt(nn)
        t = np.asarray(ev["t"])
        mean, sdm = float(th.mean()), float(th.std(ddof=1) / np.sqrt(n))
        alvo_tau = tau if rot.startswith("spec") else esp_tau
        o = {"media_tau_hat": mean, "se": sdm, "alvo": alvo_tau, "alvo_descricao": "0,10 (spec)" if rot.startswith("spec") else "E analitico (extra)",
             "tau_hat_ok": bool(abs(mean - alvo_tau) < 4 * sdm), "variancia_t": {}}
        o["distancia_em_se_de_0.10_e_do_analitico"] = {"vs_0.10": abs(mean - tau) / sdm, "vs_analitico": abs(mean - esp_tau) / sdm}
        for i, m in enumerate(s0["model_names"]):
            esp = float(sdn[i] ** 2 + tau ** 2 * s2[i])
            v = float(t[:, i].var(ddof=1)); se_v = v * np.sqrt(2.0 / (n - 1))
            sem_tau = float(sdn[i] ** 2)
            o["variancia_t"][m] = {"var_t": v, "esperado_vs_vb_tau2_sum_w2": esp, "se": se_v, "ok": bool(abs(v - esp) < 4 * se_v),
                                   "esperado_SEM_tau": sem_tau, "dist_ao_sem_tau_em_se": abs(v - sem_tau) / se_v}
        o["ok"] = bool(o["tau_hat_ok"] and all(x["ok"] for x in o["variancia_t"].values()))
        ok = ok and o["ok"]
        out["rodadas"][rot] = o
    out["ok"] = bool(ok)
    return out


@teste("T18_coerencia_monte_carlo")
def _():
    n = 5000
    P = ab.pares_de_coerencia(rede, congelado, s0)
    out = {"N": n, "itens": {}}
    ok = True
    difs = {}
    for hip in ("nulo", "lei_K"):
        y = simular_locais(n, 418001, 418002, 418003, hip)
        for nome, p in P.items():
            dif = y @ p["d"]
            z = dif / p["sd_dif"]
            difs[(hip, nome)] = dif
            mean, sd = float(z.mean()), float(z.std(ddof=1))
            chk = abs(mean) < 4 / np.sqrt(n) and abs(sd - 1) < 4 / np.sqrt(2 * n)
            out["itens"].setdefault(nome, {})[hip] = {"media_z_dif": mean, "desvio_z_dif": sd, "se_media": 1 / np.sqrt(n), "se_desvio": 1 / np.sqrt(2 * n), "ok": bool(chk)}
            ok = ok and bool(chk)
    out["invariancia_sob_K(max|dif_nulo - dif_K| com o mesmo ruido; d.A=0)"] = {nome: float(np.max(np.abs(difs[("nulo", nome)] - difs[("lei_K", nome)]))) for nome in P}
    out["ok"] = bool(ok)
    return out


@teste("F_coerencia_desenho_sd_dif", tipo="conferencia_de_consistencia")
def _():
    P = ab.pares_de_coerencia(rede, congelado, s0)
    sdn = np.asarray(s0["sd_null"], float)
    gh = np.asarray(bg["gradient_h"], float)
    vb = float(gh @ np.asarray(bg["covariance"], float) @ gh)
    out = {"itens": {k: {"sd_dif": v["sd_dif"], "sd_dif/sd_null[0](primario)": v["sd_dif"] / sdn[0], "sd_dif/sd_null[1](cefeidas livres)": v["sd_dif"] / sdn[1],
                         "sd_dif/sd_null_do_modelo_wa": v["sd_dif"] / v["sd_null_wa"]} for k, v in P.items()}}
    it1 = P["primario_vs_rede_completa"]["sd_dif"] / sdn[0]
    it2 = P["cefeidas_livres_vs_primario"]["sd_dif"] / sdn[1]
    c1 = {"obtido": it1, "alvo_da_gerencia": 0.181401, "tolerancia": 1e-5, "ok": bool(abs(it1 - 0.181401) <= 1e-5)}
    it2_p = P["cefeidas_livres_vs_primario"]["sd_dif"] / sdn[0]
    c2 = {"par": "cefeidas livres do S0 contra o primario do S0",
          "em_desvios_do_nulo_da_linha_de_cefeidas_livres": {"obtido": it2, "alvo": 0.6336125, "tolerancia": 1e-6, "ok": bool(abs(it2 - 0.6336125) <= 1e-6)},
          "em_desvios_do_nulo_do_primario": {"obtido": it2_p, "alvo": 0.8189905, "tolerancia": 1e-6, "ok": bool(abs(it2_p - 0.8189905) <= 1e-6)}}
    c2["ok"] = bool(c2["em_desvios_do_nulo_da_linha_de_cefeidas_livres"]["ok"] and c2["em_desvios_do_nulo_do_primario"]["ok"])
    # identidade de Hausman: sob o modelo publicado (GLS eficiente), Var(w_livre - w_pub) = Var(w_livre) - Var(w_pub) (confere o meu numero)
    vs = sdn ** 2 - vb
    haus = {"sd_dif_calculado": P["cefeidas_livres_vs_primario"]["sd_dif"], "sqrt(vs[1]-vs[0])": float(np.sqrt(vs[1] - vs[0]))}
    haus["ok"] = bool(abs(haus["sd_dif_calculado"] - haus["sqrt(vs[1]-vs[0])"]) < 1e-9 * haus["sd_dif_calculado"])
    # com que par o alvo 0,6489687 bate? (informativo; NAO substitui a definicao do pedido)
    wl = P["cefeidas_livres_vs_primario"]["wa"]
    d_alt = wl - np.asarray(congelado["weights"][0], float)
    sd_alt = float(np.sqrt(max(d_alt @ rede["C"] @ d_alt, 0.0)))
    alt = {"rotulo": "cefeidas livres do S0 contra a rede completa de 255", "nota": "numero RELATADO de outro par; nao entra no ok",
           "sd_dif": sd_alt, "sd_dif/sd_null[1]": sd_alt / sdn[1], "numero_dado_pela_gerencia_antes": 0.6489687,
           "coincide_a_1e-6": bool(abs(sd_alt / sdn[1] - 0.6489687) < 1e-6)}
    out.update({"item1": c1, "item2": c2, "identidade_de_Hausman_item2": haus, "cefeidas_livres_do_S0_contra_a_rede_completa_de_255": alt})
    out["ok"] = bool(c1["ok"] and c2["ok"])
    return out


@teste("T19_integridade_acrescimos")
def _():
    al = alvos_do_vetor(Y_RAW)
    N0 = np.asarray(s0["null_basis"], float)
    variantes = {}
    sa = dict(s0); sa["null_basis"] = 2.0 * N0; variantes["base_nula_S0_escalada_por_2"] = {"s0_": sa}
    sb = dict(s0); sb["null_basis"] = N0[:, :-1].copy(); variantes["base_nula_S0_com_uma_coluna_a_menos"] = {"s0_": sb}
    Nc = N0.copy(); Nc[:, 0] = N0[:, 0] + 0.5 * N0[:, 1]; Nc[:, 1] = N0[:, 0] - 0.5 * N0[:, 1]
    sc = dict(s0); sc["null_basis"] = Nc; variantes["duas_colunas_trocadas_por_combinacao_nao_ortonormal"] = {"s0_": sc}
    sd_ = dict(s0); sd_["sum_w2_touched"] = np.asarray(s0["sum_w2_touched"]) * 1.001; variantes["sum_w2_touched_x1.001"] = {"s0_": sd_}
    sh = np.asarray(s0["s_host"], float).copy(); sh[0, 3] += 1e-9
    se_ = dict(s0); se_["s_host"] = sh; variantes["um_elemento_de_s_host_mais_1e-9"] = {"s0_": se_}
    tt = np.asarray(s0["touched"]).copy()
    livre = next(i for i in range(len(keep)) if i not in set(int(x) for x in tt))
    tt[0] = livre
    sf = dict(s0); sf["touched"] = tt; variantes["touched_com_um_indice_trocado"] = {"s0_": sf}
    # extras
    cg = dict(congelado); cg["null_basis"] = 2.0 * congelado["null_basis"]; variantes["(extra) base_nula_congelada_escalada_por_2"] = {"congelado_": cg}
    sg = dict(s0); sg["host_names"] = list(reversed(s0["host_names"])); variantes["(extra) host_names_invertido_sem_reordenar_s_host"] = {"s0_": sg}
    sh2 = dict(s0); sh2["sum_abs_s_host"] = np.asarray(s0["sum_abs_s_host"]) * 1.001; variantes["(extra) sum_abs_s_host_x1.001"] = {"s0_": sh2}
    out = {"variantes": {}}
    ok = True
    for nome, kw in variantes.items():
        m = msg_de(lambda: rodar_abrir(Y_RAW, al, **kw))
        o = {"mensagem": m, "ok": bool(m and m.startswith("integridade:"))}
        ok = ok and o["ok"]
        out["variantes"][nome] = o
    out["controle_sem_defeito_passa"] = bool(rodar_abrir(Y_RAW, al)["portao_1_ok"])
    integ = ab.conferir_integridade(rede, congelado, s0, bg, RAMOS_PROD)
    out["medidas_do_desenho"] = {k: integ[k] for k in ("base_nula_S0_ortonormal_dif", "base_nula_congelado_ortonormal_dif", "postos", "touched", "sum_w2_touched_rel", "s_host_dif")}
    out["ok"] = bool(ok and out["controle_sem_defeito_passa"])
    return out


@teste("T20_decomposicao")
def _():
    out = {"casos": {}}
    ok = True
    for nome, yy in (("com_componente_nula(max|u|=0,09)", Y_RAW), ("sem_componente_nula", Y_SEM)):
        r = rodar_abrir(yy, alvos_do_vetor(yy))
        d = r["decomposicao"]
        cf = d["conferencias"]
        hosp = sorted(set(l["hospedeira"] for l in d["linhas_tocadas"]))
        anc = sorted(set(l["ancora"] for l in d["linhas_tocadas"]))
        o = {"portao_1_ok": r["portao_1_ok"], "n_linhas_tocadas": len(d["linhas_tocadas"]), "n_hospedeiras": len(hosp), "ancoras": anc,
             "n_por_hospedeira": len(d["por_hospedeira"]), "por_ancora_n_linhas": {a: v["n_linhas"] for a, v in d["por_ancora"].items()},
             "conferencias": cf, "support_l2": r["estatistica"]["support_l2"],
             "soma_r2_por_hospedeira_total": float(sum(v["soma_r2"] for v in d["por_hospedeira"].values())),
             "soma_r2_por_ancora_total": float(sum(v["soma_r2"] for v in d["por_ancora"].values())),
             "soma_w2_por_ancora_total": float(sum(v["soma_w2_primario"] for v in d["por_ancora"].values())),
             "campos_da_linha": sorted(d["linhas_tocadas"][0])}
        o["ok"] = bool(r["portao_1_ok"] and cf["soma_r2_ok"] and cf["soma_abs_a_g_ok"] and cf["soma_w2_ok"] and o["n_linhas_tocadas"] == 111
                       and o["n_hospedeiras"] == 37 and o["ancoras"] == ["LMC", "MW", "N4258"] and o["n_por_hospedeira"] == 37
                       and all(v == 37 for v in o["por_ancora_n_linhas"].values())
                       and abs(o["soma_r2_por_hospedeira_total"] - o["soma_r2_por_ancora_total"]) <= 1e-12 * max(o["soma_r2_por_ancora_total"], 1e-30)
                       and abs(o["soma_w2_por_ancora_total"] - float(s0["sum_w2_touched"][0])) <= 1e-12 * float(s0["sum_w2_touched"][0]))
        ok = ok and o["ok"]
        out["casos"][nome] = o
    out["ok"] = bool(ok)
    return out


@teste("T21_marca_dos_ramos")
def _():
    out = {"casos": {}}
    ok = True
    gerar = HERE / "gerar_ramos_v411.py"
    marca, so = "__MARCA_DE_TESTE", "__SO_DA_LEITURA_DE_TESTE"
    with tempfile.TemporaryDirectory(prefix="h0dn_v411_t21_") as td_:
        td = Path(td_)
        saida = td / "ramos_teste.json"

        def rodar(*args):
            p = subprocess.run([sys.executable, "-X", "utf8", "-B", str(gerar)] + list(args), capture_output=True, text=True, encoding="utf-8", timeout=120)
            return p.returncode, p.stdout, p.stderr
        rc, so_, se_ = rodar("--marca", marca, "--marca-so-da-leitura", so, "--saida", str(saida))
        out["geracao"] = {"rc": rc, "stdout": so_.strip(), "stderr": se_.strip()[:300]}
        if rc != 0 or not saida.exists():
            out["ok"] = False
            return out
        R = json.loads(saida.read_text(encoding="utf-8"))
        V = R["vereditos"]
        casos = [("1", (6.0, 0.0, 6.7, False)), ("2", (6.0, -5.5, 6.7, True)), ("3", (6.0, 0.0, 4.0, True)), ("4", (5.7, 1.0, 6.7, True)),
                 ("5", (5.2, 3.0, 6.7, True)), ("6", (2.0, 0.5, 6.7, True))]
        cabecas = {}
        for rotulo, (zn, zt, D, p1) in casos:
            cab, outc, ramo = veredito_h0dn_v411(zn, zt, D, p1, R)
            cabecas[rotulo] = {"ramo": ramo, "cabeca": cab, "tem_marca": marca in cab, "tem_so_da_leitura": so in cab}
        out["cabecas"] = cabecas
        out["seis_ramos"] = sorted(v["ramo"] for v in cabecas.values()) == [1, 2, 3, 4, 5, 6]
        out["todas_trazem_a_marca"] = all(v["tem_marca"] for v in cabecas.values())
        out["so_o_ramo_4_traz_a_marca_da_leitura"] = [v["ramo"] for v in cabecas.values() if v["tem_so_da_leitura"]] == [4]
        out["nenhuma_parte_traz_PROVED_inteiro"] = all("PROVED" not in p for p in V["leitura_partes"])
        cab4_prod = "".join(RAMOS_PROD["vereditos"]["leitura_partes"]) % 5
        ancora = "__PROVED_IS_VALIDITY_NOT_CREDITATION"
        esperado4 = cab4_prod.replace(ancora, so + marca + ancora, 1)
        out["cabeca_4_igual_a_producao_com_as_marcas_antes_de_PROVED"] = cabecas["4"]["cabeca"] == esperado4
        out["marca_logo_antes_de___PROVED_e_so_da_leitura_logo_antes_da_marca"] = (so + marca + ancora) in cabecas["4"]["cabeca"]
        out["sufixo_com_marca_logo_depois_de___RETRODICTION_WITHOUT_FIT"] = V["sufixo"] == RAMOS_PROD["vereditos"]["sufixo"].replace(
            "__RETRODICTION_WITHOUT_FIT", "__RETRODICTION_WITHOUT_FIT" + marca, 1)
        # nada mais muda
        R2 = json.loads(json.dumps(R)); R2["vereditos"]["sufixo"] = RAMOS_PROD["vereditos"]["sufixo"]
        R2["vereditos"]["leitura_partes"] = RAMOS_PROD["vereditos"]["leitura_partes"]
        out["nada_mais_muda"] = R2 == RAMOS_PROD
        out["partes_continuam_3_e_a_juncao_e_a_certa"] = len(V["leitura_partes"]) == 3 and "".join(V["leitura_partes"]) == "".join(RAMOS_PROD["vereditos"]["leitura_partes"]).replace(ancora, so + marca + ancora, 1)
        try:
            ab.conferir_integridade(rede, congelado, s0, bg, R); out["integridade_aceita_o_literal_de_teste"] = True
        except ValueError:
            out["integridade_aceita_o_literal_de_teste"] = False
        # so' a marca geral (sem a da leitura)
        s2 = td / "so_marca.json"
        rc2, _a, _b = rodar("--marca", marca, "--saida", str(s2))
        R3 = json.loads(s2.read_text(encoding="utf-8")) if s2.exists() else {}
        cab4_3 = veredito_h0dn_v411(5.7, 1.0, 6.7, True, R3)[0] if R3 else ""
        out["sem_marca_da_leitura_a_cabeca_4_traz_so_a_geral"] = bool(rc2 == 0 and marca in cab4_3 and "SO_DA_LEITURA" not in cab4_3)
        out["origem_gravada_com_sha256"] = bool((td / "ramos_teste_ORIGEM.json").exists() and json.loads((td / "ramos_teste_ORIGEM.json").read_text(encoding="utf-8"))["saida"]["sha256"] == sha_file(saida))
        # recusas
        recusas = {}
        for rot, args in (("sem___no_comeco", ("--marca", "MARCA", "--saida", str(td / "r1.json"))),
                          ("minuscula", ("--marca", "__marca", "--saida", str(td / "r2.json"))),
                          ("hifen", ("--marca", "__A-B", "--saida", str(td / "r3.json"))),
                          ("so_dois_underscores", ("--marca", "__", "--saida", str(td / "r4.json"))),
                          ("so_da_leitura_invalida", ("--marca", marca, "--marca-so-da-leitura", "x", "--saida", str(td / "r5.json"))),
                          ("saida_existente", ("--marca", marca, "--saida", str(saida))),
                          ("PROVED_dentro_da_marca", ("--marca", "__PROVED", "--saida", str(td / "r6.json")))):
            rr, _o, ee = rodar(*args)
            alvo = Path(args[-1])
            recusas[rot] = {"rc": rr, "recusou": bool(rr != 0), "stderr": ee.strip()[:160], "nao_criou_arquivo": (not alvo.exists()) or rot == "saida_existente"}
        out["recusas"] = recusas
        fechos = [out["seis_ramos"], out["todas_trazem_a_marca"], out["so_o_ramo_4_traz_a_marca_da_leitura"], out["nenhuma_parte_traz_PROVED_inteiro"],
                  out["cabeca_4_igual_a_producao_com_as_marcas_antes_de_PROVED"], out["marca_logo_antes_de___PROVED_e_so_da_leitura_logo_antes_da_marca"],
                  out["sufixo_com_marca_logo_depois_de___RETRODICTION_WITHOUT_FIT"], out["nada_mais_muda"], out["partes_continuam_3_e_a_juncao_e_a_certa"],
                  out["integridade_aceita_o_literal_de_teste"], out["sem_marca_da_leitura_a_cabeca_4_traz_so_a_geral"], out["origem_gravada_com_sha256"],
                  all(v["recusou"] and v["nao_criou_arquivo"] for v in recusas.values())]
        out["ok"] = bool(all(fechos))
    return out


def main():
    tests = [k for k in RESULT if k[0] in "TAF" and isinstance(RESULT[k], dict) and "ok" in RESULT[k]]
    RESULT["resumo"] = {k: bool(RESULT[k]["ok"]) for k in tests}
    RESULT["todos_ok"] = all(RESULT["resumo"].values())
    dest = OUT / "TESTES_SINTETICOS.json"
    tmp = dest.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(RESULT, ensure_ascii=False, indent=1, default=fl), encoding="utf-8")
    tmp.replace(dest)
    print(json.dumps(RESULT["resumo"], indent=1), "todos_ok =", RESULT["todos_ok"])


if __name__ == "__main__":
    main()
