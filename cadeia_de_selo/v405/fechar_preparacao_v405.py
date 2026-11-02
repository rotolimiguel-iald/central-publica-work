# -*- coding: utf-8 -*-
"""fechar_preparacao_v405.py -- o fim da preparacao, depois de gerar_relatorio_v405.py: (1) a ANOTACAO de fechamento da rota kernel.v405.preparacao_01nov no Mapa de Rotas; (2) o DEPOSITO na fila da memoria (so' a gerencia escreve o MEMORY.md); (3) a transicao ACOM da referencia propria.
Tudo LE PREPARACAO_v405_PRONTA.json: nenhum hash e' digitado aqui. Idempotente por marcador (.FECHADA_<sha16 do PRONTA>): uma segunda rodada com o mesmo PRONTA nao repete nada. uso: python -I -B -X utf8 fechar_preparacao_v405.py"""
import hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PR = os.path.join(HERE, "PREPARACAO_v405_PRONTA.json"); J = json.load(open(PR, encoding="utf-8")); S = hashlib.sha256(open(PR, "rb").read()).hexdigest()[:16]
MARCA = os.path.join(HERE, ".FECHADA_" + S)
if os.path.exists(MARCA):
    print("ja fechada para este PRONTA:", S); sys.exit(0)
PY = r"C:\Python314\python.exe"
MEM = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "memoria.py")
ROTAS = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py")
port = J["portoes"]; p_ok = [k for k, v in port.items() if v]; p_no = [k for k, v in port.items() if not v]
res = ("candidato %s (%s B, base v404 %s); pronta=%s; portoes que passaram: %s; que nao passaram: %s; kernel recibo %s; ESPERADOS %s; p00 %s (%s/%s); ensaio a seco %s; escada %s; %s bandeiras novas" % (
    J["candidato_sha16"], format(J["candidato_bytes"], ","), J["origem_sha16"], J["pronta"], ", ".join(p_ok), ", ".join(p_no) or "nenhum", J["kernel_recibo"]["sha16"], J["esperados_sha16"], J["p00"]["sha16"], J["p00"]["passaram"], J["p00"]["n"], J["ensaio_a_seco"]["veredito"], J["escada"], J["n_bandeiras_novas"]))
# (1) o Mapa
anot = [{"tipo": "ANOTACAO", "rota_id": "kernel.v405.preparacao_01nov", "estatuto": "REAL", "olhou_dados": False,
         "titulo": "v405 preparada de novo, erratas R2 a R7 (01/11/2026): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]), "resultado": res,
         "proximo_passo": "o orquestrador da gerencia instala, roda o rito e a cadeia depois do treino da nativa; a rota da versao selada e' umpy.v405.selada_massa_derivada_e_identidade_01nov",
         "nota": "a segunda revisao de terceiro NAO aprovou o candidato anterior, eaefcd095abbaee7 (1 ALTO, 4 MEDIO, 11 BAIXO; caderno revisao_terceiro/REVISAO_TERCEIRO_v405.md; os 13 achados da primeira fecharam); esta e' a refacao pela errata R7 da gerencia. Quem constroi nao aprova: " + J["nao_revisado_por_terceiro"], "artefatos": [PR, os.path.join(HERE, "RELATORIO_PREPARACAO_v405.md"), os.path.join(HERE, "PLANO_v405.md")], "refs": ["umpy.v404.selada_jo8_32_e_projecao_transversal_28out"]},
        {"tipo": "ERRATA", "rota_id": "kernel.v405.preparacao_01nov", "corrige": 1606, "estatuto": "REAL", "olhou_dados": False, "titulo": "a anotacao de 20:40 dizia pronta=true para eaefcd095abbaee7: a segunda revisao de terceiro nao aprovou esse candidato",
         "resultado": "o candidato eaefcd095abbaee7 foi reprovado pela segunda revisao de terceiro; nenhuma prova caiu, nenhum numero estava errado e o gate nao foi tocado; o candidato vigente da preparacao e' " + J["candidato_sha16"], "nota": "correcao ao lado; a anotacao anterior fica como registro"}]
