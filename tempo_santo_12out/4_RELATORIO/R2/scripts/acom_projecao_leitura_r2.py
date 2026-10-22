# -*- coding: utf-8 -*-
"""Projecao SO DE LEITURA da referencia ACOM da gerencia c1 (operacao project), para o redator R2.
Guarda so o recibo e os hashes; nenhum init, nenhuma transition (a tarefa proibe escrever na memoria)."""
import hashlib, json, os, subprocess, sys, time
REF = r"C:\IALD\MEMORIA_IALD\sessions\claude-c1_exame-geral-12out.json"
CLI = r"C:\IALD\MEMORIA_IALD\session_memory.py"
PY = r"C:\Python314\python.exe"
DB = r"C:\IALD\MEMORIA_IALD\state\memory.sqlite3"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas", "ACOM_RECIBO_PROJECAO_RELATORIO_R2.json")


def stat(p):
    s = os.stat(p)
    return {"bytes": s.st_size, "mtime_ns": s.st_mtime_ns}


antes = stat(DB)
payload = json.dumps({"operation": "project", "reference": REF, "max_chars": 24000})
t0 = time.strftime("%Y-%m-%d %H:%M:%S")
r = subprocess.run([PY, "-X", "utf8", CLI], input=payload.encode("utf-8"), capture_output=True, timeout=300)
depois = stat(DB)
raw = r.stdout
try:
    resp = json.loads(raw.decode("utf-8"))
except Exception as e:
    resp = {"erro_parse": repr(e)}
receipt = resp.get("receipt") or (resp.get("result") or {}).get("receipt") if isinstance(resp, dict) else None
proj = resp.get("projection") or (resp.get("result") or {}).get("projection") if isinstance(resp, dict) else None
rec = {"nota": "Recibo da projecao SO DE LEITURA (project) da referencia ACOM da gerencia c1, pelo redator R2 da F1.TEMPO. Nenhum init, nenhuma transition.",
       "referencia": REF, "quando_local": t0, "codigo_de_saida": r.returncode, "receipt": receipt,
       "chaves_da_resposta": sorted(resp.keys()) if isinstance(resp, dict) else None,
       "sha256_da_resposta_integral": hashlib.sha256(raw).hexdigest(), "bytes_da_resposta_integral": len(raw),
       "db_antes": antes, "db_depois": depois, "db_inalterado_pela_projecao": antes == depois}
with open(OUT + ".tmp", "wb") as f:
    f.write(json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8"))
os.replace(OUT + ".tmp", OUT)
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps(rec, ensure_ascii=False, indent=1))
print("=== PROJECAO (console, nao gravada) ===")
if isinstance(proj, str):
    print(proj[:12000])
else:
    print(json.dumps(resp, ensure_ascii=False, indent=1)[:12000])
if r.stderr:
    print("STDERR:", r.stderr.decode("utf-8", "replace")[:1500])
