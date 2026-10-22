

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
    rec8 = all(((s.get("sigma_1e-08") or {}).get("pass_frac") or 0.0) >= spec["T1"]["pass"]["1e-08"]["min_frac"] for s in t1.values())
    root = "RECOVERED" if (rec0 and rec8) else "NOT_RECOVERED"
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
            for ph in ("T3", "T2", "T1", "T4", "D128"):
                t0 = time.time()
                try:
                    if ph == "T3":
                        R["T3"] = run_T3(E, spec, beta, prog, det)
                    elif ph == "T2":
                        R["T2"] = run_T2(E, spec, beta, prog, det)
                    elif ph == "T1":
                        R["T1"] = run_T1(E, spec, prog, det)
                    elif ph == "T4":
                        R["T4"] = run_T4(E, spec, prog, det)
                    else:
                        R["D128"] = run_D128(E, spec, beta, prog)
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
