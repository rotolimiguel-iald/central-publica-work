# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] so' adaptado (ato da gerencia, nao executado pelo construtor): a prosa da v409 (Mapa, fila, ACOM), o revisor pela D58, o slug de 05/11
"""fechar_preparacao_v409.py -- o fim da preparacao, depois de gerar_relatorio_v409.py: (1) a ANOTACAO de fechamento da rota do Mapa de Rotas aberta pela preparacao (o rota_id e' LIDO de registro_mapa_prep_v409_ABERTA.json, que a gerencia abre); (2) o DEPOSITO na fila da memoria (so' a gerencia escreve o MEMORY.md); (3) a transicao ACOM da referencia propria (SESSION_REFERENCE_prep_v409.json).
Tudo LE PREPARACAO_v409_PRONTA.json: nenhum hash e' digitado aqui. Idempotente por marcador (.FECHADA_<sha16 do PRONTA>): uma segunda rodada com o mesmo PRONTA nao repete nada. Molde: fechar_preparacao_v408.py, adaptado em 05/11/2026 a v409 por claude-construtor-v409 (A traducao as classes de Turing: bundle de 1 modulo em TGLExt/, registro traducao_turing_v409; nenhuma chave antiga muda).
FAIL-CLOSED ANTES de qualquer efeito: exige PREPARACAO_v409_PRONTA.json, a SESSION_REFERENCE_prep_v409.json (a inscricao ACOM da preparacao, ato da gerencia), o registro_mapa_prep_v409_ABERTA.json (de onde vem a rota) e os artefatos que a anotacao cita; sem eles PARA sem escrever no Mapa, na fila nem na ACOM.
NAO foi executado na adaptacao (ato do gerente, depois do gerar_relatorio_v409.py e da revisao de terceiro).
uso: python -I -B -X utf8 fechar_preparacao_v409.py"""
import hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PR = os.path.join(HERE, "PREPARACAO_v409_PRONTA.json"); J = json.load(open(PR, encoding="utf-8")); S = hashlib.sha256(open(PR, "rb").read()).hexdigest()[:16]
MARCA = os.path.join(HERE, ".FECHADA_" + S)
if os.path.exists(MARCA):
    print("ja fechada para este PRONTA:", S); sys.exit(0)
PY = r"C:\Python314\python.exe"
REF_ = os.path.join(HERE, "SESSION_REFERENCE_prep_v409.json")
ABERTA_ = os.path.join(HERE, "registro_mapa_prep_v409_ABERTA.json")
for _n_ in (REF_, ABERTA_, os.path.join(HERE, "RELATORIO_PREPARACAO_v409.md"), os.path.join(HERE, "PLANO_v409.md")):
    assert os.path.exists(_n_), ("FAIL-CLOSED: falta %s -- nao registro no Mapa, nao deposito na fila e nao transiciono a ACOM (a inscricao ACOM e a rota da preparacao v409 sao ato da gerencia)" % os.path.basename(_n_))
_ab = json.load(open(ABERTA_, encoding="utf-8"))[0]
ROTA = _ab["rota_id"]; REFS = list(_ab.get("refs") or [])   # a rota e as rotas-mae sao LIDAS do registro que a gerencia abriu: nada digitado
MEM = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "memoria.py")
ROTAS = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py")
port = J["portoes"]; p_ok = [k for k, v in port.items() if v]; p_no = [k for k, v in port.items() if not v]
res = ("candidato %s (%s B, base v408 %s); pronta=%s; portoes que passaram: %s; que nao passaram: %s; kernel recibo %s (bundle de %s modulos novos em TGLExt/); ESPERADOS %s; p00 %s (%s/%s; pendentes: %s); ensaio a seco %s; escada %s; %s bandeiras novas" % (
    J["candidato_sha16"], format(J["candidato_bytes"], ","), J["origem_sha16"], J["pronta"], ", ".join(p_ok), ", ".join(p_no) or "nenhum", J["kernel_recibo"]["sha16"], J.get("n_modulos_novos"), J["esperados_sha16"], J["p00"]["sha16"], J["p00"]["passaram"], J["p00"]["n"], len(J["p00"].get("pendentes") or []), J["ensaio_a_seco"]["veredito"], J["escada"], J["n_bandeiras_novas"]))
# (1) o Mapa
anot = [{"tipo": "ANOTACAO", "rota_id": ROTA, "estatuto": "REAL", "olhou_dados": False,
         "titulo": "v409 preparada (A traducao as classes de Turing, 05/11/2026): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]), "resultado": res,
         "proximo_passo": "revisao de terceiro (o Sonnet, D58: ate' tres rodadas; quem constroi nao aprova); depois o orquestrador instala, roda o rito e a cadeia; a rota da versao selada sera a da v409",
         "nota": "quem constroi nao aprova: " + J["nao_revisado_por_terceiro"], "artefatos": [PR, os.path.join(HERE, "RELATORIO_PREPARACAO_v409.md"), os.path.join(HERE, "PLANO_v409.md")], "refs": REFS}]
