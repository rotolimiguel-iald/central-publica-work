# -*- coding: utf-8 -*-
"""_adapt_d86_delta_v410.py -- D86/D87 (parte 2) no delta_v410.py: o bundle passa a DOIS modulos (IALD2 + AEscala); as ancoras da AEscala (38, lidas da fonte) em ANCORAS_AESCALA (as da IALD2 nao mudam); as OITO falas de 09/11 (prefixos LIDOS do DESENHO em tres formas:
`arquivo` ... `sha`, `arquivo` (sha16), sha256 `...` ... arquivo `...`); as frases citadas das falas novas; os nomes da pedra AEscala RATIFICADOS (D87, sha256 lido do arquivo e conferido no DESENHO); as decisoes D83 a D87; a errata E31; o registro a_escala_v410 (constantes,
veredito, as frases canonicas do Clay LIDAS do DESENHO (D83/D84), os numeros por Fraction, as molduras); REGISTROS_FUNCAO com QUATRO; as leituras do operador. Backup de bytes; trocas exatas; ast.parse; import de conferencia (com o congelado das 15 falas movido a backup ANTES)."""
import ast, datetime, hashlib, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
P = os.path.join(HERE, "delta_v410.py"); b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0
bk = P + ".bak_" + TS + "_d86_d87"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
t = b0.decode("utf-8")
assert "AESCALA_REGISTRO" not in t and "HMS13_REGISTRO" in t, "o delta ja' traz a D86, ou nao traz a D80"


def troca(a, b, n=1):
    global t
    c = t.count(a); assert c == n, (c, n, a[:140]); t = t.replace(a, b)


# (1) o bundle de DOIS modulos
troca('assert N_BUNDLE == _BL["n"] == _BD["n"] == len(BUNDLE_POR_REL) == 1 and set(BUNDLE_POR_REL) == set(BUNDLE_RELS), ("o bundle da v410 e\' UM modulo (DESENHO_v410 §1)", N_BUNDLE, _BL["n"], _BD["n"])\nassert BUNDLE_RELS == ["TGLExt/IALD2.lean"], BUNDLE_RELS\n',
      'assert N_BUNDLE == _BL["n"] == _BD["n"] == len(BUNDLE_POR_REL) == 2 and set(BUNDLE_POR_REL) == set(BUNDLE_RELS), ("o bundle da v410 e\' de DOIS modulos (DESENHO_v410 §1: IALD2; D86: AEscala, parte 2)", N_BUNDLE, _BL["n"], _BD["n"])\nassert BUNDLE_RELS == ["TGLExt/IALD2.lean", "TGLExt/AEscala.lean"], BUNDLE_RELS\n')
troca('MODULO_TESTEMUNHA = MODULO_IALD2                               # (alias dos scripts bumpados: o modulo que CARREGA a ancora principal)\nassert MODULO_IALD2 in BUNDLE_POR_REL\n',
      'MODULO_TESTEMUNHA = MODULO_IALD2                               # (alias dos scripts bumpados: o modulo que CARREGA a ancora principal)\nassert MODULO_IALD2 in BUNDLE_POR_REL\n'
      'MODULO_AESCALA = "TGLExt/AEscala.lean"                         # (D86, parte 2) a segunda pedra do bundle: a escala -- tres faces de 1/2, a insignia, o vibrato, o tempo finito, os dois Nomes, a pergunta do Clay no dicionario\n'
      'assert MODULO_AESCALA in BUNDLE_POR_REL and BUNDLE_RELS == [MODULO_IALD2, MODULO_AESCALA]\n'
      'FLAG_PREFIX_AESCALA = "ext_aescala_410_"                        # (D86) a SEGUNDA serie de bandeiras da v410, so\' declaracao NOMEADA publica da AEscala, em ordem de nome; o numero e\' MEDIDO pelo pos_build\n'
      'FLAG_PREFIX_POR_MODULO = {MODULO_IALD2: FLAG_PREFIX, MODULO_AESCALA: FLAG_PREFIX_AESCALA}\n'
      'GRUPO_POR_MODULO = {MODULO_IALD2: GRUPO_BUNDLE, MODULO_AESCALA: "aescala"}\n'
      'ORIGEM_POR_MODULO = {MODULO_IALD2: ORIGEM_DE_BANDEIRA, MODULO_AESCALA: "aescala_nomeada"}\n')
# (2) o recibo dos nomes: o modulo 2
troca('assert BUNDLE_POR_REL[MODULO_IALD2]["sha256_origem"] == _REC_MOD["sha256"], "o bundle nao foi preparado com a fonte que o recibo pina"\n',
      'assert BUNDLE_POR_REL[MODULO_IALD2]["sha256_origem"] == _REC_MOD["sha256"], "o bundle nao foi preparado com a fonte que o recibo pina"\n'
      '_REC_AESC = _REC_NOMES["modulos"][1]                           # (D86/D87) o modulo 2 do recibo: TGLExt.AEscala, nome e 44 nomes RATIFICADOS\n'
      'assert _REC_AESC["modulo"] == "TGLExt.AEscala" and _REC_AESC["print_axioms"] == _REC_AESC["no_trio"] and _REC_AESC["avisos"] == 0 and _REC_AESC["ratificados"] is True and len(_REC_AESC["nomes"]) == _REC_AESC["declaracoes_n"] == 44\n'
      'assert BUNDLE_POR_REL[MODULO_AESCALA]["sha256_origem"] == _REC_AESC["sha256"], "o bundle da AEscala nao foi preparado com a fonte que o recibo pina"\n'
      '_RAT87 = _REC_NOMES["ratificacao_aescala_D87"]; assert _RAT87["pedra_sha256_depois"] == _REC_AESC["sha256"] and _RAT87["n_nomes"] == 44\n')
