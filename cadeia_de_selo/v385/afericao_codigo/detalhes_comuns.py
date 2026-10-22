# SO LEITURA: registros por ponto (details.jsonl) com a MESMA identidade (teste, d, nc/idx, semente) na fumaca real e na rodada V1 real -> iguais bit a bit?
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
SP = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad"
F = SP + r"\v384\fumaca_v384_20261004_152630_21081c13"
C = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\checkpoints\quantum_pillar\75dc30bc9cc8d330e31f99ca"
sf = json.load(open(F + r"\spec_fumaca.json", encoding="utf-8"))
sv = json.load(open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\quantum_pillar\pilar_quantico_spec.json", encoding="utf-8"))
print("seed fumaca", sf.get("seed"), "seed V1", sv.get("seed"))
def load(p):
    out = []
    for l in open(p, encoding="utf-8"):
        try:
            out.append(json.loads(l))
        except Exception:
            pass
    return out
df = load(F + r"\details.jsonl"); dv = load(C + r"\details.jsonl")
print("n registros", len(df), len(dv))
print("chaves exemplo fumaca:", list(df[0].keys())[:20])
def ident(r):
    return tuple((k, r.get(k)) for k in ("test", "phase", "d", "nc", "gi", "idx", "i", "k", "point", "config") if k in r)
from collections import defaultdict
iv = defaultdict(list)
for r in dv:
    iv[ident(r)].append(r)
same = diff = 0; ex = []
for r in df:
    k = ident(r)
    if k in iv and len(iv[k]) == 1:
        o = iv[k][0]
        if o == r:
            same += 1
        else:
            diff += 1
            if len(ex) < 4:
                ex.append((k, {kk: (r.get(kk), o.get(kk)) for kk in set(r) | set(o) if r.get(kk) != o.get(kk)}))
print("identidades comuns: iguais", same, "diferentes", diff)
for e in ex:
    print(str(e)[:900])
