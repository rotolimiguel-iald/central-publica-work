# -*- coding: utf-8 -*-
"""09_refina.py -- (i) os 42 numeros 'sem correspondente': busca refinada (texto bruto do core, formas LaTeX na fonte) + contexto;
(ii) bandeiras do gate no core (contagem True/False); (iii) paragrafos v374/v375 e a secao de Coma PT/EN na integra;
(iv) contextos: neutrino 2,95, eco 0,69/spin, 'nulos' nao rodados, P_ker K <-> P_F, QGSolutionComplete, evidencia primaria;
(v) contagem ampla de 'confirm*' por token nos dois TXT."""
import re, os, sys, json, collections
sys.stdout.reconfigure(encoding="utf-8")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
OUT = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(OUT, "03_extrai.json"), encoding="utf-8"))
CORE_RAW = open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8").read()
SELO_RAW = open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8").read()
R = json.loads(CORE_RAW); c = R["core"]
SRC = open(os.path.join(NOS, "um.py"), encoding="utf-8", errors="replace").read()
TXT = {l: open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8").read().splitlines() for l in ("pt", "en")}
TEX = {l: open(os.path.join(NOS, "um_absoluto_%s.tex" % l), encoding="utf-8").read().splitlines() for l in ("pt", "en")}
SEM = ["1,9×10^9", "2,74×10^16", "2.9×10^-4", "4,7×10^-2", "4,8×10^12", "6,6×10^-3", "-1.08×10^-2", "1,1×10^-3", "1137,036", "131.191", "143.20", "15,10",
       "164.037", "174.431.422", "2,2×10^-4", "2,3×10^-4", "2,9×10^-4", "2.0×10^16", "2.7×10^16", "2.9×10^-5", "3,6×10^-5", "310.396", "4,0×10^6",
       "4,9×10^2", "5,2×10^-5", "5.458.992", "5.89×10^-2", "6655.4", "9,8×10^-3"]
def forms(s):
    t = s.replace(",", ".")
    m = re.match(r"^([-+]?\d+(?:\.\d+)?)×10\^([-+]?\d+)$", t)
    out = {s, t, s.replace(".", ",")}
    if m:
        man, ex = m.group(1), int(m.group(2))
        for mm in (man, man.replace(".", ","), man.replace(".", "{,}"), man.replace(".", "{.}")):
            for ee in ("%d" % ex, "{%d}" % ex, "{%+d}" % ex):
                out.add("%s\\times10^%s" % (mm, ee)); out.add("%s\\times 10^%s" % (mm, ee)); out.add("%s \\times 10^%s" % (mm, ee))
                out.add("%s×10^%s" % (mm, ee)); out.add("%se%d" % (mm, ex)); out.add("%se%02d" % (mm, ex)); out.add("%se%+03d" % (mm, ex)); out.add("%sE%+03d" % (mm, ex))
        try:
            v = float(man) * 10 ** ex
            out.add(repr(v)); out.add("%g" % v); out.add("%.3g" % v); out.add("%.2e" % v); out.add("%.1e" % v)
        except Exception:
            pass
    else:
        out.add(t.replace(".", "")); out.add(t.replace(".", "{,}"))
    return out
def ctx(lang, needle, w=70):
    for i, l in enumerate(TXT[lang], 1):
        j = l.find(needle)
        if j >= 0:
            return "L%d ...%s..." % (i, l[max(0, j - w):j + len(needle) + w])
    return None
print("### (i) 42 NUMEROS 'SEM CORRESPONDENTE' -- busca refinada")
for s in SEM:
    fs = forms(s)
    in_core = [f for f in fs if f in CORE_RAW or f in SELO_RAW]
    in_src = [f for f in fs if f in SRC]
    print("- %-13s core/selo:%s  fonte:%s\n      %s" % (s, in_core[:3] or "NAO", in_src[:3] or "NAO", ctx("pt", s) or ctx("en", s)))

print("\n### (ii) BANDEIRAS DO GATE no core")
def bools(d, pref=""):
    out = {}
    for k, v in d.items():
        if isinstance(v, bool): out[pref + k] = v
    return out
for key in ("qg_closure", "kernel_formalization"):
    d = c.get(key, {})
    b = bools(d)
    print("%s: %d bool de topo (True %d / False %d)" % (key, len(b), sum(b.values()), len(b) - sum(b.values())))
    if key == "qg_closure":
        for kk, vv in d.items():
            if isinstance(vv, dict):
                bb = bools(vv)
                if bb: print("   %s.%s: %d bool (True %d): %s" % (key, kk, len(bb), sum(bb.values()), {a: b_ for a, b_ in bb.items()}))
    if key == "kernel_formalization":
        print("   chaves de topo:", [k for k in d.keys()][:80])
        for kk in ("theorems_total", "theorems_clean", "clean_theorems", "n_flags", "flags_true", "n_theorem_flags", "ladder_flags"):
            if kk in d: print("   ", kk, "=", str(d[kk])[:200])
# procurar 5849 no core
hits = [m.start() for m in re.finditer(r"5849", CORE_RAW)][:5]
for h in hits:
    print("   5849 no core (contexto):", CORE_RAW[max(0, h - 160):h + 40].replace("\n", " "))
print("   5849 no selo:", "5849" in SELO_RAW)
kf = c.get("kernel_formalization", {})
flags = {k: v for k, v in kf.items() if isinstance(v, bool)}
print("   kernel_formalization bools: total %d, True %d" % (len(flags), sum(flags.values())))
ext = {k: v for k, v in flags.items() if k.startswith(("ext_", "gpc_"))}
print("   ext_/gpc_: %d (True %d)" % (len(ext), sum(ext.values())))

print("\n### (iii) PARAGRAFOS v375 / v374 / v369 (tex, PT e EN) e a secao de Coma [38]")
for lang, lines in (("pt", (681, 683, 591)), ("en", (679, 681, 589))):
    for ln in lines:
        print("\n[%s tex L%d]\n%s" % (lang, ln, TEX[lang][ln - 1][:6000]))
S = json.load(open(os.path.join(OUT, "02_secoes.json"), encoding="utf-8"))
for lang in ("pt", "en"):
    i = 38
    a = S[lang][i][0]; b = S[lang][i + 1][0] - 1
    print("\n[%s secao 38, tex L%d-%d]\n%s" % (lang, a, b, "\n".join(TEX[lang][a - 1:b])[:7000]))

print("\n### (iv) CONTEXTOS")
for pat in [r"2[.,]95", r"NuFIT", r"0[.,]69\b", r"spin", r"nulos? (pré-registrad|pre-registered|de família|not run|não rodad)", r"P_\{?\\?ker", r"ker K", r"QGSolutionComplete", r"CONVERGENCE_RECLASSIFIED", r"evidência primária|primary evidence", r"as quatro bandeiras|four flags|quatro flags", r"revelad|revealed|reveal\b"]:
    print("-- padrao", pat)
    for lang in ("pt", "en"):
        n = 0
        for i, l in enumerate(TXT[lang], 1):
            for m in re.finditer(pat, l, re.I):
                a_, b_ = max(0, m.start() - 110), min(len(l), m.end() + 110)
                print("   %s L%-5d ...%s..." % (lang, i, l[a_:b_])); n += 1
                if n >= 6: break
            if n >= 6: break

print("\n### (v) 'confirm*' por token")
for lang in ("pt", "en"):
    cnt = collections.Counter(m.group(0).lower() for l in TXT[lang] for m in re.finditer(r"\b(confirm\w*)\b", l, re.I))
    print(lang, dict(cnt))
