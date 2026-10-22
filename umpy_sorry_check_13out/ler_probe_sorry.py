# -*- coding: utf-8 -*-
"""Le (sem executar o um.py) o probe SorryTerm do arquivo v361 embutido: fonte e stdout gravados pela bancada."""
import ast, base64, hashlib, lzma, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
lines = Path(r"C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um.py").read_text(encoding="utf-8").splitlines()
def block(name, closer):
    s = next(i for i, l in enumerate(lines) if l.startswith(name + " = "))
    if not lines[s].rstrip().endswith(("[", "{")):
        return ast.literal_eval(lines[s].split(" = ", 1)[1])
    j = s + 1
    while not lines[j].startswith(closer):
        j += 1
    return ast.literal_eval("\n".join(lines[s:j + 1]).split(" = ", 1)[1])
meta = block("_BENCH_ARCHIVE_V361_META", "}"); index = block("_BENCH_ARCHIVE_V361_INDEX", "]"); arch = block("_EMBEDDED_BENCH_ARCHIVE_V361", "]")
comp = base64.b64decode("".join(arch)); assert hashlib.sha256(comp).hexdigest() == meta["xz_sha256"]
blob = lzma.decompress(comp)
for r in index:
    if "SorryTerm" in r[0]:
        d = blob[r[1]:r[1] + r[2]]
        print("==", r[0], "sha_ok=", hashlib.sha256(d).hexdigest() == r[3])
        print(d.decode("utf-8", "replace")[:1500])
