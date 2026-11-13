import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
E = json.load(open(V + r"\ESPERADOS_v411.json", encoding="utf-8"))
r = E["veracidade"]["resultado"]
for k in ("original", "duravel"):
    p = r.get(k); ex = os.path.exists(p) if p else False
    h = hashlib.sha256(open(p, "rb").read()).hexdigest() if ex else None
    print(k, p, "existe:", ex, "sha ok:", h == r["sha256"])
# outras dependencias de caminho absoluto fora do pacote usadas pela leitura/conferidor no real: listar ESP chaves com 'path'/'arquivo'
def walk(o, pre=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str) and (v[1:3] == ":\\" or v[1:3] == ":/"):
                yield pre + "/" + k, v
            else:
                yield from walk(v, pre + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o[:50]):
            yield from walk(v, pre + "[%d]" % i)
n = 0; faltam = []
for k, p in walk(E):
    n += 1
    if "\kimi\\" in p.lower(): faltam.append(("KIMI", p)); continue
    if not os.path.exists(p): faltam.append((k, p))
print("caminhos absolutos no ESPERADOS:", n, "ausentes:", faltam[:8])
