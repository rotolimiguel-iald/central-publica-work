# -*- coding: utf-8 -*-
"""_fix_lista_vazia_v411.py -- (claude-construtor-v411, fork C, 12/11/2026) UMA rodada de conserto do achado do ensaio a seco da v411 na VARIANTE sem o registro (o pdflatex PARA em «Something's wrong--perhaps a missing
\\item»): quando o registro h0dn_bg1_v411 nao sela, o quadro do topo abria um itemize SEM \\item (as sete ressalvas nao foram lidas). A causa: a lista vazia. O conserto: com a lista vazia, UM item que diz que as ressalvas
nao foram lidas nesta rodada (o registro nao selou). Backup de BYTES antes; ancora unica; ast.parse depois. uso: python -B -X utf8 _fix_lista_vazia_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "quadro_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
a = '    ress_ = "".join(r"\\item[%d.] %s" % (i_ + 1, _v411_tex_unicode(x_)) for i_, x_ in enumerate(a_["ressalvas"]))\n'
n = ('    ress_ = "".join(r"\\item[%d.] %s" % (i_ + 1, _v411_tex_unicode(x_)) for i_, x_ in enumerate(a_["ressalvas"]))\n'
     '    if not ress_:   # (v411, achado do ensaio a seco: sem o registro, a lista ficava vazia e o pdflatex parava) um item que diz que as ressalvas nao foram lidas nesta rodada\n'
     '        ress_ = (r"\\item (nesta rodada o registro não selou: as sete ressalvas não foram lidas do texto embutido)" if lang_ == "pt" else r"\\item (this round the record did not seal: the seven reservations were not read from the embedded text)")\n')
assert t.count(a) == 1, t.count(a)
t = t.replace(a, n); ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_forkc"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
