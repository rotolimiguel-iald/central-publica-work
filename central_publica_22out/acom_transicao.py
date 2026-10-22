# -*- coding: utf-8 -*-
"""Transição ACOM da sessão a7 (a Central aberta, 22/10/2026). Uso: python acom_transicao.py <nome> <expected_revision>
Lê work/central_publica_22out/acom_<nome>.json ({"event_id", "records": [{..., "sources": [{"kind","ref"}]}], "flow": {...}}),
calcula o sha256 de cada fonte (nunca de memória), grava <nome>_changes.json e <nome>_req.json e chama o CLI."""
import hashlib, json, subprocess, sys
from pathlib import Path

W = Path(r"C:\IALD\Central de Patentes\work\central_publica_22out")
REF = r"C:\IALD\MEMORIA_IALD\sessions\claude-central-a7_central-publica-22out.json"
nome, rev = sys.argv[1], int(sys.argv[2])
spec = json.loads((W / ("acom_%s.json" % nome)).read_text(encoding="utf-8"))
for r in spec["records"]:
    for s in r.get("sources", []):
        if s.get("kind") == "artifact":
            s["sha256"] = hashlib.sha256(Path(s["ref"]).read_bytes()).hexdigest()
ch = W / ("%s_changes.json" % nome)
ch.write_text(json.dumps({"records": spec["records"], "flow": spec["flow"]}, ensure_ascii=False), encoding="utf-8")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": spec["event_id"],
       "actor": {"id": "claude-central-a7", "kind": "agent"}, "changes_file": str(ch),
       "changes_sha256": hashlib.sha256(ch.read_bytes()).hexdigest()}
rq = W / ("%s_req.json" % nome)
rq.write_text(json.dumps(req, ensure_ascii=False), encoding="utf-8")
out = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=rq.read_bytes(),
                     capture_output=True)
txt = out.stdout.decode("utf-8", "replace")
try:
    d = json.loads(txt)
    rc = d.get("result", {}).get("receipt") or d.get("receipt") or {}
    print("ok:", d.get("ok"), "| revision:", rc.get("revision"), "| event:", rc.get("event_id"), "| erro:", d.get("error"), d.get("message", "")[:300])
except json.JSONDecodeError:
    print(txt[:1500], out.stderr.decode("utf-8", "replace")[:800])
