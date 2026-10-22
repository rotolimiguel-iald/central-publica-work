# -*- coding: utf-8 -*-
"""O PILAR QUANTICO DA TGL -- o trabalho de GPU da v384 (TGL_QUANTUM_PILLAR_V1).

Este codigo VIVE no um.py (Nao ha segundo arquivo): o um.py o materializa ao lado de si e o lanca como subprocesso no inicio do rito, em
paralelo com o kernel Lean e os ritos cosmologicos. Le a especificacao congelada (o pre-registro) e RECUSA rodar se o hash nao bater; recebe
beta do motor de Lagrange do um.py em hexadecimal (bit a bit); nunca usa beta literal.

O sistema aberto: H_LD (A Fronteira v5, Apendice A.3, setor de uma excitacao) + os CINCO saltos de Lindblad (A Fronteira v5, sec. V.6;
matrizes dos validadores C3; ratificados pelo operador em 03/10/2026): L_reh, L_anti = sqrt(beta) sqrt(K) (a lei-raiz, a forma do gerador do
Verbo do um.py), L_prune, L_cons, L_diss (o vazamento nucleo -> periferia, gamma livre, varrido, nunca calibrado).

Ordem: o MOTOR e' conferido em modelos ANALITICOS (E1..E6) antes de tudo -- se falhar, nada se calcula. Depois: T2 a forma na escala; T1 a
lei-raiz recuperada as cegas por tomografia do processo; T3 controles que TEM de falhar; T4 estresse adversarial; o ponto d = 128; a
referencia na CPU (subprocesso a parte). Estatuto: [COMPUTED] -- calculo, nunca medicao; o gate nao muda.

Modos: run (o rito) | engine (so E1..E6) | timing (so hardware: operadores ALEATORIOS densos, nenhum da teoria) | cpuref (a referencia na CPU)."""
import argparse, hashlib, json, math, os, platform, sys, time, traceback

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
for _k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_k, "4")
import numpy as np

