import os, re, glob
import a_lib
diff = open(os.path.join(a_lib.OUT, "mydiff.diff"), "rb").read().decode("utf-8", "surrogateescape").split(chr(10))
novas = []; atual = 0
for ln in diff:
    if ln.startswith("@@"):
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", ln); atual = int(m.group(1)) - 1; continue
    if ln.startswith("+") and not ln.startswith("+++"):
        atual += 1; novas.append((atual, ln[1:].replace("\r", "")))
    elif ln.startswith(" "): atual += 1
CG = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
falas = {os.path.basename(p): open(p, "rb").read().decode("utf-8") for p in glob.glob(os.path.join(CG, "OPERADOR_*.txt"))}
tot = 0; ruins = []
for i, x in novas:
    for m in re.finditer(r"«([^»]*)»", x):
        tot += 1
        q = m.group(1)
        ok = [n for n, t in falas.items() if q in t]
        if not ok:
            ruins.append((i, q[:100], x[max(0, m.start() - 60):m.start()]))
print("aspas angulares nas linhas novas:", tot, "| sem fala correspondente (substring de OPERADOR_*.txt):", len(ruins))
for r in ruins[:25]: print("  ", r)
