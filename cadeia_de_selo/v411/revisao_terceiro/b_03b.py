from b_lib import *
d = json.load(open(SC + r"\b03_novos.json", encoding="utf-8"))
for k, (no, nn, novos) in d.items():
    nm, pk = k.split("|")
    if nm not in ("pt",): continue
    if not novos: continue
    print("=====", k, len(novos))
    seen = set()
    for c in novos:
        c2 = c[:260]
        if c2 in seen: continue
        seen.add(c2); print("  -", c.replace("\n", " ")[:260])
