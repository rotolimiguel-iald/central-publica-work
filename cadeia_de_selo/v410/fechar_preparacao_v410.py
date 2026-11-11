# -*- coding: utf-8 -*-
# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h), claude-subagente-adaptacao (Sonnet 5.5, A), a servico do construtor claude-construtor-v410] so' a PROSA da anotacao e do deposito: a v410 agora e' IALD2 e A Escala (D82 a D87), com o H0DN x BG1 pré-registrado e o recibo documental HMS/13 (D80); dois modulos; os nomes RATIFICADOS (D74 e D87); a excecao D80 ao veto da pasta do Kimi; segue ato da gerencia, NAO executado pelo adaptador
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_conferidores_v410.py] o registro ABERTO do Mapa e' um objeto, nao lista (o [0] quebrava); segue ato da gerencia, nao executado pelo construtor
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] so' adaptado (ato da gerencia, nao executado pelo construtor): a prosa da v410 (Mapa, fila, ACOM: a moldura da D64 e as ressalvas), o revisor pela D69, o slug de 06/11; conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
"""fechar_preparacao_v410.py -- o fim da preparacao, depois de gerar_relatorio_v410.py: (1) a ANOTACAO de fechamento da rota do Mapa de Rotas aberta pela preparacao (o rota_id e' LIDO de registro_mapa_prep_v410_ABERTA.json, que a gerencia abre); (2) o DEPOSITO na fila da memoria (so' a gerencia escreve o MEMORY.md); (3) a transicao ACOM da referencia propria (SESSION_REFERENCE_prep_v410.json).
Tudo LE PREPARACAO_v410_PRONTA.json: nenhum hash e' digitado aqui. Idempotente por marcador (.FECHADA_<sha16 do PRONTA>): uma segunda rodada com o mesmo PRONTA nao repete nada. Molde: fechar_preparacao_v409.py, adaptado em 06/11/2026 a v410 por claude-construtor-v410 (IALD2: bundle de 1 modulo em TGLExt/, registro iald2_v410; nenhuma chave antiga muda).
FAIL-CLOSED ANTES de qualquer efeito: exige PREPARACAO_v410_PRONTA.json, a SESSION_REFERENCE_prep_v410.json (a inscricao ACOM da preparacao, ato da gerencia), o registro_mapa_prep_v410_ABERTA.json (de onde vem a rota) e os artefatos que a anotacao cita; sem eles PARA sem escrever no Mapa, na fila nem na ACOM.
NAO foi executado na adaptacao (ato do gerente, depois do gerar_relatorio_v410.py e da revisao de terceiro).
uso: python -I -B -X utf8 fechar_preparacao_v410.py"""
import hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PR = os.path.join(HERE, "PREPARACAO_v410_PRONTA.json"); J = json.load(open(PR, encoding="utf-8")); S = hashlib.sha256(open(PR, "rb").read()).hexdigest()[:16]
MARCA = os.path.join(HERE, ".FECHADA_" + S)
if os.path.exists(MARCA):
    print("ja fechada para este PRONTA:", S); sys.exit(0)
PY = r"C:\Python314\python.exe"
REF_ = os.path.join(HERE, "SESSION_REFERENCE_prep_v410.json")
ABERTA_ = os.path.join(HERE, "registro_mapa_prep_v410_ABERTA.json")
for _n_ in (REF_, ABERTA_, os.path.join(HERE, "RELATORIO_PREPARACAO_v410.md"), os.path.join(HERE, "PLANO_v410.md")):
    assert os.path.exists(_n_), ("FAIL-CLOSED: falta %s -- nao registro no Mapa, nao deposito na fila e nao transiciono a ACOM (a inscricao ACOM e a rota da preparacao v410 sao ato da gerencia)" % os.path.basename(_n_))
_ab0 = json.load(open(ABERTA_, encoding="utf-8")); _ab = _ab0[0] if isinstance(_ab0, list) else _ab0   # (09/11: o registro ABERTO do Mapa da v410 e' UM objeto; o da v409 era lista -- achado do revisor Sonnet)
ROTA = _ab["rota_id"]; REFS = list(_ab.get("refs") or [])   # a rota e as rotas-mae sao LIDAS do registro que a gerencia abriu: nada digitado
MEM = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "memoria.py")
ROTAS = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py")
port = J["portoes"]; p_ok = [k for k, v in port.items() if v]; p_no = [k for k, v in port.items() if not v]
res = ("candidato %s (%s B, base v409 %s); pronta=%s; portoes que passaram: %s; que nao passaram: %s; kernel recibo %s (bundle de %s modulos novos em TGLExt/); ESPERADOS %s; p00 %s (%s/%s; pendentes: %s); ensaio a seco %s; escada %s; %s bandeiras novas" % (
    J["candidato_sha16"], format(J["candidato_bytes"], ","), J["origem_sha16"], J["pronta"], ", ".join(p_ok), ", ".join(p_no) or "nenhum", J["kernel_recibo"]["sha16"], J.get("n_modulos_novos"), J["esperados_sha16"], J["p00"]["sha16"], J["p00"]["passaram"], J["p00"]["n"], len(J["p00"].get("pendentes") or []), J["ensaio_a_seco"]["veredito"], J["escada"], J["n_bandeiras_novas"]))
# (1) o Mapa
anot = [{"tipo": "ANOTACAO", "rota_id": ROTA, "estatuto": "REAL", "olhou_dados": False,
         "titulo": "v410 preparada (IALD2 e AEscala, 06 a 09/11/2026): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]), "resultado": res,
         "proximo_passo": "revisao de terceiro (o Sonnet, D69: ate' tres rodadas; quem constroi nao aprova); depois o orquestrador instala, roda o rito e a cadeia; a rota da versao selada sera a da v410",
         "nota": "quem constroi nao aprova: " + J["nao_revisado_por_terceiro"], "artefatos": [PR, os.path.join(HERE, "RELATORIO_PREPARACAO_v410.md"), os.path.join(HERE, "PLANO_v410.md")], "refs": REFS}]
