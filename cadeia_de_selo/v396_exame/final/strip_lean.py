# -*- coding: utf-8 -*-
"""strip_lean.py -- remove comentarios Lean (blocos /- -/ aninhados, inclusive docstrings /-- e /-!, e linhas --) e normaliza espacos; imprime o sha16 do codigo
restante de cada arquivo e o diff de codigo entre os dois. uso: python strip_lean.py <a.lean> <b.lean>"""
import sys, re, hashlib, difflib
def strip(s):
    out, i, depth, n = [], 0, 0, len(s)
    while i < n:
        if s.startswith("/-", i):
            depth += 1; i += 2; continue
        if depth and s.startswith("-/", i):
            depth -= 1; i += 2; continue
        if depth:
            i += 1; continue
        if s.startswith("--", i):
            j = s.find("\n", i); i = n if j < 0 else j; continue
        if s[i] == '"':   # string literal: copia inteira
            j = i + 1
            while j < n and s[j] != '"':
                j += 2 if s[j] == "\\" else 1
            out.append(s[i:j + 1]); i = j + 1; continue
        out.append(s[i]); i += 1
    t = "".join(out)
    return [re.sub(r"\s+", " ", l).strip() for l in t.splitlines() if l.strip()]
A, B = (strip(open(p, encoding="utf-8").read()) for p in sys.argv[1:3])
h = lambda L: hashlib.sha256("\n".join(L).encode("utf-8")).hexdigest()[:16]
print("codigo A", h(A), len(A), "linhas | codigo B", h(B), len(B), "linhas | iguais:", A == B)
for l in list(difflib.unified_diff(A, B, lineterm="", n=0))[:40]:
    print(l[:200])
