"""CU-C2: B-01/B-02: paragrafos NOVOS (ausentes do artigo selado da v410) do artigo PT/EN (txt e tex): guarda_frases_v411.violacoes() e os quatro obrigatorios."""
import json, os, re, sys, hashlib
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
D = r"C:\t\k411c\dry_v411"
sys.dont_write_bytecode = True
sys.path.insert(0, V)
import guarda_frases_v411 as G
rd = lambda p: open(p, "rb").read().decode("utf-8").replace("\r\n", "\n")
OCC = re.compile(r"6[,.]11|BETA_\s?TGL_\s?PROVED|PROVED_?\s?IN_?\s?NATURE|provad[oa]\s+na\s+natureza|proved\s+in\s+nature|AT_?\s?6SIGMA|PRIMARY_?\s?UNDER|\bZ\b\$?[^\n]{0,30}?(?:contra\s+o\s+nulo|against\s+the\s+null)", re.I)
RQ = {
    "a_modelo": re.compile(r"sob\s+o\s+modelo\s+de\s+erros\s+publicado|under\s+the\s+(?:published\s+error\s+model|error\s+model\s+published(?:\s+by\s+the\s+collaboration)?)|UNDER_?\s?THE_?\s?PUBLISHED_?\s?MODEL", re.I),
    "b_cefeidas_numero": re.compile(r"(?:Cefeidas\s+livres|free\s+Cepheids|FREE_?\s?CEPHEIDS)[^\n]{0,260}?(?:\d+(?:\{,\}|[,.])\d+|BELOW_?\s?5SIGMA|BRANCH_?\s?\d)", re.I),
    "c_validade": re.compile(r"validade,?\s+n[\u00e3a]o\s+credita[\u00e7c][\u00e3a]o|validity,?\s+not\s+creditation|VALIDITY_?\s?NOT_?\s?CREDITATION", re.I),
    "d_retro": re.compile(r"retrodi[\u00e7c][\u00e3a]o|retrodiction|RETRODICTION", re.I),
    "d_naocego": re.compile(r"n[\u00e3a]o\s+(?:\u00e9\s+)?ceg[oa]|not\s+blind|NOT_?\s?BLIND", re.I),
}
PAR = re.compile(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*")
res = {}
for nm, novo, velho in (("pt_txt", "dry_v411_pt.txt", "um_absoluto_pt.txt"), ("en_txt", "dry_v411_en.txt", "um_absoluto_en.txt"), ("pt_tex", "dry_v411_pt.tex", "um_absoluto_pt.tex"), ("en_tex", "dry_v411_en.tex", "um_absoluto_en.tex")):
    tn, tv = rd(os.path.join(D, novo)), rd(os.path.join(NOS, velho))
    pv = {m.group(0) for m in PAR.finditer(tv)}
    novos = [m for m in PAR.finditer(tn) if m.group(0) not in pv and len(m.group(0)) < 60000]
    viol_g = []
    viol_rq = []
    for m in novos:
        p = m.group(0)
        v = G.violacoes(p)
        if v:
            viol_g.append((m.start(), len(p), [x[0][:40] for x in v][:3], p[:70].replace("\n", " ")))
        if OCC.search(p):
            falta = [k for k, rx in RQ.items() if not rx.search(p)]
            if falta:
                viol_rq.append((m.start(), len(p), falta, p[:90].replace("\n", " ")))
    res[nm] = {"paragrafos_do_novo": len(PAR.findall(tn)), "paragrafos_do_v410": len(pv), "novos_ou_alterados": len(novos), "guarda_violacoes": len(viol_g), "rq_violacoes": len(viol_rq)}
    print("==", nm, res[nm])
    for x in viol_g[:12]:
        print("   GUARDA", x)
    for x in viol_rq[:12]:
        print("   RQ", x)
json.dump(res, open(r"C:\t\k411c\revisao_CU\c2_novos_paragrafos.json", "w", encoding="utf-8"), indent=1)
