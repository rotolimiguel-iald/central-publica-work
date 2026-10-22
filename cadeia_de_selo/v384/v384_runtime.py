# ===================== v384: O PILAR QUANTICO NA GPU (ordens do operador, 02-03/10/2026) =====================
# «Eu quero que a GPU rode todo o mundo quântico da TGL com os operadores de salto, todos os operadores de dephasing, o sistema aberto, enquanto o
# código roda o kernel, enquanto o código roda os testes cosmológicos [...]» (02/10); «São cinco operadores de salto, os operadores de lindblad que já
# estão descritos na teoria. Vamos parar o servidor durante o rito. [...]» (03/10); «Concordo com tudo, vamos de rito robusto, mas coloque uma ferramenta
# para que não seja necessário a cada versão nova rodar tudo de novo [...] Daí ao ter a versão final a gente roda completa sempre.» (03/10).
# O TRABALHADOR VIVE AQUI (texto embutido, materializado ao lado, como o kernel): Nao ha segundo arquivo. A especificacao congelada (o pre-registro V1,
# por hash) tambem. O rito o lanca logo depois da inscricao do Um, em paralelo com o kernel e os ritos cosmologicos; antes do artigo, espera, le, confere o
# sha256, REDERIVA o veredito pela mesma arvore (num subprocesso, com o mesmo codigo) e registra no core, no selo (AO LADO do gate) e no artigo.
# A FERRAMENTA (o reaproveitamento): chave = sha256(trabalhador + especificacao canonica + beta em hexadecimal); a rodada completa calcula e GRAVA em
# cache/checkpoints/quantum_pillar/<chave>/; com TGL_RITE_CHECKPOINT=1 (o interruptor do v321) a rodada intermediaria REAPROVEITA o gravado se a chave,
# o ambiente (torch, CUDA, numpy, scipy, Python, GPU), o sha256 e o motor (E1..E8, rodado de novo) baterem; so resultado COMPLETO vai ao cache. A versao final
# roda sem a chave, sempre. [COMPUTED]: calculo, nunca medicao; o gate nao muda.
_QP_WORKER_SRC = __QP_WORKER_SRC__
_QP_SPEC_JSON = __QP_SPEC_JSON__
_QP_SPEC_SHA256 = "__QP_SPEC_SHA256__"
_QP_PREREG = {"json": {"path": "__QP_PREREG_JSON_PATH__", "sha256": "__QP_PREREG_JSON_SHA256__"},
              "md": {"path": "__QP_PREREG_MD_PATH__", "sha256": "__QP_PREREG_MD_SHA256__"}}
# o prazo e o intervalo do progresso sao LIDOS da especificacao congelada (execution.um_py_timeout_s; execution.progress_every_s) -- achado 9 do aferidor


def _qp_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "quantum_pillar")


def _qp_canon(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _qp_materialize():
    """Escreve o trabalhador e a especificacao ao lado deste arquivo (so se mudaram; escrita atomica) e devolve os caminhos e os sha256 lidos do disco."""
    d = _qp_dir(); os.makedirs(d, exist_ok=True)
    out = {}
    for name, text in (("pilar_quantico_worker.py", _QP_WORKER_SRC), ("pilar_quantico_spec.json", _QP_SPEC_JSON)):
        p = os.path.join(d, name); b = text.encode("utf-8")
        if not (os.path.exists(p) and open(p, "rb").read() == b):
            with open(p + ".tmp", "wb") as fh:
                fh.write(b)
            os.replace(p + ".tmp", p)
        rb = open(p, "rb").read()
        if rb != b:
            raise RuntimeError("materializacao do pilar quantico divergiu: %s" % p)
        out[name] = {"path": p, "sha256": hashlib.sha256(rb).hexdigest()}
    return out


def _qp_beta():
    """beta pelo MESMO motor do run_um (forma de Lagrange; o CODATA so valida) -- nunca literal; em hexadecimal para o trabalhador (bit a bit)."""
    _q = validate_against_qed(0.0, SEALED_CODATA_ALPHA)["q_QED"]
    b = float(alpha_lagrange_form(_q)["beta_form"])
    return b, b.hex()


def _qp_key(worker_sha, spec_canon, beta_hex):
    h = hashlib.sha256()
    h.update(worker_sha.encode("ascii")); h.update(spec_canon.encode("utf-8")); h.update(beta_hex.encode("ascii"))
    return h.hexdigest()[:24]


def _qp_env_probe():
    code = ("import json,platform,torch,numpy,scipy;ok=torch.cuda.is_available();"
            "print(json.dumps({'torch':torch.__version__,'cuda':torch.version.cuda,'numpy':numpy.__version__,'scipy':scipy.__version__,"
            "'python':platform.python_version(),'gpu':(torch.cuda.get_device_name(0) if ok else None)}))")
    try:
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=300)
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception as e:
        return {"error": repr(e)}


