import ast, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
cs = open(R + "um_v409_candidato.py", "rb").read().decode("utf-8"); bs = open(R + "base_v408/um.py", "rb").read().decode("utf-8")
def lf(src):
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_LEAN_THEOREM_FLAGS": return ast.literal_eval(n.value)
novas = {k: v for k, v in lf(cs).items() if k not in lf(bs)}
al = open(R + "kernel/audit.log", "rb").read().decode("utf-8", "replace")
dep = set(m.group(1) for m in re.finditer(r"'([^']+)' depends on axioms", al)); nodep = set(m.group(1) for m in re.finditer(r"'([^']+)' does not depend on any axioms", al))
print("novas:", len(novas), "| com 'depends on axioms':", sum(1 for v in novas.values() if v in dep), "| 'does not depend':", sum(1 for v in novas.values() if v in nodep), "| nenhum dos dois:", sum(1 for v in novas.values() if v not in dep and v not in nodep))