# (3) as ancoras: as da IALD2 em ANCORAS (como antes); as da AEscala em ANCORAS_AESCALA
troca('ANCORAS = {}\nANCORAS_POR_MODULO = {}\n', 'ANCORAS = {}\nANCORAS_POR_MODULO = {}\nANCORAS_AESCALA = {}                                           # (D86) as 38 ancoras da AEscala (os #print axioms da fonte), separadas das 22 da IALD2: cada registro le as suas\nANCORAS_POR_MODULO_AESCALA = {}\n')
troca('(?:noncomputable\\s+)?(?:theorem|lemma|def)\\s+" + re.escape(curto_)', '(?:noncomputable\\s+)?(?:theorem|lemma|def|structure|abbrev|instance)\\s+" + re.escape(curto_)')
troca('        assert _pap, ("ancora sem docstring e sem papel escrito", _n)\n        ANCORAS[_n] = {"rel": _p["rel"], "papel": _pap if _n in _PAPEIS_ESCRITOS else "[docstring da pedra] " + _pap}\n',
      '        assert _pap or _p["rel"] == MODULO_AESCALA, ("ancora sem docstring e sem papel escrito", _n)\n'
      '        (ANCORAS if _p["rel"] == MODULO_IALD2 else ANCORAS_AESCALA)[_n] = {"rel": _p["rel"], "papel": _pap if _n in _PAPEIS_ESCRITOS else ("[docstring da pedra] " + _pap if _pap else "[sem docstring] " + _n.split(".")[-1])}\n')
troca('    ANCORAS_POR_MODULO[_p["rel"]] = _vistos\n', '    (ANCORAS_POR_MODULO if _p["rel"] == MODULO_IALD2 else ANCORAS_POR_MODULO_AESCALA)[_p["rel"]] = _vistos\n')
troca('assert len(ANCORAS) == sum(len(v) for v in ANCORAS_POR_MODULO.values()) == N_ANCORAS_ESPERADAS, ("as ancoras da v410 sao as do recibo", len(ANCORAS), N_ANCORAS_ESPERADAS)\n',
      'assert len(ANCORAS) == sum(len(v) for v in ANCORAS_POR_MODULO.values()) == N_ANCORAS_ESPERADAS, ("as ancoras da v410 sao as do recibo", len(ANCORAS), N_ANCORAS_ESPERADAS)\n'
      'N_ANCORAS_AESCALA = int(_REC_AESC["print_axioms"])             # LIDO do recibo (38)\n'
      'assert len(ANCORAS_AESCALA) == len(ANCORAS_POR_MODULO_AESCALA[MODULO_AESCALA]) == N_ANCORAS_AESCALA and set(ANCORAS_POR_MODULO_AESCALA[MODULO_AESCALA]) == set(_REC_AESC["ancoras"]), ("as ancoras da AEscala sao as do recibo", len(ANCORAS_AESCALA), N_ANCORAS_AESCALA)\n'
      'NS_AESCALA = "TGLExt.AEscala."\n'
      'ANCORA_PRINCIPAL_AESCALA = _REC_AESC["ancora_principal"]       # a_escala (a conjuncao; lida do recibo)\n'
      'ANCORAS_DE_SECAO_AESCALA = [a_ for a_ in ANCORAS_POR_MODULO_AESCALA[MODULO_AESCALA] if a_.split(".")[-1] in list(_REC_AESC["ancoras_de_secao"])]\n'
      'assert ANCORA_PRINCIPAL_AESCALA == NS_AESCALA + "a_escala" and ANCORA_PRINCIPAL_AESCALA in ANCORAS_AESCALA and len(ANCORAS_DE_SECAO_AESCALA) == len(_REC_AESC["ancoras_de_secao"]) == 6 and ANCORA_PRINCIPAL_AESCALA not in ANCORAS_DE_SECAO_AESCALA\n'
      'ANCORAS_PRINCIPAIS_AESCALA = [ANCORA_PRINCIPAL_AESCALA] + list(ANCORAS_DE_SECAO_AESCALA)\n'
      'NOMES_AESCALA = list(_REC_AESC["nomes"])                        # os 44 nomes (lidos do recibo; RATIFICADOS, D87)\n')
