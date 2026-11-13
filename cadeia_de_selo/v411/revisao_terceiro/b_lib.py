import json, hashlib, re, os, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
F = r"C:\t\k411c\falso_nos_v411"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
RT = V + r"\revisao_terceiro"
SC = r"C:\t\k411c\revisao_B"
def rd(p, enc="utf-8"):
    with open(p, "rb") as f: return f.read().decode(enc)
def sha16(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
def core():
    return json.loads(rd(F + r"\um_absoluto.json"))
def pt(): return rd(F + r"\um_absoluto_pt.txt")
def en(): return rd(F + r"\um_absoluto_en.txt")
def md(): return rd(F + r"\um_absoluto_forma_canonica.md")
def man(): return rd(F + r"\um_absoluto_manifest.md")
def out(): return rd(F + r"\rodada_v411_stdout.txt")
def ctx(text, i, a=300, b=600):
    return text[max(0, i-a): i+b]
