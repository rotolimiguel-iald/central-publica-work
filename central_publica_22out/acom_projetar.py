# -*- coding: utf-8 -*-
"""project (só leitura) da própria referência ACOM desta tarefa: revisão, fase, próxima ação."""
import json, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
REF = r"C:\IALD\MEMORIA_IALD\sessions\claude-central-a7_central-publica-22out.json"
req = json.dumps({"operation": "project", "reference": REF}).encode("utf-8")
out = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=req, capture_output=True)
d = json.loads(out.stdout.decode("utf-8", "replace"))
r = d.get("result", d)
print("ok:", d.get("ok"), "| erro:", d.get("error"), d.get("message", "")[:200])
print("chaves:", list(r.keys())[:20])
for k in ("revision", "state_revision", "task_id"):
    if k in r:
        print(k, "=", r[k])
proj = r.get("projection") or r
fl = proj.get("flow") or {}
print("fluxo:", json.dumps(fl, ensure_ascii=False)[:600])
print("q (n registros):", len((proj.get("state") or {}).get("records", []) or proj.get("records", []) or []))
