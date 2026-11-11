import glob, hashlib, json, os, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
from cu_corpus import *
WK = "C:/IALD/Central de Patentes/work/"
falas = {}
for pat in (WK + "cunhagens_13out/*.txt", R + "insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v409/insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v408/insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v407/insumos/cunhagens/*.txt"):
    for p in sorted(glob.glob(pat)):
        falas[p] = open(p, "rb").read().decode("utf-8", "replace")
norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2019", "'").replace("`", "").replace("\%", "%").replace("\_", "_")).strip()
noacc = lambda s: "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()
corp = " || ".join(norm(v) for v in falas.values()); corp_na = noacc(corp)
def classe(q):
    qn = norm(q); alvo = qn.strip(" .,;:\u201c\u201d\"")
    segs = [x.strip(" .,;:\u201c\u201d\"") for x in re.split(r"…|\[\.\.\.\]|\.\.\.", alvo) if len(x.strip(" .,;:\u201c\u201d\"")) >= 4]
    if qn in corp or alvo in corp: return "exata"
    if segs and all(s in corp for s in segs): return "exata_com_elisao"
    if segs and all(noacc(s) in corp_na for s in segs): return "sem_acentos"
    return "NAO"
def segs(t): return [s.strip() for s in re.split(r"(?<=[.;:])\s+", ws(t)) if s.strip()]
q_rx = re.compile(r"«([^»]+)»")
tot = {}; ruins = []
for k in ("pt", "en", "md"):
    velho = set(segs(rd("cu_saidas/novo_%s.R3.txt" % k)))
    novos = [s for s in segs(rd("novo_%s.txt" % k)) if s not in velho]
    # quotes que cruzam segmentos: usar o texto inteiro dos novos
    txt = " ".join(novos)
    qs = [m.group(1) for m in q_rx.finditer(txt)]
    tot[k] = {}
    for q in qs:
        c = classe(q); tot[k][c] = tot[k].get(c, 0) + 1
        if c == "NAO" and len(q) >= 8: ruins.append((k, q[:200]))
print("citacoes « » nos trechos novos desde a R3:", tot)
for r in ruins: print("   NAO:", r)
# custodia e README
for nome, t in (("custodia", C_ := carregar()["custodia_ws"]), ("readme", ws(open("cu_saidas/readme_render.json", encoding="utf-8").read()))):
    qs = [m.group(1) for m in q_rx.finditer(t)]
    cl = {}
    for q in qs:
        c = classe(q); cl[c] = cl.get(c, 0) + 1
        if c == "NAO": print("   NAO (%s): %s" % (nome, q[:200]))
    print(nome, cl)
