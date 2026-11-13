# -*- coding: utf-8 -*-
"""RECONSTRUIR AS CÓPIAS (gerado pela esteira da Central pública da IALD; decisão do operador de 11/11/2026: a cópia vira referência).
Neste repositório, um arquivo idêntico, byte a byte, a outro já publicado aqui não se repete: o índice público o lista com o campo
"igual_a" (o caminho do original, com os mesmos bytes e o mesmo sha256). Num clone, este script recria cada cópia a partir do original
e confere o sha256 de cada uma. Só a biblioteca padrão.
Uso: python RECONSTRUIR_COPIAS.py [--conferir]   (--conferir: só confere os originais, não grava nada)"""
import hashlib, json, shutil, sys
from pathlib import Path

R = Path(__file__).resolve().parent


def entradas():
    cab = R / "INDICE_PUBLICO_PARTES" / "PARTES.json"
    if cab.is_file():
        for p in json.loads(cab.read_text(encoding="utf-8"))["partes"]:
            b = (R / p["arquivo"]).read_bytes()
            if hashlib.sha256(b).hexdigest() != p["sha256"]:
                sys.exit("parte do índice diferente do cabeçalho: %s" % p["arquivo"])
            yield from json.loads(b.decode("utf-8"))["arquivos"]
    else:
        yield from json.loads((R / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))["arquivos"]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def dentro(p):
    p = p.resolve()
    return p == R or R in p.parents


so_conferir = "--conferir" in sys.argv
visto, feitas, iguais, falhas = {}, 0, 0, 0
for a in entradas():
    o = a.get("igual_a")
    if not o:
        continue
    src, dst = R / o, R / a["caminho"]
    if not (dentro(src) and dentro(dst)):
        print("caminho fora do repositório:", a["caminho"]); falhas += 1; continue
    if o not in visto:
        visto[o] = sha(src) if src.is_file() else None
    if visto[o] != a["sha256"]:
        print("original ausente ou diferente do índice:", o); falhas += 1; continue
    if dst.is_file() and sha(dst) == a["sha256"]:
        iguais += 1; continue
    if so_conferir:
        continue
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    feitas += 1
print("cópias recriadas: %d | já presentes: %d | originais conferidos: %d | falhas: %d" % (feitas, iguais, len(visto), falhas))
sys.exit(1 if falhas else 0)
