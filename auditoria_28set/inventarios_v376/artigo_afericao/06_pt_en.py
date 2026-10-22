# -*- coding: utf-8 -*-
"""06_pt_en.py -- item 3: PT <-> EN por secao alinhada (223 x 223 pelo indice): numeros normalizados (separador decimal)
e tokens-veredito por secao; lista as divergencias. Mais: contextos de numeros com contagem diferente."""
import re, os, sys, json, collections
sys.stdout.reconfigure(encoding="utf-8")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
OUT = os.path.dirname(os.path.abspath(__file__))
TEX = {l: open(os.path.join(NOS, "um_absoluto_%s.tex" % l), encoding="utf-8").read().splitlines() for l in ("pt", "en")}
TXT = {l: open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8").read().splitlines() for l in ("pt", "en")}
S = json.load(open(os.path.join(OUT, "02_secoes.json"), encoding="utf-8"))
rx_sec = re.compile(r"^\s*\\(part|chapter|section|subsection|subsubsection)\*?\s*(?:\[[^\]]*\])?\{(.*)$")

def blocos(lang):
    secs = S[lang]
    out = []
    for i, (ln, kind, title) in enumerate(secs):
        end = secs[i + 1][0] - 1 if i + 1 < len(secs) else len(TEX[lang])
        body = "\n".join(TEX[lang][ln - 1:end])
        out.append((ln, kind, title, body))
    return out

def norm_nums(s):
    # PT: 0{,}85 -> 0.85 ; 1,5 -> 1.5 (entre digitos) ; milhar 1.234.567 -> 1234567 ; EN: 1,234,567 -> 1234567
    t = s.replace("{,}", ".").replace("{.}", ".")
    t = re.sub(r"(?<=\d)\.(?=\d{3}(?:\D|$))(?!\d{3}\d)", "", t) if False else t
    # milhares com 3 grupos ou mais (evita tocar decimais): 1.234.567 / 1,234,567
    t = re.sub(r"(?<!\d)(\d{1,3})[.,](\d{3})[.,](\d{3})(?!\d)", r"\1\2\3", t)
    # separador decimal virgula entre digitos -> ponto
    t = re.sub(r"(?<=\d),(?=\d)", ".", t)
    nums = re.findall(r"(?<![A-Za-z0-9_])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?(?![A-Za-z0-9_])", t)
    # so >= 3 digitos significativos
    def sig(x):
        d = re.sub(r"[eE].*$", "", x); d = re.sub(r"[^0-9]", "", d).lstrip("0"); return len(d)
    return collections.Counter(x for x in nums if sig(x) >= 3)

RX_VER = re.compile(r"(?<![A-Za-z0-9_])(?:TGL_[A-Z0-9_]+|[A-Z][A-Z0-9]*(?:_+[A-Z0-9]+){2,})(?![A-Za-z0-9_])")
BP, BE = blocos("pt"), blocos("en")
print("secoes PT %d, EN %d" % (len(BP), len(BE)))
div_num, div_tok = [], []
for i, ((lp, kp, tp, bp), (le, ke, te, be)) in enumerate(zip(BP, BE)):
    if kp != ke:
        print("!! tipo de secao difere no indice %d: PT %s (%s) vs EN %s (%s)" % (i, kp, tp[:60], ke, te[:60]))
    np_, ne = norm_nums(bp), norm_nums(be)
    if np_ != ne:
        so_pt = {k: v - ne.get(k, 0) for k, v in np_.items() if v > ne.get(k, 0)}
        so_en = {k: v - np_.get(k, 0) for k, v in ne.items() if v > np_.get(k, 0)}
        div_num.append({"i": i, "pt_linha": lp, "en_linha": le, "pt_titulo": tp[:90], "en_titulo": te[:90], "so_pt": so_pt, "so_en": so_en})
    tkp, tke = collections.Counter(RX_VER.findall(bp)), collections.Counter(RX_VER.findall(be))
    if tkp != tke:
        so_pt = {k: v - tke.get(k, 0) for k, v in tkp.items() if v > tke.get(k, 0)}
        so_en = {k: v - tkp.get(k, 0) for k, v in tke.items() if v > tkp.get(k, 0)}
        div_tok.append({"i": i, "pt_linha": lp, "en_linha": le, "pt_titulo": tp[:90], "en_titulo": te[:90], "so_pt": so_pt, "so_en": so_en})
print("\n### SECOES COM NUMEROS DIVERGENTES (normalizados): %d de %d" % (len(div_num), len(BP)))
for d in div_num:
    print("- [%d] PT L%d / EN L%d  %s\n     so PT: %s\n     so EN: %s" % (d["i"], d["pt_linha"], d["en_linha"], d["pt_titulo"], d["so_pt"], d["so_en"]))
print("\n### SECOES COM TOKENS-VEREDITO DIVERGENTES: %d de %d" % (len(div_tok), len(BP)))
for d in div_tok:
    print("- [%d] PT L%d / EN L%d  %s\n     so PT: %s\n     so EN: %s" % (d["i"], d["pt_linha"], d["en_linha"], d["pt_titulo"], d["so_pt"], d["so_en"]))
json.dump({"div_num": div_num, "div_tok": div_tok}, open(os.path.join(OUT, "06_pt_en.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print("\n### CONTEXTOS (TXT) de numeros/palavras a conferir")
def ctx(lang, pat, w=80, maxn=12):
    n = 0
    for i, l in enumerate(TXT[lang], 1):
        for m in re.finditer(pat, l):
            a, b = max(0, m.start() - w), min(len(l), m.end() + w)
            print("   %s L%-5d ...%s..." % (lang, i, l[a:b])); n += 1
            if n >= maxn: return
for pat in [r"(?<![0-9.])0[.,]300(?![0-9])", r"(?<![0-9.,])144(?![0-9.,])", r"(?<![0-9.,])1933(?![0-9])", r"(?<![0-9.,])1439(?![0-9])", r"1[.,]419", r"5849", r"unilateral|one-sided", r"ALPHA_FREE_CANDIDATE|NOT_A_CANDIDATE", r"UNDECIDED_IN_KERNEL|GA_MASS_FORM_RETIRED"]:
    print("-- padrao", pat)
    ctx("pt", pat); ctx("en", pat)
print("-- PT L1104 e L1115 (contrapartes de EN L1103/L1114 'confirmed'):")
for ln in (1104, 1115):
    l = TXT["pt"][ln - 1]
    j = max(l.find("régua"), l.find("conferiu"), l.find("confirm"))
    print("   PT L%d: ...%s..." % (ln, l[max(0, j - 150):j + 200] if j >= 0 else l[:300]))
