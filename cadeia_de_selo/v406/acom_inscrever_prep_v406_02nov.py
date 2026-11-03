# -*- coding: utf-8 -*-
"""Memoria ACOM da PREPARACAO da v406 (gerencia c1, 02/11/2026): inscreve a fonte original (a ordem verbatim do operador de 02/11: «quando terminar, compile a nova versão do um.py, rode, publique e atualize tudo por favor»)
e grava SESSION_REFERENCE_prep_v406.json, que fechar_preparacao_v406.py exige (a transition da preparacao fechada e' dele). Recibos ao lado. Nao autoriza acoes, nao move gate. Molde: acom_inscrever_sessao_c1_28out.py."""
import hashlib, json, os, subprocess, sys, uuid, datetime
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
PY = r"C:\Python314\python.exe"; SM = r"C:\IALD\MEMORIA_IALD\session_memory.py"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")


def chamar(payload, nome):
    req = os.path.join(H, "acom_prep_%s_%s.request.json" % (ts, nome)); rec = os.path.join(H, "acom_prep_%s_%s.receipt.json" % (ts, nome))
    open(req, "w", encoding="utf-8").write(json.dumps(payload, ensure_ascii=False, indent=1))
    r = subprocess.run([PY, "-X", "utf8", SM], input=json.dumps(payload, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "").strip(); err = (r.stderr or "").strip()
    open(rec, "w", encoding="utf-8").write(out + ("\n--- stderr ---\n" + err if err else ""))
    try:
        j = json.loads(out)
    except Exception:  # noqa: BLE001
        j = {"raw": out[:600], "stderr": err[:600]}
    print("==", nome, "rc", r.returncode, json.dumps({k: (str(v)[:160]) for k, v in (j.items() if isinstance(j, dict) else [])}, ensure_ascii=False)[:700])
    return r.returncode, j


OBJ = r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_02nov_quando_terminar_compile_v406_rode_publique_atualize_tudo_e_planeje_o_readme_pinado_com_o_4_44_sigma_verbatim.txt"
assert sha(OBJ)[:16] == "b5717ff445a883cd", sha(OBJ)[:16]
REF = os.path.join(H, "SESSION_REFERENCE_prep_v406.json")
if not os.path.exists(REF):
    rc, j = chamar({"operation": "init", "objective_file": OBJ, "objective_sha256": sha(OBJ), "request_id": str(uuid.uuid4()),
                    "scope": {"house": "IALD", "principal": "luiz-antonio-rotoli-miguel"}, "actor": {"id": "claude-c1", "kind": "agent"},
                    "write_reference": REF,
                    "constraints": {"unit": "preparacao_e_cadeia_de_selo_v406_o_fechamento", "no_science_gate_credentials_trust_or_user_permission_changes": True,
                                    "nothing_written_in_the_Nos_except_by_the_installer_and_the_seal_rite": True, "operator_gates_remain_operator_gates": True, "reviewer_distinct_from_builder": "Sonnet (ordem do operador, 02/11, sha16 eddcb27b6ec724bf)"}}, "init")
    assert rc == 0 and os.path.exists(REF), "init falhou"
rc, gj = chamar({"operation": "get", "reference": REF}, "get")
rev = gj["result"]["revision"]; print("revision atual:", rev)
S = lambda p: {"kind": "artifact", "ref": p + "#sha256:" + sha(p)}
C = os.path.join(H, "CANDIDATO_v406.json")
records = [{"id": "prep-v406-candidato-e-ensaio", "kind": "fact", "statute": "REAL",
            "text": "Preparacao da v406 (o fechamento entra no um.py): kernel do sandbox k406c construido (301 modulos; build 1736 s; Audit 280 s; 1794 bandeiras; escada 11860; TOTAL 33732/26911/0; 8 ancoras no trio), candidato gerado e ensaio a seco TUDO PASSOU (fechamento_v406 14/14; as quatro chaves de testemunha lidas do kernel; gate identico a v405). Em curso: conferidor/esperados/p00, pos-rito e textos, B(n) pre-selo, revisao de terceiro (Sonnet), orquestrador (instalar, rito, pos-rito, G1 --publicar).",
            "sources": [S(C), S(os.path.join(H, "kernel", "POS_BUILD_v406.json")), S(os.path.join(H, "CONTRATO_DA_CADEIA_v406.md"))]}]
rc, tj = chamar({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "prep-v406-aberta-02nov",
                 "changes": {"records": records, "flow": {"phase": "preparacao_v406__cadeia_em_curso", "next_action": "fechar a preparacao (PRONTA) depois do refazer, do B(n) pre-selo e da revisao de terceiro; entao o orquestrador instala e roda o rito"}}}, "transition")
print("transition rc", rc)
rc, vj = chamar({"operation": "verify", "reference": REF}, "verify")
print("REFERENCIA:", REF)
