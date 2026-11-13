import sys, os, json, importlib.util
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
sys.path.insert(0, V); sys.path.insert(0, V + r"\pos_rito"); sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
spec = importlib.util.spec_from_file_location("bc411r", V + r"\pos_rito\blocos_custodia_v411.py"); bc = importlib.util.module_from_spec(spec); spec.loader.exec_module(bc)
core = json.load(open(r"C:\t\k411c\falso_nos_v411\um_absoluto.json", encoding="utf-8"))["core"]
cu = core["cunhagens_v411"]
ds = bc._datas_das_inscricoes(cu)
print("datas:", ds, "| periodo EN:", bc._periodo_en(ds), "| n:", len(cu["verbatim"]))
print("casos _periodo_en:", bc._periodo_en(["12/11/2026"]), "|", bc._periodo_en(["11/11/2026", "12/11/2026", "13/11/2026"]), "|", bc._periodo_en(["30/10/2026", "02/11/2026"]))
try:
    ctx = bc.contexto_do_core(core)
    print("ctx cunhagens:", {k: v for k, v in (ctx.get("cunhagens") or {}).items()})
except Exception as e:
    print("contexto_do_core ERRO:", repr(e)[:300])
