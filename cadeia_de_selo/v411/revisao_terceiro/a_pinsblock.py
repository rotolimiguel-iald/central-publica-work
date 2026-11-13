import os, re
import a_lib
V = a_lib.V
diff = open(os.path.join(a_lib.OUT, "mydiff.diff"), "rb").read().decode("utf-8", "surrogateescape").split(chr(10))
hunks = []; cur = None
for ln in diff:
    if ln.startswith("@@"): cur = []; hunks.append(cur)
    elif cur is not None and ln.startswith("+") and not ln.startswith("+++"): cur.append(ln[1:])
blk = chr(10).join(x.replace("\r", "") for x in hunks[16]) + chr(10)
pins = open(os.path.join(V, "v411_pins.py"), "rb").read().decode("utf-8").replace("\r\n", chr(10))
print("tamanhos: bloco do candidato", len(blk), "| v411_pins.py", len(pins))
print("v411_pins.py == bloco do candidato:", pins.strip() == blk.strip())
if pins.strip() != blk.strip():
    a, b = pins.strip(), blk.strip()
    i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), None)
    print("primeira divergencia em", i, repr(a[i-60:i+60]) if i is not None else None, "||", repr(b[i-60:i+60]) if i is not None else None)
