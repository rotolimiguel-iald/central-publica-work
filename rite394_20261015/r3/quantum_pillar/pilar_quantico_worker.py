# -*- coding: utf-8 -*-
"""O PILAR QUANTICO DA TGL -- o trabalho de GPU da v384 (TGL_QUANTUM_PILLAR_V1).

Este codigo VIVE no um.py (Nao ha segundo arquivo): o um.py o materializa ao lado de si, byte a byte, e o lanca como subprocesso no inicio do rito, em
paralelo com o kernel Lean e os ritos cosmologicos. Le a especificacao congelada (o pre-registro) e RECUSA rodar se o hash da especificacao nao bater ou
se o hash DESTE arquivo nao for o que a especificacao congelou; recebe beta do motor de Lagrange do um.py em hexadecimal (bit a bit); nunca beta literal.

O sistema aberto: H_LD (A Fronteira v5, Apendice A.3, setor de uma excitacao) + os CINCO saltos de Lindblad (A Fronteira v5, sec. V.6; matrizes dos
validadores C3; ratificados pelo operador em 03/10/2026): L_reh, L_anti = sqrt(beta) sqrt(K) (a lei-raiz, a forma do gerador do Verbo do um.py), L_prune,
L_cons, L_diss (o vazamento nucleo -> periferia, gamma livre, varrido, nunca calibrado).

Ordem: o MOTOR e' conferido em modelos ANALITICOS (E1..E6), o ESTIMADOR no seu piso (E7) e o COMPARADOR da referencia na CPU (E8) antes de tudo -- se
falhar, nada se calcula. Depois: T3 os
controles (e a identidade unital N2); T2 a forma na escala; T1 o INSTRUMENTO (a lei injetada recuperada as cegas por tomografia do processo); T4 o estresse;
a referencia na CPU (subprocesso a parte, conferido pela marca da rodada); por ultimo o ponto d = 128. Estatuto: [COMPUTED] -- calculo, nunca medicao.

Modos: run (o rito) | engine (so E1..E8) | timing (so hardware: operadores ALEATORIOS densos, nenhum da teoria) | cpuref (a referencia na CPU)."""
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
    """temporario -> substituir; no Windows o leitor pode segurar o arquivo por um instante: novas tentativas, e a falha final e' visivel."""
    data = json.dumps(obj, ensure_ascii=False, indent=1, default=str)
    tmp = path + ".tmp"; last = None
    for _ in range(40):
        try:
            with open(tmp, "w", encoding="utf-8") as fh:
                fh.write(data)
            os.replace(tmp, path)
            return
        except PermissionError as e:
            last = e; time.sleep(0.25)
    raise last


def write_result(path, obj):
    """O resultado (result.json ou cpuref*.json) com o seu .sha256 ao lado -- em TODA saida, inclusive recusa e falha fatal."""
    write_json_atomic(path, obj)
    b = open(path, "rb").read()
    with open(path + ".sha256.tmp", "w", encoding="ascii") as fh:
        fh.write(sha256_bytes(b))
    os.replace(path + ".sha256.tmp", path + ".sha256")


def parent_alive(pid):
    """O processo pai (o um.py) ainda vive? No Windows por OpenProcess/GetExitCodeProcess (os.kill la' MATARIA); fora dele, os.kill(pid, 0)."""
    if not pid:
        return True
    try:
        if os.name == "nt":
            import ctypes
            k = ctypes.windll.kernel32
            h = k.OpenProcess(0x1000, False, int(pid))      # PROCESS_QUERY_LIMITED_INFORMATION
            if not h:
                return False
            code = ctypes.c_ulong()
            ok = k.GetExitCodeProcess(h, ctypes.byref(code)); k.CloseHandle(h)
            return bool(ok) and code.value == 259          # STILL_ACTIVE
        os.kill(int(pid), 0)
        return True
    except Exception:
        return False


class ParentGone(BaseException):
    """O um.py morreu. Herda de BaseException (como KeyboardInterrupt): os except Exception das fases, das instancias e do D128 NAO o engolem;
    so o handler do main o pega e grava NOT_RUN__PARENT_GONE (3a afericao)."""
    pass


class Progress:
    def __init__(self, outdir, run_id=None, parent_pid=None):
        self.p = os.path.join(outdir, "progress.json") if outdir else None
        self.t0 = time.time(); self.last = 0.0; self.state = {"run_id": run_id}; self.parent_pid = parent_pid

    def set(self, force=False, **kw):
        self.state.update(kw)
        now = time.time()
        if self.p and (force or now - self.last >= 20.0):
            if not parent_alive(self.parent_pid):        # o um.py morreu: o trabalhador nao fica orfao na GPU (achado da 2a passada)
                raise ParentGone("o processo pai %s nao vive mais" % self.parent_pid)
            self.state["elapsed_s"] = round(now - self.t0, 1)
            try:
                write_json_atomic(self.p, self.state)
            except Exception:
                pass
            self.last = now


def rng_for(seed, *parts):
    return np.random.default_rng(np.random.SeedSequence([int(seed)] + [int(x) for x in parts]))


