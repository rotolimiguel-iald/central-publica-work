# -*- coding: utf-8 -*-
"""04_detalhes.py -- detalha os nao-correspondentes do 03 e refaz (d) com regex frouxa (vereditos com partes minusculas)."""
import re, os, sys, json, collections
sys.stdout.reconfigure(encoding="utf-8")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
OUT = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(OUT, "03_extrai.json"), encoding="utf-8"))
SELO = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
R = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))
TXT = {l: open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8").read() for l in ("pt", "en")}
LINES = {l: TXT[l].splitlines() for l in TXT}

def ctx(lang, needle, w=90):
    for i, l in enumerate(LINES[lang], 1):
        j = l.find(needle)
        if j >= 0:
            return i, l[max(0, j - w):j + len(needle) + w].replace("\n", " ")
    return None, None

print("### (b/c) TOKENS-VEREDITO DO ARTIGO SEM CORRESPONDENTE NO SELO/CORE")
for r in D["tokens"]:
    if not (r["in_selo"] or r["in_core"]):
        i, c = ctx("pt", r["token"]) if r["pt"] else ctx("en", r["token"])
        print("- %s  (pt %d / en %d)  linha %s: ...%s..." % (r["token"], r["pt"], r["en"], i, c))
print()
print("### TOKENS SO NUMA LINGUA")
for r in D["tokens"]:
    if bool(r["pt"]) != bool(r["en"]):
        i, c = ctx("pt", r["token"]) if r["pt"] else ctx("en", r["token"])
        print("- %s  (pt %d / en %d)  linha %s: ...%s..." % (r["token"], r["pt"], r["en"], i, c))
print()
print("### HASHES DO ARTIGO DESCONHECIDOS NO SELO/CORE")
for r in D["hashes"]:
    if not r["known"]:
        i, c = ctx("pt", r["hash"]) if r["pt"] else ctx("en", r["hash"])
        print("- %s (pt %d / en %d) linha %s: ...%s..." % (r["hash"], r["pt"], r["en"], i, c))
print()
print("### HASHES SO NUMA LINGUA")
for r in D["hashes"]:
    if bool(r["pt"]) != bool(r["en"]):
        print("- %s (pt %d / en %d)" % (r["hash"], r["pt"], r["en"]))
print()
print("### NUMEROS (>=3 dig.) SEM CORRESPONDENTE NUMERICO/STRING NO SELO/CORE")
for r in D["numeros"]:
    if not (r["bate_num"] or r["bate_str"]):
        i, c = ctx("pt", r["texto"], 60) if r["pt"] else ctx("en", r["texto"], 60)
        print("- %-14s (pt %d / en %d) linha %s: ...%s..." % (r["texto"], r["pt"], r["en"], i, c))
print()
print("### NUMEROS SO NUMA LINGUA (contagem diferente PT vs EN)")
for r in D["numeros"]:
    if r["pt"] != r["en"]:
        print("- %-14s pt %d / en %d" % (r["texto"], r["pt"], r["en"]))

# ---- (d) refeito: vereditos do selo (frouxo) e sua presenca no artigo
RX = re.compile(r"^[A-Z][A-Za-z0-9]*(?:_[A-Za-z0-9]+){2,}$")
rows = []
def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + "[%d]" % i)
    elif isinstance(o, str):
        v = o.strip()
        if RX.match(v) and len(v) >= 12 and sum(ch.isupper() for ch in v) >= 0.5 * sum(ch.isalpha() for ch in v):
            rows.append({"chave": path, "veredito": v, "pt": v in TXT["pt"], "en": v in TXT["en"],
                         "pt_l": ctx("pt", v)[0], "en_l": ctx("en", v)[0]})
walk(SELO, "selo")
print()
print("### (d) VEREDITOS-STRING DO SELO (regex frouxa): %d ; no PT: %d ; no EN: %d ; ausentes nos dois: %d" % (
    len(rows), sum(r["pt"] for r in rows), sum(r["en"] for r in rows), sum(1 for r in rows if not r["pt"] and not r["en"])))
for r in rows:
    if not (r["pt"] and r["en"]):
        print("- %-60s pt=%s en=%s  %s" % (r["chave"], r["pt_l"], r["en_l"], r["veredito"][:150]))
json.dump(rows, open(os.path.join(OUT, "04_selo_vereditos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- os 41 vereditos de chave do selo (as chaves *_verdict e strings de topo)
print()
print("### VEREDITOS DE TOPO DO SELO (chave -> presente PT / EN, por prefixo de 40 chars tambem)")
for k, v in SELO.items():
    if isinstance(v, str) and ("_" in v) and v.isupper() is False and RX.match(v) or (isinstance(v, str) and RX.match(v)):
        p40 = v[:40]
        print("%-48s PT=%s EN=%s | prefixo40 PT=%s EN=%s" % (k, v in TXT["pt"], v in TXT["en"], p40 in TXT["pt"], p40 in TXT["en"]))
    elif isinstance(v, dict) and "verdict" in v and isinstance(v["verdict"], str):
        vv = v["verdict"]
        print("%-48s PT=%s EN=%s | prefixo40 PT=%s EN=%s  [dict.verdict]" % (k, vv in TXT["pt"], vv in TXT["en"], vv[:40] in TXT["pt"], vv[:40] in TXT["en"]))
