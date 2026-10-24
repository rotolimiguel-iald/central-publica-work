# -*- coding: utf-8 -*-
"""Inscrição ACOM da custódia v398 (24/10/2026, sessão a7 da Central): a ordem é a regra do operador «pode custodiar sempre que o handoff
aparecer, como regra», verbatim por sha256 lido; o gatilho foram as três marcas da v398 no Nós (selo 00:26; stdout 01:31; handoff 01:40;
bloco do diário)."""
import hashlib, json, subprocess, sys, uuid
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
W = Path("C:/IALD/Central de Patentes/work/custodia_v398_24out")
obj = Path("C:/IALD/Central de Patentes/work/php_e_v396_22out/OPERADOR_23out_custodiar_quando_o_handoff_aparecer_verbatim.txt")
REF = "C:/IALD/MEMORIA_IALD/sessions/claude-central-a7_custodia-v398-24out.json"
req = {"operation": "init", "objective_file": str(obj), "objective_sha256": hashlib.sha256(obj.read_bytes()).hexdigest(),
       "request_id": str(uuid.uuid4()), "scope": {"house": "IALD", "principal": "operator"},
       "actor": {"id": "claude-central-a7", "kind": "agent"}, "write_reference": REF}
(W / "init_req.json").write_text(json.dumps(req, ensure_ascii=False), encoding="utf-8")
r = subprocess.run(["C:/Python314/python.exe", "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=(W / "init_req.json").read_bytes(), capture_output=True)
d = json.loads(r.stdout.decode("utf-8", "replace"))
print("ok:", d.get("ok"), "| objetivo:", req["objective_sha256"][:16], "| erro:", d.get("error"), str(d.get("message", ""))[:200])
