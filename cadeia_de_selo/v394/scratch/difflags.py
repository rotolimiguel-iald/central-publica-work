import ast, json, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = "C:" + os.sep
R8 = os.path.join(C, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "F1.FECHO_20261015", "coverage_candidate_r8", "um_v394_prechecked.py")
t = open(R8, "rb").read().decode("utf-8"); tr = ast.parse(t)
g = {}
for n in tr.body:
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_LEAN_THEOREM_FLAGS"):
        g[n.targets[0].id] = ast.literal_eval(n.value)
AL = open(os.path.join(HERE, "kernel", "audit.log"), encoding="utf-8").read()
src = {}
for line in AL.splitlines():
    if line.startswith("TGL_DECL_SOURCE\t"):
        _, nme, mod = line.split("\t"); src[nme] = mod
new = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v394.json"), encoding="utf-8"))["novos"]
newm = {p[:-5].replace("/", ".") for p in new}
mine = {n: m for n, m in src.items() if m in newm}
TEMPO = {"TGLExt.TimeGravitonMatrix", "TGLExt.TimeGravitonScalar", "TGLExt.TimeGravitonFlow", "TGLExt.TimeGravitonKraus"}
for nome, key, pred in (("tempo", "_V394_FORMAL_CONTRACT", lambda m: m in TEMPO), ("quad", "_V394_QUADRATIC_CONTRACT", lambda m: m == "TGLExt.RuleQuadraticResidual")):
    c = set(g[key]["theorems"]); m = {n for n, mod in mine.items() if pred(mod)}
    print(nome, "codex", len(c), "meu(todas)", len(m), "so_meu", sorted(m - c)[:8], len(m - c), "so_codex", sorted(c - m)[:5])
c = set(g["_V394_NETWORK_CONTRACT"]["declarations"]); m = {n for n, mod in mine.items() if mod.startswith("TGLExt.F1Fecho394.")}
pub = {n for n in m if not n.startswith("_private.")}
print("rede codex", len(c), "meu(todas)", len(m), "meu(pub)", len(pub), "so_meu_pub", len(pub - c), sorted(pub - c)[:15], "so_codex", sorted(c - m)[:5])
# classificacao dos nomes so' meus
def suf(n):
    return n.split(".")[-1]
print("so_meu_pub por sufixo:", collections.Counter(re.sub(r"\d+", "#", suf(n)) for n in pub - c).most_common(12))
tm = {n for n, mod in mine.items() if mod in TEMPO}
print("tempo so_meu por sufixo:", collections.Counter(re.sub(r"\d+", "#", suf(n)) for n in tm - set(g["_V394_FORMAL_CONTRACT"]["theorems"])).most_common(12))
fl = set(g["_LEAN_THEOREM_FLAGS"].values())
print("codex flags nome nos meus modulos novos:", len(fl & set(mine)), "| codex flags (novas) fora dos meus:", len(fl - set(src)))
