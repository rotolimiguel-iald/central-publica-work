# -*- coding: utf-8 -*-
"""exame_codigo_v388.py -- exame ESTATICO do um.py v388 (ordem do operador 06/10 via c1). SO LEITURA do Nos: copia de bytes para esta pasta,
confere o sha16 e analisa a copia. Nada e' executado do um.py. Saida: EXAME_CODIGO_v388.json (achados com linha, gravidade, evidencia)."""
import ast, collections, hashlib, io, json, os, re, shutil, sys, time, tokenize
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
ESPERADO = "e64b00f4df75059b"
SRC = os.path.join(NOS, "um.py"); COP = os.path.join(HERE, "um_v388_copia_exame.py")
raw = open(SRC, "rb").read(); h16 = hashlib.sha256(raw).hexdigest()[:16]
assert h16 == ESPERADO, "o um.py do Nos nao e a v388 (%s)" % h16
if not (os.path.exists(COP) and open(COP, "rb").read() == raw):
    open(COP + ".tmp", "wb").write(raw); os.replace(COP + ".tmp", COP)
text = raw.decode("utf-8"); L = text.split("\n")
R = {"um_py": {"path": SRC, "sha16": h16, "bytes": len(raw), "linhas": len(L)}, "achados": [], "contagens": {}}
def achado(cat, grav, linha, evid, nota=""):
    R["achados"].append({"categoria": cat, "gravidade": grav, "linha": linha, "evidencia": evid[:300], "nota": nota})
t0 = time.time(); tree = ast.parse(text, filename="um.py"); R["ast_parse"] = {"ok": True, "s": round(time.time() - t0, 1)}
# faixa do kernel embutido (literal de dados, fora da analise de codigo)
k0 = [i for i, l in enumerate(L) if l.startswith("_EMBEDDED_KERNEL_FILES = {")]; assert len(k0) == 1
k1 = k0[0] + 1
while L[k1].rstrip("\r") != "}":
    k1 += 1
EMB = (k0[0] + 1, k1 + 1); R["kernel_embutido_linhas"] = EMB
dentro_emb = lambda ln: EMB[0] <= ln <= EMB[1]

# (a) pyflakes
try:
    from pyflakes import api as pfa, reporter as pfr, messages as pfm
    class Rep(pfr.Reporter):
        def __init__(s): s.msgs = []
        def flake(s, m): s.msgs.append(m)
        def unexpectedError(s, f, m): s.msgs.append(("ERRO", m))
        def syntaxError(s, f, m, ln, off, t): s.msgs.append(("SINTAXE", m, ln))
    rep = Rep(); t0 = time.time(); pfa.check(text, "um.py", rep); R["pyflakes_s"] = round(time.time() - t0, 1)
    por = collections.Counter(type(m).__name__ if not isinstance(m, tuple) else m[0] for m in rep.msgs); R["contagens"]["pyflakes"] = dict(por)
    GRAV = {"UndefinedName": "CORRIGIR", "UndefinedLocal": "CORRIGIR", "UndefinedExport": "CORRIGIR", "SINTAXE": "BLOQUEIA", "ERRO": "BLOQUEIA",
            "RedefinedWhileUnused": "NOTA", "UnusedImport": "NOTA", "UnusedVariable": "NOTA", "FStringMissingPlaceholders": "NOTA",
            "ImportShadowedByLoopVar": "NOTA", "IsLiteral": "CORRIGIR", "PercentFormatInvalidFormat": "CORRIGIR", "PercentFormatPositionalCountMismatch": "CORRIGIR",
            "PercentFormatExtraNamedArguments": "CORRIGIR", "PercentFormatMissingArgument": "CORRIGIR", "StringDotFormatMissingArgument": "CORRIGIR",
            "StringDotFormatExtraPositionalArguments": "NOTA", "StringDotFormatExtraNamedArguments": "NOTA", "MultiValueRepeatedKeyLiteral": "CORRIGIR",
            "DuplicateArgument": "BLOQUEIA", "ReturnOutsideFunction": "BLOQUEIA", "TooManyExpressionsInStarredAssignment": "BLOQUEIA"}
    for m in rep.msgs:
        if isinstance(m, tuple):
            achado("pyflakes:" + m[0], "BLOQUEIA", m[2] if len(m) > 2 else None, str(m[1])); continue
        n = type(m).__name__; ln = m.lineno
        achado("pyflakes:" + n, GRAV.get(n, "NOTA"), ln, (m.message % m.message_args) + " | " + L[ln - 1].strip()[:160])