def _qp_engine_now(mat):
    """Ao reaproveitar: o motor (E1..E8) roda de novo NO AMBIENTE PRESENTE, numa pasta nova; so reaproveita se passar (achado 8)."""
    d = os.path.join(_qp_dir(), "engine_" + time.strftime("%Y%m%d_%H%M%S"))
    os.makedirs(d, exist_ok=True)
    try:
        subprocess.run([sys.executable, mat["pilar_quantico_worker.py"]["path"], "--mode", "engine", "--spec", mat["pilar_quantico_spec.json"]["path"], "--out", d],
                       capture_output=True, text=True, timeout=900)
        r = json.load(open(os.path.join(d, "result.json"), encoding="utf-8"))
        return bool(r.get("verdict") == "ENGINE_SELFTEST_PASSED" and r.get("worker_sha256") == mat["pilar_quantico_worker.py"]["sha256"])
    except Exception:
        return False


def _qp_kill_tree(proc):
    """Encerra o trabalhador E o filho da CPU (no Windows, taskkill /T /F; fora, o grupo). Silencioso se ja saiu."""
    try:
        if proc is None or proc.poll() is not None:
            return
        if os.name == "nt":
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True, timeout=60)
        else:
            proc.kill()
        proc.wait(timeout=60)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


_QP_LIVE = {}


def _qp_atexit():
    """Se o um.py sair (excecao, interrupcao) com o trabalhador ainda vivo, a arvore e' encerrada: nada fica orfao na GPU (achado da 2a passada)."""
    st = _QP_LIVE.get("st")
    if st and not st.get("finished") and st.get("proc") is not None:
        _qp_kill_tree(st["proc"])


def _qp_cache_dir(key):
    return os.path.join(CACHE, "checkpoints", "quantum_pillar", key)


def _qp_cached_ok(cdir):
    rp = os.path.join(cdir, "result.json"); hp = rp + ".sha256"
    if not (os.path.exists(rp) and os.path.exists(hp)):
        return None
    if hashlib.sha256(open(rp, "rb").read()).hexdigest() != open(hp, encoding="ascii").read().strip():
        return None
    return json.load(open(rp, encoding="utf-8"))


