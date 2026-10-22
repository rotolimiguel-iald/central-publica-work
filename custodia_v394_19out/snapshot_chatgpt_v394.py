# -*- coding: utf-8 -*-
"""Snapshot INCREMENTAL da pasta Chatgpt/ (custódia do Claude; a origem é só LIDA), FORA do repositório — custódia v394 (19/10/2026, sessão a7).
Molde: snapshot_chatgpt_delta_v2.py (15/09) e a rodada de 07/10 (custódia v390/v391). As mesmas exclusões ditas no manifesto: nada dentro de
.lake/ (build Lean derivável), nada dentro de tex_environment/ (distribuição TeX), arquivo > 25 MB (catálogos públicos; listados com caminho
e bytes). Arquivo idêntico à base (o último snapshot, cujo manifesto lista TODOS os arquivos com sha256) não se copia; novo ou mudado se copia
e se confere por sha256 contra a origem. Destino novo: nada se sobrescreve."""
import hashlib
import json
import os
import time
from datetime import datetime
from pathlib import Path

SRC = Path(r"C:/IALD/Central de Patentes/Chatgpt")
ROOT = Path(r"C:/IALD/Central de Patentes_BACKUPS")
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
LIM = 25 * 1024 * 1024
EXCL_DIRS = {".lake", "tex_environment"}
t0 = time.time()


def lp(p):
    return Path("\\\\?\\" + str(p))


def sha(p):
    h = hashlib.sha256()
    with open(lp(p), "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


bases = sorted(d for d in ROOT.iterdir() if d.is_dir() and d.name.startswith("Chatgpt_") and (d / "MANIFEST.json").is_file())
base = bases[-1]
assert base.name == "Chatgpt_20261007_195426_delta_de_20261007_114440", base.name
DST = ROOT / ("Chatgpt_%s_delta_de_%s" % (TS, base.name.split("_")[1] + "_" + base.name.split("_")[2]))
assert not DST.exists(), DST
bman = json.loads((base / "MANIFEST.json").read_text(encoding="utf-8"))["arquivos"]
man = {"origem": str(SRC), "snapshot": TS, "tipo": "INCREMENTAL", "base": str(base), "versao_do_script": "v2 (custodia v394, 19/10; exclusoes iguais as de 15/09)",
       "regra": "custodia do Claude; a origem e EDITADA so pelo ChatGPT — aqui so se LE; arquivo identico a base NAO e copiado de novo",
       "regra_v2_exclusoes": ["dentro de .lake/ (build Lean derivavel)", "dentro de tex_environment/ (distribuicao TeX copiada)",
                              "arquivo > 25 MB (catalogos publicos copiados; listados abaixo com caminho e bytes)"],
       "arquivos": {}, "n_total": 0, "n_copiados": 0, "bytes_copiados": 0, "n_identicos_a_base": 0,
       "excluidos": {"lake": {"n": 0, "bytes": 0}, "tex_environment": {"n": 0, "bytes": 0}, "maiores_que_25MB": {"n": 0, "bytes": 0, "lista": []}}}

inc = []
for dp, dns, fns in os.walk(lp(SRC)):
    rel_dir = os.path.relpath(dp, str(lp(SRC)))
    keep = []
    for d in dns:
        if d in EXCL_DIRS:
            n = b = 0
            for dp2, _, fns2 in os.walk(os.path.join(dp, d)):
                for f2 in fns2:
                    try:
                        b += os.path.getsize(os.path.join(dp2, f2)); n += 1
                    except OSError:
                        pass
            k = "lake" if d == ".lake" else "tex_environment"
            man["excluidos"][k]["n"] += n; man["excluidos"][k]["bytes"] += b
        else:
            keep.append(d)
    dns[:] = keep
    for f in fns:
        full = os.path.join(dp, f)
        try:
            sz = os.path.getsize(full)
        except OSError:
            continue
        rel = (f if rel_dir == "." else rel_dir.replace("\\", "/") + "/" + f)
        if sz > LIM:
            man["excluidos"]["maiores_que_25MB"]["n"] += 1
            man["excluidos"]["maiores_que_25MB"]["bytes"] += sz
            man["excluidos"]["maiores_que_25MB"]["lista"].append({"caminho": rel, "bytes": sz})
            continue
        inc.append((rel, sz))
inc.sort()
print("varredura: %d a considerar | excluidos: lake %d, tex %d, >25MB %d | %.0f s" % (
    len(inc), man["excluidos"]["lake"]["n"], man["excluidos"]["tex_environment"]["n"], man["excluidos"]["maiores_que_25MB"]["n"], time.time() - t0), flush=True)

for i, (rel, sz) in enumerate(inc):
    src = SRC / rel
    try:
        h = sha(src)
    except OSError as e:
        man["arquivos"][rel] = {"bytes": sz, "erro_de_leitura": repr(e)[:120]}
        continue
    b = bman.get(rel)
    man["n_total"] += 1
    if b and b.get("sha256") == h:
        man["arquivos"][rel] = {"bytes": sz, "sha256": h, "em": "base"}
        man["n_identicos_a_base"] += 1
        continue
    dst = lp(DST / rel)
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(lp(src), "rb") as f:
        data = f.read()
    h2 = hashlib.sha256(data).hexdigest()
    with open(dst, "wb") as g:
        g.write(data)
    man["arquivos"][rel] = {"bytes": len(data), "sha256": h2, "em": "delta", "novo": b is None}
    man["n_copiados"] += 1
    man["bytes_copiados"] += len(data)
    if i % 50000 == 0:
        print("  ... %d/%d %.0f s" % (i, len(inc), time.time() - t0), flush=True)

div = [r for r, m in man["arquivos"].items() if m.get("em") == "delta" and sha(DST / r) != m["sha256"]]
sumidos = sorted(set(bman) - set(man["arquivos"]))
man["conferido_contra_origem"] = (len(div) == 0)
man["ausentes_na_origem_vs_base"] = sumidos
man["segundos"] = round(time.time() - t0)
DST.mkdir(parents=True, exist_ok=True)
tmp = DST / "MANIFEST.json.tmp"
tmp.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
tmp.replace(DST / "MANIFEST.json")
print("snapshot %s: total %d | copiados %d (%.3f GB) | identicos a base %d | sumidos vs base %d | divergentes %d | %d s"
      % (DST.name, man["n_total"], man["n_copiados"], man["bytes_copiados"] / 2**30, man["n_identicos_a_base"], len(sumidos), len(div), man["segundos"]),
      flush=True)
assert not div
