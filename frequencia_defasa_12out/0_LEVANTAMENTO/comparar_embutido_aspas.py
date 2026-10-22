# -*- coding: utf-8 -*-
# Variante para modulos embutidos no estilo 'TGLExt/X.lean': '...' ou 'TGLExt/X.lean': "..." (literal escapado; somente leitura).
import re, ast, hashlib, sys, json
NOS = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/"
with open(NOS + "um.py", "rb") as fh:
    U = fh.read()
PAT = {b"'": re.compile(rb"'((?:[^'\\\n]|\\.)*)'", re.S), b'"': re.compile(rb'"((?:[^"\\\n]|\\.)*)"', re.S)}
out = {}
for m in sys.argv[1:]:
    key = ("'TGLExt/%s.lean': " % m).encode()
    i = U.find(key)
    if i < 0:
        out[m] = {"no_um_py": False}
        continue
    j = i + len(key)
    q = U[j:j + 1]
    if q not in PAT:
        out[m] = {"no_um_py": True, "erro": "aspas nao reconhecidas"}
        continue
    mm = PAT[q].match(U, j)
    if mm is None:
        out[m] = {"no_um_py": True, "erro": "literal nao reconhecido"}
        continue
    s = ast.literal_eval(mm.group(0).decode("utf-8"))
    emb = s.encode("utf-8").replace(b"\r\n", b"\n")
    with open(NOS + "tgl_kernel/TGLExt/" + m + ".lean", "rb") as fh:
        kb = fh.read()
    out[m] = {"linha_chave_um_py": U.count(b"\n", 0, i) + 1, "aspas_do_valor": q.decode(),
              "sha16_arquivo_kernel": hashlib.sha256(kb).hexdigest()[:16],
              "identicos_apos_LF": emb == kb.replace(b"\r\n", b"\n"),
              "bytes_embutido": len(emb), "bytes_kernel": len(kb)}
print(json.dumps(out, ensure_ascii=False, indent=1))