TEST_CODE = {"T1": 1, "T2": 2, "T3": 3, "T4": 4, "D128": 5, "N3": 31, "E7": 7, "TIMING": 9}


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
    """Os cinco saltos, cada um JA multiplicado por sqrt(gamma_k). op = parametros do pre-registro (amplitudes, decaimentos, taxas, perfil de K).
    k_periph: espectro de K na periferia (padrao k0 + k1 (i - n_c)); law_power: 0.5 = lei-raiz (a teoria); 1.0 = lei linear (o controle N3)."""
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
    def __init__(self, torch, dev, magma_up_to_n=10 ** 9):
        self.t = torch; self.dev = dev; self.C = torch.complex128; self.magma_up_to_n = int(magma_up_to_n)

    def _nonherm(self, fn, A):
        """Autovalores NAO Hermitianos pelo MAGMA (congelado na especificacao; magma_up_to_n = 10**9 = todo tamanho). O cuSOLVER padrao do PyTorch 2.11 derruba o
        processo (violacao de acesso) de modo DETERMINISTICO e DEPENDENTE DA MATRIZ (n de 16 a 576 no estresse de 03/10: a mesma semente cai na mesma chamada, com ou
        sem determinismo, sincronizacao ou cache limpo); o MAGMA nao caiu em nenhum tamanho. Depois de cada chamada, a preferencia volta ao padrao."""
        t = self.t
        t.backends.cuda.preferred_linalg_library("magma" if A.shape[-1] <= self.magma_up_to_n else "cusolver")
        try:
            return fn(A)
        finally:
            t.backends.cuda.preferred_linalg_library("default")

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
        ev = self._nonherm(self.t.linalg.eigvals, S)
        return ev.cpu().numpy()

    @staticmethod
    def classify(ev, tol0_rel, gap_rel):
        """UNIQUE: exatamente um autovalor com |lambda| <= tol0_rel*escala e todos os outros com -Re lambda >= gap_rel*escala;
        DEGENERATE: dois ou mais no zero; AMBIGUOUS: o resto -- um no zero com espectro proximo do eixo, OU nenhum no zero (n0 = 0), e este ultimo
        e' VIOLACAO da identidade do modo zero (identity_check e o D128), nunca so «ambiguo»."""
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
        M[0, :] = tr                                  # a linha (0,0) e' combinacao das outras linhas diagonais (tr . S = 0): nada se perde
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

    def choi(self, P, d):
        J = P.reshape(d, d, d, d).permute(0, 2, 1, 3).reshape(d * d, d * d)
        return (J + J.conj().T) / 2

    def choi_min(self, P, d):
        return float(self.t.linalg.eigvalsh(self.choi(P, d)).min().item())

    def tp_residual(self, P, d):
        t = self.t
        idx = t.arange(d, device=self.dev) * (d + 1)
        row = P[idx, :].sum(dim=0)
        target = t.zeros(d * d, dtype=self.C, device=self.dev); target[idx] = 1.0
        return float(t.linalg.vector_norm(row - target).item())

    def unital_residual(self, S, d):
        """||S vec(I/d)|| / (||S||_F ||vec(I/d)||): zero (ate o arredondamento) se e so se I/d e' estacionario."""
        t = self.t
        x = t.zeros(d * d, 1, dtype=self.C, device=self.dev); x[t.arange(d, device=self.dev) * (d + 1), 0] = 1.0 / d
        num = float(t.linalg.vector_norm(S @ x).item()); den = float(t.linalg.vector_norm(S).item()) * float(t.linalg.vector_norm(x).item())
        return num / den if den > 0 else float("inf")

    def log_of(self, W, floor=1e-300):
        t = self.t
        w, V = t.linalg.eigh(W)
        lw = t.log(t.clamp(w, min=floor))
        return (V * lw.unsqueeze(-2)) @ V.conj().transpose(-1, -2), w

    def spohn(self, P, rho_ss, inits, steps, tol_abs, tol_rel):
        """D(rho(t)||rho_ss) ao longo de steps passos de P a partir de cada estado inicial (todos os passos de uma vez: uma unica transferencia)."""
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
        R = t.stack(Xs).permute(0, 2, 1).reshape((steps + 1) * m, d, d)
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

    def generator_from_propagator(self, Phi, tau, d, checks=True, S_true=None):
        """L^ = log(Phi)/tau pelo logaritmo principal (Phi = V diag(lambda) V^-1); devolve a diagonal de L^ e:
        tau_antiherm_norm = tau*||(L^ - L^dag)/2i|| -- so INFORMACAO (mede a imagem numerica, nao certifica o ramo);
        ccp_min_rel = o menor autovalor da Choi PROJETADA de L^ relativo ao maior |autovalor| -- LEGITIMIDADE (Kossakowski >= 0: L^ e' um gerador de Lindblad);
        gen_rel_dev = ||L^ - S||_F/||S||_F, so quando o ARNES passa o gerador verdadeiro S_true (injecao; o estimador nunca o ve) -- o CERTIFICADO do
        ramo principal, a posteriori."""
        t = self.t
        lam, V = self._nonherm(t.linalg.eig, Phi)
        Vinv = t.linalg.inv(V)
        ll = t.log(lam) / tau
        Lh = (V * ll.unsqueeze(0)) @ Vinv
        del V, Vinv
        diag = t.diagonal(Lh).clone()
        info = {}
        if checks:
            A = (Lh - Lh.conj().T) / 2j
            A = (A + A.conj().T) / 2
            info["tau_antiherm_norm"] = float(tau * t.max(t.abs(t.linalg.eigvalsh(A))).item())
            del A
            J = Lh.reshape(d, d, d, d).permute(0, 2, 1, 3).reshape(d * d, d * d)
            idx = t.arange(d, device=self.dev) * (d + 1)
            wJ = J[idx, :].sum(dim=0); Jw = J[:, idx].sum(dim=1); tot = J[idx][:, idx].sum()
            K = J.clone()
            K[idx, :] -= wJ.unsqueeze(0) / d
            K[:, idx] -= Jw.unsqueeze(1) / d
            K[idx.unsqueeze(1), idx.unsqueeze(0)] += tot / (d * d)
            K = (K + K.conj().T) / 2
            wk = t.linalg.eigvalsh(K)
            mx = float(t.max(t.abs(wk)).item())
            info["ccp_min_rel"] = float(wk.min().item()) / mx if mx > 0 else 0.0
            del J, K
        if S_true is not None:
            # o certificado do ramo pelo ARNES (que conhece o gerador verdadeiro): o logaritmo principal reproduziu S?
            info["gen_rel_dev"] = float((t.linalg.vector_norm(Lh - S_true) / t.linalg.vector_norm(S_true)).item())
        del Lh
        return diag, info


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


def fit_root_law(M, k, gamma_anti):
    """O ESTIMADOR CEGO: recebe so M (o bloco diagonal centrado da matriz de Kossakowski), k (a forma do K da teoria) e gamma_anti. M ~ gamma*beta*v v^T com
    v = u - mean(u), u_i = k_i^p (k_i = 0 no nucleo). O vetor dominante e' e = v/|v|; no nucleo todas as entradas valem -mean(u)/|v|, logo
    y_i = e_i - e_nucleo = k_i^p/|v| na periferia e ln y_i = p ln k_i - ln|v|: REGRESSAO LOG-LINEAR (precisao de maquina; a secao aurea da 1a versao
    parava em ~sqrt(eps)/curvatura -- achado 1 do aferidor). beta^ = lambda_1/(gamma |v|^2) = lambda_1 e^{2c}/gamma, com |v| = e^{-c} (c = o intercepto)."""
    M = (M + M.conj().T) / 2
    w, V = np.linalg.eigh(M)
    order = np.argsort(w)[::-1]
    l1 = float(w[order[0]]); l2 = float(abs(w[order[1]])) if w.size > 1 else 0.0
    out = {"rank_ratio": (l2 / l1) if l1 > 0 else float("inf"), "beta_hat": float("nan"), "p_hat": float("nan"), "misfit": float("inf")}
    e = V[:, order[0]]
    j = int(np.argmax(np.abs(e)))
    e = np.real(e * (np.conj(e[j]) / abs(e[j])))
    kk = np.asarray(k, float); per = kk > 0; core = ~per
    if l1 <= 0 or not np.any(core) or int(np.sum(per)) < 2:
        return out
    y = e[per] - float(np.mean(e[core]))
    if np.mean(y) < 0:
        y = -y
    if np.any(y <= 0):
        out["nonpositive"] = int(np.sum(y <= 0)); return out
    X = np.log(kk[per]); Y = np.log(y)
    A = np.vstack([X, np.ones_like(X)]).T
    sol, *_ = np.linalg.lstsq(A, Y, rcond=None)
    p_hat, c = float(sol[0]), float(sol[1])
    res = Y - (p_hat * X + c)
    out.update({"beta_hat": float(l1 * math.exp(2.0 * c) / gamma_anti), "p_hat": p_hat, "misfit": float(np.sqrt(np.mean(res ** 2)))})
    return out


# ----------------------------------------------------------------------------------------------------------------------------------
# E1..E8 -- o motor conferido em modelos ANALITICOS, o estimador no seu PISO e o comparador da CPU com linhas sinteticas (nenhum operador da teoria)
# ----------------------------------------------------------------------------------------------------------------------------------
def estimator_floor(seed, crit_beta, crit_p, per_config=250, near=50):
    """E7: M EXATO de posto um, d em {8,16,32,64}, n_c em {2,3,4}, p em {1/2, 1}; k uniforme em [0,5; 2,5] e, em 'near' sorteios por configuracao,
    k QUASE IGUAIS (desvio de ln k = 0,003) -- a cauda que o aferidor achou. O maximo tem de ficar <= criterio/10."""
    rg = np.random.default_rng([int(seed), TEST_CODE["E7"]])
    wb = wp = 0.0; n = 0
    for d in (8, 16, 32, 64):
        for nc in (2, 3, 4):
            for p in (0.5, 1.0):
                for t_ in range(per_config):
                    if t_ < near:
                        kper = rg.uniform(0.5, 2.5) * np.exp(rg.normal(0.0, 0.003, d - nc))
                    else:
                        kper = rg.uniform(0.5, 2.5, d - nc)
                    kk = np.zeros(d); kk[nc:] = kper
                    b = 10 ** rg.uniform(-4, -1)
                    u = np.where(kk > 0, kk ** p, 0.0); v = u - u.mean()
                    fr = fit_root_law(b * np.outer(v, v), kk, 1.0)
                    wb = max(wb, abs(fr["beta_hat"] / b - 1.0)) if fr["beta_hat"] == fr["beta_hat"] else float("inf")
                    wp = max(wp, abs(fr["p_hat"] - p)) if fr["p_hat"] == fr["p_hat"] else float("inf")
                    n += 1
    return {"n": n, "max_beta_rel_err": wb, "max_abs_p_err": wp, "limit_beta": crit_beta / 10.0, "limit_p": crit_p / 10.0,
            "ok": bool(wb <= crit_beta / 10.0 and wp <= crit_p / 10.0)}


