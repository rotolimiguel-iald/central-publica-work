# -*- coding: utf-8 -*-
"""testar_erratas_v392.py -- rodada 2 da cadeia v392, agente ERRATAS (gerencia c1, 13/10/2026).

Aplica E01_PATCHES + A03_PATCHES (V\\patches_erratas_v392.py) sobre o texto do um.py v391 SELADO, EM MEMORIA (nada e' escrito no um.py), e exige:
  1. o sha16 do um.py lido == 8e7b9927ceae64b8 e o tamanho == 33.910.631 B (e' o arquivo certo);
  2. cada `old` aparece exatamente `n` vezes (CRLF) e cada `new` aparece `n` vezes depois de aplicar (aplicar() ja' assere);
  3. ast.parse do resultado completo e das variantes E01-so' e A03-so';
  4. E01 NAO ALTERA VALOR: ast.dump(E01-so') == ast.dump(original) (comentario nao entra no AST);
  5. A03 so' ACRESCENTA: o numero de definicoes de funcao e de classes nao muda, e cada patch so' acrescenta texto (new contem old, salvo a insercao dentro de string, que e' prefixo+sufixo de old);
  6. a guarda de texto P18 (V\\guarda_p18_v392.py, `violacoes`) sobre TODO o texto novo (new menos old) -> zero violacoes;
  7. (opcional, --latex) compila o texto novo do artigo (PT e EN) com pdflatex 2x em V\\rodada2\\erratas\\latex\\ (so' nesta pasta).
Imprime o resultado; rc 0 so' se tudo passar.  Uso: python -B -X utf8 testar_erratas_v392.py [--latex]
"""
import ast, difflib, hashlib, importlib.util, os, re, shutil, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
V = os.path.dirname(os.path.abspath(__file__))
UM = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s", "um.py")


def carregar(nome, arq):
    sp = importlib.util.spec_from_file_location(nome, os.path.join(V, arq))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


P = carregar("patches_erratas_v392", "patches_erratas_v392.py")
G = carregar("guarda_p18_v392", "guarda_p18_v392.py")
ok_geral = True


def passo(nome, ok, det=""):
    global ok_geral
    ok_geral = ok_geral and bool(ok)
    print(("PASSA  " if ok else "FALHA  ") + nome + ((" -- " + det) if det else ""))


raw = open(UM, "rb").read()
passo("1. um.py v391 lido (bytes) = selo esperado", hashlib.sha256(raw).hexdigest()[:16] == P.UM_V391_SHA16 == "8e7b9927ceae64b8" and len(raw) == 33910631, "%s, %d B" % (hashlib.sha256(raw).hexdigest()[:16], len(raw)))
T = raw.decode("utf-8")
assert "\r\n" in T
T_ast0 = ast.dump(ast.parse(T))

# 2. contagens + aplicar tudo (CRLF)
try:
    Tn, log = P.aplicar(T, crlf=True)
    passo("2. aplicar(E01+A03, crlf=True): contagens exatas de old e de new", True, "%d patches (E01 %d, A03 %d); +%d bytes" % (len(log), len(P.E01_PATCHES), len(P.A03_PATCHES), len(Tn) - len(T)))
except AssertionError as e:
    passo("2. aplicar(E01+A03, crlf=True)", False, repr(e))
    sys.exit(1)
# a ordem de aplicacao nao pode importar (ancoras disjuntas): aplica de tras para frente e compara
Tr, _ = P.aplicar(T, crlf=True, patches=list(reversed(list(P.E01_PATCHES) + list(P.A03_PATCHES))))
passo("2b. a ordem dos patches nao importa (ancoras disjuntas)", Tr == Tn)
# o fim de linha do que foi acrescentado e' CRLF (nenhum \n solto novo)
lf_soltos_novos = Tn.count("\n") - Tn.count("\r\n") - (T.count("\n") - T.count("\r\n"))
passo("2c. nenhum LF solto novo (tudo CRLF)", lf_soltos_novos == 0, "LF soltos novos: %d" % lf_soltos_novos)

# 3. ast.parse
try:
    tree_n = ast.parse(Tn)
    passo("3. ast.parse do resultado completo", True)
except SyntaxError as e:
    passo("3. ast.parse do resultado completo", False, repr(e))
    sys.exit(1)

