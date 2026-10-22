# -*- coding: utf-8 -*-
"""Apaga SO' C:/t/p12 (criado por este agente). Lista antes, recusa qualquer caminho fora, grava LIMPEZA_p12.json."""
import json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.normcase(os.path.normpath(os.path.join("C:" + os.sep, "t", "p12")))
assert os.path.normcase(os.path.realpath(ALVO)) == ALVO, "juncao/link no alvo"
lst = []; tot = 0
for r, ds, fs in os.walk(ALVO, followlinks=False):
    for n in ds + fs:
        p = os.path.normcase(os.path.normpath(os.path.join(r, n)))
        if not p.startswith(ALVO + os.sep):
            raise SystemExit("RECUSA: fora do alvo " + p)
        if os.path.islink(p):
            raise SystemExit("RECUSA: link " + p)
    for n in fs:
        p = os.path.join(r, n); sz = os.path.getsize(p); tot += sz; lst.append([os.path.relpath(p, ALVO), sz])
shutil.rmtree(ALVO)
res = {"apagado": ALVO, "n_arquivos": len(lst), "bytes": tot, "existe_depois": os.path.exists(ALVO), "arquivos": lst}
with open(os.path.join(HERE, "LIMPEZA_p12.json"), "xb") as fh:
    fh.write(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8"))
print(json.dumps({k: res[k] for k in ("apagado", "n_arquivos", "bytes", "existe_depois")}))
