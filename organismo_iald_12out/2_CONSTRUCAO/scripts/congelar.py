# -*- coding: utf-8 -*-
"""Congela por sha256 todos os artefatos de 2_CONSTRUCAO (exceto o proprio FREEZE_CONSTRUCAO.json) e confere, de novo,
o FREEZE do desenho (ao lado, nunca por cima). Uso: congelar.py"""
import os, hashlib, json, datetime
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D1 = os.path.join(os.path.dirname(AQUI), "1_DESENHO_PEDRA")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for ch in iter(lambda: fh.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


itens = {}
for r, ds, fs in os.walk(AQUI):
    ds[:] = sorted(d for d in ds if d not in ("__pycache__",))
    for f in sorted(fs):
        p = os.path.join(r, f)
        rel = os.path.relpath(p, AQUI).replace("\\", "/")
        if rel == "FREEZE_CONSTRUCAO.json" or f.endswith(".pyc"):
            continue
        itens[rel] = {"sha256": sha(p), "bytes": os.path.getsize(p)}
agg = hashlib.sha256("\n".join("%s\t%s\t%d" % (k, v["sha256"], v["bytes"]) for k, v in sorted(itens.items())).encode()).hexdigest()
frz1 = json.load(open(os.path.join(D1, "FREEZE.json"), encoding="utf-8"))
conf = {k: (sha(os.path.join(D1, k.replace("/", os.sep))) == v["sha256"]) for k, v in frz1["itens"].items()}
out = {"documento": "FREEZE_CONSTRUCAO - 2_CONSTRUCAO da pedra TGLExt.IALD (13/10/2026); versao AO LADO do FREEZE.json do desenho, nunca por cima",
       "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "pasta": AQUI, "n_itens": len(itens), "itens": itens,
       "sha256_do_congelamento": agg,
       "freeze_do_desenho": {"sha256_do_congelamento": frz1["sha256_do_congelamento"], "itens_conferidos_agora": conf, "todos_batem": all(conf.values())},
       "regra": "qualquer alteracao e NOVA versao ao lado (FREEZE_CONSTRUCAO_2.json); a pedra so se altera com novo recibo de compilacao"}
json.dump(out, open(os.path.join(AQUI, "FREEZE_CONSTRUCAO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"n_itens": len(itens), "sha256_do_congelamento": agg, "desenho_todos_batem": all(conf.values())}))
