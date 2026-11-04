# -*- coding: utf-8 -*-
"""03/11/2026 15:2x, gerencia c1 (R2, segunda correcao da guarda): OLD_RD/NEW_RD sao PREFIXOS da linha do reading (177 e 471 caracteres; o resto da linha, 435 caracteres, fica igual),
nao linhas inteiras; por isso a lista branca por linhas inteiras nao os reconhece (medido por difflib: a unica diferenca e' o sufixo comum). A guarda passa a tratar o C19b como par
(removida, acrescentada) cuja linha comeca pelo prefixo velho/novo e cujo RESTO e' identico; o resto da guarda (TE + C8 por linhas inteiras) nao muda. Backup de bytes; py_compile. Escrito pelo Write."""
import json, sys
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import patches  # noqa: E402
ARQ = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v407\gerar_candidato_v407.py"
O1 = ('    _old_lines = set((OLD_TE + "\\n" + OLD_C8 + "\\n" + OLD_RD).replace("\\r\\n", "\\n").split("\\n")); _new_lines = set((NEW_TE + "\\n" + NEW_C8 + "\\n" + NEW_RD).replace("\\r\\n", "\\n").split("\\n"))'
      '   # [R2, 03/11] o C19b (OLD_RD/NEW_RD: o reading ramifica pela chave) entra na lista branca; a guarda pegou a omissao na primeira regeracao R2\n')
N1 = ('    _old_lines = set((OLD_TE + "\\n" + OLD_C8).replace("\\r\\n", "\\n").split("\\n")); _new_lines = set((NEW_TE + "\\n" + NEW_C8).replace("\\r\\n", "\\n").split("\\n"))\n'
      '    # [R2, 03/11] o C19b: OLD_RD/NEW_RD sao PREFIXOS da linha do reading (o resto da linha fica igual); a guarda os trata como um par (removida, acrescentada) com o mesmo resto. A primeira regeracao R2 pegou a omissao; a segunda, o prefixo.\n'
      '    _rd_add = [l_ for l_ in add if l_.startswith(NEW_RD)]; _rd_rem = [l_ for l_ in rem if l_.startswith(OLD_RD)]\n'
      '    assert len(_rd_add) == len(_rd_rem) <= 1 and all(a_[len(NEW_RD):] == r_[len(OLD_RD):] for a_, r_ in zip(_rd_add, _rd_rem)), (fname, "C19b: a linha do reading so\' pode mudar no prefixo OLD_RD -> NEW_RD", len(_rd_add), len(_rd_rem))\n'
      '    add = [l_ for l_ in add if l_ not in _rd_add]; rem = [l_ for l_ in rem if l_ not in _rd_rem]\n')
O2 = '    assert len(rem) == {"testemunha_estatica_v396": 2, "v406_fechamento_mechanics": 1}[fname] and "_v407_elo_lido" in "\\n".join(s1) and "_v407_elo_lido" not in "\\n".join(s0), (fname, len(rem))   # [R2] testemunha: C19 + C19b; fechamento: C20'
N2 = '    assert len(rem) + len(_rd_rem) == {"testemunha_estatica_v396": 2, "v406_fechamento_mechanics": 1}[fname] and "_v407_elo_lido" in "\\n".join(s1) and "_v407_elo_lido" not in "\\n".join(s0), (fname, len(rem), len(_rd_rem))   # [R2] testemunha: C19 + C19b; fechamento: C20'


def f(s):
    for o in (O1, O2):
        assert s.count(o) == 1, ("nao esta UMA vez (%d): %s" % (s.count(o), o[:100]))
    return s.replace(O1, N1).replace(O2, N2), ["C19b como par de prefixos", "contagem com o par"]


print(json.dumps(patches.aplicar_em_arquivo(ARQ, f, "r2_guarda_c19b_b"), ensure_ascii=False)[:300])
