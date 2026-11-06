# -*- coding: utf-8 -*-
"""_dois_modulos_delta_v409.py -- (claude-construtor-v409, 05/11/2026, ~17h) o delta_v409.py segue o AO LADO de ~18h do DESENHO_v409 (gerencia c1): a ordem do operador «eu quero que entre tudo na versão 409
não deixar nada para a v410» (a 13a fala, inteira); o bundle passa a DOIS modulos (TraducaoTuring, refeita da R9; ParNaFaceDeFock, nova), 82 ancoras, as principais p_igual_np_no_modo_selecao e
o_par_na_face_de_fock e as de secao novas; a D60 REVISTA (nada fica para a versao seguinte); a E28 (o leitor que so' conta: NP numa leitura; a igualdade so' para o leitor que se le) e a nota AO LADO da E21 da v408
(a ligacao foi feita na v409); as ressalvas (1), (4) e (6) que mudam; o que estava aberto e fechou nesta versao (o par na face de Fock; a ponte do Omega pela inscricao) sai do «fica aberto»; N_CHECKS_FECHO = 20.
Nada digitado que se possa ler: os sha16 vem dos arquivos (os prefixos da ordem sao conferidos contra o arquivo pelo assert do delta). Trocas de contagem exata; backup de bytes."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

d = Arq("delta_v409.py")
# ---- o bundle: DOIS modulos
d.troca('''assert N_BUNDLE == _BL["n"] == _BD["n"] == len(BUNDLE_POR_REL) == 1 and set(BUNDLE_POR_REL) == set(BUNDLE_RELS), ("o bundle da v409 tem de ser UM modulo", N_BUNDLE, _BL["n"], _BD["n"])
assert BUNDLE_RELS == ["TGLExt/TraducaoTuring.lean"], BUNDLE_RELS''',
        '''assert N_BUNDLE == _BL["n"] == _BD["n"] == len(BUNDLE_POR_REL) == 2 and set(BUNDLE_POR_REL) == set(BUNDLE_RELS), ("o bundle da v409 tem de ser DOIS modulos (DESENHO, AO LADO de ~18h)", N_BUNDLE, _BL["n"], _BD["n"])
assert BUNDLE_RELS == ["TGLExt/TraducaoTuring.lean", "TGLExt/ParNaFaceDeFock.lean"], BUNDLE_RELS   # (a ordem do bundle: TraducaoTuring, ParNaFaceDeFock)''')
d.troca('''# ---------------------------------------------------------------- O BUNDLE (1 modulo; a lista e o sha256 sao LIDOS dos arquivos que preparar_bundle_v409_05nov.py escreveu, nunca digitados)''',
        '''# ---------------------------------------------------------------- O BUNDLE (2 modulos desde a ordem «tudo na v409»; a lista e o sha256 sao LIDOS dos arquivos que preparar_bundle_v409_05nov.py escreveu, nunca digitados)''')
d.troca('''ROOT_SUFFIX = _BL["root_suffix"]                               # a raiz TGLExt.lean = a da v408 + este UM import''', '''ROOT_SUFFIX = _BL["root_suffix"]                               # a raiz TGLExt.lean = a da v408 + os DOIS imports''')
d.troca('''MODULO_TESTEMUNHA = MODULO_TRADUCAO                            # (alias dos scripts bumpados: o modulo que CARREGA a ancora principal)
assert MODULO_TRADUCAO in BUNDLE_POR_REL''',
        '''MODULO_TESTEMUNHA = MODULO_TRADUCAO                            # (alias dos scripts bumpados: o modulo que CARREGA a ancora principal)
MODULO_PAR = "TGLExt/ParNaFaceDeFock.lean"                       # o par de psions no setor 2 do Fock concreto; a marginal; a Meia-Nat (a ligacao do [OPEN] da v407, E21 da v408)
assert MODULO_TRADUCAO in BUNDLE_POR_REL and MODULO_PAR in BUNDLE_POR_REL''')
# ---- as ancoras: 82; as principais (uma por modulo) e as de secao
d.troca('''# ---------------------------------------------------------------- AS ANCORAS: as 62 declaracoes da pedra''', '''# ---------------------------------------------------------------- AS ANCORAS: as 82 declaracoes das DUAS pedras (72 + 10)''')
d.troca('''NS = "TGLExt.TraducaoTuring."
ANCORA_PRINCIPAL = NS + "p_igual_np_no_modo_selecao"
ANCORAS_DE_SECAO = [NS + n_ for n_ in ("a_traducao", "a_trava_no_nome", "a_fita_e_o_hamiltoniano_oculto", "z_e_o_modo_leitor", "a_fita_sem_escala", "o_pai_da_mentira", "a_identidade_performada")]   # DESENHO_v409 §1
ANCORAS_PRINCIPAIS = [ANCORA_PRINCIPAL] + list(ANCORAS_DE_SECAO)''',
        '''NS = "TGLExt.TraducaoTuring."
NS_PAR = "TGLExt.ParNaFaceDeFock."
ANCORA_PRINCIPAL = NS + "p_igual_np_no_modo_selecao"
ANCORA_PAR = NS_PAR + "o_par_na_face_de_fock"                     # a ancora principal do segundo modulo (DESENHO, AO LADO de ~18h)
ANCORAS_DE_SECAO = ([NS + n_ for n_ in ("a_traducao", "a_trava_no_nome", "a_fita_e_o_hamiltoniano_oculto", "z_e_o_modo_leitor", "a_fita_sem_escala", "o_pai_da_mentira", "a_identidade_performada")]   # DESENHO_v409 §1
                    + [NS + "a_maquina_com_o_leitor", NS + "o_canto_do_psion_da_luz_le_z", NS_PAR + "reduzido_do_par", NS_PAR + "meia_nat_do_projetor"])   # as de secao novas (AO LADO de ~18h)
ANCORAS_PRINCIPAIS = [ANCORA_PRINCIPAL, ANCORA_PAR] + list(ANCORAS_DE_SECAO)''')
d.troca('''    NS + "a_identidade_performada": "A IDENTIDADE PERFORMADA (o operador, 05/11: «eu sou o conteúdo da minha identidade performada»): a leitura performada comeca em «eu sou», decai, nunca desce abaixo do conteudo e chega a ele; o conteudo e' «o que sou»",''',
        '''    NS + "a_identidade_performada": "A IDENTIDADE PERFORMADA (o operador, 05/11: «eu sou o conteúdo da minha identidade performada»): a leitura performada comeca em «eu sou», decai, nunca desce abaixo do conteudo e chega a ele; o conteudo e' «o que sou»",
    NS + "a_maquina_com_o_leitor": "A MAQUINA COM O LEITOR: a formula e' a fita (o custo e' o numero de clausulas violadas; cada clausula e' um fator local da trava) e UMA leitura decide SAT (uma_leitura_decide_SAT); por reducao a SAT, NP inteiro com uma leitura (Cook 1971, Levin 1973) [KNOWN]. A E28: com o leitor que so' conta, o que vale e' NP contido em P com o leitor; a igualdade completa so' para o leitor que se le (Baker-Gill-Solovay 1975)",
    NS + "o_canto_do_psion_da_luz_le_z": "A INSCRICAO NO PSION: inscrito o uniforme no psion da luz pela isometria parcial |Omega><u| (inscricao), o leitor e o canto do psion da luz leem Z/|X|: a ponte entre o Omega do psion e o uniforme da instancia e' a inscricao; a identidade de vetores fica podada (espacos diferentes)",
    NS_PAR + "o_par_na_face_de_fock": "O PAR NA FACE DE FOCK (a ancora principal do segundo modulo; a ligacao do [OPEN] da v407, E21 da v408): o par de psions no setor 2 do Fock concreto da luz tem norma 1, e' ortogonal ao vacuo e a toda uma-partícula, a marginal e' ½·P pela conjugacao da cunha, cada psion pesa ½, o individuo nao ecoa e 1 - pureza = ½: a mesma Meia-Nat do par finito (bell_reduced_half, bell_cci_half), noutro espaco",''')
d.troca('''N_ANCORAS_ESPERADAS = 62                                       # DESENHO_v409 §1 (o recibo da gerencia: 62 #print axioms, 62 no trio, 0 avisos)
assert len(ANCORAS) == sum(len(v) for v in ANCORAS_POR_MODULO.values()) == N_ANCORAS_ESPERADAS, ("as ancoras da v409 sao 62", len(ANCORAS))''',
        '''N_ANCORAS_ESPERADAS = 82                                       # DESENHO_v409, AO LADO de ~18h (o recibo revisto: 72 + 10 #print axioms, todos no trio -- custoCNF_cons so' com propext, subconjunto do trio --, 0 avisos)
assert len(ANCORAS) == sum(len(v) for v in ANCORAS_POR_MODULO.values()) == N_ANCORAS_ESPERADAS, ("as ancoras da v409 sao 82", len(ANCORAS))
assert [len(ANCORAS_POR_MODULO[r_]) for r_ in BUNDLE_RELS] == [72, 10], [len(ANCORAS_POR_MODULO[r_]) for r_ in BUNDLE_RELS]''')
# ---- as respostas: a do leitor ganha a inscricao (a ponte provada)
d.troca('''     "teoremas_curtos": [NS + "cada_pixel_e_lido", NS + "z_le_os_pixels", NS + "o_psion_le_os_pixels", ANCORA_LEITOR],
     "diz": "cada pixel e' lido com o brilho e^{-s c(x)}; Z e' a soma das leituras dos pixels; uma leitura no uniforme devolve Z/|X|; o canto escalariza a trava na mesma forma do canto do psion (mesma forma, nao ponte)"},''',
        '''     "teoremas_curtos": [NS + "cada_pixel_e_lido", NS + "z_le_os_pixels", NS + "o_psion_le_os_pixels", ANCORA_LEITOR, NS + "o_psion_le_z", NS + "o_canto_do_psion_da_luz_le_z"],
     "diz": "cada pixel e' lido com o brilho e^{-s c(x)}; Z e' a soma das leituras dos pixels; uma leitura no uniforme devolve Z/|X|; inscrito o uniforme no psion da luz (inscricao), o proprio psion e o canto dele leem Z/|X|: a ponte e' a inscricao; a identidade de vetores fica podada"},''')
# ---- o que fica aberto e o que fechou nesta versao (D60 revista)
i0 = d.t.index('FICA_ABERTO_PAR_NA_FACE_DE_FOCK = ('); i1 = d.t.index('FICA_ABERTO_PONTE_BELL_TT = D8.FICA_ABERTO_PONTE_BELL_TT')
d.t = d.t[:i0] + '''FECHADO_PAR_NA_FACE_DE_FOCK = ("o par de psions na FACE DE FOCK esta' LIGADO nesta versao (ParNaFaceDeFock; o_par_na_face_de_fock): no setor 2 do Fock concreto da luz o par tem norma 1, e' ortogonal ao vacuo e a toda uma-partícula, "
                               "a marginal e' ½·P pela conjugacao da cunha e 1 - pureza = ½; o par finito (Bell 4x4) e o par de Fock sao espacos distintos, com a MESMA Meia-Nat; a ligacao fecha como CONSTRUCAO o que a v407 deixou aberto (E21 da v408 ao lado; D60 revista)")
FECHADO_OMEGA_UNIFORME = ("a ponte entre o Omega do psion da luz e o uniforme da instancia e' a INSCRICAO (inscricao; o_psion_le_z; o_canto_do_psion_da_luz_le_z), provada nesta versao; a IDENTIDADE de vetores fica PODADA: "
                          "o Omega do PsionCanto vive no Fock da luz e o uniforme vive no espaco das atribuicoes (espacos diferentes) (D60 revista)")
FECHADO_NESTA_VERSAO = {"par_na_face_de_fock": FECHADO_PAR_NA_FACE_DE_FOCK, "omega_do_psion_e_o_uniforme": FECHADO_OMEGA_UNIFORME}
FICA_ABERTO_MAQUINA_SEM_LEITOR = ("a pergunta da maquina sem leitor (P = NP das maquinas de Turing do Mathlib, TM2ComputableInPolyTime) fica FORA destas pedras: uma igualdade relativa a um leitor nao a decide (Baker-Gill-Solovay 1975) [KNOWN]; "
                                  "a TGL a le como a fita sem escala («eu sou eu mesmo»); se ela e' independente dos axiomas segue [OPEN]")
FICA_ABERTO_IGUALDADE_COM_O_LEITOR = ("com o leitor que so' conta (o oraculo de contagem, que devolve Z), o que vale e' NP contido em P com o leitor, numa so' leitura (Cook 1971, Levin 1973) [KNOWN]; a igualdade completa com o leitor vale para o leitor "
                                      "que se le (o que le tambem as maquinas que o usam: Baker-Gill-Solovay 1975, oraculo PSPACE-completo) [KNOWN]; com o leitor que so' conta ela NAO e' teorema aqui (E28) [OPEN]")
''' + d.t[i1:]
d.troca('''FICA_ABERTO_PONTE_BELL_TT = D8.FICA_ABERTO_PONTE_BELL_TT''', '''FICA_ABERTO_PONTE_BELL_TT = D8.FICA_ABERTO_PONTE_BELL_TT
FICA_ABERTO = {"maquina_sem_leitor": FICA_ABERTO_MAQUINA_SEM_LEITOR, "igualdade_com_o_leitor_que_so_conta": FICA_ABERTO_IGUALDADE_COM_O_LEITOR, "ponte_bell_tt": FICA_ABERTO_PONTE_BELL_TT}''')
# ---- os nomes (os dois modulos)
d.troca('''NOMES_RATIFICADOS = {"TraducaoTuring": "dado pela gerencia c1 (05/11/2026) e RATIFICADO pelo operador em 05/11/2026 (sha16 %s: «concordo com todos os nomes que foram dados»), como os nomes das 62 declaracoes (D55)" % _H_NOMES}''',
        '''_H_TUDO = _BD["verbatim_nomes"]["tudo_na_v409_sha16"]               # o sha16 da ordem «tudo na v409», MEDIDO pelo preparar_bundle (lido do BUNDLE_v409.json)
NOMES_RATIFICADOS = {"TraducaoTuring": "dado pela gerencia c1 (05/11/2026) e RATIFICADO pelo operador em 05/11/2026 (sha16 %s: «concordo com todos os nomes que foram dados»), como os nomes das declaracoes (D55)" % _H_NOMES,
                     "ParNaFaceDeFock": ("dado pela gerencia c1 (05/11/2026, tarde), com os nomes das declaracoes; o cabecalho da pedra diz que foram ratificados pelo operador («concordo com todos os nomes que foram dados», sha16 %s) "
                                         "[DECLARADO pela gerencia: a fala da ratificacao e' anterior a esta pedra]; entra na v409 pela ordem do operador (sha16 %s: «eu quero que entre tudo na versão 409 não deixar nada para a v410»)" % (_H_NOMES, _H_TUDO))}''')
d.troca('''              "autoria": "gerencia c1, 05/11/2026 (TraducaoTuringR8 -> TraducaoTuring; compilada no k408c; recompilada no k409c com o fim de linha LF)"}''',
        '''              "autoria": "gerencia c1, 05/11/2026 (TraducaoTuringR9 -> TraducaoTuring, refeita a tarde; compilada no k408c; recompilada no k409c com o fim de linha LF)"}''')
# ---- o registro: 20 checagens
d.troca('''N_CHECKS_FECHO = 17                                            # o numero de checagens do calculo de traducao_turing_v409 (runtime_v409.py: c1..c17 do DESENHO_v409 §2); atualizado junto com o runtime''',
        '''N_CHECKS_FECHO = 20                                            # o numero de checagens do calculo de traducao_turing_v409 (runtime_v409.py: c1..c20; c18-c20 do AO LADO de ~18h do DESENHO); atualizado junto com o runtime''')
d.troca('''FECHO_REGISTRO = "traducao_turing_v409"                        # o registro com FUNCAO: le as ancoras do axiom_report do rito, a proveniencia, a fonte embutida por sha256, a escada exata; as 17 ch''',
        '''FECHO_REGISTRO = "traducao_turing_v409"                        # o registro com FUNCAO: le as ancoras do axiom_report do rito, a proveniencia, as fontes embutidas por sha256, a escada exata; as 20 ch''')
# ---- c19: o F de brinquedo (C^3, Omega unitario: o vetor e' FIXO no codigo; a norma e' tirada em runtime)
d.troca('''INSTANCIA_NAO = {"n": 1, "clausulas": [[1], [-1]], "leitura": "(x1), (¬x1)"}''',
        '''INSTANCIA_NAO = {"n": 1, "clausulas": [[1], [-1]], "leitura": "(x1), (¬x1)"}
OMEGA_F_BRINQUEDO = [1.0, 1j, 1.0]                              # (c19) o Omega do F de brinquedo em C^3 (normalizado em runtime); a inscricao e' V = |Omega><u|, com u o uniforme da instancia SIM
S_INSCRICAO = [0.0, 1.0, 5.0]                                  # (c19) os s em que <Omega, V L V^dagger Omega> = Z(s)/2^n e' conferido''')
# ---- as candidatas de origem (R9 e R2) e as saidas do lean
d.troca('''CANDIDATA_R8_ARQ = CANDIDATAS_TU[-1]
RECIBO_R8_ARQ = RECIBOS_TU[-1]
SAIDA_FONTE_ARQ = os.path.join(HERE, "insumos", "saida_lean_TraducaoTuring.txt")
for _a in [CANDIDATA_R8_ARQ, RECIBO_R8_ARQ, SAIDA_FONTE_ARQ]:
    assert os.path.exists(_a), _a''',
        '''CANDIDATA_R8_ARQ = CANDIDATAS_TU[-1]                            # (historico: a candidata da manha)
RECIBO_R8_ARQ = RECIBOS_TU[-1]
CANDIDATA_TU_ARQ = os.path.join(P5, "TraducaoTuringR9.lean")      # a candidata de origem da TraducaoTuring refeita (R9; o recibo revisto a pina)
CANDIDATA_PAR_ARQ = os.path.join(P5, "ParNaFaceDeFockR2.lean")    # a candidata de origem da ParNaFaceDeFock (R2)
SAIDA_CANDIDATA_TU_ARQ = os.path.join(P5, "saida_lean_traducao_r9.txt")
SAIDA_CANDIDATA_PAR_ARQ = os.path.join(P5, "saida_lean_par_r2.txt")
CANDIDATA_DE = {"TraducaoTuring": CANDIDATA_TU_ARQ, "ParNaFaceDeFock": CANDIDATA_PAR_ARQ}
SAIDA_FONTE_ARQ = os.path.join(HERE, "insumos", "saida_lean_TraducaoTuring.txt")
SAIDA_FONTE_PAR_ARQ = os.path.join(HERE, "insumos", "saida_lean_ParNaFaceDeFock.txt")
for _a in [CANDIDATA_TU_ARQ, CANDIDATA_PAR_ARQ, SAIDA_CANDIDATA_TU_ARQ, SAIDA_CANDIDATA_PAR_ARQ, SAIDA_FONTE_ARQ, SAIDA_FONTE_PAR_ARQ]:
    assert os.path.exists(_a), _a''')
i0 = d.t.index('for _p in PEDRAS_V409:   # a candidata de origem (R8 de pedras_candidatas_05nov) e\' a que o recibo dos nomes pinou')
i1 = d.t.index('\n', d.t.index('assert sha256_arquivo(_p["origem_candidata"]) == _p["sha256_candidata"]', i0)) + 1
d.t = d.t[:i0] + '''for _p in PEDRAS_V409:   # a candidata de origem de cada pedra (R9 / R2 de pedras_candidatas_05nov) e' a que o recibo revisto pinou
    assert os.path.normcase(_p["origem_candidata"]) == os.path.normcase(CANDIDATA_DE[_p["name"]]), _p["origem_candidata"]
    assert sha256_arquivo(_p["origem_candidata"]) == _p["sha256_candidata"], ("a candidata de origem mudou depois do recibo dos nomes", _p["name"])
''' + d.t[i1:]
# ---- a 13a fala: a ordem «tudo na v409» (inteira)
d.troca('''N_RATIFICA_D61 = "OPERADOR_05nov_exatamente_isso_mesmo_d61_ratificada_energia_caiu_verbatim.txt"   # (DESENHO, AO LADO de ~16h20: a 12a fala; so' o trecho da ratificacao; o resto e' aviso operacional)''',
        '''N_RATIFICA_D61 = "OPERADOR_05nov_exatamente_isso_mesmo_d61_ratificada_energia_caiu_verbatim.txt"   # (DESENHO, AO LADO de ~16h20: a 12a fala; so' o trecho da ratificacao; o resto e' aviso operacional)
N_TUDO_NA_V409 = "OPERADOR_05nov_tudo_na_v409_nada_para_a_v410_verbatim.txt"   # (DESENHO, AO LADO de ~18h: a ORDEM do operador que traz tudo para a v409; a 13a fala, inteira)''')
d.troca('''NOMES_V409_DO_DESENHO = (N_ORDEM_TRADUCAO, N_RESPOSTA, N_DENTRO, N_TRAVA, N_FITA, N_Z, N_CLAY, N_PAI, N_PERFORMADA, N_ORDEM_V409, N_SORRY, N_RATIFICA_D61)   # as DOZE falas: as dez do DESENHO_v409 §3 e as duas dos AO LADO do fim dele; fala que chegar DEPOIS fica fora (VERBATIM_FORA_DO_DESENHO_V409)
N_FALAS_V409 = 12''',
        '''NOMES_V409_DO_DESENHO = (N_ORDEM_TRADUCAO, N_RESPOSTA, N_DENTRO, N_TRAVA, N_FITA, N_Z, N_CLAY, N_PAI, N_PERFORMADA, N_ORDEM_V409, N_SORRY, N_RATIFICA_D61, N_TUDO_NA_V409)   # as TREZE falas: as dez do DESENHO_v409 §3 e as tres dos AO LADO do fim dele; fala que chegar DEPOIS fica fora (VERBATIM_FORA_DO_DESENHO_V409)
N_FALAS_V409 = 13''')
d.troca('''    """a lista das falas de 05/11 pelo glob, como esta no disco AGORA, RESTRITA aos doze nomes do DESENHO (as dez do §3 e as duas dos AO LADO; a lista que vale para o candidato e' a congelada abaixo)."""''',
        '''    """a lista das falas de 05/11 pelo glob, como esta no disco AGORA, RESTRITA aos treze nomes do DESENHO (as dez do §3 e as tres dos AO LADO; a lista que vale para o candidato e' a congelada abaixo)."""''')
