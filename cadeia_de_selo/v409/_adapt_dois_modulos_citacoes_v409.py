# -*- coding: utf-8 -*-
"""_adapt_dois_modulos_citacoes_v409.py -- (claude-construtor-v409, 05/11/2026) a varredura das citacoes « » das pedras (conferir_citacoes_v409.py) achou, nas pedras NOVAS da v409 (TraducaoTuring da R9;
ParNaFaceDeFock), tres trechos entre « » que nao sao verbatim das falas nem da base. As pedras sao da gerencia, pinadas no bundle; o agente nao corrige pedra: os tres vao para _APONTADAS_PEDRAS, DITOS A GERENCIA
no relatorio, cada um com a razao conferida por grep em 05/11 ~18h (a reprovacao nao e' silenciada: a lista e o porque ficam no JSON e no relatorio):
 (1) TraducaoTuring, l.87: «com ele a igualdade vale relativa a ele» -- a FRASE DA GERENCIA que a errata E28 corrige, citada na docstring como o que estava errado; nao e' fala do operador;
 (2) TraducaoTuring, l.100: «Ω é o uniforme» -- a formulacao que a D60 revista PODA (a identidade de vetores), citada como o que fica podado; nao e' fala do operador;
 (3) ParNaFaceDeFock, l.15-16: «eu quero que entre tudo na versão 409, não deixar nada para a v410» -- a fala (sha16 fb3dc69e3c9b5516) escreve «eu quero que entre tudo na versão 409 não deixar nada para a v410, senão ...»,
     SEM a virgula depois de 409; a pedra insere a virgula (o resto do trecho e' verbatim)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("conferir_citacoes_v409.py")
a.troca('''_APONTADAS_PEDRAS = {   # (v409: o que esta entre « » na docstring da pedra TraducaoTuring,''', '''_APONTADAS_PEDRAS = {   # (v409: o que esta entre « » nas docstrings das pedras TraducaoTuring e ParNaFaceDeFock,''')
a.troca('''    "nP = modo seleção": "PARAFRASE da gerencia da leitura do operador (a fala, sha16 47f6c322d6cbff8e: «P=np (e o \\"nP\\"é o modo seleção)»), escrita entre « » na docstring de p_igual_np_no_modo_selecao"}''',
        '''    "nP = modo seleção": "PARAFRASE da gerencia da leitura do operador (a fala, sha16 47f6c322d6cbff8e: «P=np (e o \\"nP\\"é o modo seleção)»), escrita entre « » na docstring de p_igual_np_no_modo_selecao",
    "com ele a igualdade vale relativa a ele": "FRASE DA GERENCIA (05/11) que a errata E28 corrige, citada entre « » na docstring da TraducaoTuring (R9) como o que estava errado; nao e' fala do operador",
    "Ω é o uniforme": "a formulacao que a D60 revista PODA (a identidade de vetores Omega = uniforme), citada entre « » na docstring da TraducaoTuring (R9) como o que fica PODADO; nao e' fala do operador",
    "eu quero que entre tudo na versão 409, não deixar nada para a v410": "a fala (sha16 fb3dc69e3c9b5516) escreve «eu quero que entre tudo na versão 409 não deixar nada para a v410, senão ...», SEM a virgula depois de 409; a pedra ParNaFaceDeFock insere a virgula; o resto do trecho e' verbatim"}''')
a.grava()
