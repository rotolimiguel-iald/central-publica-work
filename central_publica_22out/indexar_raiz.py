# -*- coding: utf-8 -*-
"""Põe no INDICE_PUBLICO.json de um preparo as linhas (bytes, sha256) dos arquivos que o gerador dos README grava na raiz — README.md,
PATENTES.md, vinculo_patentario.json —, acrescentando ou atualizando. Uso: indexar_raiz.py <pasta_do_preparo> [...]"""
import hashlib, json, os, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
for D in map(Path, sys.argv[1:]):
    IP = D / "INDICE_PUBLICO.json"
    idx = json.loads(IP.read_text(encoding="utf-8"))
    pos = {a["caminho"]: i for i, a in enumerate(idx["arquivos"])}
    feitos = []
    for nome in ("README.md", "PATENTES.md", "vinculo_patentario.json"):
        p = D / nome
        if not p.is_file():
            continue
        b = p.read_bytes()
        linha = {"caminho": nome, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
        if nome in pos:
            idx["arquivos"][pos[nome]] = linha
        else:
            idx["arquivos"].append(linha)
        feitos.append(nome)
    idx["n_arquivos"] = len(idx["arquivos"])
    t = IP.with_name(IP.name + ".tmp_raiz")
    t.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    os.replace(t, IP)
    print("%s: %s no índice | n_arquivos %d" % (D.name, feitos, idx["n_arquivos"]))