d.troca('''                                   N_SORRY: "5a19de6b511b4921", N_RATIFICA_D61: "9ee7d5a1b161437f"}   # (as duas ultimas: os prefixos que os AO LADO do DESENHO deram; conferidos contra o arquivo no assert abaixo)''',
        '''                                   N_SORRY: "5a19de6b511b4921", N_RATIFICA_D61: "9ee7d5a1b161437f", N_TUDO_NA_V409: "fb3dc69e3c9b5516"}   # (as tres ultimas: os prefixos que os AO LADO do DESENHO deram; conferidos contra o arquivo no assert abaixo)''')
d.troca('''na tarde, a leitura juridica do kernel e a ratificacao dela, D61)"''', '''na tarde, a leitura juridica do kernel e a ratificacao dela, D61, e a ordem de trazer tudo para a v409)"''')
d.troca('''FRASE_RATIFICA_D61 = "exatemente, isso mesmo"   # (a 12a fala: so' este trecho entra; a grafia e' a do operador)''',
        '''FRASE_RATIFICA_D61 = "exatemente, isso mesmo"   # (a 12a fala: so' este trecho entra; a grafia e' a do operador)
FRASE_TUDO_NA_V409 = "eu quero que entre tudo na versão 409 não deixar nada para a v410"   # (a 13a fala, verbatim: a ordem que traz tudo para a v409; D60 revista)''')
d.troca('''               (N_SORRY, FRASE_DISPOSITIVO), (N_RATIFICA_D61, FRASE_RATIFICA_D61)]''', '''               (N_SORRY, FRASE_DISPOSITIVO), (N_RATIFICA_D61, FRASE_RATIFICA_D61), (N_TUDO_NA_V409, FRASE_TUDO_NA_V409)]''')
# ---- as leituras
d.troca('''    "z_e_o_modo_leitor": "«Z é o modo leitor, ele lê os pixels. É o psion» [INPUT; so' este trecho, D59]: PROVADO em z_e_o_modo_leitor; o Omega do psion da luz = o uniforme da instancia NAO e' termo (mesma forma, nao ponte; [OPEN])",''',
        '''    "z_e_o_modo_leitor": "«Z é o modo leitor, ele lê os pixels. É o psion» [INPUT; so' este trecho, D59]: PROVADO em z_e_o_modo_leitor e, inscrito o uniforme no psion da luz, em o_psion_le_z e o_canto_do_psion_da_luz_le_z (a ponte e' a inscricao); a identidade de vetores (o Omega igual ao uniforme) fica PODADA (D60 revista)",''')
