import os, re, sys
import a_lib
diff = open(os.path.join(a_lib.OUT, "mydiff.diff"), "rb").read().decode("utf-8", "surrogateescape").split(chr(10))
novas = []; atual = 0
for ln in diff:
    if ln.startswith("@@"):
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", ln); atual = int(m.group(1)) - 1; continue
    if ln.startswith("+") and not ln.startswith("+++"):
        atual += 1; novas.append((atual, ln[1:].replace("\r", "")))
    elif ln.startswith(" "): atual += 1
pat = re.compile(sys.argv[1], re.I)
n = 0
for i, x in novas:
    for m in pat.finditer(x):
        n += 1
        if n <= int(sys.argv[2]):
            print(i, "|", x[max(0, m.start() - 70):m.end() + 70])
print("total", n)
