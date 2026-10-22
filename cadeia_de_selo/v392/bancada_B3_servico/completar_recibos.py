import json
import os
import subprocess

D = os.path.dirname(os.path.abspath(__file__))
pp = os.path.join(D, "RECIBO_PARADA_v392.json")
rp = os.path.join(D, "RECIBO_RELIGAMENTO_v392.json")
p = json.load(open(pp, encoding="utf-8"))
p.setdefault("hora", p.get("hora_recibo"))
open(pp + ".tmp", "w", encoding="utf-8").write(json.dumps(p, ensure_ascii=False, indent=1))
os.replace(pp + ".tmp", pp)
r = json.load(open(rp, encoding="utf-8"))
pid = subprocess.run(["powershell", "-NoProfile", "-Command",
                      "(Get-NetTCPConnection -State Listen -LocalPort 18777).OwningProcess"], capture_output=True, text=True).stdout.strip()
r["versao_servida"] = r["identidade"]["canonical_version"]
r["manifesto_sha256"] = r["identidade"]["canonical_manifest_sha256"]
r["pid"] = int(pid.splitlines()[0])
r["hora"] = r.get("hora_recibo")
open(rp + ".tmp", "w", encoding="utf-8").write(json.dumps(r, ensure_ascii=False, indent=1))
os.replace(rp + ".tmp", rp)
print("ok pid", r["pid"], r["versao_servida"], r["manifesto_sha256"][:16])
