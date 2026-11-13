import re, os, hashlib
D = r"C:\t\k411c\falso_nos_v411"
cand = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\um_v411_candidato.py"
print("um.py do ensaio == candidato:", hashlib.sha256(open(os.path.join(D, "um.py"), "rb").read()).hexdigest()[:16], hashlib.sha256(open(cand, "rb").read()).hexdigest()[:16])
for f in ("um_absoluto_pt.txt", "um_absoluto_en.txt", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "rodada_v411_stdout.txt"):
    t = open(os.path.join(D, f), encoding="utf-8", errors="replace").read()
    ms = list(re.finditer(r"\bconfirm\w*|\bconfirmad[oa]s?\b|\bconfirma(?:ção|cao|ções|coes)\b", t, re.I))
    rel = []
    for m in ms:
        ctx = t[max(0, m.start() - 90):m.end() + 60].replace("\n", " ")
        if re.search(r"h0dn|hubble|raz[ãa]o|β|beta|natureza|nature|6\s*σ|5\s*σ|sigma|retrodi|provad|proved", ctx, re.I):
            rel.append(ctx)
    print("==", f, "| n confirm*:", len(ms), "| perto de H0DN/beta/natureza/sigma:", len(rel))
    for c in rel[:12]:
        print("    ", c[:230])
