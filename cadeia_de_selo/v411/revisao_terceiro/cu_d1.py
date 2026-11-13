"""CU-D1: a cadeia do pos-rito e o rito: scripts invocados existem e compilam em memoria (sem .pyc); modulos locais que eles importam existem onde o sys.path deles alcanca."""
import ast, importlib.util, os, re, subprocess, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
TOOLS = r"C:\IALD\Central de Patentes\work\cadeia_de_selo"
SEL = os.path.join(V, "pos_rito")
sys.dont_write_bytecode = True
rd = lambda p: open(p, "rb").read().decode("utf-8")
# 1. sh -n
bash = r"C:\Program Files\Git\bin\sh.exe"
if not os.path.exists(bash):
    bash = "sh"
for f in (os.path.join(SEL, "chain_pos_rito_v411.sh"), os.path.join(V, "rito_v411.sh")):
    r = subprocess.run([bash, "-n", f], capture_output=True, text=True)
    print("sh -n", os.path.basename(f), "rc", r.returncode, r.stderr[:200])
# 2. scripts .py invocados pela cadeia e pelo rito (nomes literais)
chain = rd(os.path.join(SEL, "chain_pos_rito_v411.sh"))
rito = rd(os.path.join(V, "rito_v411.sh"))
nomes = set(re.findall(r"\$(?:SEL|PK|TOOLS|ENST)/([A-Za-z0-9_./\-]+\.py)", chain + rito)) | set(re.findall(r"\"\$SEL/([A-Za-z0-9_.\-]+\.py)\"", chain))
nomes |= set(re.findall(r"\bfor q in ([^;]+); do", chain)[0].split())
nomes = {n for n in nomes if n.endswith(".py")}
print("scripts nomeados:", len(nomes))
roots = {"PK": V, "SEL": SEL, "TOOLS": TOOLS}


def achar(n):
    for base in (V, SEL, TOOLS, os.path.join(V, "bancada_B3_servico")):
        p = os.path.join(base, n.replace("/", os.sep))
        if os.path.isfile(p):
            return p
    return None


ausentes = []
compila = {}
for n in sorted(nomes):
    p = achar(n)
    if not p:
        ausentes.append(n)
        continue
    try:
        compile(rd(p), p, "exec")
        compila[n] = p
    except Exception as e:
        print("NAO COMPILA:", n, repr(e)[:150])
print("ausentes (nao achados em v411, pos_rito, cadeia_de_selo):", ausentes)
print("compilam em memoria:", len(compila))
# 3. imports locais de cada script
std = set(sys.stdlib_module_names)
faltam = {}
for n, p in sorted(compila.items()):
    t = ast.parse(rd(p))
    mods = set()
    for x in ast.walk(t):
        if isinstance(x, ast.Import):
            for a in x.names:
                mods.add(a.name.split(".")[0])
        elif isinstance(x, ast.ImportFrom) and x.level == 0 and x.module:
            mods.add(x.module.split(".")[0])
    # sys.path.insert explicitos
    extra = re.findall(r"sys\.path\.(?:insert|append)\((?:0, )?([^)]+)\)", rd(p))
    for m in sorted(mods):
        if m in std:
            continue
        locais = [b for b in (os.path.dirname(p), V, SEL, TOOLS) if os.path.isfile(os.path.join(b, m + ".py")) or os.path.isdir(os.path.join(b, m))]
        spec = None
        try:
            spec = importlib.util.find_spec(m)
        except Exception:
            spec = None
        if not locais and spec is None:
            faltam.setdefault(n, []).append((m, extra[:2]))
        elif not locais and spec is not None:
            pass
print("imports que nao achei nem local nem instalado:", faltam)
# 4. os imports locais de cada um, em que pasta: o script esta' em SEL e importa um modulo que so' existe em V (ou o contrario)?
for n, p in sorted(compila.items()):
    d = os.path.dirname(p)
    t = ast.parse(rd(p))
    mods = set()
    for x in ast.walk(t):
        if isinstance(x, ast.Import):
            for a in x.names:
                mods.add(a.name.split(".")[0])
        elif isinstance(x, ast.ImportFrom) and x.level == 0 and x.module:
            mods.add(x.module.split(".")[0])
    onde = {}
    for m in sorted(mods):
        if m in std:
            continue
        for b, tag in ((d, "mesma"), (V, "PK"), (SEL, "SEL"), (TOOLS, "TOOLS")):
            if os.path.isfile(os.path.join(b, m + ".py")):
                onde[m] = tag
                break
    alc = [m for m, tag in onde.items() if tag != "mesma"]
    sp = re.findall(r"sys\.path\.(?:insert|append)\([^)]*\)", rd(p))
    if alc:
        print("   %-34s modulos locais fora da propria pasta: %s | sys.path: %s" % (n, {m: onde[m] for m in alc}, [s[:70] for s in sp[:2]]))