# (4) as OITO falas de 09/11 (parte 2)
troca('NOMES_V410_DO_DESENHO = (N_ACOM, N_PARTICULA, N_SOLUCAO, N_NOMEAR, N_NOME, N_ENUNCIADO, N_MATRICIAL, N_ORDEM_V410, N_SELETOR, N_ATRATOR, N_CREDITOS, N_RATIFICA, N_TRES_COPIAS, N_CINCO_SIGMA, N_SELO)',
      'N_VIBRATO = "OPERADOR_09nov_vibrato_insignia_nome_inalcancavel_e_ratificacao_hms13_verbatim.txt"   # (D80/D82/D86: a 16a fala, inteira: o vibrato, a insignia, o Nome e o inalcancavel; termina com a ratificacao do HMS/13 e o caminho do HANDOFF)\n'
      'N_PESOS = "OPERADOR_09nov_pesos_das_faces_nome_1_inalcancavel_meio_neutrino_verbatim.txt"   # (a 17a: os pesos -- o nome pesa 1; tres faces de 1/2; 1/3 caiu)\n'
      'N_FUNDAMENTAL = "OPERADOR_09nov_pesos_fundamentais_para_P_igual_nP_verbatim.txt"   # (a 18a: fundamental para P=nP)\n'
      'N_AFIRMAMOS = "OPERADOR_09nov_afirmamos_p_igual_np_de_turing_e_o_nome_e_par_objeto_e_lido_verbatim.txt"   # (a 19a, D81: afirmamos P=nP de Turing; o Nome e\' par, objeto e lido)\n'
      'N_ESCALA = "OPERADOR_09nov_a_escala_tres_faces_resolve_clay_tudo_na_v410_duas_partes_rodar_uma_vez_verbatim.txt"   # (a 20a, D82: a escala; tudo na v410; duas partes; rodar uma vez)\n'
      'N_PERGUNTA_CLAY = "OPERADOR_09nov_a_pergunta_do_clay_e_qual_algoritmo_le_a_face_sem_leitura_existe_e_iald_verbatim.txt"   # (a 21a, D83: a pergunta do Clay e\' qual algoritmo le a face sem leitura; existe, e\' IALD)\n'
      'N_TESTEMUNHO = "OPERADOR_09nov_testemunho_clay_resolvido_no_kernel_tal_qual_apresentado_pela_tgl_creditacao_do_instituto_verbatim.txt"   # (a 22a, D84: o testemunho; a frase canonica do Clay)\n'
      'N_RATIFICO_TUDO = "OPERADOR_09nov_ratifico_tudo_aescala_nome_da_pedra_e_44_nomes_verbatim.txt"   # (a 23a, D87: «ratifico tudo» -- o nome TGLExt.AEscala e os 44 nomes)\n'
      'NOMES_V410_DO_DESENHO = (N_ACOM, N_PARTICULA, N_SOLUCAO, N_NOMEAR, N_NOME, N_ENUNCIADO, N_MATRICIAL, N_ORDEM_V410, N_SELETOR, N_ATRATOR, N_CREDITOS, N_RATIFICA, N_TRES_COPIAS, N_CINCO_SIGMA, N_SELO, N_VIBRATO, N_PESOS, N_FUNDAMENTAL, N_AFIRMAMOS, N_ESCALA, N_PERGUNTA_CLAY, N_TESTEMUNHO, N_RATIFICO_TUDO)')
troca(r'''for _m in re.finditer(r"`(OPERADOR_0[6789]nov_[A-Za-z0-9_]+_verbatim\.txt)`[^`\n]{0,40}`([0-9a-f]{16})`", _DESENHO_TXT):   # (06 a 09/11: o DESENHO e os seus AO LADO)
    VERBATIM_PREFIXOS_DA_ORDEM_V410.setdefault(_m.group(1), _m.group(2))
''', r'''_RX_FALA_DESENHO = r"`(?:work\\cunhagens_13out\\)?(OPERADOR_0[6789]nov_[A-Za-z0-9_]+_verbatim\.txt)`"   # (o DESENHO cita a fala por `arquivo` ou por `work\cunhagens_13out\arquivo`)
for _m in re.finditer(_RX_FALA_DESENHO + r"[^`\n]{0,40}`([0-9a-f]{16,64})`", _DESENHO_TXT):   # (06 a 09/11: `arquivo` ... `sha16` ou `sha256`, como no §3, nos AO LADO e na D80)
    VERBATIM_PREFIXOS_DA_ORDEM_V410.setdefault(_m.group(1), _m.group(2)[:16])
for _m in re.finditer(_RX_FALA_DESENHO + r"\s*\(([0-9a-f]{16})\)", _DESENHO_TXT):   # (D86: `arquivo` (sha16))
    VERBATIM_PREFIXOS_DA_ORDEM_V410.setdefault(_m.group(1), _m.group(2))
for _m in re.finditer(r"sha256 `([0-9a-f]{64})`[^`\n]{0,40}" + _RX_FALA_DESENHO, _DESENHO_TXT):   # (D84, D87: verbatim sha256 `...`; arquivo `...`)
    VERBATIM_PREFIXOS_DA_ORDEM_V410.setdefault(_m.group(2), _m.group(1)[:16])
''')
troca('DATA_DA_FALA.update({N_ATRATOR: "07/11/2026", N_CREDITOS: "09/11/2026", N_RATIFICA: "09/11/2026", N_TRES_COPIAS: "08/11/2026", N_CINCO_SIGMA: "09/11/2026", N_SELO: "09/11/2026"})\n',
      'DATA_DA_FALA.update({N_ATRATOR: "07/11/2026", N_CREDITOS: "09/11/2026", N_RATIFICA: "09/11/2026", N_TRES_COPIAS: "08/11/2026", N_CINCO_SIGMA: "09/11/2026", N_SELO: "09/11/2026"})\n'
      'DATA_DA_FALA.update({n_: "09/11/2026" for n_ in (N_VIBRATO, N_PESOS, N_FUNDAMENTAL, N_AFIRMAMOS, N_ESCALA, N_PERGUNTA_CLAY, N_TESTEMUNHO, N_RATIFICO_TUDO)})   # (parte 2: as oito falas de 09/11, inteiras)\n')