def engine_selftest(E, tol, crit_beta=1e-6, crit_p=1e-4, seed=20261003, cpu_tol=None):
    out = []
    sz = np.array([[1, 0], [0, -1]], complex); sm = np.array([[0, 1], [0, 0]], complex)  # |0><1|
    # E1 amortecimento de amplitude: H = (w/2) sz, L = sqrt(g) sigma_- ; espectro {0, -g, -g/2 +- i w}; estacionario |0><0|
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
    # E4 o estimador cego recupera b e p = 1/2 de um gerador conhecido (d = 5, H aleatorio, + um salto fora da diagonal), sem ruido; o ramo confere
    rg = np.random.default_rng(7); d = 5
    A = rg.standard_normal((d, d)) + 1j * rg.standard_normal((d, d)); H = (A + A.conj().T) / 4
    kk = np.array([0.0, 0.0, 0.8, 1.4, 2.2]); b = 0.05
    Lo = np.zeros((d, d), complex); Lo[0, 3] = 0.9; Lo[1, 4] = 0.4
    S = E.superop(E.T(H), [E.T(np.diag(np.sqrt(b * kk))), E.T(Lo)])
    tau = 0.05
    dg, inf = E.generator_from_propagator(E.propagator(S, tau), tau, d, S_true=S)
    Cc = np.eye(d) - np.ones((d, d)) / d
    fr = fit_root_law(Cc @ dg.reshape(d, d).cpu().numpy() @ Cc, kk, 1.0)
    ok = bool(abs(fr["beta_hat"] / b - 1) < crit_beta / 10 and abs(fr["p_hat"] - 0.5) < crit_p / 10 and inf["gen_rel_dev"] <= 1e-8 and inf["ccp_min_rel"] >= -1e-9)
    out.append(("E4_blind_estimator_recovers_root_law", ok, {"beta_rel_err": abs(fr["beta_hat"] / b - 1), "p_err": abs(fr["p_hat"] - 0.5), **inf}))
    # E5 qubit termico (balanco detalhado): rho_ss = diag(n+1, n)/(2n+1); Spohn monotono
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
    # E7 o PISO do estimador (achado 1 do aferidor): maximo <= criterio/10, inclusive com k quase iguais
    fl = estimator_floor(seed, crit_beta, crit_p)
    out.append(("E7_estimator_floor_below_one_tenth_of_the_criterion", fl["ok"], fl))
    # E8 o COMPARADOR da referencia na CPU, com linhas sinteticas (3a afericao): igual -> concorda; CCI fora da tolerancia -> discorda; so n(c2) diferente ->
    # concorda (informacao); tudo perto do limiar -> nao comparavel; marca da rodada errada -> recusa
    ct = cpu_tol or {"cci": 1e-9, "purity": 1e-9, "folds_n_c1": 1e-9, "gap_rel_rel": 1e-6, "choi_min": 1e-9, "min_gap_rel_for_compare": 1e-6}
    sp8 = {"cpuref": {"tol": ct}}; me8 = {"run_id": "e8", "spec_sha256": "x", "beta_hex": "0x1p-7", "worker_sha256": "w"}
    g8 = {"status": "UNIQUE", "gap_rel": 1e-3, "cci": 0.5, "purity": 0.4, "folds": [{"n": 2.9}, {"n": 2.1}], "choi_min": 0.0}
    c8 = {"status": "UNIQUE", "gap_rel": 1e-3, "cci": 0.5, "purity": 0.4, "folds_n_c1": 2.9, "folds_n_c2": 2.1, "choi_min": 0.0}
    cpu8 = lambda items, meta=me8: dict(meta, items=items)
    r_eq = compare_cpuref(sp8, {"a": g8, "b": g8}, cpu8({"a": c8, "b": c8}), me8, 0)
    r_cc = compare_cpuref(sp8, {"a": g8, "b": g8}, cpu8({"a": c8, "b": dict(c8, cci=0.5 + 1e-6)}), me8, 0)
    r_n2 = compare_cpuref(sp8, {"a": g8}, cpu8({"a": dict(c8, folds_n_c2=2.1 + 1e-5)}), me8, 0)
    r_nr = compare_cpuref(sp8, {"a": dict(g8, gap_rel=1e-8)}, cpu8({"a": dict(c8, gap_rel=1e-8)}), me8, 0)
    r_mt = compare_cpuref(sp8, {"a": g8}, cpu8({"a": c8}, dict(me8, run_id="outra")), me8, 0)
    r_nm = compare_cpuref(sp8, {"a": dict(g8, gap_rel=1e-8)}, cpu8({"a": dict(c8, gap_rel=1e-8)}, dict(me8, run_id="outra")), me8, 0)   # perto do limiar + marca errada
    ok = bool(r_eq["ok"] and r_eq["compared"] == 2 and not r_cc["ok"] and r_cc["disagreements"] == 1 and r_n2["ok"] and not r_nr["ok"] and r_nr["not_comparable"]
              and not r_mt["ok"] and not r_nm["ok"] and not r_nm["not_comparable"])
    out.append(("E8_cpu_reference_comparator_selftest", ok, {"equal": r_eq["ok"], "cci_off": r_cc["ok"], "nc2_only_off": r_n2["ok"], "all_near_threshold_not_comparable": r_nr["not_comparable"],
                                                             "wrong_run_id": r_mt["ok"], "near_threshold_wrong_run_id_not_comparable": r_nm["not_comparable"]}))
    return {"checks": [{"name": n, "ok": o, "value": v} for (n, o, v) in out], "all_ok": all(o[1] for o in out)}


# ----------------------------------------------------------------------------------------------------------------------------------
# o pipeline de UMA instancia (T2, T4): espectro, estacionario, propagador, CP/TP, Spohn, dobras, CCI
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


IDENTITIES = ("ZERO_MODE", "CP", "TP", "NONRETURN", "PSD", "SS_RES", "SPOHN")


def identity_check(rec, tol):
    """Devolve (violacoes, conferidas): o MODO ZERO (n0 >= 1: tr . S = 0 garante um zero), CP, TP e o nao-retorno em toda instancia nao degenerada; PSD, o residuo do estacionario e Spohn so no atrator
    UNICO (gap ambiguo nao e' violacao de identidade); Spohn so quando o estacionario tem posto cheio. As conferidas sao CONTADAS (achado 11)."""
    v, c = [], []
    if rec.get("status") == "DEGENERATE":
        return v, c
    c.append("ZERO_MODE")
    if rec.get("n0", 1) == 0:
        v.append("ZERO_MODE")                            # tr . S = 0 garante um zero: nao acha-lo e' o motor errando, nao «ambiguo»
    if "choi_min" in rec:
        c.append("CP")
        if rec["choi_min"] < -tol["cp"]:
            v.append("CP")
    if "tp_res" in rec:
        c.append("TP")
        if rec["tp_res"] > tol["tp"]:
            v.append("TP")
    if "choi_min_inverse" in rec:
        c.append("NONRETURN")
        if rec["choi_min_inverse"] >= -tol["cp"]:
            v.append("NONRETURN")
    if rec.get("status") != "UNIQUE":
        return v, c
    c += ["PSD", "SS_RES"]
    if rec.get("ss_min_eig", 0.0) < -tol["psd"]:
        v.append("PSD")
    if rec.get("ss_res_rel", 0.0) > tol["ss_res"]:
        v.append("SS_RES")
    sp = rec.get("spohn")
    if sp and sp.get("status") == "OK":
        c.append("SPOHN")
        if sp.get("violations", 0) > 0:
            v.append("SPOHN")
    return v, c


def jline(obj):
    return json.dumps(obj, ensure_ascii=False, default=str) + chr(10)


def _err(e):
    return "%s: %s" % (type(e).__name__, str(e)[:300])


# ----------------------------------------------------------------------------------------------------------------------------------
# T2 -- a forma na escala (o sistema canonico; gamma_diss varrido, nunca calibrado)
# ----------------------------------------------------------------------------------------------------------------------------------
def gamma_grid(spec_t2, d):
    return np.logspace(math.log10(spec_t2["gamma_lo"]), math.log10(spec_t2["gamma_hi"]), int(spec_t2["n_gamma"][str(d)]))


