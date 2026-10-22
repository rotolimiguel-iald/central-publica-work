# -*- coding: utf-8 -*-
"""Projecao SO DE LEITURA da referencia ACOM da gerencia c1 (operacao project) — auditor de estatuto R2 (F1.TEMPO).

Mesma forma dos scripts da R1 e do pre-registrador R2 (5_R2/0_ADENDO/scripts/acom_projecao_leitura_r2.py).
Guarda so o recibo, as contagens e os hashes; o texto projetado (memoria do pai) nao se copia para o disco.
Nenhum init e nenhuma transition: a tarefa proibe escrever na memoria (so em 5_R2/3_AUD_ESTATUTO) e a transicao de q/p
e ato da gerencia. O auditor nao recebeu referencia propria; projeta a da gerencia c1, so leitura, e confere que o
banco nao mudou.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

REF = r"C:\IALD\MEMORIA_IALD\sessions\claude-c1_exame-geral-12out.json"
CLI = r"C:\IALD\MEMORIA_IALD\session_memory.py"
PY = r"C:\Python314\python.exe"
DB = r"C:\IALD\MEMORIA_IALD\state\memory.sqlite3"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "saidas", "ACOM_RECIBO_PROJECAO_AUD_ESTATUTO_R2.json")


def stat(p):
    s = os.stat(p)
    return {"bytes": s.st_size, "mtime_ns": s.st_mtime_ns}


def main():
    antes = stat(DB)
    payload = json.dumps({"operation": "project", "reference": REF, "max_chars": 24000})
    t0 = time.strftime("%Y-%m-%d %H:%M:%S")
    r = subprocess.run([PY, "-X", "utf8", CLI], input=payload.encode("utf-8"),
                       capture_output=True, timeout=300)
    depois = stat(DB)
    raw = r.stdout
    resp = json.loads(raw.decode("utf-8"))
    receipt = resp.get("receipt") or resp.get("result", {}).get("receipt")
    proj = resp.get("projection") or resp.get("result", {}).get("projection")
    rec = {
        "nota": ("Recibo da projecao SO DE LEITURA da referencia ACOM da gerencia c1 "
                 "(session_memory.py, operacao project), pelo auditor de estatuto R2 da F1.TEMPO. "
                 "Guarda-se so o recibo e as contagens; o texto projetado (memoria do pai) nao se copia. "
                 "Nenhum init e nenhuma transition: a tarefa proibe escrever fora de 5_R2/3_AUD_ESTATUTO; "
                 "sem referencia propria, nao se adota outra tarefa."),
        "referencia": REF,
        "projecao_feita_em_local": t0,
        "codigo_de_saida": r.returncode,
        "receipt": receipt,
        "chaves_da_resposta": sorted(resp.keys()),
        "sha256_da_resposta_integral": hashlib.sha256(raw).hexdigest(),
        "bytes_da_resposta_integral": len(raw),
        "db_antes": antes,
        "db_depois": depois,
        "db_inalterado_pela_projecao": antes == depois,
    }
    for k in ("required_record_ids", "included_record_ids", "omitted_record_ids"):
        v = resp.get(k)
        if v is None and isinstance(resp.get("result"), dict):
            v = resp["result"].get(k)
        if isinstance(v, list):
            rec["n_" + k] = len(v)
    with open(OUT + ".tmp", "wb") as f:
        f.write(json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(OUT + ".tmp", OUT)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(rec, ensure_ascii=False, indent=1))
    print("=== PROJECAO (console, nao gravada) ===")
    if isinstance(proj, str):
        print(proj)
    else:
        print(json.dumps(resp, ensure_ascii=False, indent=1)[:30000])
    if r.stderr:
        print("STDERR:", r.stderr.decode("utf-8", "replace")[:2000])


if __name__ == "__main__":
    main()
