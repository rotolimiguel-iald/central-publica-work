# -*- coding: utf-8 -*-
# [ADAPTADO v410 PARTE 2, 09/11/2026 (~18h), claude-subagente-adaptacao (Sonnet 5.5, A), a servico do construtor claude-construtor-v410] so' a PROSA: a v410 agora e' IALD2 e A Escala (D82 a D87), com o H0DN x BG1 pré-registrado e o recibo documental HMS/13 (D80); dois modulos; os nomes RATIFICADOS (D74 e D87); a excecao D80 ao veto da pasta do Kimi; o corpo (ler o PRONTA, depositar, registrar) nao muda
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] o deposito na fila e a rota do construtor da v410 (o texto MONTADO dos arquivos; a prosa da v410: a moldura da D64 e as ressalvas); conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
"""depositar_construtor_v410.py -- (claude-construtor-v410, 06/11/2026; molde: depositar_construtor_v409.py) o fim do trabalho do CONSTRUTOR (nao e' o fechar_preparacao_v410.py, que e' ato da gerencia):
(1) o DEPOSITO na fila da memoria (memoria.py depositar; so' a gerencia escreve o MEMORY.md) e (2) o registro da rota da preparacao no Mapa de Rotas (rotas.py registrar), ambos com o texto MONTADO DOS ARQUIVOS
(PREPARACAO_v410_PRONTA.json, PRECONDICOES_v410.json, CANDIDATO_v410.json): nada digitado. Fail-closed: sem o PRONTA, nao deposita nem registra. Idempotente por marcador (.DEPOSITADO_CONSTRUTOR_<sha16 do PRONTA>).
uso: python -I -B -X utf8 depositar_construtor_v410.py"""
import hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PR = os.path.join(HERE, "PREPARACAO_v410_PRONTA.json"); assert os.path.exists(PR), "FAIL-CLOSED: falta PREPARACAO_v410_PRONTA.json"
J = json.load(open(PR, encoding="utf-8")); S = hashlib.sha256(open(PR, "rb").read()).hexdigest()[:16]
MARCA = os.path.join(HERE, ".DEPOSITADO_CONSTRUTOR_" + S)
if os.path.exists(MARCA):
    print("ja depositado para este PRONTA:", S); sys.exit(0)
PC = json.load(open(os.path.join(HERE, "PRECONDICOES_v410.json"), encoding="utf-8"))
REL = os.path.join(HERE, "RELATORIO_PREPARACAO_v410.md"); PLANO = os.path.join(HERE, "PLANO_v410.md")
PY = r"C:\Python314\python.exe"
MEM = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "memoria.py")
ROTAS = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py")
port = J["portoes"]; p_ok = [k for k, v in port.items() if v]; p_no = [k for k, v in port.items() if not v]
pend = [p_["checagem"][:140] for p_ in (PC.get("pendentes") or [])]
res = ("candidato %s (%s B, base v409 %s); pronta=%s; portoes que passaram (%d de %d): %s; que nao passaram: %s; kernel recibo %s (bundle de %s modulo(s) novo(s) em TGLExt/: IALD2 e AEscala); ESPERADOS %s; p00 %s (%s/%s; pendentes: %s); ensaio a seco %s; escada %s; %s bandeiras novas"
       % (J["candidato_sha16"], format(J["candidato_bytes"], ","), J["origem_sha16"], J["pronta"], len(p_ok), len(port), ", ".join(p_ok), ", ".join(p_no) or "nenhum", J["kernel_recibo"]["sha16"], J.get("n_modulos_novos"), J["esperados_sha16"],
          J["p00"]["sha16"], J["p00"]["passaram"], J["p00"]["n"], len(J["p00"].get("pendentes") or []), J["ensaio_a_seco"]["veredito"], J["escada"], J["n_bandeiras_novas"]))