def run_T2(E, spec, beta, prog, det):
    s2 = spec["T2"]; tol = spec["tolerances"]; op = spec["operators"]; out = {"configs": [], "identities": {}, "instance_errors": 0}
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
                try:
                    Ls, k = five_jumps(d, nc, beta, float(gd), op)
                    rec = pipeline(E, H, list(Ls.values()), d, Pi.real, tol, s2["dt"], s2["steps"], rng, want_nonreturn=(gi == mid))
                    v, c = identity_check(rec, tol)
                    rec.update({"d": d, "nc": nc, "gi": gi, "gamma_diss": float(gd), "viol": v, "checked": c})
                except Exception as e:
                    rec = {"d": d, "nc": nc, "gi": gi, "gamma_diss": float(gd), "status": "ERROR", "error": _err(e), "viol": [], "checked": []}
                    out["instance_errors"] += 1
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
        out["identities"]["VtPF_eq_PF_d%d" % d] = float(E.t.linalg.vector_norm(Pd @ x - x).item() / max(float(E.t.linalg.vector_norm(x).item()), 1e-300))
        del Sd, Pd
    return out


def summarize_T2(rows, d, nc, beta, s2):
    st = [r["status"] for r in rows]
    uniq = [r for r in rows if r["status"] == "UNIQUE"]
    um = np.array([r["status"] == "UNIQUE" for r in rows])
    g = np.array([r["gamma_diss"] for r in rows])
    cci = np.array([r.get("cci", np.nan) if r["status"] == "UNIQUE" else np.nan for r in rows])
    n1 = np.array([r["folds"][0]["n"] if (r["status"] == "UNIQUE" and "folds" in r) else np.nan for r in rows])
    n2 = np.array([r["folds"][1]["n"] if (r["status"] == "UNIQUE" and "folds" in r) else np.nan for r in rows])
    n3 = np.array([r["folds"][2]["n"] if (r["status"] == "UNIQUE" and "folds" in r) else np.nan for r in rows])
    half = um & (cci >= s2["cci_half"])
    above_uniform = um & (cci > nc / d)
    fw = s2["folds_window"]
    fwin = um & (n1 >= fw["c1"][0]) & (n1 <= fw["c1"][1]) & (n2 >= fw["c2"][0]) & (n2 <= fw["c2"][1])

    def span(mask):
        if not np.any(mask):
            return None
        return [float(g[mask].min()), float(g[mask].max()), int(mask.sum())]
    # gamma* com CCI = 1 - beta (interpolacao log-linear entre pontos UNICOS vizinhos; informativo, NAO calibracao)
    gstar = None; target = 1.0 - beta
    for i in range(len(rows) - 1):
        a, b = cci[i], cci[i + 1]
        if np.isfinite(a) and np.isfinite(b) and (a - target) * (b - target) <= 0 and a != b:
            fr = (target - a) / (b - a)
            gstar = float(10 ** (math.log10(g[i]) + fr * (math.log10(g[i + 1]) - math.log10(g[i]))))
            break
    nr = [r.get("choi_min_inverse") for r in rows if r.get("choi_min_inverse") is not None]
    checked = {k: sum(1 for r in rows if k in r.get("checked", [])) for k in IDENTITIES}
    fin = lambda a_: [float(np.nanmin(a_)), float(np.nanmax(a_))] if np.any(np.isfinite(a_)) else None
    return {"d": d, "nc": nc, "n_points": len(rows), "unique": st.count("UNIQUE"), "degenerate": st.count("DEGENERATE"), "ambiguous": st.count("AMBIGUOUS"),
            "errors": st.count("ERROR"), "gap_rel_min": float(min((r["gap_rel"] for r in uniq), default=float("nan"))),
            "cci_range_unique": fin(cci), "cci_half_window": span(half), "cci_above_uniform_window": span(above_uniform), "folds_window": span(fwin),
            "n_folds_range_unique": {"c1": fin(n1), "c2": fin(n2), "c3": fin(n3)},
            "gamma_star_cci_1_minus_beta": gstar, "identity_violations": sum(len(r["viol"]) for r in rows), "identities_checked": checked,
            "nonreturn_choi_min_inverse": nr[0] if nr else None}


# ----------------------------------------------------------------------------------------------------------------------------------
# T1 -- o INSTRUMENTO: a lei INJETADA recuperada AS CEGAS do sistema aberto inteiro (tomografia do processo; o estimador nao ve beta nem a lei)
# ----------------------------------------------------------------------------------------------------------------------------------
def t1_instance(E, spec, d, idx, law_power, test_code, with_noise):
    s1 = spec["T1"]; op = spec["operators"]; tol = spec["tolerances"]
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
    Phi = E.propagator(S, s1["tau"])        # S fica: o arnes certifica o ramo comparando L^ com o gerador verdadeiro (o estimador NAO ve S)
    Cc = np.eye(d) - np.ones((d, d)) / d
    out = []
    gen = E.t.Generator(device=E.dev); gen.manual_seed(int(r.integers(0, 2 ** 62)))
    for sigma in s1["noise"]:
        if sigma > 0 and not with_noise:
            continue
        if sigma > 0:
            Nz = (E.t.randn(Phi.shape, generator=gen, dtype=E.t.float64, device=E.dev) + 1j * E.t.randn(Phi.shape, generator=gen, dtype=E.t.float64, device=E.dev)) / math.sqrt(2)
            Phin = Phi + sigma * Nz; del Nz
        else:
            Phin = Phi
        dg, inf = E.generator_from_propagator(Phin, s1["tau"], d, S_true=S)
        M = Cc @ dg.reshape(d, d).cpu().numpy() @ Cc
        fr = fit_root_law(M, k, op.get("anti_gamma", 1.0))      # CEGO: so M, k e gamma_anti
        # sigma = 0: o certificado a posteriori (gen_rel_dev contra o S verdadeiro, que so o arnes conhece) E a Choi projetada >= -tol (L^ e' Lindblad legitimo);
        # sigma > 0: so o certificado -- a Choi projetada recebe o ruido no seu nucleo enorme (autovalores ~ -sigma d/tau) e vira so informacao (achado 1 da 2a passada)
        branch_ok = bool((inf["gen_rel_dev"] <= s1["branch_dev_sigma0"] and inf["ccp_min_rel"] >= -tol["ccp_rel"]) if sigma == 0
                         else inf["gen_rel_dev"] <= s1["branch_dev_noisy"])
        out.append({"sigma": sigma, "beta_rel_err": (abs(fr["beta_hat"] / beta_inj - 1.0) if fr["beta_hat"] == fr["beta_hat"] else float("inf")),
                    "p_hat": fr["p_hat"], "misfit": fr["misfit"], "rank_ratio": fr["rank_ratio"], "branch_ok": branch_ok, **inf})
        if sigma > 0:
            del Phin
    del Phi, S
    return {"d": d, "nc": nc, "idx": idx, "law_power_injected": law_power, "beta_inj": beta_inj, "gamma_diss": gd, "levels": out}


def run_T1(E, spec, prog, det, law_power=0.5, counts=None, noise_subset=None, test_code=None, phase="T1"):
    s1 = spec["T1"]; test_code = test_code or TEST_CODE["T1"]
    counts = counts if counts is not None else s1["d_counts"]
    noise_subset = noise_subset if noise_subset is not None else s1["noise_subset"]
    total = sum(int(v) for v in counts.values()); done = 0; per = {}
    for ds, n in counts.items():
        d = int(ds); rows = []; errs = 0
        for idx in range(int(n)):
            try:
                rec = t1_instance(E, spec, d, idx, law_power, test_code, with_noise=(idx < int(noise_subset.get(ds, 0))))
            except Exception as e:
                rec = {"d": d, "idx": idx, "error": _err(e), "levels": []}; errs += 1
            rows.append(rec); det.write(jline(dict(T=phase, **rec)))
            done += 1; prog.set(phase=phase, done=done, total=total)
        per[ds] = summarize_T1(rows, s1, law_power); per[ds]["errors"] = errs
    return per


