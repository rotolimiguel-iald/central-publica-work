#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C3 gamma LIVRE -- rodada pre-registrada (19/10/2026, gerencia c1).

PERGUNTA: o piso das dobras D_folds(c3) do estado estacionario GKLS e uma OITAVA (ln 2)
quando o parametro de fuga gamma e LIVRE (varrido), em todas as configuracoes do validador v52?

FONTE (somente leitura): C:\\IALD\\projetos_pyhton\\acom\\TGL_C3_validator_v52.py
  build_system e lindblad_superoperator sao copiados sem alterar a logica;
  o observavel e o M7 no terceiro nivel (c3): p_i ~ lambda_i^(1/4).

NAO HA neste script: calibracao de gamma, busca de raiz, alvo de peso do core nem constante
da teoria. A conferencia e feita por grep no proprio arquivo (v. PREREGISTRO.json).

Uso:  python -B -u rodar.py        (CPU, NumPy; exige PREREGISTRO.json conferindo)
Uma unica rodada: se manifesto_dados.json existe, o script recusa rodar de novo.
"""

import os
import sys
import json
import csv
import time
import math
import hashlib
import inspect
import warnings

import numpy as np
import scipy.linalg as sla

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREGISTRO.json")
MANIFESTO = os.path.join(HERE, "manifesto_dados.json")
LN2 = math.log(2.0)

# ======================================================================================
# ESPECIFICACAO FIXADA (entra no pre-registro por sha256)
# ======================================================================================

# (d, nc, eps) -- as 9 configs de run_protocol_11 da fonte, na mesma ordem
CONFIGS = [
    (8, 2, 5.0), (10, 2, 5.0), (12, 2, 5.0), (14, 2, 5.0), (16, 2, 5.0),
    (16, 3, 5.0), (20, 3, 5.0), (24, 3, 5.0), (32, 4, 5.0),
]
SEEDS = [42, 43, 44, 45, 46]            # 42 = semente original de build_system; depois +1, +2, +3, +4
GAMMAS = np.logspace(-4.0, 0.0, 25)     # taxa da quarta dissipacao (core -> periferia), LIVRE
FIXED_RATES = [1.0, 0.5, 2.0]           # taxas das tres primeiras dissipacoes, como na fonte
N1_STATES = 200                         # estados de Hilbert-Schmidt por dimensao d
RNG_TAG = 20261019                      # etiqueta das sementes dos controles aleatorios

# tolerancias de convergencia do estado estacionario (um ponto que falha NAO converge)
TOL = {
    "s1_rel_max": 1e-9,        # menor valor singular / maior: o nucleo existe
    "s2_rel_min": 1e-8,        # segundo menor / maior: o nucleo e isolado (unico)
    "herm_max": 1e-8,          # || rho - rho^dagger || / || rho ||  antes de hermitianizar
    "trace_raw_min": 1e-6,     # |Tr| do vetor singular de norma 1: a normalizacao por traco e possivel
    "trace_err_max": 1e-12,    # |Tr rho - 1| depois de normalizar
    "tp_err_rel_max": 1e-10,   # || vec(I)^T L || / || L ||: o gerador preserva o traco
    "psd_min": -1e-9,          # menor autovalor de rho (psd)
}


# ======================================================================================
# SISTEMA (copiado da fonte: build_system e lindblad_superoperator)
# ======================================================================================

def build_system(d, nc, eps=5.0, seed=42):
    """Sistema de d niveis e nc canais core (logica da fonte, sem alteracao)."""
    np.random.seed(seed)

    mu = np.zeros(d)
    mu[:nc] = -1.0 * np.arange(nc, 0, -1)
    mu[nc:] = 0.5 + 0.3 * np.arange(d - nc)

    J = np.random.randn(d, d) * 0.2
    J = (J + J.T) / 2
    np.fill_diagonal(J, 0)
    J[:nc, :nc] *= 2

    Pi = np.zeros((d, d))
    Pi[:nc, :nc] = np.eye(nc)

    H = np.diag(mu) + J - eps * Pi
    H = (H + H.T) / 2

    ev = np.linalg.eigvalsh(H)
    E_sc = float(ev[-1] - ev[0])

    L1 = np.zeros((d, d), dtype=complex)
    for i in range(nc):
        for j in range(nc, min(nc + d // 2, d)):
            L1[i, j] = np.sqrt(0.5) * np.exp(-0.2 * (j - nc))

    L3 = np.zeros((d, d), dtype=complex)
    for i in range(nc + d // 3, d):
        L3[0, i] = np.sqrt((i - nc) / d)

    L4 = np.zeros((d, d), dtype=complex)
    for i in range(nc):
        for j in range(nc, min(nc + d // 2, d)):
            L4[i, j] = np.sqrt(0.3) * np.exp(-0.3 * abs(j - nc))

    L5 = np.zeros((d, d), dtype=complex)
    for j in range(nc, min(nc + d // 2, d)):
        for i in range(nc):
            L5[j, i] = np.sqrt(0.5) * np.exp(-0.2 * (j - nc))

    return {
        'H': H, 'Pi': Pi,
        'L_ops': [L1, L3, L4, L5],
        'd': d, 'nc': nc, 'E_sc': E_sc
    }


def lindblad_superoperator(sys_dict, gamma_leak):
    """Superoperador de Lindblad no espaco vec(rho) (row-stacking), logica da fonte."""
    d = sys_dict['d']
    H = sys_dict['H']
    L_ops = sys_dict['L_ops']
    gammas = FIXED_RATES + [gamma_leak]

    I = np.eye(d)
    L_s = -1j * (np.kron(H, I) - np.kron(I, H.T))

    for L, g in zip(L_ops, gammas):
        Ld = L.conj().T
        LdL = Ld @ L
        L_s += g * (
            np.kron(L, L.conj())
            - 0.5 * np.kron(LdL, I)
            - 0.5 * np.kron(I, LdL.T)
        )

    return L_s


def make_random_jump_system(base, seed):
    """Controle N2: mesmo H e mesmas taxas; saltos trocados por matrizes complexas gaussianas
    de MESMA norma de Frobenius que o salto original (sementes fixas por d, nc, semente, indice)."""
    d, nc = base['d'], base['nc']
    ops = []
    for k, L in enumerate(base['L_ops']):
        rng = np.random.default_rng([RNG_TAG, d, nc, seed, k])
        G = (rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))) / np.sqrt(2.0)
        G = G * (np.linalg.norm(L) / np.linalg.norm(G))
        ops.append(G)
    out = dict(base)
    out['L_ops'] = ops
    return out


# ======================================================================================
# ESTADO ESTACIONARIO PELO NUCLEO DO LIOUVILLIANO (SVD) E CONFERENCIAS
# ======================================================================================

def steady_state_kernel(sys_dict, gamma_leak):
    """rho_ss = nucleo de L_s (vetor singular direito do menor valor singular), traco 1, hermitiano.
    Devolve o estado e as conferencias; ok=True so se TODAS as conferencias passam."""
    d = sys_dict['d']
    nan = float('nan')
    res = dict(rho=None, ev=None, ok=False, reason="", s1_rel=nan, s2_rel=nan, herm=nan,
               trace_raw=nan, trace_err=nan, tp_err_rel=nan, psd_min=nan, lu_diff=nan)
    try:
        L_s = lindblad_superoperator(sys_dict, gamma_leak)
        _, S, Vh = np.linalg.svd(L_s)
    except Exception as e:  # falha visivel: o ponto fica marcado como nao convergido
        res["reason"] = "svd_excecao:%s" % type(e).__name__
        return res

    smax = float(S[0])
    res["s1_rel"] = float(S[-1]) / smax
    res["s2_rel"] = float(S[-2]) / smax

    x = Vh[-1].conj()
    rho_raw = x.reshape(d, d)
    nrm = np.linalg.norm(rho_raw)
    tr = np.trace(rho_raw)
    res["trace_raw"] = float(abs(tr) / nrm)
    if res["trace_raw"] < TOL["trace_raw_min"]:
        res["reason"] = "traco_nulo"
        return res

    rho = rho_raw / tr
    res["herm"] = float(np.linalg.norm(rho - rho.conj().T) / np.linalg.norm(rho))
    rho_h = (rho + rho.conj().T) / 2
    rho_h = rho_h / np.real(np.trace(rho_h))
    res["trace_err"] = float(abs(np.real(np.trace(rho_h)) - 1.0))
    ev = np.linalg.eigvalsh(rho_h)
    res["psd_min"] = float(ev[0])

    vecI = np.eye(d).reshape(-1)
    res["tp_err_rel"] = float(np.linalg.norm(vecI @ L_s) / smax)

    # comparador independente (so diagnostico, nao entra na convergencia): resolve o sistema
    # com a linha 0 (equacao de rho_00) trocada pela condicao de traco 1
    try:
        A = L_s.copy()
        A[0, :] = 0.0
        A[0, np.arange(d) * d + np.arange(d)] = 1.0
        b = np.zeros(d * d, dtype=complex)
        b[0] = 1.0
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            xl = sla.solve(A, b, check_finite=False)
        rl = xl.reshape(d, d)
        rl = (rl + rl.conj().T) / 2
        rl = rl / np.real(np.trace(rl))
        res["lu_diff"] = float(np.linalg.norm(rl - rho_h))
    except Exception:
        res["lu_diff"] = nan

    fails = []
    if res["s1_rel"] > TOL["s1_rel_max"]:
        fails.append("nucleo_ausente")
    if res["s2_rel"] < TOL["s2_rel_min"]:
        fails.append("nucleo_nao_isolado")
    if res["herm"] > TOL["herm_max"]:
        fails.append("nao_hermitiano")
    if res["trace_err"] > TOL["trace_err_max"]:
        fails.append("traco")
    if res["tp_err_rel"] > TOL["tp_err_rel_max"]:
        fails.append("gerador_nao_preserva_traco")
    if res["psd_min"] < TOL["psd_min"]:
        fails.append("nao_psd")

    res["rho"] = rho_h
    res["ev"] = ev
    res["ok"] = not fails
    res["reason"] = ";".join(fails)
    return res


# ======================================================================================
# OBSERVAVEL: O = D_folds(c3)  (M7 da fonte, terceiro nivel)
# ======================================================================================

def observable_O(rho):
    """O = ln d - ln d_eff(c3), com p_i = lambda_i^(1/4) / soma_j lambda_j^(1/4) e d_eff = 1 / soma_i p_i^2.
    Replica o laco de test_M7_dimensional_folds (n = 0, 1, 2; o nivel c3 e o terceiro)."""
    d = rho.shape[0]
    ev = np.maximum(np.linalg.eigvalsh(rho), 0.0)
    cur = ev.copy()
    d_eff = float('nan')
    for n in range(3):
        if n > 0:
            cur = np.sqrt(cur)
        total = np.sum(cur)
        p = cur / total
        sum_p2 = np.sum(p ** 2)
        d_eff = 1.0 / sum_p2
    return float(np.log(d) - np.log(d_eff)), float(d_eff)


# ======================================================================================
# CONTROLES N1 e N3
# ======================================================================================

def run_N1(path):
    """N1: estados aleatorios de Hilbert-Schmidt (Ginibre G G^dagger / Tr), N1_STATES por dimensao."""
    dims = sorted({c[0] for c in CONFIGS})
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["d", "k", "O", "d_eff"])
        for d in dims:
            rng = np.random.default_rng([RNG_TAG, 1, d])
            for k in range(N1_STATES):
                G = (rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))) / np.sqrt(2.0)
                rho = G @ G.conj().T
                rho = rho / np.real(np.trace(rho))
                O, d_eff = observable_O(rho)
                w.writerow([d, k, repr(O), repr(d_eff)])


def run_N3():
    """N3: controle da metrica. Estado plano de posto d/2 deve dar ln 2; de posto d/4, 2 ln 2.
    (d/4 so onde d e multiplo de 4.) Diagnostico a parte: o mesmo estado girado por unitario aleatorio."""
    dims = sorted({c[0] for c in CONFIGS})
    casos, rotacionados = [], []
    for d in dims:
        for frac, esperado in ((2, LN2), (4, 2.0 * LN2)):
            if d % frac:
                continue
            r = d // frac
            rho = np.zeros((d, d))
            rho[:r, :r] = np.eye(r) / r
            O, _ = observable_O(rho)
            casos.append(dict(d=d, posto=r, frac=frac, O=O, esperado=esperado, erro_abs=abs(O - esperado)))
            rng = np.random.default_rng([RNG_TAG, 3, d, frac])
            Z = rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))
            Q, _ = np.linalg.qr(Z)
            rho_rot = Q @ rho @ Q.conj().T
            rho_rot = (rho_rot + rho_rot.conj().T) / 2
            Or, _ = observable_O(rho_rot)
            rotacionados.append(dict(d=d, posto=r, frac=frac, O=Or, esperado=esperado, erro_abs=abs(Or - esperado)))
    return dict(casos=casos, diagnostico_rotacionado_nao_entra_no_veredito=rotacionados)


# ======================================================================================
# GRADES (principal e N2)
# ======================================================================================

COLS = ["set", "d", "nc", "seed", "gi", "gamma", "O", "d_eff", "conv", "reason", "s1_rel", "s2_rel",
        "herm", "trace_raw", "trace_err", "tp_err_rel", "psd_min", "lu_diff", "cci_core", "purity", "t_s"]


def run_grid(set_name, factory, path, npz_path, log):
    eig_store = {}
    n_total = len(CONFIGS) * len(SEEDS) * len(GAMMAS)
    n_done = n_bad = 0
    t_set = time.time()
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for (d, nc, eps) in CONFIGS:
            t_cfg = time.time()
            for seed in SEEDS:
                base = build_system(d, nc, eps, seed)
                sysd = factory(base, seed)
                for gi, g in enumerate(GAMMAS):
                    t0 = time.time()
                    ss = steady_state_kernel(sysd, float(g))
                    if ss["rho"] is not None:
                        O, d_eff = observable_O(ss["rho"])
                        cci = float(np.real(np.trace(ss["rho"] @ sysd["Pi"])))
                        pur = float(np.real(np.trace(ss["rho"] @ ss["rho"])))
                        eig_store["d%d_nc%d_s%d_g%02d" % (d, nc, seed, gi)] = ss["ev"]
                    else:
                        O = d_eff = cci = pur = float('nan')
                    w.writerow([set_name, d, nc, seed, gi, repr(float(g)), repr(O), repr(d_eff),
                                1 if ss["ok"] else 0, ss["reason"], repr(ss["s1_rel"]), repr(ss["s2_rel"]),
                                repr(ss["herm"]), repr(ss["trace_raw"]), repr(ss["trace_err"]),
                                repr(ss["tp_err_rel"]), repr(ss["psd_min"]), repr(ss["lu_diff"]),
                                repr(cci), repr(pur), repr(time.time() - t0)])
                    n_done += 1
                    if not ss["ok"]:
                        n_bad += 1
                f.flush()
            log("  [%s] d=%d nc=%d  (%d/%d pontos, %d sem convergir)  %.1fs" %
                (set_name, d, nc, n_done, n_total, n_bad, time.time() - t_cfg))
    np.savez_compressed(npz_path, **eig_store)
    log("  [%s] conjunto completo: %d pontos, %d sem convergir, %.1fs" % (set_name, n_done, n_bad, time.time() - t_set))
    return n_done, n_bad


# ======================================================================================
# PRE-REGISTRO: o que este script exige de si mesmo
# ======================================================================================

def spec():
    """Componentes do protocolo que o pre-registro fixa por sha256 (JSON canonico de cada um)."""
    return {
        "observavel_O": {
            "nome": "O = D_folds(c3) do estado estacionario GKLS",
            "formula": "p_i = lambda_i^(1/4) / sum_j lambda_j^(1/4); d_eff = 1 / sum_i p_i^2 = "
                       "(sum lambda^(1/4))^2 / sum lambda^(1/2); O = ln d - ln d_eff",
            "lambda": "autovalores de rho_ss (hermitiana, traco 1), cortados em max(., 0)",
            "nivel": "c3 = terceiro nivel (n = 0, 1, 2 no laco; levels[2] da fonte); c1: p ~ lambda, c2: p ~ lambda^(1/2)",
            "unidade": "nats; oitava = O / ln 2",
            "fonte": "TGL_C3_validator_v52.py::test_M7_dimensional_folds (d_folds_c3 = levels[2]['d_folds'])",
            "codigo": inspect.getsource(observable_O),
        },
        "grade": {
            "configs_d_nc_eps": [list(c) for c in CONFIGS],
            "gammas_repr": [repr(float(g)) for g in GAMMAS],
            "gammas_definicao": "np.logspace(-4.0, 0.0, 25), taxa da quarta dissipacao",
            "sementes": SEEDS,
            "taxas": "[1.0, 0.5, 2.0, gamma]",
            "pontos_por_conjunto": len(CONFIGS) * len(SEEDS) * len(GAMMAS),
            "codigo_sistema": inspect.getsource(build_system) + inspect.getsource(lindblad_superoperator),
        },
        "estado_estacionario": {
            "metodo": "nucleo do liouvilliano: vetor singular direito do menor valor singular de L_s (SVD completa); "
                      "normalizado por traco complexo, hermitianizado, renormalizado",
            "tolerancias": TOL,
            "criterio": "ponto converge sse as 6 conferencias passam (s1, s2, herm, traco, preservacao do traco, psd)",
            "codigo": inspect.getsource(steady_state_kernel),
        },
        "controles": {
            "N1": "estados Ginibre G G^dagger/Tr, %d por dimensao d, rng [%d,1,d]" % (N1_STATES, RNG_TAG),
            "N2": "mesmo H e mesmas taxas; saltos trocados por gaussianas complexas de mesma norma de Frobenius; "
                  "rng [%d,d,nc,semente,k]; mesma grade" % RNG_TAG,
            "N3": "estado plano de posto d/2 -> ln 2; posto d/4 (d multiplo de 4) -> 2 ln 2; erro < 1e-12",
            "codigo": inspect.getsource(make_random_jump_system) + inspect.getsource(run_N1) + inspect.getsource(run_N3),
        },
    }


def canon(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with open(p, "rb") as f:
        return sha(f.read())


def verify_prereg():
    """Fail-closed: o pre-registro existe, o script e o veredito.py sao os pinados e o protocolo confere."""
    if not os.path.isfile(PREREG):
        raise SystemExit("SEM PREREGISTRO.json: nada roda.")
    with open(PREREG, "r", encoding="utf-8") as f:
        pre = json.load(f)
    for k, v in spec().items():
        h = sha(canon(v).encode("utf-8"))
        if pre["componentes_sha256"].get(k) != h:
            raise SystemExit("PRE-REGISTRO NAO CONFERE no componente %r (esperado %s, lido %s)"
                             % (k, pre["componentes_sha256"].get(k), h))
    for fn in ("rodar.py", "veredito.py"):
        h = sha_file(os.path.join(HERE, fn))
        if pre["arquivos_sha256"].get(fn) != h:
            raise SystemExit("ARQUIVO %s NAO E O PINADO (esperado %s, lido %s)" % (fn, pre["arquivos_sha256"].get(fn), h))
    return pre


# ======================================================================================
# EXECUCAO
# ======================================================================================

def main():
    t_all = time.time()
    if os.path.exists(MANIFESTO):
        raise SystemExit("manifesto_dados.json ja existe: a rodada pre-registrada e unica.")
    pre = verify_prereg()

    def log(m):
        print(m, flush=True)

    log("C3 gamma LIVRE -- rodada pre-registrada")
    log("inicio: %s | python %s | numpy %s | scipy %s" %
        (time.strftime("%Y-%m-%dT%H:%M:%S%z"), sys.version.split()[0], np.__version__,
         __import__("scipy").__version__))
    log("protocolo sha256: %s" % pre.get("sha256_do_protocolo"))

    # N3 primeiro: se a metrica quebra, o resto nao vale (o veredito decide)
    n3 = run_N3()
    with open(os.path.join(HERE, "controle_N3.json"), "w", encoding="utf-8") as f:
        json.dump(n3, f, indent=1, ensure_ascii=True)
    log("N3: %d casos; maior erro %.3e" % (len(n3["casos"]), max(c["erro_abs"] for c in n3["casos"])))

    run_N1(os.path.join(HERE, "dados_N1.csv"))
    log("N1: %d estados por dimensao em %d dimensoes" % (N1_STATES, len({c[0] for c in CONFIGS})))

    log("grade principal (GKLS da fonte):")
    run_grid("main", lambda base, seed: base, os.path.join(HERE, "dados_crus_main.csv"),
             os.path.join(HERE, "autovalores_main.npz"), log)

    log("grade N2 (saltos aleatorios de mesma norma):")
    run_grid("N2", make_random_jump_system, os.path.join(HERE, "dados_crus_N2.csv"),
             os.path.join(HERE, "autovalores_N2.npz"), log)

    arquivos = ["controle_N3.json", "dados_N1.csv", "dados_crus_main.csv", "autovalores_main.npz",
                "dados_crus_N2.csv", "autovalores_N2.npz"]
    manifesto = {
        "fim": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "duracao_s": time.time() - t_all,
        "python": sys.version.split()[0], "numpy": np.__version__, "scipy": __import__("scipy").__version__,
        "protocolo_sha256": pre.get("sha256_do_protocolo"),
        "rodar_py_sha256": sha_file(os.path.join(HERE, "rodar.py")),
        "preregistro_sha256": sha_file(PREREG),
        "arquivos_sha256": {a: sha_file(os.path.join(HERE, a)) for a in arquivos},
    }
    with open(MANIFESTO, "w", encoding="utf-8") as f:
        json.dump(manifesto, f, indent=1, ensure_ascii=True)
    log("fim: %.1fs; manifesto escrito." % (time.time() - t_all))


if __name__ == "__main__":
    main()