def quantum_pillar_start_v384():
    """Logo depois da inscricao do Um: decide REAPROVEITAR (so com TGL_RITE_CHECKPOINT=1 e tudo batendo) ou CALCULAR (lanca o subprocesso)."""
    st = {"t0": time.time(), "mode": None, "checkpoint_switch": bool(_RITE_CKPT_ON)}
    try:
        spec = json.loads(_QP_SPEC_JSON)
        canon = _qp_canon(spec)
        if hashlib.sha256(canon.encode("utf-8")).hexdigest() != _QP_SPEC_SHA256:
            st["refused"] = "SPEC_HASH_MISMATCH_IN_UM_PY"; return st
        mat = _qp_materialize()
        b, bhex = _qp_beta()
        key = _qp_key(mat["pilar_quantico_worker.py"]["sha256"], canon, bhex)
        st.update({"key": key, "beta": b, "beta_hex": bhex, "materialized": mat})
        cdir = _qp_cache_dir(key)
        if _RITE_CKPT_ON:
            cached = _qp_cached_ok(cdir)
            if cached is not None:
                env = _qp_env_probe(); cenv = cached.get("env") or {}
                same = all(env.get(k) == cenv.get(k) for k in ("torch", "cuda", "numpy", "scipy", "python", "gpu"))
                if same and str(cached.get("verdict", "")).startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__") and _qp_engine_now(mat):
                    st.update({"mode": "REUSE", "cache_dir": cdir, "env_now": env})
                    print("[v384] pilar quantico: REAPROVEITADO da rodada de %s (chave %s) -- a versao FINAL roda sem TGL_RITE_CHECKPOINT" % (cached.get("finished"), key), flush=True)
                    return st
                st["reuse_refused"] = {"env_now": env, "env_cached": {k: cenv.get(k) for k in ("torch", "cuda", "numpy", "scipy", "python", "gpu")}}
        import uuid
        run_id = uuid.uuid4().hex                     # a MARCA UNICA da rodada (achado 7): conferida em todas as saidas
        run_dir = os.path.join(_qp_dir(), "run_" + time.strftime("%Y%m%d_%H%M%S") + "_" + run_id[:8])
        os.makedirs(run_dir, exist_ok=False)
        st["run_dir"] = run_dir   # ja aqui: o marcador mede esta pasta mesmo se o lancamento falhar (8a afericao)
        flags = 0x00004000 if os.name == "nt" else 0   # BELOW_NORMAL_PRIORITY_CLASS: o rito tem a vez na CPU
        env = dict(os.environ); env["PYTHONIOENCODING"] = "utf-8"
        logf = open(os.path.join(run_dir, "worker_stdout.txt"), "w", encoding="utf-8")
        proc = subprocess.Popen([sys.executable, mat["pilar_quantico_worker.py"]["path"], "--mode", "run", "--spec", mat["pilar_quantico_spec.json"]["path"],
                                 "--spec-sha256", _QP_SPEC_SHA256, "--beta-hex", bhex, "--run-id", run_id, "--parent-pid", str(os.getpid()), "--out", run_dir],
                                stdout=logf, stderr=subprocess.STDOUT, env=env, creationflags=flags)
        import atexit
        _QP_LIVE["st"] = st; atexit.register(_qp_atexit)
        st.update({"mode": "COMPUTE", "proc": proc, "run_dir": run_dir, "log": logf, "cache_dir": cdir, "run_id": run_id,
                   "timeout_s": int(spec["execution"]["um_py_timeout_s"]), "progress_every_s": int(spec["execution"]["progress_every_s"])})
        print("[v384] pilar quantico: o trabalhador da GPU foi lancado (PID %d), em paralelo com o kernel e os ritos cosmologicos; chave %s" % (proc.pid, key), flush=True)
    except Exception as e:
        st["refused"] = "LAUNCH_FAILED: %r" % (e,)
    return st


def _qp_wait(st):
    proc = st["proc"]; last = 0.0; timed_out = False
    while True:
        rc = proc.poll()
        if rc is not None:
            break
        el = time.time() - st["t0"]
        if el > st["timeout_s"]:
            _qp_kill_tree(proc); timed_out = True; rc = None; break
        if time.time() - last >= st["progress_every_s"]:
            last = time.time()
            try:
                pg = json.load(open(os.path.join(st["run_dir"], "progress.json"), encoding="utf-8"))
                print("   [v384] pilar quantico em curso: fase %s, %s/%s, %.0f min desde o lancamento" % (pg.get("phase"), pg.get("done", "-"), pg.get("total", "-"), el / 60), flush=True)
            except Exception:
                print("   [v384] pilar quantico em curso: %.0f min desde o lancamento" % (el / 60), flush=True)
        time.sleep(5)
    try:
        st["log"].close()
    except Exception:
        pass
    return rc, timed_out