def summarize_T1(rows, s1, law_power):
    out = {"n": len(rows)}
    for sigma in s1["noise"]:
        lv = [l for r in rows for l in r.get("levels", []) if l["sigma"] == sigma]
        be = np.array([l["beta_rel_err"] for l in lv]); pe = np.array([l["p_hat"] for l in lv], float)
        br = np.array([l["branch_ok"] for l in lv])
        crit = s1["pass"].get(repr(float(sigma)))
        ok_frac = None
        if crit is not None and len(lv):
            okm = (be <= crit["beta_rel"]) & (np.abs(pe - law_power) <= crit["p_abs"]) & br
            ok_frac = float(np.mean(okm))
        out["sigma_%s" % repr(float(sigma))] = {
            "n": len(lv), "median_beta_rel_err": float(np.median(be)) if be.size else None, "max_beta_rel_err": float(np.max(be)) if be.size else None,
            "median_abs_p_err": float(np.nanmedian(np.abs(pe - law_power))) if pe.size else None, "max_abs_p_err": float(np.nanmax(np.abs(pe - law_power))) if pe.size else None,
            "branch_ok_frac": float(np.mean(br)) if br.size else None, "pass_frac": ok_frac, "required_frac": (crit or {}).get("min_frac"),
            "n_nonfinite_beta": int(np.sum(~np.isfinite(be))) if be.size else 0,
            "root_law_rejected_frac": float(np.mean(np.abs(pe - 0.5) > 0.1)) if pe.size else None}
    return out


# ----------------------------------------------------------------------------------------------------------------------------------
# T3 -- os controles que TEM de falhar (N1, N3, N4, N5) e a IDENTIDADE unital (N2: I/d e' estacionario sem os saltos nao unitais)
# ----------------------------------------------------------------------------------------------------------------------------------
def run_T3(E, spec, beta, prog, det):
    s3 = spec["T3"]; tol = spec["tolerances"]; op = spec["operators"]; res = {}
    nc = s3["nc"]; gd = s3["gamma_diss"]
    total = len(s3["d"]) * 4; done = 0
    for d in s3["d"]:
        H, Pi = canonical_H(d, nc, spec["eps_H"])
        Ls, k = five_jumps(d, nc, beta, gd, op)
        r = {}
        # N1 dephasing sozinho (H = 0): o nucleo de L tem dimensao d + n_c(n_c - 1) -- o atrator NAO e' unico [kernel: IALDRhoStar.tgl_fix_iff;
        # ModularDephasingBridge.spectral_preserves_every_diagonal; a contagem e' elementar]
        S = E.superop(E.T(np.zeros((d, d))), [E.T(Ls["anti"])]); ev = E.spectrum(S); cl = Engine.classify(ev, tol["tol0_rel"], tol["gap_rel"]); del S
        r["N1_dephasing_only"] = {"status": cl["status"], "n0": cl["n0"], "expected_n0": d + nc * (nc - 1),
                                  "failed_as_required": bool(cl["status"] == "DEGENERATE" and cl["n0"] == d + nc * (nc - 1))}
        done += 1; prog.set(phase="T3", done=done, total=total)
        # N2 (IDENTIDADE, achado 5): a parte unital (H_LD + so o dephasing) deixa I/d estacionario -- a morte termica e' ponto fixo; status e gap informativos
        S = E.superop(E.T(H), [E.T(Ls["anti"])])
        ures = E.unital_residual(S, d)
        ev = E.spectrum(S); cl = Engine.classify(ev, tol["tol0_rel"], tol["gap_rel"]); del S
        r["N2_unital_identity"] = {"unital_residual_rel": ures, "identity_ok": bool(ures <= tol["identity_rel"]), "info_status": cl["status"],
                                   "info_n0": cl["n0"], "info_gap_rel": cl["gap_rel"], "cci_of_I_over_d": nc / d}
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
    # N3 a lei LINEAR injetada (u = k): o estimador cego TEM de recuperar a lei injetada (p ~ 1 e beta dentro do criterio) e rejeitar a lei-raiz
    res["N3_linear_law"] = run_T1(E, spec, prog, det, law_power=1.0, counts=s3["N3_counts"], noise_subset={}, test_code=TEST_CODE["N3"], phase="T3_N3")
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
        d = int(ds)
        agg = {"n": 0, "UNIQUE": 0, "DEGENERATE": 0, "AMBIGUOUS": 0, "ERROR": 0, "viol": {}, "checked": {k: 0 for k in IDENTITIES},
               "all_identities_checked": 0, "cci_above_uniform": 0, "rotated": 0, "gap_rel_min": None}
        for idx in range(int(n)):
            try:
                H, Ls, Pi, nc, rot, r = t4_instance(spec, d, idx)
                rec = pipeline(E, H, Ls, d, Pi, tol, s4["dt"], s4["steps"], r)
                v, c = identity_check(rec, tol)
            except Exception as e:
                agg["n"] += 1; agg["ERROR"] += 1
                det.write(jline({"T": "T4", "d": d, "idx": idx, "status": "ERROR", "error": _err(e)}))
                done += 1; prog.set(phase="T4", done=done, total=total)
                continue
            agg["n"] += 1; agg[rec["status"]] += 1; agg["rotated"] += int(rot)
            for x in v:
                agg["viol"][x] = agg["viol"].get(x, 0) + 1
            for x in c:
                agg["checked"][x] += 1
            if set(c) >= {"ZERO_MODE", "CP", "TP", "PSD", "SS_RES", "SPOHN"}:
                agg["all_identities_checked"] += 1
            if rec["status"] == "UNIQUE":
                agg["gap_rel_min"] = rec["gap_rel"] if agg["gap_rel_min"] is None else min(agg["gap_rel_min"], rec["gap_rel"])
                if rec.get("cci", 0) > nc / d:
                    agg["cci_above_uniform"] += 1
            det.write(jline({"T": "T4", "d": d, "idx": idx, "nc": nc, "rot": rot, "status": rec["status"], "viol": v, "checked": c,
                             "gap_rel": rec.get("gap_rel"), "cci": rec.get("cci")}))
            done += 1; prog.set(phase="T4", done=done, total=total)
        per[ds] = agg
    return per


# ----------------------------------------------------------------------------------------------------------------------------------
# D128 -- uma instancia canonica em d = 128 (superoperador 16384 x 16384): espectro, estacionario, dobras; Spohn por RK4 em d x d (informativo)
# ----------------------------------------------------------------------------------------------------------------------------------
def lindblad_rhs(H, Ls, LdLsum, rho):
    out = -1j * (H @ rho - rho @ H) - 0.5 * (LdLsum @ rho + rho @ LdLsum)
    for L in Ls:
        out = out + L @ rho @ L.conj().T
    return out


def run_D128(E, spec, beta, prog, on_spectrum=None):
    sd = spec["D128"]; tol = spec["tolerances"]; t = E.t
    d, nc, gd = sd["d"], sd["nc"], sd["gamma_diss"]
    out = {"d": d, "nc": nc, "gamma_diss": gd, "started": True}
    try:
        H, Pi = canonical_H(d, nc, spec["eps_H"])
        Ls, k = five_jumps(d, nc, beta, gd, spec["operators"])
        Hg = E.T(H); Lg = [E.T(L) for L in Ls.values()]
        prog.set(phase="D128", step="superop", force=True)
        S = E.superop(Hg, Lg); E.sync()
        prog.set(phase="D128", step="spectrum", force=True)
        t0 = time.time(); ev = E.spectrum(S); out["spectrum_s"] = time.time() - t0
        cl = Engine.classify(ev, tol["tol0_rel"], tol["gap_rel"]); out.update({k2: cl[k2] for k2 in ("status", "n0", "gap", "gap_rel", "scale", "max_re")})
        out["zero_mode_ok"] = bool(cl["n0"] >= 1)      # a IDENTIDADE do modo zero tambem em d = 128 (tr . S = 0 garante um zero; 3a afericao)
        if on_spectrum is not None:                     # o parcial ja leva n0 e zero_mode_ok: sobrevive a uma MORTE do processo depois do espectro (5a afericao)
            try:
                on_spectrum(dict(out))
            except Exception as e_:
                out["partial_write_error"] = _err(e_)   # a falha da gravacao do parcial deixa marca (6a afericao)
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
            states = init_states(E, d, rng_for(spec["seed"], TEST_CODE["D128"], d))
            h = sd["rk4_dt"]; viol = 0; Dprev = None; maxrise = -float("inf")
            t0 = time.time()
            for s in range(sd["rk4_steps"] + 1):
                if s % 50 == 0:
                    prog.set(phase="D128", step="spohn_rk4", rk4_step=s)   # confere o pai a cada 20 s no maximo (3a afericao)
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
            out["spohn_rk4_informative"] = {"violations": viol, "max_rise": maxrise, "steps": sd["rk4_steps"], "dt": h, "s": time.time() - t0}
        else:
            del S
        out["ran"] = True; out["status_code"] = "RAN"
    except Exception as e:
        out["ran"] = False; out["status_code"] = "NOT_RUN_ERROR_" + type(e).__name__.upper(); out["error"] = _err(e)
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


