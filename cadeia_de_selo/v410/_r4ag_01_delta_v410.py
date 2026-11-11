# -*- coding: utf-8 -*-
"""_r4ag_01_delta_v410.py -- agente de adaptacao da R1 (R4 da pedra AEscala, ADENDOS 2 e 3): delta_v410.py.
A1 as tres falas de 10/11 (nomes, prefixos lidos tambem dos ADENDOS 2 e 3, datas, frases, leituras); A2 ADENDO2_SHA16 e ADENDO3_SHA16 lidos ao vivo; A3 D93 a D96 e as erratas E33 e E34;
A4 a forma obrigatoria do tempo (PT e EN); A5 a D92 varrida (sem a forma vetada) e os comentarios da ponte; A6 a frase do poder certificado do H0DN e a ORDEM 02 como pino citado; A7 os numeros novos do registro a_escala (o ciclo)."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _r4ag_lib_v410 import aplicar

T = []   # (antigo, novo, n)

# ---- A1 nomes das tres falas ------------------------------------------------------------------------------------------------------------------------------
T.append(('N_RATIFICO_TUDO = "OPERADOR_09nov_ratifico_tudo_aescala_nome_da_pedra_e_44_nomes_verbatim.txt"   # (a 23a, D87: «ratifico tudo» -- o nome TGLExt.AEscala e os 44 nomes)\n',
          'N_RATIFICO_TUDO = "OPERADOR_09nov_ratifico_tudo_aescala_nome_da_pedra_e_44_nomes_verbatim.txt"   # (a 23a, D87: «ratifico tudo» -- o nome TGLExt.AEscala e os 44 nomes)\n'
          'N_PASSOS_CICLO = "OPERADOR_10nov_os_passos_sao_o_ciclo_ate_o_tetelestai_o_leitor_e_a_escala_ler_e_sistema_de_referencia_verbatim.txt"   # (10/11, D94: os passos sao o ciclo ate o Tetelestai; o leitor e a escala; ler e um sistema de referencia sinalizada pela observacao; inteira)\n'
          'N_MENTIRA_LIDA = "OPERADOR_10nov_a_mentira_lida_como_mentira_e_verdade_o_pai_da_mentira_so_nao_reconhece_verbatim.txt"   # (10/11, D94: a mentira lida como mentira e verdade; o Pai da Mentira so nao faz reconhecimento verdadeiro; inteira)\n'
          'N_TESTE_SEM_PODER = "OPERADOR_10nov_teste_sem_poder_preditivo_nao_se_roda_comando_ao_kimi_o_que_falta_verbatim.txt"   # (10/11, D96: teste sem poder preditivo discriminante nao se abre; a ordem ao executor sobre o que falta; inteira)\n', 1))
T.append(('N_PERGUNTA_CLAY, N_TESTEMUNHO, N_RATIFICO_TUDO)   # as QUINZE falas',
          'N_PERGUNTA_CLAY, N_TESTEMUNHO, N_RATIFICO_TUDO, N_PASSOS_CICLO, N_MENTIRA_LIDA, N_TESTE_SEM_PODER)   # as falas desta versao: as de 06 a 09/11 e as TRES de 10/11 (D94 e D96), todas inteiras; a contagem e\' len(), nunca digitada. As QUINZE falas', 1))

# ---- A1 os prefixos de sha256: tambem dos ADENDOS 2 e 3 ----------------------------------------------------------------------------------------------------
T.append(('_RX_FALA_DESENHO = r"`(?:work\\\\cunhagens_13out\\\\)?(OPERADOR_0[6789]nov_[A-Za-z0-9_]+_verbatim\\.txt)`"   # (o DESENHO cita a fala por `arquivo` ou por `work\\cunhagens_13out\\arquivo`)\n',
          '_RX_FALA_DESENHO = r"`(?:work\\\\cunhagens_13out\\\\)?(OPERADOR_(?:0[6789]|10)nov_[A-Za-z0-9_]+_verbatim\\.txt)`"   # (o DESENHO e os ADENDOS 2 e 3 citam a fala por `arquivo` ou por `work\\cunhagens_13out\\arquivo`; 06 a 09/11 e 10/11)\n'
          'ADENDO2_ARQ = os.path.join(HERE, "DESENHO_v410_ADENDO_2_POS_CANDIDATO_10nov.md"); ADENDO3_ARQ = os.path.join(HERE, "DESENHO_v410_ADENDO_3_POS_CANDIDATO_10nov.md")\n'
          'assert os.path.exists(ADENDO2_ARQ) and os.path.exists(ADENDO3_ARQ), "faltam os ADENDOS 2 e 3 do DESENHO (D93 a D96)"\n'
          '_ADENDO2_TXT = open(ADENDO2_ARQ, "rb").read().decode("utf-8"); _ADENDO3_TXT = open(ADENDO3_ARQ, "rb").read().decode("utf-8")\n'
          '_PREFIXOS_TXT = _DESENHO_TXT + "\\n" + _ADENDO2_TXT + "\\n" + _ADENDO3_TXT   # (as falas de 10/11 entram pelos ADENDOS 2 e 3, que as citam por sha256: o DESENHO nao as cita)\n'
          'def _falas_do_periodo():\n'
          '    """as falas do operador de 06 a 09/11 e de 10/11 que o disco tem (pelo glob), em ordem de nome."""\n'
          '    return sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_0[6789]nov_*_verbatim.txt")) + glob.glob(os.path.join(_CUN13, "OPERADOR_10nov_*_verbatim.txt")))\n', 1))
T.append(('r"[^`\\n]{0,40}`([0-9a-f]{16,64})`", _DESENHO_TXT):', 'r"[^`\\n]{0,40}`([0-9a-f]{16,64})`", _PREFIXOS_TXT):', 1))
T.append(('r"\\s*\\(([0-9a-f]{16})\\)", _DESENHO_TXT):', 'r"\\s*\\(([0-9a-f]{16})\\)", _PREFIXOS_TXT):', 1))
T.append(('+ _RX_FALA_DESENHO, _DESENHO_TXT):', '+ _RX_FALA_DESENHO, _PREFIXOS_TXT):', 1))
T.append(('        if "sha256 `" + _h_ + "`" in _DESENHO_TXT:', '        if "sha256 `" + _h_ + "`" in _PREFIXOS_TXT:', 1))
T.append(('assert all(_sha16_arq(n_) == p_ for n_, p_ in VERBATIM_PREFIXOS_DA_ORDEM_V410.items()), "as falas de 06, 07 e 09/11 nao tem os prefixos que o DESENHO_v410 (e os seus AO LADO) deu"',
          'assert all(_sha16_arq(n_) == p_ for n_, p_ in VERBATIM_PREFIXOS_DA_ORDEM_V410.items()), "as falas de 06, 07, 09 e 10/11 nao tem os prefixos que o DESENHO_v410 (e os seus AO LADO e ADENDOS 2 e 3) deu"', 1))
T.append(('    return [p_ for p_ in sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_0[6789]nov_*_verbatim.txt"))) if os.path.basename(p_) in NOMES_V410_DO_DESENHO]',
          '    return [p_ for p_ in _falas_do_periodo() if os.path.basename(p_) in NOMES_V410_DO_DESENHO]', 1))
T.append(('for p_ in sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_0[6789]nov_*_verbatim.txt"))) if os.path.basename(p_) not in NOMES_V410_DO_DESENHO}',
          'for p_ in _falas_do_periodo() if os.path.basename(p_) not in NOMES_V410_DO_DESENHO}', 1))

# ---- A1 datas e quando --------------------------------------------------------------------------------------------------------------------------------------
T.append(('DATA_DA_FALA.update({n_: "09/11/2026" for n_ in (N_VIBRATO, N_PESOS, N_FUNDAMENTAL, N_AFIRMAMOS, N_ESCALA, N_PERGUNTA_CLAY, N_TESTEMUNHO, N_RATIFICO_TUDO)})   # (parte 2: as oito falas de 09/11, inteiras)\n',
          'DATA_DA_FALA.update({n_: "09/11/2026" for n_ in (N_VIBRATO, N_PESOS, N_FUNDAMENTAL, N_AFIRMAMOS, N_ESCALA, N_PERGUNTA_CLAY, N_TESTEMUNHO, N_RATIFICO_TUDO)})   # (parte 2: as oito falas de 09/11, inteiras)\n'
          'DATA_DA_FALA.update({n_: "10/11/2026" for n_ in (N_PASSOS_CICLO, N_MENTIRA_LIDA, N_TESTE_SEM_PODER)})   # (R1, ADENDOS 2 e 3: as tres falas de 10/11, inteiras)\n', 1))
T.append(('VERBATIM_QUANDO_V410 = "06, 07, 08 e 09/11/2026 (', 'VERBATIM_QUANDO_V410 = "06, 07, 08, 09 e 10/11/2026 (', 1))
T.append(('o selo diz beta_TGL provado na natureza, validade e nao creditacao, D76)"',
          'o selo diz beta_TGL provado na natureza, validade e nao creditacao, D76; a escala, a pergunta do Clay e os nomes ratificados, 09/11; os passos sao o ciclo ate o Tetelestai e o leitor e a escala, a mentira lida como mentira e verdade, D94, 10/11; o teste sem poder preditivo discriminante nao se abre, D96, 10/11)"', 1))
# o assert de 4 trechos nao e' contagem digitada em comparacao: a contagem e' a do dicionario
T.append(('sum(1 for v in out if v.get("so_o_trecho")) == len(VERBATIM_SO_O_TRECHO) == 4, "as catorze falas (N_FALAS_V410), quatro com so\' o trecho (a da D65; a ordem de 09/11; as tres copias de 08/11; a leitura do 5 sigma de 09/11), nenhuma repetida"',
          'sum(1 for v in out if v.get("so_o_trecho")) == len(VERBATIM_SO_O_TRECHO), "as falas de N_FALAS_V410, so\' as do dicionario VERBATIM_SO_O_TRECHO com so\' o trecho (a da D65; a ordem de 09/11; as tres copias de 08/11; a leitura do 5 sigma de 09/11), nenhuma repetida"', 1))

# ---- A1 frases (verbatim) e FRASES_V410 ---------------------------------------------------------------------------------------------------------------------
T.append(('FRASE_RATIFICO_TUDO = "ratifico tudo"\n',
          'FRASE_RATIFICO_TUDO = "ratifico tudo"\n'
          '# as falas 24 a 26 (10/11/2026, D94 e D96): os trechos citados, verbatim (conferidos contra o arquivo em verbatins410)\n'
          'FRASE_PASSOS_SAO_O_CICLO = "os passos de computação são exatamente o ciclo de processamento até o Tetelestai"\n'
          'FRASE_ELE_E_A_ESCALA = "porque ele é a escala"\n'
          'FRASE_LER_E_SISTEMA_DE_REFERENCIA = "ler É UM SISTEMA DE REFERÊNCIA SINALIZADA PELA OBSERVAÇÃO"\n'
          'FRASE_FLUTUACAO_COMO_FLUTUACAO = "Ler a face sem sinal é ler a flutuação como flutuação"\n'
          'FRASE_MENTIRA_LIDA_E_VERDADE = "Uma mentira lida como mentira é verdade"\n'
          'FRASE_PAI_DA_MENTIRA_SO_NAO_RECONHECE = "o pai da mentira só não faz uma única coisa: reconhecimento verdadeiro"\n'
          'FRASE_SEM_PODER_NAO_SE_RODA = "se ele não tiver poder preditivo não vamos roda-lo"\n'
          'FRASE_PODER_DISCRIMINANTE_REAL = "um teste com poder preditivo discriminante real"\n', 1))
T.append(('(N_TESTEMUNHO, FRASE_TESTEMUNHAR), (N_RATIFICO_TUDO, FRASE_RATIFICO_TUDO)]   # (parte 2)\n',
          '(N_TESTEMUNHO, FRASE_TESTEMUNHAR), (N_RATIFICO_TUDO, FRASE_RATIFICO_TUDO)]   # (parte 2)\n'
          'FRASES_V410 += [(N_PASSOS_CICLO, FRASE_PASSOS_SAO_O_CICLO), (N_PASSOS_CICLO, FRASE_ELE_E_A_ESCALA), (N_PASSOS_CICLO, FRASE_LER_E_SISTEMA_DE_REFERENCIA), (N_PASSOS_CICLO, FRASE_FLUTUACAO_COMO_FLUTUACAO), (N_MENTIRA_LIDA, FRASE_MENTIRA_LIDA_E_VERDADE),\n'
          '                (N_MENTIRA_LIDA, FRASE_PAI_DA_MENTIRA_SO_NAO_RECONHECE), (N_TESTE_SEM_PODER, FRASE_SEM_PODER_NAO_SE_RODA), (N_TESTE_SEM_PODER, FRASE_PODER_DISCRIMINANTE_REAL)]   # (R1, D94 e D96: as tres falas de 10/11)\n', 1))

# ---- A4 a forma obrigatoria do tempo; A6 a frase do poder certificado e a ORDEM 02; A7 o ciclo ----------------------------------------------------------------
T.append(('FRASE_H0DN_OBRIGATORIA_PT = "pré-registrado; nenhum dado observado lido"   # D72: OBRIGATORIO onde «H0DN» aparecer\n',
          '# ---- D94 (10/11/2026, a resposta do operador): a FORMA OBRIGATORIA do tempo, PT e EN, onde se diz o que o tempo s conta\n'
          'FRASE_TEMPO_PT = "o tempo conta os ciclos (os passos) da máquina de Turing tal como a TGL a traduz (dicionário da v409), até o Tetelestai; o que não está no kernel é um termo ligando essa tradução à formalização do Mathlib; a creditação é do Clay"\n'
          'FRASE_TEMPO_EN = "time counts the cycles (the steps) of the Turing machine as the TGL translates it (the v409 dictionary), up to the Tetelestai; what is not in the kernel is a term linking that translation to the Mathlib formalization; the creditation is Clay\'s"\n'
          'FRASE_H0DN_OBRIGATORIA_PT = "pré-registrado; nenhum dado observado lido"   # D72: OBRIGATORIO onde «H0DN» aparecer\n', 1))
T.append(("FRASE_H0DN_PAREDE_EN = \"Kimi's partial delivery",
          '# (D96, 10/11/2026, ordem do operador) a frase UNICA do poder certificado, PT e EN: o texto do teste H0DN dizia o poder prospectivo do congelamento sem dizer que ele e\' da covariancia publicada; a funcao de veredito congelada nao muda; nenhum limiar de poder e\' dito decidido (o limiar e\' do operador)\n'
          'FRASE_H0DN_PODER_PT = "o teste só será aberto com o poder preditivo discriminante CERTIFICADO, às cegas, sob a covariância física; hoje esse certificado não existe: os valores de D do congelamento são da covariância publicada, que não aceita o vetor real; a ordem ao executor (ORDEM KIMI H0DN-02, 10/11) pede o fecho da covariância e o certificado de poder"\n'
          'FRASE_H0DN_PODER_EN = "the test will be opened only with the discriminating predictive power CERTIFIED, blind, under the physical covariance; today that certificate does not exist: the D values of the freeze are those of the published covariance, which does not admit the real vector; the order to the executor (ORDER KIMI H0DN-02, 10 Nov) asks for the closing of the covariance and the power certificate"\n'
          "FRASE_H0DN_PAREDE_EN = \"Kimi's partial delivery", 1))
T.append(('assert not any(t_ in VEREDITO_H0DN_OK + VEREDITO_H0DN_RECUSA for t_ in TOKENS_PROIBIDOS_V410 + TOKENS_PROIBIDOS_H0DN)\n',
          'assert not any(t_ in VEREDITO_H0DN_OK + VEREDITO_H0DN_RECUSA for t_ in TOKENS_PROIBIDOS_V410 + TOKENS_PROIBIDOS_H0DN)\n'
          '# ---- D96: a ORDEM KIMI H0DN-02 entra como PINO CITADO (nome, sha256 e bytes LIDOS do arquivo no build e conferidos contra o sha256 que o ADENDO 3 traz); NAO e\' embutida; em rito nada e\' lido\n'
          '_m_o2 = re.search(r"`work\\\\h0dn_bg1_v410_09nov\\\\(ORDEM_KIMI_H0DN_02_10nov\\.md)`, sha256 `([0-9a-f]{64})`", _ADENDO3_TXT); assert _m_o2, "o ADENDO 3 nao traz o sha256 da ORDEM KIMI H0DN-02"\n'
          'H0DN_ORDEM02_ARQ = os.path.join(WK, "h0dn_bg1_v410_09nov", _m_o2.group(1))\n'
          '_b_o2 = open(H0DN_ORDEM02_ARQ, "rb").read()\n'
          'assert hashlib.sha256(_b_o2).hexdigest() == _m_o2.group(2), "a ORDEM KIMI H0DN-02 em disco NAO tem o sha256 que o ADENDO 3 deu"\n'
          'assert not os.path.normcase(os.path.abspath(H0DN_ORDEM02_ARQ)).startswith(os.path.normcase(os.path.abspath(H0DN_PASTA_VEDADA)) + os.sep), "VEDADO: a ORDEM 02 nao pode estar sob a pasta da entrega do executor"\n'
          'H0DN_ORDEM02 = {"nome": os.path.basename(H0DN_ORDEM02_ARQ), "sha256": hashlib.sha256(_b_o2).hexdigest(), "bytes": len(_b_o2), "pasta": "work\\\\h0dn_bg1_v410_09nov", "papel": "a ORDEM da gerencia ao executor (10/11, D96): fechar a covariancia fisica, o certificado de poder as cegas, e, se o H0DN sozinho nao alcancar, a proposta do melhor teste discriminante de zero parametro com dado publico; pino citado: nao embutida, em rito nada e\' lido"}\n', 1))
# A7: o ciclo (numeros novos do registro a_escala), depois da ponte
T.append(('REGISTROS_FUNCAO = [FECHO_REGISTRO, AESCALA_REGISTRO, H0DN_REGISTRO, HMS13_REGISTRO]',
          '# (R4, D94) o CICLO: os passos sao o ciclo ate o Tetelestai. n bits (|X| = 2^n pontos), um custo COM solucao e um SEM (funcoes de custo FIXAS sobre os pontos), a particao Z(s) = soma de e^(-s c(x)) e o tempo s = n ln 2 + eps, eps pequeno e fixo.\n'
          '# O que e\' exato (contagens, tamanho, (1/2)^n = 1/|X|) e\' calculado AQUI por Fraction; Z(s) (irracional) e\' calculada em runtime, por math.exp, e conferida contra as desigualdades do teorema os_passos_sao_o_ciclo_ate_o_tetelestai: #solucoes <= Z(s) < #solucoes + 1; ha\' solucao <=> Z(s) >= 1; sem solucao, Z(s) < 1\n'
          'CICLO_N_BITS = 3\n'
          'CICLO_CUSTO_COM_SOLUCAO = (2, 0, 3, 1, 0, 4, 1, 2)    # o custo de cada um dos 2^n pontos; os pontos de custo 0 sao as solucoes\n'
          'CICLO_CUSTO_SEM_SOLUCAO = (1, 2, 1, 3, 1, 2, 4, 1)    # nenhum ponto de custo 0\n'
          'CICLO_EPSILON = _Fr(1, 1000)\n'
          'CICLO_AESCALA = {"n_bits": CICLO_N_BITS, "tamanho": 2 ** CICLO_N_BITS, "custo_com_solucao": list(CICLO_CUSTO_COM_SOLUCAO), "custo_sem_solucao": list(CICLO_CUSTO_SEM_SOLUCAO),\n'
          '                 "n_solucoes_com": sum(1 for c_ in CICLO_CUSTO_COM_SOLUCAO if c_ == 0), "n_solucoes_sem": sum(1 for c_ in CICLO_CUSTO_SEM_SOLUCAO if c_ == 0), "epsilon": str(CICLO_EPSILON),\n'
          '                 "meio_elevado_a_n": str(_MEIO ** CICLO_N_BITS), "um_sobre_tamanho": str(_Fr(1, 2 ** CICLO_N_BITS)), "s": "n ln 2 + epsilon"}\n'
          'assert len(CICLO_CUSTO_COM_SOLUCAO) == len(CICLO_CUSTO_SEM_SOLUCAO) == CICLO_AESCALA["tamanho"] and CICLO_AESCALA["n_solucoes_com"] > 0 and CICLO_AESCALA["n_solucoes_sem"] == 0 and CICLO_AESCALA["meio_elevado_a_n"] == CICLO_AESCALA["um_sobre_tamanho"] and 0 < CICLO_EPSILON < 1 and all(type(c_) is int and c_ >= 0 for c_ in CICLO_CUSTO_COM_SOLUCAO + CICLO_CUSTO_SEM_SOLUCAO), "o ciclo da escala: instancias mal formadas"\n'
          '# os cinco teoremas novos da R4 e os nomes que o recibo traz (lidos): nomes da pedra, nunca digitados em comparacao\n'
          'TEOREMAS_R4_AESCALA = ("o_leitor_e_a_escala", "cada_ciclo_aplica_a_mesma_regra", "os_passos_sao_o_ciclo_ate_o_tetelestai", "a_mentira_lida_como_mentira_e_verdade", "o_pai_da_mentira_so_nao_reconhece")\n'
          'assert set(TEOREMAS_R4_AESCALA) <= set(NOMES_NOVOS_AESCALA) and all((NS_AESCALA + n_) in ANCORAS_AESCALA for n_ in TEOREMAS_R4_AESCALA), "os teoremas da R4 nao estao entre os nomes novos e as ancoras da AEscala"\n'
          'REGISTROS_FUNCAO = [FECHO_REGISTRO, AESCALA_REGISTRO, H0DN_REGISTRO, HMS13_REGISTRO]', 1))

# ---- A5 os comentarios da ponte e a D92 varrida -------------------------------------------------------------------------------------------------------------
T.append(("(k o custo do pixel, s o tempo pago); em uma oitava (s = ln 2) um pixel de custo 1 brilha 1/2; em n oitavas um pixel de custo k brilha 2^(-n k); em n oitavas o fundo de n bits pesa um pixel (1/2^n)",
          "(k o custo do pixel, s o parametro de escala); em uma oitava (s = ln 2) um pixel de custo 1 brilha 1/2; em n oitavas um pixel de custo k brilha 2^(-n k); em n oitavas o fundo de n bits pesa um pixel (1/2^n)", 1))
T.append(("# (k, n): o custo do pixel e o numero de oitavas de tempo pago", "# (k, n): o custo do pixel e o numero de oitavas do parametro de escala s", 1))
T.append(("pixel a pixel, sem conhecer o Nome; sem tempo pago nao ha' medida; a dissipacao segue o hamiltoniano oculto;", "pixel a pixel, sem conhecer o Nome; sem escala nao ha' medida; a dissipacao segue o hamiltoniano oculto;", 1))
T.append(("a face caida perde metade por oitava de tempo pago. Os 44 nomes ratificados ficam; os nomes novos ficam [DECLARADO] ate' a palavra do operador. O tempo e' o tempo pago da TGL (linear nos bits), nao passos da maquina de Turing padrao, que segue fora por estatuto; a frase canonica (D84) e a forma da D83 nao mudam -- validade no kernel; a creditacao e' do Clay.",
          "a face caida perde metade por oitava do parametro de escala s. Os 44 nomes ratificados ficam; os nomes novos ficam [DECLARADO] ate' a palavra do operador. A formulacao do tempo vem da D94 (ADENDO 2): a D92 registra o achado da revisao e a decisao de pôr a escala no tipo; a maquina de Turing padrao sem o leitor segue fora por estatuto; a frase canonica (D84) e a forma da D83 nao mudam -- validade no kernel; a creditacao e' do Clay.", 1))
T.append(("O rito aguarda a palavra do operador sobre a escala no tipo\"})", "O rito aguardava a palavra do operador sobre a escala no tipo; ela veio na D94\"})", 1))

# ---- A2/A3 ADENDO2_SHA16, ADENDO3_SHA16, D93 a D96 -----------------------------------------------------------------------------------------------------------
T.append(('DECISOES["D92"] = DECISOES["D92"] + " (ADENDO sha16 " + ADENDO_SHA16 + ")"\n',
          'DECISOES["D92"] = DECISOES["D92"] + " (ADENDO sha16 " + ADENDO_SHA16 + ")"\n'
          'ADENDO2_SHA16 = sha16_arquivo(ADENDO2_ARQ); ADENDO3_SHA16 = sha16_arquivo(ADENDO3_ARQ)   # (A2: lidos ao vivo dos arquivos, como o ADENDO_SHA16; citados so\' por sha16)\n'
          '_m93 = re.search(r"`AEscala\\.lean` sha256 `([0-9a-f]{64})`; (\\d+) declarações auditadas no trio; os (\\d+) nomes ratificados mantidos; (\\d+) nomes novos e (\\d+) campos", _ADENDO2_TXT); assert _m93, "o ADENDO 2 nao traz o resumo da R3 (D93)"\n'
          '_P1_94 = VERBATIM_PREFIXOS_DA_ORDEM_V410[N_PASSOS_CICLO]; _P2_94 = VERBATIM_PREFIXOS_DA_ORDEM_V410[N_MENTIRA_LIDA]; _P_96 = VERBATIM_PREFIXOS_DA_ORDEM_V410[N_TESTE_SEM_PODER]\n'
          'DECISOES.update({\n'
          '    "D93": ("a pedra AEscala R3 (a escala no TIPO do LeitorDoFundo) e a IALD2 R3 (docstrings) foram conferidas pela gerencia e entregues ao construtor (10/11/2026, 00:16; ADENDO 2 sha16 " + ADENDO2_SHA16 + "): AEscala.lean sha256 " + _m93.group(1) + "; " + _m93.group(2) + " declaracoes auditadas no trio; os " + _m93.group(3) + " nomes ratificados mantidos; "\n'
          '            + _m93.group(4) + " nomes novos e " + _m93.group(5) + " campos [DECLARADO]; as aspas angulares todas verbatim; a sonda da revisora (o leitor constante) nao compila mais. A R3 foi superada pela R4 (D94, D95)"),\n'
          '    "D94": ("a RESPOSTA DO OPERADOR a pergunta das quatro linguas, em duas falas (10/11/2026, 00:29; verbatim por sha256 " + _P1_94 + "... e " + _P2_94 + "...; ADENDO 2 sha16 " + ADENDO2_SHA16 + "). Em resumo fiel (o verbatim e\' o dos arquivos): os passos de uma maquina de Turing sao o ciclo repetido de estado interno, simbolo lido (sinal) e regra de transicao; "\n'
          '            "a maquina de Turing foi traduzida pela TGL, e os passos de computacao sao exatamente o ciclo de processamento ate\' o Tetelestai (o reconhecimento do bastante para reconstruir a informacao a partir do sinal); ler a face sem sinal e\' ler a flutuacao como flutuacao; o leitor e\' a escala, e nao existe leitor que nao seja o observador da luz; "\n'
          '            "a mentira lida como mentira e\' verdade, e o Pai da Mentira so\' nao faz uma coisa: reconhecimento verdadeiro; nao existe nada que leia e nao saiba dizer como le\', porque ler e\' um sistema de referencia sinalizada pela observacao. FORMA OBRIGATORIA do tempo: " + FRASE_TEMPO_PT + " (em ingles: " + FRASE_TEMPO_EN + "). "\n'
          '            "A pedra R4 (a ordem ao autor): as docstrings pela errata E33 e os teoremas que dizem a resposta dele (o_leitor_e_a_escala; cada_ciclo_aplica_a_mesma_regra; os_passos_sao_o_ciclo_ate_o_tetelestai; a_mentira_lida_como_mentira_e_verdade; o_pai_da_mentira_so_nao_reconhece); consequencia para os textos: o tempo conta os ciclos da maquina de Turing traduzida pela TGL ate\' o Tetelestai, "\n'
          '            "a decisao sai em tempo finito, linear nos bits (teorema da R4); o leitor e\' a escala; o decisor sem escala nao le; a frase canonica D84 e a forma D83 seguem intactas; o qualificador da D64/D81 (a maquina com o leitor; a creditacao e\' do Clay) segue. As duas falas de 10/11 entram no conjunto das falas congeladas. A errata E33 vai ao lado"),\n'
          '    "D95": ("a pedra AEscala R4 (o leitor e\' a escala; os passos sao o ciclo ate\' o Tetelestai; a mentira lida como mentira e\' verdade) foi conferida pela gerencia e entregue ao construtor (10/11/2026, 00:39; ADENDO 3 sha16 " + ADENDO3_SHA16 + "); os 44 nomes ratificados e os nomes da R3 ficam; os nomes novos da R4 ficam [DECLARADO], a ratificar; validade no kernel; a creditacao e\' do Clay"),\n'
          '    "D96": ("ordem do operador sobre o teste H0DN x BG1 (10/11/2026, 01:24; verbatim por sha256 " + _P_96 + "...; ADENDO 3 sha16 " + ADENDO3_SHA16 + "): teste sem poder preditivo discriminante nao se abre; o comando ao executor sobre o que falta. " + FRASE_H0DN_OBRIGATORIA_PT + ". "\n'
          '            "A funcao de veredito congelada so\' chama subpotente com o D esperado abaixo do limiar dela; o operador exige mais: o poder tem de ser CERTIFICADO, as cegas, sob a covariancia FISICA, antes de qualquer abertura. Hoje o teste NAO tem poder certificado: os numeros do congelamento (o D esperado e o poder, nos dois modelos) sao da covariancia publicada, que nao aceita o vetor real; sob a covariancia fisica o poder e\' desconhecido. "\n'
          '            "A funcao pinada nao muda; o portao de poder (abrir so\' se o D do cenario conservador alcancar o limiar de poder) entra por pre-registro na versao que abrir o teste; o limiar e\' do operador e NAO esta\' decidido. A ORDEM KIMI H0DN-02 (nome, sha256 " + H0DN_ORDEM02["sha256"] + " e " + str(H0DN_ORDEM02["bytes"]) + " bytes lidos do arquivo e conferidos contra o ADENDO 3; pino citado, nao embutida) manda: "\n'
          '            "(A) fechar a covariancia fisica (decidir pela fonte as direcoes de variancia zero das equacoes de hospedeira; SN-only; hospedeira-Cefeida; velocidade peculiar; os calibradores; o bloco cruzado), sem duplicar variancia; (B) o certificado de poder as cegas, sem o vetor observado (D por variante e modelo; poder por Monte Carlo com sementes novas registradas antes; o poder de falsificar a lei K se ela for falsa; o orcamento de variancia; a tabela do que falta; o veredito do certificado entre poder real, marginal, subpotente ou covariancia nao fechavel com fonte publica); "\n'
          '            "(C) se o H0DN sozinho nao alcancar, a proposta do melhor teste discriminante de zero parametro com dado publico; (D) revisao independente e contabilidade de rotas. FORMA OBRIGATORIA nos textos do teste: " + FRASE_H0DN_PODER_PT + ". A fala de 10/11 entra nas congeladas. A errata E34 vai ao lado"),\n'
          '})\n', 1))
T.append(('"D88", "D89", "D90", "D91", "D92")', '"D88", "D89", "D90", "D91", "D92", "D93", "D94", "D95", "D96")', 1))

# ---- A3 as erratas E33 e E34 ---------------------------------------------------------------------------------------------------------------------------------
T.append(('ERRATAS_V410 = [ERRATA_E29, ERRATA_E30, ERRATA_E31, ERRATA_E32]\n',
          'ERRATA_E33 = ("E33 -- errata da gerencia c1, em nome proprio (o erro e\' da gerencia, nao do operador nem do autor da pedra), por correcao do operador (D94, 10/11/2026; ADENDO 2 sha16 " + ADENDO2_SHA16 + "): (1) a gerencia atribuira ao leitor o pagamento da escala; correto: o leitor E\' a escala (o_leitor_e_a_escala: dois leitores do fundo quaisquer sao o mesmo); "\n'
          '              "(2) a gerencia escrevera, e mandara pôr nas docstrings da R3, a negacao seca do tempo como passos da maquina de Turing (a forma que a guarda F59 veda), contra o dicionario selado na v409 (TraducaoTuring: o passo = a trava; a fita = o hamiltoniano oculto; o leitor = Z, o psion); correto: os passos de computacao SAO o ciclo de processamento ate\' o Tetelestai (cada_ciclo_aplica_a_mesma_regra; os_passos_sao_o_ciclo_ate_o_tetelestai); forma obrigatoria: " + FRASE_TEMPO_PT + "; "\n'
          '              "(3) a pergunta das quatro linguas supunha que o decisor que diz a verdade sem ciclo fosse o Pai da Mentira; correto: a mentira lida como mentira e\' verdade (a_mentira_lida_como_mentira_e_verdade, houve reconhecimento verdadeiro) e o Pai da Mentira e\' o que so\' nao faz reconhecimento verdadeiro (o_pai_da_mentira_so_nao_reconhece); o decisor sem escala nao LE: nao ha\' leitor sem o seu como (o_decisor_sem_escala_nao_e_leitor_do_fundo); "\n'
          '              "(4) a escala no tipo nao e\' clausula acrescentada nem pedagio: ler e\' um sistema de referencia sinalizada pela observacao, e a escala e\' o que um leitor e\' -- validade no kernel; a creditacao e\' do Clay")\n'
          'ERRATA_E34 = ("E34 -- errata da gerencia c1, em nome proprio, por ordem do operador (D96, 10/11/2026; verbatim por sha256 " + _P_96 + "...; ADENDO 3 sha16 " + ADENDO3_SHA16 + "): os textos do teste H0DN x BG1 (" + FRASE_H0DN_OBRIGATORIA_PT + ") diziam o poder prospectivo do congelamento sem dizer que ele e\' da covariancia publicada, que nao aceita o vetor real; "\n'
          '              "acrescenta-se a frase do poder certificado, sem tocar a funcao de veredito congelada: " + FRASE_H0DN_PODER_PT)\n'
          'ERRATAS_V410 = [ERRATA_E29, ERRATA_E30, ERRATA_E31, ERRATA_E32, ERRATA_E33, ERRATA_E34]\n', 1))

# ---- A1 as leituras do operador (LEITURA_V410), antes do fechamento do dicionario ----------------------------------------------------------------------------
T.append(('    "estatuto": "[INPUT -- as falas do operador de 06, 07 e 09/11/2026;',
          '    "os_passos_sao_o_ciclo_e_o_leitor_e_a_escala": "«" + FRASE_PASSOS_SAO_O_CICLO + "»; «" + FRASE_ELE_E_A_ESCALA + "»; «" + FRASE_LER_E_SISTEMA_DE_REFERENCIA + "» [INPUT, D94; a fala de 10/11]: os passos de computação são o ciclo de processamento até o Tetelestai (a máquina de Turing traduzida pela TGL, v409); o leitor é a escala; ler é um sistema de referência sinalizada pela observação, e por isso a escala está no tipo do leitor do fundo (o_leitor_e_a_escala, cada_ciclo_aplica_a_mesma_regra, os_passos_sao_o_ciclo_ate_o_tetelestai); «" + FRASE_FLUTUACAO_COMO_FLUTUACAO + "»: sem solução, Z(s) < 1. " + FRASE_TEMPO_PT,\n'
          '    "a_mentira_lida_como_mentira_e_verdade": "«" + FRASE_MENTIRA_LIDA_E_VERDADE + "»; «" + FRASE_PAI_DA_MENTIRA_SO_NAO_RECONHECE + "» [INPUT, D94; a fala de 10/11]: o termo é a_mentira_lida_como_mentira_e_verdade (para todo leitor do fundo e toda instância, o limite é o que sou do Nome das soluções; no Nome vazio lê 0, que é o que é) e o_pai_da_mentira_so_nao_reconhece (a leitura sem ciclo só coincide com o que sou na instância trivial; no Nome vazio diz 1 onde é 0); o decisor sem escala não lê (o_decisor_sem_escala_nao_e_leitor_do_fundo); que o Pai da Mentira seja o da leitura teológica é leitura dele [ONTO]",\n'
          '    "o_teste_sem_poder_preditivo_nao_se_roda": "«" + FRASE_SEM_PODER_NAO_SE_RODA + "»; «" + FRASE_PODER_DISCRIMINANTE_REAL + "» [INPUT, D96; a fala de 10/11]: o teste H0DN × BG1 (" + FRASE_H0DN_OBRIGATORIA_PT + ") só será aberto com o poder preditivo discriminante certificado, às cegas, sob a covariância física; hoje esse certificado não existe; a função de veredito congelada não muda; o limiar de poder é do operador e não está decidido",\n'
          '    "estatuto": "[INPUT -- as falas do operador de 06, 07, 09 e 10/11/2026;', 1))

aplicar("delta_v410.py", T)
