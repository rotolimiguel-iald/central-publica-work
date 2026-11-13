import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
mem = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
pino = json.load(open(V + r"\PINO_MEMORIA_PY_v411.json", encoding="utf-8"))
mp = mem + r"\fila\memoria.py"
h = hashlib.sha256(open(mp, "rb").read()).hexdigest()
print("memoria.py agora:", h[:16], "pino:", pino.get("sha16"), "igual:", h == pino.get("sha256"), "mtime", os.path.getmtime(mp))
print("PAUSA_VIGIA existe:", os.path.exists(mem + r"\fila\PAUSA_VIGIA.json"))
raw = open(mem + r"\MEMORY.md", "rb").read()
print("MEMORY.md agora:", len(raw), "B", raw.count(b"\n"), "linhas")
pm = json.load(open(mem + r"\fila\PINO_MEMORY.json", encoding="utf-8"))
print("pino do indice confere:", pm.get("sha256") == hashlib.sha256(raw).hexdigest(), pm.get("pinado_em"), pm.get("por"))
