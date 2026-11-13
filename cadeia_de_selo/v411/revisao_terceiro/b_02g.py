from b_lib import *
import re
exec(open("b_02_obrigatorios.py", encoding="utf-8").read().split("res = {}")[0].split("texts = {")[0])
texts = {"pt": pt(), "en": en(), "md": md()}
exec(open("b_02_obrigatorios.py", encoding="utf-8").read().split("RQ = {")[1].join(["RQ = {",""]).split("res = {}")[0]) if False else None
src = open("b_02_obrigatorios.py", encoding="utf-8").read()
RQsrc = src[src.index("RQ = {"):src.index("res = {}")]
exec(RQsrc)
OCC2 = re.compile(r"num\s+canal|in\s+one\s+channel|12/11/2026|12\s+Nov\s+2026|2026-11-12|H0DN|razão\s+de\s+Hubble|Hubble\s+ratio|natureza\s+a\s+5|nature\s+at\s+5|acima\s+de\s+\$?5|above\s+\$?5", re.I)
for n, tx in texts.items():
    print("==", n)
    for m in re.finditer(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", tx):
        p = m.group(0)
        if not OCC2.search(p): continue
        if len(p) > 20000: 
            print("  @%d LONG len=%d %s" % (m.start(), len(p), p[:80].replace("\n"," "))); continue
        falta = [k for k, rx in RQ.items() if not rx.search(p)]
        print("  @%d len=%d faltam=%s | %s" % (m.start(), len(p), falta, p[:110].replace("\r"," ").replace("\n"," ")))