ja = os.path.join(HERE, "registro_mapa_preparacao_v405_ANOTACAO.json")
tmp = ja + ".tmp"; open(tmp, "w", encoding="utf-8").write(json.dumps(anot, ensure_ascii=False, indent=1)); os.replace(tmp, ja)
r1 = subprocess.run([PY, "-B", "-X", "utf8", ROTAS, "registrar", ja, "--quem", "claude-prep-v405"], capture_output=True, text=True, encoding="utf-8")
print("mapa:", r1.returncode, r1.stdout[-240:].replace("\n", " "))
assert r1.returncode == 0, r1.stdout + r1.stderr
# (2) a fila da memoria
txt = ("v405 preparada de novo em 01/11/2026 por claude-prep-v405 para a gerencia c1, pelas erratas R2 a R7, depois de a segunda revisao de terceiro nao aprovar o candidato eaefcd095abbaee7 (nada instalado; o rito nao rodou). Este deposito substitui o de 20:40 (20261101_204059_v405-preparada-r2.md, seq 191). " + res + ".\n\n"
       "A moldura vale em todo texto: os campos das estruturas fecharam, as leituras do operador passaram do campo para a definicao, a leitura fisica nao virou teorema. A guarda das frases (guarda_frases_v405.py) roda no rito e em toda superficie.\n\n"
       "Licoes novas: (1) nome longo de fala passa do MAX_PATH numa arvore emulada, logo a saida dos harnesses mora em caminho curto; (2) o JSON do rito real tem chaves no topo que o ensaio nao guarda, e a emulacao as le da constante do candidato; (3) a subida de versao funde os rotulos 403 e 404, e as pastas irmas e os registros recriados pedem regra propria; (4) a lista das falas e' congelada em VERBATIM_CONGELADO_v405.json, para que fala nova nao reprove o conferidor nem mude o candidato; (5) o corpus de uma conferencia de citacoes nao pode conter o texto conferido; (6) guarda que nao varre a origem deixa o residuo onde ninguem olha; (7) contagem literal envelhece quando um registro entra: a leitura exigia quatro registros por spec depois de o quinto entrar, e so' o harness pegou; (8) um harness que reprova cedo nao roda os controles negativos: a primeira passada limpa leva muito mais tempo que a reprovada, e nao e' travamento; (9) a mesma palavra para duas grandezas numa secao so' e' achado de ALTO, ainda que cada igualdade esteja certa: o gap espectral e o valor esperado precisavam de nomes distintos.\n\n"
       "Avisos para a gerencia:\n" + "\n".join("- " + a for a in J["avisos"]) + "\n\nQuem constroi nao aprova: " + J["nao_revisado_por_terceiro"] + ".\n")
ta = os.path.join(HERE, "DEPOSITO_PREPARACAO_v405.md")
tmp = ta + ".tmp"; open(tmp, "w", encoding="utf-8").write(txt); os.replace(tmp, ta)
r2 = subprocess.run([PY, "-X", "utf8", MEM, "depositar", "--quem", "claude-prep-v405", "--tipo", "project", "--estatuto", "REAL", "--alvo", "novo:v405-preparada-01nov", "--casa", "Central de Patentes", "--slug", "v405-preparada-r7",
                     "--fonte", PR, "--fonte", os.path.join(HERE, "RELATORIO_PREPARACAO_v405.md"), "--texto-arquivo", ta], capture_output=True, text=True, encoding="utf-8")
print("fila:", r2.returncode, (r2.stdout + r2.stderr)[-300:].replace("\n", " "))
assert r2.returncode == 0, r2.stdout + r2.stderr
# (3) a transicao ACOM (revisao lida agora; evento estavel pelo sha16 do PRONTA)
ref = os.path.join(HERE, "SESSION_REFERENCE_prep_v405.json"); CLI = [PY, "-X", "utf8", os.path.join("C:" + os.sep, "IALD", "MEMORIA_IALD", "session_memory.py")]
g = subprocess.run(CLI, input=json.dumps({"operation": "get", "reference": ref}), capture_output=True, text=True, encoding="utf-8"); rev = json.loads(g.stdout)["result"]["revision"]
req = {"operation": "transition", "reference": ref, "expected_revision": rev, "event_id": "prep-v405-r7-fechada-" + S, "actor": {"id": "claude-prep-v405", "kind": "agent"},
       "changes": {"records": [{"id": "prep_v405_fechada_" + S, "kind": "fact", "statute": "REAL", "text": res, "sources": [{"kind": "artifact", "ref": PR}]}], "flow": {"phase": "entregue_a_gerencia", "next_action": "a gerencia e o orquestrador pos-treino decidem a partir de PREPARACAO_v405_PRONTA.json"}}}
r3 = subprocess.run(CLI, input=json.dumps(req, ensure_ascii=False), capture_output=True, text=True, encoding="utf-8")
print("acom:", r3.returncode, r3.stdout[:160])
assert r3.returncode == 0, r3.stdout + r3.stderr
open(MARCA, "w", encoding="utf-8").write(S + "\n")
print("preparacao fechada:", S)
