# X19 (so teste; a decisao e do operador): as linhas de Audit da LightNetStandardWedgeDataBGL lidas pela regex do um.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leanlib as L  # noqa: E402
from etapa_C_raiz_auditoria import aux, ler_umpy  # noqa: E402

F = L.F
OV = os.path.join(F, "ov")
CONJ = os.path.join(F, "conj")
LOG = os.path.join(F, "logs", "C")
J2 = os.path.join(F, "logs", "B", "B_J2_ConjuntoV392ComX19_r1.log")
decl = []
for l in open(J2, encoding="utf-8"):
    if l.startswith("COB\t"):
        c = l.rstrip("\n").split("\t")
        if c[1] == "TGLExt.LightNetStandardWedgeDataBGL" and c[3] in ("thm", "def", "induct") and not aux(c[2]):
            decl.append((c[2], c[3]))
decl.sort()
p = os.path.join(CONJ, "C_AuditDeltaX19.lean")
if not os.path.exists(p):
    open(p, "w", encoding="utf-8", newline="\n").write(
        "-- AUDITORIA DELTA X19 (so teste; decisao do operador), exame F_KERNEL 12/10/2026\nimport TGL\n"
        "import TGLExt.LightNetStandardWedgeDataBGL\n\n" + "".join("#print axioms %s\n" % n for n, _ in decl))
r = L.run_lean("C_audit_delta_x19", p, CONJ, None, LOG, kernel_lib=OV)
ax = ler_umpy(open(r["log"], "rb").read().decode("utf-8", "replace"))
falt = [n for n, _ in decl if n not in ax]
fora = [n for n, _ in decl if n in ax and not set(ax[n]) <= L.TRIO]
r.update({"declaracoes": decl, "lidos": len(ax), "faltam": falt, "fora": fora})
print("x19 delta rc", r["rc"], "s", r["segundos"], "decl", len(decl), "lidos", len(ax), "faltam", len(falt), "fora", len(fora))
print(L.dump(r, os.path.join(F, "RESULTADO_C_delta_x19.json")))
