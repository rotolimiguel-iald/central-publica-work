# -*- coding: utf-8 -*-
"""03/11/2026 15:3x, gerencia c1 (R2): o ensaio a seco explicava a diferenca do selo em testemunha_estatica_v396 so' pela chave do lema (False -> True) e pelo dict elo_v407; com o C19b
o fock_face.reading tambem muda: ganha um PREFIXO quando o lema e' lido, e a frase antiga fica verbatim como sufixo. A explicacao passa a admitir exatamente isso (prefixo que diz que o lema
e' termo e que a frase que segue e' registro; sufixo == o reading da v406) e NADA mais. Backup de bytes; py_compile. Escrito pelo Write."""
import json, sys
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import patches  # noqa: E402
ARQ = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v407\ensaio_a_seco_v407.py"
O_A = '        return bool(fa_.get("linked_to_the_corner_by_a_lemma") is False and fb_.get("linked_to_the_corner_by_a_lemma") is True and "elo_v407" not in fa_ and isinstance(fb_.get("elo_v407"), dict)'
N_A = ('        _ra, _rb = str(fa_.get("reading")), str(fb_.get("reading"))   # [R2, 03/11; C19b] o reading ganha so\' um PREFIXO quando o lema e\' lido; a frase antiga fica, verbatim, como sufixo\n'
       '        _rd_ok = bool(_rb.endswith(_ra) and len(_rb) > len(_ra) and _rb[:-len(_ra)].startswith("since v407 the lemma of the two faces is a term of the kernel of the rite") and "kept as record: " in _rb[:-len(_ra)])\n'
       '        return bool(_rd_ok and fa_.get("linked_to_the_corner_by_a_lemma") is False and fb_.get("linked_to_the_corner_by_a_lemma") is True and "elo_v407" not in fa_ and isinstance(fb_.get("elo_v407"), dict)')
O_B = 'and {x_: v_ for x_, v_ in fa_.items() if x_ not in ("linked_to_the_corner_by_a_lemma",)} == {x_: v_ for x_, v_ in fb_.items() if x_ not in ("linked_to_the_corner_by_a_lemma", "elo_v407")}'
N_B = 'and {x_: v_ for x_, v_ in fa_.items() if x_ not in ("linked_to_the_corner_by_a_lemma", "reading")} == {x_: v_ for x_, v_ in fb_.items() if x_ not in ("linked_to_the_corner_by_a_lemma", "elo_v407", "reading")}'
O_C = '(ii) testemunha_estatica_v396: o fock_face ganha o dict elo_v407 e a chave linked passa de False a True, e NADA mais'
N_C = '(ii) testemunha_estatica_v396: o fock_face ganha o dict elo_v407, a chave linked passa de False a True e o reading ganha o prefixo do C19b (R2: a frase antiga fica como sufixo, verbatim), e NADA mais'


def f(s):
    for o in (O_A, O_B, O_C):
        assert s.count(o) == 1, ("nao esta UMA vez (%d): %s" % (s.count(o), o[:100]))
    return s.replace(O_A, N_A).replace(O_B, N_B).replace(O_C, N_C), ["_rd_ok (prefixo + sufixo verbatim)", "reading fora da igualdade do resto", "comentario (ii)"]


print(json.dumps(patches.aplicar_em_arquivo(ARQ, f, "r2_ensaio_c19b"), ensure_ascii=False)[:300])
