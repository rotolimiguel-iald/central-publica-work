import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
p = "v384_runtime.py"
s = open(p, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (c, old[:100]); s = s.replace(old, new)
rep('_QP_TIMEOUT_S = 4 * 3600          # prazo duro desde o lancamento; passado, o trabalhador e\' encerrado e vale o resultado parcial (dito)\n_QP_PROGRESS_EVERY_S = 300\n',
    '# o prazo e o intervalo do progresso sao LIDOS da especificacao congelada (execution.um_py_timeout_s; execution.progress_every_s) -- achado 9 do aferidor\n')
rep('''    code = ("import json,torch,numpy;ok=torch.cuda.is_available();"
            "print(json.dumps({'torch':torch.__version__,'cuda':torch.version.cuda,'numpy':numpy.__version__,'gpu':(torch.cuda.get_device_name(0) if ok else None)}))")''',
    '''    code = ("import json,platform,torch,numpy,scipy;ok=torch.cuda.is_available();"
            "print(json.dumps({'torch':torch.__version__,'cuda':torch.version.cuda,'numpy':numpy.__version__,'scipy':scipy.__version__,"
            "'python':platform.python_version(),'gpu':(torch.cuda.get_device_name(0) if ok else None)}))")''')
rep('''def _qp_cache_dir(key):''', '''def _qp_engine_now(mat):
    """Ao reaproveitar: o motor (E1..E7) roda de novo NO AMBIENTE PRESENTE, numa pasta nova; so reaproveita se passar (achado 8)."""
    d = os.path.join(_qp_dir(), "engine_" + time.strftime("%Y%m%d_%H%M%S"))
    os.makedirs(d, exist_ok=True)
    try:
        subprocess.run([sys.executable, mat["pilar_quantico_worker.py"]["path"], "--mode", "engine", "--spec", mat["pilar_quantico_spec.json"]["path"], "--out", d],
                       capture_output=True, text=True, timeout=900)
        r = json.load(open(os.path.join(d, "result.json"), encoding="utf-8"))
        return bool(r.get("verdict") == "ENGINE_SELFTEST_PASSED" and r.get("worker_sha256") == mat["pilar_quantico_worker.py"]["sha256"])
    except Exception:
        return False


def _qp_cache_dir(key):''')
rep('''                env = _qp_env_probe(); cenv = cached.get("env") or {}
                same = all(env.get(k) == cenv.get(k) for k in ("torch", "cuda", "numpy", "gpu"))
                if same:''', '''                env = _qp_env_probe(); cenv = cached.get("env") or {}
                same = all(env.get(k) == cenv.get(k) for k in ("torch", "cuda", "numpy", "scipy", "python", "gpu"))
                if same and str(cached.get("verdict", "")).startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__") and _qp_engine_now(mat):''')
rep('''                st["reuse_refused"] = {"env_now": env, "env_cached": {k: cenv.get(k) for k in ("torch", "cuda", "numpy", "gpu")}}''',
    '''                st["reuse_refused"] = {"env_now": env, "env_cached": {k: cenv.get(k) for k in ("torch", "cuda", "numpy", "scipy", "python", "gpu")}}''')
rep('''        run_dir = os.path.join(_qp_dir(), "run_" + time.strftime("%Y%m%d_%H%M%S"))
        os.makedirs(run_dir, exist_ok=True)''', '''        import uuid
        run_id = uuid.uuid4().hex                     # a MARCA UNICA da rodada (achado 7): conferida em todas as saidas
        run_dir = os.path.join(_qp_dir(), "run_" + time.strftime("%Y%m%d_%H%M%S") + "_" + run_id[:8])
        os.makedirs(run_dir, exist_ok=False)''')
rep('''                                 "--spec-sha256", _QP_SPEC_SHA256, "--beta-hex", bhex, "--out", run_dir],''',
    '''                                 "--spec-sha256", _QP_SPEC_SHA256, "--beta-hex", bhex, "--run-id", run_id, "--out", run_dir],''')
rep('''        st.update({"mode": "COMPUTE", "proc": proc, "run_dir": run_dir, "log": logf, "cache_dir": cdir})''',
    '''        st.update({"mode": "COMPUTE", "proc": proc, "run_dir": run_dir, "log": logf, "cache_dir": cdir, "run_id": run_id,
                   "timeout_s": int(spec["execution"]["um_py_timeout_s"]), "progress_every_s": int(spec["execution"]["progress_every_s"])})''')
rep('''        if el > _QP_TIMEOUT_S:''', '''        if el > st["timeout_s"]:''')
rep('''        if time.time() - last >= _QP_PROGRESS_EVERY_S:''', '''        if time.time() - last >= st["progress_every_s"]:''')
rep('''        same_code = bool(R.get("spec_sha256") == _QP_SPEC_SHA256 and R.get("worker_sha256") == st["materialized"]["pilar_quantico_worker.py"]["sha256"] and all(pr_ok.values()))''',
    '''        same_code = bool(R.get("spec_sha256") == _QP_SPEC_SHA256 and R.get("worker_sha256") == st["materialized"]["pilar_quantico_worker.py"]["sha256"] and all(pr_ok.values())
                         and (reuse or R.get("run_id") == st.get("run_id")))      # a marca da rodada: o resultado e' DESTA rodada (achado 7)''')
rep('''        if partial and same_code and der:''', '''        if partial and same_code and der and str((R.get("D128") or {}).get("status_code")) == "STARTED":
            der = der.replace("__D128_INTERRUPTED__", "__D128_INTERRUPTED__")   # a arvore ja le STARTED como INTERROMPIDO
        if partial and same_code and der:''')
rep('''            if ok_chain and not partial:
                out["reuse"]["saved_to_cache"] = _qp_save_cache(st, rp)''', '''            if ok_chain and not partial and verdict.startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__") and "__PARTIAL_" not in verdict:
                out["reuse"]["saved_to_cache"] = _qp_save_cache(st, rp)      # so resultado COMPLETO vai ao cache; falha de ambiente nunca (achado 8)''')
rep('''        out.update({"result_sha256": rsha, "result_sha_file_ok": bool(sha_ok), "partial": partial, "worker_sha256": R.get("worker_sha256"),''',
    '''        out.update({"result_sha256": rsha, "result_sha_file_ok": bool(sha_ok), "partial": partial, "worker_sha256": R.get("worker_sha256"), "run_id": R.get("run_id"),''')
ast.parse(s.replace("__QP_WORKER_SRC__", "''").replace("__QP_SPEC_JSON__", "''"))
open(p + ".tmp", "w", encoding="utf-8", newline=chr(10)).write(s); os.replace(p + ".tmp", p); print("ok")
