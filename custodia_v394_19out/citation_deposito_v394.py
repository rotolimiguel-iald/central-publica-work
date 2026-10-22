# -*- coding: utf-8 -*-
"""Custódia v394: a linha do depósito no CITATION.cff volta ao molde que os geradores leem («byte-identical to the seal: um.py sha256 …»)
e diz no passado que os 15 arquivos conferiam com o repositório NA v392 (a cabeça agora é a v394). Backup de bytes; temporário; troca."""
import os, time

P = r"C:\IALD\Artigo\the_boundary\CITATION.cff"
raw = open(P, "rb").read()
s = raw.decode("utf-8")
a = ("Zenodo deposit of v392, deposited 2026-10-14 (byte-identical to the v392 seal: um.py sha256 b590c0aa80055e2a\u2026; "
     "the 15 deposited files match this repository by md5)")
b = ("Zenodo deposit of v392, deposited 2026-10-14 (byte-identical to the seal: um.py sha256 b590c0aa80055e2a\u2026; "
     "the 15 deposited files matched this repository at v392 by md5)")
if b in s:
    print("já aplicado"); raise SystemExit
assert s.count(a) == 1, s.count(a)
s = s.replace(a, b)
open(P + ".bak_" + time.strftime("%Y%m%d_%H%M%S"), "wb").write(raw)
open(P + ".tmp", "wb").write(s.encode("utf-8"))
os.replace(P + ".tmp", P)
print("ok", len(raw), "->", os.path.getsize(P))
