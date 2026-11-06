# -*- coding: utf-8 -*-
"""_dois_modulos_registros_v409.py -- (claude-construtor-v409, 05/11/2026, ~17h) registros_v409.py segue o AO LADO de ~18h do DESENHO_v409: as FONTES pinadas das DUAS pedras (a embutida, a fonte normalizada,
a saida do lean, a candidata de origem R9 / R2 e a saida da candidata), o bundle e a medida do Audit; o contrato com os dois modulos, o que fica aberto (sem o que fechou) e o que fechou nesta versao, a inscricao de brinquedo
da c19; o texto do registro com a inscricao, a maquina com o leitor, o par na face de Fock e a E28; as erratas E28 e a nota ao lado da E21 no spec cunhagens_v409; o «nao diz» sem as frases que a D60 revista proibe.
Trocas de contagem exata; backup de bytes."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

r = Arq("registros_v409.py")
r.troca('''CHAVE_PEDRA = {"TraducaoTuring": "pedra_traducao_turing"}                  # a pedra normalizada EMBUTIDA no kernel (copia duravel: insumos\\TraducaoTuring_embutida.lean)
CHAVE_FONTE = {"TraducaoTuring": "fonte_traducao_turing_05nov"}            # a fonte normalizada da gerencia, com os #print axioms (insumos\\TraducaoTuring.lean: as ancoras saem dela)
CHAVE_SAIDA_FONTE = {"TraducaoTuring": "saida_lean_traducao_turing_05nov"}  # a saida do lean ao compilar a fonte no sandbox da v408''',
        '''CHAVE_PEDRA = {"TraducaoTuring": "pedra_traducao_turing", "ParNaFaceDeFock": "pedra_par_na_face_de_fock"}                  # a pedra normalizada EMBUTIDA no kernel (copia duravel: insumos\\<nome>_embutida.lean)
CHAVE_FONTE = {"TraducaoTuring": "fonte_traducao_turing_05nov", "ParNaFaceDeFock": "fonte_par_na_face_de_fock_05nov"}            # a fonte normalizada da gerencia, com os #print axioms (insumos\\<nome>.lean: as ancoras saem dela)
CHAVE_SAIDA_FONTE = {"TraducaoTuring": "saida_lean_traducao_turing_05nov", "ParNaFaceDeFock": "saida_lean_par_na_face_de_fock_05nov"}  # a saida do lean ao compilar a fonte no sandbox da v408''')
r.troca('''CHAVE_CANDIDATA_R8 = "candidata_traducao_turing_r8_05nov"
CHAVE_RECIBO_R8 = "recibo_traducao_turing_r8_05nov"''',
        '''CHAVE_CANDIDATA = {"TraducaoTuring": "candidata_traducao_turing_r9_05nov", "ParNaFaceDeFock": "candidata_par_na_face_de_fock_r2_05nov"}   # a candidata de origem de cada pedra (o recibo revisto pina as duas)
CHAVE_SAIDA_CANDIDATA = {"TraducaoTuring": "saida_lean_traducao_turing_r9_05nov", "ParNaFaceDeFock": "saida_lean_par_na_face_de_fock_r2_05nov"}''')
i0 = r.t.index("ORIGENS = ([")
i1 = r.t.index("assert len({f[\"chave\"] for f in FONTES}) == len(FONTES)")
r.t = r.t[:i0] + '''ORIGENS = ([("%s_embutida.lean" % p["name"], p["src"]) for p in DL.PEDRAS_V409]
           + [("%s.lean" % p["name"], p["origem"]) for p in DL.PEDRAS_V409]
           + [("saida_lean_%s.txt" % p["name"], os.path.join(INS, "saida_lean_%s.txt" % p["name"])) for p in DL.PEDRAS_V409]
           + [("TraducaoTuringR9.lean", DL.CANDIDATA_TU_ARQ), ("ParNaFaceDeFockR2.lean", DL.CANDIDATA_PAR_ARQ), ("saida_lean_traducao_r9.txt", DL.SAIDA_CANDIDATA_TU_ARQ), ("saida_lean_par_r2.txt", DL.SAIDA_CANDIDATA_PAR_ARQ),
              ("BUNDLE_v409.json", DL.BUNDLE_ARQ), (DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v409.json"))])
_PAPEL_PEDRA = {"TraducaoTuring": ("a pedra TraducaoTuring (gerencia c1, 05/11/2026, refeita a tarde da R9; o nome e os nomes das declaracoes dados pela gerencia e RATIFICADOS pelo operador em 05/11): o dicionario de Turing; o modo selecao (o Tetelestai); "
                                   "a trava no Nome; a fita e' o hamiltoniano oculto; Z e' o modo leitor; a inscricao no psion (o psion le Z); a formula e' a fita e uma leitura decide SAT (a maquina com o leitor; a E28 no cabecalho); a fita sem escala e o Pai da Mentira; "
                                   "a identidade performada; a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256 [REAL]"),
                "ParNaFaceDeFock": ("a pedra ParNaFaceDeFock (gerencia c1, 05/11/2026, tarde; entra na v409 pela ordem do operador de trazer tudo para esta versao): o par de psions no setor 2 do Fock concreto da luz; norma 1; ortogonal ao vacuo e a toda uma-partícula; "
                                    "a marginal e' ½·P pela conjugacao da cunha; cada psion pesa ½; o individuo nao ecoa; 1 - pureza = ½ (a mesma Meia-Nat do par finito); a que vale no rito e' a EMBUTIDA no kernel, conferida por sha256 em formal_files_sha256 [REAL]")}
FONTES = []
for _p in DL.PEDRAS_V409:
    _n = _p["name"]
    FONTES += [{"chave": CHAVE_PEDRA[_n], "arquivo": os.path.join(INS, "%s_embutida.lean" % _n), "papel": _PAPEL_PEDRA[_n]},
               {"chave": CHAVE_FONTE[_n], "arquivo": os.path.join(INS, "%s.lean" % _n),
                "papel": "a fonte normalizada da %s (gerencia c1, 05/11/2026; modulo/namespace = o nome final; com os #print axioms que sao as ancoras do registro; fim de linha CRLF): a embutida e' esta sem os #print axioms e com o fim de linha LF [REAL: sha256]" % _n},
               {"chave": CHAVE_SAIDA_FONTE[_n], "arquivo": os.path.join(INS, "saida_lean_%s.txt" % _n),
                "papel": "a saida do lean ao compilar a fonte normalizada da %s no sandbox da v408 (todas as declaracoes no trio; 0 avisos) [DECLARADO pela gerencia; refeito no k409c e no Audit do rito]" % _n}]
FONTES += [
    {"chave": CHAVE_CANDIDATA["TraducaoTuring"], "arquivo": os.path.join(INS, "TraducaoTuringR9.lean"), "papel": "a candidata de origem da TraducaoTuring refeita (R9 da gerencia, 05/11/2026, tarde: + a inscricao no psion, + a formula e' a fita, + a E28 no cabecalho) [DECLARADO pela gerencia na origem; o que vale e' a embutida]"},
    {"chave": CHAVE_CANDIDATA["ParNaFaceDeFock"], "arquivo": os.path.join(INS, "ParNaFaceDeFockR2.lean"), "papel": "a candidata de origem da ParNaFaceDeFock (R2 da gerencia, 05/11/2026, tarde) [DECLARADO pela gerencia na origem; o que vale e' a embutida]"},
    {"chave": CHAVE_SAIDA_CANDIDATA["TraducaoTuring"], "arquivo": os.path.join(INS, "saida_lean_traducao_r9.txt"), "papel": "a saida do lean da candidata R9 no sandbox da v408 [DECLARADO pela gerencia; refeito no k409c e no Audit do rito]"},
    {"chave": CHAVE_SAIDA_CANDIDATA["ParNaFaceDeFock"], "arquivo": os.path.join(INS, "saida_lean_par_r2.txt"), "papel": "a saida do lean da candidata R2 no sandbox da v408 [DECLARADO pela gerencia; refeito no k409c e no Audit do rito]"},
    {"chave": CHAVE_BUNDLE, "arquivo": os.path.join(INS, "BUNDLE_v409.json"), "papel": "o bundle dos dois modulos (preparar_bundle_v409_05nov.py): sha256 de cada modulo normalizado, a fonte de origem e o sha256 dela, as ancoras, o sha16 da fala da ordem e dos nomes e o da ordem de trazer tudo para a v409 [REAL]"},
    {"chave": CHAVE_KH, "arquivo": os.path.join(INS, DL.KH_N1_INSUMO), "papel": "a medida da cobertura no Audit do sandbox da v409 (pos_build_kernel_v409.py)"},
]
''' + r.t[i1:]
# ---- o contrato
r.troca('''    return {"bundle": {"n": DL.N_BUNDLE, "pedras": [p["name"] for p in DL.PEDRAS_V409], "traducao": DL.MODULO_TRADUCAO, "da_gerencia": list(DL.BUNDLE_DA_GERENCIA), "da_bancada": 0,''',
        '''    return {"bundle": {"n": DL.N_BUNDLE, "pedras": [p["name"] for p in DL.PEDRAS_V409], "traducao": DL.MODULO_TRADUCAO, "par": DL.MODULO_PAR, "da_gerencia": list(DL.BUNDLE_DA_GERENCIA), "da_bancada": 0,''')
r.troca('''"ancoras": anc, "n_ancoras": len(anc), "ancoras_por_modulo": {k: list(v) for k, v in DL.ANCORAS_POR_MODULO.items()}, "ancora_principal": DL.ANCORA_PRINCIPAL, "ancoras_principais": list(DL.ANCORAS_PRINCIPAIS), "ancoras_de_secao": list(DL.ANCORAS_DE_SECAO),''',
        '''"ancoras": anc, "n_ancoras": len(anc), "ancoras_por_modulo": {k: list(v) for k, v in DL.ANCORAS_POR_MODULO.items()}, "ancora_principal": DL.ANCORA_PRINCIPAL, "ancora_par": DL.ANCORA_PAR, "ancoras_principais": list(DL.ANCORAS_PRINCIPAIS), "ancoras_de_secao": list(DL.ANCORAS_DE_SECAO),''')
r.troca('''            "fica_aberto": {"par_na_face_de_fock": DL.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, "omega_do_psion_e_o_uniforme": DL.FICA_ABERTO_OMEGA_UNIFORME, "maquina_sem_leitor": DL.FICA_ABERTO_MAQUINA_SEM_LEITOR, "ponte_bell_tt": DL.FICA_ABERTO_PONTE_BELL_TT},
            "alcance": dict(ALCANCE), "instancia_sim": dict(DL.INSTANCIA_SIM), "instancia_nao": dict(DL.INSTANCIA_NAO),''',
        '''            "fica_aberto": dict(DL.FICA_ABERTO), "fechado_nesta_versao": dict(DL.FECHADO_NESTA_VERSAO),
            "alcance": dict(ALCANCE), "instancia_sim": dict(DL.INSTANCIA_SIM), "instancia_nao": dict(DL.INSTANCIA_NAO),
            "inscricao_brinquedo": {"omega": [[complex(z_).real, complex(z_).imag] for z_ in DL.OMEGA_F_BRINQUEDO], "s": list(DL.S_INSCRICAO), "f": "C^3", "nota": "c19: V = |Omega><u|, com u o uniforme da instancia SIM; o Omega e' normalizado em runtime"},''')
# ---- o texto do registro com funcao
r.troca('''        "estatuto": "[REAL] os termos do kernel do rito: as %d ancoras da pedra TraducaoTuring (TGLExt.TraducaoTuring.*), no trio, com proveniencia no modulo esperado, e o modulo por sha256; "
                    "[REAL] as 17 checagens (a instancia de brinquedo fixa, as solucoes calculadas; aritmetica com beta em runtime; gate congelado; escada exata; guardas; beta = alfa CODATA 2018 x sqrt(e)); "''',
        '''        "estatuto": "[REAL] os termos do kernel do rito: as %d ancoras das DUAS pedras (TGLExt.TraducaoTuring.* e TGLExt.ParNaFaceDeFock.*), no trio, com proveniencia no modulo esperado, e os modulos por sha256; "
                    "[REAL] as 20 checagens (a instancia de brinquedo fixa, as solucoes calculadas; a marginal do par de Bell finito; a inscricao num F de brinquedo; uma leitura decide SAT; aritmetica com beta em runtime; gate congelado; escada exata; guardas; beta = alfa CODATA 2018 x sqrt(e)); "''')
r.troca('''        "escopo": "[REAL] O que entra no um.py: 1 modulo novo em TGLExt/ -- TraducaoTuring (o nome e os nomes das 62 declaracoes dados pela gerencia c1 e ratificados pelo operador em 05/11/2026). "''',
        '''        "escopo": "[REAL] O que entra no um.py: 2 modulos novos em TGLExt/ -- TraducaoTuring (o nome e os nomes das declaracoes dados pela gerencia c1 e ratificados pelo operador em 05/11/2026) e ParNaFaceDeFock (pela ordem do operador de trazer tudo para a v409). "''')
r.troca('''                  "(G) A IDENTIDADE PERFORMADA (a_identidade_performada): comeca em «eu sou», decai, nunca abaixo do conteudo, chega a ele. O ALCANCE: " + DL.FRASE_D56_PT + "; " + DL.FRASE_QUALIFICADOR_PT + ". Nenhuma chave antiga muda. O registro confere, em runtime: as "
                  + str(len(DL.ANCORAS)) + " ancoras; o sha256 do modulo; a raiz com o import; as respostas do operador pelos teoremas da pedra; a aritmetica da instancia de brinquedo com beta em runtime; o gate congelado; a escada exata; as guardas; beta = alfa sqrt e.",''',
        '''                  "(G) A IDENTIDADE PERFORMADA (a_identidade_performada): comeca em «eu sou», decai, nunca abaixo do conteudo, chega a ele. "
                  "(H) A INSCRICAO NO PSION (inscricao, o_psion_le_z, o_canto_do_psion_da_luz_le_z): inscrito o uniforme no psion da luz pela isometria parcial |Omega><u|, o leitor e o canto do psion da luz leem Z/|X|; a ponte e' a inscricao; a identidade de vetores fica podada. "
                  "(I) A FORMULA E' A FITA E A MAQUINA COM O LEITOR (custoCNF, a_trava_da_formula_fatora_na_clausula, uma_leitura_decide_SAT, a_maquina_com_o_leitor): o custo e' o numero de clausulas violadas; cada clausula e' um fator local da trava; uma leitura decide SAT; "
                  "por reducao a SAT, NP inteiro com uma leitura (Cook-Levin [KNOWN]); com o leitor que so' conta, NP contido em P com o leitor, e a igualdade completa so' para o leitor que se le (E28). "
                  "(J) O PAR NA FACE DE FOCK (ParNaFaceDeFock: reduzido_do_par, meia_nat_do_projetor, o_par_na_face_de_fock): o par de psions no setor 2 do Fock concreto; norma 1; ortogonal ao vacuo e a toda uma-partícula; a marginal e' ½·P pela conjugacao da cunha; "
                  "cada psion pesa ½; o individuo nao ecoa; 1 - pureza = ½, a mesma Meia-Nat do par finito, noutro espaco. O ALCANCE: " + DL.FRASE_D56_PT + "; " + DL.FRASE_QUALIFICADOR_PT + ". Nenhuma chave antiga muda. O registro confere, em runtime: as "
                  + str(len(DL.ANCORAS)) + " ancoras das duas pedras; o sha256 de cada modulo; a raiz com os imports; as respostas do operador pelos teoremas da pedra; a aritmetica da instancia de brinquedo com beta em runtime; a marginal do par de Bell finito; "
                  "a inscricao num F de brinquedo; uma leitura decide SAT; o gate congelado; a escada exata; as guardas; beta = alfa sqrt e.",''')
r.troca('''        "limites": ["[REAL, alcance; KNOWN] " + DL.RESSALVAS_V409[0], "[KNOWN; OPEN] " + DL.RESSALVAS_V409[1], "[KNOWN; fora] " + DL.RESSALVAS_V409[2], "[OPEN] " + DL.RESSALVAS_V409[3], "[INPUT/ONTO, fora do kernel] " + DL.RESSALVAS_V409[4], "[OPEN] " + DL.RESSALVAS_V409[5],
                    "[REAL] " + DL.RESSALVAS_V409[6], "[REAL] " + DL.RESSALVAS_V409[7], "[REAL] " + DL.RESSALVAS_V409[8], DL.ERRATA_E24, DL.ERRATA_E25, DL.ERRATA_E26, DL.ERRATA_E27] + _LIM_COMUM,''',
        '''        "limites": ["[KNOWN; OPEN a igualdade com o leitor que so' conta] " + DL.RESSALVAS_V409[0], "[KNOWN; OPEN] " + DL.RESSALVAS_V409[1], "[KNOWN; fora] " + DL.RESSALVAS_V409[2], "[REAL a ponte; podada a identidade] " + DL.RESSALVAS_V409[3], "[INPUT/ONTO, fora do kernel] " + DL.RESSALVAS_V409[4], "[REAL] " + DL.RESSALVAS_V409[5],
                    "[REAL] " + DL.RESSALVAS_V409[6], "[REAL] " + DL.RESSALVAS_V409[7], "[REAL] " + DL.RESSALVAS_V409[8], DL.ERRATA_E24, DL.ERRATA_E25, DL.ERRATA_E26, DL.ERRATA_E27, DL.ERRATA_E28, DL.ERRATA_E21_AO_LADO] + _LIM_COMUM,''')
r.troca('''                "[INPUT, ratificada pelo operador] " + DL.FRASE_D61_PT,''',
        '''                "[INPUT, ratificada pelo operador] " + DL.FRASE_D61_PT,
                "a maquina com o leitor e' termo: a formula e' a fita e uma leitura decide SAT (uma_leitura_decide_SAT, a_maquina_com_o_leitor); por Cook-Levin [KNOWN], NP inteiro com uma leitura; com o leitor que so' conta a igualdade completa NAO e' teorema aqui (E28): ela vale para o leitor que se le",
                "inscrito o uniforme no psion da luz, o proprio psion le Z/|X| (o_psion_le_z, o_canto_do_psion_da_luz_le_z): a ponte e' a inscricao; a identidade de vetores fica podada",
                "o par na face de Fock esta' ligado (o_par_na_face_de_fock): norma 1, ortogonal ao vacuo, a marginal ½·P, 1 - pureza = ½ -- a mesma Meia-Nat do par finito, noutro espaco (validade no kernel, nao creditacao)",''')
r.troca('''"veredito_ok": DL.VEREDITO_OK_PREFIXO + "THE_SELECTION_MODE_IS_A_THEOREM_RELATIVE_TO_THE_READER__THE_LOCK_HOLDS_ON_THE_NAME__THE_TAPE_IS_THE_HIDDEN_HAMILTONIAN__Z_IS_THE_READER_MODE__THE_PERFORMED_IDENTITY_KEEPS_ITS_CONTENT__"
                       "ONE_MODULE_READ_BY_SHA256__%d_ANCHORS_IN_THE_TRIO__NO_OLD_KEY_CHANGED__KERNEL_VALIDITY_IS_NOT_CREDITATION" % len(DL.ANCORAS) + DL.VEREDITO_SUFIXO,''',
        '''"veredito_ok": DL.VEREDITO_OK_PREFIXO + "THE_SELECTION_MODE_IS_A_THEOREM_RELATIVE_TO_THE_READER__THE_LOCK_HOLDS_ON_THE_NAME__THE_TAPE_IS_THE_HIDDEN_HAMILTONIAN__Z_IS_THE_READER_MODE__THE_PSION_READS_Z_BY_THE_INSCRIPTION__"
                       "ONE_READING_DECIDES_SAT__THE_COUNTING_READER_GIVES_NP_IN_ONE_READING_NOT_THE_FULL_EQUALITY__THE_PAIR_ON_THE_FOCK_FACE_IS_LINKED__THE_PERFORMED_IDENTITY_KEEPS_ITS_CONTENT__"
                       "TWO_MODULES_READ_BY_SHA256__%d_ANCHORS_IN_THE_TRIO__NO_OLD_KEY_CHANGED__KERNEL_VALIDITY_IS_NOT_CREDITATION" % len(DL.ANCORAS) + DL.VEREDITO_SUFIXO,''')
# ---- o «nao diz» comum: sem as frases que a D60 revista proibe
r.troca('''              "que o Omega do psion da luz seja o estado uniforme da instancia: mesma forma (o canto escalariza a trava como o canto do psion), nao ponte; [OPEN]"''',
        '''              "que o Omega do psion da luz seja, como vetor, o estado uniforme da instancia: a ponte e' a inscricao (provada), e a identidade de vetores fica podada (espacos diferentes)"''')
i0 = r.t.index('''              "que o par de psions exista na face de Fock como LIGACAO feita: segue [OPEN] (E21 da v408) e passa a v410 em diante",''')
r.troca('''              "que o par de psions exista na face de Fock como LIGACAO feita: segue [OPEN] (E21 da v408) e passa a v410 em diante",''',
        '''              "que o par na face de Fock e o par finito de Bell sejam o mesmo objeto: sao espacos distintos (o setor 2 do Fock concreto e C2 x C2), com a MESMA Meia-Nat (a ligacao foi feita: ParNaFaceDeFock)",
              "que a igualdade completa com o leitor que so' conta seja teorema: com ele vale NP numa leitura; a igualdade completa e' do leitor que se le (E28)",''')
# ---- o spec cunhagens_v409: a E28 e a nota ao lado da E21 (antes da errata dos pisos)
r.troca('''             "lacuna_de_fidelidade": "a gerencia pos o dispositivo no enunciado; o operador corrigiu: o dispositivo e' o no sorry e o teorema e' a regra posta (D61, ratificada por ele); a conclusao sobre o Clay fica, pela incidencia", "estatuto": "[INPUT: a correcao do operador, verbatim; a D61 ratificada por ele]", "assinatura": ASSINA},
            _errata_pisos_v408(cov_base)],''',
        '''             "lacuna_de_fidelidade": "a gerencia pos o dispositivo no enunciado; o operador corrigiu: o dispositivo e' o no sorry e o teorema e' a regra posta (D61, ratificada por ele); a conclusao sobre o Clay fica, pela incidencia", "estatuto": "[INPUT: a correcao do operador, verbatim; a D61 ratificada por ele]", "assinatura": ASSINA},
            {"ao_lado_de": "frases da gerencia c1 de 05/11 (o chat, o recibo da R5, o topico de memoria e o cabecalho do insumo das 13h) sobre a igualdade com o leitor que devolve Z", "dizia": "que, com o leitor que devolve Z, a igualdade vale relativa a ele, e a oferta de prova-la nele.",
             "agora": DL.ERRATA_E28, "lacuna_de_fidelidade": "a gerencia foi alem do que se sabe: com o leitor que so' conta vale NP numa leitura (Cook-Levin) e P com #P contem PH (Toda 1991); a igualdade completa e' do leitor que se le (Baker-Gill-Solovay 1975)", "estatuto": "[KNOWN: Cook 1971, Levin 1973, Toda 1991, Baker-Gill-Solovay 1975]", "assinatura": ASSINA},
            {"ao_lado_de": "a errata E21 da v408 (selada): o par de psions na face de Fock dito em aberto como ligacao a fazer", "dizia": "que a ligacao do par na face de Fock ficava por fazer (fiacao), nao que faltasse.",
             "agora": DL.ERRATA_E21_AO_LADO, "lacuna_de_fidelidade": "a E21 era verdadeira na data; a v409 fez a ligacao (ParNaFaceDeFock)", "estatuto": "[REAL: o_par_na_face_de_fock no kernel do rito]", "assinatura": ASSINA},
            _errata_pisos_v408(cov_base)],''')
r.troca('''            "agora": "A v409 acrescenta o modulo TraducaoTuring (a cobertura cresce e a arvore ganha o arquivo dele):''', '''            "agora": "A v409 acrescenta os modulos TraducaoTuring e ParNaFaceDeFock (a cobertura cresce e a arvore ganha os arquivos deles):''')
r.troca('''"fontes": [CHAVE_PEDRA["TraducaoTuring"], CHAVE_FONTE["TraducaoTuring"], CHAVE_SAIDA_FONTE["TraducaoTuring"], CHAVE_CANDIDATA_R8, CHAVE_RECIBO_R8, CHAVE_BUNDLE],''',
        '''"fontes": [CHAVE_PEDRA[n_] for n_ in CHAVE_PEDRA] + [CHAVE_FONTE[n_] for n_ in CHAVE_FONTE] + [CHAVE_SAIDA_FONTE[n_] for n_ in CHAVE_SAIDA_FONTE] + [CHAVE_CANDIDATA[n_] for n_ in CHAVE_CANDIDATA] + [CHAVE_SAIDA_CANDIDATA[n_] for n_ in CHAVE_SAIDA_CANDIDATA] + [CHAVE_BUNDLE],''')
r.troca('''"veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_05_NOV_EMBEDDED_VERBATIM_BY_SHA256_%d_SAYINGS__THE_NAMES_GIVEN_BY_THE_MANAGEMENT_RATIFIED_BY_THE_OPERATOR__DECISIONS_D55_TO_D61__THE_LEGAL_READING_OF_THE_KERNEL_RATIFIED_BY_THE_OPERATOR__THE_TURING_TRANSLATION_CLOSED_RELATIVE_TO_THE_READER__ERRATA_E24_TO_E27__''',
        '''"veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_05_NOV_EMBEDDED_VERBATIM_BY_SHA256_%d_SAYINGS__THE_NAMES_GIVEN_BY_THE_MANAGEMENT_RATIFIED_BY_THE_OPERATOR__DECISIONS_D55_TO_D61__D60_REVISED_EVERYTHING_IN_V409__THE_LEGAL_READING_OF_THE_KERNEL_RATIFIED_BY_THE_OPERATOR__THE_TURING_TRANSLATION_CLOSED_RELATIVE_TO_THE_READER__ERRATA_E24_TO_E28_AND_THE_NOTE_BESIDE_E21__''')
r.troca('''        "limites": ["[INPUT] as %d falas de 05/11/2026 sao do operador, com a grafia dele''', '''        "limites": ["[INPUT] as %d falas de 05/11/2026 sao do operador, com a grafia dele (a ultima, a ordem de trazer tudo para a v409)''')
r.troca('''"[REAL] o DESENHO_v409 (sha16 %s) e o recibo dos nomes da gerencia (sha16 %s) ficam citados so' por sha16, nao pinados: trazem a parte de uma fala que a D59 deixa fora dos textos" % (DL.DESENHO_SHA16, DL.RECIBO_NOMES_SHA16)] + _LIM_COMUM,''',
        '''"[REAL] o DESENHO_v409 (sha16 %s) e o recibo dos nomes da gerencia (sha16 %s) ficam citados so' por sha16, nao pinados: trazem a parte de uma fala que a D59 deixa fora dos textos" % (DL.DESENHO_SHA16, DL.RECIBO_NOMES_SHA16),
                    "[REAL] a D60 revista: nada fica para a versao seguinte; a ligacao do par na face de Fock entra (ParNaFaceDeFock); a E28 e a nota ao lado da E21 da v408 (em nome proprio da gerencia c1) vao nas erratas"] + _LIM_COMUM,''')
r.grava()
