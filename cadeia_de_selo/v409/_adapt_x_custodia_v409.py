# -*- coding: utf-8 -*-
"""_adapt_x_custodia_v409.py -- (claude-construtor-v409) a previa do post do X da custodia (pos_rito/gerar_x_custodia_v409.py) reprovou na guarda das frases: F41 («o par de psions na face de Fock segue em aberto como
ligacao», D60 revista) e F43 (o leitor que devolve Z aparece nas ressalvas, cortadas a 120 caracteres, e o corte tira as marcas da E28). A causa e' o texto do post: o par passa a LIGADO, a E28 e' dita inteira numa
frase propria do post (NP contido em P numa leitura; a igualdade completa e' a do leitor que se le), e o post diz os dois modulos. A guarda nao muda."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("pos_rito/gerar_x_custodia_v409.py")
a.troca('''O que entrou: a tradução às classes de Turing. {DL.N_BUNDLE} módulo novo no kernel Lean ({nomes}, nome dado pela gerência e ratificado pelo operador: «{DL.FRASE_NOMES_RATIFICADOS_V409}»),''',
        '''O que entrou: a tradução às classes de Turing e o par na face de Fock. {DL.N_BUNDLE} módulos novos no kernel Lean ({nomes}; os nomes dados pela gerência, os da TraducaoTuring ratificados pelo operador: «{DL.FRASE_NOMES_RATIFICADOS_V409}»),''')
a.troca('''· O alcance: {DL.FRASE_D56_PT}. Validade no kernel, não creditação.''',
        '''· O alcance: {DL.FRASE_D56_PT}. Validade no kernel, não creditação. Com o leitor que só conta, vale NP contido em P numa leitura (Cook 1971, Levin 1973); a igualdade completa é a do leitor que se lê, que lê também as máquinas que o usam (Baker–Gill–Solovay 1975): é a errata E28.''')
a.troca('''o par de psíons na face de Fock segue em aberto como ligação; β_TGL na natureza a 5σ segue em aberto.''',
        '''o par de psíons na face de Fock está ligado nesta versão (ParNaFaceDeFock; validade no kernel, não creditação); β_TGL na natureza a 5σ segue em aberto.''')
a.grava()