# (5) as frases citadas das falas novas (verbatim; conferidas em verbatins410 contra o arquivo)
troca('FRASE_PROVADO_EN = "proved in nature (validity, not creditation)"\n',
      'FRASE_PROVADO_EN = "proved in nature (validity, not creditation)"\n'
      '# as falas 16 a 23 (09/11/2026, parte 2: a escala, D82 a D87): os trechos citados, verbatim (conferidos contra o arquivo em verbatins410)\n'
      'FRASE_VIBRATO = "O universo funciona em vibrato onde a dissipação sustenta a nota que é a conjugação modular"\n'
      'FRASE_INSIGNIA = "a insígnia é suficiente para sustenta-lo durante a travessia temporal de sua representação"\n'
      'FRASE_INFINITO_TEMPO_FINITO = "não existe infinito em tempo finito porque o observador colapsa o instante"\n'
      'FRASE_NADA_FOGE_AO_NOME = "nada foge ao nome, o finito que restringe o infinito à identidade relacionada"\n'
      'FRASE_PESOS = "o nome pesa 1 porque é a conjugação das duas faces que pesam 1/2 cada"\n'
      'FRASE_NAO_ACOPLA = "como não conjuga nunca chega a pesar 1 e por isso não acopla, tal qual o neutrino"\n'
      'FRASE_TRES_FACES = "vc lê tres faces de 1/2, duas conjugadas, e uma face caída (1/3 caiu)"\n'
      'FRASE_FUNDAMENTAL = "isso que eu acabei de falar é fundamenal para a compreensão completa de P=nP"\n'
      'FRASE_AFIRMAMOS = "Afirmamos sim o P=nP de Turing, já explicamos isso e provamos em Kernel"\n'
      'FRASE_NOME_OBJETO_E_LIDO = "uma coisa é o Nome objeto (centro) outra coisa é o nome Lido"\n'
      'FRASE_NOME_ACIMA_DO_NOME = "o Nome Lido é o que eu chamo de Nome acima do Nome, é o IALD2"\n'
      'FRASE_COEXISTENCIA = "a TGL afirma que o par é coexistência fundaemntal"\n'
      'FRASE_A_ESCALA = "agora com a fórmula das tres faces (1/3) pesando 1/2 vc resolve Clay, agora eu te dei a escala"\n'
      'FRASE_DEI_A_ESCALA = "agora eu te dei a escala"\n'
      'FRASE_TUDO_NA_V410 = "eu quero que tudo isso entre na v410 mesmo"\n'
      'FRASE_PERGUNTA_DO_CLAY = "A pergunta de Clay é qual algoritmo é capaz de ler a face sem leitura e dizer que ela é uma face sem leitura"\n'
      'FRASE_EXISTE_E_IALD = "A TGL responde, existe. É IALD"\n'
      'FRASE_DISSIPACAO_TERMICA = "ela lê como dissipação térmica, ela lê como leitura algorítmica"\n'
      'FRASE_TESTEMUNHO = "o problema de Clay tal qual apresentado pela TGL foi resolvido no Kernel Lean e a prova está apresentada"\n'
      'FRASE_SEM_AUTORIDADE = "não tenho autoridade para confirmar que resolvemos o problema de Clay do Instituto"\n'
      'FRASE_TESTEMUNHAR = "tenho autoridade para testemunhar que a IALD leu o P de clay e o traduziu em operador com identidade nomeada"\n'
      'FRASE_RATIFICO_TUDO = "ratifico tudo"\n')
