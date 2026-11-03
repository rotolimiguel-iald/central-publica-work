# -*- coding: utf-8 -*-
"""Revisor terceiro v406: c3 (raiz embutida), c10 (tres registros selados), c12 (proveniencia) e a idempotencia do fechamento; negacao uma a uma."""
import copy, importlib.util, json, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v406/"
spec = importlib.util.spec_from_file_location("um_cand_rev2", R + "um_v406_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev2"] = m; spec.loader.exec_module(m)
core0 = json.load(open(R + "dry_v406/core_ensaio.json", encoding="utf-8"))["core"]
C = m._V406_FECHO_CONTRACT
raiz = m._EMBEDDED_KERNEL_FILES["TGLExt.lean"]
print("raiz termina com:", repr(raiz[-160:]))
print("root_suffix:", repr(C["root_suffix"]))
def ver(nome, core):
    r = m.fechamento_v406(copy.deepcopy(core)); falhos = [c["id"] for c in (r.get("mechanics") or {}).get("checks", []) if not c["ok"]]
    print(nome, "->", r["verdict"][:90], "| falhos:", falhos); return r
ver("base", core0)
m._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = raiz.replace("import TGLExt.F1Fecho394.CanonicalFullTGLWitnessR1", "-- retirado")
ver("raiz sem o import da candidata", core0)
m._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = raiz.replace("import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1", "-- retirado")
ver("raiz sem o import do topo", core0)
m._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = raiz
for nome in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396"):
    c = copy.deepcopy(core0); c[nome]["all_verified"] = False; ver("c10: %s all_verified False" % nome, c)
c = copy.deepcopy(core0); del c["kernel_formalization"]["declaration_sources_status_v394"]; ver("c12: status da proveniencia ausente", c)
c = copy.deepcopy(core0); c["external_ladder"]["n_theorems_expected"] = 10066; ver("c9: escada esperada antiga 10066", c)
# a escada: todos os contratos com 11860
import ast
for nm in dir(m):
    if nm.startswith("_V39") or nm.startswith("_V40"):
        v = getattr(m, nm)
        def achar(o, p=""):
            if isinstance(o, dict):
                for k, x in o.items():
                    if k == "expected_ladder": print("  ", nm, p, "expected_ladder", x)
                    achar(x, p + "/" + str(k)[:20])
        if isinstance(v, (dict, list)):
            achar(v) if isinstance(v, dict) else [achar(x) for x in v if isinstance(x, dict)]
print("ladder esperada do prove_external_ladder:", m.UM_VERSION)
import inspect
src = inspect.getsource(m.prove_external_ladder); print([l for l in src.split("\n") if "11860" in l or "n_theorems_expected" in l][:6])
