import importlib.util, json, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/"
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v408_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev"] = m; spec.loader.exec_module(m)
C = m._V408_TERMINAL_CONTRACT
print("n_declarations_public", C["n_declarations_public"], "excluidas", C["excluidas_auxiliares"], "n_flags", C["n_flags"], "ancoras", len(C["ancoras"]), "expected_ladder", C["expected_ladder"], "baseline ladder", C["baseline"]["ladder"])
nao = [d for d in C["declarations"] if d not in C["ancoras"]]
print(len(nao), nao)
cj = json.load(open(R + "CANDIDATO_v408.json", encoding="utf-8")); print(json.dumps(cj["politica_de_bandeiras"], ensure_ascii=False)[:900])
import re
al = open(R + "kernel/audit.log", "rb").read().decode("utf-8", "replace")
src = {mm.group(1): mm.group(2) for mm in re.finditer(r"^TGL_DECL_SOURCE\t([^\t]+)\t(\S+)", al, re.M)}
mods = {"TGLExt.TetelestaiTerminal", "TGLExt.TempoIgualMoeda", "TGLExt.PontoDeContradicao", "TGLExt.PIgualNP"}
todos = sorted(n for n, s in src.items() if s in mods)
print("decl no audit nos 4 modulos:", len(todos))
excl = [n for n in todos if n not in C["declarations"]]
print("sem bandeira:", excl)