except ImportError as e:
    R["pyflakes"] = "AUSENTE: %s" % e

# (b) except vazios / silenciosos
nb = ns = 0
for n in ast.walk(tree):
    if isinstance(n, ast.ExceptHandler):
        if n.type is None:
            nb += 1; achado("except_nu", "NOTA", n.lineno, L[n.lineno - 1].strip())
        if len(n.body) == 1 and isinstance(n.body[0], ast.Pass):
            ns += 1; achado("except_silencioso_pass", "NOTA", n.lineno, L[n.lineno - 1].strip() + " ... pass")
R["contagens"]["except_nu"] = nb; R["contagens"]["except_pass"] = ns

# (c) literais de beta: constantes float no CODIGO (fora do kernel embutido) e ocorrencias do digito em texto/comentario
BETA_RE = re.compile(r"0\.0120313")
nfl = 0
for n in ast.walk(tree):
    if isinstance(n, ast.Constant) and isinstance(n.value, float) and abs(n.value - 0.0120313004) < 5e-8:
        nfl += 1; achado("beta_literal_no_codigo", "BLOQUEIA", n.lineno, L[n.lineno - 1].strip())
toks = {"comentario": 0, "string": 0}
cl = []
for tk in tokenize.generate_tokens(io.StringIO(text).readline):
    if tk.type in (tokenize.COMMENT, tokenize.STRING) and BETA_RE.search(tk.string):
        toks["comentario" if tk.type == tokenize.COMMENT else "string"] += 1
        if tk.type == tokenize.STRING and not dentro_emb(tk.start[0]):
            cl.append((tk.start[0], tk.string[:120]))
R["contagens"]["beta_literal_float_no_codigo"] = nfl; R["contagens"]["beta_digitos_em_texto"] = toks
for ln, s in cl:
    ctx = L[ln - 1]
    g = "NOTA"
    achado("beta_digitos_em_string", g, ln, ctx.strip()[:200], "texto/citacao/guarda; nao e' motor (o motor e' ALPHA*SQRT_E)")

# (d) vereditos proibidos em literais de string (fora do kernel embutido)
PROIB = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED")
GUARDA_CTX = re.compile(r"proib|forbid|FORBID|guard|GUARD|nunca|never|NEVER|!=|not in|nao e|não é|is not|PROIB|BANNED|banned|refus|recus|vedad|disallow|assert not|_BAD|BAD_|blacklist|NOT_A_|NAO_|em vez de|instead|nem |nor ", re.I)
npr = collections.Counter()
for n in ast.walk(tree):
    if isinstance(n, ast.Constant) and isinstance(n.value, str) and not dentro_emb(n.lineno) and PROIB.search(n.value):
        ctx = "\n".join(L[max(0, n.lineno - 3): n.lineno + 1])
        if GUARDA_CTX.search(ctx) or GUARDA_CTX.search(n.value):
            npr["em_guarda_ou_negacao"] += 1
        else:
            npr["a_revisar"] += 1; achado("veredito_proibido_em_literal", "CORRIGIR", n.lineno, n.value[:200], "contexto sem guarda/negacao detectada -- revisar")
R["contagens"]["vereditos_proibidos_em_literais"] = dict(npr)