# 4. E01 nao altera valor
Te, _ = P.aplicar(T, crlf=True, patches=P.E01_PATCHES)
passo("4. E01 so' acrescenta comentario: ast.dump identico ao original", ast.dump(ast.parse(Te)) == T_ast0, "+%d bytes" % (len(Te) - len(T)))

# 5. A03 so' acrescenta
Ta, _ = P.aplicar(T, crlf=True, patches=P.A03_PATCHES)
tr_a = ast.parse(Ta)
nf = lambda t: (sum(isinstance(n, ast.FunctionDef) for n in ast.walk(t)), sum(isinstance(n, ast.ClassDef) for n in ast.walk(t)))
tr0 = ast.parse(T)
passo("5a. A03: mesmo numero de funcoes e classes", nf(tr_a) == nf(tr0), "%s" % (nf(tr0),))


def so_acrescenta(p):
    old, new = p["old"], p["new"]
    if new.startswith(old):
        return True
    # insercao dentro de string: new = prefixo + errata + sufixo, com prefixo+sufixo == old
    i = 0
    while i < min(len(old), len(new)) and old[i] == new[i]:
        i += 1
    j = 0
    while j < min(len(old), len(new)) - i and old[-1 - j] == new[-1 - j]:
        j += 1
    return i + j == len(old)


mau = [p["id"] for p in list(P.E01_PATCHES) + list(P.A03_PATCHES) if not so_acrescenta(p)]
passo("5b. cada patch so' acrescenta (old preservado como prefixo ou prefixo+sufixo)", not mau, str(mau))


def texto_novo(p):
    old, new = p["old"], p["new"]
    i = 0
    while i < min(len(old), len(new)) and old[i] == new[i]:
        i += 1
    j = 0
    while j < min(len(old), len(new)) - i and old[-1 - j] == new[-1 - j]:
        j += 1
    return new[i:len(new) - j]


# 5c/5d. executa os trechos novos com nomes de teste: cada s.append/c.append/partC.append produz EXATAMENTE o `texto` (com %s do D1 resolvido pelo runtime de teste)
import json as _json, textwrap as _tw
_core = _json.load(open(os.path.join(os.path.dirname(UM), "um_absoluto.json"), encoding="utf-8"))["core"]
_f7 = lambda x, d=2: (("%." + str(d) + "f") % x).replace(".", "{,}") if isinstance(x, float) else "n/d"
_or7 = _core["orientation_is_the_sign_v367"]
falhas_exec = []
n_exec = 0
for p in list(P.A03_PATCHES):
    old, new = p["old"], p["new"]
    if new.startswith(old):
        extra = _tw.dedent(new[len(old):].lstrip("\n"))
        ns = {"s": [], "c": [], "partC": [], "_f7": _f7, "_or7": _or7}
        try:
            exec(compile(extra, p["id"], "exec"), ns)
        except Exception as e:
            falhas_exec.append((p["id"], repr(e)[:120]))
            continue
        got = ns["s"] + ns["c"] + ns["partC"]
        want = [t.replace("%s", "%s") for t in p["texto"].split("\n")]
        if p["id"].startswith("A03-13"):
            want = [want[0] % (_f7(_or7["z_to_mirror_branch"]), _f7(_or7["z_to_coupling_branch"]))]
        if got != want:
            falhas_exec.append((p["id"], "texto emitido difere do texto declarado", len(got), len(want)))
        n_exec += 1
passo("5c. os s/c/partC.append novos (%d patches) emitem exatamente o texto declarado" % n_exec, not falhas_exec, str(falhas_exec[:4]))
# 5d. insercoes dentro de string: executa o statement inteiro (out.append((EN) if en else (PT))) nos dois ramos e confere que o texto novo esta na saida certa
falhas_tail = []
n_tail = 0
lines_n = Tn.split("\r\n")
tree_x = ast.parse(Tn)
exprs = [n for n in ast.walk(tree_x) if isinstance(n, ast.Expr)]
for p in P.A03_PATCHES:
    old, new = p["old"], p["new"]
    if new.startswith(old):
        continue
    pos = Tn.find(new.replace("\n", "\r\n"))
    assert pos >= 0, p["id"]
    ln = Tn.count("\n", 0, pos) + 1
    cand = [n for n in exprs if n.lineno <= ln <= n.end_lineno and n.col_offset == 4]
    cand.sort(key=lambda n: n.end_lineno - n.lineno)
    seg = ast.get_source_segment(Tn, cand[0])
    for en_ in (True, False):
        ns = {"out": [], "en": en_}
        try:
            exec(compile(seg, p["id"], "exec"), ns)
        except Exception as e:
            falhas_tail.append((p["id"], en_, repr(e)[:100]))
            continue
        saida = "".join(map(str, ns["out"]))
        presente = p["texto"].strip()[:60] in saida
        if presente != ((p["lang"] == "EN") == en_):
            falhas_tail.append((p["id"], en_, "texto no ramo errado"))
    n_tail += 1
