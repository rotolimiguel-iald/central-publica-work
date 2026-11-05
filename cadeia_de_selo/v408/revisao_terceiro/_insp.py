import importlib.util, json, sys, time
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/"
t0 = time.time()
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v408_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev"] = m; spec.loader.exec_module(m)
print("import", round(time.time() - t0, 1), "s", m.UM_VERSION)
C = m._V408_TERMINAL_CONTRACT
for k, v in C.items():
    print(k, "::", repr(v)[:230])
print("TEXT keys", list(m._V408_TERMINAL_TEXT.keys()))
print("SPECS", [s.get("registro") or list(s)[:3] for s in m._V408_SPECS])
print("NOMES", m._V408_NOMES_REGISTROS, m._V408_REGISTROS_FUNCAO)
