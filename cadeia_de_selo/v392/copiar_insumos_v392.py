# -*- coding: utf-8 -*-
"""copiar_insumos_v392.py -- P11: copia para C:\\IALD\\Central de Patentes\\work\\v392_insumos\\ os insumos que a cadeia v392 le de pastas NAO duraveis (scratchpad exame12),
conferindo sha256 da ORIGEM (contra a lista M10 da R2) e da COPIA. Caminhos relativos preservados (F_KERNEL/..., H_BANCADA/..., D_BANCADA/...). Idempotente; nunca apaga;
nao sobrescreve arquivo diferente (recusa). Grava INSUMOS_v392.json (origem, destino, bytes, sha256). Gerencia c1, 13/10/2026.
Uso: python -I -B -X utf8 copiar_insumos_v392.py"""
import hashlib, json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
M10 = os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD", "exame_12out", "J_SINTESE", "R2", "medidas", "M10_insumos_scratchpad_a_tornar_duraveis.json")
DEST = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "v392_insumos")
sha = lambda b: hashlib.sha256(b).hexdigest()
d = json.load(open(M10, encoding="utf-8")); base = d["base"]
os.makedirs(DEST, exist_ok=True)
rel, ok, n_novo, n_ja = [], True, 0, 0
for a in d["arquivos"]:
    src = os.path.join(base, *a["caminho"].split("/")); dst = os.path.join(DEST, *a["caminho"].split("/"))
    b = open(src, "rb").read()
    assert sha(b) == a["sha256"] and len(b) == a["bytes"], ("origem diferente da lista M10", a["caminho"])
    if os.path.exists(dst):
        assert sha(open(dst, "rb").read()) == a["sha256"], ("destino existe e difere: nao sobrescrevo", dst)
        n_ja += 1
    else:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst + ".tmp", "wb").write(b); assert sha(open(dst + ".tmp", "rb").read()) == a["sha256"]; os.replace(dst + ".tmp", dst); n_novo += 1
    rel.append({"caminho": a["caminho"], "origem": src, "destino": dst, "bytes": a["bytes"], "sha256": a["sha256"]})
out = {"quando": "13/10/2026 (rodada 2 da preparacao)", "origem_da_lista": M10, "destino": DEST, "n": len(rel), "novos": n_novo, "ja_existiam": n_ja, "arquivos": rel}
json.dump(out, open(os.path.join(DEST, "INSUMOS_v392.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("insumos:", len(rel), "novos", n_novo, "ja", n_ja, "->", DEST)