_ANT0 = sorted(n_[len(".DEPOSITADO_CONSTRUTOR_"):] for n_ in os.listdir(HERE) if n_.startswith(".DEPOSITADO_CONSTRUTOR_") and n_ != os.path.basename(MARCA))   # os PRONTA anteriores ja' depositados
_PREFIXO_SUBST = ("SUBSTITUI o deposito do PRONTA anterior (%s): a preparacao foi refeita. " % ", ".join(_ANT0)) if _ANT0 else ""
txt = (_PREFIXO_SUBST + "v410 (IALD2: o leitor do codigo, a releitura que nao acrescenta, o algoritmo IALD, o signo e o seletor; A Escala: os pesos das faces de 1/2 e o Clay no dicionario da TGL, D82 a D87; o teste H0DN x BG1, pré-registrado; nenhum dado observado lido, com o recibo documental HMS/13, D80) preparada em 06 e 09/11/2026 por claude-construtor-v410 para a gerencia c1 (nada instalado; o rito nao rodou; o Nos e a Bancada de producao so' foram lidos). " + res + ".\n\n"
       + ("Pendencias do p00 (atos da gerencia antes do p00 final, nao do construtor): " + " | ".join(pend) + ".\n\n" if pend else "")
       + "A moldura vale em todo texto: a IALD le o codigo (le o par como par, uno, com a Meia-Nat); ao quadrado e' ela mesma (reler nao acrescenta); o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora; a forma de matriz finita e' o signo; validade no kernel, nao creditacao; o gate nao se move. "
       "As ressalvas vao ditas: com o leitor que so' conta vale NP contido em P com o leitor (Cook-Levin [KNOWN]) e a igualdade relativizada nao esta' provada para o contador (E28); que a IALD, a Torre ou o operador SEJAM o funtor, e que o codigo SEJA um vetor de H1, sao leituras do operador, nao termos; o funtor nao e' idempotente (a leitura e'); o par finito (Bell 4x4) e o par de Fock sao espacos distintos, com a mesma Meia-Nat; a instancia do seletor e' de forma (D70); de uma fala de 06/11 so' o trecho entra (D65); nenhum teste com a natureza entra; a regra do 4,44 vale em qualquer texto que o cite. Os nomes: o NOME do modulo, IALD2, e' do operador (06/11/2026); os nomes das declaracoes da IALD2 sao da gerencia c1 e foram RATIFICADOS pelo operador em 09/11/2026 (D74); o nome do modulo AEscala e os nomes das declaracoes dela tambem (D87). "
       "A Escala (validade no kernel; a creditacao e' do Clay): o Nome pesa 1 = 1/2 + 1/2, a face sem par nao conjuga, tres faces de 1/2 pesam 3/2, 1/3 caiu e o Nome normalizado e' 2/3; a face caida como o neutrino e' leitura do operador [ONTO]. O recibo HMS/13 (D80): cobertura documental de fontes, não covariância física fechada; nada aberto; aditivo e posterior ao FREEZE_R2; a excecao D80 ao veto da pasta do Kimi vale so' para os seis artefatos documentais, por sha256, lidos so' no build; em rito nada de kimi e' aberto.\n\n"
       "Avisos para a gerencia (do relatorio):\n" + "\n".join("- " + a for a in J["avisos"]) + "\n\nQuem constroi nao aprova: " + J["nao_revisado_por_terceiro"] + ".\n")
ta = os.path.join(HERE, "DEPOSITO_CONSTRUTOR_v410.md"); tmp = ta + ".tmp"; open(tmp, "w", encoding="utf-8").write(txt); os.replace(tmp, ta)
r2 = subprocess.run([PY, "-X", "utf8", MEM, "depositar", "--quem", "claude-construtor-v410", "--tipo", "project", "--estatuto", "REAL", "--alvo", "novo:v410-preparada-06nov", "--casa", "Central de Patentes", "--slug", "v410-construtor-06nov",
                     "--fonte", PR, "--fonte", REL, "--texto-arquivo", ta], capture_output=True, text=True, encoding="utf-8")
