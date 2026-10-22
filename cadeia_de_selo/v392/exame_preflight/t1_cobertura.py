import re, sys, io
C = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\um_v392_candidato.py"
lines = open(C, encoding="utf-8").read().split("\n")
def grab(start_pat):
    i = next(k for k,l in enumerate(lines) if l.startswith(start_pat))
    j = i+1
    while j < len(lines) and (lines[j].startswith((" ", "\t")) or lines[j]=="" ): j += 1
    return "\n".join(lines[i:j])
g = {}
exec(grab("_V392_KH ="), g)
exec(grab("def _v392_axiom_coverage"), g)
N = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" + "\\"
def parts(fn):
    t = open(N+fn, encoding="utf-8").read()
    so = t.split("--- STDOUT ---\n",1)[1]; out, err = so.split("\n--- STDERR ---\n",1)
    return out, err, t[:300]
for stage in ["", "_selftest_restored", "_selftest_tampered"]:
    bo, be, h = parts("tgl_kernel_build_capture%s.txt"%stage)
    ao, ae, h2 = parts("tgl_kernel_audit_capture%s.txt"%stage)
    blob = bo+be+ao+ae
    axioms = {}
    for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", blob, re.S):
        axioms[m.group(1)] = [a.strip() for a in m.group(2).replace("\n"," ").split(",") if a.strip()]
    for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", blob):
        axioms.setdefault(m.group(1), [])
    print("== stage", stage or "principal", h.splitlines()[:3], h2.splitlines()[:3])
    print(" audit-only:", g["_v392_axiom_coverage"](ao+ae, axioms))
    print(" blob:", {k:v for k,v in g["_v392_axiom_coverage"](blob, axioms).items() if k in ("ok","motivo","linhas")})
    print(" n axioms", len(axioms), "TOTAL lines build", len(re.findall(r"TGL_AXIOM_COVERAGE_TOTAL", bo+be)), "audit", len(re.findall(r"TGL_AXIOM_COVERAGE_TOTAL", ao+ae)))
    print(" sorryAx in blob", "sorryAx" in blob, "build rc / audit rc lines", h.splitlines()[2], h2.splitlines()[2])
