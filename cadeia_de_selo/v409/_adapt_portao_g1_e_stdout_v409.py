# -*- coding: utf-8 -*-
"""_adapt_portao_g1_e_stdout_v409.py -- (claude-construtor-v409, 05/11/2026) tres causas achadas pelo harness dos textos (fim_de_cadeia, 18:17), todas minhas, corrigidas na causa; nenhum teste relaxado:
 (1) o portao do G1 (S6d, D57): «provada» sem o estatuto na MESMA frase (o portao corta a frase em . ; : ! ?) em textos novos que entram no um.py e no handoff: a D60 revista e FECHADO_OMEGA_UNIFORME (delta_v409.py),
     o nao_diz do registro (registros_v409.py) e a anotacao da R5 no mapa (pos_rito/registrar_mapa_v409.py): cada um ganha «validade no kernel, nao creditacao» na propria frase;
 (2) a anotacao da R_INV no mapa ainda dizia «o par na face de Fock segue [OPEN] como ligacao (D60)» (F41, D60 revista): passa a dizer que esta' ligado nesta versao;
 (3) a leitura do pos-rito achava a linha do bloco da v409 no stdout pelo SINGULAR «modulo do bundle ok» (para nao casar a linha da v408, que diz «modulos»); com dois modulos o candidato imprime «modulos»:
     a leitura passa a ancorar a linha da v409 no CABECALHO do bloco («A TRADUCAO AS CLASSES DE TURING [v409»), a linha imediatamente anterior -- a v408 nao casa, e os numeros seguem conferidos um a um."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

d = Arq("delta_v409.py")
d.troca("do Omega do psion e do uniforme, a PONTE (a inscricao) esta' provada e a IDENTIDADE de vetores fica PODADA (espacos diferentes);",
        "do Omega do psion e do uniforme, a PONTE (a inscricao) esta' provada no kernel (validade no kernel, nao creditacao) e a IDENTIDADE de vetores fica PODADA (espacos diferentes);")
d.troca("o_canto_do_psion_da_luz_le_z), provada nesta versao;", "o_canto_do_psion_da_luz_le_z), provada nesta versao (validade no kernel, nao creditacao);")
d.grava()

g = Arq("registros_v409.py")
g.troca("a ponte e' a inscricao (provada), e a identidade de vetores fica podada (espacos diferentes)", "a ponte e' a inscricao (provada no kernel, validade no kernel e nao creditacao), e a identidade de vetores fica podada (espacos diferentes)")
g.grava()

m = Arq("pos_rito/registrar_mapa_v409.py")
m.troca("A ponte entre o Omega do psion da luz e o uniforme da instancia e' a inscricao, provada na R9 (inscricao; o_psion_le_z);", "A ponte entre o Omega do psion da luz e o uniforme da instancia e' a inscricao, provada na R9 (validade no kernel, nao creditacao; inscricao, o_psion_le_z);")
m.troca('''"o par na face de Fock segue [OPEN] como ligacao (D60).", refs=[R_PROG], estatuto="REAL (a leitura do kernel do rito e o registro herdado); OPEN (a ligacao do par na face de Fock)"))''',
        '''"o par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock; D60 revista), sem chave nova no inventario.", refs=[R_PROG, R_PARF], estatuto="REAL (a leitura do kernel do rito e o registro herdado; o par na face de Fock ligado na v409)"))''')
m.grava()

l = Arq("pos_rito/leitura_v409.py")
l.troca('''m_tt_ = re.search(r'ancoras ok = (\\d+)/(\\d+) ; modulo do bundle ok = (\\d+)/(\\d+) ; bandeiras True = (\\d+)/(\\d+) ; escada = (\\[.*?\\]) ; gate = (.*)$', out, flags=re.M)   # a linha do bloco A TRADUCAO AS CLASSES DE TURING («modulo», no singular; as dos blocos herdados dizem «modulos»)''',
        '''m_tt_ = re.search(r'^A TRADUCAO AS CLASSES DE TURING \\[v409[^\\n]*\\n  ancoras ok = (\\d+)/(\\d+) ; modulos do bundle ok = (\\d+)/(\\d+) ; bandeiras True = (\\d+)/(\\d+) ; escada = (\\[.*?\\]) ; gate = (.*)$', out, flags=re.M)   # a linha do bloco A TRADUCAO AS CLASSES DE TURING, ancorada no CABECALHO do bloco (dois modulos: diz «modulos», como as dos blocos herdados; o cabecalho a separa da linha da v408)''')
l.grava()
