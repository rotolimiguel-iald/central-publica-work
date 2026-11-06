# -*- coding: utf-8 -*-
"""_papeis_auxiliares_v409.py -- (claude-construtor-v409, 05/11/2026) as ancoras auxiliares da TraducaoTuring refeita (R9) que nao tem docstring ganham o papel escrito (como trava_smul e
leituraPerformada_e_a_leitura ja' tinham): o que cada enunciado diz, lido da assinatura dele na pedra."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
d = Arq("delta_v409.py")
d.troca('''    NS + "leituraPerformada_e_a_leitura": "(auxiliar) a leitura performada e' a leitura do psion na trava (a definicao desdobrada)",''',
        '''    NS + "leituraPerformada_e_a_leitura": "(auxiliar) a leitura performada e' a leitura do psion na trava (a definicao desdobrada)",
    NS + "travaOp_apply": "(auxiliar) o operador da trava aplicado a um vetor e' a trava daquele vetor (a definicao desdobrada)",
    NS + "inscricao_do_uniforme": "(auxiliar) a inscricao leva o uniforme da instancia no Omega do psion da luz",
    NS + "adjunta_da_inscricao_no_psion": "(auxiliar) a adjunta da inscricao leva o Omega do psion da luz de volta ao uniforme da instancia",
    NS + "custoCNF_cons": "(auxiliar) o custo da formula com uma clausula a mais e' o custo da clausula mais o custo do resto (depende so' de propext, subconjunto do trio)",
    NS + "custoCNF_zero_sse": "(auxiliar) o custo da formula e' zero exatamente quando a atribuicao satisfaz todas as clausulas",''')
d.grava()
