import ast, sys, json
sys.stdout.reconfigure(encoding="utf-8")
A = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
B = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\coverage_candidate_r8\um_v394_prechecked.py"


def lit(p, names):
    t = open(p, "rb").read().decode("utf-8"); tr = ast.parse(t); out = {}
    for n in tr.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in names:
            out[n.targets[0].id] = ast.literal_eval(n.value)
    return out


nm = {"_V393_SPECS", "_V393_FONTES", "_V393_VERBATINS2"}
a = lit(A, nm); b = lit(B, nm)
sa = {s["nome"]: s for s in a["_V393_SPECS"]}; sb = {s["nome"]: s for s in b["_V393_SPECS"]}
for k in sb:
    if k not in sa:
        print("NOVO spec", k, json.dumps(sb[k], ensure_ascii=False)[:2500])
    elif sa[k] != sb[k]:
        print("MUDOU spec", k)
        for kk in sb[k]:
            if sa[k].get(kk) != sb[k].get(kk):
                print("   campo", kk, str(sa[k].get(kk))[:1500], "->", str(sb[k].get(kk))[:1500])
print("fontes mudadas:", [k for k in a["_V393_FONTES"] if a["_V393_FONTES"][k] != b["_V393_FONTES"].get(k)])
print("verb igual:", a["_V393_VERBATINS2"] == b["_V393_VERBATINS2"])
