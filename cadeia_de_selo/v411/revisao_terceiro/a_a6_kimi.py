import os, re, json
import a_lib
diff = open(os.path.join(a_lib.OUT, "mydiff.diff"), "rb").read().decode("utf-8", "surrogateescape").split(chr(10))
novas = []; atual = 0
for ln in diff:
    if ln.startswith("@@"):
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", ln); atual = int(m.group(1)) - 1; continue
    if ln.startswith("+") and not ln.startswith("+++"):
        atual += 1; novas.append((atual, ln[1:]))
    elif ln.startswith(" "): atual += 1
for i, x in novas:
    for m in re.finditer(r"kimi", x, re.I):
        ctx = x[max(0, m.start() - 70):m.end() + 50].replace("\r", "")
        sob = bool(re.search(r"kimi[\/]{1,4}[A-Za-z0-9_.]", x[m.start():m.start() + 40], re.I))
        print(i, "SOB_KIMI" if sob else "-", "|", ctx)
