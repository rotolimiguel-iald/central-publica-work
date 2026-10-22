# -*- coding: utf-8 -*-
"""aplicar_bloco.py -- ferramenta do DELTA 19/10: troca um BLOCO de linhas de um script da cadeia por outro (lido de arquivo), entre duas ancoras (a primeira linha que COMECA com a ancora inicial; a ultima linha
que CONTEM a ancora final, a partir dali), com asserts de unicidade, backup de BYTES antes e substituicao atomica. Nao interpreta o conteudo.
uso: python -I -B -X utf8 aplicar_bloco.py <arquivo> <ancora_inicial> <ancora_final> <arquivo_do_bloco>"""
import os, sys, time
alvo, a_ini, a_fim, blk = sys.argv[1:5]
raw = open(alvo, "rb").read(); t = raw.decode("utf-8")
nl = "\r\n" if "\r\n" in t else "\n"
L = t.split(nl)
ini = [i for i, l in enumerate(L) if l.startswith(a_ini)]
assert len(ini) == 1, ("ancora inicial nao unica", len(ini))
fim = [i for i, l in enumerate(L) if i >= ini[0] and a_fim in l]
assert fim, "ancora final ausente"
fim = fim[0]
novo = open(blk, "rb").read().decode("utf-8").replace("\r\n", "\n").rstrip("\n").split("\n")
L2 = L[:ini[0]] + novo + L[fim + 1:]
out = nl.join(L2)
bk = alvo + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_c1blk"
open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
tmp = alvo + ".tmp_blk"; open(tmp, "wb").write(out.encode("utf-8")); assert os.path.getsize(tmp) == len(out.encode("utf-8")); os.replace(tmp, alvo)
print("ok: linhas %d..%d (%d) trocadas por %d; backup %s" % (ini[0] + 1, fim + 1, fim - ini[0] + 1, len(novo), os.path.basename(bk)))