def _qp_rederive(st, result_path):
    """O veredito REDERIVADO pela mesma arvore, num subprocesso com o mesmo codigo (o processo do rito nao importa torch)."""
    mat = st["materialized"]
    code = ("import json,sys,importlib.util;s=importlib.util.spec_from_file_location('w',sys.argv[1]);w=importlib.util.module_from_spec(s);s.loader.exec_module(w);"
            "spec=json.load(open(sys.argv[2],encoding='utf-8'));R=json.load(open(sys.argv[3],encoding='utf-8'));print(w.derive_verdict(spec,R))")
    r = subprocess.run([sys.executable, "-c", code, mat["pilar_quantico_worker.py"]["path"], mat["pilar_quantico_spec.json"]["path"], result_path],
                       capture_output=True, text=True, timeout=300, encoding="utf-8")
    return r.stdout.strip().splitlines()[-1] if r.stdout.strip() else None


def _qp_save_cache(st, R_path):
    cdir = st["cache_dir"]; tmp = cdir + ".tmp_" + time.strftime("%Y%m%d_%H%M%S")
    os.makedirs(tmp, exist_ok=True)
    for f in ("result.json", "result.json.sha256", "details.jsonl", "cpuref.json", "progress.json", "worker_stdout.txt"):
        p = os.path.join(st["run_dir"], f)
        if os.path.exists(p):
            shutil.copyfile(p, os.path.join(tmp, f))
    old = None
    if os.path.isdir(cdir):
        old = cdir + ".old_" + time.strftime("%Y%m%d_%H%M%S")
        os.replace(cdir, old)
    try:
        os.replace(tmp, cdir)
    except Exception as e1:
        e2 = None
        if old:                                          # a troca falhou: o cache antigo VOLTA ao lugar (3a afericao); se a volta falhar, isso fica dito (4a)
            try:
                os.replace(old, cdir)
            except Exception as e_r:
                e2 = e_r
        shutil.rmtree(tmp, ignore_errors=True)
        raise RuntimeError("a troca do cache falhou: %r; a volta do antigo: %s" % (e1, ("FALHOU: %r (o antigo ficou em %s)" % (e2, old)) if e2 else ("ok" if old else "nao havia antigo")))
    if old:
        shutil.rmtree(old, ignore_errors=True)
    return cdir


def _qp_retry(fn, n=40, dt=0.25):
    """Tenta de novo SO PermissionError (como o write_json_atomic do trabalhador): um leitor ou o antivirus segurando o arquivo por instantes nao derruba a
    escrita; FileNotFoundError e os demais erros sobem na hora (6a afericao)."""
    for i_ in range(n):
        try:
            return fn()
        except PermissionError:
            if i_ == n - 1:
                raise
            time.sleep(dt)


def _qp_out_marker(verdict, st, reason):
    """O um_absoluto_pilar_quantico.json do Nos sem o resultado DESTA rodada: um marcador desta rodada (troca atomica, com novas tentativas), com o MOTIVO;
    devolve o sha256 do que escreveu (3a e 5a afericoes)."""
    p = os.path.join(OUT, "um_absoluto_pilar_quantico.json"); tmp = p + ".tmp_qp"
    _rd = st.get("cache_dir") if st.get("mode") == "REUSE" else st.get("run_dir")   # MEDIDO no disco, aqui (7a afericao); None = nao verificado
    _absent = (not (os.path.exists(os.path.join(_rd, "result.json")) or os.path.exists(os.path.join(_rd, "result_partial.json")))) if _rd else None
    b = json.dumps({"verdict": verdict, "marker": True, "reason": reason, "result_file_absent": _absent, "run_id": st.get("run_id"), "key": st.get("key")},
                   ensure_ascii=False, indent=1).encode("utf-8")
    try:
        with open(tmp, "wb") as fh:
            fh.write(b)
        _qp_retry(lambda: os.replace(tmp, p))
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass
    return hashlib.sha256(b).hexdigest()   # os bytes escritos, sem reler o Nos depois da troca (7a afericao)


