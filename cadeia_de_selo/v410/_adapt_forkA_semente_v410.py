# -*- coding: utf-8 -*-
"""_adapt_forkA_semente_v410.py -- (claude-construtor-v410, fork A, 06/11/2026) a SEMENTE dos textos da v410 = textos_v409.py FINAL (montado na v409) com os rotulos subidos pelo motor (_bump_copia_v410.py:
o pos_rito\\textos_v410.py que o bump gravou), so' com a marca [A ADAPTAR v410] trocada por uma nota e o fim de linha LF. A semente anterior (a subida da textos_v409.semente, que e' a textos_v408.py subida duas vezes) vai para backup.
Backup de BYTES dos dois arquivos antes; temporario -> tamanho -> substituicao; ast.parse."""
import ast, datetime, os
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pos_rito")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
src_p = os.path.join(HERE, "textos_v410.py"); dst_p = os.path.join(HERE, "textos_v410.semente")
raw = open(src_p, "rb").read(); t = raw.decode("utf-8").replace("\r\n", "\n")
ls = t.split("\n")
assert ls[1].startswith("# [A ADAPTAR v410] SUBIDA MECANICA DE ROTULO (v409->v410) do molde v409/pos_rito/textos_v409.py"), ls[1][:120]
ls[1] = "# [ADAPTADO v410, 06/11/2026, claude-construtor-v410 (fork A)] SEMENTE = textos_v409.py FINAL (montado na v409) com os rotulos subidos pelo motor (bump/pos_rito__textos_v410.py.diff); o cabecalho e as definicoes da v410 vem do fragmento textos_v410_novo.pysnip (montar_textos_v410.py)."
novo = "\n".join(ls)
ast.parse(novo)
for p in (src_p, dst_p):
    b = open(p, "rb").read(); bk = p + ".bak_" + TS + "_semente"; open(bk, "wb").write(b); assert open(bk, "rb").read() == b
nb = novo.encode("utf-8")
open(dst_p + ".tmp", "wb").write(nb); assert os.path.getsize(dst_p + ".tmp") == len(nb); os.replace(dst_p + ".tmp", dst_p)
print("textos_v410.semente:", len(nb), "B (de textos_v410.py subido:", len(raw), "B)")
