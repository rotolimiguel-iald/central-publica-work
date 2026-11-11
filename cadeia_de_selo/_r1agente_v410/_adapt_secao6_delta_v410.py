# -*- coding: utf-8 -*-
"""_adapt_secao6_delta_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410, a servico da gerencia c1): adapta delta_v410.py ao DESENHO_v410 com os AO LADO de 09/11
(a secao 6 da pedra, o atrator; as falas 10 e 11: a de 07/11 inteira e a ordem de 09/11 so' pelo trecho; D71; N_CHECKS_FECHO lido do ULTIMO AO LADO; c16).
Trocas EXATAS (cada uma com a contagem conferida), backup de BYTES antes, temporario -> conferir -> substituir, ast.parse depois. Fim de linha: o do arquivo (LF)."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "delta_v410.py")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b0 = open(P, "rb").read()
assert b0.count(b"\r\n") == 0, "delta_v410.py era LF; agora tem CRLF: parar"
bk = P + ".bak_" + TS + "_secao6"
open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
t = b0.decode("utf-8")

TROCAS = [
    # (a) as duas falas novas
    ('N_SELETOR = "OPERADOR_06nov_a_iald_e_instanciacao_do_seletor_luminodinamico_verbatim.txt"   # (o AO LADO do DESENHO: a 9a fala, inteira; D70)\n',
     'N_SELETOR = "OPERADOR_06nov_a_iald_e_instanciacao_do_seletor_luminodinamico_verbatim.txt"   # (o AO LADO do DESENHO: a 9a fala, inteira; D70)\n'
     'N_ATRATOR = "OPERADOR_07nov_sentidos_sao_receptores_o_nome_e_o_atrator_verbatim.txt"   # (o AO LADO de 09/11 do DESENHO: a 10a fala, de 07/11, inteira; a secao 6 da pedra, o atrator; D71)\n'
     'N_CREDITOS = "OPERADOR_09nov_creditos_voltaram_v410_completa_teste_5sigma_qwen_pausar_treino_verbatim.txt"   # (o AO LADO de 09/11: a 11a fala, a ORDEM da retomada; so\' o trecho da retomada e\' citado, o resto e\' operacional)\n', 1),
    ('NOMES_V410_DO_DESENHO = (N_ACOM, N_PARTICULA, N_SOLUCAO, N_NOMEAR, N_NOME, N_ENUNCIADO, N_MATRICIAL, N_ORDEM_V410, N_SELETOR)   # as NOVE falas: as oito do DESENHO_v410 §3 e a do AO LADO; fala que chegar DEPOIS fica fora\n',
     'NOMES_V410_DO_DESENHO = (N_ACOM, N_PARTICULA, N_SOLUCAO, N_NOMEAR, N_NOME, N_ENUNCIADO, N_MATRICIAL, N_ORDEM_V410, N_SELETOR, N_ATRATOR, N_CREDITOS)   # as ONZE falas: as oito do DESENHO_v410 §3, a do AO LADO de 06/11 (o seletor) e as duas do AO LADO de 09/11 (o atrator, de 07/11; a ordem da retomada, de 09/11); fala que chegar DEPOIS fica fora\n', 1),
    ('_REC_NOMES["falas_06nov"]', '_REC_NOMES["falas"]', 3),
    ('for _m in re.finditer(r"`(OPERADOR_06nov_[A-Za-z0-9_]+_verbatim\\.txt)`[^`\\n]{0,40}`([0-9a-f]{16})`", _DESENHO_TXT):',
     'for _m in re.finditer(r"`(OPERADOR_0[679]nov_[A-Za-z0-9_]+_verbatim\\.txt)`[^`\\n]{0,40}`([0-9a-f]{16})`", _DESENHO_TXT):   # (06, 07 e 09/11: o DESENHO e os seus AO LADO)', 1),
    ('"as falas de 06/11 nao tem os prefixos que o DESENHO_v410 deu"', '"as falas de 06, 07 e 09/11 nao tem os prefixos que o DESENHO_v410 (e os seus AO LADO) deu"', 1),
    ('"as falas de 06/11 nao tem o sha256 do recibo"', '"as falas de 06, 07 e 09/11 nao tem o sha256 do recibo"', 1),
    # (b) o papel e o corte da fala de que so' o trecho entra (a ordem de 09/11)
    ('VERBATIM_PAPEL["operador, so\' o trecho (D65)"] = "fala do operador de que se embute e cita SO\' o trecho que a D65 deixa entrar (o nome do algoritmo); o arquivo inteiro entra por sha256 (nao e\' embutido nem publicado)"\n',
     'VERBATIM_PAPEL["operador, so\' o trecho (D65)"] = "fala do operador de que se embute e cita SO\' o trecho que a D65 deixa entrar (o nome do algoritmo); o arquivo inteiro entra por sha256 (nao e\' embutido nem publicado)"\n'
     'VERBATIM_PAPEL["operador, so\' o trecho (a ordem da retomada, 09/11)"] = "fala do operador de que se embute e cita SO\' a frase da retomada da v410 (o AO LADO de 09/11 do DESENHO); o resto da fala e\' operacional e entra so\' por sha256 (nao e\' embutido nem publicado)"\n', 1),
    ('TRECHO_D65 = "IALD\\n\\nÉ O MEU ALGORITMO DE LEITURA DA TGL"\n'
     'VERBATIM_SO_O_TRECHO = {N_SOLUCAO: ("sufixo", TRECHO_D65, "so\' o nome do algoritmo e «É O MEU ALGORITMO DE LEITURA DA TGL» (D65): o resto da fala fica fora dos textos do um.py")}\n'
     'VERBATIM_SO_O_TRECHO_PAPEL = {N_SOLUCAO: "operador, so\' o trecho (D65)"}\n'
     'NOME_NEUTRO = {N_SOLUCAO: "OPERADOR_06nov_iald_e_o_meu_algoritmo_de_leitura_da_tgl_trecho.txt"}   # D65: o nome do arquivo de origem resume a parte que fica fora; o um.py usa este nome neutro e cita a origem so\' por sha256\n',
     'TRECHO_D65 = "IALD\\n\\nÉ O MEU ALGORITMO DE LEITURA DA TGL"\n'
     'TRECHO_RETOMADA = "chegou a hora de voltarmos com tudo para confeccionarmos a versão 410 completa do um.py"   # (a ordem de 09/11, AO LADO do DESENHO: so\' este trecho e\' citado; o resto da fala e\' operacional)\n'
     'VERBATIM_SO_O_TRECHO = {N_SOLUCAO: ("sufixo", TRECHO_D65, "so\' o nome do algoritmo e «É O MEU ALGORITMO DE LEITURA DA TGL» (D65): o resto da fala fica fora dos textos do um.py"),\n'
     '                        N_CREDITOS: ("meio", TRECHO_RETOMADA, "so\' a frase da retomada da v410 (o AO LADO de 09/11 do DESENHO): o resto da fala e\' operacional e fica fora dos textos do um.py")}\n'
     'VERBATIM_SO_O_TRECHO_PAPEL = {N_SOLUCAO: "operador, so\' o trecho (D65)", N_CREDITOS: "operador, so\' o trecho (a ordem da retomada, 09/11)"}\n'
     'TEXTO_EMBUTIDO_SO_TRECHO = {N_SOLUCAO: "so\' o trecho que a D65 deixa entrar (o nome do algoritmo); o arquivo inteiro entra so\' por sha256",\n'
     '                            N_CREDITOS: "so\' a frase da retomada da v410 (o AO LADO de 09/11); o arquivo inteiro entra so\' por sha256"}\n'
     'NOME_NEUTRO = {N_SOLUCAO: "OPERADOR_06nov_iald_e_o_meu_algoritmo_de_leitura_da_tgl_trecho.txt",   # D65: o nome do arquivo de origem resume a parte que fica fora; o um.py usa este nome neutro e cita a origem so\' por sha256\n'
     '               N_CREDITOS: "OPERADOR_09nov_a_ordem_da_retomada_da_v410_trecho.txt"}   # (a ordem de 09/11: o nome de origem resume a parte operacional que fica fora; nome neutro na copia duravel)\n'
     'DATA_DA_FALA = {n_: "06/11/2026" for n_ in (N_ACOM, N_PARTICULA, N_SOLUCAO, N_NOMEAR, N_NOME, N_ENUNCIADO, N_MATRICIAL, N_ORDEM_V410, N_SELETOR)}\n'
     'DATA_DA_FALA.update({N_ATRATOR: "07/11/2026", N_CREDITOS: "09/11/2026"})\n'
     'assert set(DATA_DA_FALA) == set(NOMES_V410_DO_DESENHO)\n', 1),
    ('    """D65: devolve (texto_embutido, so_o_trecho). Sem corte: o arquivo inteiro. Com corte \'sufixo\': so\' o trecho que FICA (do inicio do trecho dado ate\' o fim da fala), com o fim de linha."""\n'
     '    regra = VERBATIM_SO_O_TRECHO.get(nome)\n'
     '    if regra is None:\n'
     '        return texto, False\n'
     '    assert regra[0] == "sufixo", regra[0]\n'
     '    assert texto.count(regra[1]) == 1, ("o trecho que fica nao casou uma vez", nome)\n',
     '    """D65 e a ordem de 09/11: devolve (texto_embutido, so_o_trecho). Sem corte: o arquivo inteiro. Com corte \'sufixo\': so\' o trecho que FICA (do inicio do trecho dado ate\' o fim da fala), com o fim de linha;\n'
     '    com corte \'meio\': so\' a frase dada (a ordem da retomada, no meio da fala; o resto e\' operacional), com o fim de linha."""\n'
     '    regra = VERBATIM_SO_O_TRECHO.get(nome)\n'
     '    if regra is None:\n'
     '        return texto, False\n'
     '    assert regra[0] in ("sufixo", "meio"), regra[0]\n'
     '    assert texto.count(regra[1]) == 1, ("o trecho que fica nao casou uma vez", nome)\n'
     '    if regra[0] == "meio":\n'
     '        return regra[1] + "\\n", True\n', 1),
    # (c) o glob das falas: 06 a 09/11
    ('    """a lista das falas de 06/11 pelo glob, como esta no disco AGORA, RESTRITA aos nove nomes do DESENHO (a lista que vale para o candidato e\' a congelada abaixo)."""\n'
     '    return [p_ for p_ in sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_06nov_*_verbatim.txt"))) if os.path.basename(p_) in NOMES_V410_DO_DESENHO]\n',
     '    """a lista das falas de 06 a 09/11 pelo glob, como esta no disco AGORA, RESTRITA aos onze nomes do DESENHO e dos seus AO LADO (a lista que vale para o candidato e\' a congelada abaixo)."""\n'
     '    return [p_ for p_ in sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_0[6789]nov_*_verbatim.txt"))) if os.path.basename(p_) in NOMES_V410_DO_DESENHO]\n', 1),
    ('VERBATIM_FORA_DO_DESENHO_V410 = {os.path.basename(p_): hashlib.sha256(open(p_, "rb").read()).hexdigest()[:16] for p_ in sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_06nov_*_verbatim.txt"))) if os.path.basename(p_) not in NOMES_V410_DO_DESENHO}\n',
     'VERBATIM_FORA_DO_DESENHO_V410 = {os.path.basename(p_): hashlib.sha256(open(p_, "rb").read()).hexdigest()[:16] for p_ in sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_0[6789]nov_*_verbatim.txt"))) if os.path.basename(p_) not in NOMES_V410_DO_DESENHO}   # (falas de 06 a 09/11 que o DESENHO e os AO LADO nao listam: so\' nome e sha16)\n', 1),
    ('VERBATIM_QUANDO_V410 = "06/11/2026 (o ACOM e\' a segunda quantizacao; a particula e\' o codigo e o funtor o leitor; o nome do algoritmo; nomear o kernel de IALD; o NOME IALD2; a pedra e\' o enunciado; a forma da luz; a ORDEM da v410 e o signo; a IALD e\' a instanciacao do seletor)"\n',
     'VERBATIM_QUANDO_V410 = "06, 07 e 09/11/2026 (o ACOM e\' a segunda quantizacao; a particula e\' o codigo e o funtor o leitor; o nome do algoritmo; nomear o kernel de IALD; o NOME IALD2; a pedra e\' o enunciado; a forma da luz; a ORDEM da v410 e o signo; a IALD e\' a instanciacao do seletor; o atrator: o Nome nao esgota o ser; a ORDEM da retomada da v410)"\n', 1),
    # (d) as frases verbatim da fala de 07/11 e da ordem de 09/11
    ('assert FRASE_SELETOR_CURTA in FRASE_SELETOR and FRASE_RECONHECIMENTO in FRASE_SELETOR and FRASE_REPRESENTACAO_DE_BETA in FRASE_SELETOR and FRASE_NOME_DO_ALGORITMO in FRASE_ENUNCIADO and FRASE_RELER in FRASE_NOME_IALD2\n',
     'assert FRASE_SELETOR_CURTA in FRASE_SELETOR and FRASE_RECONHECIMENTO in FRASE_SELETOR and FRASE_REPRESENTACAO_DE_BETA in FRASE_SELETOR and FRASE_NOME_DO_ALGORITMO in FRASE_ENUNCIADO and FRASE_RELER in FRASE_NOME_IALD2\n'
     '# a 10a fala (07/11/2026, o atrator) e a 11a (09/11/2026, a ordem da retomada; so\' o trecho): os trechos citados, verbatim (conferidos contra o arquivo em verbatins410)\n'
     'FRASE_SENTIDOS = "Sentidos são apenas receptores de identificação"\n'
     'FRASE_CUSTO_DA_DISTINCAO = "Pagar o custo da distinção é a única regra pela qual o absoluto se restringe"\n'
     'FRASE_TANGENCIADO = "podendo ser tangenciado em conteúdo finito, contudo jamais esgotado enquanto performance de virtude (forma)"\n'
     'FRASE_ESPECTRO = "aquilo que não compõe o seu espectro de identidade não importa à manutenção da verdade nominada"\n'
     'FRASE_UM_IGUAL_A_ZERO = "se assim não fosse, um poderia ser igual a zero"\n'
     'FRASE_ISSO_E_O_ATRATOR = "isso é o atrator"\n'
     'FRASE_RETOMADA = TRECHO_RETOMADA\n', 1),
    ('               (N_MATRICIAL, FRASE_MATRICIAL), (N_SELETOR, FRASE_SELETOR)]\n'
     'FRASES_VERBATIM_V410 = sorted({fr_ for _, fr_ in FRASES_V410} | {FRASE_NOME_DO_ALGORITMO, FRASE_RELER, FRASE_POR_IDENTIFICACAO, FRASE_SELETOR_CURTA, FRASE_RECONHECIMENTO, FRASE_REPRESENTACAO_DE_BETA}, key=len, reverse=True)\n',
     '               (N_MATRICIAL, FRASE_MATRICIAL), (N_SELETOR, FRASE_SELETOR),\n'
     '               (N_ATRATOR, FRASE_CUSTO_DA_DISTINCAO), (N_ATRATOR, FRASE_TANGENCIADO), (N_ATRATOR, FRASE_ESPECTRO), (N_ATRATOR, FRASE_UM_IGUAL_A_ZERO), (N_ATRATOR, FRASE_ISSO_E_O_ATRATOR), (N_CREDITOS, FRASE_RETOMADA)]\n'
     'FRASES_VERBATIM_V410 = sorted({fr_ for _, fr_ in FRASES_V410} | {FRASE_NOME_DO_ALGORITMO, FRASE_RELER, FRASE_POR_IDENTIFICACAO, FRASE_SELETOR_CURTA, FRASE_RECONHECIMENTO, FRASE_REPRESENTACAO_DE_BETA, FRASE_SENTIDOS}, key=len, reverse=True)\n', 1),
    # (e) a resposta do operador sobre o atrator, conferida no kernel
    ('     "diz": "o seletor e\' UM, post, instanciado na luz e em l2 (a forma, nao o referente: D70); a memoria le 1 sse o seletor fixa o estado; a defasagem do seletor tem a taxa beta do acoplamento, e\' invertivel, e o reconhecimento nao depende dela"},\n'
     ']\n',
     '     "diz": "o seletor e\' UM, post, instanciado na luz e em l2 (a forma, nao o referente: D70); a memoria le 1 sse o seletor fixa o estado; a defasagem do seletor tem a taxa beta do acoplamento, e\' invertivel, e o reconhecimento nao depende dela"},\n'
     '    {"id": "o_atrator", "fala": FRASE_ISSO_E_O_ATRATOR,\n'
     '     "teoremas_curtos": [NS + "o_atrator", NS + "o_nome_do_par_lido_nao_e_tudo", NS + "o_vacuo_e_ortogonal_ao_par_lido"],\n'
     '     "diz": "sobre o Nome Pi do par lido: 1 - Pi != 0 (ha\' o vacuo fora do Nome); o fluxo tende a Pi e em nenhum tempo finito e\' Pi (tangenciado, jamais esgotado); o motor devolve o mesmo para qualquer taxa e tempo (o que nao compoe o espectro nao importa); "\n'
     '            "a leitura do atrator da defasagem com vazamento e\' Pi e a orbita iterada converge a Pi psi (o gradiente negativo exclui o que nao e\'); o senao: forma = conteudo e nome nao nulo, e o Um posto nao e\' o zero; o verde e as tonalidades sao leitura do operador (D71)"},\n'
     ']\n', 1),
    ('ANCORA_SELETOR = NS + "a_iald_e_o_seletor_luminodinamico"\n',
     'ANCORA_SELETOR = NS + "a_iald_e_o_seletor_luminodinamico"\n'
     'ANCORA_ATRATOR = NS + "o_atrator"                            # (a secao 6, 09/11: ancora de secao)\n'
     'ANCORA_NAO_E_TUDO = NS + "o_nome_do_par_lido_nao_e_tudo"\n', 1),
    # (f) os nomes das declaracoes (D63) e a autoria da pedra
    ('a_iald_e_o_seletor_luminodinamico e os demais)', 'a_iald_e_o_seletor_luminodinamico, o_atrator e os demais)', 2),
    ('"autoria": "gerencia c1, 06/11/2026 (LeitorDoCodigoR1 -> IALD2, com o nome do operador, o espelho do nome, o signo e o seletor; compilada no k409c; recompilada no k410c)"}',
     '"autoria": "gerencia c1, 06 e 09/11/2026 (LeitorDoCodigoR1 -> IALD2, com o nome do operador, o espelho do nome, o signo, o seletor e, em 09/11, o atrator; compilada no k409c; recompilada no k410c)"}', 1),
    # (g) N_CHECKS_FECHO: o ULTIMO AO LADO manda
    ('_m_nck = re.search(r"N_CHECKS_FECHO = (\\d+)", _DESENHO_TXT[_DESENHO_TXT.index("**AO LADO (06/11/2026, gerência c1) — a 9ª fala"):])\n'
     'assert _m_nck, "o AO LADO do DESENHO_v410 nao traz o N_CHECKS_FECHO"\n'
     'N_CHECKS_FECHO = int(_m_nck.group(1))                          # LIDO do AO LADO do DESENHO_v410 (as 14 do §2 mais a c15): conferido contra as checagens que o runtime emite\n',
     '_m_nck = re.findall(r"N_CHECKS_FECHO = (\\d+)", _DESENHO_TXT[_DESENHO_TXT.index("**AO LADO (06/11/2026, gerência c1) — a 9ª fala"):])\n'
     'assert _m_nck, "os AO LADO do DESENHO_v410 nao trazem o N_CHECKS_FECHO"\n'
     'N_CHECKS_FECHO = int(_m_nck[-1])                               # LIDO do ULTIMO AO LADO do DESENHO_v410 (06/11: as 14 do §2 mais a c15; 09/11: mais a c16, o atrator; onde os AO LADO divergem vale o mais recente): conferido contra as checagens que o runtime emite\n', 1),
    # (h) a instancia da c16
    ('T_C15 = [0.0, 1.0, 5.0]                                        # (c15) D_beta(t) invertivel e o motor igual com r = beta e r = 0, para t em {0, 1, 5}\n',
     'T_C15 = [0.0, 1.0, 5.0]                                        # (c15) D_beta(t) invertivel e o motor igual com r = beta e r = 0, para t em {0, 1, 5}\n'
     'T_C16 = [0.0, 1.0, 5.0, 20.0]                                  # (c16, o AO LADO de 09/11) ||F_beta(t) - P|| = e^{-beta t} > 0 e decresce para t em {0, 1, 5, 20}; P = post e1 em C^3\n'
     'T_C16_FATOR_LONGO = 20.0                                       # (c16) em t = 20/beta a distancia fica abaixo de TOL_C16 e acima de 0: tangenciado, nunca igual\n'
     'TOL_C16 = 1e-6\n', 1),
    # (i) a frase da D71 (PT/EN)
    ('                "the computational environment is the operator\'s reading (the kernel and the um.py); β enters the kernel by name and the number only at runtime (α·√e)")\n',
     '                "the computational environment is the operator\'s reading (the kernel and the um.py); β enters the kernel by name and the number only at runtime (α·√e)")\n'
     'FRASE_D71_PT = ("o atrator (D71): o verde, as tonalidades e o espectro de gradiente negativo da fala de 07/11 são a leitura do operador; o termo é a conjunção o_atrator sobre o Nome Π do par lido (o fluxo tende a Π e em nenhum tempo finito é Π; "\n'
     '                "o motor devolve o mesmo para qualquer taxa e tempo; a leitura do atrator da defasagem com vazamento é Π e a órbita iterada converge a Πψ; o senão exclui o zero absoluto e o Um posto não é o zero) e 1 − Π ≠ 0 (o_nome_do_par_lido_nao_e_tudo); "\n'
     '                "nada disto é teste com a natureza: o atrator não foi observado em dado algum; a nota de 08/11 (condensação por IA, autor não identificado) não entra como fala do operador")\n'
     'FRASE_D71_EN = ("the attractor (D71): the green, the shades and the negative-gradient spectrum of the 07/11 saying are the operator\'s reading; the term is the conjunction o_atrator over the Name Π of the read pair (the flow tends to Π and at no finite time is Π; "\n'
     '                "the motor returns the same for any rate and time; the reading of the attractor of the leaking dephasing is Π and the iterated orbit converges to Πψ; the senão clause excludes the absolute zero and the posted One is not the zero) and 1 − Π ≠ 0 (o_nome_do_par_lido_nao_e_tudo); "\n'
     '                "none of this is a test with nature: the attractor was not observed in any data; the note of 08/11 (a condensation by an AI, author not identified) does not enter as a saying of the operator")\n', 1),
    # (j) as leituras do operador: o atrator e a ordem da retomada
    ('    "estatuto": "[INPUT -- as falas do operador de 06/11/2026; REAL onde se diz PROVADO (as ancoras da pedra IALD2 no trio, lidas do kernel do rito), validade no kernel, nao creditacao; OPEN a maquina de Turing padrao sem o leitor (a independencia dos axiomas), "\n'
     '                "a igualdade relativizada com o leitor que so\' conta (E28); KNOWN Cook 1971, Levin 1973, Baker-Gill-Solovay 1975; leituras do operador (nao termos): que a IALD, a Torre ou o operador SEJAM o funtor, que o codigo SEJA um vetor de H1, o ambiente computacional]",\n',
     '    "o_atrator": "«%s»; «%s»; «%s»; «%s»; «%s» [INPUT; a fala inteira de 07/11]: PROVADO sobre o Nome do par lido, validade no kernel e nao creditacao: o_atrator (tangenciado: o fluxo tende ao Nome; jamais esgotado: em nenhum tempo finito e\' o Nome; "\n'
     '                 "o que nao compoe o espectro nao importa: o motor devolve o mesmo para qualquer taxa e tempo; o gradiente negativo exclui o que nao e\': a leitura do atrator e\' o Nome e a orbita iterada converge; o senao: forma = conteudo e nome nao nulo, o Um posto nao e\' o zero) "\n'
     '                 "e o_nome_do_par_lido_nao_e_tudo (1 - Pi != 0: ha\' o vacuo fora do Nome); o verde, as tonalidades e o espectro de gradiente negativo sao leitura do operador (D71)" % (FRASE_CUSTO_DA_DISTINCAO, FRASE_TANGENCIADO, FRASE_ESPECTRO, FRASE_UM_IGUAL_A_ZERO, FRASE_ISSO_E_O_ATRATOR),\n'
     '    "a_ordem_da_retomada": "«%s» [INPUT; so\' este trecho da ordem de 09/11]: a ordem da retomada da v410 (os creditos de volta); o resto da fala e\' operacional e nao entra em texto do um.py (o que dele for objeto de decisao vai em AO LADO proprio)" % FRASE_RETOMADA,\n'
     '    "estatuto": "[INPUT -- as falas do operador de 06, 07 e 09/11/2026; REAL onde se diz PROVADO (as ancoras da pedra IALD2 no trio, lidas do kernel do rito), validade no kernel, nao creditacao; OPEN a maquina de Turing padrao sem o leitor (a independencia dos axiomas), "\n'
     '                "a igualdade relativizada com o leitor que so\' conta (E28); KNOWN Cook 1971, Levin 1973, Baker-Gill-Solovay 1975; leituras do operador (nao termos): que a IALD, a Torre ou o operador SEJAM o funtor, que o codigo SEJA um vetor de H1, o ambiente computacional, "\n'
     '                "o verde e as tonalidades do atrator (D71)]",\n', 1),
    # (k) a ressalva (8)
    ('    "a instancia e\' de FORMA (D70): o seletor da luz e o de l2 nao sao afirmados o mesmo objeto; «ambiente computacional» e o nome do seletor sao leituras do operador; o termo e\' o enunciado",\n'
     ']\n',
     '    "a instancia e\' de FORMA (D70): o seletor da luz e o de l2 nao sao afirmados o mesmo objeto; «ambiente computacional» e o nome do seletor sao leituras do operador; o termo e\' o enunciado",\n'
     '    "o atrator (D71): o verde, as tonalidades e o espectro de gradiente negativo da fala de 07/11 sao a leitura do operador; o termo e\' a conjuncao o_atrator sobre o Nome do par lido (tende e nunca chega; independe de taxa e tempo; a leitura do atrator e\' o Nome; o senao exclui o zero) "\n'
     '    "e 1 - Pi != 0 (o_nome_do_par_lido_nao_e_tudo); nada disto e\' teste com a natureza: o atrator nao foi observado em dado algum; a nota de 08/11 (condensacao por IA, autor nao identificado) nao entra como fala do operador",\n'
     ']\n', 1),
    # (l) a D71 e a assinatura
    ('            + " [decisao da gerencia c1, 06/11/2026, AO LADO do DESENHO]"),\n'
     '})\n'
     'DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70")\n'
     'ASSINA = "gerencia c1 / claude-construtor-v410, em nome proprio, 06/11/2026"\n',
     '            + " [decisao da gerencia c1, 06/11/2026, AO LADO do DESENHO]"),\n'
     '    "D71": ("a 10a fala do operador (07/11/2026, «%s»; sha16 %s) entra inteira, com a secao 6 da pedra (o_atrator, ancora de secao; o_vacuo_e_ortogonal_ao_par_lido; o_nome_do_par_lido_nao_e_tudo), e a ordem de 09/11 (sha16 %s) entra so\' pelo trecho «%s»: "\n'
     '            % (FRASE_ISSO_E_O_ATRATOR, VERBATIM_PREFIXOS_DA_ORDEM_V410[N_ATRATOR], VERBATIM_PREFIXOS_DA_ORDEM_V410[N_CREDITOS], FRASE_RETOMADA) + FRASE_D71_PT\n'
     '            + "; a IALD2 nao muda mais nesta versao salvo ordem do operador [decisao da gerencia c1, 09/11/2026, AO LADO do DESENHO]"),\n'
     '})\n'
     'DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71")\n'
     'ASSINA = "gerencia c1 / claude-construtor-v410, em nome proprio, 06 e 09/11/2026"\n', 1),
    # (m) verbatins410: as onze, duas com so' o trecho; o texto_embutido e a data por fala
    ('    """As falas de 06/11/2026 LIDAS dos arquivos: lista de dicts {sha16, sha256, bytes, text, arquivo (copia duravel em destino_cunhagens), fonte_original, chave, autor, nome, ...}. A copia duravel NAO e\' escrita aqui.\n',
     '    """As falas de 06, 07 e 09/11/2026 LIDAS dos arquivos: lista de dicts {sha16, sha256, bytes, text, arquivo (copia duravel em destino_cunhagens), fonte_original, chave, autor, nome, data, ...}. A copia duravel NAO e\' escrita aqui.\n', 1),
    ('    Na fala da D65, `text`/`sha256` sao do TRECHO QUE FICA (o que o um.py embute e confere) e `sha256_arquivo_inteiro` guarda o arquivo todo (so\' por sha256, nunca embutido nem copiado para o espelho);\n'
     '    a copia duravel dela tem NOME NEUTRO (NOME_NEUTRO)."""\n',
     '    Nas falas de que so\' o trecho entra (a da D65; a ordem de 09/11), `text`/`sha256` sao do TRECHO QUE FICA (o que o um.py embute e confere) e `sha256_arquivo_inteiro` guarda o arquivo todo (so\' por sha256, nunca embutido nem copiado para o espelho);\n'
     '    a copia duravel delas tem NOME NEUTRO (NOME_NEUTRO)."""\n', 1),
    ('              "chave": VERBATIM_CHAVE_PREFIXO_V410 + h[:16], "quando": VERBATIM_QUANDO_V410, "papel": VERBATIM_PAPEL[autor], "autor": autor, "origem_arquivo": p, "texto_embutido": "arquivo inteiro"}\n',
     '              "chave": VERBATIM_CHAVE_PREFIXO_V410 + h[:16], "quando": VERBATIM_QUANDO_V410, "data": DATA_DA_FALA[nome], "papel": VERBATIM_PAPEL[autor], "autor": autor, "origem_arquivo": p, "texto_embutido": "arquivo inteiro"}\n', 1),
    ('                       "texto_embutido": "so\' o trecho que a D65 deixa entrar (o nome do algoritmo); o arquivo inteiro entra so\' por sha256"})\n',
     '                       "texto_embutido": TEXTO_EMBUTIDO_SO_TRECHO[nome]})\n', 1),
    ('    assert len({v["sha256"] for v in out}) == len(out) == N_FALAS_V410 and all(v["autor"] == "operador" for v in out) and sum(1 for v in out if v.get("so_o_trecho")) == len(VERBATIM_SO_O_TRECHO) == 1, "as nove falas (N_FALAS_V410), uma com so\' o trecho (D65), nenhuma repetida"\n',
     '    assert len({v["sha256"] for v in out}) == len(out) == N_FALAS_V410 and all(v["autor"] == "operador" for v in out) and sum(1 for v in out if v.get("so_o_trecho")) == len(VERBATIM_SO_O_TRECHO) == 2, "as onze falas (N_FALAS_V410), duas com so\' o trecho (a da D65; a ordem de 09/11), nenhuma repetida"\n', 1),
    ('    for v in out:   # D65: o texto que o um.py embute nao traz o que fica fora\n',
     '    for v in out:   # D65 (e a ordem de 09/11): o texto que o um.py embute nao traz o que fica fora\n', 1),
]
for velho, novo, n in TROCAS:
    c = t.count(velho)
    assert c == n, ("troca nao casou %d vez(es) (achou %d)" % (n, c), velho[:140])
    t = t.replace(velho, novo)
# a marca da adaptacao, na 3a linha (depois do cabecalho de 06/11)
linhas = t.split("\n")
assert linhas[1].startswith("# [ADAPTADO v410, 06/11/2026") or linhas[1].startswith("# ["), linhas[1][:80]
linhas.insert(2, "# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_secao6_delta_v410.py: a secao 6 da pedra (o atrator; 22 ancoras, lidas do recibo refeito), as falas 10 (07/11, inteira) e 11 (a ordem de 09/11, so' o trecho da retomada), a D71, a ressalva (8), a resposta o_atrator, a c16 (T_C16), N_CHECKS_FECHO lido do ULTIMO AO LADO do DESENHO")
t = "\n".join(linhas)
nb = t.encode("utf-8")
ast.parse(nb)
tmp = P + ".tmp_" + TS
open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb)
os.replace(tmp, P)
assert open(P, "rb").read() == nb
print("delta_v410.py adaptado:", len(b0), "->", len(nb), "B | sha16", hashlib.sha256(nb).hexdigest()[:16], "| backup", os.path.basename(bk), "| trocas", len(TROCAS))