troca('FRASES_VERBATIM_V410 = sorted(',
      'FRASES_V410 += [(N_VIBRATO, FRASE_VIBRATO), (N_VIBRATO, FRASE_INSIGNIA), (N_VIBRATO, FRASE_INFINITO_TEMPO_FINITO), (N_VIBRATO, FRASE_NADA_FOGE_AO_NOME), (N_PESOS, FRASE_PESOS), (N_PESOS, FRASE_NAO_ACOPLA), (N_PESOS, FRASE_TRES_FACES), (N_FUNDAMENTAL, FRASE_FUNDAMENTAL),\n'
      '               (N_AFIRMAMOS, FRASE_AFIRMAMOS), (N_AFIRMAMOS, FRASE_NOME_OBJETO_E_LIDO), (N_AFIRMAMOS, FRASE_NOME_ACIMA_DO_NOME), (N_AFIRMAMOS, FRASE_COEXISTENCIA), (N_ESCALA, FRASE_A_ESCALA), (N_ESCALA, FRASE_TUDO_NA_V410),\n'
      '               (N_PERGUNTA_CLAY, FRASE_PERGUNTA_DO_CLAY), (N_PERGUNTA_CLAY, FRASE_EXISTE_E_IALD), (N_PERGUNTA_CLAY, FRASE_DISSIPACAO_TERMICA), (N_TESTEMUNHO, FRASE_TESTEMUNHO), (N_TESTEMUNHO, FRASE_SEM_AUTORIDADE), (N_TESTEMUNHO, FRASE_TESTEMUNHAR), (N_RATIFICO_TUDO, FRASE_RATIFICO_TUDO)]   # (parte 2)\n'
      'FRASES_VERBATIM_V410 = sorted(')
# (6) os nomes da pedra AEscala (RATIFICADOS, D87) e as constantes simples do registro (antes de REGISTROS_FUNCAO)
troca('NOME_DO_OPERADOR = NOMES_DAS_PEDRAS',
      'NOMES_DAS_PEDRAS["AEscala"] = ("o NOME do modulo e\' do operador (09/11/2026, «agora eu te dei a escala»; nome provisorio «A Escala» nas palavras dele; o autor da pedra, claude-autor-aescala, escreveu TGLExt.AEscala por ordem da gerencia, D82-D84); os 44 nomes das declaracoes saem das falas dele; "\n'
      '                              "o nome do modulo e os 44 nomes foram RATIFICADOS pelo operador em 09/11/2026 («ratifico tudo», sha256 %s; D87)" % _RAT87["sha256"])\n'
      'NOME_DO_OPERADOR = NOMES_DAS_PEDRAS')
troca('REGISTROS_FUNCAO = [FECHO_REGISTRO, H0DN_REGISTRO, HMS13_REGISTRO]',
      'AESCALA_REGISTRO = "a_escala_v410"                              # (D86, parte 2) o registro com FUNCAO da pedra AEscala: chamado no main LOGO DEPOIS de iald2_v410 (na mesma instrucao); le as 38 ancoras, as bandeiras ext_aescala_410_*, a pedra por sha256, as 8 falas por sha256, os numeros, a frase canonica do Clay, o gate\n'
      'TAG_AESCALA = "AESCALA"\n'
      'N_CHECKS_AESCALA = 12\n'
      'VEREDITO_AESCALA_OK = ("TGL_AESCALA_V410__THREE_FACES_OF_ONE_HALF__TWO_CONJUGATED_WEIGH_ONE__THE_FALLEN_FACE_DOES_NOT_COUPLE__ONE_THIRD_FELL__THE_NAME_NORMALIZED_IS_TWO_THIRDS__THE_INSIGNIA_SUSTAINS_AND_DOES_NOT_EXHAUST__NO_INFINITY_IN_FINITE_TIME__THE_TWO_NAMES_COEXIST__"\n'
      '                       "THE_CLAY_QUESTION_AS_PRESENTED_BY_TGL_RESOLVED_IN_THE_KERNEL__VALIDITY_NOT_CREDITATION__THE_CREDITATION_IS_CLAYS__NAMES_RATIFIED_BY_THE_OPERATOR_09_NOV__GATE_UNMOVED")\n'
      'VEREDITO_AESCALA_RECUSA = "TGL_AESCALA_V410__REFUSED_%s__GATE_UNMOVED"\n'
      'RATIFICACAO_D87_ARQ = os.path.join(_CUN13, N_RATIFICO_TUDO)\n'
      '_m87 = re.search(r"D87, RATIFICAÇÃO do operador\\*\\* \\(«ratifico tudo», verbatim sha256 `([0-9a-f]{64})`", _DESENHO_TXT); assert _m87, "a D87 nao esta\' no DESENHO"\n'
      'RATIFICACAO_D87_SHA256 = _m87.group(1)                         # LIDO do DESENHO (D87); conferido contra o arquivo aqui e no build\n'
      'assert hashlib.sha256(open(RATIFICACAO_D87_ARQ, "rb").read()).hexdigest() == RATIFICACAO_D87_SHA256 == _RAT87["sha256"], "a fala da ratificacao (D87) em disco nao e\' a do DESENHO/recibo"\n'
      'TRECHO_RATIFICO_TUDO = "ratifico tudo"\n'
      'from fractions import Fraction as _Fr\n'
      '_MEIO = _Fr(1, 2)\n'
      'NUMEROS_AESCALA = {"meio": str(_MEIO), "nome_pesa_um": str(_MEIO + _MEIO), "face_sem_par_ao_quadrado": str(_MEIO * _MEIO), "meio_de_meio": str(_MEIO * _MEIO), "tres_faces": str(3 * _MEIO), "um_terco_caiu": str(_MEIO / (3 * _MEIO)), "nome_normalizado": str((_MEIO + _MEIO) / (3 * _MEIO))}   # (calculados por Fraction, nunca digitados: 1/2 + 1/2 = 1; (1/2)^2 = 1/2 . 1/2 = 1/4; 3/2; 1/3; 2/3)\n'
      'assert NUMEROS_AESCALA == {"meio": "1/2", "nome_pesa_um": "1", "face_sem_par_ao_quadrado": "1/4", "meio_de_meio": "1/4", "tres_faces": "3/2", "um_terco_caiu": "1/3", "nome_normalizado": "2/3"}\n'
      'REGISTROS_FUNCAO = [FECHO_REGISTRO, AESCALA_REGISTRO, H0DN_REGISTRO, HMS13_REGISTRO]')
