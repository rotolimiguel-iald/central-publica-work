# -*- coding: utf-8 -*-
"""foto_memoria_real.py -- SO LEITURA: sha256/tamanho/mtime de todo arquivo do diretorio REAL da memoria (para provar que o exame nao o tocou). uso: python foto_memoria_real.py <tag>"""
import hashlib, json, os, sys
M = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
out = {}
for d, ds, fs in os.walk(M):
    for f in fs:
        p = os.path.join(d, f)
        try:
            st = os.stat(p); out[os.path.relpath(p, M)] = [st.st_size, st.st_mtime_ns, hashlib.sha256(open(p, "rb").read()).hexdigest()]
        except OSError as e:
            out[os.path.relpath(p, M)] = ["erro", str(e)]
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "MEMORIA_REAL_%s.json" % sys.argv[1]), "w", encoding="utf-8"), indent=0)
mm = os.path.join(M, "MEMORY.md"); t = open(mm, "rb").read()
print(len(out), "arquivos; MEMORY.md", len(t), "B", t.count(b"\n"), "linhas; PAUSA_VIGIA existe:", os.path.exists(os.path.join(M, "fila", "PAUSA_VIGIA.json")))