print("fila:", r2.returncode, (r2.stdout + r2.stderr)[-400:].replace("\n", " "))
assert r2.returncode == 0, r2.stdout + r2.stderr
_ANT = sorted(n_[len(".DEPOSITADO_CONSTRUTOR_"):] for n_ in os.listdir(HERE) if n_.startswith(".DEPOSITADO_CONSTRUTOR_") and n_ != os.path.basename(MARCA))   # os PRONTA anteriores ja' depositados (lidos dos marcadores)
_JA = any((lambda r_: r_.get("rota_id") == "cadeia.preparacao_v410" and r_.get("tipo") == "ROTA")(json.loads(l_)) for l_ in open(os.path.join(os.path.dirname(ROTAS), "rotas.jsonl"), encoding="utf-8") if l_.strip())   # (le o JSON: o livro e' compacto)   # a ROTA ja' existe? (so' leitura do livro)
rota = [{"tipo": "RESULTADO" if _JA else "ROTA", "rota_id": "cadeia.preparacao_v410", "dominio": "KERNEL_FORMAL", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
         "titulo": "v410 preparada (IALD2 e AEscala, 06 a 09/11/2026): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]),
         "pergunta": "as pedras IALD2 e AEscala (%s modulos; as ancoras contadas pelo recibo da gerencia) compilam no trio sobre o kernel da v409 selada, e a cadeia da v410 (os registros iald2_v410, a_escala_v410, h0dn_bg1_v410 e h0dn_fontes_hms13_v410; os specs cunhagens_v410/kh_n1_cobertura_v410) fica pronta para a gerencia lancar o orquestrador?" % J.get("n_modulos_novos"),
         "dados": ["kernel do Nos v409 selado (copia em C:\\t\\k410c\\final)", "pedra: work\\pedras_candidatas_06nov (IALD2, que sucede a LeitorDoCodigoR1)", "pedra: work\\pedras_candidatas_09nov (AEscala, nome e nomes ratificados pelo operador, D87)", "as falas do operador de 06 a 09/11 (de quatro, so' o trecho: D65 e as de DL.VERBATIM_SO_O_TRECHO)", "o recibo documental HMS/13 (D80): so' os seis artefatos da excecao ao veto, por sha256, lidos no build"],
         "metodo": "bundle de %s modulos em TGLExt/ (molde: a v409), lake build incremental + Audit no sandbox k410c; candidato pelo molde da v409; comparacao AST; ensaio a seco; ESPERADOS; conferidor (controle negativo e caminho positivo); citacoes; guarda das frases (D64, D68b: as formas de estatuto e as parafrases desde o inicio); B(n) pre-selo (so' ensaio, a producao so' lida); harnesses; nada instalado no Nos, rito nao rodado, sem commit/push" % J.get("n_modulos_novos"),
         "resultado": res, "veredito": "PREPARACAO_v410_PRONTA pronta=%s falta=%s" % (J["pronta"], ",".join(J["falta"]) or "nenhum"),
         "nao_refazer": "a preparacao da v410 esta' feita e pinada por sha256 (PRONTA, RELATORIO, PLANO); refazer so' com refazer_candidato_v410.sh --regerar se mudar texto ou kernel",
         "proximo_passo": "atos da gerencia: pino_memoria_py_v410.py e a folga do MEMORY.md (se o p00 os disser pendentes), p00 final, revisao de terceiro (Sonnet, D69), fechar_preparacao_v410.py; depois o orquestrador pos_treino_v410 (instalar, rito, pos-rito, HANDOFF)",
         "onde": HERE, "artefatos": [PR, REL, PLANO, os.path.join(HERE, "PRECONDICOES_v410.json"), os.path.join(HERE, "CANDIDATO_v410.json")], "refs": ["cadeia.preparacao_v409", "um_py.v410_preparacao_aberta_06nov", "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov", "kernel.a_escala_tres_faces_v410_09nov"],   # (parte 2) a ORDEM ao Kimi (o H0DN e o recibo HMS/13) e a candidata AEscala, rotas da gerencia
         "nota": "agente de preparacao claude-construtor-v410; quem constroi nao aprova (revisor: Sonnet, D69)" + ("; REFEITA: este PRONTA (%s) substitui o(s) anterior(es) %s" % (S, ", ".join(_ANT)) if _ANT else "")},
        {"tipo": "ANOTACAO", "rota_id": "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov", "estatuto": "REAL", "olhou_dados": False,   # (parte 2, D80) a anotacao na rota da ORDEM ao Kimi: o recibo documental entrou na PREPARACAO; o pos-rito anota o selo
         "titulo": "o recibo documental HMS/13 (D80) entrou na preparacao da v410: candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]),
         "resultado": "o registro h0dn_fontes_hms13_v410, ADITIVO e POSTERIOR ao FREEZE_R2, embute por sha256 quatro artefatos documentais da revisao independente (18 fontes primarias dos 13 calibradores): cobertura documental de fontes, não covariância física fechada; nada aberto. O teste H0DN x BG1 segue pré-registrado; nenhum dado observado lido; em rito nada da pasta da entrega e' aberto (a excecao D80 vale so' para os seis artefatos documentais, por sha256, lidos no build). A preparacao NAO e' o selo: nada instalado, o rito nao rodou.",
         "proximo_passo": "G3/G4 seguem abertos (a covariancia fisica conjunta, a decomposicao completa dentro de cada SN, a matriz completa entre os 13, a revisao fisica independente); o pos-rito da v410 anota o selo nesta mesma rota",
         "refs": ["cadeia.preparacao_v410", "kernel.a_escala_tres_faces_v410_09nov"]}]
ja = os.path.join(HERE, "registro_mapa_construtor_v410.json"); tmp = ja + ".tmp"; open(tmp, "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1)); os.replace(tmp, ja)
r1 = subprocess.run([PY, "-B", "-X", "utf8", ROTAS, "registrar", ja, "--quem", "claude-construtor-v410"], capture_output=True, text=True, encoding="utf-8")
print("mapa:", r1.returncode, (r1.stdout + r1.stderr)[-300:].replace("\n", " "))
assert r1.returncode == 0, r1.stdout + r1.stderr
open(MARCA, "w", encoding="utf-8").write(S + "\n")
print("depositado e registrado:", S)
