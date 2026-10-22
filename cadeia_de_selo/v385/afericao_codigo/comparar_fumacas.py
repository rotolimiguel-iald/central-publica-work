# -*- coding: utf-8 -*-
# SO LEITURA: pares de rodadas REAIS do mesmo trabalhador e do mesmo spec (fumaca) -> o comparador do candidato (teste empirico do determinismo)
import json, os, sys, hashlib, itertools
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
roots = [r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad", r"C:\IALD\Bancada_Um"]
groups = {}
for r in roots:
    for dp, dn, fn in os.walk(r):
        if "result.json" in fn:
            p = os.path.join(dp, "result.json")
            try:
                raw = open(p, "rb").read(); R = json.loads(raw)
            except Exception:
                continue
            if not isinstance(R, dict) or "spec_sha256" not in R or not R.get("run_id") or "SINTET" in str(R.get("run_id")).upper():
                continue
            if not str(R.get("verdict", "")).startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__"):
                continue
            k = (R["spec_sha256"][:16], R["worker_sha256"][:16], R.get("beta_hex"))
            groups.setdefault(k, {})
            groups[k].setdefault(R["run_id"], (p, R, hashlib.sha256(raw).hexdigest()[:16]))
for k, runs in groups.items():
    print("GRUPO", k, "rodadas distintas:", len(runs))
    for rid, (p, R, h) in runs.items():
        print("   ", rid[:8], h, R.get("finished"), (R.get("env") or {}).get("gpu"), p[-110:])
    for (ra, (pa, Ra, ha)), (rb, (pb, Rb, hb)) in itertools.combinations(runs.items(), 2):
        prev = {"read": True, "summary": ns["_qp_summary"](Ra), "verdict": Ra.get("verdict"), "sha256": ha, "finished": Ra.get("finished"), "run_id": ra, "key": "k"}
        rec = {"summary": ns["_qp_summary"](Rb), "verdict": Rb.get("verdict"), "reuse": {"reused": False}, "result_sha256": hb, "run_id": rb, "finished": Rb.get("finished")}
        out = ns["quantum_pillar_reproducibility_v385"](prev, rec)
        print("  PAR", ra[:8], "x", rb[:8], "->", out["verdict"][:130], "| n_differ", out.get("n_differ"), "max_rel", out.get("max_rel_diff"))
        for d in (out.get("first_differences") or [])[:12]:
            print("       ", d)
