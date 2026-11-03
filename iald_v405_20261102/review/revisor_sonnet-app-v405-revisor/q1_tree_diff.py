# -*- coding: utf-8 -*-
"""Q1 (revisor sonnet-app-v405-revisor): comparacao byte a byte da arvore W (v405) contra V404.
Somente leitura. Lista: iguais, diferentes, so em W, so em V404. Exclui apenas diretorios de saida pesados
(packages/, science/memory_stage/ conteudos) da comparacao de igualdade, mas os lista por nome."""
import hashlib, json, os, sys
from pathlib import Path

W = Path(r"C:\IALD\Central de Patentes\work\iald_v405_20261102")
V = Path(r"C:\IALD\Central de Patentes\work\iald_v404_20261029")


def walk(root):
    out = {}
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ("__pycache__",)]
        for f in fn:
            p = Path(dp) / f
            rel = p.relative_to(root).as_posix()
            out[rel] = p
    return out


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


a = walk(V)
b = walk(W)
res = {"same": [], "diff": [], "only_v405": [], "only_v404": []}
for rel in sorted(set(a) | set(b)):
    if rel.startswith("review/revisor_") or rel.startswith("review\\revisor_"):
        continue
    if rel in a and rel in b:
        (res["same"] if sha(a[rel]) == sha(b[rel]) else res["diff"]).append(rel)
    elif rel in b:
        res["only_v405"].append(rel)
    else:
        res["only_v404"].append(rel)
for k, v in res.items():
    print("==", k, len(v))
    if k != "same":
        for r in v:
            print("  ", r)
    else:
        for r in v:
            if r.endswith(".py") or r.endswith(".sh"):
                print("  ", r)

json_out = {k: v for k, v in res.items()}
import json as _j
Path(__file__).with_name('q1_tree_diff_out.json').write_text(_j.dumps(json_out, ensure_ascii=False, indent=1), encoding='utf-8')