def run_cpuref(spec, beta, outdir, meta, parent_pid=None):
    import scipy.linalg as sl
    s2 = spec["T2"]; tol = spec["tolerances"]; op = spec["operators"]; out = {}
    t0 = time.time()
    for (d, nc, gi) in cpuref_items(spec):
        if not parent_alive(parent_pid):                # o trabalhador morreu (por exemplo, queda nativa): o filho nao fica orfao (3a afericao)
            raise ParentGone("o trabalhador %s nao vive mais" % parent_pid)
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
            fo = folds(w, d)
            rec.update({"cci": float(np.real(np.trace(Pi.real @ rho))), "purity": float(np.real(np.trace(rho @ rho))), "ss_min_eig": float(w.min()),
                        "folds_n_c1": fo[0]["n_folds"], "folds_n_c2": fo[1]["n_folds"]})
            P = sl.expm(s2["dt"] * S)
            J = P.reshape(d, d, d, d).transpose(0, 2, 1, 3).reshape(n, n); J = (J + J.conj().T) / 2
            rec["choi_min"] = float(np.linalg.eigvalsh(J).min())
        out["%d_%d_%d" % (d, nc, gi)] = rec
    res = dict(meta); res.update({"worker": WORKER_ID, "mode": "cpuref", "items": out, "n": len(out), "seconds": time.time() - t0, "numpy": np.__version__})
    write_result(os.path.join(outdir, "cpuref.json"), res)
    return res


def compare_cpuref(spec, gpu_rows, cpu, meta, child_rc):
    tol = spec["cpuref"]["tol"]; bad = []; n = 0
    maxd = {"cci": 0.0, "purity": 0.0, "folds_n_c1": 0.0, "folds_n_c2": 0.0, "gap_rel_rel": 0.0, "choi_min": 0.0}
    meta_ok = all(cpu.get(k) == v for k, v in meta.items())
    gmin = tol["min_gap_rel_for_compare"]; near = 0
    for key, c in (cpu.get("items") or {}).items():
        g = gpu_rows.get(key)
        if g is None:
            bad.append((key, "GPU_ROW_MISSING")); continue
        n += 1
        if min(float(g.get("gap_rel") or 0.0), float(c.get("gap_rel") or 0.0)) < gmin:
            near += 1; continue                          # perto do limiar: relatado, nao comparado (o status pode virar entre bibliotecas corretas)
        if g["status"] != c["status"]:
            bad.append((key, "STATUS %s != %s" % (g["status"], c["status"]))); continue
        if c["status"] != "UNIQUE":
            continue
        dd = {"cci": abs(g["cci"] - c["cci"]), "purity": abs(g["purity"] - c["purity"]), "folds_n_c1": abs(g["folds"][0]["n"] - c["folds_n_c1"]),
              "folds_n_c2": abs(g["folds"][1]["n"] - c["folds_n_c2"]), "gap_rel_rel": abs(g["gap_rel"] - c["gap_rel"]) / max(abs(c["gap_rel"]), 1e-300),
              "choi_min": abs(g["choi_min"] - c["choi_min"])}
        for k_, v_ in dd.items():
            maxd[k_] = max(maxd[k_], v_)
        if any(dd[k_] > tol[k_] for k_ in dd if k_ in tol):     # so as chaves com tolerancia no spec decidem; n(c2) e' INFORMACAO (3a afericao)
            bad.append((key, "TOL"))
    return {"read": n, "compared": n - near, "near_threshold_not_compared": near,
            "not_comparable": bool(n > 0 and n == near and meta_ok and child_rc == 0 and not bad),   # so a referencia DESTA rodada, completa (4a afericao)
            "disagreements": len(bad),
            "first_disagreements": bad[:10], "max_diffs": maxd, "informative_only": sorted(k_ for k_ in maxd if k_ not in tol), "meta_ok": meta_ok,
            "child_rc": child_rc, "ok": bool(n > near and not bad and meta_ok and child_rc == 0)}


# ----------------------------------------------------------------------------------------------------------------------------------
# a sonda de tempo do proprio pipeline -- SO hardware: operadores ALEATORIOS densos, nenhum operador da teoria
# ----------------------------------------------------------------------------------------------------------------------------------
def run_timing(E, outdir, reps=None):
    reps = reps or {8: 30, 16: 10, 32: 4, 64: 3}   # d = 64 com 3 repeticoes: a mediana tira o custo de arranque do MAGMA na primeira chamada
    tol = {"tol0_rel": 1e-10, "gap_rel": 1e-8, "spohn_abs": 1e-10, "spohn_rel": 1e-9}
    res = {}
    for d, nrep in reps.items():
        rg = np.random.default_rng([TEST_CODE["TIMING"], d]); tp = []; t1 = []; t1n = []
        for _ in range(nrep):
            A = rg.standard_normal((d, d)) + 1j * rg.standard_normal((d, d)); H = (A + A.conj().T) / 2
            Ls = [(rg.standard_normal((d, d)) + 1j * rg.standard_normal((d, d))) / d for _ in range(5)]
            Pi = np.zeros((d, d)); Pi[:2, :2] = np.eye(2)
            E.sync(); a = time.time(); pipeline(E, H, Ls, d, Pi, tol, 0.05, 64, rg); E.sync(); tp.append(time.time() - a)
            a = time.time()
            S = E.superop(E.T(H), [E.T(L) for L in Ls]); Phi = E.propagator(S, 0.05)
            kk = np.r_[np.zeros(2), np.linspace(0.5, 2.5, d - 2)]; Cc = np.eye(d) - np.ones((d, d)) / d
            dg, inf = E.generator_from_propagator(Phi, 0.05, d, S_true=S)
            fit_root_law(Cc @ dg.reshape(d, d).cpu().numpy() @ Cc, kk, 1.0); E.sync(); t1.append(time.time() - a)
            a = time.time()
            dg, inf = E.generator_from_propagator(Phi + 1e-8 * E.T(rg.standard_normal(Phi.shape)), 0.05, d, S_true=S)
            fit_root_law(Cc @ dg.reshape(d, d).cpu().numpy() @ Cc, kk, 1.0); E.sync(); t1n.append(time.time() - a)
            del Phi, S
        res[str(d)] = {"pipeline_s": float(np.median(tp)), "t1_injection_sigma0_s": float(np.median(t1)), "t1_extra_noise_level_s": float(np.median(t1n)), "reps": nrep}
        print("timing d=%d" % d, res[str(d)], flush=True)
    return res


