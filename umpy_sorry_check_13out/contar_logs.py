# -*- coding: utf-8 -*-
"""Conta (so leitura) os dois formatos da mensagem de sorry do Lean no bancada_corpus do Nos."""
import json, collections
from pathlib import Path
B = Path(r"C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/bancada_corpus")
OUT = Path(r"C:/IALD/Central de Patentes/work/umpy_sorry_check_13out")
F_BT = b"declaration uses `sorry`"
F_SQ = b"declaration uses 'sorry'"
by_ext = collections.Counter(); by_ext_sq = collections.Counter(); files_bt = collections.Counter(); n_files = 0
for p in B.rglob("*"):
    if not p.is_file():
        continue
    n_files += 1
    try:
        d = p.read_bytes()
    except OSError:
        continue
    a, b = d.count(F_BT), d.count(F_SQ)
    ext = p.suffix.lower() or "(sem)"
    if a:
        by_ext[ext] += a; files_bt[ext] += 1
    if b:
        by_ext_sq[ext] += b
res = {"dir": str(B), "n_files": n_files, "backtick_by_ext": dict(by_ext), "backtick_files_by_ext": dict(files_bt),
       "backtick_total": sum(by_ext.values()), "single_quote_by_ext": dict(by_ext_sq), "single_quote_total": sum(by_ext_sq.values())}
(OUT / "contagem_formatos_logs.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(res, ensure_ascii=False, indent=1))
