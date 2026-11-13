"""CU-C5: formato do numero das Cefeidas livres no topo e nos fechos (PT e EN, txt e tex); o fecho no fim dos dois blocos; o baseline de R1 para 'O que o teste nao decide'."""
import json, os, re
D = r"C:\t\k411c\dry_v411"
rd = lambda p: open(p, "rb").read().decode("utf-8").replace("\r\n", "\n")
for nm in ("dry_v411_pt.txt", "dry_v411_en.txt", "dry_v411_pt.tex", "dry_v411_en.tex"):
    t = rd(os.path.join(D, nm))
    fm = re.findall(r"[^\w]4(?:\{,\}|[,.])38[^\d]", t)
    print(nm, "formatos de 4,38 e contagens:", {x: fm.count(x) for x in set(fm)})
    # contexto: onde as Cefeidas livres aparecem com 4,38
    for m in list(re.finditer(r"(?:Cefeidas livres|free Cepheids)[^\n]{0,200}?4(?:\{,\}|[,.])38", t))[:12]:
        s = t[max(0, m.start() - 60):m.start()].replace("\n", " ")
        print("    @%d ...%s | %s" % (m.start(), s[-40:], m.group(0)[:20] + "..." + m.group(0)[-34:]))
# baseline de R1
try:
    b = json.load(open(r"C:\t\k411c\revisao_B\b02_resultado.json", encoding="utf-8"))
    for k, v in b.items():
        print("R1", k, [(o["ini"], o["faltam"], o["abre"][:50]) for o in v if o["faltam"]][:6])
except Exception as e:
    print("sem baseline R1:", e)