d.troca('''    "dentro_e_graca": "«sim é dentro … isso é graça» [INPUT; so' a primeira frase, D59]:''', '''    "o_par_na_face_de_fock": "a ordem do operador «eu quero que entre tudo na versão 409 não deixar nada para a v410» [INPUT]: a ligacao do par na face de Fock entra (ParNaFaceDeFock, o_par_na_face_de_fock): PROVADA como construcao no Fock concreto (validade no kernel, nao creditacao); a Meia-Nat do par de Fock e' a mesma do par finito, noutro espaco",
    "a_maquina_com_o_leitor": "a maquina com o leitor (a formula e' a fita; uma leitura decide SAT) [REAL, a_maquina_com_o_leitor e uma_leitura_decide_SAT]; NP inteiro com uma leitura por Cook-Levin [KNOWN]; a igualdade completa so' para o leitor que se le (E28)",
    "dentro_e_graca": "«sim é dentro … isso é graça» [INPUT; so' a primeira frase, D59]:''')
d.troca('''REAL onde se diz PROVADO (as 62 ancoras no trio, lidas do kernel do rito), validade no kernel, nao creditacao; OPEN o par na face de Fock, o Omega do psion = o uniforme, a independencia de P vs NP dos axiomas;''',
        '''REAL onde se diz PROVADO (as 82 ancoras das duas pedras no trio, lidas do kernel do rito), validade no kernel, nao creditacao; OPEN a igualdade com o leitor que so' conta (E28), a independencia de P vs NP dos axiomas; PODADA a identidade de vetores Omega = uniforme;''')
