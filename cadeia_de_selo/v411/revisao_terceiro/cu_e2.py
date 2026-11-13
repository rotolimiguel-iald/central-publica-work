"""CU-E2: (1) o portao 'kernel' de gerar_relatorio_v411.py: o AST de hoje x o do backup (quais condicoes sumiram); (2) varredura das linhas ACRESCENTADAS nos 29 arquivos (.py) por comentario inline que engole codigo (comentario com and/or/==/.get( depois do #)."""
import ast, difflib, glob, hashlib, io, os, re, sys, tokenize
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
rd = lambda p: open(p, "rb").read().decode("utf-8")
new = rd(os.path.join(V, "gerar_relatorio_v411.py"))
old = rd(os.path.join(V, "gerar_relatorio_v411.py.bak_20261112_194113_r1fix"))


def portao_kernel(src):
    t = ast.parse(src)
    for n in ast.walk(t):
        if isinstance(n, ast.Dict):
            for k, v in zip(n.keys, n.values):
                if isinstance(k, ast.Constant) and k.value == "kernel" and isinstance(v, ast.Call):
                    return v
    return None


def conds(call):
    b = call.args[0]
    out = []
    if isinstance(b, ast.BoolOp):
        for x in b.values:
            out.append(ast.unparse(x)[:150])
    return out


co, cn = conds(portao_kernel(old)), conds(portao_kernel(new))
print("condicoes do portao kernel: antes", len(co), "| hoje", len(cn))
print("SUMIRAM:", [c for c in co if c not in cn])
print("ENTRARAM:", [c for c in cn if c not in co])
# onde esta' o # na linha
for i, l in enumerate(new.splitlines(), 1):
    if '"kernel": bool(' in l:
        j = l.index("#")
        print("linha", i, "| o # esta' na coluna", j, "| o que vem DEPOIS do # na mesma linha (150 chars):", l[j:j + 150])
# (2) varredura geral
bks = [b for b in glob.glob(os.path.join(V, "**", "*r1fix*"), recursive=True) if os.sep + "revisao_terceiro" + os.sep not in b]
susp = []
for b in sorted(bks):
    o = re.sub(r"\.bak_\d{8}_\d{6}_r1fix$", "", b)
    if not o.endswith(".py"):
        continue
    a = rd(b).splitlines()
    c = rd(o).splitlines()
    for ln in difflib.unified_diff(a, c, lineterm="", n=0):
        if not ln.startswith("+") or ln.startswith("+++"):
            continue
        s = ln[1:]
        if s.lstrip().startswith("#") or "#" not in s:
            continue
        # tokeniza para achar o COMENTARIO real
        try:
            toks = list(tokenize.generate_tokens(io.StringIO(s + "\n").readline))
        except Exception:
            continue
        for tk in toks:
            if tk.type == tokenize.COMMENT:
                com = tk.string
                if re.search(r"\band\b.*(?:==|\.get\(|\bis\b|\)\s*$)|\bor\b.*\.get\(|\)\s*==", com) and re.search(r"\.get\(|==|\bis True\b", com):
                    susp.append((os.path.relpath(o, V), s[:60], com[:200]))
print("linhas acrescentadas com comentario que parece conter codigo:", len(susp))
for x in susp:
    print("   ", x)
