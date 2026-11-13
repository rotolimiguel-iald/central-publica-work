import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
src = rd(V + r"\instalar_v411.py")
marca = 'ts = time.strftime("%Y%m%d_%H%M%S"); rec = {"ts": ts, "backups": {}}'
i = src.index(marca)
pre = src[:i]
# so' a parte anterior a primeira escrita: leituras e asserts
import ast
for nd in ast.walk(ast.parse(pre)):
    if isinstance(nd, ast.Call):
        f = ast.unparse(nd.func)
        assert f not in ("os.replace", "os.makedirs", "shutil.copyfile", "os.rename", "os.remove"), ("a parte lida tem escrita", f)
        if f == "open" and len(nd.args) > 1 and isinstance(nd.args[1], ast.Constant) and any(c in str(nd.args[1].value) for c in "wax+"):
            raise AssertionError(("a parte lida tem open de escrita", ast.unparse(nd)))
ns = {"__file__": V + r"\instalar_v411.py", "__name__": "instalar_reads"}
try:
    exec(compile(pre, "instalar_v411.py(parte so' de leitura)", "exec"), ns)
    print("TODAS AS ASSERTS DE LEITURA DO INSTALAR PASSAM hoje (nenhuma escrita foi feita)")
    print("um.py do Nos (v410):", h16(ns["raw0"]) if "h16" in ns else "?", "| candidato:", ns["ESP"]["candidato_sha16"], "| modulos novos:", ns.get("_N"))
except AssertionError as e:
    print("ASSERT FALHOU:", repr(e)[:400])
except SystemExit as e:
    print("SystemExit:", e)
except Exception as e:
    import traceback
    print("EXCECAO:", traceback.format_exc()[-600:])
