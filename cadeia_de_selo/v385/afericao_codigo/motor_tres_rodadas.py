# SO LEITURA: o bloco engine_selftest (E1..E8) em rodadas REAIS distintas na GPU (o mesmo trabalhador) -- teste empirico do determinismo bit a bit
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
SP = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad"
P = {"cache_v384_full": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\checkpoints\quantum_pillar\75dc30bc9cc8d330e31f99ca\result.json",
     "fumaca_21081c13": SP + r"\v384\fumaca_v384_20261004_152630_21081c13\result.json",
     "teste_motor_v8": SP + r"\v384\teste_motor_v8\result.json"}
def flat(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from flat(v, p + "." + str(k) if p else str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from flat(v, "%s[%d]" % (p, i))
    else:
        yield p, o
E = {}
for n, p in P.items():
    R = json.load(open(p, encoding="utf-8"))
    es = R.get("engine_selftest") if "engine_selftest" in R else R
    print(n, "run_id", str(R.get("run_id"))[:10], "worker", str(R.get("worker_sha256"))[:12], "seed?", R.get("seed"), "keys", list((es or {}).keys())[:8])
    E[n] = dict(flat((es or {}).get("checks")))
a, b, c = E["cache_v384_full"], E["fumaca_21081c13"], E["teste_motor_v8"]
print("n campos:", len(a), len(b), len(c))
for k in sorted(set(a) | set(b) | set(c)):
    va, vb, vc = a.get(k), b.get(k), c.get(k)
    if not (va == vb == vc):
        print("DIFERE", k, "| cache:", va, "| fumaca:", vb, "| motor_v8:", vc)
print("fim")
