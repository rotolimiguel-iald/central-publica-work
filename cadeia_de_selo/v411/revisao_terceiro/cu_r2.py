"""CU-R2: reconferencia SO' do CU-1: diff do backup _cu1fix, AST do portao kernel (12 antes do conserto + a do C-10), compila em memoria, sha16."""
import ast, difflib, glob, hashlib, os, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
rd = lambda p: open(p, "rb").read().decode("utf-8")
atual = os.path.join(V, "gerar_relatorio_v411.py")
bk_cu1 = glob.glob(os.path.join(V, "gerar_relatorio_v411.py.bak_*_cu1fix"))
bk_r1 = os.path.join(V, "gerar_relatorio_v411.py.bak_20261112_194113_r1fix")
print("backups cu1fix:", [os.path.basename(b) for b in bk_cu1], sha16(bk_cu1[0]))
print("atual sha16:", sha16(atual), "| r1fix sha16:", sha16(bk_r1))
a, c = rd(bk_cu1[0]).splitlines(), rd(atual).splitlines()
print("linhas: backup", len(a), "hoje", len(c))
hunks = [l for l in difflib.unified_diff(a, c, lineterm="", n=0) if l.startswith("@@")]
print("hunks:", hunks)
mud = [l for l in difflib.unified_diff(a, c, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
print("linhas +/-:", len(mud))
for l in mud:
    print("   ", l[:130], "...", l[-110:])


def portao_kernel(src):
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Dict):
            for k, v in zip(n.keys, n.values):
                if isinstance(k, ast.Constant) and k.value == "kernel" and isinstance(v, ast.Call):
                    return v
    return None


def conds(call):
    return [ast.unparse(x) for x in call.args[0].values]


co, cn = conds(portao_kernel(rd(bk_r1))), conds(portao_kernel(rd(atual)))
print("condicoes: antes do conserto", len(co), "| hoje", len(cn))
print("falta alguma das 12 de antes do conserto:", [x for x in co if x not in cn])
print("a mais hoje:", [x[:120] for x in cn if x not in co])
print("ordem das 12 preservada:", [x for x in cn if x in co] == co)
# o resto do arquivo por AST: mesmo AST do backup cu1fix?
print("AST do arquivo inteiro igual ao do backup cu1fix:", ast.dump(ast.parse(rd(bk_cu1[0]))) == ast.dump(ast.parse(rd(atual))))
# compila em memoria
compile(rd(atual), atual, "exec")
print("compila em memoria: sim")
# demais PORTOES: mesmas condicoes que no backup r1fix, fora o kernel?


def todos(src):
    t = ast.parse(src)
    for n in ast.walk(t):
        if isinstance(n, ast.Dict) and any(isinstance(k, ast.Constant) and k.value == "kernel" for k in n.keys):
            return {k.value: ast.unparse(v) for k, v in zip(n.keys, n.values) if isinstance(k, ast.Constant)}


pa, pn = todos(rd(bk_cu1[0])), todos(rd(atual))
print("portoes: n antes", len(pa), "hoje", len(pn), "| portoes com expressao diferente:", [k for k in pa if pa[k] != pn.get(k)])
