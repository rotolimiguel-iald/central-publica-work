import importlib.util, json, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/"
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v408_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev"] = m; spec.loader.exec_module(m)
T = m._V408_TERMINAL_TEXT
for k in ("estatuto", "escopo", "veredito_ok"): print(k, "::", T[k]); print()
for k in ("limites", "diz", "nao_diz"):
    print("=====", k)
    v = T[k]
    if isinstance(v, (list, tuple)):
        for i, x in enumerate(v): print(" %d. %s" % (i + 1, x))
    else: print(v)
print("extras keys", list(T["extras"].keys()))
