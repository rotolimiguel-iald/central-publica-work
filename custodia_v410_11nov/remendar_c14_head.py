# -*- coding: utf-8 -*-
r"""Errata AO LADO no G1 (central.py, caminhos_a_commitar), 11/11/2026, claude-site-custodia: comparar contra o HEAD (worktree + indice), nao so
a worktree contra o indice. Na v410, a rodada 7 do C14 fez `git add` e parou na lista negra; na rodada 8 os arquivos ja estavam no indice,
`git diff --name-only` nao os via, e o C14 os preservou como «alheios» (148: os resultados dos 16 dispositivos e o Atlas). Bytes, CRLF, backup."""
import os
import shutil
import sys
import time

P = r"C:\IALD\Central de Patentes\tools\custodia_g1\central.py"
b = open(P, "rb").read()
assert b.count(b"\r\n") == b.count(b"\n"), "nao e CRLF puro"
shutil.copy2(P, P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_c14_contra_o_head")
t = b.decode("utf-8").replace("\r\n", "\n")
A1 = r'''    mod = util.git(cen, "diff", "--name-only", "--", "patents").splitlines() + util.git(cen, "ls-files", "--others", "--exclude-standard", "--", "patents").splitlines()'''
N1 = r'''    # AO LADO (11/11/2026, claude-site-custodia; v410): contra o HEAD (worktree + índice). Um C14 que parou depois do `git add` deixa os seus próprios
    # arquivos no índice; `git diff --name-only` (worktree x índice) não os via e a rodada seguinte os tomava por alheios.
    mod = util.git(cen, "diff", "HEAD", "--name-only", "--", "patents").splitlines() + util.git(cen, "ls-files", "--others", "--exclude-standard", "--", "patents").splitlines()'''
A2 = r'''    num = util.git(cen, "diff", "--numstat", "--", atlas).split()'''
N2 = r'''    num = util.git(cen, "diff", "HEAD", "--numstat", "--", atlas).split()     # AO LADO (11/11/2026, v410): contra o HEAD, pela mesma razão'''
for a, n in ((A1, N1), (A2, N2)):
    k = t.count(a)
    if k != 1:
        sys.exit("trecho encontrado %d vezes: %r" % (k, a[:80]))
    t = t.replace(a, n, 1)
nb = t.replace("\n", "\r\n").encode("utf-8")
tmp = P + ".tmp"
open(tmp, "wb").write(nb)
assert os.path.getsize(tmp) == len(nb)
os.replace(tmp, P)
print(len(b), "->", len(nb), "B | CRLF", nb.count(b"\r\n"), "| LF solto", nb.count(b"\n") - nb.count(b"\r\n"))