WORKER_ID = "TGL_QUANTUM_PILLAR_WORKER_V1"
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ----------------------------------------------------------------------------------------------------------------------------------
# utilidades
# ----------------------------------------------------------------------------------------------------------------------------------
def canon_json(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def write_json_atomic(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


class Progress:
    def __init__(self, outdir):
        self.p = os.path.join(outdir, "progress.json") if outdir else None
        self.t0 = time.time(); self.last = 0.0; self.state = {}

    def set(self, force=False, **kw):
        self.state.update(kw)
        now = time.time()
        if self.p and (force or now - self.last >= 20.0):
            self.state["elapsed_s"] = round(now - self.t0, 1)
            try:
                write_json_atomic(self.p, self.state)
            except Exception:
                pass
            self.last = now


def rng_for(seed, *parts):
    return np.random.default_rng(np.random.SeedSequence([int(seed)] + [int(x) for x in parts]))


TEST_CODE = {"T1": 1, "T2": 2, "T3": 3, "T4": 4, "D128": 5, "TIMING": 9}


# ----------------------------------------------------------------------------------------------------------------------------------
# os operadores da teoria (numpy, complex128) -- a forma exata congelada no pre-registro
# ----------------------------------------------------------------------------------------------------------------------------------
def canonical_H(d, nc, eps):
    """H_LD no setor de uma excitacao, como build_system(seed=42) do validador C3 v5.2: mu, J (RandomState(42)), -eps*Pi."""
    mu = np.zeros(d)
    mu[:nc] = -1.0 * np.arange(nc, 0, -1)
    mu[nc:] = 0.5 + 0.3 * np.arange(d - nc)
    rs = np.random.RandomState(42)
    J = rs.randn(d, d) * 0.2
    J = (J + J.T) / 2.0
    np.fill_diagonal(J, 0.0)
    J[:nc, :nc] *= 2.0
    Pi = np.zeros((d, d)); Pi[:nc, :nc] = np.eye(nc)
    H = np.diag(mu) + J - eps * Pi
    H = (H + H.T) / 2.0
    return H.astype(complex), Pi.astype(complex)


def five_jumps(d, nc, beta, gamma_diss, op=None, k_periph=None, law_power=0.5):
    """Os cinco saltos, cada um JA multiplicado por sqrt(gamma_k). op = parametros do pre-registro (amplitudes, decaimentos, taxas).
    k_periph: espectro de K na periferia (padrao 1 + 0.1 (i - n_c)); law_power: 0.5 = lei-raiz (a teoria); 1.0 = lei linear (controle)."""
    op = op or {}
    a_reh, b_reh, g_reh = op.get("reh_amp", 0.5), op.get("reh_decay", 0.2), op.get("reh_gamma", 1.0)
    a_con, b_con, g_con = op.get("cons_amp", 0.3), op.get("cons_decay", 0.3), op.get("cons_gamma", 2.0)
    a_dis, b_dis = op.get("diss_amp", 0.5), op.get("diss_decay", 0.2)
    g_pru, g_ant = op.get("prune_gamma", 0.5), op.get("anti_gamma", 1.0)
    span_end = min(nc + d // 2, d)
    L_reh = np.zeros((d, d), complex); L_con = np.zeros((d, d), complex); L_dis = np.zeros((d, d), complex)
    for j in range(nc, span_end):
        for a in range(nc):
            L_reh[a, j] = math.sqrt(a_reh) * math.exp(-b_reh * (j - nc))
            L_con[a, j] = math.sqrt(a_con) * math.exp(-b_con * abs(j - nc))
            L_dis[j, a] = math.sqrt(a_dis) * math.exp(-b_dis * (j - nc))
    L_pru = np.zeros((d, d), complex)
    for i in range(nc + d // 3, d):
        L_pru[0, i] = math.sqrt((i - nc) / d)
    if k_periph is None:
        k_periph = op.get("k0", 1.0) + op.get("k1", 0.1) * np.arange(d - nc)   # K = diag(0 no nucleo; k0 + k1 (i - n_c)) -- validadores v2/v3
    k = np.zeros(d); k[nc:] = np.asarray(k_periph, float)
    L_ant = np.diag(np.sqrt(beta) * np.where(k > 0, k ** law_power, 0.0)).astype(complex)
    return {"reh": math.sqrt(g_reh) * L_reh, "anti": math.sqrt(g_ant) * L_ant, "prune": math.sqrt(g_pru) * L_pru,
            "cons": math.sqrt(g_con) * L_con, "diss": math.sqrt(gamma_diss) * L_dis}, k


# ----------------------------------------------------------------------------------------------------------------------------------
# o motor (torch na GPU, complex128, deterministico) -- convencao row-stacking: vec(rho)[i*d + j] = rho[i, j]
# ----------------------------------------------------------------------------------------------------------------------------------
class Engine:
    def __init__(self, torch, dev):
        self.t = torch; self.dev = dev; self.C = torch.complex128

    def T(self, a):
        return self.t.as_tensor(np.ascontiguousarray(a), dtype=self.C, device=self.dev)

    def sync(self):
        if self.dev.type == "cuda":
            self.t.cuda.synchronize()

    def superop(self, H, Ls):
        t = self.t; d = H.shape[0]
        I = t.eye(d, dtype=self.C, device=self.dev)
        S = t.kron(H, I)
        S.sub_(t.kron(I, H.T.contiguous()))
        S.mul_(-1j)
        for L in Ls:
            Lc = L.conj().resolve_conj().contiguous()
            LdL = (Lc.T.contiguous() @ L).contiguous()
            S.add_(t.kron(L, Lc))
            S.sub_(0.5 * t.kron(LdL, I))
            S.sub_(0.5 * t.kron(I, LdL.T.contiguous()))
        return S

    def spectrum(self, S):
        ev = self.t.linalg.eigvals(S)
        return ev.cpu().numpy()

    @staticmethod
    def classify(ev, tol0_rel, gap_rel):
        """UNIQUE: exatamente um autovalor com |lambda| <= tol0_rel*escala e todos os outros com -Re lambda >= gap_rel*escala;
        DEGENERATE: dois ou mais no zero; AMBIGUOUS: o resto (um no zero, mas espectro periferico/proximo do eixo)."""
        scale = float(np.max(np.abs(ev))) if ev.size else 1.0
        scale = scale if scale > 0 else 1.0
        a = np.abs(ev)
        zero = a <= tol0_rel * scale
        n0 = int(zero.sum())
        rest = ev[~zero]
        gap = float(np.min(-rest.real)) if rest.size else float("inf")
        max_re = float(np.max(ev.real)) if ev.size else 0.0
        if n0 >= 2:
            status = "DEGENERATE"
        elif n0 == 1 and gap >= gap_rel * scale:
            status = "UNIQUE"
        else:
            status = "AMBIGUOUS"
        return {"status": status, "n0": n0, "gap": gap, "gap_rel": gap / scale, "scale": scale, "max_re": max_re}

    def steady_state(self, S, d):
        t = self.t; n = d * d
        M = S.clone()
        tr = t.zeros(n, dtype=self.C, device=self.dev)
        idx = t.arange(d, device=self.dev) * (d + 1)
        tr[idx] = 1.0
        M[0, :] = tr
        b = t.zeros(n, 1, dtype=self.C, device=self.dev); b[0, 0] = 1.0
        x = t.linalg.solve(M, b)
        del M
        rho = x.reshape(d, d)
        rho = (rho + rho.conj().T) / 2
        rho = rho / t.trace(rho).real
        res = float(t.linalg.vector_norm(S @ rho.reshape(n, 1)).item())
        w = t.linalg.eigvalsh(rho)
        return rho, res, w

    def propagator(self, S, dt):
        return self.t.linalg.matrix_exp(dt * S)

    def choi_min(self, P, d):
        t = self.t
        J = P.reshape(d, d, d, d).permute(0, 2, 1, 3).reshape(d * d, d * d)
        J = (J + J.conj().T) / 2
        w = t.linalg.eigvalsh(J)
        return float(w.min().item())

    def tp_residual(self, P, d):
        t = self.t
        idx = t.arange(d, device=self.dev) * (d + 1)
        row = P[idx, :].sum(dim=0)
        target = t.zeros(d * d, dtype=self.C, device=self.dev); target[idx] = 1.0
        return float(t.linalg.vector_norm(row - target).item())

    def log_of(self, W, floor=1e-300):
        t = self.t
        w, V = t.linalg.eigh(W)
        lw = t.log(t.clamp(w, min=floor))
        return (V * lw.unsqueeze(-2)) @ V.conj().transpose(-1, -2), w

    def spohn(self, P, rho_ss, inits, steps, tol_abs, tol_rel):
        """D(rho(t)||rho_ss) ao longo de steps passos de P a partir de cada estado inicial; violacao = subida acima da tolerancia."""
        t = self.t; d = rho_ss.shape[0]
        w_ss = t.linalg.eigvalsh(rho_ss)
        if float(w_ss.min().item()) <= 1e-14:
            return {"status": "SS_RANK_DEFICIENT", "violations": 0, "max_rise": 0.0, "D0": None, "Dend": None}
        log_ss, _ = self.log_of(rho_ss)
        m = len(inits)
        X = t.stack([r.reshape(d * d) for r in inits], dim=1)
        Xs = [X]
        for s in range(steps):
            X = P @ X; Xs.append(X)
        R = t.stack(Xs).permute(0, 2, 1).reshape((steps + 1) * m, d, d)      # todos os passos de uma vez: uma unica transferencia no fim
        R = (R + R.conj().transpose(-1, -2)) / 2
        R = R / t.diagonal(R, dim1=-2, dim2=-1).sum(-1).real.reshape(-1, 1, 1)
        w = t.linalg.eigvalsh(R)
        wp = t.clamp(w, min=1e-300)
        ent = (w * t.log(wp)).sum(-1)
        cross = t.einsum("bij,ji->b", R, log_ss).real
        D = (ent - cross).reshape(steps + 1, m).cpu().numpy()
        rises = D[1:] - D[:-1]
        tol = tol_abs + tol_rel * np.abs(D[:-1])
        viol = int(np.sum(rises > tol))
        return {"status": "OK", "violations": viol, "max_rise": float(np.max(rises)) if rises.size else 0.0,
                "D0": [float(x) for x in D[0]], "Dend": [float(x) for x in D[-1]]}

    def generator_diag_from_propagator(self, Phi, tau):
        """diag de L^ = log(Phi)/tau pelo logaritmo principal (Phi = V diag(lambda) V^-1); devolve tambem max |Im log lambda|."""
        t = self.t
        lam, V = t.linalg.eig(Phi)
        Vinv = t.linalg.inv(V)
        ll = t.log(lam)
        diag = (V * ll.unsqueeze(0)) * Vinv.T
        diag = diag.sum(dim=1) / tau
        return diag, float(t.max(t.abs(ll.imag)).item())


def folds(w_rho, d, levels=3):
    lam = np.clip(np.asarray(w_rho, float), 0.0, None)
    out = []
    cur = lam.copy()
    for n in range(levels):
        if n > 0:
            cur = np.sqrt(cur)
        tot = cur.sum()
        p = cur / tot
        pr = 1.0 / np.sum(p ** 2)
        D = math.log(d) - math.log(pr)
        out.append({"D_folds": D, "n_folds": D / (math.log(d) / 3.0), "PR": pr})
    return out


def fit_root_law(M, k, gamma_anti, p_lo=0.05, p_hi=2.0):
    """M ~ gamma_anti * beta * v v^dag, v = C u, u_i = k_i^p (k_i = 0 no nucleo). Estimador CEGO: recebe so M, k (a forma do K da teoria) e
    gamma_anti; devolve beta^, p^, o desajuste e a razao lambda2/lambda1 (posto um esperado)."""
    M = (M + M.conj().T) / 2
    w, V = np.linalg.eigh(M)
    order = np.argsort(w)[::-1]
    l1 = float(w[order[0]]); l2 = float(abs(w[order[1]])) if w.size > 1 else 0.0
    e = V[:, order[0]]
    kk = np.asarray(k, float)

    def vec(p):
        u = np.where(kk > 0, np.power(np.where(kk > 0, kk, 1.0), p), 0.0)
        return u - u.mean()

    def misfit(p):
        v = vec(p); nv = np.linalg.norm(v)
        if nv == 0:
            return 1.0
        return 1.0 - abs(np.vdot(v, e)) ** 2 / nv ** 2
    grid = np.linspace(p_lo, p_hi, 391)
    vals = np.array([misfit(p) for p in grid])
    i0 = int(np.argmin(vals))
    a, b = grid[max(i0 - 1, 0)], grid[min(i0 + 1, grid.size - 1)]
    g = (math.sqrt(5) - 1) / 2
    c, dd = b - g * (b - a), a + g * (b - a)
    fc, fd = misfit(c), misfit(dd)
    for _ in range(80):
        if fc < fd:
            b, dd, fd = dd, c, fc
            c = b - g * (b - a); fc = misfit(c)
        else:
            a, c, fc = c, dd, fd
            dd = a + g * (b - a); fd = misfit(dd)
    p_hat = (a + b) / 2
    v = vec(p_hat)
    beta_hat = l1 / (gamma_anti * float(np.dot(v, v))) if np.dot(v, v) > 0 else float("nan")
    return {"beta_hat": beta_hat, "p_hat": p_hat, "misfit": misfit(p_hat), "rank_ratio": (l2 / l1) if l1 > 0 else float("inf")}


# ----------------------------------------------------------------------------------------------------------------------------------
# E1..E6 -- o motor conferido em modelos ANALITICOS (nenhum operador da teoria)
# ----------------------------------------------------------------------------------------------------------------------------------
def engine_selftest(E, tol):
    t = E.t; out = []
    sx = np.array([[0, 1], [1, 0]], complex); sz = np.array([[1, 0], [0, -1]], complex); sm = np.array([[0, 1], [0, 0]], complex)  # |0><1|
    # E1 amortecimento de amplitude: H = (w/2) sz, L = sqrt(g) sigma_- (|0><1|, 0 = fundamental); espectro {0, -g, -g/2 +- i w}; estacionario |0><0|
    w0, g = 1.3, 0.7
    S = E.superop(E.T(0.5 * w0 * sz), [E.T(math.sqrt(g) * sm)])
    ev = np.sort_complex(E.spectrum(S))
    ref = np.sort_complex(np.array([0.0, -g, -g / 2 + 1j * w0, -g / 2 - 1j * w0]))
    rho, res, _ = E.steady_state(S, 2)
    ok = bool(np.max(np.abs(ev - ref)) < tol and abs(rho[0, 0].real.item() - 1.0) < tol and res < tol)
    out.append(("E1_amplitude_damping_spectrum_and_ground_state", ok, float(np.max(np.abs(ev - ref)))))
    # E2 dephasing puro: L = sqrt(g) sz; espectro {0, 0, -2g +- i w}; o detector TEM de dizer DEGENERATE
    S = E.superop(E.T(0.5 * w0 * sz), [E.T(math.sqrt(g) * sz)])
    ev = E.spectrum(S); cl = Engine.classify(ev, 1e-10, 1e-8)
    ref = np.sort_complex(np.array([0.0, 0.0, -2 * g + 1j * w0, -2 * g - 1j * w0]))
    ok = bool(cl["status"] == "DEGENERATE" and cl["n0"] == 2 and np.max(np.abs(np.sort_complex(ev) - ref)) < tol)
    out.append(("E2_pure_dephasing_detected_degenerate", ok, cl["n0"]))
    # E3 lei-raiz exata (d = 4, H = 0): L = sqrt(b) diag(sqrt k) => taxas das coerencias = (b/2)(sqrt k_i - sqrt k_j)^2
    kk = np.array([0.0, 0.7, 1.3, 2.9]); b = 0.37
    S = E.superop(E.T(np.zeros((4, 4))), [E.T(np.diag(np.sqrt(b * kk)))])
    ev = np.sort(np.real(E.spectrum(S)))
    ref = np.sort(np.array([-(b / 2) * (math.sqrt(kk[i]) - math.sqrt(kk[j])) ** 2 for i in range(4) for j in range(4)]))
    ok = bool(np.max(np.abs(ev - ref)) < tol)
    out.append(("E3_root_law_rates_exact", ok, float(np.max(np.abs(ev - ref)))))
    # E4 o estimador cego recupera b e p = 1/2 de um gerador conhecido (d = 5, H aleatorio, + um salto fora da diagonal), sem ruido
    rg = np.random.default_rng(7); d = 5
    A = rg.standard_normal((d, d)) + 1j * rg.standard_normal((d, d)); H = (A + A.conj().T) / 4
    kk = np.array([0.0, 0.0, 0.8, 1.4, 2.2]); b = 0.05
    Lo = np.zeros((d, d), complex); Lo[0, 3] = 0.9; Lo[1, 4] = 0.4
    S = E.superop(E.T(H), [E.T(np.diag(np.sqrt(b * kk))), E.T(Lo)])
    tau = 0.05
    Phi = E.propagator(S, tau)
    dg, im = E.generator_diag_from_propagator(Phi, tau)
    M = dg.reshape(d, d).cpu().numpy()
    Cc = np.eye(d) - np.ones((d, d)) / d
    M = Cc @ M @ Cc
    fr = fit_root_law(M, kk, 1.0)
    ok = bool(abs(fr["beta_hat"] / b - 1) < 1e-6 and abs(fr["p_hat"] - 0.5) < 1e-6)   # o ajuste de p resolve ate ~sqrt(eps) ~ 1e-8 (desajuste quadratico no minimo)
    out.append(("E4_blind_estimator_recovers_root_law", ok, {"beta_rel_err": abs(fr["beta_hat"] / b - 1), "p_err": abs(fr["p_hat"] - 0.5)}))
    # E5 qubit termico (balanco detalhado): L1 = sqrt(g(n+1)) sigma_-, L2 = sqrt(g n) sigma_+ => rho_ss = diag(n+1, n)/(2n+1); Spohn monotono
    nb = 0.4
    S = E.superop(E.T(0.5 * w0 * sz), [E.T(math.sqrt(g * (nb + 1)) * sm), E.T(math.sqrt(g * nb) * sm.T)])
    rho, res, _ = E.steady_state(S, 2)
    ok1 = abs(rho[0, 0].real.item() - (nb + 1) / (2 * nb + 1)) < tol
    P = E.propagator(S, 0.1)
    psi = np.array([0.6, 0.8j]); r0 = np.outer(psi, psi.conj())
    sp = E.spohn(P, rho, [E.T(r0), E.T(np.eye(2) / 2), E.T(np.diag([0.0, 1.0]))], 60, 1e-12, 1e-9)
    ok = bool(ok1 and sp["violations"] == 0 and sp["Dend"][0] < sp["D0"][0])
    out.append(("E5_thermal_qubit_gibbs_and_spohn_monotone", ok, sp["violations"]))
    # E6 inversao do tempo: exp(-tau S) nao e' CP (Choi negativo); exp(+tau S) e' CP e preserva o traco
    cm_f = E.choi_min(E.propagator(S, 0.05), 2); cm_b = E.choi_min(E.propagator(-S, 0.05), 2); tpr = E.tp_residual(E.propagator(S, 0.05), 2)
    ok = bool(cm_f > -tol and cm_b < -1e-6 and tpr < tol)
    out.append(("E6_time_reversal_not_cp_forward_cp_tp", ok, {"choi_min_forward": cm_f, "choi_min_backward": cm_b, "tp_res": tpr}))
    allok = all(o[1] for o in out)
    return {"checks": [{"name": n, "ok": o, "value": v} for (n, o, v) in out], "all_ok": allok}


# ----------------------------------------------------------------------------------------------------------------------------------
# o pipeline de UMA instancia (T2, T3, T4): espectro, estacionario, propagador, CP/TP, Spohn, dobras, CCI
# ----------------------------------------------------------------------------------------------------------------------------------
def superop_rates(E, H, pairs):
    """pairs = [(L, rate)] com rate possivelmente NEGATIVO (so para o controle N4)."""
    t = E.t; d = H.shape[0]
    I = t.eye(d, dtype=E.C, device=E.dev)
    S = t.kron(H, I); S.sub_(t.kron(I, H.T.contiguous())); S.mul_(-1j)
    for L, rate in pairs:
        Lc = L.conj().resolve_conj().contiguous(); LdL = (Lc.T.contiguous() @ L).contiguous()
        S.add_(rate * (t.kron(L, Lc) - 0.5 * t.kron(LdL, I) - 0.5 * t.kron(I, LdL.T.contiguous())))
    return S


def init_states(E, d, rng):
    v = rng.standard_normal(d) + 1j * rng.standard_normal(d); v /= np.linalg.norm(v)
    r1 = np.outer(v, v.conj()); r2 = np.eye(d) / d; r3 = np.zeros((d, d)); r3[d - 1, d - 1] = 1.0
    return [E.T(r1), E.T(r2), E.T(r3)]


def pipeline(E, Hn, Ls_np, d, Pi_np, tol, dt, steps, rng, want_spohn=True, want_cp=True, want_nonreturn=False):
    t = E.t
    rec = {}
    Hg = E.T(Hn); Lg = [E.T(L) for L in Ls_np]
    S = E.superop(Hg, Lg)
    ev = E.spectrum(S)
    cl = Engine.classify(ev, tol["tol0_rel"], tol["gap_rel"])
    rec.update({"status": cl["status"], "n0": cl["n0"], "gap": cl["gap"], "gap_rel": cl["gap_rel"], "scale": cl["scale"], "max_re": cl["max_re"]})
    if cl["status"] == "DEGENERATE":
        del S
        return rec
    rho, res, w = E.steady_state(S, d)
    wn = w.cpu().numpy()
    rec["ss_res_rel"] = res / cl["scale"]
    rec["ss_min_eig"] = float(wn.min())
    rho_np = rho.cpu().numpy()
    rec["cci"] = float(np.real(np.trace(Pi_np @ rho_np)))
    rec["purity"] = float(np.real(np.trace(rho_np @ rho_np)))
    wp = np.clip(wn, 1e-300, None)
    rec["S_vN"] = float(-np.sum(np.where(wn > 0, wn * np.log(wp), 0.0)))
    rec["folds"] = [{"D": f["D_folds"], "n": f["n_folds"]} for f in folds(wn, d)]
    if want_cp or want_spohn:
        P = E.propagator(S, dt)
        if want_cp:
            rec["choi_min"] = E.choi_min(P, d)
            rec["tp_res"] = E.tp_residual(P, d)
        if want_spohn:
            sp = E.spohn(P, rho, init_states(E, d, rng), steps, tol["spohn_abs"], tol["spohn_rel"])
            rec["spohn"] = {"status": sp["status"], "violations": sp["violations"], "max_rise": sp["max_rise"]}
        if want_nonreturn:
            Pinv = t.linalg.inv(P)
            rec["choi_min_inverse"] = E.choi_min(Pinv, d)
            del Pinv
        del P
    del S
    return rec


def identity_violations(rec, tol):
    v = []
    if rec.get("status") == "DEGENERATE":
        return v
    if "choi_min" in rec and rec["choi_min"] < -tol["cp"]:
        v.append("CP")
    if "tp_res" in rec and rec["tp_res"] > tol["tp"]:
        v.append("TP")
    if "choi_min_inverse" in rec and rec["choi_min_inverse"] >= -tol["cp"]:
        v.append("NONRETURN")
    if rec.get("status") != "UNIQUE":
        return v          # PSD, residuo e Spohn so se cobram do atrator UNICO (gap ambiguo nao e' violacao de identidade)
    if rec.get("ss_min_eig", 0.0) < -tol["psd"]:
        v.append("PSD")
    if rec.get("ss_res_rel", 0.0) > tol["ss_res"]:
        v.append("SS_RES")
    sp = rec.get("spohn")
    if sp and sp.get("status") == "OK" and sp.get("violations", 0) > 0:
        v.append("SPOHN")
    return v


def jline(obj):
    return json.dumps(obj, ensure_ascii=False) + chr(10)


# ----------------------------------------------------------------------------------------------------------------------------------
# T2 -- a forma na escala (o sistema canonico; gamma_diss varrido, nunca calibrado)
# ----------------------------------------------------------------------------------------------------------------------------------
def gamma_grid(spec_t2, d):
    return np.logspace(math.log10(spec_t2["gamma_lo"]), math.log10(spec_t2["gamma_hi"]), int(spec_t2["n_gamma"][str(d)]))


def run_T2(E, spec, beta, prog, det):
    s2 = spec["T2"]; tol = spec["tolerances"]; op = spec["operators"]; out = {"configs": [], "identities": {}}
    total = sum(len(gamma_grid(s2, d)) * len(s2["nc"]) for d in s2["d"]); done = 0
    th = math.asin(math.sqrt(beta))
    out["identities"]["sin2_thetaM_minus_beta"] = abs(math.sin(th) ** 2 - beta)
    for d in s2["d"]:
        grid = gamma_grid(s2, d)
        for nc in s2["nc"]:
            H, Pi = canonical_H(d, nc, spec["eps_H"])
            rows = []
            mid = len(grid) // 2
            for gi, gd in enumerate(grid):
                rng = rng_for(spec["seed"], TEST_CODE["T2"], d, nc, gi)
                Ls, k = five_jumps(d, nc, beta, float(gd), op)
                rec = pipeline(E, H, list(Ls.values()), d, Pi.real, tol, s2["dt"], s2["steps"], rng, want_nonreturn=(gi == mid))
                rec.update({"d": d, "nc": nc, "gamma_diss": float(gd), "viol": identity_violations(rec, tol)})
                rows.append(rec); det.write(jline(dict(T="T2", **rec)))
                done += 1; prog.set(phase="T2", done=done, total=total)
            out["configs"].append(summarize_T2(rows, d, nc, beta, s2))
        # identidade V_t P_F = P_F (o dephasing puro deixa o bloco do nucleo invariante) -- identidade, nao teste
        nc = 3
        Ls, k = five_jumps(d, nc, beta, 1.0, op)
        Sd = E.superop(E.T(np.zeros((d, d))), [E.T(Ls["anti"])])
        Pd = E.propagator(Sd, 7.0)
        rg = rng_for(spec["seed"], TEST_CODE["T2"], d, 99)
        X = np.zeros((d, d), complex); A = rg.standard_normal((nc, nc)) + 1j * rg.standard_normal((nc, nc)); X[:nc, :nc] = A + A.conj().T
        x = E.T(X).reshape(d * d, 1)
        out["identities"]["VtPF_eq_PF_d%d" % d] = float(E.t.linalg.vector_norm(Pd @ x - x).item())
        del Sd, Pd
    return out


def summarize_T2(rows, d, nc, beta, s2):
    st = [r["status"] for r in rows]
    uniq = [r for r in rows if r["status"] == "UNIQUE"]
    g = np.array([r["gamma_diss"] for r in rows])
    cci = np.array([r.get("cci", np.nan) for r in rows])
    n1 = np.array([r["folds"][0]["n"] if "folds" in r else np.nan for r in rows])
    n2 = np.array([r["folds"][1]["n"] if "folds" in r else np.nan for r in rows])
    n3 = np.array([r["folds"][2]["n"] if "folds" in r else np.nan for r in rows])
    half = cci >= s2["cci_half"]
    above_uniform = cci > nc / d
    fw = s2["folds_window"]
    fwin = (n1 >= fw["c1"][0]) & (n1 <= fw["c1"][1]) & (n2 >= fw["c2"][0]) & (n2 <= fw["c2"][1])

    def span(mask):
        if not np.any(mask):
            return None
        return [float(g[mask].min()), float(g[mask].max()), int(mask.sum())]
    # gamma* com CCI = 1 - beta (interpolacao log-linear; informativo, NAO calibracao)
    gstar = None; target = 1.0 - beta
    for i in range(len(rows) - 1):
        a, b = cci[i], cci[i + 1]
        if np.isfinite(a) and np.isfinite(b) and (a - target) * (b - target) <= 0 and a != b:
            fr = (target - a) / (b - a)
            gstar = float(10 ** (math.log10(g[i]) + fr * (math.log10(g[i + 1]) - math.log10(g[i]))))
            break
    nr = [r.get("choi_min_inverse") for r in rows if r.get("choi_min_inverse") is not None]
    return {"d": d, "nc": nc, "n_points": len(rows), "unique": st.count("UNIQUE"), "degenerate": st.count("DEGENERATE"),
            "ambiguous": st.count("AMBIGUOUS"), "gap_rel_min": float(min((r["gap_rel"] for r in uniq), default=float("nan"))),
            "cci_min": float(np.nanmin(cci)) if np.any(np.isfinite(cci)) else None, "cci_max": float(np.nanmax(cci)) if np.any(np.isfinite(cci)) else None,
            "cci_half_window": span(half), "cci_above_uniform_window": span(above_uniform), "folds_window": span(fwin),
            "n_folds_range": {"c1": [float(np.nanmin(n1)), float(np.nanmax(n1))], "c2": [float(np.nanmin(n2)), float(np.nanmax(n2))],
                              "c3": [float(np.nanmin(n3)), float(np.nanmax(n3))]} if np.any(np.isfinite(n1)) else None,
            "gamma_star_cci_1_minus_beta": gstar, "identity_violations": sum(len(r["viol"]) for r in rows),
            "nonreturn_choi_min_inverse": nr[0] if nr else None}


# ----------------------------------------------------------------------------------------------------------------------------------
# T1 -- a lei-raiz recuperada AS CEGAS do sistema aberto inteiro (tomografia do processo; o estimador nao ve beta nem a lei)
# ----------------------------------------------------------------------------------------------------------------------------------
def t1_instance(E, spec, d, idx, law_power, test_code):
    s1 = spec["T1"]; op = spec["operators"]
    r = rng_for(spec["seed"], test_code, d, idx)
    nc = int(r.choice(s1["nc"]))
    beta_inj = float(10 ** r.uniform(*s1["beta_log_range"]))
    kper = r.uniform(s1["k_range"][0], s1["k_range"][1], d - nc)
    gd = float(10 ** r.uniform(*s1["gamma_diss_log_range"]))
    jseed = int(r.integers(0, 2 ** 31 - 1))
    rs = np.random.RandomState(jseed); Jr = rs.randn(d, d) * 0.2; Jr = (Jr + Jr.T) / 2; np.fill_diagonal(Jr, 0); Jr[:nc, :nc] *= 2
    mu = np.zeros(d); mu[:nc] = -1.0 * np.arange(nc, 0, -1); mu[nc:] = 0.5 + 0.3 * np.arange(d - nc)
    Pi = np.zeros((d, d)); Pi[:nc, :nc] = np.eye(nc)
    H = (np.diag(mu) + Jr - spec["eps_H"] * Pi).astype(complex)
    Ls, k = five_jumps(d, nc, beta_inj, gd, op, k_periph=kper, law_power=law_power)
    S = E.superop(E.T(H), [E.T(L) for L in Ls.values()])
    Phi = E.propagator(S, s1["tau"]); del S
    Cc = np.eye(d) - np.ones((d, d)) / d
    out = []
    gen = E.t.Generator(device=E.dev); gen.manual_seed(int(r.integers(0, 2 ** 62)))
    for sigma in s1["noise"]:
        if sigma > 0:
            Nz = (E.t.randn(Phi.shape, generator=gen, dtype=E.t.float64, device=E.dev) + 1j * E.t.randn(Phi.shape, generator=gen, dtype=E.t.float64, device=E.dev)) / math.sqrt(2)
            Phin = Phi + sigma * Nz; del Nz
        else:
            Phin = Phi
        dg, maxim = E.generator_diag_from_propagator(Phin, s1["tau"])
        M = Cc @ dg.reshape(d, d).cpu().numpy() @ Cc
        fr = fit_root_law(M, k, op.get("anti_gamma", 1.0))      # CEGO: so M, k e gamma_anti
        out.append({"sigma": sigma, "beta_rel_err": abs(fr["beta_hat"] / beta_inj - 1.0), "p_hat": fr["p_hat"], "misfit": fr["misfit"],
                    "rank_ratio": fr["rank_ratio"], "branch_ok": bool(maxim < math.pi - 0.1)})
        if sigma > 0:
            del Phin
    del Phi
    return {"d": d, "nc": nc, "idx": idx, "law_power_injected": law_power, "beta_inj": beta_inj, "gamma_diss": gd, "levels": out}


def run_T1(E, spec, prog, det, law_power=0.5, counts=None, test_code=None, phase="T1"):
    s1 = spec["T1"]; test_code = test_code or TEST_CODE["T1"]
    counts = counts if counts is not None else s1["d_counts"]
    total = sum(int(v) for v in counts.values()); done = 0; per = {}
    for ds, n in counts.items():
        d = int(ds); rows = []
        for idx in range(int(n)):
            rec = t1_instance(E, spec, d, idx, law_power, test_code)
            rows.append(rec); det.write(jline(dict(T=phase, **rec)))
            done += 1; prog.set(phase=phase, done=done, total=total)
        per[ds] = summarize_T1(rows, s1, law_power)
    return per


def summarize_T1(rows, s1, law_power):
    out = {"n": len(rows)}
    for li, sigma in enumerate(s1["noise"]):
        be = np.array([r["levels"][li]["beta_rel_err"] for r in rows]); pe = np.array([r["levels"][li]["p_hat"] for r in rows])
        br = np.array([r["levels"][li]["branch_ok"] for r in rows])
        crit = s1["pass"].get(repr(float(sigma)))
        ok_frac = None
        if crit is not None and len(rows):
            okm = (be <= crit["beta_rel"]) & (np.abs(pe - law_power) <= crit["p_abs"]) & br
            ok_frac = float(np.mean(okm))
        out["sigma_%s" % repr(float(sigma))] = {
            "median_beta_rel_err": float(np.median(be)) if be.size else None, "max_beta_rel_err": float(np.max(be)) if be.size else None,
            "median_abs_p_err": float(np.median(np.abs(pe - law_power))) if pe.size else None,
            "max_abs_p_err": float(np.max(np.abs(pe - law_power))) if pe.size else None,
            "branch_ok_frac": float(np.mean(br)) if br.size else None, "pass_frac": ok_frac,
            "required_frac": (crit or {}).get("min_frac"), "root_law_rejected_frac": float(np.mean(np.abs(pe - 0.5) > 0.1)) if pe.size else None}
    return out


# ----------------------------------------------------------------------------------------------------------------------------------
# T3 -- os controles que TEM de falhar
# ----------------------------------------------------------------------------------------------------------------------------------
def run_T3(E, spec, beta, prog, det):
    s3 = spec["T3"]; tol = spec["tolerances"]; op = spec["operators"]; res = {}
    nc = s3["nc"]; gd = s3["gamma_diss"]
    total = len(s3["d"]) * 4; done = 0
    for d in s3["d"]:
        H, Pi = canonical_H(d, nc, spec["eps_H"])
        Ls, k = five_jumps(d, nc, beta, gd, op)
        r = {}
        # N1 dephasing sozinho (H = 0): o nucleo de L tem dimensao d + n_c(n_c - 1) -- o atrator NAO e' unico (o kernel prova)
        S = E.superop(E.T(np.zeros((d, d))), [E.T(Ls["anti"])]); ev = E.spectrum(S); cl = Engine.classify(ev, tol["tol0_rel"], tol["gap_rel"]); del S
        r["N1_dephasing_only"] = {"status": cl["status"], "n0": cl["n0"], "expected_n0": d + nc * (nc - 1),
                                  "failed_as_required": bool(cl["status"] == "DEGENERATE" and cl["n0"] == d + nc * (nc - 1))}
        done += 1; prog.set(phase="T3", done=done, total=total)
        # N2 unital (H_LD + so o dephasing): o atrator e' I/d -- a morte termica; o Nome NAO se forma
        S = E.superop(E.T(H), [E.T(Ls["anti"])]); ev = E.spectrum(S); cl = Engine.classify(ev, tol["tol0_rel"], tol["gap_rel"])
        n2 = {"status": cl["status"], "n0": cl["n0"]}
        if cl["status"] != "DEGENERATE":
            rho, resid, w = E.steady_state(S, d); rn = rho.cpu().numpy()
            n2["dist_to_I_over_d"] = float(np.linalg.norm(rn - np.eye(d) / d)); n2["cci"] = float(np.real(np.trace(Pi.real @ rn))); n2["cci_uniform"] = nc / d
            n2["failed_as_required"] = bool(cl["status"] != "UNIQUE" or n2["dist_to_I_over_d"] <= 1e-8)
        else:
            n2["failed_as_required"] = True
        del S
        r["N2_unital_heat_death"] = n2
        done += 1; prog.set(phase="T3", done=done, total=total)
        # N4 taxa NEGATIVA (gamma_cons -> -0.5): nao e' CP; o detector TEM de acusar
        pairs = [(E.T(Ls["reh"]), 1.0), (E.T(Ls["anti"]), 1.0), (E.T(Ls["prune"]), 1.0), (E.T(Ls["diss"]), 1.0),
                 (E.T(Ls["cons"] / math.sqrt(op.get("cons_gamma", 2.0))), -0.5)]
        S = superop_rates(E, E.T(H), pairs); cm = E.choi_min(E.propagator(S, s3["tau_N4"]), d); del S
        r["N4_negative_rate_not_cp"] = {"choi_min": cm, "failed_as_required": bool(cm < -tol["cp"])}
        done += 1; prog.set(phase="T3", done=done, total=total)
        # N5 inversao do tempo: exp(-tau S) nao e' canal
        S = E.superop(E.T(H), [E.T(L) for L in Ls.values()]); cmb = E.choi_min(E.propagator(-S, s3["tau_N5"]), d); del S
        r["N5_time_reversal_not_cp"] = {"choi_min": cmb, "failed_as_required": bool(cmb < -tol["cp"])}
        done += 1; prog.set(phase="T3", done=done, total=total)
        res["d%d" % d] = r
        det.write(jline(dict(T="T3", d=d, **r)))
    # N3 a lei LINEAR injetada: o estimador cego TEM de devolver p ~ 1 e rejeitar a lei-raiz
    res["N3_linear_law"] = run_T1(E, spec, prog, det, law_power=1.0, counts=s3["N3_counts"], test_code=31, phase="T3_N3")
    return res


# ----------------------------------------------------------------------------------------------------------------------------------
# T4 -- estresse adversarial (o molde dos cinco saltos com coeficientes, taxas, K, H e base ALEATORIOS)
# ----------------------------------------------------------------------------------------------------------------------------------
def haar_unitary(rng, d):
    Z = (rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))) / math.sqrt(2)
    Q, R = np.linalg.qr(Z)
    ph = np.diag(R) / np.abs(np.diag(R))
    return Q * ph


def t4_instance(spec, d, idx):
    s4 = spec["T4"]; r = rng_for(spec["seed"], TEST_CODE["T4"], d, idx)
    nc = int(r.choice(s4["nc"]))
    mu = np.zeros(d); mu[:nc] = -1.0 * np.arange(nc, 0, -1) * r.uniform(0.5, 1.5, nc)
    mu[nc:] = (0.5 + 0.3 * np.arange(d - nc)) * r.uniform(0.5, 1.5, d - nc) + r.normal(0, 0.1, d - nc)
    sJ = r.uniform(0.05, 0.5); J = r.standard_normal((d, d)) * sJ; J = (J + J.T) / 2; np.fill_diagonal(J, 0); J[:nc, :nc] *= 2
    eps = r.uniform(0.0, 10.0)
    Pi = np.zeros((d, d)); Pi[:nc, :nc] = np.eye(nc)
    H = (np.diag(mu) + J - eps * Pi).astype(complex)
    span = int(r.integers(max(1, (d - nc) // 4), d - nc + 1)); end = nc + span
    L_reh = np.zeros((d, d), complex); L_con = np.zeros((d, d), complex); L_dis = np.zeros((d, d), complex)
    ar, br_ = r.uniform(0.1, 1.0), r.uniform(0.0, 0.5); ac, bc = r.uniform(0.1, 1.0), r.uniform(0.0, 0.5); ad, bd = r.uniform(0.1, 1.0), r.uniform(0.0, 0.5)
    for j in range(nc, end):
        for a in range(nc):
            L_reh[a, j] = math.sqrt(ar) * math.exp(-br_ * (j - nc)); L_con[a, j] = math.sqrt(ac) * math.exp(-bc * (j - nc)); L_dis[j, a] = math.sqrt(ad) * math.exp(-bd * (j - nc))
    L_pru = np.zeros((d, d), complex); st = int(r.integers(nc, d))
    for i in range(st, d):
        L_pru[0, i] = math.sqrt((i - nc + 1) / d) * r.uniform(0.5, 1.5)
    beta_any = 10 ** r.uniform(-4, -1); kk = np.zeros(d); kk[nc:] = r.uniform(0.5, 2.5, d - nc)
    L_ant = np.diag(np.sqrt(beta_any * kk)).astype(complex)
    l3 = math.log10(3.0)
    gam = {"reh": 1.0 * 10 ** r.uniform(-l3, l3), "anti": 1.0 * 10 ** r.uniform(-l3, l3), "prune": 0.5 * 10 ** r.uniform(-l3, l3),
           "cons": 2.0 * 10 ** r.uniform(-l3, l3), "diss": 10 ** r.uniform(-4, 2)}
    Ls = [math.sqrt(gam["reh"]) * L_reh, math.sqrt(gam["anti"]) * L_ant, math.sqrt(gam["prune"]) * L_pru, math.sqrt(gam["cons"]) * L_con, math.sqrt(gam["diss"]) * L_dis]
    rot = bool(r.random() < 0.5)
    if rot:
        U = haar_unitary(r, d); Ud = U.conj().T
        H = U @ H @ Ud; Ls = [U @ L @ Ud for L in Ls]; Pi = U @ Pi @ Ud
    return H, Ls, Pi, nc, rot, r


def run_T4(E, spec, prog, det):
    s4 = spec["T4"]; tol = spec["tolerances"]; per = {}
    total = sum(int(v) for v in s4["d_counts"].values()); done = 0
    for ds, n in s4["d_counts"].items():
        d = int(ds); agg = {"n": 0, "UNIQUE": 0, "DEGENERATE": 0, "AMBIGUOUS": 0, "viol": {}, "cci_above_uniform": 0, "rotated": 0, "gap_rel_min": None}
        for idx in range(int(n)):
            H, Ls, Pi, nc, rot, r = t4_instance(spec, d, idx)
            rec = pipeline(E, H, Ls, d, Pi, tol, s4["dt"], s4["steps"], r)
            v = identity_violations(rec, tol)
            agg["n"] += 1; agg[rec["status"]] += 1; agg["rotated"] += int(rot)
            for x in v:
                agg["viol"][x] = agg["viol"].get(x, 0) + 1
            if rec["status"] == "UNIQUE":
                agg["gap_rel_min"] = rec["gap_rel"] if agg["gap_rel_min"] is None else min(agg["gap_rel_min"], rec["gap_rel"])
                if rec.get("cci", 0) > nc / d:
                    agg["cci_above_uniform"] += 1
            det.write(jline({"T": "T4", "d": d, "idx": idx, "nc": nc, "rot": rot, "status": rec["status"], "viol": v,
                             "gap_rel": rec.get("gap_rel"), "cci": rec.get("cci")}))
            done += 1; prog.set(phase="T4", done=done, total=total)
        per[ds] = agg
    return per


# ----------------------------------------------------------------------------------------------------------------------------------
# D128 -- uma instancia canonica em d = 128 (superoperador 16384 x 16384): espectro, estacionario, dobras, Spohn por RK4 em d x d
# ----------------------------------------------------------------------------------------------------------------------------------
def lindblad_rhs(H, Ls, LdLsum, rho):
    out = -1j * (H @ rho - rho @ H) - 0.5 * (LdLsum @ rho + rho @ LdLsum)
    for L in Ls:
        out = out + L @ rho @ L.conj().T
    return out


def run_D128(E, spec, beta, prog):
    sd = spec["D128"]; tol = spec["tolerances"]; t = E.t
    d, nc, gd = sd["d"], sd["nc"], sd["gamma_diss"]
    out = {"d": d, "nc": nc, "gamma_diss": gd}
    try:
        H, Pi = canonical_H(d, nc, spec["eps_H"])
        Ls, k = five_jumps(d, nc, beta, gd, spec["operators"])
        Hg = E.T(H); Lg = [E.T(L) for L in Ls.values()]
        prog.set(phase="D128", step="superop", force=True)
        S = E.superop(Hg, Lg); E.sync()
        prog.set(phase="D128", step="spectrum", force=True)
        t0 = time.time(); ev = E.spectrum(S); out["spectrum_s"] = time.time() - t0
        cl = Engine.classify(ev, tol["tol0_rel"], tol["gap_rel"]); out.update({k2: cl[k2] for k2 in ("status", "n0", "gap", "gap_rel", "scale", "max_re")})
        if cl["status"] != "DEGENERATE":
            prog.set(phase="D128", step="steady_state", force=True)
            t0 = time.time(); rho, res, w = E.steady_state(S, d); out["steady_state_s"] = time.time() - t0
            del S
            wn = w.cpu().numpy(); rn = rho.cpu().numpy()
            out.update({"ss_res_rel": res / cl["scale"], "ss_min_eig": float(wn.min()), "cci": float(np.real(np.trace(Pi.real @ rn))),
                        "folds": [{"D": f["D_folds"], "n": f["n_folds"]} for f in folds(wn, d)]})
            prog.set(phase="D128", step="spohn_rk4", force=True)
            LdLsum = sum((L.conj().T @ L) for L in Lg)
            log_ss, _ = E.log_of(rho)
            rng = rng_for(spec["seed"], TEST_CODE["D128"], d)
            states = init_states(E, d, rng)
            h = sd["rk4_dt"]; viol = 0; Dprev = None; maxrise = -float("inf")
            t0 = time.time()
            for s in range(sd["rk4_steps"] + 1):
                Dn = []
                for r_ in states:
                    R = (r_ + r_.conj().T) / 2; R = R / t.trace(R).real
                    w_ = t.linalg.eigvalsh(R); wp = t.clamp(w_, min=1e-300)
                    Dn.append(float(((w_ * t.log(wp)).sum() - t.trace(R @ log_ss).real).item()))
                Dn = np.array(Dn)
                if Dprev is not None:
                    rise = Dn - Dprev; maxrise = max(maxrise, float(rise.max()))
                    viol += int(np.sum(rise > tol["spohn_abs"] + tol["spohn_rel"] * np.abs(Dprev)))
                Dprev = Dn
                if s < sd["rk4_steps"]:
                    new = []
                    for r_ in states:
                        k1 = lindblad_rhs(Hg, Lg, LdLsum, r_); k2 = lindblad_rhs(Hg, Lg, LdLsum, r_ + 0.5 * h * k1)
                        k3 = lindblad_rhs(Hg, Lg, LdLsum, r_ + 0.5 * h * k2); k4 = lindblad_rhs(Hg, Lg, LdLsum, r_ + h * k3)
                        new.append(r_ + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4))
                    states = new
            out["spohn_rk4"] = {"violations": viol, "max_rise": maxrise, "steps": sd["rk4_steps"], "dt": h, "s": time.time() - t0}
        else:
            del S
        out["ran"] = True
    except Exception as e:
        out["ran"] = False; out["error"] = "%s: %s" % (type(e).__name__, str(e)[:300])
    try:
        t.cuda.empty_cache()
    except Exception:
        pass
    return out


# ----------------------------------------------------------------------------------------------------------------------------------
# a referencia na CPU (numpy/scipy, subprocesso a parte, 4 fios, prioridade baixa) -- recalcula um subconjunto do T2 canonico
# ----------------------------------------------------------------------------------------------------------------------------------
def superop_np(H, Ls):
    d = H.shape[0]; I = np.eye(d)
    S = -1j * (np.kron(H, I) - np.kron(I, H.T))
    for L in Ls:
        LdL = L.conj().T @ L
        S = S + np.kron(L, L.conj()) - 0.5 * np.kron(LdL, I) - 0.5 * np.kron(I, LdL.T)
    return S


def cpuref_items(spec):
    s2 = spec["T2"]; sc = spec["cpuref"]; items = []
    for d in sc["d_all"]:
        for nc in s2["nc"]:
            for gi in range(int(s2["n_gamma"][str(d)])):
                items.append((int(d), int(nc), gi))
    for ds, picks in sc["d_pick"].items():
        for nc, gi in picks:
            items.append((int(ds), int(nc), int(gi)))
    return items


def run_cpuref(spec, beta, outdir):
    import scipy.linalg as sl
    s2 = spec["T2"]; tol = spec["tolerances"]; op = spec["operators"]; out = {}
    t0 = time.time()
    for (d, nc, gi) in cpuref_items(spec):
        gd = float(gamma_grid(s2, d)[gi])
        H, Pi = canonical_H(d, nc, spec["eps_H"])
        Ls, k = five_jumps(d, nc, beta, gd, op)
        S = superop_np(H, list(Ls.values()))
        ev = np.linalg.eigvals(S)
        cl = Engine.classify(ev, tol["tol0_rel"], tol["gap_rel"])
        rec = {"status": cl["status"], "n0": cl["n0"], "gap_rel": cl["gap_rel"]}
        if cl["status"] != "DEGENERATE":
            n = d * d; M = S.copy(); tr = np.zeros(n, complex); tr[np.arange(d) * (d + 1)] = 1.0; M[0, :] = tr
            b = np.zeros(n, complex); b[0] = 1.0
            x = np.linalg.solve(M, b); rho = x.reshape(d, d); rho = (rho + rho.conj().T) / 2; rho = rho / np.trace(rho).real
            w = np.linalg.eigvalsh(rho)
            rec.update({"cci": float(np.real(np.trace(Pi.real @ rho))), "purity": float(np.real(np.trace(rho @ rho))), "ss_min_eig": float(w.min()),
                        "folds_n": [f["n_folds"] for f in folds(w, d)]})
            P = sl.expm(s2["dt"] * S)
            J = P.reshape(d, d, d, d).transpose(0, 2, 1, 3).reshape(n, n); J = (J + J.conj().T) / 2
            rec["choi_min"] = float(np.linalg.eigvalsh(J).min())
        out["%d_%d_%d" % (d, nc, gi)] = rec
    res = {"worker": WORKER_ID, "mode": "cpuref", "items": out, "n": len(out), "seconds": time.time() - t0, "numpy": np.__version__}
    write_json_atomic(os.path.join(outdir, "cpuref.json"), res)
    return res


def compare_cpuref(spec, gpu_rows, cpu):
    tol = spec["cpuref"]["tol"]; bad = []; n = 0; maxd = {"cci": 0.0, "purity": 0.0, "folds_n": 0.0, "gap_rel_rel": 0.0, "choi_min": 0.0}
    for key, c in (cpu.get("items") or {}).items():
        g = gpu_rows.get(key)
        if g is None:
            bad.append((key, "GPU_ROW_MISSING")); continue
        n += 1
        if g["status"] != c["status"]:
            bad.append((key, "STATUS %s != %s" % (g["status"], c["status"]))); continue
        if c["status"] == "DEGENERATE":
            continue
        dc = abs(g["cci"] - c["cci"]); dp = abs(g["purity"] - c["purity"])
        df = max(abs(a - b) for a, b in zip([f["n"] for f in g["folds"]], c["folds_n"]))
        dg = abs(g["gap_rel"] - c["gap_rel"]) / max(abs(c["gap_rel"]), 1e-300)
        dch = abs(g["choi_min"] - c["choi_min"])
        maxd["cci"] = max(maxd["cci"], dc); maxd["purity"] = max(maxd["purity"], dp); maxd["folds_n"] = max(maxd["folds_n"], df)
        maxd["gap_rel_rel"] = max(maxd["gap_rel_rel"], dg); maxd["choi_min"] = max(maxd["choi_min"], dch)
        if dc > tol["cci"] or dp > tol["purity"] or df > tol["folds_n"] or dg > tol["gap_rel_rel"] or dch > tol["choi_min"]:
            bad.append((key, "TOL"))
    return {"compared": n, "disagreements": len(bad), "first_disagreements": bad[:10], "max_diffs": maxd, "ok": bool(n > 0 and not bad)}


# ----------------------------------------------------------------------------------------------------------------------------------
# a sonda de tempo do proprio pipeline -- SO hardware: operadores ALEATORIOS densos, nenhum operador da teoria
# ----------------------------------------------------------------------------------------------------------------------------------
def run_timing(E, outdir, reps=None):
    reps = reps or {8: 30, 16: 10, 32: 4, 64: 1}
    tol = {"tol0_rel": 1e-10, "gap_rel": 1e-8, "spohn_abs": 1e-10, "spohn_rel": 1e-9}
    res = {}
    for d, nrep in reps.items():
        rg = np.random.default_rng([9, d]); tp = []; t1 = []
        for _ in range(nrep):
            A = rg.standard_normal((d, d)) + 1j * rg.standard_normal((d, d)); H = (A + A.conj().T) / 2
            Ls = [(rg.standard_normal((d, d)) + 1j * rg.standard_normal((d, d))) / d for _ in range(5)]
            Pi = np.zeros((d, d)); Pi[:2, :2] = np.eye(2)
            E.sync(); a = time.time(); pipeline(E, H, Ls, d, Pi, tol, 0.05, 64, rg); E.sync(); tp.append(time.time() - a)
            a = time.time()
            S = E.superop(E.T(H), [E.T(L) for L in Ls]); Phi = E.propagator(S, 0.05); del S
            for sigma in (0.0, 1e-8, 1e-6):
                Phin = Phi + sigma * E.T(rg.standard_normal(Phi.shape)) if sigma > 0 else Phi
                dg, mx = E.generator_diag_from_propagator(Phin, 0.05)
                Cc = np.eye(d) - np.ones((d, d)) / d
                fit_root_law(Cc @ dg.reshape(d, d).cpu().numpy() @ Cc, np.r_[np.zeros(2), np.linspace(0.5, 2.5, d - 2)], 1.0)
            del Phi; E.sync(); t1.append(time.time() - a)
        res[str(d)] = {"pipeline_s": float(np.median(tp)), "t1_injection_3_levels_s": float(np.median(t1)), "reps": nrep}
        print("timing d=%d" % d, res[str(d)], flush=True)
    return res


# ----------------------------------------------------------------------------------------------------------------------------------
# a arvore de vereditos (congelada no pre-registro; o um.py a REDERIVA destes mesmos numeros)
# ----------------------------------------------------------------------------------------------------------------------------------
def derive_verdict(spec, R):
    P = "TGL_QUANTUM_PILLAR_V1__"
    if R.get("refused"):
        return P + "NOT_RUN__" + R["refused"] + "__GATE_UNTOUCHED"
    if not (R.get("engine_selftest") or {}).get("all_ok"):
        return P + "ENGINE_SELFTEST_FAILED__NO_RESULT__GATE_UNTOUCHED"
    for ph in ("T3", "T2", "T1", "T4"):
        if not isinstance(R.get(ph), dict) or R[ph].get("error"):
            return P + "PHASE_%s_FAILED__RESULTS_INCOMPLETE__GATE_UNTOUCHED" % ph
    tol = spec["tolerances"]
    # 1. os controles TEM de falhar
    t3 = R["T3"]; ctl_ok = True
    for dk, r in t3.items():
        if dk.startswith("d"):
            for nm in ("N1_dephasing_only", "N2_unital_heat_death", "N4_negative_rate_not_cp", "N5_time_reversal_not_cp"):
                ctl_ok = ctl_ok and bool((r.get(nm) or {}).get("failed_as_required"))
    for ds, s in (t3.get("N3_linear_law") or {}).items():
        lv = s.get("sigma_0.0") or {}
        ctl_ok = ctl_ok and (lv.get("pass_frac") == 1.0) and (lv.get("root_law_rejected_frac") == 1.0)
    if not ctl_ok:
        return P + "CONTROL_DID_NOT_FAIL__INSTRUMENT_BLIND__RESULTS_VOID__GATE_UNTOUCHED"
    # 2. as identidades (CP, TP, PSD, Spohn, V_t P_F = P_F, sin^2 theta_M = beta) -- se uma cair, o motor e' suspeito
    nv = sum(c["identity_violations"] for c in R["T2"]["configs"])
    nv += sum(sum(a["viol"].values()) for a in R["T4"].values())
    ids = R["T2"]["identities"]
    nv += int(ids.get("sin2_thetaM_minus_beta", 1.0) > tol["identity_abs"])
    nv += sum(int(v > tol["identity_abs"]) for k, v in ids.items() if k.startswith("VtPF"))
    if nv > 0:
        return P + "IDENTITY_VIOLATED_%d__ENGINE_SUSPECT__RESULTS_VOID__GATE_UNTOUCHED" % nv
    # 3. a referencia na CPU
    if not (R.get("cpuref_compare") or {}).get("ok"):
        return P + "CPU_REFERENCE_DISAGREES_OR_ABSENT__RESULTS_VOID__GATE_UNTOUCHED"
    # 4. os resultados
    cf = R["T2"]["configs"]; npts = sum(c["n_points"] for c in cf); nun = sum(c["unique"] for c in cf)
    uniq = "ALL_%d" % npts if nun == npts else ("%d_OF_%d" % (nun, npts))
    t1 = R["T1"]; rec0 = all((s.get("sigma_0.0") or {}).get("pass_frac") == 1.0 for s in t1.values())
    root = "RECOVERED" if rec0 else "NOT_RECOVERED"      # so o nivel SEM ruido decide; os niveis com ruido sao a curva de resolucao (relatada)
    nconf = len(cf); fw = sum(1 for c in cf if c["folds_window"]); nm = sum(1 for c in cf if c["cci_half_window"])
    t4 = R["T4"]; n4 = sum(a["n"] for a in t4.values()); u4 = sum(a["UNIQUE"] for a in t4.values())
    dd = R.get("D128") or {}
    d128 = ("D128_" + dd.get("status", "NA")) if dd.get("ran") else "D128_NOT_RUN"
    return (P + "FIVE_JUMP_GKLS__ATTRACTOR_UNIQUE_%s__ROOT_LAW_%s_BLIND__CONTROLS_FAILED_AS_REQUIRED__STRESS_%d_ZERO_IDENTITY_VIOLATIONS_%d_UNIQUE__"
            "NAME_IN_CORE_%d_OF_%d__FOLDS_WINDOW_%d_OF_%d__%s__CPU_REFERENCE_AGREES__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED"
            % (uniq, root, n4, u4, nm, nconf, fw, nconf, d128))


# ----------------------------------------------------------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------------------------------------------------------
def _below_normal_flags():
    if os.name == "nt":
        return 0x00004000   # BELOW_NORMAL_PRIORITY_CLASS: o lake build do rito tem prioridade sobre a CPU
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["run", "engine", "timing", "cpuref"])
    ap.add_argument("--spec"); ap.add_argument("--spec-sha256"); ap.add_argument("--beta-hex"); ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    prog = Progress(args.out)
    me = os.path.abspath(__file__)
    R = {"worker": WORKER_ID, "mode": args.mode, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "worker_sha256": sha256_bytes(open(me, "rb").read()),
         "status_statement": "[COMPUTED] -- calculo do sistema aberto da teoria; NAO e' medicao; o gate nao muda"}
    rp = os.path.join(args.out, "result.json")
    spec = None
    try:
        if args.spec:
            spec = json.loads(open(args.spec, "rb").read().decode("utf-8"))
            R["spec_sha256"] = sha256_bytes(canon_json(spec).encode("utf-8"))
            if args.spec_sha256 and R["spec_sha256"] != args.spec_sha256:
                R["refused"] = "SPEC_HASH_MISMATCH"; R["verdict"] = derive_verdict(spec, R); write_json_atomic(rp, R); sys.exit(4)
        beta = float.fromhex(args.beta_hex) if args.beta_hex else None
        R["beta_hex"] = args.beta_hex; R["beta"] = beta
        if args.mode == "cpuref":
            run_cpuref(spec, beta, args.out); return
        import torch
        R["env"] = {"torch": torch.__version__, "cuda": torch.version.cuda, "numpy": np.__version__, "python": platform.python_version(),
                    "platform": platform.platform(), "cuda_available": bool(torch.cuda.is_available())}
        if not torch.cuda.is_available():
            R["refused"] = "GPU_UNAVAILABLE"; R["verdict"] = derive_verdict(spec, R) if spec else "NOT_RUN__GPU_UNAVAILABLE"; write_json_atomic(rp, R); sys.exit(6)
        torch.use_deterministic_algorithms(True)
        torch.backends.cuda.matmul.allow_tf32 = False; torch.backends.cudnn.allow_tf32 = False
        torch.set_num_threads(4)
        dev = torch.device("cuda")
        R["env"]["gpu"] = torch.cuda.get_device_name(0)
        R["env"]["determinism"] = {"use_deterministic_algorithms": True, "CUBLAS_WORKSPACE_CONFIG": os.environ.get("CUBLAS_WORKSPACE_CONFIG"), "tf32": False, "threads": 4}
        E = Engine(torch, dev)
        prog.set(phase="engine_selftest", force=True)
        R["engine_selftest"] = engine_selftest(E, (spec or {}).get("tolerances", {}).get("engine", 1e-9))
        if not R["engine_selftest"]["all_ok"]:
            R["verdict"] = "TGL_QUANTUM_PILLAR_V1__ENGINE_SELFTEST_FAILED__NO_RESULT__GATE_UNTOUCHED"; write_json_atomic(rp, R); sys.exit(5)
        if args.mode == "engine":
            R["verdict"] = "ENGINE_SELFTEST_PASSED"; write_json_atomic(rp, R); return
        if args.mode == "timing":
            R["timing"] = run_timing(E, args.out); write_json_atomic(rp, R); return
        # ---------------- o rito ----------------
        import subprocess
        cpu_proc = subprocess.Popen([sys.executable, me, "--mode", "cpuref", "--spec", args.spec, "--spec-sha256", R["spec_sha256"], "--beta-hex", args.beta_hex,
                                     "--out", args.out], stdout=subprocess.DEVNULL, stderr=open(os.path.join(args.out, "cpuref.stderr.txt"), "w"),
                                    creationflags=_below_normal_flags())
        detp = os.path.join(args.out, "details.jsonl")
        R["phase_seconds"] = {}
        gpu_rows = {}
        with open(detp, "w", encoding="utf-8") as det:
            for ph in ("T3", "T2", "T1", "T4"):
                t0 = time.time()
                try:
                    if ph == "T3":
                        R["T3"] = run_T3(E, spec, beta, prog, det)
                    elif ph == "T2":
                        R["T2"] = run_T2(E, spec, beta, prog, det)
                    elif ph == "T1":
                        R["T1"] = run_T1(E, spec, prog, det)
                    else:
                        R["T4"] = run_T4(E, spec, prog, det)
                except Exception as e:
                    R[ph] = {"error": "%s: %s" % (type(e).__name__, str(e)[:500]), "trace": traceback.format_exc()[-2000:]}
                R["phase_seconds"][ph] = round(time.time() - t0, 1)
                det.flush()
                write_json_atomic(os.path.join(args.out, "result_partial.json"), R)
        # as linhas do T2 para a comparacao com a CPU (lidas de volta do arquivo de detalhes)
        with open(detp, "r", encoding="utf-8") as fh:
            for line in fh:
                o = json.loads(line)
                if o.get("T") == "T2":
                    gi = int(np.argmin(np.abs(np.log10(gamma_grid(spec["T2"], o["d"])) - math.log10(o["gamma_diss"]))))
                    gpu_rows["%d_%d_%d" % (o["d"], o["nc"], gi)] = o
        prog.set(phase="cpuref_wait", force=True)
        try:
            cpu_proc.wait(timeout=spec["cpuref"]["timeout_s"])
        except Exception:
            cpu_proc.kill()
        cp = os.path.join(args.out, "cpuref.json")
        if os.path.exists(cp):
            cpu = json.load(open(cp, encoding="utf-8"))
            R["cpuref_compare"] = compare_cpuref(spec, gpu_rows, cpu); R["cpuref_compare"]["cpu_seconds"] = cpu.get("seconds")
        else:
            R["cpuref_compare"] = {"ok": False, "error": "cpuref.json ausente"}
        R["details_sha256"] = sha256_bytes(open(detp, "rb").read())
        write_json_atomic(os.path.join(args.out, "result_partial.json"), R)
        # o ponto d = 128 por ultimo, com prazo: se o prazo ja passou, NAO roda (dito no resultado, nunca escondido)
        t0 = time.time()
        if time.time() - prog.t0 <= spec["D128"]["start_deadline_s"]:
            R["D128"] = run_D128(E, spec, beta, prog)
        else:
            R["D128"] = {"ran": False, "error": "DEADLINE: o prazo de inicio (%d s) ja tinha passado" % spec["D128"]["start_deadline_s"]}
        R["phase_seconds"]["D128"] = round(time.time() - t0, 1)
        R["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
        R["verdict"] = derive_verdict(spec, R)
        write_json_atomic(rp, R)
        b = open(rp, "rb").read()
        with open(rp + ".sha256", "w", encoding="ascii") as fh:
            fh.write(sha256_bytes(b))
        prog.set(phase="done", force=True)
    except SystemExit:
        raise
    except Exception as e:
        R["fatal"] = "%s: %s" % (type(e).__name__, str(e)[:500]); R["trace"] = traceback.format_exc()[-3000:]
        R["verdict"] = "TGL_QUANTUM_PILLAR_V1__NOT_RUN__WORKER_FATAL__GATE_UNTOUCHED"
        write_json_atomic(rp, R); sys.exit(1)


if __name__ == "__main__":
    main()
