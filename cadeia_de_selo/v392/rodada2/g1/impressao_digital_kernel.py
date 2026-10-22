# -*- coding: utf-8 -*-
"""impressao_digital_kernel.py -- impressao digital SO-LEITURA do tgl_kernel do Nos, sem seguir juncoes/links (.lake/packages e' juncao e e' pulada).
Uso: python -I -B -X utf8 impressao_digital_kernel.py <rotulo> [pasta]   -> grava fp_<rotulo>.json ao lado e imprime o resumo."""
import hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
K = sys.argv[2] if len(sys.argv) > 2 else os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "tgl_kernel")
rot = sys.argv[1]
REPARSE = 0x400
h = hashlib.sha256(); hs = hashlib.sha256(); ho = hashlib.sha256(); n = 0; tot = 0; nsrc = 0; nol = 0; puladas = []
for r, ds, fs in os.walk(K, followlinks=False):
    keep = []
    for d in sorted(ds):
        p = os.path.join(r, d)
        if getattr(os.lstat(p), "st_file_attributes", 0) & REPARSE or os.path.islink(p):
            puladas.append(p)
        else:
            keep.append(d)
    ds[:] = keep
    for f in sorted(fs):
        p = os.path.join(r, f); st = os.lstat(p); rel = os.path.relpath(p, K)
        h.update(("%s|%d|%d\n" % (rel, st.st_size, st.st_mtime_ns)).encode("utf-8")); n += 1; tot += st.st_size
        if f.endswith(".lean") and ".lake" not in rel.split(os.sep):
            hs.update((rel + "|").encode("utf-8") + hashlib.sha256(open(p, "rb").read()).digest()); nsrc += 1
        if f.endswith(".olean") and rel.startswith(os.path.join(".lake", "build", "lib", "lean", "TGLExt")):
            ho.update((rel + "|").encode("utf-8") + hashlib.sha256(open(p, "rb").read()).digest()); nol += 1
res = {"rotulo": rot, "pasta": K, "arquivos": n, "bytes": tot, "metadados_sha16": h.hexdigest()[:16], "fontes_lean_fora_de_lake": nsrc, "fontes_sha16": hs.hexdigest()[:16],
       "oleans_TGLExt": nol, "oleans_sha16": ho.hexdigest()[:16], "juncoes_puladas": puladas}
open(os.path.join(HERE, "fp_%s.json" % rot), "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
print(json.dumps(res, ensure_ascii=False))
