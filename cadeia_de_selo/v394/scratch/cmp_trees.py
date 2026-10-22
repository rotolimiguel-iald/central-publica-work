import os, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "tgl_kernel")
CX = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "F1.FECHO_20261015", "candidate_r8", "tgl_kernel")


def walk(root):
    d = {}
    for dp, dn, fn in os.walk(root):
        dn[:] = [x for x in dn if x != ".lake"]
        for f in fn:
            if ".bak_" in f:
                continue
            p = os.path.join(dp, f)
            r = os.path.relpath(p, root).replace(os.sep, "/")
            d[r] = p
    return d


a = walk(NOS); b = walk(CX)
print(len(a), len(b))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
onlyb = [k for k in b if k not in a]; onlya = [k for k in a if k not in b]
print("onlyA", len(onlya), onlya[:10]); print("onlyB", len(onlyb))
chg = [k for k in a if k in b and h(a[k]) != h(b[k])]
print("changed", chg)
print([k for k in onlyb if not k.endswith(".lean")])
print("CX has .lake:", os.path.exists(os.path.join(CX, ".lake")))
