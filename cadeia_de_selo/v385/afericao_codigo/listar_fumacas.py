import json, os, sys, hashlib
sys.stdout.reconfigure(encoding="utf-8")
roots = [r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad", r"C:\IALD\Bancada_Um"]
for r in roots:
    for dp, dn, fn in os.walk(r):
        if "result.json" in fn:
            p = os.path.join(dp, "result.json")
            try:
                raw = open(p, "rb").read(); R = json.loads(raw)
            except Exception:
                continue
            if isinstance(R, dict) and str(R.get("worker_sha256", "")).startswith("0c9ba7fd") and not str(R.get("spec_sha256", "")).startswith("ff1973"):
                print(R.get("spec_sha256", "")[:8], str(R.get("run_id"))[:10], hashlib.sha256(raw).hexdigest()[:10], str(R.get("finished"))[:19], (R.get("env") or {}).get("gpu"), str(R.get("verdict"))[:60], p.split("scratchpad")[-1][:120])