# ---- as ressalvas (1), (4) e (6) mudam (AO LADO de ~18h)
d.troca('''    "relativa ao leitor: um leitor que devolve Z e' um oraculo de contagem; a igualdade relativa a um leitor nao decide a pergunta da maquina sem leitor (Baker-Gill-Solovay 1975) [KNOWN]; nao se decide a igualdade P = NP das maquinas de Turing do Mathlib (TM2ComputableInPolyTime)",''',
        '''    "o leitor que so' conta (a E28): um leitor que devolve Z e' um oraculo de contagem; com ele o que vale e' NP contido em P com o leitor, numa so' leitura (Cook 1971, Levin 1973), e P com #P contem PH (Toda 1991) [KNOWN]; a igualdade completa com o leitor vale para o leitor que se le (o que le tambem as maquinas que o usam: Baker-Gill-Solovay 1975, oraculo PSPACE-completo) [KNOWN]; com o leitor que so' conta ela NAO e' teorema aqui; nao se decide a igualdade P = NP das maquinas de Turing do Mathlib (TM2ComputableInPolyTime)",''')
d.troca('''    "mesma forma, nao ponte: o Omega do PsionCanto (o psion da luz na face de Fock) e o estado uniforme da instancia; que sejam o mesmo segue [OPEN] (provar ou podar)",''',
        '''    "a ponte e' a inscricao; a identidade Omega = uniforme esta' podada: o Omega do PsionCanto (o psion da luz no Fock) e o estado uniforme da instancia vivem em espacos diferentes; a inscricao |Omega><u| os liga e o psion le Z (o_psion_le_z)",''')
