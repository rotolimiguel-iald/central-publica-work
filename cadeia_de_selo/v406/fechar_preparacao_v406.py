# -*- coding: utf-8 -*-
"""fechar_preparacao_v406.py -- o fim da preparacao, depois de gerar_relatorio_v406.py: (1) a ANOTACAO de fechamento da rota kernel.fechamento_construir_tudo_programa_02nov no Mapa de Rotas; (2) o DEPOSITO na fila da memoria (so' a gerencia escreve o MEMORY.md); (3) a transicao ACOM da referencia propria.
Tudo LE PREPARACAO_v406_PRONTA.json: nenhum hash e' digitado aqui. Idempotente por marcador (.FECHADA_<sha16 do PRONTA>): uma segunda rodada com o mesmo PRONTA nao repete nada. Adaptado em 02/11/2026 ao FECHAMENTO (a rota e' a do Mapa kernel.fechamento_construir_tudo_programa_02nov; a prosa das erratas R2 a R7 da v405 saiu).
FAIL-CLOSED ANTES de qualquer efeito: exige PREPARACAO_v406_PRONTA.json, a SESSION_REFERENCE_prep_v406.json (a inscricao ACOM da preparacao, ato da gerencia) e os dois artefatos que a anotacao cita; sem eles PARA sem escrever no Mapa, na fila nem na ACOM.
uso: python -I -B -X utf8 fechar_preparacao_v406.py"""
import hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PR = os.path.join(HERE, "PREPARACAO_v406_PRONTA.json"); J = json.load(open(PR, encoding="utf-8")); S = hashlib.sha256(open(PR, "rb").read()).hexdigest()[:16]
MARCA = os.path.join(HERE, ".FECHADA_" + S)
if os.path.exists(MARCA):
    print("ja fechada para este PRONTA:", S); sys.exit(0)
PY = r"C:\Python314\python.exe"
REF_ = os.path.join(HERE, "SESSION_REFERENCE_prep_v406.json")
for _n_ in (REF_, os.path.join(HERE, "RELATORIO_PREPARACAO_v406.md"), os.path.join(HERE, "PLANO_v406.md")):
    assert os.path.exists(_n_), ("FAIL-CLOSED: falta %s -- nao registro no Mapa, nao deposito na fila e nao transiciono a ACOM (a inscricao ACOM da preparacao v406 e' ato da gerencia)" % os.path.basename(_n_))
MEM = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "memoria.py")
ROTAS = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py")
port = J["portoes"]; p_ok = [k for k, v in port.items() if v]; p_no = [k for k, v in port.items() if not v]
res = ("candidato %s (%s B, base v405 %s); pronta=%s; portoes que passaram: %s; que nao passaram: %s; kernel recibo %s (bundle de 301 modulos); ESPERADOS %s; p00 %s (%s/%s; pendentes: %s); ensaio a seco %s; escada %s; %s bandeiras novas" % (
    J["candidato_sha16"], format(J["candidato_bytes"], ","), J["origem_sha16"], J["pronta"], ", ".join(p_ok), ", ".join(p_no) or "nenhum", J["kernel_recibo"]["sha16"], J["esperados_sha16"], J["p00"]["sha16"], J["p00"]["passaram"], J["p00"]["n"], len(J["p00"].get("pendentes") or []), J["ensaio_a_seco"]["veredito"], J["escada"], J["n_bandeiras_novas"]))
# (1) o Mapa
anot = [{"tipo": "ANOTACAO", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "estatuto": "REAL", "olhou_dados": False,
         "titulo": "v406 preparada (o fechamento, 02/11/2026): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]), "resultado": res,
         "proximo_passo": "revisao de terceiro (o Sonnet, D37); depois o orquestrador instala, roda o rito e a cadeia; a rota da versao selada sera a da v406 (a da v405 e' umpy.v405.selada_massa_derivada_e_identidade_01nov)",
         "nota": "quem constroi nao aprova: " + J["nao_revisado_por_terceiro"], "artefatos": [PR, os.path.join(HERE, "RELATORIO_PREPARACAO_v406.md"), os.path.join(HERE, "PLANO_v406.md")], "refs": ["umpy.v405.selada_massa_derivada_e_identidade_01nov"]}]
