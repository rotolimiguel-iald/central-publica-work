# -*- coding: utf-8 -*-
"""Revisor v410 R1: o diff da correcao preparada (R2_aspas/AEscala.lean) contra a fonte ratificada (insumos/AEscala.lean): (a) so' mudam delimitadores de citacao? (b) quais trechos; (c) sha256 do arquivo; (d) apos o conserto, o resto do arquivo e' byte a byte igual? (e) os trechos que continuam com « » sao todos verbatim (rodado em e_citacoes_v410)."""
import difflib, hashlib, re, sys
sys.stdout.reconfigure(encoding="utf-8")
W = "C:/IALD/Central de Patentes/work/"
a = open(W + "cadeia_de_selo/v410/insumos/AEscala.lean", "rb").read()
b = open(W + "pedras_candidatas_09nov/R2_aspas/AEscala.lean", "rb").read()
print("insumos sha256", hashlib.sha256(a).hexdigest(), len(a))
print("R2      sha256", hashlib.sha256(b).hexdigest(), len(b))
at = a.decode("utf-8"); bt = b.decode("utf-8")
al = at.split("\n"); bl = bt.split("\n")
sm = difflib.SequenceMatcher(None, al, bl, autojunk=False)
n_lin = 0; fora = []; trocas = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal": continue
    n_lin += (i2 - i1)
    A = "\n".join(al[i1:i2]); B = "\n".join(bl[j1:j2])
    # normaliza: troca os delimitadores nos dois lados e compara
    An = A.replace("«", "<").replace("»", ">").replace("\u201c", "<").replace("\u201d", ">")
    Bn = B.replace("«", "<").replace("»", ">").replace("\u201c", "<").replace("\u201d", ">")
    if An != Bn: fora.append((i1 + 1, A[:300], B[:300]))
    trocas.append((i1 + 1, A.count("«"), B.count("«"), B.count("\u201c")))
print("linhas diferentes:", n_lin, "| hunks:", len(trocas), "| hunks cuja diferenca NAO e' so' troca de delimitador:", len(fora))
for f in fora: print("   FORA(linha %d):\n      A: %r\n      B: %r" % f)
print("« na fonte:", at.count("«"), "| « no R2:", bt.count("«"), "| \u201c no R2:", bt.count("\u201c"), "| \u201c na fonte:", at.count("\u201c"))
# o que mudou, em palavras: lista dos trechos que perderam « »
q = re.compile(r"«([^»]+)»")
qa = [x for x in q.findall(at)]; qb = [x for x in q.findall(bt)]
print("citacoes « » na fonte", len(qa), "| no R2", len(qb), "| perderam « »:", len(qa) - len(qb))
perd = [x for x in qa if x not in qb]
for x in perd: print("   perdeu « »:", x[:140].replace("\n", " "))
# cabecalho: a linha de convencao
for i, l in enumerate(bl[:30]):
    if "\u201c" in l or "convenç" in l.lower() or "aspas" in l.lower(): print("   cab L%d: %s" % (i + 1, l[:240]))
# diferencas de tamanho de linhas: linhas inseridas/removidas
print("linhas fonte", len(al), "R2", len(bl))
