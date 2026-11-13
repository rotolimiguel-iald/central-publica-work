import sys, os, json, re
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411")
os.chdir(r"C:\t\k411c\revisao_B")
import guarda_frases_v411 as G
F = r"C:\t\k411c\falso_nos_v411"
d = json.load(open(r"C:\t\k411c\revisao_B\b09c_blocos.json", encoding="utf-8"))
for lang in ("pt", "en"):
    n = 0
    for blk in d[lang]:
        for p in blk["new"]:
            v = G.violacoes(p)
            if v:
                n += 1; print(lang, "NOVO paragrafo com violacao:", [x[0][:40] for x in v][:3], "|", p[:70].replace("\n", " "))
    print(lang, "paragrafos novos/alterados com violacao da guarda:", n)
for nm in ("um_absoluto_pt.txt",):
    tx = open(F + "\\" + nm, "rb").read().decode("utf-8").replace("\r\n", "\n")
    c = 0
    for m in re.finditer(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", tx):
        v = G.violacoes(m.group(0))
        if v:
            c += 1
            if c <= 8: print("  (todo o texto) @%d" % m.start(), [x[0][:50] for x in v][:2], "|", m.group(0)[:70])
    print(nm, "paragrafos (texto inteiro) com violacao:", c)
