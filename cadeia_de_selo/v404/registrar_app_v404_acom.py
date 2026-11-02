# -*- coding: utf-8 -*-
"""ACOM da sessão c1 (rev 12 -> 13), 29/10/2026: a release do app v404 (C21) fechada pela sessão do site e CONFERIDA pela gerência; unidade
F9.APP_V404_20261029 AUDITADA (evento 1359); G1 v404 42/42; quadro 87 OK / 0 DEFASADO / 4 do operador; a RPI não lida hoje (INPI 503)."""
import hashlib, json, subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
PY = "C:/Python314/python.exe"; sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
CEN = "C:/IALD/Central de Patentes"
CONF = CEN + "/work/iald_v404_20261029/gerencia_c1/CONFERENCIA_GERENCIA_APP_V404_29out.json"; c = json.loads(Path(CONF).read_text(encoding="utf-8")); assert c["veredito"] == "CONFERIDA"
IV = CEN + "/work/iald_v404_20261029/INSTALLED_VERIFICATION.json"; RF = CEN + "/work/iald_v404_20261029/validation/review_final.json"; Q = CEN + "/organismo/ESTADO_DO_ORGANISMO.json"
REF = CEN + "/work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json"
def sm(p):
    r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(p, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (json.loads(r.stdout) if r.stdout.strip().startswith("{") else {"raw": (r.stdout + r.stderr)[:400]})
rc, g = sm({"operation": "get", "reference": REF}); rev = (g.get("result") or {}).get("revision"); print("get rc", rc, "rev", rev); assert rev is not None, g
S = lambda p: {"kind": "artifact", "ref": p.replace("/", chr(92)) + "#sha256:" + sha(p)}
texto = ("%s: C21 fechado pela sessão do site (gerência a7): app v402 -> v404 instalado (backend compartilhado, sem build nova de cliente), construtor sonnet-app-v404-construtor e revisor sonnet-app-v404-revisor distintos, "
         "review_final PASS, deploy 30/30 (1464 arquivos), verify 14/14, nenhuma chamada paga; decisões da a7 registradas no depósito (haiku55 política D; shared variante F; pino do público em 1d3c4cbe). "
         "Conferida pela gerência c1 por script: 13/13 (hashes declarados = disco; source_sha256 = pin do um.py do Nós lido agora; quadro lê v404; git limpo = remoto). Unidade F9.APP_V404_20261029 AUDITADA (evento 1359); "
         "depósito claude-site promovido ao tópico do app (seq 149). G1 v404: 42/42, CUSTODIADA (E19 e C19 rodados pela a7). Quadro 09:22:45: 87 OK, 0 DEFASADO, 4 PENDENTE_OPERADOR (iald.ia.br x3, Zenodo). "
         "Falha visível do dia: a RPI não foi lida (INPI HTTP 503 às 09:00 e 09:24; commit 0d8e6444 da a7); não é «sem movimentação». NOT_FALSIFIED nunca é CONFIRMED; PROVADA = validade; o gate não se moveu." % time.strftime("%d/%m/%Y %H:%M"))
rc, t = sm({"operation": "transition", "reference": REF, "actor": {"id": "claude-c1", "kind": "agent"}, "expected_revision": rev, "event_id": "c1-app-v404-conferido-c21-fechado-29out",
            "changes": {"records": [{"id": "c1-app-v404-conferido-c21-fechado", "kind": "fact", "statute": "REAL", "sources": [S(CONF), S(IV), S(RF), S(Q)], "text": texto}],
                        "flow": {"phase": "v404_COMPLETA__custodia_42_42__V7_no_ar__vitrine_X_aceita__app_v404_conferido__so_decisoes_do_operador",
                                 "next_action": "nada da v404 pende da gerência. Vigiar: RPI (INPI 503 hoje; sentinela 09:00 de amanhã), X diário 17:30, consulta diária 03:00. Ao operador: login WIPO (2FA) e o e-mail de preparações técnicas com a agente de PI [LEGAL]; E0; D2; iald.ia.br (llms/sitemap/robots 404); Zenodo (v401 -> v404); nome definitivo da pedra ProjecaoTransversalDaMeiaNat; conjunto D fechado salvo ordem. Molde da v405: passo do G1 para CUSTODIA_vNNN.txt + adendos 022/026; app como perna do G1 com a7; compactação da base do haiku55 (lição da a7 para a v406)."}}})
print("transition rc", rc, "rev", (t.get("result") or {}).get("revision"), t.get("message", "") or t.get("raw", ""))
