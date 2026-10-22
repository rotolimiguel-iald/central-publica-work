import re, sys
sys.stdout.reconfigure(encoding="utf-8")
PAT = re.compile(r'(?i)((api[-_ ]?key|token|senha|password|secret|bearer|authorization)\S*\s*[=:]?\s*)(["\']?)[^\s"\'\)]+')
for p in sys.argv[1:]:
    print("=" * 20, p)
    try:
        t = open(p, encoding="utf-8-sig", errors="replace").read()
    except Exception as e:
        print("FALHA DE LEITURA:", e); continue
    for i, l in enumerate(t.splitlines(), 1):
        print("%4d  %s" % (i, PAT.sub(lambda m: m.group(1) + m.group(3) + "<REDIGIDO>", l)))