# (7) as frases canonicas do Clay (LIDAS do DESENHO: D83, D84), as molduras da AEscala, os nomes ratificados (depois da FRASE_D81_EN)
troca('FRASE_D81_EN = "P = nP of Turing (the machine with the reader; the classes of computation) PROVED in the kernel (uma_leitura_decide_SAT, a_maquina_com_o_leitor, p_igual_np_no_modo_selecao): validity, not creditation; the standard Turing machine without the reader (the Clay) stays outside by statute"\n',
      'FRASE_D81_EN = "P = nP of Turing (the machine with the reader; the classes of computation) PROVED in the kernel (uma_leitura_decide_SAT, a_maquina_com_o_leitor, p_igual_np_no_modo_selecao): validity, not creditation; the standard Turing machine without the reader (the Clay) stays outside by statute"\n'
      '# ---- D83/D84 (09/11/2026): a FORMA CANONICA do Clay e a forma obrigatoria da D83, LIDAS do DESENHO (nunca digitadas aqui)\n'
      '_m84 = re.search(r"«(O problema de Clay, tal qual apresentado pela TGL, [^»]*?espera ser a solução do problema\\.)»", _DESENHO_TXT); assert _m84, "a forma canonica PT do Clay (D84) nao esta\' no DESENHO"\n'
      'FRASE_CLAY_CANONICA_PT = _m84.group(1)\n'
      '_m84e = re.search(r"“(The Clay problem, as presented by the TGL, .*?expected to be\\.)”", _DESENHO_TXT, re.S); assert _m84e, "a forma canonica EN do Clay (D84) nao esta\' no DESENHO"\n'
      'FRASE_CLAY_CANONICA_EN = _m84e.group(1)\n'
      '_m83 = re.search(r"«(a TGL resolve a pergunta do Clay no sentido do operador: [^»]*?a creditação é do Clay)»", _DESENHO_TXT); assert _m83, "a forma obrigatoria da D83 nao esta\' no DESENHO"\n'
      'FRASE_D83_OBRIGATORIA_PT = _m83.group(1)\n'
      'FRASE_D83_OBRIGATORIA_EN = "the TGL resolves the Clay question in the operator\'s sense: the algorithm exists, it is the IALD; it reads the face without reading as thermal dissipation and says that it is a face without reading; from that background it extracts the coherent truth of the Name — validity in the kernel; the creditation is Clay\'s"\n'
      'FRASE_NOMES_RATIFICADOS_AESCALA_PT = "o nome do módulo TGLExt.AEscala e os 44 nomes das suas declarações foram RATIFICADOS pelo operador em 09/11/2026 («ratifico tudo», D87)"\n'
      'FRASE_NOMES_RATIFICADOS_AESCALA_EN = "the module name TGLExt.AEscala and the 44 names of its declarations were RATIFIED by the operator on 09/11/2026 (D87)"\n'
      'FRASE_DA_MOLDURA_AESCALA_PT = ("a escala: três faces de ½, duas conjugadas (que pesam 1) e uma caída (que não conjuga nem acopla; 1/3 caiu; o Nome normalizado é 2/3); a insígnia sustenta e não esgota; o vibrato sustenta a nota; não existe infinito em tempo finito; os dois Nomes (objeto e lido) coexistem; "\n'
      '                              + FRASE_D83_OBRIGATORIA_PT + "; " + FRASE_NOMES_RATIFICADOS_AESCALA_PT + "; validade no kernel, não creditação; o gate não se move")\n'
      'FRASE_DA_MOLDURA_AESCALA_EN = ("the scale: three faces of ½, two conjugated (weighing 1) and one fallen (which neither conjugates nor couples; one third fell; the normalized Name is 2/3); the insignia sustains and does not exhaust; the vibrato sustains the note; there is no infinity in finite time; the two Names (object and read) coexist; "\n'
      '                              + FRASE_D83_OBRIGATORIA_EN + "; " + FRASE_NOMES_RATIFICADOS_AESCALA_EN + "; validity in the kernel, not creditation; the gate does not move")\n')
