import sys, os, json, importlib.util
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
sys.path.insert(0, V); sys.path.insert(0, V + r"\pos_rito")
spec = importlib.util.spec_from_file_location("leitura_rev2", V + r"\pos_rito\leitura_v411.py")
L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
E = json.load(open(V + r"\ESPERADOS_v411.json", encoding="utf-8"))
ap = {"um_py_novo": {"sha16": E["candidato_sha16"]}, "backups": {"um.py": {"sha16": E["origem_sha16"], "backup": V + r"\base_um_v410.py"}}, "ts": "20261112_190000"}
L._aplicado = lambda: (ap, "emulado")
L.NOS = r"C:\t\k411c\revisao_C\nos_pos"
V_, P = L.ler()
for p in P: print("-", p[:230])
