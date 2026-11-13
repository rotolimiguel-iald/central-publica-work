import a_lib, hashlib, os, json, time
t0 = time.time()
f = a_lib.Fonte(a_lib.CAND, "cand")
print("idx _EMBEDDED_KERNEL_FILES:", f.idx.get("_EMBEDDED_KERNEL_FILES"))
ns = f.carregar(["_EMBEDDED_KERNEL_FILES"])
E = ns["_EMBEDDED_KERNEL_FILES"]
print(type(E).__name__, len(E), "| %.1fs" % (time.time() - t0))
k = next(iter(E)); v = E[k]
print("amostra chave:", k, "| tipo valor:", type(v).__name__, (list(v.keys()) if isinstance(v, dict) else len(v)))
SB = r"C:\t\k411c\final"; NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
sha = lambda b: hashlib.sha256(b).hexdigest()
def lerarq(root, rel):
    p = os.path.join(root, rel.replace("/", os.sep))
    return open(p, "rb").read() if os.path.exists(p) else None
eq_sb = eq_nos = ausente_sb = ausente_nos = 0; dif = []
for rel, txt in E.items():
    b = txt.encode("utf-8")
    s = lerarq(SB, rel); n = lerarq(NOS, rel)
    if s is None: ausente_sb += 1
    elif s == b: eq_sb += 1
    else: dif.append(("sandbox", rel))
    if n is None: ausente_nos += 1
    elif n == b: eq_nos += 1
    else: dif.append(("nos", rel))
print("embutido vs sandbox C:\t\k411c\final: iguais", eq_sb, "ausentes", ausente_sb, "| vs Nos(v410): iguais", eq_nos, "ausentes", ausente_nos, "| diferentes:", dif[:5], len(dif))
# o dict base == o dict candidato (por sha do dumps), a partir do base
fb = a_lib.Fonte(a_lib.BASE, "base")
nb = fb.carregar(["_EMBEDDED_KERNEL_FILES"]); Eb = nb["_EMBEDDED_KERNEL_FILES"]
print("dict embutido do candidato == o da base v410:", E == Eb, len(Eb))
ns2 = f.carregar(["_LEAN_THEOREM_FLAGS"]); nb2 = fb.carregar(["_LEAN_THEOREM_FLAGS"])
print("_LEAN_THEOREM_FLAGS igual:", ns2["_LEAN_THEOREM_FLAGS"] == nb2["_LEAN_THEOREM_FLAGS"], len(ns2["_LEAN_THEOREM_FLAGS"]))
# o sha do audit.log da v410 e da v411
for p in (r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\kernel\audit.log", r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\kernel\audit.log"):
    print(p[-45:], os.path.exists(p) and sha(open(p, "rb").read())[:16])
