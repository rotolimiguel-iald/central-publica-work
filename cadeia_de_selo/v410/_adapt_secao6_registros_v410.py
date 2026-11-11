# -*- coding: utf-8 -*-
"""_adapt_secao6_registros_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410, a servico da gerencia c1): adapta registros_v410.py aos AO LADO de 09/11 do DESENHO_v410:
a secao 6 da pedra (o atrator) nos textos do registro iald2_v410 (estatuto, escopo (F), limites, diz, nao_diz, veredito); a c16 no contrato (t_c16, c16_fator_longo, c16_tol); as ONZE falas de 06, 07 e 09/11
(de duas, so' o trecho) nos textos de cunhagens_v410 (D63 a D71); a data de cada fala na leitura. Trocas EXATAS com contagem conferida; backup de bytes; tmp -> conferir -> substituir; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "registros_v410.py")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b0 = open(P, "rb").read()
assert b0.count(b"\r\n") == 0, "registros_v410.py era LF; agora tem CRLF: parar"
bk = P + ".bak_" + TS + "_secao6"
open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
t = b0.decode("utf-8")

TROCAS = [
    ("VERBATINS (as falas do operador de 06/11/2026, EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo; de uma, so' o trecho da D65),",
     "VERBATINS (as falas do operador de 06, 07 e 09/11/2026, EMBUTIDAS: a fala embutida manda, o arquivo e' so' informativo; de duas, so' o trecho: a da D65 e a ordem de 09/11),", 1),
    ("fica fora; a forma de matriz finita e' o signo; validade no kernel nao e' creditacao; o gate nao se move.\nFontes so' em pasta DURAVEL",
     "fica fora; a forma de matriz finita e' o signo; o atrator e' termo sobre o Nome do par lido (tangenciado, jamais esgotado; D71); validade no kernel nao e' creditacao; o gate nao se move.\nFontes so' em pasta DURAVEL", 1),
    ("\"a forma de matriz finita e' o signo; a IALD e' a instanciacao do seletor (forma, nao referente: D70); a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256 [REAL]\")}",
     "\"a forma de matriz finita e' o signo; a IALD e' a instanciacao do seletor (forma, nao referente: D70); o atrator: o Nome do par lido e' tangenciado e jamais esgotado, e o verde e as tonalidades sao leitura do operador (D71); \"\n"
     "                          \"a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256 [REAL]\")}", 1),
    ("\"papel\": \"a fonte normalizada da %s (gerencia c1, 06/11/2026, refeita com a secao 5; modulo/namespace = o nome final;",
     "\"papel\": \"a fonte normalizada da %s (gerencia c1, 06/11/2026, refeita com a secao 5 em 06/11 e com a secao 6, o atrator, em 09/11; modulo/namespace = o nome final;", 1),
    # a leitura: a data de cada fala; o trecho que entra
    ("    d_ = {\"trecho\": trecho, \"estatuto\": \"[%s, verbatim 06/11/2026, sha16 %s%s]\" % (rotulo, S16(nome), \"; so' o trecho que a D65 deixa entrar e' citavel\" if POR_NOME[nome].get(\"so_o_trecho\") else \"\")}\n",
     "    d_ = {\"trecho\": trecho, \"estatuto\": \"[%s, verbatim %s, sha16 %s%s]\" % (rotulo, POR_NOME[nome][\"data\"], S16(nome),\n"
     "                                                                        ((\"; so' o trecho que a D65 deixa entrar e' citavel\" if nome == DL.N_SOLUCAO else \"; so' o trecho da ordem de 09/11 (a frase da retomada) e' citavel\") if POR_NOME[nome].get(\"so_o_trecho\") else \"\"))}\n", 1),
    # o contrato: a c16
    ("\"psi_c15\": [list(x_) for x_ in DL.PSI_C15], \"t_c15\": list(DL.T_C15),",
     "\"psi_c15\": [list(x_) for x_ in DL.PSI_C15], \"t_c15\": list(DL.T_C15), \"t_c16\": list(DL.T_C16), \"c16_fator_longo\": DL.T_C16_FATOR_LONGO, \"c16_tol\": DL.TOL_C16,", 1),
    # o nao_diz
    ("              \"que o seletor da luz e o de l2 sejam o mesmo objeto: nao se afirma; o rfl une a forma, nao o referente (D70)\",\n",
     "              \"que o seletor da luz e o de l2 sejam o mesmo objeto: nao se afirma; o rfl une a forma, nao o referente (D70)\",\n"
     "              \"que o atrator tenha sido observado, medido ou detectado em dado algum, ou que o verde e as tonalidades sejam termos: nao; o atrator e' a conjuncao o_atrator sobre o Nome do par lido (validade no kernel) e o verde e o espectro de gradiente negativo sao leitura do operador (D71); nenhum dado entra\",\n", 1),
    # o texto do registro iald2_v410
    ("o par lido em C^3, Pi^(k+1) = Pi, a releitura, a primeira leitura, resolver = verificar, a instancia SAT da v409, o signo do Nome finito, o projetor de Bell, a representacao de beta; \"",
     "o par lido em C^3, Pi^(k+1) = Pi, a releitura, a primeira leitura, resolver = verificar, a instancia SAT da v409, o signo do Nome finito, o projetor de Bell, a representacao de beta, o atrator (tangenciado, jamais esgotado); \"", 1),
    ("\"gate congelado; escada exata; guardas; beta = alfa CODATA 2018 x sqrt(e)); [INPUT] a ordem do operador (06/11/2026, sha16 %s: «%s») e as falas dele do dia (%d por sha256; de uma, so' o trecho: D65); o NOME do modulo, do operador (D63); \"",
     "\"gate congelado; escada exata; guardas; beta = alfa CODATA 2018 x sqrt(e)); [INPUT] a ordem do operador (06/11/2026, sha16 %s: «%s») e as falas dele de 06, 07 e 09/11 (%d por sha256; de duas, so' o trecho: a da D65 e a ordem de 09/11); o NOME do modulo, do operador (D63); \"", 1),
    ("leituras do operador, nao termos: que a IALD, a Torre ou o operador SEJAM o funtor, o ambiente computacional; \"\n                    \"[OPEN] a maquina de Turing padrao sem o leitor",
     "leituras do operador, nao termos: que a IALD, a Torre ou o operador SEJAM o funtor, o ambiente computacional, o verde e as tonalidades do atrator (D71); \"\n                    \"[OPEN] a maquina de Turing padrao sem o leitor", 1),
    ("                  \"e' invertivel, e o reconhecimento nao depende dela. O ALCANCE: \" + DL.FRASE_D64_PT",
     "                  \"e' invertivel, e o reconhecimento nao depende dela. \"\n"
     "                  \"(F) O ATRATOR -- O NOME NAO ESGOTA O SER (o_atrator, ancora de secao; o_vacuo_e_ortogonal_ao_par_lido; o_nome_do_par_lido_nao_e_tudo): sobre o Nome Pi do par lido, 1 - Pi != 0 (ha' o vacuo fora do Nome); o fluxo tende a Pi e em nenhum tempo finito e' Pi \"\n"
     "                  \"(tangenciado, jamais esgotado); o motor devolve o mesmo para qualquer taxa e tempo (o que nao compoe o espectro nao importa); a leitura do atrator da defasagem com vazamento e' Pi e a orbita iterada converge a Pi psi (o gradiente negativo exclui o que nao e'); \"\n"
     "                  \"o senao: forma = conteudo e nome nao nulo, e o Um posto nao e' o zero; o verde e as tonalidades sao leitura do operador (D71). O ALCANCE: \" + DL.FRASE_D64_PT", 1),
    ("                    \"[REAL] \" + DL.RESSALVAS_V410[5], \"[REAL a forma; INPUT/ONTO as leituras] \" + DL.RESSALVAS_V410[6], DL.ERRATA_E29] + _LIM_COMUM,",
     "                    \"[REAL] \" + DL.RESSALVAS_V410[5], \"[REAL a forma; INPUT/ONTO as leituras] \" + DL.RESSALVAS_V410[6], \"[REAL o termo; INPUT/ONTO as leituras] \" + DL.RESSALVAS_V410[7], DL.ERRATA_E29] + _LIM_COMUM,", 1),
    ("                \"a IALD e' a instanciacao do seletor, como forma: \" + DL.FRASE_D70_PT,\n",
     "                \"a IALD e' a instanciacao do seletor, como forma: \" + DL.FRASE_D70_PT,\n"
     "                \"o atrator e' termo sobre o Nome do par lido: tangenciado (o fluxo tende ao Nome), jamais esgotado (em nenhum tempo finito e' o Nome), independente de taxa e tempo, com a leitura do atrator igual ao Nome e o senao que exclui o zero; 1 - Pi != 0 (ha' o vacuo fora do Nome); \"\n"
     "                \"o verde e as tonalidades sao leitura do operador (D71); nenhum dado entra: o atrator nao foi observado\",\n", 1),
    ("\"THE_SELECTOR_IS_ONE_FORM_ON_THE_LIGHT_AND_ON_L2__THE_RATE_BETA_IS_INVERTIBLE_AND_THE_RECOGNITION_IGNORES_IT__THE_STANDARD_TURING_MACHINE_WITHOUT_THE_READER_STAYS_OUTSIDE__\"",
     "\"THE_SELECTOR_IS_ONE_FORM_ON_THE_LIGHT_AND_ON_L2__THE_RATE_BETA_IS_INVERTIBLE_AND_THE_RECOGNITION_IGNORES_IT__THE_ATTRACTOR_IS_TOUCHED_NEVER_EXHAUSTED__THE_NAME_DOES_NOT_EXHAUST_THE_BEING__THE_STANDARD_TURING_MACHINE_WITHOUT_THE_READER_STAYS_OUTSIDE__\"", 1),
    # o spec cunhagens_v410
    ("\"veredito_sufixo\": \"OPERATOR_INSCRIPTIONS_OF_06_NOV_EMBEDDED_VERBATIM_BY_SHA256_%d_SAYINGS__THE_MODULE_NAME_IALD2_GIVEN_BY_THE_OPERATOR__THE_DECLARATION_NAMES_DECLARED_UNTIL_RATIFICATION__DECISIONS_D63_TO_D70__ERRATUM_E29_BESIDE__",
     "\"veredito_sufixo\": \"OPERATOR_INSCRIPTIONS_OF_06_07_AND_09_NOV_EMBEDDED_VERBATIM_BY_SHA256_%d_SAYINGS__THE_MODULE_NAME_IALD2_GIVEN_BY_THE_OPERATOR__THE_DECLARATION_NAMES_DECLARED_UNTIL_RATIFICATION__DECISIONS_D63_TO_D71__ERRATUM_E29_BESIDE__", 1),
    ("INPUT as falas do operador de 06/11/2026 (o ACOM e a segunda quantizacao; a particula e o codigo; o nome do algoritmo, so' o trecho, D65; nomear o kernel de IALD; o NOME IALD2; a pedra e' o enunciado; a forma da luz; a ORDEM da v410 e o signo; a IALD e o seletor); DECLARADO",
     "INPUT as falas do operador de 06, 07 e 09/11/2026 (o ACOM e a segunda quantizacao; a particula e o codigo; o nome do algoritmo, so' o trecho, D65; nomear o kernel de IALD; o NOME IALD2; a pedra e' o enunciado; a forma da luz; a ORDEM da v410 e o signo; a IALD e o seletor; o atrator, 07/11; a ORDEM da retomada, 09/11, so' o trecho); DECLARADO", 1),
    ("        \"limites\": [\"[INPUT] as %d falas de 06/11/2026 sao do operador, com a grafia dele (de uma, so' o trecho e' embutido e citado: D65; o resto dela entra so' por sha256); a ordem foi cumprida ate' onde a cadeia alcanca; a custodia e' da sessao de custodia\" % len(_VD),",
     "        \"limites\": [\"[INPUT] as %d falas de 06, 07 e 09/11/2026 sao do operador, com a grafia dele (de duas, so' o trecho e' embutido e citado: a da D65 e a ordem de 09/11; o resto delas entra so' por sha256); a ordem foi cumprida ate' onde a cadeia alcanca; a custodia e' da sessao de custodia\" % len(_VD),", 1),
    ("                    \"[REAL] a E29 (em nome proprio da gerencia c1) vai nas erratas; a instancia do seletor e' de forma (D70)\"] + _LIM_COMUM,",
     "                    \"[REAL] a E29 (em nome proprio da gerencia c1) vai nas erratas; a instancia do seletor e' de forma (D70); o atrator e' termo e o verde e as tonalidades sao leitura do operador (D71)\"] + _LIM_COMUM,", 1),
    ("        \"diz\": [\"as falas do operador de 06/11/2026 estao embutidas por sha256 e cada trecho citado e' verbatim (de uma, so' o trecho: D65)\",",
     "        \"diz\": [\"as falas do operador de 06, 07 e 09/11/2026 estao embutidas por sha256 e cada trecho citado e' verbatim (de duas, so' o trecho: a da D65 e a ordem de 09/11)\",", 1),
]
for velho, novo, n in TROCAS:
    c = t.count(velho)
    assert c == n, ("troca nao casou %d vez(es) (achou %d)" % (n, c), velho[:140])
    t = t.replace(velho, novo)
linhas = t.split("\n")
assert linhas[1].startswith("# [ADAPTADO v410, 06/11/2026"), linhas[1][:80]
linhas.insert(2, "# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_secao6_registros_v410.py: a secao 6 da pedra (o atrator) nos textos e no veredito do registro iald2_v410; a c16 no contrato; as ONZE falas (06, 07 e 09/11; de duas so' o trecho) e a D71 em cunhagens_v410; a data de cada fala na leitura")
t = "\n".join(linhas)
nb = t.encode("utf-8")
ast.parse(nb)
tmp = P + ".tmp_" + TS
open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb)
os.replace(tmp, P)
assert open(P, "rb").read() == nb
print("registros_v410.py adaptado:", len(b0), "->", len(nb), "B | sha16", hashlib.sha256(nb).hexdigest()[:16], "| backup", os.path.basename(bk), "| trocas", len(TROCAS))