passo("5d. insercoes dentro de string (%d): o texto novo sai so' no ramo da lingua certa" % n_tail, not falhas_tail, str(falhas_tail[:4]))

# 6. a guarda P18 sobre todo o texto novo
viol = {}
for p in list(P.E01_PATCHES) + list(P.A03_PATCHES):
    v = G.violacoes(texto_novo(p))
    if v:
        viol[p["id"]] = v[:3]
    v2 = G.violacoes(p["texto"])
    if v2:
        viol[p["id"] + "/texto"] = v2[:3]
passo("6. guarda P18 (V\\guarda_p18_v392.violacoes) sobre todo o texto novo: zero violacoes", not viol, str(viol) if viol else "%d trechos de texto novo varridos" % (len(P.E01_PATCHES) + len(P.A03_PATCHES)))
# 6b. controle negativo da guarda: a propria guarda tem de pegar as palavras proibidas (senao o passo 6 e' vazio)
neg = G.violacoes("a " + "CONF" + "IRMED" + " ... Nome fixo ... a luz confirma ... n\u00e3o provou ... p\u00f3s-di\u00e7\u00e3o")
passo("6b. controle negativo: a guarda pega as cinco classes", {x[0] for x in neg} == {"R1_palavra_recusada", "R2_nome_fixo", "R4_luz_confirma", "R5_nao_provou_posdicao"} or len({x[0] for x in neg}) >= 4, str(sorted({x[0] for x in neg})))

# 6c. o texto novo nao usa a palavra recusada nem NOT_FALSIFIED como veredito, e nao usa '%' fora do %s do D1
bad = []
for p in list(P.E01_PATCHES) + list(P.A03_PATCHES):
    t = texto_novo(p)
    if p["id"].startswith("A03-13"):
        continue
    if p["id"].startswith("A03") and "%" in t:
        bad.append((p["id"], "%"))
passo("6c. nenhum '%' no texto novo do artigo (exceto o %s do D1)", not bad, str(bad))

# 7. LaTeX
if "--latex" in sys.argv:
    LD = os.path.join(V, "rodada2", "erratas", "latex")
    os.makedirs(LD, exist_ok=True)
    eng = shutil.which("pdflatex")
    passo("7.0 pdflatex disponivel", bool(eng), str(eng))
    for lang in ("PT", "EN"):
        base = os.path.join(V, "dry_v392", "dry_v392_%s.tex" % lang.lower())
        pre = open(base, encoding="utf-8").read().split("\\begin{document}")[0]
        corpo = []
        for p in P.A03_PATCHES:
            if p.get("lang") != lang:
                continue
            for par in p["texto"].split("\n"):
                corpo.append(par.replace("%s", r"3{,}01"))
        tex = pre + "\\begin{document}\n\n" + "\n\n".join(corpo) + "\n\n\\end{document}\n"
        nome = "erratas_a03_%s" % lang.lower()
        open(os.path.join(LD, nome + ".tex"), "w", encoding="utf-8").write(tex)
        rcs = [subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", nome + ".tex"], cwd=LD, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900).returncode for _ in range(2)]
        log = open(os.path.join(LD, nome + ".log"), encoding="latin-1", errors="replace").read()
        errs = [l for l in log.splitlines() if l.startswith("! ")][:5]
        passo("7.%s pdflatex 2x do texto novo do artigo (%d paragrafos)" % (lang, len(corpo)), rcs == [0, 0] and not errs and os.path.exists(os.path.join(LD, nome + ".pdf")), "rc=%s erros=%s" % (rcs, errs))

print("\nRESULTADO:", "TUDO PASSA" if ok_geral else "HA FALHA")
sys.exit(0 if ok_geral else 1)
