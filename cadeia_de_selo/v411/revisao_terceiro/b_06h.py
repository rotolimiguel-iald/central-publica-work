from b_lib import *
import re
texts = {"pt": pt(), "en": en(), "md": md(), "man": man(), "out": out()}
old = {"pt": rd(NOS + r"\um_absoluto_pt.txt"), "en": rd(NOS + r"\um_absoluto_en.txt"), "md": rd(NOS + r"\um_absoluto_forma_canonica.md")}
RXC = {"calibrado": r"calibrad|calibrated", "abaixo": r"abaixo\s+do\s+degrau|abaixo\s+de\s+\$?5|below\s+(?:the\s+)?(?:5\$?\s*\?σ|5\s*σ|step|5σ)|< ?5|<5|abaixo|below", "nao_sigma": r"n[ãa]o\s+é\s+\$?σ|not\s+a\s+\$?σ|Bayes|n[ãa]o\s+é\s+σ", "nao_indep": r"n[ãa]o\s+é\s+evid[êe]ncia\s+independente|not\s+independent"}
for nm, tx in texts.items():
    paras = [m for m in re.finditer(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", tx.replace("\r\n", "\n"))]
    n = 0
    for m in paras:
        p = m.group(0)
        if not re.search(r"4[,.]44", p): continue
        n += 1
        flags = {k: bool(re.search(rx, p, re.I)) for k, rx in RXC.items()}
        was_old = (nm in old) and (re.sub(r"\s+", " ", p)[:200] in re.sub(r"\s+", " ", old[nm].replace("\r\n", "\n")))
        print("%-3s @%-7d len=%6d old_text=%s flags=%s | %s" % (nm, m.start(), len(p), was_old, flags, p[:70].replace("\n", " ")))
    print(nm, "paragrafos com 4,44:", n)
