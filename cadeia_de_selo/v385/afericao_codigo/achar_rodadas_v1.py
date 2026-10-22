# -*- coding: utf-8 -*-
# SO LEITURA: acha result.json com o MESMO spec V1 (ff1973...) e compara com o cache da v384 usando o comparador do candidato
import json, os, sys, hashlib
sys.stdout.reconfigure(encoding="utf-8")
PK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(PK, "um_v385_candidato.py"), encoding="utf-8").read().splitlines()
def grab(start_pat):
    i = [k for k, l in enumerate(src) if l.startswith(start_pat)][0]
    j = i + 1
    while j < len(src) and (src[j].startswith((" ", "\t")) or src[j].strip() == ""):
        j += 1
    return "\n".join(src[i:j])
ns = {"os": os, "hashlib": hashlib, "json": json}
for p in ("def _qp_summary(", "_QP_REPRO_SKIP_V385 =", "def _qp_flat_v385(", "def quantum_pillar_reproducibility_v385("):
    exec(grab(p), ns)
C = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\checkpoints\quantum_pillar\75dc30bc9cc8d330e31f99ca\result.json"
R0 = json.load(open(C, encoding="utf-8"))
print("cache: worker", R0["worker_sha256"][:16], "spec", R0["spec_sha256"][:16], "run_id", R0["run_id"][:8], "verdict", R0["verdict"][:90])
roots = [r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad", r"C:\IALD\Bancada_Um", r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um"]
seen = []
for r in roots:
    for dp, dn, fn in os.walk(r):
        if "result.json" in fn:
            p = os.path.join(dp, "result.json")
            try:
                R = json.load(open(p, encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(R, dict) or "spec_sha256" not in R:
                continue
            seen.append((p, R.get("spec_sha256", "")[:16], R.get("worker_sha256", "")[:16], str(R.get("verdict"))[:70], R.get("run_id", "")[:8] if R.get("run_id") else None))
from collections import Counter
print("n result.json do trabalhador:", len(seen))
print(Counter((s[1], s[2]) for s in seen))
for s in seen:
    if s[1] == R0["spec_sha256"][:16]:
        print("MESMO SPEC:", s)
