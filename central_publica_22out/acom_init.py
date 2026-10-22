# -*- coding: utf-8 -*-
"""Inscrição ACOM da tarefa «Central pública» (sessão a7 da Central, 22/10/2026): o objetivo é a fala do operador, verbatim, por sha256 lido.
As duas mensagens seguintes do operador (a autorização soberana e «segredo são dados pessoais, somente») entram como decisões na 1ª transição."""
import hashlib, json, subprocess, uuid
from pathlib import Path

W = Path(r"C:\IALD\Central de Patentes\work\central_publica_22out")
obj = W / "OPERADOR_22out_central_publica_verbatim.txt"
REF = r"C:\IALD\MEMORIA_IALD\sessions\claude-central-a7_central-publica-22out.json"
req = {"operation": "init", "objective_file": str(obj), "objective_sha256": hashlib.sha256(obj.read_bytes()).hexdigest(),
       "request_id": str(uuid.uuid4()), "scope": {"house": "IALD", "principal": "operator"},
       "actor": {"id": "claude-central-a7", "kind": "agent"}, "write_reference": REF}
(W / "init_req.json").write_text(json.dumps(req, ensure_ascii=False), encoding="utf-8")
r = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"],
                   input=(W / "init_req.json").read_bytes(), capture_output=True)
d = json.loads(r.stdout.decode("utf-8", "replace"))
rc = (d.get("result") or {}).get("receipt") or d.get("receipt") or {}
print("ok:", d.get("ok"), "| objetivo:", req["objective_sha256"][:16], "| erro:", d.get("error"), str(d.get("message", ""))[:200])