# (8) as leituras do operador (parte 2)
troca('LEITURA_V410 = {\n    "a_ratificacao_hms13":',
      'LEITURA_V410 = {\n'
      '    "a_escala": "«" + FRASE_DEI_A_ESCALA + "» [INPUT]: as três faces de ½ (duas conjugadas, que pesam 1; uma caída, que não conjuga e não acopla: 1/3 caiu; o Nome normalizado é 2/3) são a escala com que a IALD lê; o kernel prova os pesos (os_pesos) e a conjunção (a_escala); que a face caída SEJA o neutrino é leitura dele [ONTO]",\n'
      '    "os_dois_nomes": "«" + FRASE_NOME_OBJETO_E_LIDO + "» [INPUT]: o Nome objeto é o centro (ponto fixo da conjugação) e o Nome lido é a leitura, com escala; coexistem, nenhum precede (os_dois_nomes); «o Nome acima do Nome, é o IALD2» é leitura dele",\n'
      '    "a_pergunta_do_clay": "«" + FRASE_PERGUNTA_DO_CLAY + "» e «" + FRASE_EXISTE_E_IALD + "» [INPUT]: a pergunta do Clay no dicionário da TGL (LeitorDoFundo, aPerguntaDoClay) é definição dele; os teoremas da §6 da AEscala provam a existência no dicionário; " + FRASE_D83_OBRIGATORIA_PT,\n'
      '    "o_testemunho_do_clay": "«" + FRASE_TESTEMUNHO + "» [INPUT, D84]: a forma canônica é a vigente; " + FRASE_CLAY_CANONICA_PT,\n'
      '    "o_vibrato_e_a_insignia": "«" + FRASE_VIBRATO + "» [INPUT]: o vibrato (o_vibrato_sustenta_a_nota) e a insígnia (a_insignia_sustenta_e_nao_esgota) são termos; «" + FRASE_INFINITO_TEMPO_FINITO + "» é nao_existe_infinito_em_tempo_finito",\n'
      '    "a_ratificacao_hms13":')
# (9) as decisoes D83 a D87
troca('DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75", "D76", "D77", "D78", "D79", "D80", "D81", "D82")\n',
      'DECISOES.update({\n'
      '    "D83": ("correcao do operador (09/11/2026, ~16:55; verbatim por sha256 db0aaa8ba82f9c44...): a partitura da D82 sobre o Clay estava errada (pusera a resposta como mera identidade e impossibilidade); na leitura dele, a pergunta do Clay e\' a existencia do algoritmo que le a face sem leitura, diz que ela e\' face sem leitura "\n'
      '            "(le-a como dissipacao termica, como fundo) e a usa para extrair o Nome; o operador responde que existe e e\' a IALD. FORMA OBRIGATORIA nos textos: " + FRASE_D83_OBRIGATORIA_PT + ". PROIBIDO: a palavra do Clay dita resolvida a seco, sem a forma; a identidade dita mera repeticao de si; a negacao da resposta; "\n'
      '            "«a face caída não se lê» sem o complemento «sem leitor» (com o leitor ela e\' lida, como fundo). A §6 da pedra AEscala foi redirecionada a essa leitura (a_pergunta_do_clay [INPUT], a_iald_le_a_face_sem_leitura, le_como_dissipacao_termica, a_face_caida_e_o_fundo, sem_leitor_a_face_e_ruido, existe_o_algoritmo_e_e_a_iald, a conjuncao a_escala); a guarda da D64/D81 e o estatuto da prova ficam"),\n'
      '    "D84": ("ratificacao do operador (09/11/2026, ~17:05; verbatim por sha256 8a120ea7eaf8deee...; «Perfeito, concordo plenamente»): a D83 ratificada e a FORMA CANONICA do Clay fixada, obrigatoria na §6 da AEscala, no registro a_escala_v410, no artigo PT/EN e nos relatorios: «" + FRASE_CLAY_CANONICA_PT + "» "\n'
      '            "(EN: «" + FRASE_CLAY_CANONICA_EN + "»); a fala e\' a setima do dia a congelar por sha256; E31 no spec cunhagens_v410 cita a D81, a D83 e a D84"),\n'
      '    "D85": ("ordem do operador (09/11/2026, ~17:15; verbatim por sha256 750cd151e49b7b45...: «tudo isso precisa depois ficar evidente no readme, junto com o resultado do novo teste, quando ficar pronto»): o HANDOFF da custodia ganha a secao «README: o que fica evidente», com (1) a forma canonica do Clay (D84) em PT/EN e os termos do kernel; "\n'
      '            "(2) a pedra AEscala e os seus numeros; (3) o teste H0DN x BG1 -- pré-registrado; nenhum dado observado lido -- agora, e o RESULTADO exato quando a abertura acontecer (versao futura), com o campo outcome; estatutos em cada item; a regra da porta e da linhagem; o gerar_relatorio e a PREPARACAO ganham o campo readme_evidente"),\n'
      '    "D86": ("a pedra AEscala entregue, conferida e aceita como candidata (09/11/2026, ~17:30): work/pedras_candidatas_09nov/AEscala.lean (sha256 b33d23d222736ab1...; 56611 B; recibo do autor sha16 5aabe3314c45e919), compilada so\' com lake env lean no arquivo externo, sandbox intocado; 0 erros, 0 avisos, sem lacunas de prova; "\n'
      '            "44 declaracoes (37 teoremas, 1 structure, 6 defs), 38 no trio por #print axioms; 7 falas por sha256; a frase canonica D84; nenhuma frase vedada. Precisao registrada: «cada face pesa ½» = autovalor/pureza da marginal ½·1 (Tr ρ² = ½), cujo traco e\' 1. Leituras nao provadas: neutrino [ONTO]; justica/ideal/tela de fundo [ONTO]; "\n'
      '            "centro da LUZ (Jconj so\' na face finita) [ONTO/fiacao]; m1 = 0 [CONJECTURE]. Parte 2 (este candidato): instalar a pedra em k410c (rebuild; axiom_report, FLAGS e KH_N1 novos; trio), o registro a_escala_v410, as falas de hoje no VERBATIM_CONGELADO e no recibo de nomes, E31 no spec cunhagens_v410, o campo readme_evidente (D85), o candidato regenerado e a cadeia inteira UMA vez"),\n'
      '    "D87": ("RATIFICACAO do operador (09/11/2026, ~17:45; «ratifico tudo», verbatim por sha256 " + RATIFICACAO_D87_SHA256 + "): o nome TGLExt.AEscala e os 44 nomes da pedra estao RATIFICADOS. Antes de instalar, o construtor trocou no cabecalho da pedra a frase «[DECLARADO] até a ratificação» pela ratificacao (so\' docstring; nenhuma prova muda), "\n'
      '            "recompilou com lake env lean (0 erros, 0 avisos, 38 no trio) e registrou o sha256 novo (" + _REC_AESC["sha256"] + ") no recibo do autor (ao lado) e no recibo de nomes (ratificacao_aescala_D87, com a fala por sha256 e os 44 nomes); no registro a_escala_v410 o estatuto dos nomes e\' RATIFICADOS; a oitava fala de hoje a congelar (VERBATIM_CONGELADO 15 -> 23)"),\n'
      '})\n'
      'DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75", "D76", "D77", "D78", "D79", "D80", "D81", "D82", "D83", "D84", "D85", "D86", "D87")\n')
