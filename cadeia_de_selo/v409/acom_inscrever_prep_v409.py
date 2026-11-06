# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] so' adaptado (ato da gerencia, nao executado pelo construtor): o uso, a unidade e o revisor (D58) da v409; o texto de abertura LE os numeros dos arquivos (nada digitado); o proximo passo com o fim no HANDOFF (D57a)
"""Memoria ACOM da PREPARACAO da v409 (gerencia c1, 05/11/2026; molde: acom_inscrever_prep_v408.py): inscreve a fonte original (DESENHO_v409.md, por sha256 lido do arquivo)
e grava SESSION_REFERENCE_prep_v409.json. Uso: `acom_inscrever_prep_v409.py` (init + get + transition de abertura + verify) ou `acom_inscrever_prep_v409.py --fechar` (transition de conclusao,
que le PREPARACAO_v409_PRONTA.json). Recibos ao lado. Nao autoriza acoes, nao move gate. Molde: acom_inscrever_prep_v408.py."""
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


OBJ = os.path.join(H, "DESENHO_v409.md")
REF = os.path.join(H, "SESSION_REFERENCE_prep_v409.json")
ACTOR = {"id": "claude-c1-prep-v409", "kind": "agent"}
if not os.path.exists(REF):
    rc, j = chamar({"operation": "init", "objective_file": OBJ, "objective_sha256": sha(OBJ), "request_id": str(uuid.uuid4()),
                    "scope": {"house": "IALD", "principal": "luiz-antonio-rotoli-miguel"}, "actor": ACTOR, "write_reference": REF,
                    "constraints": {"unit": "preparacao_e_cadeia_de_selo_v409_traducao_as_classes_de_turing", "no_science_gate_credentials_trust_or_user_permission_changes": True,
                                    "nothing_written_in_the_Nos_except_by_the_installer_and_the_seal_rite": True, "operator_gates_remain_operator_gates": True,
                                    "no_install_no_rite_no_commit_no_push": True, "reviewer_distinct_from_builder": "Sonnet (D58 da v409, como a D54 da v408; ordem do operador, 02/11, sha16 eddcb27b6ec724bf)"}}, "init")
    assert rc == 0 and os.path.exists(REF), "init falhou"
rc, gj = chamar({"operation": "get", "reference": REF}, "get")
rev = gj["result"]["revision"]
print("revision atual:", rev)
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}
_lj = lambda n_: (json.load(open(os.path.join(H, n_), encoding="utf-8")) if os.path.exists(os.path.join(H, n_)) else {})
_cm, _en, _pc, _pr = _lj("CANDIDATO_v409.json"), _lj("ensaio_a_seco_v409.json"), _lj("PRECONDICOES_v409.json"), _lj("PREPARACAO_v409_PRONTA.json")   # (v409) os numeros sao LIDOS destes arquivos, nunca digitados
_n_p00 = len(_pc.get("checagens") or []); _ok_p00 = sum(1 for c_ in (_pc.get("checagens") or []) if c_.get("ok")); _port = _pr.get("portoes") or {}
if not FECHAR:
    records = [{"id": "prep-v409-aberta", "kind": "fact", "statute": "REAL",
                "text": "Preparacao da v409 (A traducao as classes de Turing e o par na face de Fock): 2 modulos (TraducaoTuring e ParNaFaceDeFock; o nome TraducaoTuring e os nomes das declaracoes das rodadas R1 a R8, dados pela gerencia c1, foram RATIFICADOS pelo operador em 05/11/2026 («concordo com todos os nomes que foram dados»); os nomes acrescentados na R9 (a inscricao no psion e a formula SAT) e os da ParNaFaceDeFock, tambem da gerencia, foram RATIFICADOS por ele em 05/11/2026 («Ratifico os nomes», D62); D55) no sandbox k409c; kernel construido e auditado; candidato %s, ensaio a seco %s, p00 %s/%s, PRONTA %s/%s portoes (pronta=%s), pelo construtor (agente); revisao de terceiro do Sonnet (D58) em curso. Nada instalado no Nos; rito nao rodado; sem commit/push." % (_cm.get("sha16"), _en.get("veredito"), _ok_p00, _n_p00, sum(1 for v_ in _port.values() if v_), len(_port), _pr.get("pronta")),
                "sources": [S(OBJ), S(os.path.join(H, "BUNDLE_v409.json"))]}]
    rc, tj = chamar({"operation": "transition", "reference": REF, "actor": ACTOR, "expected_revision": rev, "event_id": "prep-v409-aberta-05nov",
                     "changes": {"records": records, "flow": {"phase": "preparacao_v409__pronta__revisao_de_terceiro", "next_action": "revisao do Sonnet (REVISAO_TERCEIRO_v409.json); fechar_preparacao_v409; a gerencia lanca o orquestrador pos_treino_v409"}}}, "transition")
else:
    pronta = os.path.join(H, "PREPARACAO_v409_PRONTA.json")
    assert os.path.exists(pronta), "PREPARACAO_v409_PRONTA.json nao existe"
    pj = json.load(open(pronta, encoding="utf-8"))
    records = [{"id": "prep-v409-fechada", "kind": "fact", "statute": "REAL",
                "text": "Preparacao da v409 fechada: pronta=%s; candidato %s; falta=%s. Quem constroi nao aprova: a revisao de terceiro e do Sonnet (REVISAO_TERCEIRO_v409.json). Nada instalado; rito nao rodado." % (pj.get("pronta"), pj.get("candidato_sha16"), pj.get("falta")),
                "sources": [S(pronta), S(os.path.join(H, "RELATORIO_PREPARACAO_v409.md"))]}]
    rc, tj = chamar({"operation": "transition", "reference": REF, "actor": ACTOR, "expected_revision": rev, "event_id": "prep-v409-fechada-%s" % ts,
                     "changes": {"records": records, "flow": {"phase": "preparacao_v409__fechada", "next_action": "a gerencia lanca o orquestrador pos_treino_v409.py (instalar, rito, pos-rito, os textos da custodia e o HANDOFF, que e' o fim da cadeia desta versao; a custodia completa e o release do app sao da sessao de custodia, D57a)"}}}, "transition")
print("transition rc", rc)
rc, vj = chamar({"operation": "verify", "reference": REF}, "verify")
print("REFERENCIA:", REF)
