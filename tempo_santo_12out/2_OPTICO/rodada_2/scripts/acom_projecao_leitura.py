"""Projecao SO DE LEITURA da referencia ACOM da gerencia c1 (rodada 2 do construtor otico F1.TEMPO).
Nenhuma inscricao (init) e nenhuma transition: a tarefa proibe escrever fora de 2_OPTICO e a
transicao de q/p e ato da gerencia. Guarda-se so o recibo e contagens; o texto projetado (memoria
do pai) nao se copia para a pasta. Confere tamanho e mtime do memory.sqlite3 antes e depois.
Uso: python -I -X utf8 acom_projecao_leitura.py <saida_recibo.json>"""
import datetime
import hashlib
import json
import os
import subprocess
import sys

CLI = r"C:\IALD\MEMORIA_IALD\session_memory.py"
PY = r"C:\Python314\python.exe"
REF = r"C:\IALD\MEMORIA_IALD\sessions\claude-c1_exame-geral-12out.json"
DB = r"C:\IALD\MEMORIA_IALD\state\memory.sqlite3"


def stat(p):
    st = os.stat(p)
    return {"bytes": st.st_size, "mtime_ns": st.st_mtime_ns,
            "mtime_utc": datetime.datetime.fromtimestamp(st.st_mtime, datetime.timezone.utc).isoformat()}


req = json.dumps({"operation": "project", "reference": REF, "max_chars": 24000}).encode("utf-8")
antes = stat(DB)
t = datetime.datetime.now(datetime.timezone.utc).isoformat()
cp = subprocess.run([PY, "-X", "utf8", CLI], input=req, capture_output=True, timeout=300)
depois = stat(DB)
raw = cp.stdout
rec = {
    "nota": "Projecao SO DE LEITURA (operacao project) da referencia ACOM da gerencia c1. Nenhum init e nenhuma transition (a tarefa proibe escrever na memoria; a transicao e ato da gerencia). Guarda-se so o recibo; o texto projetado nao se copia.",
    "referencia": REF,
    "feita_em_utc": t,
    "exit_code": cp.returncode,
    "stderr_sha256": hashlib.sha256(cp.stderr).hexdigest(),
    "sha256_da_resposta_integral": hashlib.sha256(raw).hexdigest(),
    "bytes_da_resposta_integral": len(raw),
    "db_antes": antes,
    "db_depois": depois,
    "db_igual_antes_depois": antes == depois,
}
try:
    d = json.loads(raw.decode("utf-8"))
    rec["ok"] = d.get("ok")
    rec["protocol"] = d.get("protocol")
    if isinstance(d.get("result"), dict):
        rec["chaves_do_result"] = sorted(d["result"].keys())
        d = dict(d, **d["result"])
    rec["receipt"] = d.get("receipt")
    for k in ("required_record_ids", "included_record_ids", "omitted_record_ids"):
        if k in d:
            rec["n_" + k] = len(d[k])
    for k in ("overflow", "projection_sha256"):
        if k in d:
            rec[k] = d[k]
    if "projection" in d and "projection_sha256" not in d:
        rec["projection_sha256_calculado"] = hashlib.sha256(str(d["projection"]).encode("utf-8")).hexdigest()
    if not d.get("ok"):
        rec["erro"] = {"error": d.get("error"), "message": d.get("message")}
    rec["chaves_da_resposta"] = sorted(d.keys())
except Exception as e:  # falha visivel, nunca ok falso
    rec["ok"] = False
    rec["erro_de_leitura"] = repr(e)
tmp = sys.argv[1] + ".tmp"
with open(tmp, "w", encoding="utf-8") as fo:
    json.dump(rec, fo, indent=1, ensure_ascii=False)
os.replace(tmp, sys.argv[1])
print(json.dumps({k: rec.get(k) for k in ("ok", "exit_code", "db_igual_antes_depois", "bytes_da_resposta_integral")}))
if rec.get("receipt"):
    print(json.dumps(rec["receipt"], ensure_ascii=False))
