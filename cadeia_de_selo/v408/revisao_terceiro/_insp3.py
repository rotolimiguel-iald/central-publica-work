import importlib.util, json, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/"
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v408_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev"] = m; spec.loader.exec_module(m)
for s in m._V408_SPECS:
    print("=== SPEC", s["nome"], "| keys", list(s.keys()))
    for k in ("veredito_prefixo", "veredito_sufixo", "escopo", "estatuto"):
        if k in s: print("  ", k, "::", str(s[k])[:400])
    for c in s["checks"]:
        print("   -", c["id"], c.get("op"), "|", c.get("descricao")[:200], "| onde:", c.get("onde"), "| valor:", repr(c.get("valor"))[:100])
    print("  erratas:", len(s.get("erratas", [])))
import inspect
print(inspect.getsource(m._v408_rodar_specs)[:3000])
