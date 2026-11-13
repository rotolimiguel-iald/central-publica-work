from b_lib import *
import re
texts = {"pt": pt(), "en": en(), "md": md(), "man": man(), "out": out()}
# occurrence patterns (mine)
OCC = re.compile(r"6[,.]11|BETA_\s?TGL_\s?PROVED|PROVED_?\s?IN_?\s?NATURE|provad[oa]\s+na\s+natureza|proved\s+in\s+nature|AT_?\s?6SIGMA|PRIMARY_?\s?UNDER|\bZ\b[^\n]{0,30}?(?:contra\s+o\s+nulo|against\s+the\s+null)", re.I)
RQ = {
 "a_modelo": re.compile(r"sob\s+o\s+modelo\s+de\s+erros\s+publicado|under\s+the\s+(?:published\s+error\s+model|error\s+model\s+published)|UNDER_?\s?THE_?\s?PUBLISHED_?\s?MODEL", re.I),
 "b_cefeidas_numero": re.compile(r"(?:Cefeidas\s+livres|free\s+Cepheids|FREE_?\s?CEPHEIDS)[^\n]{0,200}?(?:\d+[,.]\d+|BELOW_?\s?5SIGMA|BRANCH_?\s?\d)", re.I),
 "c_validade": re.compile(r"validade,?\s+n[ãa]o\s+credita[çc][ãa]o|validity,?\s+not\s+creditation|VALIDITY_?\s?NOT_?\s?CREDITATION", re.I),
 "d_retro": re.compile(r"retrodi[çc][ãa]o|retrodiction|RETRODICTION", re.I),
 "d_naocego": re.compile(r"n[ãa]o\s+(?:é\s+)?ceg[oa]|not\s+blind|NOT_?\s?BLIND", re.I),
 "e_sete": re.compile(r"sete\s+ressalvas|seven\s+reservations", re.I),
}
res = {}
for n, tx in texts.items():
    paras = [m for m in re.finditer(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", tx)]
    out_ = []
    for m in paras:
        p = m.group(0)
        occ = [o.group(0) for o in OCC.finditer(p)]
        if not occ: continue
        falta = [k for k, rx in RQ.items() if not rx.search(p)]
        out_.append({"ini": m.start(), "len": len(p), "occ": sorted(set(x.strip() for x in occ))[:6], "faltam": falta, "abre": p[:90].replace("\n"," ")})
    res[n] = out_
    print("==", n, "paragrafos com ocorrencia:", len(out_))
    for o in out_:
        print("  @%d len=%d faltam=%s occ=%s | %s" % (o["ini"], o["len"], o["faltam"], o["occ"][:3], o["abre"]))
json.dump(res, open(SC + r"\b02_resultado.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
