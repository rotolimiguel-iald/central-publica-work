from b_lib import *
import re
exec(open("b_01_topo.py", encoding="utf-8").read().split("def norm(s):")[0])
H = rd(V + r"\pos_rito\HARNESS_TEXTOS_ENSAIO_v411.json")
print(len(H))
exp = {}
for k in ("painel_readme_pt", "painel_readme_en", "estado_pt", "estado_en"):
    s = T[k]
    for a, b in vpt.items(): s = s.replace(a, b)
    for a, b in ven.items(): s = s.replace(a, b)
    assert "⟨" not in s, k
    exp[k] = s
    # JSON-escaped form too
    esc = json.dumps(s, ensure_ascii=False)[1:-1]
    print(k, "literal:", s in H, "| escapado:", esc in H, "| len", len(s))
    # fuzzy: normalized compare
    def n(x): return re.sub(r"[^\w]", "", x.replace("\n", ""))
    print("    normalizado presente:", n(s) in n(H))