# (e) versao: UM_VERSION, versoes futuras, carimbos de versao corrente
uv = [i + 1 for i, l in enumerate(L) if re.match(r'UM_VERSION\s*=', l)]
R["UM_VERSION"] = {"linhas": uv, "valor": [re.search(r'"(v\d+)"', L[i - 1]).group(1) for i in uv]}
if R["UM_VERSION"]["valor"] != ["v388"]:
    achado("versao", "BLOQUEIA", uv, str(R["UM_VERSION"]))
FUT = re.compile(r"\bv3(89|9\d)\b|\bv4\d\d\b")
for i, l in enumerate(L, 1):
    if not dentro_emb(i) and FUT.search(l):
        achado("versao_futura_citada", "NOTA", i, l.strip()[:200], "versao > v388 citada (plano/rota?)")
# um_version literal atribuido fora de UM_VERSION
for i, l in enumerate(L, 1):
    m = re.search(r'["\']um_version["\']\s*:\s*["\'](v\d+)["\']', l)
    if m and not dentro_emb(i):
        achado("um_version_literal", "CORRIGIR" if m.group(1) != "v388" else "NOTA", i, l.strip()[:200])

# (f) funcoes definidas duas vezes no MESMO escopo; registros core["..._vNNN"] atribuidos mais de uma vez
def escopo(body, nome):
    c = collections.defaultdict(list)
    for s in body:
        if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            c[s.name].append(s.lineno)
    for k, v in c.items():
        if len(v) > 1:
            achado("definida_duas_vezes", "CORRIGIR", v, "%s em %s: linhas %s" % (k, nome, v), "a ultima definicao vence; a(s) anterior(es) e' codigo morto")
    for s in body:
        if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            escopo(s.body, s.name)
escopo(tree.body, "<modulo>")
REG = re.compile(r'core\[\s*["\']([A-Za-z0-9_]+_v\d{3})["\']\s*\]\s*=(?!=)')
regs = collections.defaultdict(list)
for i, l in enumerate(L, 1):
    for m in REG.finditer(l):
        regs[m.group(1)].append(i)
dup = {k: v for k, v in regs.items() if len(v) > 1}
R["contagens"]["registros_vNNN"] = len(regs); R["contagens"]["registros_vNNN_atribuidos_mais_de_uma_vez"] = len(dup)
for k, v in dup.items():
    achado("registro_vNNN_duplicado", "NOTA", v, "%s atribuido em %s" % (k, v), "pode ser try/except (fallback) -- ver as linhas")

# (g) chaves do selo sem produtor no codigo
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
semp = [k for k in selo if ('"%s"' % k) not in text and ("'%s'" % k) not in text]
R["contagens"]["chaves_do_selo"] = len(selo); R["contagens"]["chaves_do_selo_sem_produtor_literal"] = len(semp)
for k in semp:
    achado("chave_do_selo_sem_produtor", "NOTA", None, k, "nenhum literal da chave no codigo (pode ser composta dinamicamente)")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
semc = [k for k in core if ('"%s"' % k) not in text and ("'%s'" % k) not in text]
R["contagens"]["chaves_do_core"] = len(core); R["contagens"]["chaves_do_core_sem_literal"] = len(semc)
R["chaves_do_core_sem_literal"] = semc[:200]

# (h) escada
el = core.get("external_ladder") or {}; kf = core.get("kernel_formalization") or {}
nflags_ext = sum(1 for k in kf if k.startswith("ext_") and kf[k] is True)
R["escada"] = {"n_theorems_clean": el.get("n_theorems_clean"), "n_theorems_expected": el.get("n_theorems_expected"), "ext_True_em_kernel_formalization": nflags_ext,
               "selo_um_version": selo.get("um_version")}
if not (el.get("n_theorems_clean") == el.get("n_theorems_expected") == 6154):
    achado("escada", "BLOQUEIA", None, json.dumps(R["escada"]))

