from b_lib import *
import re
d = json.load(open(SC + r"\b09c_blocos.json", encoding="utf-8"))
rxp = re.compile(r"P\s?=\s?nP|P=nP", re.I)
need = {"relativo_leitor": r"relativo\s+ao\s+leitor|relative\s+to\s+the\s+reader", "fora": r"sem\s+o\s+leitor\s+fica\s+fora|without\s+the\s+reader\s+stays\s+outside|standard\s+Turing\s+machine\s+without", "validade": r"validade,?\s+n[ãa]o\s+credita|validity,?\s+not\s+credita"}
for lang in ("pt", "en"):
    for blk in d[lang]:
        for p in blk["new"]:
            if rxp.search(p):
                flags = {k: bool(re.search(v, p, re.I)) for k, v in need.items()}
                print(lang, len(p), flags, "|", p[:60].replace("\n", " "))
                for m in re.finditer(r"[^.;]*\bClay\b[^.;]*", p): print("     CLAY:", m.group(0)[:260])
# md: new lines
old = set(l.rstrip("\r") for l in rd(NOS + r"\um_absoluto_forma_canonica.md").split("\n"))
for l in md().split("\n"):
    l = l.rstrip("\r")
    if l not in old and rxp.search(l): print("md new line with P=nP:", l[:200])
# D84 canonical phrase in v410 DESENHO
t = open(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\DESENHO_v410.md", encoding="utf-8").read()
i = t.index("**Forma canônica obrigatória**"); print(t[i:i+900])
# where the canonical D84 phrase lives in the renders (v410 old) and whether it is intact in v411
frag = "tal qual apresentado pela TGL"
for nm, tx in (("pt", pt()), ("en", en())):
    print(nm, "ocorrencias 'tal qual apresentado/as presented by the TGL':", len(re.findall(r"tal\s+qual\s+apresentad[oa]\s+pela\s+TGL|as\s+presented\s+by\s+the\s+TGL", tx)))
