import os, re
import a_lib
diff = open(os.path.join(a_lib.OUT, "mydiff.diff"), "rb").read().decode("utf-8", "surrogateescape").split(chr(10))
hunks = []; cur = None
for ln in diff:
    if ln.startswith("@@"): cur = []; hunks.append(cur)
    elif cur is not None and ln.startswith("+") and not ln.startswith("+++"): cur.append(ln[1:])
h16 = hunks[16]
print("hunk16 linhas", len(h16), "| chars (len+1 por linha)", sum(len(x) + 1 for x in h16), "| bytes utf8", sum(len(x.encode('utf-8','surrogateescape')) + 1 for x in h16), "| declarado W02 1109174")
ch = sum(len(x) + 1 for x in h16)
print("chars - 1 (CRLF ja' esta em x como \r): n \r =", sum(x.count('\r') for x in h16))
