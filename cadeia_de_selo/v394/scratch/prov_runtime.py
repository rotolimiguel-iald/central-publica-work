import ast, os, sys, hashlib, json
sys.stdout.reconfigure(encoding="utf-8")
C = "C:" + os.sep
T = os.path.join(C, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019")
R8 = os.path.join(T, "F1.FECHO_20261015", "coverage_candidate_r8", "um_v394_prechecked.py")
SRC = [os.path.join(T, "F1.TEMPO.V394", "runtime", "time_runtime_v394_r3.py"), os.path.join(T, "F1.TEMPO.V394", "runtime", "time_runtime_v394_r2.py"), os.path.join(T, "F1.TEMPO.V394", "runtime", "time_runtime_v394.py"),
       os.path.join(T, "F1.FECHO_20261015", "quadratic_runtime.py"), os.path.join(T, "F1.FECHO_20261015", "network_runtime_r2.py"), os.path.join(T, "F1.FECHO_20261015", "network_runtime_r1.py")]
# os runtimes de tempo: tem outros nomes? listar tambem physical_parameters etc.
extra = []
for dp, dn, fn in os.walk(os.path.join(T, "F1.TEMPO.V394")):
    dn[:] = [d for d in dn if d not in ("tgl_kernel", "lib", "builds", "candidate", "candidate_r2", "baseline", "formal_verified", "src")]
    for f in fn:
        if f.endswith(".py"):
            extra.append(os.path.join(dp, f))
SRC = SRC + [e for e in extra if e not in SRC]
t8 = open(R8, "rb").read().decode("utf-8"); tr8 = ast.parse(t8)
dump = lambda n: ast.dump(n)
srcs = {}
for p in SRC:
    try:
        tt = open(p, "rb").read().decode("utf-8"); srcs[p] = (tt, ast.parse(tt))
    except Exception as e:
        print("ERRO", p, e)
NEW = ["_V394_FORMAL_CONTRACT", "_V394_INSCRIPTIONS", "V394PhysicalContractError", "_v394_finite_real", "v394_physical_parameters", "v394_kms_clock", "v394_gibbs_root_parameters", "_v394_finite", "_v394_matrix", "_v394_geometry", "_v394_read",
       "_v394_channel", "_v394_rule", "_v394_clock_modulus", "_v394_clock_phase", "_v394_independent_liouvillian", "v394_time_frequency_checks", "tempo_frequencia_v394", "_v394_article_tex", "_V394_QUADRATIC_CONTRACT", "_v394_quadratic_residual",
       "v394_quadratic_checks", "regra_quadratica_v394", "_V394_NETWORK_CONTRACT", "rede_fock_v394"]
nm = lambda n: n.name if isinstance(n, (ast.FunctionDef, ast.ClassDef)) else (ast.unparse(n.targets[0]) if isinstance(n, ast.Assign) else None)
b8 = {nm(n): n for n in tr8.body if nm(n)}
res = {}
for name in NEW:
    n8 = b8[name]; ach = []
    for p, (tt, tr) in srcs.items():
        for n in tr.body:
            if nm(n) == name:
                ach.append((os.path.relpath(p, T), "IGUAL" if dump(n) == dump(n8) else "DIFERE"))
    res[name] = ach
    print("%-34s %s" % (name, ach[:4] if ach else "SEM FONTE IDENTICA/HOMONIMA nos runtimes do Codex"))
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "prov_runtime.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
