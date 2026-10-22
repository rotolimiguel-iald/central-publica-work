# -*- coding: utf-8 -*-
"""10_fecho.py -- (a) vereditos INTEIROS do artigo (com '__' e partes minusculas) conferidos no core/selo; (b) vereditos do core
(chave 'verdict' de cada dict) presentes inteiros no PT/EN; (c) tolerancia correta (mantissa) p/ os numeros x10^ restantes;
(d) os 18 tokens na fonte em forma LaTeX-escapada; (e) alinhamento PT/EN ao nivel de \\paragraph; (f) contextos finais."""
import re, os, sys, json, math, collections
sys.stdout.reconfigure(encoding="utf-8")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
OUT = os.path.dirname(os.path.abspath(__file__))
CORE_RAW = open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8").read()
SELO_RAW = open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8").read()
R = json.loads(CORE_RAW); c = R["core"]; SELO = json.loads(SELO_RAW)
SRC = open(os.path.join(NOS, "um.py"), encoding="utf-8", errors="replace").read()
STD = open(os.path.join(NOS, "rodada_v375_stdout.txt"), encoding="utf-8", errors="replace").read()
TXT = {l: open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8").read() for l in ("pt", "en")}
TXL = {l: TXT[l].splitlines() for l in TXT}
TEX = {l: open(os.path.join(NOS, "um_absoluto_%s.tex" % l), encoding="utf-8").read().splitlines() for l in ("pt", "en")}
BIG = CORE_RAW + "\n" + SELO_RAW
def ln(lang, needle):
    for i, l in enumerate(TXL[lang], 1):
        if needle in l: return i
    return None

# (a) vereditos inteiros no artigo
RX = re.compile(r"(?<![A-Za-z0-9_])[A-Z][A-Z0-9]*(?:_+[A-Za-z0-9]+){2,}(?![A-Za-z0-9_])")
runs = {l: collections.Counter(m for m in RX.findall(TXT[l]) if "__" in m and len(m) >= 24) for l in TXT}
allr = set(runs["pt"]) | set(runs["en"])
miss = []
for r in sorted(allr):
    # a tabela do artigo escapa '_' como '\_'? no TXT nao. Confere inteiro no core/selo.
    if r not in BIG:
        # tenta sem sufixo apos ultimo '__' (truncamento de tabela)
        miss.append(r)
print("### (a) vereditos INTEIROS (com '__', >=24 chars) no artigo: %d distintos; ausentes inteiros no core/selo: %d" % (len(allr), len(miss)))
for r in miss:
    lang = "pt" if runs["pt"].get(r) else "en"
    i = ln(lang, r)
    # o maior prefixo presente no core/selo
    parts = r.split("__"); pref = None
    for k in range(len(parts) - 1, 0, -1):
        p = "__".join(parts[:k])
        if p in BIG: pref = p; break
    print("- %s L%s (pt %d / en %d)\n     %s\n     maior prefixo no core/selo: %s" % (lang, i, runs["pt"].get(r, 0), runs["en"].get(r, 0), r[:230], (pref or "NENHUM")[:120]))

# (b) vereditos do core no artigo
rows = []
for k, v in c.items():
    if isinstance(v, dict):
        vv = v.get("verdict") or v.get("status") or v.get("selo")
        if isinstance(vv, str) and len(vv) >= 12 and "_" in vv:
            rows.append({"chave": k, "veredito": vv, "pt": vv in TXT["pt"], "en": vv in TXT["en"], "pt40": vv[:40] in TXT["pt"], "en40": vv[:40] in TXT["en"]})
print("\n### (b) vereditos do CORE (verdict|status|selo por dict): %d ; inteiros no PT: %d ; no EN: %d ; ausentes nos dois (inteiro): %d ; ausentes ate por prefixo40: %d" % (
    len(rows), sum(r["pt"] for r in rows), sum(r["en"] for r in rows), sum(1 for r in rows if not r["pt"] and not r["en"]), sum(1 for r in rows if not r["pt40"] and not r["en40"])))
print("-- ausentes ate por prefixo40 (chave: veredito[:110]):")
for r in rows:
    if not r["pt40"] and not r["en40"]:
        print("   %-40s %s" % (r["chave"], r["veredito"][:110]))
print("-- presentes por prefixo40 mas nao inteiros (truncados/alterados no artigo?):")
for r in rows:
    if (r["pt40"] or r["en40"]) and not (r["pt"] and r["en"]):
        i = ln("pt", r["veredito"][:40]); l = TXL["pt"][i - 1] if i else ""
        j = l.find(r["veredito"][:40])
        print("   %-40s PT L%s: ...%s..." % (r["chave"], i, l[max(0, j - 20):j + 150]))
print("-- presentes so numa lingua (inteiro):")
for r in rows:
    if r["pt"] != r["en"]:
        print("   %-40s PT=%s EN=%s %s" % (r["chave"], r["pt"], r["en"], r["veredito"][:100]))

# (c) numeros x10^ restantes, tolerancia pela mantissa
def flat_nums(o, acc):
    if isinstance(o, dict):
        for v in o.values(): flat_nums(v, acc)
    elif isinstance(o, list):
        for v in o: flat_nums(v, acc)
    elif isinstance(o, bool): pass
    elif isinstance(o, (int, float)):
        if not (isinstance(o, float) and (math.isnan(o) or math.isinf(o))): acc.append(float(o))
NUMS = []; flat_nums(R, NUMS); flat_nums(SELO, NUMS); NUMS = sorted(set(NUMS))
REST = ["1,9×10^9", "4,8×10^12", "-1.08×10^-2", "2.7×10^16", "2.9×10^-5", "4,0×10^6", "5,2×10^-5", "5.89×10^-2", "6655.4", "143.20", "-950", "1.33×10^-5", "1.3×10^-1", "2×10^4", "2×10^5", "2,74×10^16", "2.0×10^16", "4,9×10^2"]
print("\n### (c) numeros restantes: tolerancia pela MANTISSA")
for s in REST:
    t = s.replace(",", ".")
    m = re.match(r"^([-+]?\d+(?:\.\d+)?)(?:×10\^([-+]?\d+))?$", t)
    man, ex = m.group(1), int(m.group(2) or 0)
    v = float(man) * 10 ** ex; nd = len(re.sub(r"[^0-9]", "", man).lstrip("0")) or 1
    tol = 0.6 * 10 ** (-(nd - 1))
    hits = [x for x in NUMS if x != 0 and abs(x - v) / max(abs(x), abs(v)) <= tol]
    print("- %-12s v=%g nd=%d tol=%.1e -> core/selo: %s" % (s, v, nd, tol, (["%g" % h for h in hits[:4]] or "NAO")))

# (d) os 18 tokens em forma escapada na fonte
print("\n### (d) tokens sem par: na fonte do um.py em forma LaTeX-escapada (\\_)?")
for t in ["ALPHA_FREE_CANDIDATE", "ALPHA_VALUE_QED_CHALLENGE", "C3_REGISTER_SELF_INSCRIPTION_THEOREM_STRUCTURAL_CLOSED", "E_01E_10", "FORMALLY_CLOSED_NATURE_TEST",
          "HOLOGRAPHIC_DEAD_SIGNAL_RECONSTRUCTION_THEOREM_STRUCTURAL_CLOSED", "IDEMPOTENT_RECONSTRUCTION_FORM_FORMULATED", "LET_THERE_BE_LIGHT", "NOT_A_CANDIDATE", "MIRROR_FUNCTION_D_OPEN"]:
    esc = t.replace("_", "\\_"); esc2 = t.replace("_", "\\\\_")
    n1, n2 = SRC.count(esc), SRC.count(esc2)
    print("- %-64s '%s' x%d ; '%s' x%d" % (t, "\\_", n1, "\\\\_", n2))
i = SRC.find("ALPHA\\_FREE\\_CANDIDATE")
if i < 0: i = SRC.find("ALPHA\\\\_FREE\\\\_CANDIDATE")
if i >= 0:
    print("   contexto na fonte (linha %d): ...%s..." % (SRC.count("\n", 0, i) + 1, SRC[max(0, i - 200):i + 120].replace("\n", " ")))

# (e) alinhamento ao nivel de \paragraph
S = json.load(open(os.path.join(OUT, "02_secoes.json"), encoding="utf-8"))
rxp = re.compile(r"\\paragraph\*?\{([^}]*)")
print("\n### (e) \\paragraph por secao alinhada (PT vs EN): divergencias de contagem")
nd_ = 0
for i in range(len(S["pt"])):
    a, b = S["pt"][i][0], (S["pt"][i + 1][0] - 1 if i + 1 < len(S["pt"]) else len(TEX["pt"]))
    a2, b2 = S["en"][i][0], (S["en"][i + 1][0] - 1 if i + 1 < len(S["en"]) else len(TEX["en"]))
    pp = rxp.findall("\n".join(TEX["pt"][a - 1:b])); pe = rxp.findall("\n".join(TEX["en"][a2 - 1:b2]))
    if len(pp) != len(pe):
        nd_ += 1
        print("- [%d] PT L%d (%d par.) / EN L%d (%d par.)  %s\n     PT: %s\n     EN: %s" % (i, a, len(pp), a2, len(pe), S["pt"][i][2][:70], [p[:60] for p in pp], [p[:60] for p in pe]))
print("secoes com contagem de \\paragraph diferente:", nd_)

# (f) contextos finais
print("\n### (f) contextos")
def ctx(lang, pat, w=120, maxn=8):
    n = 0
    for i, l in enumerate(TXL[lang], 1):
        for m in re.finditer(pat, l):
            a_, b_ = max(0, m.start() - w), min(len(l), m.end() + w)
            print("   %s L%-5d ...%s..." % (lang, i, l[a_:b_])); n += 1
            if n >= maxn: return
for pat in [r"\bconfirmo\b", r"\bconfirma\b", r"\bconfirms\b", r"THE_GEOMETRIC_COST_OF_ABSOLUTE_ZERO", r"True nesta rodada: 18|True in this run: 18", r"TheMarkIsNotATypeMark"]:
    print("-- padrao", pat); ctx("pt", pat); ctx("en", pat)
print("-- PT L19 (evidencia primaria, janela larga):")
l = TXL["pt"][18]; j = l.find("evidência primária"); print("   ", l[max(0, j - 100):j + 700])
print("-- PT tex L593-600 (secao 'A evidencia primaria'):")
print("\n".join(TEX["pt"][592:600])[:3000])
print("-- EN tex L591-598:")
print("\n".join(TEX["en"][590:598])[:3000])
