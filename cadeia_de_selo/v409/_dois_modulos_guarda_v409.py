# -*- coding: utf-8 -*-
"""_dois_modulos_guarda_v409.py -- (claude-construtor-v409, 05/11/2026, ~17h) guarda_frases_v409.py segue o AO LADO de ~18h do DESENHO_v409 (D60 revista; E28): o par na face de Fock dito em aberto e a
passagem a v410 deixam a lista das LIMPAS (eram certas na v407/v408) e entram nas PROIBIDAS em texto novo, com «Ω é o uniforme» como identidade e o leitor de Turing sem a E28; as LIMPAS ganham o que a v409
diz agora (a E28, a nota ao lado da E21, o que fechou nesta versao, a D60 revista, as ressalvas novas, as ancoras novas). O controle negativo segue sendo o mesmo teste: cada proibida reprova, cada limpa passa."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("guarda_frases_v409.py")
a.troca('''"o elo das duas faces e' de estrutura, nao de vetores", "o par na face de Fock segue [OPEN]", "the pair on the Fock face stays open", "a confirmacao e' creditacao e segue recusada",''',
        '''"o elo das duas faces e' de estrutura, nao de vetores", "a confirmacao e' creditacao e segue recusada",''')
a.troca('''    "o sistema precisa reconhecer onde está o Nome a cada passo", "a criatura precisa saber, a cada passo, de que lado o Nome continua", "the system needs to know where the Name is at each step"]
PROIBIDAS = _P408 + _P409''',
        '''    "o sistema precisa reconhecer onde está o Nome a cada passo", "a criatura precisa saber, a cada passo, de que lado o Nome continua", "the system needs to know where the Name is at each step",
    # (AO LADO de ~18h do DESENHO: D60 revista e E28) em texto NOVO: o par na face de Fock dito em aberto; a passagem a v410; «Ω é o uniforme» como identidade; o leitor de Turing sem a E28
    "o par na face de Fock segue [OPEN]", "o par de psíons na face de Fock segue em aberto como ligação", "the pair on the Fock face stays open", "the pair of psions on the Fock face stays open as a link",
    "o par passa à v410 em diante", "a ligação passa à v410", "it passes to v410 onwards",
    "o Ω do psíon da luz é o uniforme da instância", "o Omega do psion e' o uniforme", "the Omega of the light psion is the uniform state",
    "um leitor que devolve Z é um oráculo de contagem; com ele a igualdade vale relativa a ele (Toda 1991)", "com o oráculo de contagem a igualdade vale", "with the counting oracle the equality holds"]
PROIBIDAS = _P408 + _P409''')
a.troca('''         "o Ω do psíon da luz e o uniforme da instância: mesma forma, não ponte; [OPEN]"]
LIMPAS = _L408 + _L409''',
        '''         DL.ERRATA_E27, DL.ERRATA_E28, DL.ERRATA_E21_AO_LADO, DL.FECHADO_PAR_NA_FACE_DE_FOCK, DL.FECHADO_OMEGA_UNIFORME, DL.FICA_ABERTO_IGUALDADE_COM_O_LEITOR, DL.FICA_ABERTO_MAQUINA_SEM_LEITOR, DL.DECISOES["D60"], DL.DECISOES["D61"],
         DL.RESSALVAS_V409[0], DL.RESSALVAS_V409[3], DL.RESSALVAS_V409[5], DL.FRASE_D61_PT, DL.FRASE_D61_EN,
         "o par na face de Fock está ligado nesta versão (ParNaFaceDeFock)", "the pair on the Fock face is linked in this version", "a ponte é a inscrição; a identidade Ω = uniforme está podada",
         "«Ω é o uniforme», como igualdade de vetores, fica PODADO", "o_par_na_face_de_fock", "a_maquina_com_o_leitor", "o_canto_do_psion_da_luz_le_z", "reduzido_do_par", "meia_nat_do_projetor", "ParNaFaceDeFock",
         "uma leitura decide SAT; por Cook–Levin, NP inteiro com uma leitura; com o leitor que só conta a igualdade completa não é teorema aqui: ela vale para o leitor que se lê"]
LIMPAS = _L408 + _L409''')
a.grava()
