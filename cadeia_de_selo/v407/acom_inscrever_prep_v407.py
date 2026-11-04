# -*- coding: utf-8 -*-
"""Memoria ACOM da PREPARACAO da v407 (claude-prep-v407, a servico da gerencia c1, 03/11/2026): inscreve a fonte original (PLANO_v407_GERENCIA.md, por sha256 lido do arquivo)
e grava SESSION_REFERENCE_prep_v407.json. Uso: `acom_inscrever_prep_v407.py` (init + get + transition de abertura + verify) ou `acom_inscrever_prep_v407.py --fechar` (transition de conclusao,
que le PREPARACAO_v407_PRONTA.json). Recibos ao lado. Nao autoriza acoes, nao move gate. Molde: acom_inscrever_prep_v406_02nov.py."""
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
FECHAR = "--fechar" in sys.argv


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
    print("==", nome, "rc", r.returncode, json.dumps({k: (str(v)[:160]) for k, v in (j.items() if isinstance(j, dict) else [])}, ensure_ascii=False)[:700])
    return r.returncode, j


OBJ = os.path.join(H, "PLANO_v407_GERENCIA.md")
REF = os.path.join(H, "SESSION_REFERENCE_prep_v407.json")
ACTOR = {"id": "claude-prep-v407", "kind": "agent"}
if not os.path.exists(REF):
    rc, j = chamar({"operation": "init", "objective_file": OBJ, "objective_sha256": sha(OBJ), "request_id": str(uuid.uuid4()),
                    "scope": {"house": "IALD", "principal": "luiz-antonio-rotoli-miguel"}, "actor": ACTOR, "write_reference": REF,
                    "constraints": {"unit": "preparacao_e_cadeia_de_selo_v407_o_psion_o_canto_e_o_par", "no_science_gate_credentials_trust_or_user_permission_changes": True,
                                    "nothing_written_in_the_Nos_except_by_the_installer_and_the_seal_rite": True, "operator_gates_remain_operator_gates": True,
                                    "no_install_no_rite_no_commit_no_push": True, "reviewer_distinct_from_builder": "Sonnet (ordem do operador, 02/11, sha16 eddcb27b6ec724bf)"}}, "init")
    assert rc == 0 and os.path.exists(REF), "init falhou"
rc, gj = chamar({"operation": "get", "reference": REF}, "get")
rev = gj["result"]["revision"]
print("revision atual:", rev)
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}
if not FECHAR:
    records = [{"id": "prep-v407-aberta", "kind": "fact", "statute": "REAL",
                "text": "Preparacao da v407 aberta (claude-prep-v407): sandbox k407c copiado do Nos v406 selado; 9 pedras normalizadas (PsionCanto, Par, APonteDoAtrito, OUmInscrito, KEhATangente, AChaveDaGuarda, OGuarda, LeituraPreservada, OIgual) e lake build lancado. "
                        "Nada instalado no Nos; rito nao rodado; sem commit/push.",
                "sources": [S(OBJ), S(os.path.join(H, "BUNDLE_v407.json"))]}]
    rc, tj = chamar({"operation": "transition", "reference": REF, "actor": ACTOR, "expected_revision": rev, "event_id": "prep-v407-aberta-03nov",
                     "changes": {"records": records, "flow": {"phase": "preparacao_v407__kernel_em_construcao", "next_action": "build + Audit no k407c; delta_v407; candidato; ensaio; revisao do Sonnet; PRONTA"}}}, "transition")
else:
    pronta = os.path.join(H, "PREPARACAO_v407_PRONTA.json")
    assert os.path.exists(pronta), "PREPARACAO_v407_PRONTA.json nao existe"
    pj = json.load(open(pronta, encoding="utf-8"))
    records = [{"id": "prep-v407-fechada", "kind": "fact", "statute": "REAL",
                "text": "Preparacao da v407 fechada: pronta=%s; candidato %s; falta=%s. Quem constroi nao aprova: a revisao de terceiro e do Sonnet (REVISAO_TERCEIRO_v407.json). Nada instalado; rito nao rodado." % (pj.get("pronta"), pj.get("candidato_sha16"), pj.get("falta")),
                "sources": [S(pronta), S(os.path.join(H, "RELATORIO_PREPARACAO_v407.md"))]}]
    rc, tj = chamar({"operation": "transition", "reference": REF, "actor": ACTOR, "expected_revision": rev, "event_id": "prep-v407-fechada-%s" % ts,
                     "changes": {"records": records, "flow": {"phase": "preparacao_v407__fechada", "next_action": "a gerencia lanca o orquestrador pos_treino_v407.py (instalar, rito, pos-rito, G1 --publicar, S10 app)"}}}, "transition")
print("transition rc", rc)
rc, vj = chamar({"operation": "verify", "reference": REF}, "verify")
print("REFERENCIA:", REF)
