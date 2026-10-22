import os
T = os.path.expanduser("~") + r"\.elan\toolchains\leanprover--lean4---v4.31.0"
m, mp = 0, ""
for dp, dn, fn in os.walk(T):
    for f in fn:
        r = os.path.relpath(os.path.join(dp, f), T)
        if len(r) > m:
            m, mp = len(r), r
print("toolchain rel max:", m, mp)
L = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\.lake\build\lib\lean"
m, mp = 0, ""
for dp, dn, fn in os.walk(L):
    for f in fn:
        p = os.path.join(dp, f)
        if len(p) > m:
            m, mp = len(p), p
print("lake build max abs:", m, mp[-100:])
