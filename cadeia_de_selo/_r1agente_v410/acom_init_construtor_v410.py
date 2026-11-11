# -*- coding: utf-8 -*-
"""acom_init_construtor_v410.py -- memoria ACOM da PREPARACAO da v410: o agente claude-construtor-v410 inscreve a SUA referencia (init da fonte original
DESENHO_v410.md, sha256 LIDO do arquivo) e grava SESSION_REFERENCE_prep_v410.json; depois faz `project` (so' leitura). Molde: acom_init_construtor_v409.py.
Nao adota a tarefa de outra sessao; nao autoriza acoes; nao move gate. A transicao de abertura/fecho e' da gerencia (acom_inscrever_prep_v410.py).
Uso: C:\\Python314\\python.exe -X utf8 acom_init_construtor_v410.py   (reexecutavel: se a referencia existe, so' faz project)"""
import datetime
import hashlib
import json
import os
import subprocess
import sys
import uuid

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
PY = r"C:\Python314\python.exe"
SM = r"C:\IALD\MEMORIA_IALD\session_memory.py"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")


def chamar(payload, nome):
    req = os.path.join(H, "acom_prep_%s_%s.request.json" % (ts, nome))
    rec = os.path.join(H, "acom_prep_%s_%s.receipt.json" % (ts, nome))
    open(req, "w", encoding="utf-8").write(json.dumps(payload, ensure_ascii=False, indent=1))
    r = subprocess.run([PY, "-X", "utf8", SM], input=json.dumps(payload, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    open(rec, "w", encoding="utf-8").write(out + ("\n--- stderr ---\n" + err if err else ""))
    try:
        j = json.loads(out)
    except Exception:  # noqa: BLE001
        j = {"raw": out[:600], "stderr": err[:600]}
    print("==", nome, "rc", r.returncode, json.dumps({k: (str(v)[:200]) for k, v in (j.items() if isinstance(j, dict) else [])}, ensure_ascii=False)[:900])
    return r.returncode, j


OBJ = os.path.join(H, "DESENHO_v410.md")
REF = os.path.join(H, "SESSION_REFERENCE_prep_v410.json")
ACTOR = {"id": "claude-construtor-v410", "kind": "agent"}
if not os.path.exists(REF):
    rc, j = chamar({"operation": "init", "objective_file": OBJ, "objective_sha256": sha(OBJ), "request_id": str(uuid.uuid4()),
                    "scope": {"house": "IALD", "principal": "luiz-antonio-rotoli-miguel"}, "actor": ACTOR, "write_reference": REF,
                    "constraints": {"unit": "preparacao_e_cadeia_de_selo_v410_iald2", "no_science_gate_credentials_trust_or_user_permission_changes": True,
                                    "nothing_written_in_the_Nos_except_by_the_installer_and_the_seal_rite": True, "operator_gates_remain_operator_gates": True,
                                    "no_install_no_rite_no_commit_no_push": True, "reviewer_distinct_from_builder": "Sonnet (D69; ordem do operador, 02/11, sha16 eddcb27b6ec724bf)"}}, "init")
    assert rc == 0 and os.path.exists(REF), "init falhou"
rc, pj = chamar({"operation": "project", "reference": REF}, "project")
assert rc == 0, "project falhou"
print("referencia:", REF, "sha16", sha(REF)[:16])