# (i) kernel embutido x Nos\tgl_kernel x sandboxes (v376 e v388)
d = ast.literal_eval("".join(l + "\n" for l in L[EMB[0] - 1:EMB[1]]).split("=", 1)[1].strip())
R["kernel_embutido_n_arquivos"] = len(d)
def compara(raiz, nome):
    eq = dif = falta = 0; difs = []; faltas = []
    for rel, conteudo in d.items():
        p = os.path.join(raiz, *rel.replace("\\", "/").split("/"))
        if not os.path.isfile(p):
            falta += 1; faltas.append(rel); continue
        b = open(p, "rb").read()
        cb = conteudo.encode("utf-8") if isinstance(conteudo, str) else conteudo
        if b == cb or b.replace(b"\r\n", b"\n") == cb.replace(b"\r\n", b"\n"):
            eq += 1
        else:
            dif += 1; difs.append(rel)
    return {"raiz": raiz, "iguais": eq, "diferentes": dif, "ausentes": falta, "diferentes_lista": difs[:60], "ausentes_lista": faltas[:80]}
SB376 = os.path.join("C:" + os.sep, "Users", "rotol", "AppData", "Local", "Temp", "claude", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d", "scratchpad", "v376", "kernel_src")
SB388 = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "v388_kernel", "kernel_src")
R["kernel_comparacao"] = {"Nos_tgl_kernel": compara(os.path.join(NOS, "tgl_kernel"), "nos"), "sandbox_v376": compara(SB376, "v376"), "sandbox_v388": compara(SB388, "v388")}
for k, v in R["kernel_comparacao"].items():
    if k != "sandbox_v376" and (v["diferentes"] or v["ausentes"]):
        achado("kernel_embutido_difere", "CORRIGIR", None, "%s: %d diferentes, %d ausentes" % (k, v["diferentes"], v["ausentes"]))

# (j) TODO/FIXME/XXX/sorry no codigo (fora do kernel embutido)
TF = re.compile(r"\bTODO\b|\bFIXME\b|\bXXX\b|\bHACK\b")
SR = re.compile(r"\bsorry\b")
c_tf = c_sr = 0
for i, l in enumerate(L, 1):
    if dentro_emb(i):
        continue
    if TF.search(l):
        c_tf += 1; achado("TODO_FIXME", "NOTA", i, l.strip()[:200])
    if SR.search(l):
        c_sr += 1
R["contagens"]["TODO_FIXME_fora_do_kernel"] = c_tf; R["contagens"]["linhas_com_sorry_fora_do_kernel"] = c_sr
# sorry DENTRO do kernel embutido (codigo Lean): conta tokens 'sorry' fora de comentario Lean
nsl = []
for rel, c in d.items():
    if not rel.endswith(".lean"):
        continue
    s = re.sub(r"/-.*?-/", "", c, flags=re.S); s = re.sub(r"--[^\n]*", "", s)
    s = re.sub(r'"(?:[^"\\]|\\.)*"', '""', s)
    if re.search(r"\bsorry\b|\badmit\b", s):
        nsl.append(rel)
R["contagens"]["arquivos_lean_com_sorry_fora_de_comentario"] = len(nsl)
for rel in nsl:
    achado("sorry_no_lean_embutido", "BLOQUEIA", None, rel)

R["resumo"] = dict(collections.Counter(a["gravidade"] for a in R["achados"]))
R["por_categoria"] = {}
for a in R["achados"]:
    R["por_categoria"].setdefault(a["categoria"], collections.Counter())[a["gravidade"]] += 1
R["por_categoria"] = {k: dict(v) for k, v in R["por_categoria"].items()}
p = os.path.join(HERE, "EXAME_CODIGO_v388.json")
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print(json.dumps({"resumo": R["resumo"], "por_categoria": R["por_categoria"], "contagens": R["contagens"], "escada": R["escada"],
                  "kernel": {k: {kk: v[kk] for kk in ("iguais", "diferentes", "ausentes")} for k, v in R["kernel_comparacao"].items()}}, ensure_ascii=False, indent=1))