# ----------------------------------------------------------------------------------------------------------------------------------
# a arvore de vereditos (congelada no pre-registro; o um.py a REDERIVA destes mesmos numeros, com este mesmo codigo)
# ----------------------------------------------------------------------------------------------------------------------------------
def derive_verdict(spec, R):
    P = "TGL_QUANTUM_PILLAR_V1__"
    if R.get("fatal"):
        return P + "NOT_RUN__" + ("PARENT_GONE" if R.get("parent_gone") else "WORKER_FATAL") + "__GATE_UNTOUCHED"
    if R.get("refused"):
        return P + "NOT_RUN__" + R["refused"] + "__GATE_UNTOUCHED"
    if not (R.get("engine_selftest") or {}).get("all_ok"):
        return P + "ENGINE_SELFTEST_FAILED__NO_RESULT__GATE_UNTOUCHED"
    for ph in ("T3", "T2", "T1", "T4"):
        if not isinstance(R.get(ph), dict) or R[ph].get("error"):
            return P + "PHASE_%s_FAILED__RESULTS_INCOMPLETE__GATE_UNTOUCHED" % ph
    tol = spec["tolerances"]
    # 0. excecao em qualquer instancia: o motor e' suspeito (achado 9)
    ne = R["T2"].get("instance_errors", 0) + sum(a.get("ERROR", 0) for a in R["T4"].values()) + sum(s.get("errors", 0) for s in R["T1"].values())
    ne += sum(s.get("errors", 0) for s in (R["T3"].get("N3_linear_law") or {}).values())
    if ne > 0:
        return P + "INSTANCE_ERRORS_%d__ENGINE_SUSPECT__RESULTS_VOID__GATE_UNTOUCHED" % ne
    # 1. os controles TEM de falhar (N1, N4, N5 em cada d; N3: a lei linear injetada recuperada -- p e beta -- e a lei-raiz rejeitada, 100% sem ruido)
    t3 = R["T3"]; ctl_ok = True
    for dk, r in t3.items():
        if dk.startswith("d"):
            for nm in ("N1_dephasing_only", "N4_negative_rate_not_cp", "N5_time_reversal_not_cp"):
                ctl_ok = ctl_ok and bool((r.get(nm) or {}).get("failed_as_required"))
    n3 = t3.get("N3_linear_law") or {}
    ctl_ok = ctl_ok and bool(n3)
    for ds, s in n3.items():
        lv = s.get("sigma_0.0") or {}
        ctl_ok = ctl_ok and (lv.get("pass_frac") == 1.0) and (lv.get("root_law_rejected_frac") == 1.0)
    if not ctl_ok:
        return P + "CONTROL_DID_NOT_FAIL__INSTRUMENT_BLIND__RESULTS_VOID__GATE_UNTOUCHED"
    # 2. as identidades (o modo zero no T2, no T4 e no D128; CP, TP, nao-retorno, PSD, residuo, Spohn; V_t P_F = P_F; sin^2 theta_M = beta; N2: I/d estacionario na parte unital)
    nv = sum(c["identity_violations"] for c in R["T2"]["configs"])
    nv += sum(sum(a["viol"].values()) for a in R["T4"].values())
    ids = R["T2"]["identities"]
    nv += int(ids.get("sin2_thetaM_minus_beta", 1.0) > tol["identity_abs"])
    nv += sum(int(v > tol["identity_rel"]) for k, v in ids.items() if k.startswith("VtPF"))
    nv += sum(int(not (r.get("N2_unital_identity") or {}).get("identity_ok")) for dk, r in t3.items() if dk.startswith("d"))
    nv += int((R.get("D128") or {}).get("zero_mode_ok") is False)   # o modo zero em d = 128: conta mesmo se o D128 cair DEPOIS do espectro (4a afericao)
    if nv > 0:
        return P + "IDENTITY_VIOLATED_%d__ENGINE_SUSPECT__RESULTS_VOID__GATE_UNTOUCHED" % nv
    # 3. a referencia na CPU (conferida pela marca da rodada e pelo codigo de saida do filho)
    if not (R.get("cpuref_compare") or {}).get("ok"):
        if (R.get("cpuref_compare") or {}).get("not_comparable"):
            return P + "CPU_REFERENCE_NOT_COMPARABLE__RESULTS_VOID__GATE_UNTOUCHED"     # nenhum ponto longe do limiar: nao houve discordancia, nem conferencia
        return P + "CPU_REFERENCE_DISAGREES_OR_ABSENT__RESULTS_VOID__GATE_UNTOUCHED"
    # 4. os resultados (janelas so com atrator UNICO; 'na grade')
    cf = R["T2"]["configs"]; npts = sum(c["n_points"] for c in cf); nun = sum(c["unique"] for c in cf)
    uniq = ("ALL_%d" % npts) if nun == npts else ("%d_OF_%d" % (nun, npts))
    t1 = R["T1"]; rec0 = bool(t1) and all((s.get("sigma_0.0") or {}).get("pass_frac") == 1.0 for s in t1.values())
    inst = "T1_INSTRUMENT_RECOVERS_INJECTED_LAW_BLIND" if rec0 else "T1_INSTRUMENT_DOES_NOT_RECOVER_INJECTED_LAW"
    nconf = len(cf); fw = sum(1 for c in cf if c["folds_window"]); nm = sum(1 for c in cf if c["cci_half_window"])
    t4 = R["T4"]; n4 = sum(a["n"] for a in t4.values()); u4 = sum(a["UNIQUE"] for a in t4.values()); m4 = sum(a["all_identities_checked"] for a in t4.values())
    dd = R.get("D128") or {}
    _sc = str(dd.get("status_code") or "NOT_RUN")
    d128 = ("D128_" + dd.get("status", "NA")) if dd.get("ran") else ("D128_INTERRUPTED" if _sc == "STARTED" else "D128_" + _sc)   # STARTED so persiste se o processo morreu no meio
    return (P + "FIVE_JUMP_GKLS__ATTRACTOR_UNIQUE_%s_ON_THE_GRID__%s__CONTROLS_FAILED_AS_REQUIRED__IDENTITIES_HOLD__STRESS_%d_INSTANCES_%d_UNIQUE_ALL_IDENTITIES_CHECKED_IN_%d__"
            "NAME_IN_CORE_%d_OF_%d_ON_THE_GRID__FOLDS_WINDOW_%d_OF_%d_ON_THE_GRID__%s__CPU_REFERENCE_AGREES__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED"
            % (uniq, inst, n4, u4, m4, nm, nconf, fw, nconf, d128))


# ----------------------------------------------------------------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------------------------------------------------------------
def _below_normal_flags():
    if os.name == "nt":
        return 0x00004000   # BELOW_NORMAL_PRIORITY_CLASS: o rito tem prioridade sobre a CPU
    return 0


