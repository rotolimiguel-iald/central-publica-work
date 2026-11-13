from b_lib import *
import re
t = open(r"C:\IALD\Central de Patentes\work\h0dn_bg1_v411_emenda_11nov\EMENDA_E_PRE_REGISTRO_V411.md", "rb").read().decode("utf-8").replace("\r\n", "\n")
for pat in [r"37\s+hospedeir", r"\b111\b", r"\b72\b", r"\b13\s+(?:calibrador|extra)", r"90\s?%", r"pseudo-?invers", r"D162", r"peso zero|zero weight|pesos congelados"]:
    ms = [m for m in re.finditer(pat, t)]
    print(pat, len(ms))
    for m in ms[:2]: print("    ", t[max(0, m.start()-100): m.end()+120].replace("\n", " "))
d = json.load(open(SC + r"\b09c_blocos.json", encoding="utf-8"))
for lang in ("en",):
    for blk in d[lang]:
        for p in blk["new"]:
            for m in re.finditer(r"caveat|accredit", p, re.I): print("EN", m.group(0), "|", p[max(0,m.start()-60):m.end()+60])
C = core()["core"]["h0dn_bg1_v411"]["values"]
print(json.dumps(C["estresse"]["i_tau_por_linha"], ensure_ascii=False)[:500])
