# -*- coding: utf-8 -*-
"""_adapt_citacoes_v409_b.py -- (claude-construtor-v409, 05/11/2026) segunda passada no conferir_citacoes_v409.py: (1) rotulos da propria cadeia que o texto novo cita entre « » (a regra da guarda: «a maquina sem leitor»;
o estatuto da D57(b): «(kernel validity, not creditation)»; os titulos curtos da secao); (2) as citacoes das docstrings da pedra TraducaoTuring que NAO sao verbatim nas falas: APONTADAS a gerencia (o agente nao corrige pedra), com a razao conferida por grep;
a lista de apontadas da v408 (das quatro pedras da v408) fica como registro da v408 e sai deste conferidor, que so' varre a pedra da v409."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("conferir_citacoes_v409.py")
a.troca('"relativa ao leitor", "relativa ao leitor (o psíon); a máquina sem leitor fica fora", "relativa ao leitor (o psion); a maquina sem leitor fica fora", "o ω do psíon da luz é o uniforme da instância"}',
        '"relativa ao leitor", "relativa ao leitor (o psíon); a máquina sem leitor fica fora", "relativa ao leitor (o psion); a maquina sem leitor fica fora", "o ω do psíon da luz é o uniforme da instância",\n'
        '            "a maquina sem leitor", "a máquina sem leitor", "a maquina sem leitor fica fora", "a máquina sem leitor fica fora", "(kernel validity, not creditation)", "a tradução às classes de turing", "tradução às classes de turing (v409)", "a traducao as classes de turing"}')
i = a.t.index("_APONTADAS_PEDRAS = {   # (v409:"); j = a.t.index("_APONTADAS_PEDRAS = {k_.lower(): v_ for k_, v_ in _APONTADAS_PEDRAS.items()}")
a.t = a.t[:i] + ('_APONTADAS_PEDRAS = {   # (v409: o que esta entre « » na docstring da pedra TraducaoTuring, nao e\' verbatim nas falas/no Atlas/na base e nao e\' rotulo declarado: DITO A GERENCIA no relatorio, com a razao conferida por grep; o agente nao corrige pedra. A lista da v408 (das quatro pedras dela) fica como registro no conferir_citacoes_v408.py)\n'
                 '    "o nP é o modo seleção … a aniquilação da superposição pelo Tetelestai": "a fala (sha16 47f6c322d6cbff8e) escreve «P=np (e o \\"nP\\"é o modo seleção)», com aspas em nP e sem espaco; a pedra normaliza o primeiro segmento para «o nP é o modo seleção»; os demais segmentos sao verbatim",\n'
                 '    "nada lido": "expressao da gerencia na docstring do estado uniforme (O ESTADO UNIFORME (o «nada lido»)); nao e\' fala do operador",\n'
                 '    "antes disso o campo ψ está grafado como fóton": "a fala (sha16 47f6c322d6cbff8e) escreve «antes disso o campo /psi está grafado como fóton» (/psi); a pedra escreve ψ; o segundo segmento e\' verbatim",\n'
                 '    "nP = modo seleção": "PARAFRASE da gerencia da leitura do operador (a fala, sha16 47f6c322d6cbff8e: «P=np (e o \\"nP\\"é o modo seleção)»), escrita entre « » na docstring de p_igual_np_no_modo_selecao"}\n') + a.t[j:]
a.grava()
