# -*- coding: utf-8 -*-
"""Impressao digital do tgl_kernel do Nos (so leitura): caminho relativo, tamanho e mtime_ns de cada arquivo,
sem seguir junções nem links simbolicos. Uso: impressao_digital.py <saida.json>"""
import os, sys, json, hashlib, datetime
K = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/tgl_kernel"
h = hashlib.sha256()
n = 0
pulados = []
for raiz, dirs, files in os.walk(K, followlinks=False):
    keep = []
    for d in sorted(dirs):
        p = os.path.join(raiz, d)
        if os.path.islink(p) or (hasattr(os.path, "isjunction") and os.path.isjunction(p)):
            pulados.append(os.path.relpath(p, K).replace("\\", "/"))
        else:
            keep.append(d)
    dirs[:] = keep
    for f in sorted(files):
        p = os.path.join(raiz, f)
        if os.path.islink(p):
            pulados.append(os.path.relpath(p, K).replace("\\", "/"))
            continue
        st = os.lstat(p)
        rel = os.path.relpath(p, K).replace("\\", "/")
        h.update(("%s|%d|%d\n" % (rel, st.st_size, st.st_mtime_ns)).encode("utf-8"))
        n += 1
out = {"kernel": K, "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "n_arquivos": n, "impressao_sha256": h.hexdigest(), "pulados_juncao_ou_link": pulados}
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: out[k] for k in ("n_arquivos", "impressao_sha256")}), len(pulados))
