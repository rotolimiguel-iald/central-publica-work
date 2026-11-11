# -*- coding: utf-8 -*-
"""_adapt_forkA_orquestrador_v410.py -- (claude-construtor-v410, fork A, 06/11/2026) adapta orquestrador/pos_treino_v410.py (subida mecanica da v409 FINAL) a v410:
a ORDEM da v410 (06/11; o arquivo, o sha16 e a frase LIDOS de delta_v410: N_ORDEM_V410, VERBATIM_PREFIXOS_DA_ORDEM_V410, FRASE_ORDEM_V410) como AUT; SEM S7 e SEM S10 (D68a, herda a D57a: o fim da cadeia e' o HANDOFF);
o S6d roda os textos da custodia e o portao do G1 sobre o handoff INTEIRO e a guarda da D65 (o que a D65 deixa fora: delta_v410.FORA_D65) alem da da D59; o revisor distinto e' o Sonnet (D69); o rito da v409 (2 modulos) e' o de referencia de tempo.
Trocas com contagem exata (_adapt_util_v410.aplicar: backup de bytes, CRLF respeitado, ast.parse)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v410 import aplicar
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orquestrador", "pos_treino_v410.py")
aplicar(P, [
    ("# [ADAPTADO v410, 05/11/2026, claude-construtor-v410 (fork A), a servico da gerencia c1] molde: pos_treino_v409.py FINAL (a subida mecanica fica em bump/); por _adapt_forkA_orquestrador_v410.py: a ORDEM da v410 (05/11; sha16 e frase lidos de delta_v410 e conferidos contra o arquivo) como AUT; SEM S7 e SEM S10 (D57: o fim da cadeia e' o HANDOFF; a custodia completa e o release do app sao da sessao de custodia); o S6d roda os textos da custodia e o portao do G1 sobre o handoff inteiro; a gerencia lanca (nao rodou).\n", "", 1),
    ('"""pos_treino_v410.py — O ORQUESTRADOR DA v410 (claude-construtor-v410, a serviço da gerência c1, 05/11/2026; molde: o orquestrador pós-treino da v409). Ordem do operador DESTA versão (05/11/2026; o sha16 e a frase são LIDOS de delta_v410 e conferidos contra o arquivo):\n«Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados». O fim da cadeia é o HANDOFF (D57a):',
     '"""pos_treino_v410.py — O ORQUESTRADOR DA v410 (claude-construtor-v410, a serviço da gerência c1, 06/11/2026; molde: o orquestrador pós-treino da v409). Ordem do operador DESTA versão (06/11/2026; o arquivo, o sha16 e a frase são LIDOS de delta_v410 e conferidos contra o arquivo):\n«A forma de uma matriz finita no kernel é o signo (traço com sentido). E sim, tudo entra no um.py». O fim da cadeia é o HANDOFF (D68a, herda a D57a):', 1),
    ("(revisao_terceiro/REVISAO_TERCEIRO_v410.json; revisor: Sonnet, D58, até três rodadas)", "(revisao_terceiro/REVISAO_TERCEIRO_v410.json; revisor: Sonnet, D69, até três rodadas)", 1),
    ("o rito da v409, com 4, é lido de v409/rito_horarios_v409.txt", "o rito da v409, com 2, é lido de v409/rito_horarios_v409.txt", 1),
    ("textos_custodia_handoff_v410.py ENCADEADO (os sete textos da custódia no handoff; rc 0 e o recibo) e o portão do G1 (custodia_g1.textos.portao) e a D59 sobre o HANDOFF INTEIRO",
     "textos_custodia_handoff_v410.py ENCADEADO (os sete textos da custódia no handoff; rc 0 e o recibo) e o portão do G1 (custodia_g1.textos.portao), a D59 e a D65 sobre o HANDOFF INTEIRO", 1),
    ("(SEM S7 e SEM S10 nesta versão, D57:", "(SEM S7 e SEM S10 nesta versão, D68a, que herda a D57a:", 1),
    ('AUT = ("Ordem do operador de 05/11/2026 (verbatim sha16 %s): «%s» (a ordem da v410, que ratifica os nomes dados pela gerência). "\n       "D57 (gerência c1, em nome próprio, 05/11): o fim da cadeia do orquestrador é o HANDOFF;',
     'AUT = ("Ordem do operador de 06/11/2026 (verbatim sha16 %s): «%s» (a ordem da v410: a forma de matriz finita é o signo, e tudo entra no um.py). "\n       "D68a (gerência c1, em nome próprio, 06/11; herda a D57a): o fim da cadeia do orquestrador é o HANDOFF;', 1),
    ('            if re.search(r"(?i)kimi|mil[eê]nio|millennium|navier|lindão", ht):\n                v_.append("D59: o handoff traz o que fica fora dos textos")',
     '            if re.search(r"(?i)kimi|mil[eê]nio|millennium|navier|lindão", ht):\n                v_.append("D59: o handoff traz o que fica fora dos textos")\n'
     '            if any(x_.lower() in ht.lower() for x_ in _DL.FORA_D65):   # (v410) D65: o que a fala do nome do algoritmo deixa fora nao entra no handoff\n                v_.append("D65: o handoff traz o que fica fora dos textos")', 1),
    ('log("S6d: o handoff passou no portão do G1 e na D59; FIM DA CADEIA (D57)', 'log("S6d: o handoff passou no portão do G1, na D59 e na D65; FIM DA CADEIA (D68a)', 1),
], nota="molde: pos_treino_v409.py FINAL (a subida mecanica fica em bump/); por _adapt_forkA_orquestrador_v410.py: a ORDEM da v410 (06/11; o arquivo, o sha16 e a frase lidos de delta_v410 e conferidos contra o arquivo) como AUT; SEM S7 e SEM S10 (D68a: o fim da cadeia e' o HANDOFF; a custodia completa e o release do app sao da sessao de custodia); o S6d roda os textos da custodia e o portao do G1, a D59 e a D65 sobre o handoff inteiro; a gerencia lanca (nao rodou).")