def _qp_out_marker_safe(out, verdict, st, reason):
    """O marcador desta rodada; se ele mesmo falhar, o arquivo do pilar no Nos e' REMOVIDO (com novas tentativas). Se nem a remocao for possivel (outro
    processo segurando o arquivo), os erros ficam no registro do selo e o SELO grava NOT_THIS_RUN para esse arquivo (W09b: so o que o runtime escreveu
    nesta rodada, out_file_sha256, e' hasheado) -- 4a e 5a afericoes."""
    try:
        out["out_file_sha256"] = _qp_out_marker(verdict, st, reason)
    except Exception as e_:
        out["out_marker_error"] = repr(e_)
        try:
            _qp_retry(lambda: os.remove(os.path.join(OUT, "um_absoluto_pilar_quantico.json")))
            out["out_file_removed"] = True
        except FileNotFoundError:
            out["out_file_removed"] = True
        except Exception as e2:
            out["out_file_remove_error"] = repr(e2)


def _qp_summary(R):
    """Os numeros que o artigo e o selo leem (lidos do resultado; nada recalculado aqui)."""
    s = {}
    t2 = R.get("T2") or {}; cf = t2.get("configs") or []
    if cf:
        s["T2"] = {"configs": len(cf), "points": sum(c["n_points"] for c in cf), "unique": sum(c["unique"] for c in cf),
                   "ambiguous": sum(c["ambiguous"] for c in cf), "degenerate": sum(c["degenerate"] for c in cf), "errors": sum(c.get("errors", 0) for c in cf),
                   "name_in_core_configs": sum(1 for c in cf if c.get("cci_half_window")), "folds_window_configs": sum(1 for c in cf if c.get("folds_window")),
                   "identities_checked": {k: sum((c.get("identities_checked") or {}).get(k, 0) for c in cf) for k in sorted({kk for c in cf for kk in (c.get("identities_checked") or {})})},
                   "gamma_star": {"d%d_nc%d" % (c["d"], c["nc"]): c.get("gamma_star_cci_1_minus_beta") for c in cf},
                   "cci_half_window": {"d%d_nc%d" % (c["d"], c["nc"]): c.get("cci_half_window") for c in cf},
                   "folds_window": {"d%d_nc%d" % (c["d"], c["nc"]): c.get("folds_window") for c in cf},
                   "n_folds_range_unique": {"d%d_nc%d" % (c["d"], c["nc"]): c.get("n_folds_range_unique") for c in cf},
                   "gap_rel_min": min((c["gap_rel_min"] for c in cf if isinstance(c.get("gap_rel_min"), float) and c["gap_rel_min"] == c["gap_rel_min"]), default=None),
                   "identities": t2.get("identities")}
    t1 = R.get("T1") or {}
    if t1 and not t1.get("error"):
        s["T1"] = {"injections": sum(v["n"] for v in t1.values()), "errors": sum(v.get("errors", 0) for v in t1.values()),
                   "per_d": {d: {"n": v["n"], "pass_sigma0": (v.get("sigma_0.0") or {}).get("pass_frac"),
                                 "n_by_sigma": {k[6:]: (v[k] or {}).get("n") for k in v if k.startswith("sigma_")},
                                 "median_beta_rel_err": {k[6:]: (v[k] or {}).get("median_beta_rel_err") for k in v if k.startswith("sigma_")},
                                 "median_abs_p_err": {k[6:]: (v[k] or {}).get("median_abs_p_err") for k in v if k.startswith("sigma_")},
                                 "max_beta_rel_err": {k[6:]: (v[k] or {}).get("max_beta_rel_err") for k in v if k.startswith("sigma_")},
                                 "n_nonfinite_beta": {k[6:]: (v[k] or {}).get("n_nonfinite_beta") for k in v if k.startswith("sigma_")}} for d, v in t1.items()}}
    t3 = R.get("T3") or {}
    if t3 and not t3.get("error"):
        dks = [dk for dk in t3 if dk.startswith("d")]
        s["T3"] = {"controls": {dk: {nm: bool((t3[dk].get(nm) or {}).get("failed_as_required")) for nm in ("N1_dephasing_only", "N4_negative_rate_not_cp", "N5_time_reversal_not_cp")} for dk in dks},
                   "N2_unital_identity": {dk: {k: (t3[dk].get("N2_unital_identity") or {}).get(k) for k in ("identity_ok", "unital_residual_rel", "info_status", "info_gap_rel")} for dk in dks},
                   "N3_linear_law": {d: {"n": v["n"], "p_recovered_sigma0": (v.get("sigma_0.0") or {}).get("pass_frac"),
                                         "root_law_rejected": (v.get("sigma_0.0") or {}).get("root_law_rejected_frac")} for d, v in (t3.get("N3_linear_law") or {}).items()}}
    t4 = R.get("T4") or {}
    if t4 and not t4.get("error"):
        s["T4"] = {"instances": sum(a["n"] for a in t4.values()), "unique": sum(a["UNIQUE"] for a in t4.values()),
                   "ambiguous": sum(a["AMBIGUOUS"] for a in t4.values()), "degenerate": sum(a["DEGENERATE"] for a in t4.values()), "errors": sum(a.get("ERROR", 0) for a in t4.values()),
                   "identity_violations": sum(sum(a["viol"].values()) for a in t4.values()), "rotated": sum(a["rotated"] for a in t4.values()),
                   "all_identities_checked": sum(a.get("all_identities_checked", 0) for a in t4.values()),
                   "per_d": {d: {k: a.get(k) for k in ("n", "UNIQUE", "AMBIGUOUS", "DEGENERATE", "ERROR", "cci_above_uniform", "rotated", "all_identities_checked")} for d, a in t4.items()}}
    s["D128"] = R.get("D128"); s["cpuref"] = R.get("cpuref_compare"); s["engine"] = (R.get("engine_selftest") or {}).get("checks")
    s["phase_seconds"] = R.get("phase_seconds"); s["env"] = R.get("env")
    return s


