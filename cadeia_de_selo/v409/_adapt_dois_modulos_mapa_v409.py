# -*- coding: utf-8 -*-
"""_adapt_dois_modulos_mapa_v409.py -- (claude-construtor-v409, 05/11/2026) o registro da v409 no mapa de rotas (pos_rito\\registrar_mapa_v409.py, que so' MONTA; quem registra e' a gerencia/custodia) e o texto da custodia
(pos_rito\\textos_custodia_handoff_v409.py) passam ao AO LADO mais novo do DESENHO_v409.md: a pedra TraducaoTuring vem da R9 (rota kernel.traducao_turing_r9_inscricao_e_sat_05nov, conferida no livro em 05/11 17h, so' leitura),
a ParNaFaceDeFock entra (rota kernel.par_na_face_de_fock_ligado_05nov, idem); as duas ganham ANOTACAO; a R8 passa a dizer que a linha seguiu na R9; o par na face de Fock LIGADO; a ponte Omega-uniforme e' a inscricao (a identidade
de vetores PODADA); nada passa a v410; as erratas do registro sao E21 (ao lado), E24 a E28; decisoes D55 a D61. Nenhuma conferencia relaxada."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

m = Arq("pos_rito/registrar_mapa_v409.py")
m.troca('''R8 = "kernel.traducao_turing_a_identidade_performada_r8_05nov"        # R8: a identidade performada; a candidata que entrou no kernel como TGLExt/TraducaoTuring''',
        '''R8 = "kernel.traducao_turing_a_identidade_performada_r8_05nov"        # R8: a identidade performada (a linha seguiu na R9)
R9 = "kernel.traducao_turing_r9_inscricao_e_sat_05nov"                 # R9: a inscricao no psion e SAT como a fita; E28; a candidata que entrou no kernel como TGLExt/TraducaoTuring
R_PARF = "kernel.par_na_face_de_fock_ligado_05nov"                     # ParNaFaceDeFock: o par na face de Fock LIGADO (E21 da v408 ao lado); entrou no kernel como TGLExt/ParNaFaceDeFock''')
m.troca('''# a afericao do traco (v408); o par na face de Fock segue [OPEN] como ligacao''', '''# a afericao do traco (v408); a ligacao do par na face de Fock foi feita na v409 (R_PARF)''')
m.troca('''ANOTADAS = (R1, R2, R3, R4, R5, R6, R7, R8, R_DIC,''', '''ANOTADAS = (R1, R2, R3, R4, R5, R6, R7, R8, R9, R_PARF, R_DIC,''')
m.troca('''o modulo de kernel TraducaoTuring (a candidata R8 de 05/11, com o nome e os nomes das 62 declaracoes dados pela gerencia e ratificados pelo operador, D55;''',
        '''os DOIS modulos de kernel TraducaoTuring (a candidata R9 de 05/11, com o nome e os nomes das 72 declaracoes dados pela gerencia e ratificados pelo operador, D55) e ParNaFaceDeFock (o par na face de Fock ligado; ordem «tudo na v409»;''')
m.troca('''(traducao_turing_v409: le do kernel do proprio rito as 62 ancoras, o modulo por sha256,''', '''(traducao_turing_v409: le do kernel do proprio rito as 82 ancoras, os dois modulos por sha256,''')
m.troca('''assert sorted(E) == ["E24", "E25", "E26", "E27"], "as erratas do registro nao sao E24 a E27"''', '''assert sorted(E) == ["E21", "E24", "E25", "E26", "E27", "E28"], "as erratas do registro nao sao E24 a E28 e a E21 ao lado"''')
m.troca('''LIN = "a linha das candidatas R1 a R8 de 05/11 desemboca no modulo TGLExt/%s (a fonte pinada e' a da R8,''', '''LIN = "a linha das candidatas R1 a R9 de 05/11 desemboca no modulo TGLExt/%s (a fonte pinada e' a da R9,''')
m.troca('''; mesma forma do canto do psion, nao ponte" % (S, P0["name"]),''', '''; a ponte com o canto do psion e' a inscricao (o_canto_do_psion_da_luz_le_z, na R9)" % (S, P0["name"]),''')
m.troca('''O Omega do psion da luz como o estado uniforme da instancia segue [OPEN] (mesma forma, nao ponte).",''', '''A ponte entre o Omega do psion da luz e o uniforme da instancia e' a inscricao, provada na R9 (inscricao; o_psion_le_z); a identidade dos vetores fica podada (D60 revista).",''')
m.troca('''estatuto=EST_C + "; OPEN (o Omega do psion = o uniforme)"))''', '''estatuto=EST_C + "; PODADO (a identidade de vetores Omega = uniforme: espacos diferentes; a ponte e' a inscricao)"))''')
m.troca('''T9.append(anot(R8, "v409 SELADA %s: a candidata R8 entrou no kernel do rito como TGLExt/%s (nome da gerencia ratificado pelo operador, D55); a identidade performada (a_identidade_performada)" % (S, P0["name"]),
                   f"a pedra {P0['name']} esta no kernel do rito com o sha256 pinado ({sha_ped}), {n_anc} ancoras no trio; a fonte pinada e' a da candidata R8 (sha16 {P0['sha256_candidata'][:16]}),''',
        '''T9.append(anot(R8, "v409 SELADA %s: a linha da R8 seguiu na R9, que entrou no kernel do rito como TGLExt/%s (nome da gerencia ratificado pelo operador, D55); a identidade performada (a_identidade_performada)" % (S, P0["name"]),
                   f"a pedra {P0['name']} esta no kernel do rito com o sha256 pinado ({sha_ped}), {n_anc} ancoras no trio; a fonte pinada e' a da candidata R9 (sha16 {P0['sha256_candidata'][:16]}),''')
m.troca('''"o registro traducao_turing_v409 le estas ancoras a cada rito; c11 confere a performance; o par na face de Fock segue [OPEN] como ligacao (D60).", refs=[R1, R2, R3, R4, R5, R6, R7], artefatos=[ped, DL_.CANDIDATA_R8_ARQ, DL_.RECIBO_R8_ARQ, KR],
                   estatuto=EST_C, defeito="as ressalvas, ditas no registro: " + ress))''',
        '''"o registro traducao_turing_v409 le estas ancoras a cada rito; c11 confere a performance; o par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock; D60 revista).", refs=[R1, R2, R3, R4, R5, R6, R7, R9], artefatos=[DL_.CANDIDATA_R8_ARQ, DL_.RECIBO_R8_ARQ],
                   estatuto=EST_C, defeito="as ressalvas, ditas no registro: " + ress))
    T9.append(anot(R9, "v409 SELADA %s: a candidata R9 entrou no kernel do rito como TGLExt/%s: a inscricao do uniforme no psion da luz (o leitor do psion le Z) e a maquina com o leitor (uma leitura decide SAT); E28" % (S, P0["name"]),
                   f"a pedra {P0['name']} esta no kernel do rito com o sha256 pinado ({sha_ped}), {n_anc} ancoras no trio; a fonte pinada e' a da candidata R9 (sha16 {P0['sha256_candidata'][:16]}); "
                   f"c19 confere a inscricao num F de brinquedo e c20 a leitura que decide SAT na instancia de brinquedo. {corpo('E28')}. O alcance: {ALC}.",
                   "o registro traducao_turing_v409 le estas ancoras a cada rito; com o leitor que so' conta vale NP contido em P numa leitura, e a igualdade completa e' a do leitor que se le (E28): ela segue [OPEN] com o leitor que so' conta.", refs=[R8, R5, R_PSION], artefatos=[ped, DL_.CANDIDATA_TU_ARQ, DL_.SAIDA_CANDIDATA_TU_ARQ, KR],
                   estatuto=EST_C + "; KNOWN (Cook 1971, Levin 1973, Toda 1991, Baker-Gill-Solovay 1975); OPEN (a igualdade completa com o leitor que so' conta)", defeito="as ressalvas, ditas no registro: " + ress))
    P1 = [p_ for p_ in DL_.PEDRAS_V409 if p_["rel"] == DL_.MODULO_PAR][0]
    ped_par = os.path.join(PK, "pedra", P1["name"] + ".lean")
    T9.append(anot(R_PARF, "v409 SELADA %s: a pedra %s entrou no kernel do rito como TGLExt/%s: o par de psions na face de Fock LIGADO (o_par_na_face_de_fock); a E21 da v408 ao lado" % (S, P1["name"], P1["name"]),
                   f"a pedra {P1['name']} esta no kernel do rito com o sha256 pinado ({DL_.BUNDLE_POR_REL[P1['rel']]['sha256'][:16]}), {len(DL_.ANCORAS_POR_MODULO[P1['rel']])} ancoras no trio; a fonte pinada e' a da candidata (sha16 {P1['sha256_candidata'][:16]}); "
                   f"c18 confere o reduzido do par de Bell finito (½·I; 1 - pureza = ½). {corpo('E21')}. A ordem do operador, verbatim: {_aspas_(DL_.FRASE_TUDO_NA_V409)}.",
                   "o registro traducao_turing_v409 le estas ancoras a cada rito; o par finito (Bell 4x4) e o par de Fock sao espacos distintos, com a mesma Meia-Nat (nao identificacao); a ponte Bell-TT segue [OPEN].", refs=[R_PAR, R_FOCK, R_PSION], artefatos=[ped_par, DL_.CANDIDATA_PAR_ARQ, DL_.SAIDA_CANDIDATA_PAR_ARQ, KR],
                   estatuto="REAL (os termos no kernel do rito); INPUT (a ordem do operador de 05/11); DECLARADO (o recibo de compilacao da candidata; a ratificacao do nome dita pelo cabecalho da pedra)"))''')
m.troca('''"v409 SELADA %s: o programa do fechamento nao ganha chave nova nem perde nenhuma; a traducao as classes de Turing fica fechada relativa ao leitor; o par na face de Fock segue [OPEN] como ligacao" % S,''',
        '''"v409 SELADA %s: o programa do fechamento nao ganha chave nova nem perde nenhuma; a traducao as classes de Turing fica fechada relativa ao leitor; o par na face de Fock ligado (ParNaFaceDeFock)" % S,''')
m.troca('''"a ligacao do par na face de Fock (v410 em diante, D60), a ponte Bell-TT, K(O) != bot para O compacto e o teste com a natureza seguem [OPEN]; o programa do fechamento nao e' fechado por esta anotacao.", refs=[R_INV, R8],''',
        '''"a igualdade completa com o leitor que so' conta (E28), a ponte Bell-TT, K(O) != bot para O compacto e o teste com a natureza seguem [OPEN]; o programa do fechamento nao e' fechado por esta anotacao.", refs=[R_INV, R9, R_PARF],''')
m.troca('''estatuto="REAL (a leitura do kernel do rito); OPEN (a ligacao do par na face de Fock; K(O) != bot para O compacto)"))''', '''estatuto="REAL (a leitura do kernel do rito; o par na face de Fock ligado); OPEN (a igualdade completa com o leitor que so' conta; K(O) != bot para O compacto)"))''')
m.troca('''"proximo_passo": "a ligacao do par na face de Fock (v410 em diante, D60); o Omega do psion da luz como o uniforme da instancia (provar ou podar); a independencia da pergunta da maquina sem leitor, [OPEN];''',
        '''"proximo_passo": "a igualdade completa com o leitor que so' conta (E28) e a independencia da pergunta da maquina sem leitor, [OPEN];''')
m.troca('''as erratas E24 a E27 e as decisoes D55 a D60 sao da gerencia c1, em nome proprio, ao lado''', '''as erratas E24 a E28 e a E21 ao lado e as decisoes D55 a D60 sao da gerencia c1, em nome proprio (a D61, ratificada pelo operador), ao lado''')
m.grava()
