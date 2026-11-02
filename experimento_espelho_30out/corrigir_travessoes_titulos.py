# -*- coding: utf-8 -*-
"""Troca o '---' literal dos oito títulos \\section*{Leitura N --- ...} pelo travessão Unicode (a fonte dos títulos não tem
as ligaduras TeX). Backup de BYTES antes; temporário conferido; os.replace. Só toca os títulos; nada mais muda."""
import hashlib
import os
import re
import time
from pathlib import Path

MEMORIAL = Path(r"C:\IALD\Artigo\Haja_Luz\memorial_13ago2026\memorial.tex")
BS = chr(92)
pat = re.compile(re.escape(BS + "section*{Leitura ") + r"(\d) --- ")

raw = MEMORIAL.read_bytes()
t = raw.decode("utf-8")
hits = pat.findall(t)
print("títulos com --- :", len(hits))
if hits:
    ts = time.strftime("%Y%m%d_%H%M%S")
    bak = MEMORIAL.with_name(MEMORIAL.name + f".bak_{ts}")
    bak.write_bytes(raw)
    assert bak.read_bytes() == raw
    novo = pat.sub(lambda m: BS + "section*{Leitura " + m.group(1) + " \u2014 ", t).encode("utf-8")
    tmp = MEMORIAL.with_name(MEMORIAL.name + ".tmp_dash")
    tmp.write_bytes(novo)
    assert tmp.read_bytes() == novo
    os.replace(tmp, MEMORIAL)
    print("backup:", bak.name, "| antes", len(raw), "depois", len(novo), "| sha16", hashlib.sha256(novo).hexdigest()[:16])
    print("ainda com ---:", len(pat.findall(novo.decode("utf-8"))))
