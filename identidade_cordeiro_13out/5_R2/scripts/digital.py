# -*- coding: utf-8 -*-
"""Impressao digital do auditor (independente): rel|size|mtime_ns de todo arquivo do tgl_kernel, sem seguir
juncoes/links; e sha256 de conteudo dos arquivos fora de .lake. Uso: digital.py <saida.json>"""
import os, sys, json, hashlib, datetime
K = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/tgl_kernel"
hm = hashlib.sha256(); hc = hashlib.sha256(); n = 0; nc = 0; pul = []
for raiz, dirs, files in os.walk(K, followlinks=False):
    keep = []
    for d in sorted(dirs):
        p = os.path.join(raiz, d)
        if os.path.islink(p) or os.path.isjunction(p):
            pul.append(os.path.relpath(p, K).replace(os.sep, "/"))
        else:
            keep.append(d)
    dirs[:] = keep
    for f in sorted(files):
        p = os.path.join(raiz, f)
        rel = os.path.relpath(p, K).replace(os.sep, "/")
        if os.path.islink(p):
            pul.append(rel); continue
        st = os.lstat(p)
        hm.update(("%s|%d|%d\n" % (rel, st.st_size, st.st_mtime_ns)).encode("utf-8")); n += 1
        if not rel.startswith(".lake/"):
            h = hashlib.sha256(open(p, "rb").read()).hexdigest()
            hc.update((rel + "|" + h + "\n").encode("utf-8")); nc += 1
out = {"kernel": K, "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "n_arquivos": n,
       "impressao_meta_sha256": hm.hexdigest(), "n_conteudo_fora_lake": nc, "impressao_conteudo_sha256": hc.hexdigest(),
       "pulados": pul}
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: out[k] for k in ("n_arquivos", "impressao_meta_sha256", "n_conteudo_fora_lake", "impressao_conteudo_sha256", "pulados")}))
