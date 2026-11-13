import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
E = json.load(open(V + r"\ESPERADOS_v411.json", encoding="utf-8"))
h = E["registros_funcao_v411"]["h0dn"]
print("fora_do_values:", json.dumps(h["fora_do_values_porque_dependem_da_pasta_do_rito"], ensure_ascii=False)[:500])
vals = h["values"]
hits = []
def walk(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, p + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, p + "[%d]" % i)
    elif isinstance(o, str):
        if re.search(r"[A-Za-z]:\|\\|/c/|tmp|Temp|\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d", o): hits.append((p, o[:90]))
walk(vals)
print("strings dependentes de caminho/hora em values:", len(hits))
for x in hits[:12]: print("  ", x)
