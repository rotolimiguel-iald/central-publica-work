# -*- coding: utf-8 -*-
"""Parte 3 dos ajustes da v407, depois do 2o teste do escopo medido: um arquivo que passa de legivel a ilegivel (ou vice-versa) entre os dois snapshots
NAO e' mudanca confirmada, e' nao medido; antes ele era contado como 'changed'. Agora 'changed' so' conta arquivos legiveis nos dois lados (ou presentes em um lado so'). Uma troca, uma ocorrencia."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent
p = W / "transaction.py"
t = p.read_bytes().decode("utf-8")
eol = "\r\n" if "\r\n" in t else "\n"
velho = ("        changed = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))\n"
         "        unreadable = sorted({k for side in (a, b) for k, v in side.items() if 'error' in v})\n").replace("\n", eol)
novo = ("        bad = {k for side in (a, b) for k, v in side.items() if 'error' in v}\n"
        "        unreadable = sorted(bad)\n"
        "        changed = sorted(k for k in set(a) | set(b) if k not in bad and a.get(k) != b.get(k))   # ilegivel num dos lados = nao medido, nao mudanca\n").replace("\n", eol)
assert t.count(velho) == 1, t.count(velho)
p.write_bytes(t.replace(velho, novo).encode("utf-8"))
print(json.dumps({"ajustados": ["transaction.py"], "trocas": 1}))