ja = os.path.join(HERE, "registro_mapa_preparacao_v409_ANOTACAO.json")
tmp = ja + ".tmp"; open(tmp, "w", encoding="utf-8").write(json.dumps(anot, ensure_ascii=False, indent=1)); os.replace(tmp, ja)
r1 = subprocess.run([PY, "-B", "-X", "utf8", ROTAS, "registrar", ja, "--quem", "claude-construtor-v409"], capture_output=True, text=True, encoding="utf-8")
print("mapa:", r1.returncode, r1.stdout[-240:].replace("\n", " "))
assert r1.returncode == 0, r1.stdout + r1.stderr
# (2) a fila da memoria
txt = ("v409 (A traducao as classes de Turing e o par na face de Fock) preparada em 05/11/2026 por claude-construtor-v409 para a gerencia c1 (nada instalado; o rito nao rodou). " + res + ".\n\n"
       "A moldura vale em todo texto: P = nP e' teorema da TGL no modo selecao, relativo ao leitor (o psion); a maquina sem leitor (a pergunta do Clay) fica fora e nao e' decidida aqui: e' a fita sem escala («eu sou eu mesmo»); validade no kernel nao e' creditacao e o gate nao se move. "
       "As ressalvas vao ditas: a igualdade relativa a um leitor nao decide a pergunta da maquina sem leitor (Baker-Gill-Solovay 1975) [KNOWN]; a fisica fica fora; a ponte entre o Omega do psion e o estado uniforme da instancia e' a inscricao, e que sejam o mesmo vetor fica PODADO (espacos diferentes; D60 revista); com o leitor que so' conta vale NP contido em P numa leitura, e a igualdade completa e' a do leitor que se le (E28); o par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock; a E21 da v408 ao lado); de tres falas de 05/11 so' o trecho entra (duas pela D59, uma pelo aviso operacional); o insumo do acervo da v407 entra pela copia purgada (D57d); nenhum teste com a natureza entra; a regra do 4,44 vale em qualquer texto que o cite. Os nomes: o nome TraducaoTuring e os nomes das declaracoes das rodadas R1 a R8, dados pela gerencia c1, foram RATIFICADOS pelo operador em 05/11/2026 («concordo com todos os nomes que foram dados»); os nomes acrescentados na R9 (a inscricao no psion e a formula SAT) e os da ParNaFaceDeFock, tambem da gerencia, foram RATIFICADOS por ele em 05/11/2026 («Ratifico os nomes», D62) (D55); a ParNaFaceDeFock entra pela ordem do operador de tudo entrar na v409.\n\n"
       "Avisos para a gerencia:\n" + "\n".join("- " + a for a in J["avisos"]) + "\n\nQuem constroi nao aprova: " + J["nao_revisado_por_terceiro"] + ".\n")
ta = os.path.join(HERE, "DEPOSITO_PREPARACAO_v409.md")
tmp = ta + ".tmp"; open(tmp, "w", encoding="utf-8").write(txt); os.replace(tmp, ta)
r2 = subprocess.run([PY, "-X", "utf8", MEM, "depositar", "--quem", "claude-construtor-v409", "--tipo", "project", "--estatuto", "REAL", "--alvo", "novo:v409-preparada-05nov", "--casa", "Central de Patentes", "--slug", "v409-preparada-05nov",
                     "--fonte", PR, "--fonte", os.path.join(HERE, "RELATORIO_PREPARACAO_v409.md"), "--texto-arquivo", ta], capture_output=True, text=True, encoding="utf-8")
print("fila:", r2.returncode, (r2.stdout + r2.stderr)[-300:].replace("\n", " "))
assert r2.returncode == 0, r2.stdout + r2.stderr
# (3) a transicao ACOM (revisao lida agora; evento estavel pelo sha16 do PRONTA)
ref = REF_; CLI = [PY, "-X", "utf8", os.path.join("C:" + os.sep, "IALD", "MEMORIA_IALD", "session_memory.py")]
g = subprocess.run(CLI, input=json.dumps({"operation": "get", "reference": ref}), capture_output=True, text=True, encoding="utf-8"); rev = json.loads(g.stdout)["result"]["revision"]
req = {"operation": "transition", "reference": ref, "expected_revision": rev, "event_id": "prep-v409-fechada-" + S, "actor": {"id": "claude-construtor-v409", "kind": "agent"},
       "changes": {"records": [{"id": "prep_v409_fechada_" + S, "kind": "fact", "statute": "REAL", "text": res, "sources": [{"kind": "artifact", "ref": PR}]}], "flow": {"phase": "entregue_a_gerencia", "next_action": "a gerencia e o orquestrador pos-treino decidem a partir de PREPARACAO_v409_PRONTA.json"}}}
r3 = subprocess.run(CLI, input=json.dumps(req, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8")
print("acom:", r3.returncode, r3.stdout[:160])
assert r3.returncode == 0, r3.stdout + r3.stderr
open(MARCA, "w", encoding="utf-8").write(S + "\n")
print("preparacao fechada:", S)