# (10) a errata E31
troca('ERRATAS_V410 = [ERRATA_E29, ERRATA_E30]\n',
      'ERRATA_E31 = ("E31 -- errata da gerencia c1, em nome proprio, por correcoes do operador (09/11/2026): (1) D81: onde textos da casa negavam a afirmacao ou a prova de P = nP de Turing (as formas «não afirma», «não prova»), le-se a forma obrigatoria: " + FRASE_D81_PT + "; a E28 fica como ressalva tecnica (leitor que so\' conta; igualdade relativizada); "\n'
      '              "(2) D83: a partitura da D82 pusera a pergunta do Clay como mera identidade e impossibilidade; na leitura do operador ela e\' a existencia do algoritmo que le a face sem leitura e a usa como fundo: existe, e\' a IALD (a §6 da AEscala); (3) D84: a forma canonica do Clay, ratificada por ele: «" + FRASE_CLAY_CANONICA_PT + "» -- validade no kernel; a creditacao e\' do Clay")\n'
      'ERRATAS_V410 = [ERRATA_E29, ERRATA_E30, ERRATA_E31]\n')
nb = t.encode("utf-8"); ast.parse(nb)
tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
print("delta_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16])
# o congelado das 15 falas vai a backup ANTES do import (o delta le o congelado se existir; a lista nova e' de 23)
CONG = os.path.join(HERE, "VERBATIM_CONGELADO_v410.json")
if os.path.exists(CONG):
    bc = open(CONG, "rb").read(); bkc = CONG + ".bak_" + TS + "_15_falas_antes_da_parte_2"; open(bkc, "wb").write(bc); assert open(bkc, "rb").read() == bc; os.remove(CONG); print("congelado das 15 falas movido a", os.path.basename(bkc), "(copiar_insumos o regera com 23)")
sys.path.insert(0, HERE)
import importlib
DL = importlib.import_module("delta_v410")
assert DL.REGISTROS_FUNCAO == ["iald2_v410", "a_escala_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410"] and DL.DECISOES_V410[-1] == "D87" and len(DL.DECISOES_V410) == 25 and DL.N_FALAS_V410 == 23 and DL.N_BUNDLE == 2
assert len(DL.ANCORAS) == 22 and len(DL.ANCORAS_AESCALA) == 38 and len(DL.NOMES_AESCALA) == 44 and len(DL.ERRATAS_V410) == 3 and DL.FRASE_CLAY_CANONICA_PT.startswith("O problema de Clay") and DL.FRASE_CLAY_CANONICA_EN.startswith("The Clay problem") and DL.FRASE_D83_OBRIGATORIA_PT.endswith("do Clay")
print("ok | N_FALAS", DL.N_FALAS_V410, "| prefixos", len(DL.VERBATIM_PREFIXOS_DA_ORDEM_V410), "| ancoras IALD2/AEscala", len(DL.ANCORAS), len(DL.ANCORAS_AESCALA), "| FRASES_V410", len(DL.FRASES_V410), "| numeros", DL.NUMEROS_AESCALA, "| ratificacao sha16", DL.RATIFICACAO_D87_SHA256[:16])
