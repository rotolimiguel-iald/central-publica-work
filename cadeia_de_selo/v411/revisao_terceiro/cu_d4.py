import ast, glob, hashlib, os
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
# C-09 (a): compila em memoria; so' a linha 237 mudou
p = os.path.join(V, "orquestrador", "pos_treino_v411.py")
src = open(p, "rb").read().decode("utf-8")
compile(src, p, "exec")
print("orquestrador/pos_treino_v411.py compila em memoria; sha16", sha16(p))
b = glob.glob(p + ".bak_*_r1fix")[0]
import difflib
a = open(b, "rb").read().decode("utf-8").splitlines()
c = src.splitlines()
d = [l for l in difflib.unified_diff(a, c, lineterm="", n=0) if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
print("linhas diferentes (+/-):", len(d), "| numeros de linha do hunk:", [l for l in difflib.unified_diff(a, c, lineterm="", n=0) if l.startswith("@@")])
# C-11
pr = os.path.join(V, "pos_rito")
print("pos_rito: arquivos *DEPURACAO*:", [f for f in os.listdir(pr) if "DEPURACAO" in f])
dd = r"C:\t\k411c\conserto_r1\depuracao"
if os.path.isdir(dd):
    print("depuracao movida:", {f: sha16(os.path.join(dd, f)) for f in os.listdir(dd)})
# arquivos .pyc / __pycache__ novos no pacote?
print("__pycache__ no pacote:", [r for r, ds, fs in os.walk(V) if os.path.basename(r) == "__pycache__"][:5])
