import os, re
A = ("entuasi" + "asmos").encode(); B = ("484ad9" + "82").encode(); C = ("filho Be" + "nto").encode(); D = ("ratificada_be" + "nto").encode()
rx = re.compile(re.escape(A) + b"|" + re.escape(B), re.I); rx2 = re.compile(re.escape(C) + b"|" + re.escape(D), re.I)
tot = 0
for raiz in (r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\revisao_terceiro", r"C:\t\k411c\revisao_C"):
    n = 0; h1 = []; h2 = []
    for d, ds, fs in os.walk(raiz):
        for f in fs:
            p = os.path.join(d, f); n += 1
            try:
                b = open(p, "rb").read()
            except OSError:
                continue
            if rx.search(b): h1.append(p)
            if rx2.search(b): h2.append(p)
    print(raiz, "arquivos:", n, "| padrao A/B:", len(h1), h1[:3], "| padrao C/D:", len(h2), h2[:3])