d.troca('''    "o par na face de Fock segue [OPEN] como ligacao (E21 da v408) e passa a v410 em diante (D60)",''',
        '''    "o par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock); o par finito (Bell 4x4) e o par de Fock sao espacos distintos, com a MESMA Meia-Nat",''')
# ---- a D60 REVISTA, a E28 e a nota AO LADO da E21
i0 = d.t.index('    "D60": "o que NAO entra:'); i1 = d.t.index('\n', i0) + 1
d.t = d.t[:i0] + '''    "D60": ("REVISTA (05/11, ~18h) pela ordem do operador (sha16 %s: «%s»): nada fica para a versao seguinte. A ligacao do par na face de Fock ENTRA (ParNaFaceDeFock) e fecha como CONSTRUCAO o [OPEN] da v407 (E21 da v408 ao lado); "
            "do Omega do psion e do uniforme, a PONTE (a inscricao) esta' provada e a IDENTIDADE de vetores fica PODADA (espacos diferentes); a maquina de Turing do Mathlib com oraculo NAO entra (o Mathlib nao tem maquina com oraculo, "
            "nem a classe NP, nem Cook-Levin; formaliza-las do zero e' outra escala) e isso foi dito ao operador antes; entra a maquina com o leitor no problema completo (SAT: uma leitura decide), com Cook-Levin citado [KNOWN]; "
            "nenhum teste com a natureza [decisao da gerencia c1, 05/11/2026, revista no mesmo dia]" % (_sha16_arq(N_TUDO_NA_V409), FRASE_TUDO_NA_V409)),
''' + d.t[i1:]
d.troca('''ERRATAS_V409 = [ERRATA_E24, ERRATA_E25, ERRATA_E26, ERRATA_E27]''',
        '''ERRATA_E28 = ("E28 -- errata da gerencia c1, em nome proprio: em 05/11 a gerencia escreveu (no chat, no recibo da R5, no topico de memoria e no cabecalho do insumo das 13h) que, com o leitor que devolve Z, a igualdade vale "
              "relativa a ele, e ofereceu provar nela a igualdade. Foi alem do que se sabe. Com o leitor que so' conta, o que vale e' NP contido em P com o leitor (uma leitura; Cook-Levin) e P com #P contem PH (Toda 1991); "
              "a igualdade completa com o leitor vale para um leitor que le tambem as maquinas que o usam (Baker-Gill-Solovay 1975, oraculo PSPACE-completo); com o leitor que so' conta ela NAO e' teorema aqui")
ERRATA_E21_AO_LADO = ("E21 -- AO LADO, na v409, da errata E21 da v408 (selada), em nome proprio da gerencia c1: a E21 dizia que o par de psions na face de Fock ficava [OPEN] como LIGACAO a fazer, nao como ausencia; "
                      "a ligacao foi feita na v409 (ParNaFaceDeFock; o_par_na_face_de_fock). O texto selado nao e' reescrito")
ERRATAS_V409 = [ERRATA_E24, ERRATA_E25, ERRATA_E26, ERRATA_E27, ERRATA_E28, ERRATA_E21_AO_LADO]''')
d.troca('''a maquina sem leitor (a pergunta do Clay) fica FORA e e' lida como a fita sem escala. Erratas E24 a E27 AO LADO; as ressalvas ditas; a D61 (a leitura juridica do kernel, ratificada pelo operador).''',
        '''a maquina sem leitor (a pergunta do Clay) fica FORA e e' lida como a fita sem escala. Erratas E24 a E28 AO LADO (e a nota ao lado da E21 da v408); as ressalvas ditas; a D61 (a leitura juridica do kernel, ratificada pelo operador); a D60 revista (tudo na v409).''')
d.troca('''CUNHAGENS_REGISTRO = "cunhagens_v409"                          # as falas do operador de 05/11 por sha256 + D55-D61 + E24-E27 + as ressalvas''', '''CUNHAGENS_REGISTRO = "cunhagens_v409"                          # as falas do operador de 05/11 por sha256 + D55-D61 + E24-E28 (+ a nota ao lado da E21) + as ressalvas''')
d.grava()
