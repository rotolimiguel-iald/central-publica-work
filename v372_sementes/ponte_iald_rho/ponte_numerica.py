# -*- coding: utf-8 -*-
"""Espelho numerico da ponte rho*_IALD = rho*_TGL, ALEM da face do Lean: M_n (n = 2..5), estado fiel
generico NAO diagonal, e estado com espectro DEGENERADO (centralizador nao abeliano).
Lado TGL: Delta xi = rho xi rho^-1 na forma de Hilbert-Schmidt; K = -log Delta; P_F = projecao sobre ker K;
T_t = exp(-t|K|). Lado IALD: centralizador M^w = {x : x rho = rho x}; projecao de Jones e = projecao ortogonal
(HS) sobre M^w Omega, Omega = rho^1/2; U_s = e + exp(-rs)(1 - e). Checa: polar de Tomita; e == P_F;
Fix iguais; atratores iguais. Controles: estado tracial; subalgebra errada (C1 e uma masa que nao comuta com rho).
Todo check pode falhar; tolerancias declaradas. Semente fixa."""
import numpy as np, scipy.linalg as sl, json, sys, time
rng = np.random.default_rng(20260926)
TOL = 1e-9

def vec(x): return x.reshape(-1)
def unvec(v, n): return v.reshape(n, n)

def op_matrix(f, n):
    """matriz (n^2 x n^2) do mapa linear f: M_n -> M_n na base das unidades."""
    cols = []
    for k in range(n * n):
        E = np.zeros(n * n, complex); E[k] = 1
        cols.append(vec(f(unvec(E, n))))
    return np.array(cols).T

def proj_onto(cols):
    """projecao ortogonal (produto HS = produto euclidiano em vec) sobre o span das colunas."""
    Q, R = np.linalg.qr(cols)
    rank = int(np.sum(np.abs(np.diag(R)) > 1e-10 * max(1, np.abs(R).max())))
    # base ortonormal robusta via SVD
    U, S, _ = np.linalg.svd(cols, full_matrices=False)
    r = int(np.sum(S > 1e-10 * S.max()))
    B = U[:, :r]
    return B @ B.conj().T, r

def random_state(n, degenerate=False, tracial=False):
    if tracial:
        w = np.ones(n) / n
    elif degenerate:
        w = rng.uniform(0.2, 1.0, n); w[1] = w[0]; w = w / w.sum()
    else:
        w = rng.uniform(0.1, 1.0, n); w = w / w.sum()
    Umat, _ = np.linalg.qr(rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)))
    return Umat @ np.diag(w) @ Umat.conj().T, w

def centralizer_basis(rho, n):
    """base de M^w: nucleo de x -> x rho - rho x."""
    C = op_matrix(lambda x: x @ rho - rho @ x, n)
    _, S, Vh = np.linalg.svd(C)
    null = Vh[np.sum(S > 1e-10 * max(1, S.max())):].conj().T
    return [unvec(null[:, k], n) for k in range(null.shape[1])]

def run(n, kind):
    rho, w = random_state(n, degenerate=(kind == "degenerado"), tracial=(kind == "tracial"))
    rh = sl.sqrtm(rho); rinv = np.linalg.inv(rho); rhinv = np.linalg.inv(rh)
    Omega = rh
    Delta = op_matrix(lambda x: rho @ x @ rinv, n)
    DeltaH = op_matrix(lambda x: rh @ x @ rhinv, n)
    # Tomita: J DeltaH (x Omega) = x^H Omega
    tom = max(np.abs(( (rh @ (x @ Omega) @ rhinv).conj().T) - x.conj().T @ Omega).max()
              for x in [rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)) for _ in range(5)])
    K = -sl.logm(Delta)
    K = (K + K.conj().T) / 2
    ev, EV = np.linalg.eigh(K)
    ker = EV[:, np.abs(ev) < 1e-8]
    PF = ker @ ker.conj().T
    cb = centralizer_basis(rho, n)
    e, rank_e = proj_onto(np.array([vec(x @ Omega) for x in cb]).T)
    I = np.eye(n * n)
    bridge = np.abs(e - PF).max()
    # dinamicas e atratores
    r, s_big, t_big = 0.5, 80.0, 80.0
    U = e + np.exp(-r * s_big) * (I - e)
    absK = EV @ np.diag(np.abs(ev)) @ EV.conj().T
    T = sl.expm(-t_big * absK)
    gap = np.min(np.abs(ev[np.abs(ev) > 1e-8])) if np.any(np.abs(ev) > 1e-8) else 0.0
    att_iald = np.abs(U - e).max(); att_tgl = np.abs(T - PF).max()
    rho_star_diff = np.abs(U - T).max()
    # Fix a tempo finito: autoespaco de autovalor 1
    def fixproj(A):
        w_, V_ = np.linalg.eig(A); F = V_[:, np.abs(w_ - 1) < 1e-8]
        return proj_onto(F)[0] if F.shape[1] else np.zeros_like(A)
    U1 = e + np.exp(-r * 1.0) * (I - e); T1 = sl.expm(-1.0 * absK)
    fix_diff = np.abs(fixproj(U1) - fixproj(T1)).max()
    # controles: subalgebra errada
    eC, _ = proj_onto(vec(Omega)[:, None])                 # C1 ⊂ M
    Wm, _ = np.linalg.qr(rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)))
    masa = [Wm @ np.diag(np.eye(n)[k]) @ Wm.conj().T for k in range(n)]
    eMasa, _ = proj_onto(np.array([vec(x @ Omega) for x in masa]).T)
    return dict(n=n, estado=kind, dim_centralizador=len(cb), posto_e=rank_e, traco_normalizado_e=rank_e / n**2,
                tomita_residuo=float(tom), ponte_e_menos_PF=float(bridge), fix_residuo=float(fix_diff),
                atrator_iald=float(att_iald), atrator_tgl=float(att_tgl), rho_estrela_diff=float(rho_star_diff),
                gap_K=float(gap), controle_C1=float(np.abs(eC - PF).max()), controle_masa_errada=float(np.abs(eMasa - PF).max()))

res = []
for n in (2, 3, 4, 5):
    for kind in ("generico", "degenerado", "tracial"):
        if kind == "degenerado" and n < 3: continue
        res.append(run(n, kind))
ok = True
for d in res:
    ponte = d["ponte_e_menos_PF"] < TOL and d["fix_residuo"] < 1e-7 and d["tomita_residuo"] < 1e-8
    atr = d["atrator_iald"] < 1e-9 and (d["atrator_tgl"] < 1e-9 or d["gap_K"] * 80 < 25)
    ctrl = d["controle_C1"] > 1e-3 and d["controle_masa_errada"] > 1e-3
    d["PONTE"] = bool(ponte); d["ATRATORES"] = bool(atr); d["CONTROLES_RECUSAM"] = bool(ctrl)
    if d["estado"] == "tracial":
        # no tracial: K = 0, P_F = 1; o centralizador e M inteiro e e = 1 tambem -> a ponte vale TRIVIALMENTE (as duas dinamicas param)
        d["nota"] = "tracial: K=0, P_F=1, centralizador=M, e=1 -> iguais e TRIVIAIS (o relogio para); nao discrimina nada"
    ok &= ponte and ctrl
    print(json.dumps(d, ensure_ascii=False))
print("VEREDITO:", "BRIDGE_HOLDS_IN_EVERY_FINITE_FACE_TESTED__CONTROLS_REFUSE" if ok else "BRIDGE_FAILED_SOMEWHERE")