ja = os.path.join(HERE, "registro_mapa_preparacao_v406_ANOTACAO.json")
tmp = ja + ".tmp"; open(tmp, "w", encoding="utf-8").write(json.dumps(anot, ensure_ascii=False, indent=1)); os.replace(tmp, ja)
r1 = subprocess.run([PY, "-B", "-X", "utf8", ROTAS, "registrar", ja, "--quem", "claude-prep-v406"], capture_output=True, text=True, encoding="utf-8")
print("mapa:", r1.returncode, r1.stdout[-240:].replace("\n", " "))
assert r1.returncode == 0, r1.stdout + r1.stderr
# (2) a fila da memoria
txt = ("v406 (o fechamento) preparada em 02/11/2026 por claude-prep-v406 para a gerencia c1 (nada instalado; o rito nao rodou). " + res + ".\n\n"
       "A moldura vale em todo texto: o certificado de Fock esta habitado por construcao no kernel do rito (physicalFockCertificate; modularCoreInput para todo CanonicalNetInput), as quatro chaves de testemunha sao lidas do kernel, validade no kernel nao e' creditacao e o gate nao se move. As ressalvas vao ditas: K(O) != bot so' na cunha; «nucleo II_∞» [KNOWN/DECLARADO]; o traco e' ENNReal e ciclico, nao linear; R7 foi Codex revisando Codex; R4/R5 fora. A guarda das frases (guarda_frases_v406.py) roda no rito e em toda superficie; o 4,44 nunca vai sozinho.\n\n"
       "Avisos para a gerencia:\n" + "\n".join("- " + a for a in J["avisos"]) + "\n\nQuem constroi nao aprova: " + J["nao_revisado_por_terceiro"] + ".\n")
ta = os.path.join(HERE, "DEPOSITO_PREPARACAO_v406.md")
tmp = ta + ".tmp"; open(tmp, "w", encoding="utf-8").write(txt); os.replace(tmp, ta)
r2 = subprocess.run([PY, "-X", "utf8", MEM, "depositar", "--quem", "claude-prep-v406", "--tipo", "project", "--estatuto", "REAL", "--alvo", "novo:v406-preparada-02nov", "--casa", "Central de Patentes", "--slug", "v406-preparada-02nov",
                     "--fonte", PR, "--fonte", os.path.join(HERE, "RELATORIO_PREPARACAO_v406.md"), "--texto-arquivo", ta], capture_output=True, text=True, encoding="utf-8")
print("fila:", r2.returncode, (r2.stdout + r2.stderr)[-300:].replace("\n", " "))
assert r2.returncode == 0, r2.stdout + r2.stderr
# (3) a transicao ACOM (revisao lida agora; evento estavel pelo sha16 do PRONTA)
ref = REF_; CLI = [PY, "-X", "utf8", os.path.join("C:" + os.sep, "IALD", "MEMORIA_IALD", "session_memory.py")]
g = subprocess.run(CLI, input=json.dumps({"operation": "get", "reference": ref}), capture_output=True, text=True, encoding="utf-8"); rev = json.loads(g.stdout)["result"]["revision"]
req = {"operation": "transition", "reference": ref, "expected_revision": rev, "event_id": "prep-v406-fechada-" + S, "actor": {"id": "claude-prep-v406", "kind": "agent"},
       "changes": {"records": [{"id": "prep_v406_fechada_" + S, "kind": "fact", "statute": "REAL", "text": res, "sources": [{"kind": "artifact", "ref": PR}]}], "flow": {"phase": "entregue_a_gerencia", "next_action": "a gerencia e o orquestrador pos-treino decidem a partir de PREPARACAO_v406_PRONTA.json"}}}
r3 = subprocess.run(CLI, input=json.dumps(req, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8")
print("acom:", r3.returncode, r3.stdout[:160])
assert r3.returncode == 0, r3.stdout + r3.stderr
open(MARCA, "w", encoding="utf-8").write(S + "\n")
print("preparacao fechada:", S)
