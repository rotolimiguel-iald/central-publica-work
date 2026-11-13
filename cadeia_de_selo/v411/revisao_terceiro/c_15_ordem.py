import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
j = json.load(open(V + r"\ensaio_a_seco_v411.json", encoding="utf-8"))
o = j.get("ordem_de_chamada_v411") or {}
print("ok:", o.get("ok"), "chaves do dict:", list(o)[:10])
for fn, d in (o.get("funcoes") or {}).items():
    print(fn, {k: (v if not isinstance(v, (list, dict)) else (len(v), (v if len(json.dumps(v)) < 300 else str(v)[:300]))) for k, v in d.items()})
print("controle negativo:", json.dumps(j.get("ordem_de_chamada_v411_controle_negativo"), ensure_ascii=False)[:500])
