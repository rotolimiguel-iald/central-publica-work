# -*- coding: utf-8 -*-
"""07_refaz.py -- (d) refeito com regex que aceita '__' e '-'; numeros nao-batidos refeitos com tolerancia por digitos e
fontes secundarias (manifesto, stdout da rodada, fonte do um.py); os 9 hashes e os 18 tokens conferidos no manifesto,
no CHAIN_OF_CUSTODY.json do cache e na fonte do um.py."""
import re, os, sys, json, math, collections
sys.stdout.reconfigure(encoding="utf-8")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
CACHE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache"
OUT = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(OUT, "03_extrai.json"), encoding="utf-8"))
SELO = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
R = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))
TXT = {l: open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8").read() for l in ("pt", "en")}
MAN = open(os.path.join(NOS, "um_absoluto_manifest.md"), encoding="utf-8", errors="replace").read()
STD = open(os.path.join(NOS, "rodada_v375_stdout.txt"), encoding="utf-8", errors="replace").read()
SRC = open(os.path.join(NOS, "um.py"), encoding="utf-8", errors="replace").read()
coc_p = os.path.join(CACHE, "CHAIN_OF_CUSTODY.json")
COC = open(coc_p, encoding="utf-8", errors="replace").read() if os.path.exists(coc_p) else ""
print("fontes: manifesto %d bytes, stdout %d, um.py %d, CHAIN_OF_CUSTODY %d (%s)" % (len(MAN), len(STD), len(SRC), len(COC), coc_p if COC else "AUSENTE"))

def lineno_of(text, needle):
    for i, l in enumerate(text.splitlines(), 1):
        if needle in l:
            return i
    return None

# ---- (d) refeito
RX = re.compile(r"^[A-Z][A-Za-z0-9\-]*(?:_+[A-Za-z0-9\-]+){2,}$")
rows = []
def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, path + "[%d]" % i)
    elif isinstance(o, str):
        v = o.strip()
        if RX.match(v) and len(v) >= 12 and sum(ch.isupper() for ch in v) >= 0.5 * max(1, sum(ch.isalpha() for ch in v)):
            rows.append({"chave": path, "veredito": v, "pt": v in TXT["pt"], "en": v in TXT["en"],
                         "pt40": v[:40] in TXT["pt"], "en40": v[:40] in TXT["en"],
                         "pt_l": lineno_of(TXT["pt"], v), "en_l": lineno_of(TXT["en"], v)})
walk(SELO, "selo")
print("\n### (d) VEREDITOS-STRING DO SELO: %d ; integrais no PT: %d ; no EN: %d ; ausentes (integral) nos dois: %d ; ausentes ate por prefixo40 nos dois: %d" % (
    len(rows), sum(r["pt"] for r in rows), sum(r["en"] for r in rows), sum(1 for r in rows if not r["pt"] and not r["en"]),
    sum(1 for r in rows if not r["pt40"] and not r["en40"])))
print("-- ausentes nos dois (integral):")
for r in rows:
    if not r["pt"] and not r["en"]:
        print("   %-58s pref40 PT=%s EN=%s | %s" % (r["chave"], r["pt40"], r["en40"], r["veredito"][:130]))
print("-- presentes so numa lingua (integral):")
for r in rows:
    if r["pt"] != r["en"]:
        print("   %-58s PT=%s(L%s) EN=%s(L%s) | %s" % (r["chave"], r["pt"], r["pt_l"], r["en"], r["en_l"], r["veredito"][:110]))
json.dump(rows, open(os.path.join(OUT, "07_selo_vereditos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- numeros nao-batidos: tolerancia por digitos + fontes secundarias
def flat_nums(o, acc):
    if isinstance(o, dict):
        for v in o.values(): flat_nums(v, acc)
    elif isinstance(o, list):
        for v in o: flat_nums(v, acc)
    elif isinstance(o, bool): pass
    elif isinstance(o, (int, float)):
        if not (isinstance(o, float) and (math.isnan(o) or math.isinf(o))): acc.append(float(o))
NUMS = []; flat_nums(R, NUMS); flat_nums(SELO, NUMS)
NUMS = sorted(set(NUMS))
def sig(s):
    d = re.sub(r"[eE].*$", "", s); d = re.sub(r"[^0-9]", "", d).lstrip("0"); return len(d)
def close_d(a, b, nd):
    if a == b: return True
    if b == 0: return abs(a) < 10 ** (-nd)
    return abs(a - b) / max(abs(a), abs(b)) <= 0.6 * 10 ** (-(nd - 1))
print("\n### NUMEROS NAO-BATIDOS (88): reclassificacao")
cls = collections.Counter()
for r in D["numeros"]:
    if r["bate_num"] or r["bate_str"]: continue
    s = r["texto"]; nd = sig(s); vals = r["vals"]
    num_ok = any(close_d(v, c, nd) for v in vals for c in NUMS) if vals else False
    alt = [s, s.replace(",", "."), s.replace(".", ","), s.replace("×10^", "e"), s.replace("×10^", "e+"), s.replace("×10^-", "e-")]
    in_man = any(a in MAN for a in alt); in_std = any(a in STD for a in alt); in_src = any(a in SRC for a in alt)
    if num_ok: c = "bate no core/selo com tolerancia por digitos"
    elif in_man: c = "esta no MANIFESTO (saida da rodada)"
    elif in_std: c = "esta no STDOUT da rodada"
    elif in_src: c = "LITERAL na fonte do um.py (prosa/literatura), nao calculado"
    else: c = "SEM CORRESPONDENTE em core/selo/manifesto/stdout/fonte"
    cls[c] += 1
    print("- %-14s (pt %d / en %d) -> %s" % (s, r["pt"], r["en"], c))
print("resumo:", dict(cls))

# ---- os 9 hashes
print("\n### HASHES DESCONHECIDOS (9): no manifesto / CHAIN_OF_CUSTODY / fonte um.py")
for r in D["hashes"]:
    if not r["known"]:
        h = r["hash"]
        print("- %s manifesto=%s chain=%s fonte=%s" % (h, h in MAN, h in COC, h in SRC))

# ---- os 18 tokens
print("\n### TOKENS SEM PAR NO SELO/CORE (18): na fonte do um.py? no stdout? no manifesto?")
for r in D["tokens"]:
    if not (r["in_selo"] or r["in_core"]):
        t = r["token"]
        print("- %-64s fonte=%s stdout=%s manifesto=%s" % (t, t in SRC, t in STD, t in MAN))
