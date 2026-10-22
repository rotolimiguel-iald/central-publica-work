# -*- coding: utf-8 -*-
"""Varre o um.py por tokenize (sem executar) e lista toda STRING curta que contem 'sorry'
(literais de deteccao), com a linha de codigo. So leitura."""
import io, json, tokenize, hashlib
from pathlib import Path

UM = Path(r"C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py")
OUT = Path(r"C:/IALD/Central de Patentes/work/umpy_sorry_check_13out")
raw = UM.read_bytes()
lines = raw.decode("utf-8").splitlines()
hits = []
for tok in tokenize.tokenize(io.BytesIO(raw).readline):
    if tok.type == tokenize.STRING and "sorry" in tok.string.lower() and len(tok.string) < 400:
        ln = tok.start[0]
        hits.append({"line": ln, "string": tok.string, "code": lines[ln - 1].strip()[:300]})
(OUT / "deteccoes_tokenize.json").write_text(json.dumps({"um_py_sha16": hashlib.sha256(raw).hexdigest()[:16], "n": len(hits), "hits": hits}, ensure_ascii=False, indent=1), encoding="utf-8")
seen = set()
for h in hits:
    key = h["string"]
    print(h["line"], h["string"][:160])