def quantum_pillar_finish_v384(st, core):
    """Antes do artigo: espera (com prazo e progresso), le, confere, REDERIVA, grava o cache (rodada completa) e devolve o registro do core."""
    out = {"theorem": "O pilar quantico da TGL na GPU (v384): o sistema aberto H_LD + cinco saltos de Lindblad, calculado e testado",
           "status": "[COMPUTED] -- calculo do sistema aberto da teoria; NAO e' medicao; o gate nao muda",
           "preregistration": {"spec_sha256": _QP_SPEC_SHA256, "files": _QP_PREREG}, "key": st.get("key"), "beta_hex": st.get("beta_hex"),
           "checkpoint_switch": st.get("checkpoint_switch"), "mode": st.get("mode"), "does_not_gate_core": True}
    try:
        if st.get("refused"):
            out.update({"verdict": "TGL_QUANTUM_PILLAR_V1__NOT_RUN__%s__GATE_UNTOUCHED" % re.sub(r"[^A-Z0-9_]", "_", st["refused"].split(":")[0].upper()),
                        "all_verified": False, "refused": st["refused"]})
            st["finished"] = True
            _qp_out_marker_safe(out, out["verdict"], st, "not_run")
            return out
        # o pre-registro em disco tem de ser o congelado (hash lido)
        pr_ok = {}
        for k, v in _QP_PREREG.items():
            pr_ok[k] = bool(os.path.exists(v["path"]) and hashlib.sha256(open(v["path"], "rb").read()).hexdigest() == v["sha256"])
        out["preregistration"]["on_disk_matches"] = pr_ok
        if st["mode"] == "REUSE":
            rdir = st["cache_dir"]; reuse = True
        else:
            rc, timed_out = _qp_wait(st)
            out["worker_rc"] = rc; out["timed_out"] = timed_out
            rdir = st["run_dir"]; reuse = False
        rp = os.path.join(rdir, "result.json"); partial = False
        if not os.path.exists(rp) and os.path.exists(os.path.join(rdir, "result_partial.json")):
            rp = os.path.join(rdir, "result_partial.json"); partial = True
        if not os.path.exists(rp):
            out.update({"verdict": "TGL_QUANTUM_PILLAR_V1__NOT_RUN__NO_RESULT_FILE__GATE_UNTOUCHED", "all_verified": False})
            _qp_out_marker_safe(out, out["verdict"], st, "no_result_file")   # o arquivo de uma rodada anterior NAO fica no Nos (3a, 4a e 5a afericoes)
            st["finished"] = True
            return out
        raw = open(rp, "rb").read(); rsha = hashlib.sha256(raw).hexdigest()
        hp = os.path.join(rdir, "result.json.sha256")
        sha_ok = (not partial) and os.path.exists(hp) and open(hp, encoding="ascii").read().strip() == rsha
        R = json.loads(raw.decode("utf-8"))
        der = _qp_rederive(st, rp)
        out.update({"result_sha256": rsha, "result_sha_file_ok": bool(sha_ok), "partial": partial, "worker_sha256": R.get("worker_sha256"), "run_id": R.get("run_id"),
                    "spec_sha256_in_result": R.get("spec_sha256"), "details_sha256": R.get("details_sha256"), "cpuref_sha256": R.get("cpuref_sha256"), "run_dir": rdir,
                    "verdict_worker": R.get("verdict"), "verdict_rederived": der, "started": R.get("started"), "finished": R.get("finished")})
        beta_ok = bool(st.get("beta_hex") and isinstance(core.get("beta"), float) and float(core["beta"]).hex() == st["beta_hex"] == R.get("beta_hex"))
        out["beta_matches_core"] = beta_ok
        # o pre-registro em disco e' INFORMATIVO (o um.py nao depende de um caminho local): a especificacao embutida, conferida pelo hash, e' o congelado
        same_code = bool(R.get("spec_sha256") == _QP_SPEC_SHA256 and R.get("worker_sha256") == st["materialized"]["pilar_quantico_worker.py"]["sha256"] and beta_ok
                         and (reuse or R.get("run_id") == st.get("run_id")))      # a marca da rodada: o resultado e' DESTA rodada (achado 7 da 1a passada)
        ok_chain = bool(sha_ok and der and der == R.get("verdict") and same_code)
        verdict = der or R.get("verdict") or "TGL_QUANTUM_PILLAR_V1__NOT_RUN__NO_VERDICT__GATE_UNTOUCHED"
        if partial and same_code and der:
            # o parcial e' resultado legitimo, mas PARCIAL -- dito com a CAUSA (o prazo ou a morte do trabalhador), nunca gravado no cache
            _cause = "WORKER_STOPPED_BY_TIMEOUT" if out.get("timed_out") else ("WORKER_DIED_RC_%s" % out.get("worker_rc"))
            verdict = verdict.replace("__GATE_UNTOUCHED", "__PARTIAL_RESULT_%s__GATE_UNTOUCHED" % _cause)
        elif not ok_chain and "__RESULTS_VOID__" not in verdict and "__NOT_RUN__" not in verdict:
            verdict = verdict.replace("__GATE_UNTOUCHED", "__CUSTODY_CHAIN_INCOMPLETE__GATE_UNTOUCHED")
        out["verdict"] = verdict
        out["custody_chain_ok"] = ok_chain
        out["all_verified"] = bool(ok_chain and verdict.startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__"))
        try:
            out["summary"] = _qp_summary(R)
        except Exception as e_:
            out["summary"] = {}; out["summary_error"] = repr(e_)       # um passo acessorio nao rebaixa o veredito (achado 33 da 2a passada)
        try:
            # o resultado no Nos, para o selo o hashear junto (achado 36 da 2a passada); troca atomica
            _tq = os.path.join(OUT, "um_absoluto_pilar_quantico.json.tmp_qp")
            shutil.copyfile(rp, _tq)
            _hq = _qp_retry(lambda: hashlib.sha256(open(_tq, "rb").read()).hexdigest())   # o sha256 ANTES da troca (6a afericao)
            if _hq != rsha:
                raise RuntimeError("a copia temporaria do resultado nao confere com o result.json (%s != %s)" % (_hq[:16], rsha[:16]))
            _qp_retry(lambda: os.replace(_tq, os.path.join(OUT, "um_absoluto_pilar_quantico.json")))
            out["out_file_sha256"] = _hq                                                   # o que o selo aceita (W09b)
            out["copied_to_out"] = True
        except Exception as e_:
            out["copy_to_out_error"] = repr(e_)
            # o resultado nao chegou ao Nos: a cadeia ate o selo NAO fecha (4a afericao) -- nada ao cache, all_verified False, dito no veredito
            ok_chain = False; out["custody_chain_ok"] = False; out["all_verified"] = False
            if "__RESULTS_VOID__" not in verdict and "__NOT_RUN__" not in verdict and "__CUSTODY_CHAIN_INCOMPLETE__" not in verdict:
                verdict = verdict.replace("__GATE_UNTOUCHED", "__CUSTODY_CHAIN_INCOMPLETE__GATE_UNTOUCHED"); out["verdict"] = verdict
        if reuse:
            out["reuse"] = {"reused": True, "from_run_finished": R.get("finished"), "cache_dir": rdir,
                            "reading": "RODADA_INTERMEDIARIA__PILAR_QUANTICO_REAPROVEITADO__A_VERSAO_FINAL_RODA_SEM_A_CHAVE"}
        else:
            out["reuse"] = {"reused": False, "reading": "PILAR_QUANTICO_CALCULADO_NESTA_RODADA"}
            if (ok_chain and not partial and verdict.startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__") and "__PARTIAL_" not in verdict
                    and str((R.get("D128") or {}).get("status_code")) == "RAN"):
                try:
                    out["reuse"]["saved_to_cache"] = _qp_save_cache(st, rp)  # so resultado COMPLETO (com o D128 rodado) vai ao cache; falha de ambiente nunca
                except Exception as e_:
                    out["reuse"]["cache_error"] = repr(e_)                    # a falha do cache nao rebaixa o veredito (achados 7 e 33 da 2a passada)
            else:
                _d128sc = str((R.get("D128") or {}).get("status_code"))
                _d128_only = bool(ok_chain and not partial and verdict.startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__") and _d128sc != "RAN")
                out["reuse"]["not_cached_code"] = ("D128_NOT_RAN:" + _d128sc) if _d128_only else "NOT_COMPLETE_OR_NOT_CHECKED"   # o artigo compoe a frase em cada lingua
                out["reuse"]["not_cached_because"] = ("o D128 nao rodou nesta rodada (%s): o cache so guarda resultado completo com o D128" % _d128sc
                                                      if _d128_only else "resultado nao completo ou nao conferido")
        print("[v384] pilar quantico: %s" % verdict, flush=True)
        st["finished"] = True
    except Exception as e:
        out.update({"verdict": "TGL_QUANTUM_PILLAR_V1__NOT_RUN__FINISH_FAILED__GATE_UNTOUCHED", "all_verified": False, "error": repr(e)})
        _qp_kill_tree(st.get("proc")); st["finished"] = True
    if not out.get("copied_to_out"):
        try:
            os.remove(os.path.join(OUT, "um_absoluto_pilar_quantico.json.tmp_qp"))   # a sobra de uma copia que falhou (5a afericao)
        except OSError:
            pass
        _qp_out_marker_safe(out, out.get("verdict"), st, "copy_failed" if out.get("copy_to_out_error") else "finish_failed")   # o fato (result_file_absent) e' medido no marcador   # o marcador desta rodada, ou a remocao (3a-5a)
    return out
