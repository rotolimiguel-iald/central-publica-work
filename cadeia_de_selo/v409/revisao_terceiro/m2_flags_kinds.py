import ast, json, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
cs = open(R + "um_v409_candidato.py", "rb").read().decode("utf-8"); bs = open(R + "base_v408/um.py", "rb").read().decode("utf-8")
def lf(src):
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_LEAN_THEOREM_FLAGS": return ast.literal_eval(n.value)
F7 = lf(cs); F6 = lf(bs); novas = {k: v for k, v in F7.items() if k not in F6}
al = open(R + "kernel/audit.log", "rb").read().decode("utf-8", "replace")
trio = {"propext", "Classical.choice", "Quot.sound"}
kind = {}; ax2 = {}
for m in re.finditer(r"BENCH_DECL\t([^\t]+)\t([^\t]+)\t([^\n]*)", al):
    kind[m.group(1)] = m.group(2); ax2[m.group(1)] = set(x for x in m.group(3).strip().split(",") if x)
cont = collections.Counter(kind.get(v, "?") for v in novas.values())
print("novas", len(novas), "por tipo (BENCH_DECL):", dict(cont))
sem_kind = [v for v in novas.values() if v not in kind]
print("sem BENCH_DECL:", len(sem_kind), sem_kind[:5])
fora = [v for v in novas.values() if v in ax2 and not ax2[v] <= trio]
print("novas fora do trio por BENCH_DECL:", fora[:5])
anc = json.load(open(R + "CANDIDATO_v409.json", encoding="utf-8"))["kernel"]["ancoras"]
print("ancoras:", len(anc), "tipos:", dict(collections.Counter(kind.get(a, "?") for a in anc)))
print("nao-teorema com bandeira:", len([v for v in novas.values() if kind.get(v) != "theorem"]), "| teoremas com bandeira:", len([v for v in novas.values() if kind.get(v) == "theorem"]))
