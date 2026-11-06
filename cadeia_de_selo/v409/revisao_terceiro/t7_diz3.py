import importlib.util, sys, json
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v409_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev"] = m; spec.loader.exec_module(m)
T = m._V409_TRADUCAO_TEXT
for i, x in enumerate(T["diz"]):
    if "leitor que so" in x or "leitor que se" in x or "ela vale" in x: print("diz[%d]:" % i, x)
for k in ("limites", "nao_diz"):
    for i, x in enumerate(T[k]):
        if "igualdade" in x: print(k, "[%d]:" % i, x[:700])
core = json.load(open(R + "dry_v409/core_ensaio.json", encoding="utf-8"))["core"]
print("core diz == candidato diz:", core["traducao_turing_v409"]["diz"] == T["diz"])