ja = os.path.join(HERE, "registro_mapa_preparacao_v410_ANOTACAO.json")
tmp = ja + ".tmp"; open(tmp, "w", encoding="utf-8").write(json.dumps(anot, ensure_ascii=False, indent=1)); os.replace(tmp, ja)
r1 = subprocess.run([PY, "-B", "-X", "utf8", ROTAS, "registrar", ja, "--quem", "claude-construtor-v410"], capture_output=True, text=True, encoding="utf-8")
print("mapa:", r1.returncode, r1.stdout[-240:].replace("\n", " "))
assert r1.returncode == 0, r1.stdout + r1.stderr
# (2) a fila da memoria
txt = ("v410 (IALD2: o leitor do codigo, a releitura que nao acrescenta, o algoritmo IALD, o signo e o seletor; A Escala: os pesos das faces de 1/2 e o Clay no dicionario da TGL, D82 a D87; o teste H0DN x BG1, pré-registrado; nenhum dado observado lido, com o recibo documental HMS/13, D80) preparada em 06 e 09/11/2026 por claude-construtor-v410 para a gerencia c1 (nada instalado; o rito nao rodou). " + res + ".\n\n"
       "A moldura vale em todo texto: a IALD le o codigo (le o par como par, uno, com a Meia-Nat); ao quadrado e' ela mesma (reler nao acrescenta); o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora; a forma de matriz finita e' o signo; validade no kernel, nao creditacao; o gate nao se move. "
       "As ressalvas vao ditas: com o leitor que so' conta vale NP contido em P com o leitor (Cook-Levin [KNOWN]) e a igualdade relativizada nao esta' provada para o contador (E28); que a IALD, a Torre ou o operador SEJAM o funtor, e que o codigo SEJA um vetor de H1, sao leituras do operador, nao termos; o funtor nao e' idempotente (a leitura e'); o par finito (Bell 4x4) e o par de Fock sao espacos distintos, com a mesma Meia-Nat; a instancia do seletor e' de forma (D70); de uma fala de 06/11 so' o trecho entra (D65); nenhum teste com a natureza entra; a regra do 4,44 vale em qualquer texto que o cite. Os nomes: o NOME do modulo, IALD2, e' do operador (06/11/2026); os nomes das declaracoes da IALD2 sao da gerencia c1 e foram RATIFICADOS pelo operador em 09/11/2026 (D74); o nome do modulo AEscala e os nomes das declaracoes dela tambem (D87). "
       "A Escala (validade no kernel; a creditacao e' do Clay): o Nome pesa 1 = 1/2 + 1/2, a face sem par nao conjuga, tres faces de 1/2 pesam 3/2, 1/3 caiu e o Nome normalizado e' 2/3. O recibo HMS/13 (D80): cobertura documental de fontes, não covariância física fechada; nada aberto; a excecao D80 ao veto da pasta do Kimi vale so' para os seis artefatos documentais, por sha256, lidos so' no build; em rito nada de kimi e' aberto.\n\n"
       "Avisos para a gerencia:\n" + "\n".join("- " + a for a in J["avisos"]) + "\n\nQuem constroi nao aprova: " + J["nao_revisado_por_terceiro"] + ".\n")
ta = os.path.join(HERE, "DEPOSITO_PREPARACAO_v410.md")
tmp = ta + ".tmp"; open(tmp, "w", encoding="utf-8").write(txt); os.replace(tmp, ta)
r2 = subprocess.run([PY, "-X", "utf8", MEM, "depositar", "--quem", "claude-construtor-v410", "--tipo", "project", "--estatuto", "REAL", "--alvo", "novo:v410-preparada-06nov", "--casa", "Central de Patentes", "--slug", "v410-preparada-06nov",
                     "--fonte", PR, "--fonte", os.path.join(HERE, "RELATORIO_PREPARACAO_v410.md"), "--texto-arquivo", ta], capture_output=True, text=True, encoding="utf-8")
print("fila:", r2.returncode, (r2.stdout + r2.stderr)[-300:].replace("\n", " "))
assert r2.returncode == 0, r2.stdout + r2.stderr
# (3) a transicao ACOM (revisao lida agora; evento estavel pelo sha16 do PRONTA)
ref = REF_; CLI = [PY, "-X", "utf8", os.path.join("C:" + os.sep, "IALD", "MEMORIA_IALD", "session_memory.py")]
g = subprocess.run(CLI, input=json.dumps({"operation": "get", "reference": ref}), capture_output=True, text=True, encoding="utf-8"); rev = json.loads(g.stdout)["result"]["revision"]
req = {"operation": "transition", "reference": ref, "expected_revision": rev, "event_id": "prep-v410-fechada-" + S, "actor": {"id": "claude-construtor-v410", "kind": "agent"},
       "changes": {"records": [{"id": "prep_v410_fechada_" + S, "kind": "fact", "statute": "REAL", "text": res, "sources": [{"kind": "artifact", "ref": PR}]}], "flow": {"phase": "entregue_a_gerencia", "next_action": "a gerencia e o orquestrador pos-treino decidem a partir de PREPARACAO_v410_PRONTA.json"}}}
r3 = subprocess.run(CLI, input=json.dumps(req, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8")
print("acom:", r3.returncode, r3.stdout[:160])
assert r3.returncode == 0, r3.stdout + r3.stderr
open(MARCA, "w", encoding="utf-8").write(S + "\n")
print("preparacao fechada:", S)