FRESH_GUARD = ("result.json", "result.json.sha256", "result_partial.json", "cpuref.json", "cpuref_error.json", "details.jsonl", "progress.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["run", "engine", "timing", "cpuref"])
    ap.add_argument("--spec"); ap.add_argument("--spec-sha256"); ap.add_argument("--beta-hex"); ap.add_argument("--run-id"); ap.add_argument("--parent-pid", type=int); ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    me = os.path.abspath(__file__)
    my_sha = sha256_bytes(open(me, "rb").read())
    if args.mode == "run" and any(os.path.exists(os.path.join(args.out, f)) for f in FRESH_GUARD):
        print("RECUSO: a pasta de saida nao e' nova (ha saidas de outra rodada) -- nada escrito"); sys.exit(3)
    prog = Progress(args.out, args.run_id, args.parent_pid)
    cpu_proc = None
    R = {"worker": WORKER_ID, "mode": args.mode, "run_id": args.run_id, "started": time.strftime("%Y-%m-%d %H:%M:%S"), "worker_sha256": my_sha,
         "status_statement": "[COMPUTED] -- calculo do sistema aberto da teoria; NAO e' medicao; o gate nao muda"}
    rp = os.path.join(args.out, "result.json") if args.mode != "cpuref" else os.path.join(args.out, "cpuref_error.json")
    spec = None
    try:
        if args.mode in ("run", "cpuref"):
            if not (args.spec and args.spec_sha256 and args.beta_hex and (args.run_id or args.mode == "cpuref")):
                R["refused"] = "MISSING_ARGUMENTS"; R["verdict"] = "TGL_QUANTUM_PILLAR_V1__NOT_RUN__MISSING_ARGUMENTS__GATE_UNTOUCHED"; write_result(rp, R); sys.exit(4)
        if args.spec:
            spec = json.loads(open(args.spec, "rb").read().decode("utf-8"))
            R["spec_sha256"] = sha256_bytes(canon_json(spec).encode("utf-8"))
            if args.spec_sha256 and R["spec_sha256"] != args.spec_sha256:
                R["refused"] = "SPEC_HASH_MISMATCH"; R["verdict"] = derive_verdict(spec, R); write_result(rp, R); sys.exit(4)
            if args.mode in ("run", "cpuref") and spec.get("worker_sha256") != my_sha:
                R["refused"] = "WORKER_HASH_MISMATCH"; R["verdict"] = derive_verdict(spec, R); write_result(rp, R); sys.exit(4)
        beta = float.fromhex(args.beta_hex) if args.beta_hex else None
        R["beta_hex"] = args.beta_hex; R["beta"] = beta
        meta = {"run_id": args.run_id, "spec_sha256": R.get("spec_sha256"), "beta_hex": args.beta_hex, "worker_sha256": my_sha}
        if args.mode == "cpuref":
            run_cpuref(spec, beta, args.out, meta, parent_pid=args.parent_pid); return
        import torch
        import scipy
        R["env"] = {"torch": torch.__version__, "cuda": torch.version.cuda, "numpy": np.__version__, "scipy": scipy.__version__, "python": platform.python_version(),
                    "platform": platform.platform(), "cuda_available": bool(torch.cuda.is_available())}
        if not torch.cuda.is_available():
            R["refused"] = "GPU_UNAVAILABLE"; R["verdict"] = derive_verdict(spec, R) if spec else "TGL_QUANTUM_PILLAR_V1__NOT_RUN__GPU_UNAVAILABLE__GATE_UNTOUCHED"
            write_result(rp, R); sys.exit(6)
        torch.use_deterministic_algorithms(True)
        torch.backends.cuda.matmul.allow_tf32 = False; torch.backends.cudnn.allow_tf32 = False
        torch.set_num_threads(4)
        dev = torch.device("cuda")
        R["env"]["gpu"] = torch.cuda.get_device_name(0)
        try:
            fr_, to_ = torch.cuda.mem_get_info(); R["env"]["vram_free_total_MiB"] = [round(fr_ / 2 ** 20), round(to_ / 2 ** 20)]
        except Exception:
            pass
        R["env"]["determinism"] = {"use_deterministic_algorithms": True, "CUBLAS_WORKSPACE_CONFIG": os.environ.get("CUBLAS_WORKSPACE_CONFIG"), "tf32": False, "threads": 4}
        E = Engine(torch, dev, (((spec or {}).get("linalg") or {}).get("nonhermitian_eig_backend") or {}).get("magma_up_to_n", 10 ** 9))
        R["env"]["linalg_magma_up_to_n"] = E.magma_up_to_n
        prog.set(phase="engine_selftest", force=True)
        crit = ((spec or {}).get("T1") or {}).get("pass", {}).get("0.0") or {"beta_rel": 1e-6, "p_abs": 1e-4}
        R["engine_selftest"] = engine_selftest(E, (spec or {}).get("tolerances", {}).get("engine", 1e-9), crit["beta_rel"], crit["p_abs"], (spec or {}).get("seed", 20261003),
                                               (((spec or {}).get("cpuref") or {}).get("tol")))
        if not R["engine_selftest"]["all_ok"]:
            R["verdict"] = "TGL_QUANTUM_PILLAR_V1__ENGINE_SELFTEST_FAILED__NO_RESULT__GATE_UNTOUCHED"; write_result(rp, R); sys.exit(5)
        if args.mode == "engine":
            R["verdict"] = "ENGINE_SELFTEST_PASSED"; write_result(rp, R); return
        if args.mode == "timing":
            R["timing"] = run_timing(E, args.out); write_result(rp, R); return
        # ---------------- o rito ----------------
        import subprocess
        cpu_err = open(os.path.join(args.out, "cpuref.stderr.txt"), "w")
        cpu_proc = subprocess.Popen([sys.executable, me, "--mode", "cpuref", "--spec", args.spec, "--spec-sha256", R["spec_sha256"], "--beta-hex", args.beta_hex,
                                     "--run-id", args.run_id, "--parent-pid", str(os.getpid()), "--out", args.out],
                                    stdout=subprocess.DEVNULL, stderr=cpu_err, creationflags=_below_normal_flags())   # o filho confere o trabalhador (3a afericao)
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
                    R[ph] = {"error": _err(e), "trace": traceback.format_exc()[-2000:]}
                R["phase_seconds"][ph] = round(time.time() - t0, 1)
                det.flush()
                write_json_atomic(os.path.join(args.out, "result_partial.json"), R)
        # as linhas do T2 para a comparacao com a CPU (lidas de volta do arquivo de detalhes, pela chave d_nc_gi gravada)
        with open(detp, "r", encoding="utf-8") as fh:
            for line in fh:
                o = json.loads(line)
                if o.get("T") == "T2" and o.get("status") != "ERROR":
                    gpu_rows["%d_%d_%d" % (o["d"], o["nc"], o["gi"])] = o
        prog.set(phase="cpuref_wait", force=True)
        child_rc = None; t_w = time.time()
        while True:                                      # em fatias de 20 s: o pai e' conferido durante a espera (3a afericao)
            try:
                child_rc = cpu_proc.wait(timeout=20); break
            except subprocess.TimeoutExpired:
                prog.set(phase="cpuref_wait", force=True)      # levanta ParentGone se o um.py morreu
                if time.time() - t_w > spec["cpuref"]["timeout_s"]:
                    cpu_proc.kill(); child_rc = None; break
        cpu_err.close()
        cp = os.path.join(args.out, "cpuref.json")
        if os.path.exists(cp):
            cpu = json.load(open(cp, encoding="utf-8"))
            R["cpuref_sha256"] = sha256_bytes(open(cp, "rb").read())   # a referencia na CPU amarrada ao result.json, que o selo hasheia (3a afericao)
            R["cpuref_compare"] = compare_cpuref(spec, gpu_rows, cpu, meta, child_rc); R["cpuref_compare"]["cpu_seconds"] = cpu.get("seconds")
        else:
            R["cpuref_compare"] = {"ok": False, "error": "cpuref.json ausente", "error_code": "CPUREF_JSON_ABSENT", "child_rc": child_rc}   # o codigo: cada lingua compoe a frase (6a)
        R["details_sha256"] = sha256_bytes(open(detp, "rb").read())
        # o ponto d = 128 por ultimo, com prazo; o parcial marca que ele COMECOU (se o processo morrer no meio, o um.py le INTERROMPIDO)
        t0 = time.time()
        if time.time() - prog.t0 <= spec["D128"]["start_deadline_s"]:
            R["D128"] = {"started": True, "ran": False, "status_code": "STARTED"}
            write_json_atomic(os.path.join(args.out, "result_partial.json"), R)
            def _d128_parcial(o_):
                R["D128"] = dict(o_, ran=False, status_code="STARTED"); write_json_atomic(os.path.join(args.out, "result_partial.json"), R)
            R["D128"] = run_D128(E, spec, beta, prog, on_spectrum=_d128_parcial)
        else:
            R["D128"] = {"started": False, "ran": False, "status_code": "NOT_RUN_DEADLINE",
                         "error": "o prazo de inicio (%d s desde o comeco do trabalhador) ja tinha passado" % spec["D128"]["start_deadline_s"]}
        R["phase_seconds"]["D128"] = round(time.time() - t0, 1)
        R["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
        R["verdict"] = derive_verdict(spec, R)
        write_result(rp, R)
        try:                                             # a marca final do progresso NAO pode rebaixar um resultado completo (3a afericao)
            prog.state["phase"] = "done"; write_json_atomic(prog.p, prog.state)
        except Exception:
            pass
    except SystemExit:
        raise
    except (Exception, ParentGone) as e:
        R["fatal"] = _err(e); R["trace"] = traceback.format_exc()[-3000:]
        R["parent_gone"] = isinstance(e, ParentGone)
        R["verdict"] = derive_verdict(spec or {}, R)
        try:
            cpu_proc.kill()                              # o filho da CPU nao fica orfao (achado da 2a passada)
        except Exception:
            pass
        write_result(rp, R); sys.exit(1)


if __name__ == "__main__":
    main()
