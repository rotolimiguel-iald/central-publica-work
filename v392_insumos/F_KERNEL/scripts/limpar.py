# -*- coding: utf-8 -*-
"""Limpeza SEGURA do sandbox F_KERNEL (licao do incidente da 1a execucao: um filtro do PowerShell foi ignorado e tudo
foi apagado). Regras: (1) so apaga DENTRO de F_KERNEL; (2) so as pastas nomeadas (tc, ov, demo_build) e arquivos cujo nome
termina em .olean/.ilean; (3) lista tudo antes; (4) recusa se algum alvo nao obedecer as regras; (5) usa o prefixo \\\\?\\;
(6) depois confere que o resto do sandbox ficou (contagem dos arquivos que NAO eram alvo, antes e depois).
Uso: python -I limpar.py listar|apagar"""
import json
import os
import shutil
import sys

F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assert F.lower().endswith(os.path.join("exame12", "f_kernel")), F
PASTAS = ["tc", "ov", "demo_build"]
EXT = (".olean", ".ilean")
LP = lambda p: "\\\\?\\" + os.path.abspath(p)


def inventario():
    alvos_pastas = [os.path.join(F, d) for d in PASTAS if os.path.isdir(os.path.join(F, d))]
    alvos_arq, resto = [], []
    for r, ds, fs in os.walk(F):
        if any(os.path.abspath(r).startswith(os.path.abspath(p)) for p in alvos_pastas):
            continue
        for f in fs:
            p = os.path.join(r, f)
            (alvos_arq if f.lower().endswith(EXT) else resto).append(p)
    return alvos_pastas, alvos_arq, resto


def contar(p):
    n = s = 0
    for r, ds, fs in os.walk(LP(p)):
        for f in fs:
            n += 1
            s += os.path.getsize(os.path.join(r, f))
    return n, s


modo = sys.argv[1]
pastas, arqs, resto = inventario()
for p in pastas + arqs:
    ap = os.path.abspath(p)
    assert ap.startswith(os.path.abspath(F) + os.sep), ap
    assert (os.path.basename(ap) in PASTAS and os.path.dirname(ap) == os.path.abspath(F)) or ap.lower().endswith(EXT), ap
rel = {"pastas": [(os.path.relpath(p, F),) + contar(p) for p in pastas], "arquivos_olean_ilean": [os.path.relpath(p, F) for p in arqs],
       "outros_arquivos_que_ficam": len(resto)}
print(json.dumps({k: (v if k != "arquivos_olean_ilean" else len(v)) for k, v in rel.items()}, ensure_ascii=False))
if modo == "apagar":
    for p in pastas:
        shutil.rmtree(LP(p))
    for p in arqs:
        os.remove(LP(p))
    p2, a2, r2 = inventario()
    rel["depois"] = {"pastas_restantes": [os.path.relpath(p, F) for p in p2], "olean_ilean_restantes": len(a2), "outros_arquivos": len(r2)}
    assert not p2 and not a2, rel["depois"]
    assert len(r2) >= len(resto), ("arquivos que nao eram alvo sumiram", len(resto), len(r2))
    out = os.path.join(F, "LIMPEZA.json")
    open(out, "w", encoding="utf-8").write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps(rel["depois"], ensure_ascii=False))
