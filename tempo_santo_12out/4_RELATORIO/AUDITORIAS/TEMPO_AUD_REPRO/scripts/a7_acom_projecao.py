"""A7 — projecao SO DE LEITURA (operation=project) da referencia ACOM da gerencia c1, pelo CLI instalado.
Sem init, sem transition (a tarefa proibe escrever fora da pasta do auditor). Guarda so o recibo e hashes;
o texto projetado nao e copiado. Confere mtime/tamanho do banco antes e depois."""
import hashlib
import json
import os
import subprocess
import sys
import time

REF = r"C:\IALD\MEMORIA_IALD\sessions\claude-c1_exame-geral-12out.json"
CLI = r"C:\IALD\MEMORIA_IALD\session_memory.py"
DB = r"C:\IALD\MEMORIA_IALD\state\memory.sqlite3"


def st(p):
    s = os.stat(p)
    return {"bytes": s.st_size, "mtime_ns": s.st_mtime_ns}


antes = st(DB)
req = json.dumps({"operation": "project", "reference": REF, "max_chars": 24000})
r = subprocess.run([sys.executable, "-X", "utf8", CLI], input=req.encode("utf-8"), capture_output=True)
time.sleep(0.5)
depois = st(DB)
out = {"referencia": REF, "exit": r.returncode, "db_antes": antes, "db_depois": depois, "db_igual": antes == depois,
       "sha256_resposta": hashlib.sha256(r.stdout).hexdigest(), "bytes_resposta": len(r.stdout),
       "stderr": r.stderr.decode("utf-8", "replace")[:500]}
try:
    resp = json.loads(r.stdout.decode("utf-8"))
    rec = resp.get("receipt") or {}
    out["receipt"] = {k: rec.get(k) for k in ("context_id", "revision", "event_id", "state_sha256", "objective_sha256",
                                               "anchor_sha256", "replayed")}
    out["chaves_da_resposta"] = sorted(resp.keys())
except Exception as e:
    out["erro_parse"] = repr(e)
with open(sys.argv[1], "w", encoding="utf-8") as fo:
    json.dump(out, fo, indent=1, ensure_ascii=False)
print(json.dumps(out, ensure_ascii=False, indent=1))
