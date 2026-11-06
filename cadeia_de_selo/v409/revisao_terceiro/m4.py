import json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
FL = json.load(open(R + "kernel/FLAGS_v409.json", encoding="utf-8"))
names = [f[1] for f in FL["flags"]]
al = open(R + "kernel/audit.log", "rb").read().decode("utf-8", "replace")
dep = set(m.group(1) for m in re.finditer(r"'([^']+)' depends on axioms", al)); nodep = set(m.group(1) for m in re.finditer(r"'([^']+)' does not depend on any axioms", al))
print("flags:", len(names), "| 'depends on axioms':", sum(1 for n in names if n in dep), "| 'does not depend':", sum(1 for n in names if n in nodep), "| nenhum:", sum(1 for n in names if n not in dep and n not in nodep))
anc = set(json.load(open(R + "CANDIDATO_v409.json", encoding="utf-8"))["kernel"]["ancoras"])
print("ancoras (teoremas-ancora):", len(anc), "| flags que NAO sao ancoras:", len([n for n in names if n not in anc]))
