import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
sys.dont_write_bytecode = True
sys.path.insert(0, V)
import delta_v411 as DL
H = r"C:\t\k411c\ensaio_topo_proposto\pos_rito_textos\positivo\nos\HANDOFF_v411_CUSTODIA.md"
h = rd(H)
print("handoff (S6d real sobre Nos sintetico, positivo):", len(h.encode("utf-8")), "B sha16", sha16(H))
# blocos = paragrafos separados por linha em branco
blocos = [b for b in re.split(r"\n\s*\n", h) if b.strip()]
print("blocos:", len(blocos))
pt = {"modelo": DL.OBRIG_MODELO_PT, "cef": DL.OBRIG_CEFEIDAS_PT, "val": DL.OBRIG_VALIDADE_PT, "retro": DL.OBRIG_RETRO_PT, "nc": DL.OBRIG_NAO_CEGO_PT}
en = {"modelo": DL.OBRIG_MODELO_EN, "cef": DL.OBRIG_CEFEIDAS_EN, "val": DL.OBRIG_VALIDADE_EN, "retro": DL.OBRIG_RETRO_EN, "nc": DL.OBRIG_NAO_CEGO_EN}
# gatilhos: o Z do primario contra o nulo (6,11 / 6.11), a cabeca do teste, 'provado na natureza' / 'proved in nature' / 'read in nature above 5'
zs = ["6,11", "6.11"]
cab = "BETA_TGL_PROVED_IN_NATURE_AT_"
gat = re.compile(r"6[,.]11|provad[oa]s? na natureza|proved in nature|BETA_TGL_PROVED_IN_NATURE_AT_|lido na natureza acima de 5|read in nature above 5", re.I)
falhas = []; n = 0
for i, b in enumerate(blocos):
    if gat.search(b):
        n += 1
        lang = "pt" if re.search(r"[ãõçé]", b) and not re.search(r"\b(the|under|which)\b", b) else "en"
        ob = pt if lang == "pt" else en
        faltam = [k for k, v in ob.items() if v.lower() not in b.lower()]
        # aceita a forma do outro idioma no mesmo bloco (blocos mistos)
        faltam2 = [k for k in faltam if en[k].lower() not in b.lower() and pt[k].lower() not in b.lower()]
        if faltam2:
            falhas.append((i, faltam2, b[:120].replace("\n", " ")))
print("blocos com gatilho:", n, "| com obrigatorio faltando:", len(falhas))
for f in falhas[:12]:
    print("   bloco", f[0], "falta", f[1], "|", f[2])
# secao do ESTADO / sete ressalvas / cinco do que nao decide
print("menciona sete ressalvas:", bool(re.search(r"sete ressalvas|seven reservations", h)), "| 'nao decide':", bool(re.search(r"n[aã]o decide|does not decide", h)))
ress = re.findall(r"^\s*\d\.\s", h, re.M)
print("itens numerados no handoff:", len(ress))
# D59 e D65
print("D59 (milenio/millennium/navier/lindao):", bool(re.search(r"(?i)mil[eê]nio|millennium|navier|lindão", h)), "| kimi sem h0dn:", bool(re.search(r"(?i)kimi", h)) and not re.search(r"(?i)h0dn", h))
print("D65 fora:", [x for x in DL.FORA_D65 if x.lower() in h.lower()])
print("vocativo/nomes D59 em prosa (busca por listas do delta):", [k for k in dir(DL) if "VEDAD" in k.upper() or "D59" in k.upper()][:10])
