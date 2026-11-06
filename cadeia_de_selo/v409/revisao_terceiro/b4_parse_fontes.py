import re, json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/revisao_terceiro/_fontes_compilar/"
trio = {"propext", "Classical.choice", "Quot.sound"}
out = {}
for N in ("TraducaoTuring", "ParNaFaceDeFock"):
    t = open(R + "out_%s.txt" % N, encoding="utf-8").read()
    ax = {m.group(1): sorted(x.strip() for x in re.sub(r"\s+", " ", m.group(2)).split(",") if x.strip()) for m in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]*)\]", t)}
    fora = {k: v for k, v in ax.items() if not set(v) <= trio or not v}
    linhas_estranhas = [l for l in t.split("\n") if l.strip() and "depends on axioms" not in l and not l.startswith("rc=") and not l.startswith("  ") and "propext" not in l]
    out[N] = {"print_axioms": len(ax), "fora_do_trio": len(fora), "so_propext": [k for k, v in ax.items() if v == ["propext"]], "rc": re.findall(r"rc=(\d+)", t), "tempo": open(R + "tempo_%s.txt" % N).read().strip(), "linhas_estranhas": linhas_estranhas[:5]}
    print(N, out[N])
json.dump(out, open(R + "../b4_fontes_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
