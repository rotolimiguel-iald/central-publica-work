# -*- coding: utf-8 -*-
"""03/11/2026 15:1x, gerencia c1 (R2): a guarda do gerar_candidato_v407.py («as duas funcoes tocadas: so' as linhas dos patches C19/C20 mudam») pegou, na primeira regeracao R2,
que o patch C19b (OLD_RD/NEW_RD: o campo fock_face.reading da testemunha ramifica pela chave lida) nao estava na sua lista branca. Aqui a lista branca ganha o RD e o numero de linhas
removidas esperado passa a ser por funcao (testemunha: C19 + C19b = 2; fechamento: C20 = 1). Backup de bytes pelo patches.aplicar_em_arquivo; py_compile depois. Escrito pelo Write."""
import json, sys
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import patches  # noqa: E402
ARQ = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v407\gerar_candidato_v407.py"
O1 = '    _old_lines = set((OLD_TE + OLD_C8).replace("\\r\\n", "\\n").split("\\n")); _new_lines = set((NEW_TE + NEW_C8).replace("\\r\\n", "\\n").split("\\n"))'
N1 = ('    _old_lines = set((OLD_TE + "\\n" + OLD_C8 + "\\n" + OLD_RD).replace("\\r\\n", "\\n").split("\\n")); _new_lines = set((NEW_TE + "\\n" + NEW_C8 + "\\n" + NEW_RD).replace("\\r\\n", "\\n").split("\\n"))'
      '   # [R2, 03/11] o C19b (OLD_RD/NEW_RD: o reading ramifica pela chave) entra na lista branca; a guarda pegou a omissao na primeira regeracao R2')
O2 = '    assert len(rem) == 1 and "_v407_elo_lido" in "\\n".join(s1) and "_v407_elo_lido" not in "\\n".join(s0), (fname, len(rem))'
N2 = ('    assert len(rem) == {"testemunha_estatica_v396": 2, "v406_fechamento_mechanics": 1}[fname] and "_v407_elo_lido" in "\\n".join(s1) and "_v407_elo_lido" not in "\\n".join(s0), (fname, len(rem))'
      '   # [R2] testemunha: C19 + C19b; fechamento: C20')
O3 = "# as duas funcoes tocadas: so' as linhas dos patches C19/C20 mudam"
N3 = "# as duas funcoes tocadas: so' as linhas dos patches C19/C19b/C20 mudam"


def f(s):
    for o in (O1, O2, O3):
        assert s.count(o) == 1, ("nao esta UMA vez (%d): %s" % (s.count(o), o[:100]))
    return s.replace(O1, N1).replace(O2, N2).replace(O3, N3), ["lista branca com RD", "rem esperado por funcao", "comentario"]


print(json.dumps(patches.aplicar_em_arquivo(ARQ, f, "r2_guarda_c19b"), ensure_ascii=False)[:300])
