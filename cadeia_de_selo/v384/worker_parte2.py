

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
