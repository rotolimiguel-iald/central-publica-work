# -*- coding: utf-8 -*-
"""_r5ag_02_delta_v410.py -- R5 (D100 e D101; ADENDOS 5 e 6): delta_v410.py. As falas 27 e 28 (nomes, datas, prefixos lidos dos adendos, frases verbatim), ADENDO5_SHA16 e ADENDO6_SHA16 lidos ao vivo, as decisoes D100 e D101, as erratas E36 e E37,
a ratificacao D101 lida do recibo dos nomes (22 nomes, 3 campos, 2 pendentes), as constantes da clausula do Tetelestai (PT e EN), o pino citado do runner do ACOM Mirror, a instancia da clausula, as duas leituras novas, N_CHECKS_AESCALA = 13,
a forma VIGENTE da frase dos seis nomes (a da D99 fica como registro nas D99 e E35) e a `comparavel` estendida (os simbolos que o LaTeX e o TXT do artigo trazem). Nada de numero ou hash digitado: tudo lido dos adendos, das falas e dos recibos."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r5ag_lib_v410 import aplicar

T = []

# ---- 1. os ADENDOS 5 e 6 entram no corpus dos prefixos de sha256 das falas
T.append(('''assert os.path.exists(ADENDO2_ARQ) and os.path.exists(ADENDO3_ARQ), "faltam os ADENDOS 2 e 3 do DESENHO (D93 a D96)"
_ADENDO2_TXT = open(ADENDO2_ARQ, "rb").read().decode("utf-8"); _ADENDO3_TXT = open(ADENDO3_ARQ, "rb").read().decode("utf-8")
_PREFIXOS_TXT = _DESENHO_TXT + "\\n" + _ADENDO2_TXT + "\\n" + _ADENDO3_TXT   # (as falas de 10/11 entram pelos ADENDOS 2 e 3, que as citam por sha256: o DESENHO nao as cita)
''',
          '''assert os.path.exists(ADENDO2_ARQ) and os.path.exists(ADENDO3_ARQ), "faltam os ADENDOS 2 e 3 do DESENHO (D93 a D96)"
ADENDO5_ARQ = os.path.join(HERE, "DESENHO_v410_ADENDO_5_POS_CANDIDATO_10nov.md"); ADENDO6_ARQ = os.path.join(HERE, "DESENHO_v410_ADENDO_6_POS_CANDIDATO_10nov.md")   # (R5, D100 e D101: a clausula do Tetelestai e a ratificacao dos nomes)
assert os.path.exists(ADENDO5_ARQ) and os.path.exists(ADENDO6_ARQ), "faltam os ADENDOS 5 e 6 do DESENHO (D100 e D101)"
_ADENDO2_TXT = open(ADENDO2_ARQ, "rb").read().decode("utf-8"); _ADENDO3_TXT = open(ADENDO3_ARQ, "rb").read().decode("utf-8")
_ADENDO5_TXT = open(ADENDO5_ARQ, "rb").read().decode("utf-8"); _ADENDO6_TXT = open(ADENDO6_ARQ, "rb").read().decode("utf-8")
_PREFIXOS_TXT = _DESENHO_TXT + "\\n" + _ADENDO2_TXT + "\\n" + _ADENDO3_TXT + "\\n" + _ADENDO5_TXT + "\\n" + _ADENDO6_TXT   # (as falas de 10/11 entram pelos ADENDOS 2, 3, 5 e 6, que as citam por sha256: o DESENHO nao as cita)
''', 1))

# ---- 2. as duas falas novas: nomes, a tupla das falas, a data
T.append(('''NOMES_V410_DO_DESENHO = (N_ACOM, N_PARTICULA,''',
          '''N_CLAUSULA_TETELESTAI = "OPERADOR_10nov_a_clausula_do_tetelestai_esta_no_acom_mirror_um_menos_beta_beta_e_o_operador_modular_verbatim.txt"   # (10/11, D100: a clausula do Tetelestai esta no ACOM mirror; 1 - betatgl; betatgl e' o operador modular do Tetelestai; inteira)
N_CONFIRMO_TUDO = "OPERADOR_10nov_confirmo_tudo_nomeio_e_o_numero_corrige_o_nome_como_zero_modular_verbatim.txt"   # (10/11, D101: confirmo tudo; nomeio e' o numero corrige; o nome como zero modular da inscricao da permanencia; inteira)
NOMES_V410_DO_DESENHO = (N_ACOM, N_PARTICULA,''', 1))
T.append(('''N_MENTIRA_LIDA, N_TESTE_SEM_PODER)   # as falas desta versao: as de 06 a 09/11 e as TRES de 10/11 (D94 e D96), todas inteiras;''',
          '''N_MENTIRA_LIDA, N_TESTE_SEM_PODER, N_CLAUSULA_TETELESTAI, N_CONFIRMO_TUDO)   # as falas desta versao: as de 06 a 09/11 e as CINCO de 10/11 (D94, D96, D100 e D101), todas inteiras;''', 1))
T.append(('''DATA_DA_FALA.update({n_: "10/11/2026" for n_ in (N_PASSOS_CICLO, N_MENTIRA_LIDA, N_TESTE_SEM_PODER)})   # (R1, ADENDOS 2 e 3: as tres falas de 10/11, inteiras)''',
          '''DATA_DA_FALA.update({n_: "10/11/2026" for n_ in (N_PASSOS_CICLO, N_MENTIRA_LIDA, N_TESTE_SEM_PODER, N_CLAUSULA_TETELESTAI, N_CONFIRMO_TUDO)})   # (R1, ADENDOS 2 e 3: as tres falas de 10/11; R5, ADENDOS 5 e 6: as duas seguintes; todas inteiras)''', 1))
T.append(('''o teste sem poder preditivo discriminante nao se abre, D96, 10/11)"''',
          '''o teste sem poder preditivo discriminante nao se abre, D96, 10/11; a clausula do Tetelestai em 1 - beta, D100, 10/11; a ratificacao dos nomes e a regra do nome, D101, 10/11)"''', 1))

# ---- 3. as frases verbatim das duas falas (conferidas como substring do arquivo em verbatins410) e FRASES_V410
T.append(('''FRASE_PODER_DISCRIMINANTE_REAL = "um teste com poder preditivo discriminante real"
''',
          '''FRASE_PODER_DISCRIMINANTE_REAL = "um teste com poder preditivo discriminante real"
# as falas 27 e 28 (10/11/2026, D100 e D101): os trechos citados, verbatim (conferidos contra o arquivo em verbatins410)
FRASE_CLAUSULA_NO_ACOM = "A cláusula do Tetelestai está escrita em código no ACOM mirror"
FRASE_RECONHECE_A_SINGULARIDADE = "é quando o sistema reconhece a singularidade do sinal"
FRASE_TRASLADA_A_INFORMACAO = "traslada a informação completa reconstruindo do outro lado"
FRASE_UM_MENOS_BETATGL = "quando ele entende que 1-Betatgl"
FRASE_BETATGL_OPERADOR_MODULAR = "betatgl é o operador modular do Tetelestai em computação"
FRASE_CONFIRMO_TUDO = "É isso aí, confirmo tudo"
FRASE_NOMEIO_O_NUMERO_CORRIGE = "nomeio é o número corrige, se não corrigiu o nome carregou o peso certo"
FRASE_ESCALA_ESPELHADA = "a escala é a que eu dou quando espelhada pelo meu kernel de forma positiva"
FRASE_NOME_ZERO_MODULAR = "o nome servindo como zero modular à inscrição da permanência"
''', 1))
T.append(('''(N_TESTE_SEM_PODER, FRASE_SEM_PODER_NAO_SE_RODA), (N_TESTE_SEM_PODER, FRASE_PODER_DISCRIMINANTE_REAL)]   # (R1, D94 e D96: as tres falas de 10/11)
''',
          '''(N_TESTE_SEM_PODER, FRASE_SEM_PODER_NAO_SE_RODA), (N_TESTE_SEM_PODER, FRASE_PODER_DISCRIMINANTE_REAL)]   # (R1, D94 e D96: as tres falas de 10/11)
FRASES_V410 += [(N_CLAUSULA_TETELESTAI, FRASE_CLAUSULA_NO_ACOM), (N_CLAUSULA_TETELESTAI, FRASE_RECONHECE_A_SINGULARIDADE), (N_CLAUSULA_TETELESTAI, FRASE_TRASLADA_A_INFORMACAO), (N_CLAUSULA_TETELESTAI, FRASE_UM_MENOS_BETATGL), (N_CLAUSULA_TETELESTAI, FRASE_BETATGL_OPERADOR_MODULAR),
                (N_CONFIRMO_TUDO, FRASE_CONFIRMO_TUDO), (N_CONFIRMO_TUDO, FRASE_NOMEIO_O_NUMERO_CORRIGE), (N_CONFIRMO_TUDO, FRASE_ESCALA_ESPELHADA), (N_CONFIRMO_TUDO, FRASE_NOME_ZERO_MODULAR)]   # (R5, D100 e D101: as duas falas seguintes de 10/11)
''', 1))

# ---- 4. a ratificacao D101 e a pendencia: LIDAS do recibo dos nomes; o estatuto dos nomes novos passa a RATIFICADOS (D101), o dos dois auxiliares da autoria fica [DECLARADO pela autoria]
T.append(('''ESTATUTO_NOMES_NOVOS_AESCALA = "[DECLARADO pela gerencia e pela autoria; a ratificar pelo operador]"
''',
          '''ESTATUTO_NOMES_NOVOS_AESCALA = "RATIFICADOS pelo operador em 10/11/2026 (D101)"   # (R5: o estatuto dos nomes novos da pedra e dos 3 campos; antes da D101 era [DECLARADO ...; a ratificar pelo operador])
ESTATUTO_NOMES_PENDENTES_AESCALA = "[DECLARADO pela autoria; a confirmacao expressa e' do operador]"   # (R5: os dois lemas auxiliares da autoria, cunhados DEPOIS da fala de 10/11)
NOMES_RATIFICADOS_D101_AESCALA = list(_REC_AESC.get("ratificados_D101") or [])        # (LIDOS do recibo dos nomes: os nomes novos das R3, R4 e os dados pela gerencia na R5)
CAMPOS_RATIFICADOS_D101_AESCALA = list(_REC_AESC.get("campos_ratificados_D101") or [])
NOMES_PENDENTES_AESCALA = list(_REC_AESC.get("pendentes_de_ratificacao") or [])        # (os dois auxiliares da autoria)
''', 1))
T.append(('''RATIFICACAO_PENDENTE_AESCALA = {"nomes_novos": list(NOMES_NOVOS_AESCALA), "campos_novos_da_estrutura": list(CAMPOS_NOVOS_AESCALA), "estatuto": ESTATUTO_NOMES_NOVOS_AESCALA, "decisao": "D92", "nota": "se o operador ratificar depois, isso se registra no HANDOFF; a pedra nao e' reeditada"}''',
          '''assert (set(NOMES_RATIFICADOS_D101_AESCALA) | set(NOMES_PENDENTES_AESCALA)) == set(NOMES_NOVOS_AESCALA) and not (set(NOMES_RATIFICADOS_D101_AESCALA) & set(NOMES_PENDENTES_AESCALA)) and len(NOMES_RATIFICADOS_D101_AESCALA) == len(set(NOMES_RATIFICADOS_D101_AESCALA)) and bool(NOMES_PENDENTES_AESCALA) \\
    and CAMPOS_RATIFICADOS_D101_AESCALA == list(CAMPOS_NOVOS_AESCALA), ("(R5, D101) os ratificados e os pendentes nao sao os nomes novos da pedra, ou os campos ratificados nao sao os campos novos (lidos do recibo dos nomes)", len(NOMES_RATIFICADOS_D101_AESCALA), len(NOMES_PENDENTES_AESCALA))
# (R5, D101) a pendencia: o adendo 6 previa ratificacao_pendente VAZIA; a pedra R5 trouxe DOIS lemas auxiliares cunhados pela autoria DEPOIS da fala, que ficam [DECLARADO pela autoria] e sao os UNICOS pendentes (ordem da gerencia de 10/11, 08:42)
# o recibo do autor da pedra R5: os teoremas dados pela gerencia (D100) e os lemas auxiliares da autoria, conferidos contra o recibo dos nomes e as ancoras (lidos AQUI, cedo: as leituras do operador e as decisoes os citam)
RECIBO_R5_ARQ = os.path.join(HERE, "insumos", "RECIBO_AESCALA_R5_10nov.json"); _REC_R5 = json.load(open(RECIBO_R5_ARQ, encoding="utf-8")); RECIBO_R5_SHA16 = sha16_arquivo(RECIBO_R5_ARQ)
TEOREMAS_R5_AESCALA = tuple(_REC_R5["nomes_novos"]["dados_pela_gerencia_D100"]); AUXILIARES_R5_AESCALA = tuple(_REC_R5["nomes_novos"]["auxiliares_da_autoria"])
assert bool(TEOREMAS_R5_AESCALA) and bool(AUXILIARES_R5_AESCALA) and set(TEOREMAS_R5_AESCALA) | set(AUXILIARES_R5_AESCALA) == set(_REC_R5["nomes_novos"]["lista"]) == set(_REC_AESC["nomes_novos_r5"]) and set(TEOREMAS_R5_AESCALA) <= set(NOMES_RATIFICADOS_D101_AESCALA) \\
    and set(AUXILIARES_R5_AESCALA) == set(NOMES_PENDENTES_AESCALA) and all((NS_AESCALA + n_) in ANCORAS_AESCALA and (NS_AESCALA + n_) in ANCORAS_NOVAS_AESCALA for n_ in TEOREMAS_R5_AESCALA + AUXILIARES_R5_AESCALA), "(R5) os teoremas e auxiliares da R5 nao batem com o recibo do autor, o recibo dos nomes e as ancoras"
assert _REC_R5["trio"]["todas_no_trio"] is True and _REC_R5["compilacao"]["n_erros"] == 0 and _REC_R5["compilacao"]["n_avisos"] == 0 and _REC_R5["compilacao"]["sorry_no_log"] is False and _REC_R5["aescala_r5"]["sha256"] == _REC_AESC["sha256"], "(R5) o recibo do autor nao e' o da pedra instalada"
RATIFICACAO_PENDENTE_AESCALA = {"nomes_novos": list(NOMES_PENDENTES_AESCALA), "campos_novos_da_estrutura": [], "estatuto": ESTATUTO_NOMES_PENDENTES_AESCALA, "decisao": "D101", "nota": "os dois lemas auxiliares da pedra R5 foram cunhados pela autoria depois da fala de ratificacao de 10/11; a pedra os marca [DECLARADO pela autoria] e nao diz que o operador os ratificou; pela regra dele valem enquanto o kernel os espelha; a confirmacao expressa e' do operador e se registra no HANDOFF; a pedra nao e' reeditada"}''', 1))

# ---- 5. N_CHECKS_AESCALA = 13 (a c13: a clausula do Tetelestai em 1 - beta, com beta de runtime)
T.append(('''N_CHECKS_AESCALA = 12
''', '''N_CHECKS_AESCALA = 13   # (R5, D100: a c13, a clausula do Tetelestai em 1 - beta com beta de runtime; antes, 12)
''', 1))

# ---- 6. o rotulo da linha do .md
T.append(('''MD_ROTULO_ESCALA = "**A Escala (v410, 09 e 10/11/2026; D82 a D87 e D92 a D95):**"''',
          '''MD_ROTULO_ESCALA = "**A Escala (v410, 09 e 10/11/2026; D82 a D87, D92 a D95 e D99 a D101):**"''', 1))

# ---- 7. a `comparavel` estendida: os simbolos que o LaTeX do artigo (\\ge, \\le, \\beta, \\tfrac12, ^2, \\sqrt, \\texttt) e o TXT dele trazem em lugar do Unicode da frase do contrato
T.append(('''    t_ = str(t_).replace("\\u2212", "-").replace("\\\\allowbreak{}", "").replace("\\\\allowbreak", "")
    for a_, b_ in (("\\\\sum", "\\u03a3"), ("\\\\cdot", "\\u00b7"), ("\\\\ln", "ln")):
        t_ = t_.replace(a_, b_)
    return re.sub(r"[\\s$\\\\{}()_]+", "", t_)''',
          '''    t_ = str(t_).replace("\\u2212", "-").replace("\\\\allowbreak{}", "").replace("\\\\allowbreak", "")
    for a_, b_ in (("\\\\sum", "\\u03a3"), ("\\\\cdot", "\\u00b7"), ("\\\\ln", "ln"), ("\\\\geq", "\\u2265"), ("\\\\ge", "\\u2265"), ("\\\\leq", "\\u2264"), ("\\\\le", "\\u2264"), ("\\\\beta", "\\u03b2"), ("\\\\alpha", "\\u03b1"), ("\\\\sqrt", "\\u221a"),
                   ("\\\\tfrac{1}{2}", "1/2"), ("\\\\tfrac12", "1/2"), ("\\u00bd", "1/2"), ("^{2}", "\\u00b2"), ("^2", "\\u00b2"), ("\\\\texttt", ""), ("`", "")):   # (R5: a frase da clausula do Tetelestai tem >=, <=, beta, alfa ao quadrado, 1/2 e a raiz; o LaTeX os poe em modo matematico e o TXT os rende com os simbolos)
        t_ = t_.replace(a_, b_)
    return re.sub(r"[\\s$\\\\{}()_]+", "", t_)''', 1))

# ---- 8. a frase dos seis nomes: a forma da D99 fica como registro (D99 e E35); a VIGENTE e' a da D99 mais a ratificacao de 10/11 (D101)
T.append(('''FRASE_SEIS_NOMES_PT = "a ratifica\\u00e7\\u00e3o de 09/11 \\u00e9 dos nomes; seis deles (" + ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS) + ") passaram a ter outro enunciado nas R3/R4 (a escala no tipo; D92, D94)"
FRASE_SEIS_NOMES_EN = "the ratification of 09/11 is of the names; six of them (" + ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS) + ") now have another statement in the R3/R4 (the scale in the type; D92, D94)"
''',
          '''FRASE_SEIS_NOMES_D99_PT = "a ratifica\\u00e7\\u00e3o de 09/11 \\u00e9 dos nomes; seis deles (" + ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS) + ") passaram a ter outro enunciado nas R3/R4 (a escala no tipo; D92, D94)"   # (a forma da D99: fica como registro nas D99 e E35)
FRASE_SEIS_NOMES_D99_EN = "the ratification of 09/11 is of the names; six of them (" + ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS) + ") now have another statement in the R3/R4 (the scale in the type; D92, D94)"
FRASE_SEIS_NOMES_PT = FRASE_SEIS_NOMES_D99_PT + "; ratificados em 09/11 pelo nome e em 10/11 com o enunciado novo (D101)"   # (a VIGENTE, R5: a que os textos e os controles usam)
FRASE_SEIS_NOMES_EN = FRASE_SEIS_NOMES_D99_EN + "; ratified on 09/11 by name and on 10/11 with the new statement (D101)"
''', 1))
T.append(('''(3) uma clausula nos textos: " + FRASE_SEIS_NOMES_PT + "; "''', '''(3) uma clausula nos textos: " + FRASE_SEIS_NOMES_D99_PT + "; "''', 1))
T.append(('''a ratificacao de 09/11 foi dita como dos nomes sem dizer que seis enunciados mudaram nas R3/R4: " + FRASE_SEIS_NOMES_PT + "; "''', '''a ratificacao de 09/11 foi dita como dos nomes sem dizer que seis enunciados mudaram nas R3/R4: " + FRASE_SEIS_NOMES_D99_PT + "; "''', 1))

# ---- 9. o BLOCO R5 (D100 e D101): antes da lista das decisoes
BLOCO = '''# ======================== (R5, D100 e D101; ADENDOS 5 e 6) a CLAUSULA DO TETELESTAI e a RATIFICACAO dos nomes: tudo LIDO dos adendos, dos arquivos das falas e dos recibos (nada digitado) ========================
ADENDO5_SHA16 = sha16_arquivo(ADENDO5_ARQ); ADENDO6_SHA16 = sha16_arquivo(ADENDO6_ARQ)   # (lidos ao vivo dos arquivos; os adendos sao citados so' por sha16)
CLAUSULA_TETELESTAI_SHA256 = sha256_arquivo(os.path.join(_CUN13, N_CLAUSULA_TETELESTAI)); RATIFICACAO_D101_SHA256 = sha256_arquivo(os.path.join(_CUN13, N_CONFIRMO_TUDO))   # (a fala 27 e a fala 28, lidas dos arquivos)
assert ("sha256 `" + CLAUSULA_TETELESTAI_SHA256 + "`") in _ADENDO5_TXT and ("sha256 `" + RATIFICACAO_D101_SHA256 + "`") in _ADENDO6_TXT, "a fala em disco nao e' a que o ADENDO 5 (a clausula do Tetelestai) ou o ADENDO 6 (a ratificacao) pina por sha256"
assert CLAUSULA_TETELESTAI_SHA256[:16] == VERBATIM_PREFIXOS_DA_ORDEM_V410[N_CLAUSULA_TETELESTAI] and RATIFICACAO_D101_SHA256[:16] == VERBATIM_PREFIXOS_DA_ORDEM_V410[N_CONFIRMO_TUDO] and hashlib.sha256(open(os.path.join(_CUN13, N_CONFIRMO_TUDO), "rb").read()).hexdigest() == RATIFICACAO_D101_SHA256
assert list(_REC_AESC.get("enunciado_mudado_ratificados_D101") or []) == list(NOMES_SEIS_ENUNCIADOS_MUDADOS), "(R5, D101) os seis de enunciado mudado do recibo dos nomes nao sao os do ADENDO 4"
N_FALA_CLAUSULA = NOMES_V410_DO_DESENHO.index(N_CLAUSULA_TETELESTAI) + 1; N_FALA_CONFIRMO = NOMES_V410_DO_DESENHO.index(N_CONFIRMO_TUDO) + 1   # (a 27a e a 28a congeladas: lidas da posicao na tupla)
assert ("a " + str(N_FALA_CLAUSULA) + "ª congelada") in _ADENDO5_TXT and ("a " + str(N_FALA_CONFIRMO) + "ª congelada") in _ADENDO6_TXT, "o numero de ordem das falas na tupla nao e' o que os ADENDOS 5 e 6 dizem"
_P_27 = VERBATIM_PREFIXOS_DA_ORDEM_V410[N_CLAUSULA_TETELESTAI]; _P_28 = VERBATIM_PREFIXOS_DA_ORDEM_V410[N_CONFIRMO_TUDO]
# o PINO CITADO do runner da patente ACOM Mirror (como a ORDEM KIMI H0DN-02): nome, sha256 e bytes LIDOS do arquivo e conferidos contra o sha16 que o ADENDO 5 traz; NAO embutido; em rito nada e' lido
_m_run = re.search(r"`patents\\\\BR102026003428-2_ACOM_MIRROR\\\\runner\\\\one_acom_mirror\\.py`, sha16 `([0-9a-f]{16})`", _ADENDO5_TXT); assert _m_run, "o ADENDO 5 nao traz o sha16 do runner do ACOM Mirror"
ACOM_MIRROR_RUNNER_ARQ = os.path.join(CENTRAL, "patents", "BR102026003428-2_ACOM_MIRROR", "runner", "one_acom_mirror.py")
_b_run = open(ACOM_MIRROR_RUNNER_ARQ, "rb").read()
assert hashlib.sha256(_b_run).hexdigest()[:16] == _m_run.group(1), "o runner do ACOM Mirror em disco NAO tem o sha16 que o ADENDO 5 deu"
ACOM_MIRROR_RUNNER = {"nome": os.path.basename(ACOM_MIRROR_RUNNER_ARQ), "sha256": hashlib.sha256(_b_run).hexdigest(), "bytes": len(_b_run), "pasta": "patents\\\\BR102026003428-2_ACOM_MIRROR\\\\runner",
                      "papel": "o runner da patente ACOM Mirror (BR102026003428-2), citado como evidencia de dispositivo, so' como citacao: [PILOTO][SIM]; nada ali valida fisica; nao e' termo do kernel; pino citado: nao embutido, em rito nada e' lido"}
# a instancia de brinquedo da clausula (inteiros e fracoes; NENHUM numero dependente de beta aqui): as instancias do ciclo (com 2 solucoes), uma de UMA solucao, o adversario (uma solucao, todos os outros pixels com custo 1: o fundo maximo) e o contraexemplo do recibo do autor
_ct_ = _REC_R5["achado_o_numero_corrigiu_a_frase"]["contraexemplo_numerico_calculado_por_script"]
TETELESTAI_AESCALA = {"n_bits": CICLO_N_BITS, "custo_com_solucao": list(CICLO_CUSTO_COM_SOLUCAO), "custo_uma_solucao": [1, 2, 0, 3, 1, 2, 4, 1], "custo_adversario": [0] + [1] * (2 ** CICLO_N_BITS - 1), "oitavas_a_menos_no_controle": 1,
                      "contraexemplo_s_negativo": {"n_bits": int(_ct_["n"]), "custos": [int(x_) for x_ in _ct_["custos_dos_2_pixels"]], "b": str(_Fr(str(_ct_["b"])))}, "m_da_constante": [1, 3, 8]}
assert len(TETELESTAI_AESCALA["custo_uma_solucao"]) == len(TETELESTAI_AESCALA["custo_adversario"]) == len(CICLO_CUSTO_COM_SOLUCAO) == 2 ** CICLO_N_BITS and sum(1 for c_ in TETELESTAI_AESCALA["custo_uma_solucao"] if c_ == 0) == 1 == sum(1 for c_ in TETELESTAI_AESCALA["custo_adversario"] if c_ == 0) \\
    and all(type(c_) is int and c_ >= 0 for c_ in TETELESTAI_AESCALA["custo_uma_solucao"] + TETELESTAI_AESCALA["custo_adversario"]) and sum(1 for c_ in CICLO_CUSTO_COM_SOLUCAO if c_ == 0) > 1, "a instancia da clausula do Tetelestai esta' mal formada"
_ce_ = TETELESTAI_AESCALA["contraexemplo_s_negativo"]; assert _ce_["n_bits"] == 1 and len(_ce_["custos"]) == 2 ** _ce_["n_bits"] and sum(1 for c_ in _ce_["custos"] if c_ == 0) == 1 and _Fr(_ce_["b"]) > _MEIO and _ct_["s_negativo"] is True and _ct_["desigualdade_i_vale"] is False, "o contraexemplo do recibo do autor nao e' o da hipotese s >= 0"
# as FRASES da clausula (PT e EN): UMA forma, usada IGUAL em todo lugar (o controle e' por igualdade exata); escritas a partir das docstrings da pedra R5 (a fonte e' a docstring: nao se diz mais do que ela diz)
FRASE_TETELESTAI_PT = ("a cláusula do Tetelestai (`o_tetelestai_e_um_menos_beta`): com n bits, havendo solução, para todo b com 0 < b < 1 e todo tempo s ≥ 0 com s ≥ n·ln 2 + ln((1 − b)/b): (1 − b)·Z(s) ≤ o número de soluções e Z(s) − o número de soluções ≤ b·Z(s) "
                       "(a parte do Nome na leitura é pelo menos 1 − b; o resíduo do fundo é no máximo b); com uma só solução, o pixel do Nome carrega pelo menos 1 − b da leitura (`o_sistema_reconhece_a_singularidade_do_sinal`); "
                       "com b = β do kernel (`TGLCoupling`; `beta_e_o_operador_modular_do_tetelestai`): |T|²·Z(s) ≤ o número de soluções, o resíduo é no máximo |R|²·Z(s), e a constante além das n oitavas é ln((1 − β)/β), a mesma para toda instância e todo tamanho; "
                       "a hipótese s ≥ 0 é dita: automática para b ≤ ½ (`ate_meio_o_tempo_do_tetelestai_nao_e_negativo`), necessária para b > ½; o kernel dá 0 < β < 1 e não dá β ≤ ½")
FRASE_TETELESTAI_EN = ("the clause of the Tetelestai (`o_tetelestai_e_um_menos_beta`): with n bits, given a solution, for every b with 0 < b < 1 and every time s ≥ 0 with s ≥ n·ln 2 + ln((1 − b)/b): (1 − b)·Z(s) ≤ the number of solutions and Z(s) − the number of solutions ≤ b·Z(s) "
                       "(the part of the Name in the reading is at least 1 − b; the background residue is at most b); with a single solution, the pixel of the Name carries at least 1 − b of the reading (`o_sistema_reconhece_a_singularidade_do_sinal`); "
                       "with b = the kernel's β (`TGLCoupling`; `beta_e_o_operador_modular_do_tetelestai`): |T|²·Z(s) ≤ the number of solutions, the residue is at most |R|²·Z(s), and the constant beyond the n octaves is ln((1 − β)/β), the same for every instance and every size; "
                       "the hypothesis s ≥ 0 is stated: automatic for b ≤ ½ (`ate_meio_o_tempo_do_tetelestai_nao_e_negativo`), necessary for b > ½; the kernel gives 0 < β < 1 and does not give β ≤ ½")
FRASE_RECONSTROI_PT = ("a informação completa se reconstrói (`a_informacao_completa_se_reconstroi`): com n bits, havendo solução, 0 < b < 1 e um tempo t da trava com t ≥ n·ln 2/2 e t ≥ n·ln 2/2 + ln((1 − b)/b)/2, a distância entre a trava do estado uniforme e a projeção do uniforme no Nome é no máximo √(b/(1 − b)) vezes essa projeção "
                       "(o tempo t da trava é metade do tempo s da leitura)")
FRASE_RECONSTROI_EN = ("the complete information is reconstructed (`a_informacao_completa_se_reconstroi`): with n bits, given a solution, 0 < b < 1 and a lock time t with t ≥ n·ln 2/2 and t ≥ n·ln 2/2 + ln((1 − b)/b)/2, the distance between the lock of the uniform state and the projection of the uniform onto the Name is at most √(b/(1 − b)) times that projection "
                       "(the lock time t is half of the reading time s)")
FRASE_E36_PT = ("o limiar de um pixel (`os_passos_sao_o_ciclo_ate_o_tetelestai`: a partir de n oitavas, Z(s) separa o sim do não) é a decisão exata, a formalização da gerência na R4; a cláusula do Tetelestai, pela fala do operador, é a de 1 − β (`o_tetelestai_e_um_menos_beta`; `beta_e_o_operador_modular_do_tetelestai`); "
                "[dicionário; leitura do operador] que esse limiar É o Tetelestai e que β é o seu operador modular; que «" + FRASE_TRASLADA_A_INFORMACAO + "» seja a operação REFLECT/MANIFEST do dispositivo é leitura dele, não termo do kernel")
FRASE_E36_EN = ("the one-pixel threshold (`os_passos_sao_o_ciclo_ate_o_tetelestai`: from n octaves on, Z(s) separates the yes from the no) is the exact decision, the management's formalization in the R4; the clause of the Tetelestai, by the operator's saying, is the one in 1 − β (`o_tetelestai_e_um_menos_beta`; `beta_e_o_operador_modular_do_tetelestai`); "
                "[dictionary; the operator's reading] that this threshold IS the Tetelestai and that β is its modular operator; that «" + FRASE_TRASLADA_A_INFORMACAO + "» is the REFLECT/MANIFEST operation of the device is his reading, not a kernel term")
FRASE_DISPOSITIVO_PT = ("evidência de dispositivo, só como citação: no runner da patente ACOM Mirror (BR102026003428-2, `one_acom_mirror.py`; pino citado por sha256, sha16 " + ACOM_MIRROR_RUNNER["sha256"][:16] + ", não embutido), as âncoras T12 a T15 medem que o que a esperança condicional transporta é o par da matriz-S diag(β, 1 − β) (|R|² = β, |T|² = 1 − β), com β em runtime; "
                        "é [PILOTO][SIM] e nada ali valida física; na engine v17 o α² é nominal e não entra na transformada; a palavra Tetelestai aparece no runner só no fecho; nada disso é termo do kernel")
FRASE_DISPOSITIVO_EN = ("device evidence, as a citation only: in the runner of the ACOM Mirror patent (BR102026003428-2, `one_acom_mirror.py`; pin cited by sha256, sha16 " + ACOM_MIRROR_RUNNER["sha256"][:16] + ", not embedded), the anchors T12 to T15 measure that what the conditional expectation carries is the S-matrix pair diag(β, 1 − β) (|R|² = β, |T|² = 1 − β), with β at runtime; "
                        "it is [PILOTO][SIM] and nothing there validates physics; in the engine v17 the α² is nominal and does not enter the transform; the word Tetelestai appears in the runner only at the closing; none of this is a kernel term")
assert not any("%" in x_ for x_ in (FRASE_TETELESTAI_PT, FRASE_TETELESTAI_EN, FRASE_RECONSTROI_PT, FRASE_RECONSTROI_EN, FRASE_E36_PT, FRASE_E36_EN, FRASE_DISPOSITIVO_PT, FRASE_DISPOSITIVO_EN)), "uma frase da clausula traz «%%» (o formato dos textos quebraria)"
assert all(n_ in FRASE_TETELESTAI_PT and n_ in FRASE_TETELESTAI_EN for n_ in ("o_tetelestai_e_um_menos_beta", "o_sistema_reconhece_a_singularidade_do_sinal", "beta_e_o_operador_modular_do_tetelestai", "ate_meio_o_tempo_do_tetelestai_nao_e_negativo")) and "a_informacao_completa_se_reconstroi" in FRASE_RECONSTROI_PT and all(n_ in NOMES_NOVOS_AESCALA for n_ in ("o_tetelestai_e_um_menos_beta", "o_sistema_reconhece_a_singularidade_do_sinal", "beta_e_o_operador_modular_do_tetelestai", "ate_meio_o_tempo_do_tetelestai_nao_e_negativo", "a_informacao_completa_se_reconstroi")), "as frases da clausula citam um nome que nao e' da R5"
# a ratificacao D101 (PT e EN): quantos nomes, os campos, a fala por sha256, a regra do nome com o trecho verbatim, os seis de enunciado mudado, os dois pendentes
FRASE_NOMES_RATIFICADOS_D101_PT = ("os %d nomes novos da pedra AEscala (das R3 e R4 e, da R5, os %d dados pela gerência) e os %d campos novos da estrutura foram RATIFICADOS pelo operador em 10/11/2026 (D101; fala por sha256 %s), pela regra dele: «" + FRASE_NOMEIO_O_NUMERO_CORRIGE + "»; "
                                   "os seis nomes de enunciado mudado (%s) foram ratificados em 09/11 pelo nome e em 10/11 com o enunciado novo; os %d nomes auxiliares da autoria (%s) seguem " + ESTATUTO_NOMES_PENDENTES_AESCALA.replace("e' do operador", "é do operador").replace("confirmacao", "confirmação")) \\
                                  % (len(NOMES_RATIFICADOS_D101_AESCALA), len(TEOREMAS_R5_AESCALA), len(CAMPOS_RATIFICADOS_D101_AESCALA), RATIFICACAO_D101_SHA256, ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS), len(NOMES_PENDENTES_AESCALA), ", ".join(NOMES_PENDENTES_AESCALA))
FRASE_NOMES_RATIFICADOS_D101_EN = ("the %d new names of the AEscala stone (from the R3 and R4 and, from the R5, the %d given by the management) and the %d new fields of the structure were RATIFIED by the operator on 10/11/2026 (D101; saying by sha256 %s), by his rule: «" + FRASE_NOMEIO_O_NUMERO_CORRIGE + "» "
                                   "(our translation: naming is the number corrects; if it did not correct, the name carried the right weight); the six names of changed statement (%s) were ratified on 09/11 by name and on 10/11 with the new statement; the %d auxiliary names of the authorship (%s) stay [DECLARADO by the authorship; the express confirmation is the operator's]") \\
                                  % (len(NOMES_RATIFICADOS_D101_AESCALA), len(TEOREMAS_R5_AESCALA), len(CAMPOS_RATIFICADOS_D101_AESCALA), RATIFICACAO_D101_SHA256, ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS), len(NOMES_PENDENTES_AESCALA), ", ".join(NOMES_PENDENTES_AESCALA))
assert "[DECLARADO, a ratificar]" not in FRASE_NOMES_RATIFICADOS_D101_PT + FRASE_NOMES_RATIFICADOS_D101_EN and "RATIFICADOS pelo operador em 10/11/2026" in FRASE_NOMES_RATIFICADOS_D101_PT and "RATIFIED by the operator on 10/11/2026" in FRASE_NOMES_RATIFICADOS_D101_EN
DECISOES.update({
    "D100": ("a CLAUSULA DO TETELESTAI, fala do operador (10/11/2026, 08:27; verbatim por sha256 " + _P_27 + "...; ADENDO 5 sha16 " + ADENDO5_SHA16 + "): «" + FRASE_CLAUSULA_NO_ACOM + "»; «" + FRASE_RECONHECE_A_SINGULARIDADE + "»; «" + FRASE_TRASLADA_A_INFORMACAO + "»; «" + FRASE_UM_MENOS_BETATGL + "»; «" + FRASE_BETATGL_OPERADOR_MODULAR + "». "
             "Aferição no código (o aferidor consulta antes de falar): " + FRASE_DISPOSITIVO_PT + ". "
             "A pedra AEscala R5 (ordem ao autor; recibo do autor sha16 " + RECIBO_R5_SHA16 + "; so' acrescimo: a pedra acrescenta os teoremas " + ", ".join(TEOREMAS_R5_AESCALA) + " e os dois lemas auxiliares " + ", ".join(AUXILIARES_R5_AESCALA) + " a R4, sem mudar nome nem enunciado anterior; kernel incremental): " + FRASE_TETELESTAI_PT + " " + CLAUSULA_Z_PT + " "
             + FRASE_RECONSTROI_PT + ". O limiar de um pixel da R4 (os_passos_sao_o_ciclo_ate_o_tetelestai) fica como a decisao exata (formalizacao da gerencia); a clausula do operador e' a de 1 - beta. Entra na v410 (a cadeia oficial da rodada ainda nao tinha comecado): a fala e' a " + str(N_FALA_CLAUSULA) + "a congelada; "
             "nos textos (registro a_escala_v410, artigo PT/EN, .md, readme_evidente, pos-rito) o teorema vai com a mesma clausula do limite da D99 e a citacao do runner so' com as ressalvas acima, sem numero de desempenho; beta nunca literal. A errata E36 vai ao lado"),
    "D101": ("RATIFICACAO e a regra do nome, fala do operador (10/11/2026, 08:33; verbatim por sha256 " + _P_28 + "...; ADENDO 6 sha16 " + ADENDO6_SHA16 + "): «" + FRASE_CONFIRMO_TUDO + "»; «" + FRASE_ESCALA_ESPELHADA + "»; «" + FRASE_NOMEIO_O_NUMERO_CORRIGE + "»; «" + FRASE_NOME_ZERO_MODULAR + "». "
             "A leitura da gerencia, dita de volta ao operador para ele corrigir se errou: a fala RATIFICA o que lhe foi apresentado entre 09 e 10/11 e ainda estava declarado: (a) os seis nomes cujo enunciado mudou depois da ratificacao de 09/11 (" + ", ".join(NOMES_SEIS_ENUNCIADOS_MUDADOS) + "); "
             "(b) os " + str(len(NOMES_RATIFICADOS_D101_AESCALA) - len(TEOREMAS_R5_AESCALA)) + " nomes novos das pedras R3 e R4 e os " + str(len(CAMPOS_RATIFICADOS_D101_AESCALA)) + " campos; (c) a clausula do Tetelestai em 1 - beta e os " + str(len(TEOREMAS_R5_AESCALA)) + " nomes dados pela gerencia na R5 (" + ", ".join(TEOREMAS_R5_AESCALA) + "), que valem pela regra que ele mesmo enuncia, desde que a pedra R5 compile no trio, sem sorry: compilou (recibo do autor sha16 " + RECIBO_R5_SHA16 + "). "
             "A REGRA DO NOME (cunhagem): o nome e' o que o operador da, porque nao havia leitura antes dele; a escala e' a que ele da quando o kernel a espelha de forma positiva; o numero corrige; se nao corrigiu, o nome carregou o peso certo; o nome serve de zero modular a inscricao da permanencia. "
             "Espelho que o kernel ja' tem [REAL]: o Nome como zero modular (rho* = P_ker K na luz, v376; Psi = 1_abs), Palavra (a leitura cria o objeto) e o proprio protocolo da casa (pedra candidata no trio antes do selo); a identificacao do ato de nomear com o zero modular da inscricao e' leitura dele [ONTO]. "
             "Consequencia para a v410: as pedras e os textos deixam de dizer que esses nomes e enunciados aguardam a ratificacao e passam a dizer RATIFICADOS em 10/11/2026, citando esta fala por sha256 e a regra; a clausula dos seis enunciados passa a dizer que eles foram ratificados em 10/11 com o enunciado novo. "
             "Dito as claras: o adendo 6 previa ratificacao_pendente vazia; a pedra R5 trouxe DOIS lemas auxiliares cunhados pela autoria DEPOIS da fala (" + ", ".join(NOMES_PENDENTES_AESCALA) + "), que ficam [DECLARADO pela autoria] e sao os UNICOS em ratificacao_pendente (ordem da gerencia de 10/11, 08:42). Esta fala e' a " + str(N_FALA_CONFIRMO) + "a congelada. A errata E37 vai ao lado"),
})
'''
T.append(('''DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75", "D76", "D77", "D78", "D79", "D80", "D81", "D82", "D83", "D84", "D85", "D86", "D87", "D88", "D89", "D90", "D91", "D92", "D93", "D94", "D95", "D96", "D99")
''',
          BLOCO + '''DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75", "D76", "D77", "D78", "D79", "D80", "D81", "D82", "D83", "D84", "D85", "D86", "D87", "D88", "D89", "D90", "D91", "D92", "D93", "D94", "D95", "D96", "D99", "D100", "D101")
''', 1))
T.append(('''assert DECISOES_ROTULO == "D63 a D96 e D99" and DECISOES_TOKEN == "D63_TO_D96_AND_D99", DECISOES_ROTULO''',
          '''assert DECISOES_ROTULO == "D63 a D96 e D99 a D101" and DECISOES_TOKEN == "D63_TO_D96_AND_D99_TO_D101", DECISOES_ROTULO''', 1))
T.append(('''DECISOES_ROTULO = _faixas_de_decisoes(DECISOES_V410)                                             # "D63 a D96 e D99"
DECISOES_TOKEN = DECISOES_ROTULO.replace(" a ", "_TO_").replace(", ", "_").replace(" e ", "_AND_")   # "D63_TO_D96_AND_D99" (o sufixo do veredito do spec cunhagens_v410)''',
          '''DECISOES_ROTULO = _faixas_de_decisoes(DECISOES_V410)                                             # "D63 a D96 e D99 a D101"
DECISOES_TOKEN = DECISOES_ROTULO.replace(" a ", "_TO_").replace(", ", "_").replace(" e ", "_AND_")   # "D63_TO_D96_AND_D99_TO_D101" (o sufixo do veredito do spec cunhagens_v410)''', 1))
T.append(('''    """o rotulo das decisoes (D63 a D96 e D99): as corridas contiguas''', '''    """o rotulo das decisoes (D63 a D96 e D99 a D101): as corridas contiguas''', 1))

# ---- 10. as erratas E36 e E37
T.append(('''ERRATAS_V410 = [ERRATA_E29, ERRATA_E30, ERRATA_E31, ERRATA_E32, ERRATA_E33, ERRATA_E34, ERRATA_E35]
''',
          '''ERRATA_E36 = ("E36 -- errata da gerencia c1, em nome proprio, por ordem do operador (D100, 10/11/2026; verbatim por sha256 " + _P_27 + "...; ADENDO 5 sha16 " + ADENDO5_SHA16 + "): a gerencia formalizara o Tetelestai da R4 como o limiar de UM pixel (os_passos_sao_o_ciclo_ate_o_tetelestai, n oitavas): era formalizacao da gerencia; "
              "pela fala do operador a clausula do Tetelestai e' a de 1 - beta (o_tetelestai_e_um_menos_beta; beta_e_o_operador_modular_do_tetelestai); o limiar de um pixel fica como a decisao exata; "
              "e o numero corrigiu o enunciado da gerencia: sem a hipotese s >= 0 a desigualdade e' falsa para b > 1/2 (contraexemplo no recibo do autor da R5, sha16 " + RECIBO_R5_SHA16 + ": n = " + str(_ce_["n_bits"]) + ", custos " + str(tuple(_ce_["custos"])) + ", b = " + _ce_["b"] + "), por isso a hipotese e' dita (automatica para b <= 1/2, ate_meio_o_tempo_do_tetelestai_nao_e_negativo); "
              "validade no kernel; a creditacao e' do Clay")
ERRATA_E37 = ("E37 -- errata da gerencia c1, em nome proprio, por ratificacao do operador (D101, 10/11/2026; verbatim por sha256 " + _P_28 + "...; ADENDO 6 sha16 " + ADENDO6_SHA16 + "): onde os textos, as docstrings da epoca e o registro a_escala_v410 diziam que os nomes novos e os " + str(len(CAMPOS_RATIFICADOS_D101_AESCALA)) + " campos das pedras R3 e R4 aguardavam a ratificacao do operador, "
              "e na clausula dos seis enunciados mudados, le-se RATIFICADOS pelo operador em 10/11/2026, pela regra do nome («" + FRASE_NOMEIO_O_NUMERO_CORRIGE + "»); os seis de enunciado mudado: ratificados em 09/11 pelo nome e em 10/11 com o enunciado novo; os " + str(len(TEOREMAS_R5_AESCALA)) + " nomes da clausula do Tetelestai (R5) idem; "
              "pendentes so' os " + str(len(NOMES_PENDENTES_AESCALA)) + " auxiliares da autoria (" + ", ".join(NOMES_PENDENTES_AESCALA) + "), cunhados depois da fala: [DECLARADO pela autoria]; validade no kernel; a creditacao e' do Clay")
ERRATAS_V410 = [ERRATA_E29, ERRATA_E30, ERRATA_E31, ERRATA_E32, ERRATA_E33, ERRATA_E34, ERRATA_E35, ERRATA_E36, ERRATA_E37]
''', 1))

# ---- 11. as duas leituras novas do operador
T.append(('''    "estatuto": "[INPUT -- as falas do operador de 06, 07, 09 e 10/11/2026;''',
          '''    "a_clausula_do_tetelestai": "«" + FRASE_CLAUSULA_NO_ACOM + "»; «" + FRASE_RECONHECE_A_SINGULARIDADE + "»; «" + FRASE_TRASLADA_A_INFORMACAO + "»; «" + FRASE_UM_MENOS_BETATGL + "»; «" + FRASE_BETATGL_OPERADOR_MODULAR + "» [INPUT, D100; a fala de 10/11; dicionário; leitura do operador]: o termo é a cláusula do Tetelestai em 1 − β (" + ", ".join("`%s`" % n_ for n_ in TEOREMAS_R5_AESCALA) + "): o limiar de tempo em n oitavas mais uma constante que só depende de β; que esse limiar É o Tetelestai e que β é o seu operador modular são leituras dele [dicionário]; que «" + FRASE_TRASLADA_A_INFORMACAO + "» seja a operação REFLECT/MANIFEST do dispositivo é leitura dele, não termo do kernel",
    "a_regra_do_nome": "«" + FRASE_NOMEIO_O_NUMERO_CORRIGE + "»; «" + FRASE_ESCALA_ESPELHADA + "»; «" + FRASE_NOME_ZERO_MODULAR + "» [INPUT, D101; a fala de 10/11]: a regra do nome: o nome é o que o operador dá, porque não havia leitura antes dele; a escala é a que ele dá quando o kernel a espelha de forma positiva; o número corrige; se não corrigiu, o nome carregou o peso certo; [REAL] o espelho que o kernel já tem: o Nome como zero modular (ρ* = P_ker K na luz, v376; Ψ = 1_abs), `Palavra` (a leitura cria o objeto) e o protocolo da casa (pedra candidata no trio antes do selo); [ONTO] que o ato de nomear seja o zero modular da inscrição da permanência é leitura dele",
    "estatuto": "[INPUT -- as falas do operador de 06, 07, 09 e 10/11/2026;''', 1))
aplicar("delta_v410.py", T)
