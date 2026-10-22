# -*- coding: utf-8 -*-
"""Manifesto da rodada 2 do construtor do kernel F1.TEMPO: sha256 e tamanho de todo arquivo de 3_KERNEL\rodada_2
(exceto o próprio manifesto). Uso: python -I manifesto.py"""
import datetime, hashlib, json, os
R2 = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\3_KERNEL\rodada_2"
OUT = os.path.join(R2, "MANIFESTO_RODADA_2.json")
arqs = []
for dp, dn, fn in os.walk(R2):
    dn.sort()
    for f in sorted(fn):
        p = os.path.join(dp, f)
        if os.path.abspath(p) == os.path.abspath(OUT):
            continue
        b = open(p, "rb").read()
        arqs.append({"arquivo": os.path.relpath(p, R2).replace("\\", "/"), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
m = {"pasta": R2, "gerado_em_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "n_arquivos": len(arqs),
     "bytes_total": sum(a["bytes"] for a in arqs), "arquivos": arqs}
open(OUT + ".tmp", "w", encoding="utf-8").write(json.dumps(m, ensure_ascii=False, indent=1))
os.replace(OUT + ".tmp", OUT)
print(m["n_arquivos"], m["bytes_total"], hashlib.sha256(open(OUT, "rb").read()).hexdigest())
