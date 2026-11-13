import sys, json, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
E = json.load(open(V + r"\ESPERADOS_v411.json", encoding="utf-8"))
print("ESP pilar:", json.dumps(E.get("pilar"), ensure_ascii=False)[:600])
src = rd(V + r"\um_v411_candidato.py")
for m in re.finditer(r"def (_?\w*(pillar|pilar)\w*)\(", src):
    print("def", m.group(1), src[:m.start()].count("\n") + 1)
for m in re.finditer(r"TGL_CACHE_DIR|cache_key|def _quantum_pillar_key|pillar_key", src):
    ln = src[:m.start()].count("\n") + 1
    print(ln, src.split("\n")[ln-1][:200])
    if ln > 0 and m.start() > 0 and len([1]) and False: pass
