"""CU-C1: B-01 (fecho nos dois blocos, PT e EN; os quatro obrigatorios em toda ocorrencia do primario) sobre o RENDIDO novo."""
import json, re, os, hashlib
F = r"C:\t\k411c\falso_nos_v411"
D = r"C:\t\k411c\dry_v411"
rd = lambda p: open(p, "rb").read().decode("utf-8").replace("\r\n", "\n")
texts = {"pt_txt": rd(os.path.join(D, "dry_v411_pt.txt")), "en_txt": rd(os.path.join(D, "dry_v411_en.txt")), "md": rd(os.path.join(F, "um_absoluto_forma_canonica.md")),
         "man": rd(os.path.join(F, "um_absoluto_manifest.md")), "out": rd(os.path.join(F, "rodada_v411_stdout.txt")),
         "pt_tex": rd(os.path.join(D, "dry_v411_pt.tex")), "en_tex": rd(os.path.join(D, "dry_v411_en.tex"))}
OCC = re.compile(r"6[,.]11|BETA_\s?TGL_\s?PROVED|PROVED_?\s?IN_?\s?NATURE|provad[oa]\s+na\s+natureza|proved\s+in\s+nature|AT_?\s?6SIGMA|PRIMARY_?\s?UNDER|\bZ\$?\s+(?:contra\s+o\s+nulo|against\s+the\s+null)|\bZ\b[^\n]{0,30}?(?:contra\s+o\s+nulo|against\s+the\s+null)", re.I)
RQ = {
    "a_modelo": re.compile(r"sob\s+o\s+modelo\s+de\s+erros\s+publicado|under\s+the\s+(?:published\s+error\s+model|error\s+model\s+published(?:\s+by\s+the\s+collaboration)?)|UNDER_?\s?THE_?\s?PUBLISHED_?\s?MODEL", re.I),
    "b_cefeidas_numero": re.compile(r"(?:Cefeidas\s+livres|free\s+Cepheids|FREE_?\s?CEPHEIDS)[^\n]{0,260}?(?:\d+[,.]\d+|BELOW_?\s?5SIGMA|BRANCH_?\s?\d)", re.I),
    "c_validade": re.compile(r"validade,?\s+n[\u00e3a]o\s+credita[\u00e7c][\u00e3a]o|validity,?\s+not\s+creditation|VALIDITY_?\s?NOT_?\s?CREDITATION", re.I),
    "d_retro": re.compile(r"retrodi[\u00e7c][\u00e3a]o|retrodiction|RETRODICTION", re.I),
    "d_naocego": re.compile(r"n[\u00e3a]o\s+(?:\u00e9\s+)?ceg[oa]|not\s+blind|NOT_?\s?BLIND", re.I),
}
res = {}
tot_viol = 0
for n, tx in texts.items():
    # para os .tex o paragrafo e' o bloco entre linhas em branco
    paras = [m for m in re.finditer(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", tx)]
    n_occ = 0
    viol = []
    for m in paras:
        p = m.group(0)
        if len(p) > 60000:
            continue
        occ = [o.group(0) for o in OCC.finditer(p)]
        if not occ:
            continue
        n_occ += 1
        falta = [k for k, rx in RQ.items() if not rx.search(p)]
        if falta:
            viol.append({"ini": m.start(), "len": len(p), "faltam": falta, "abre": p[:80].replace("\n", " ")})
    res[n] = {"paragrafos_com_ocorrencia": n_occ, "violacoes": viol}
    print("==", n, "paragrafos com ocorrencia:", n_occ, "| sem os quatro:", len(viol))
    for v in viol:
        print("   @%d len=%d faltam=%s | %s" % (v["ini"], v["len"], v["faltam"], v["abre"]))
    tot_viol += len(viol)
print("TOTAL violacoes (pt_txt, en_txt, md, man, out, tex):", tot_viol)
json.dump(res, open(r"C:\t\k411c\revisao_CU\c1_obrigatorios.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# fecho: os dois blocos
core = json.load(open(os.path.join(D, "core_ensaio.json"), encoding="utf-8"))["core"]
zn = core["h0dn_bg1_v411"]["values"]["cefeidas_livres"]["z_null"]
print("z_null cefeidas livres (core):", zn)
for lang, tx, head1, head2, mk in (("pt", texts["pt_txt"], "Os estresses", "O esperado pelos agregados", "Cefeidas livres"), ("en", texts["en_txt"], "The stresses", "What the public aggregates predict", "free Cepheids")):
    for h in (head1, head2):
        i = tx.find(h)
        if i < 0:
            print(lang, "cabecalho nao achado:", h)
            continue
        p = re.match(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", tx[i:]).group(0)
        print(lang, "|", h, "| len", len(p), "| termina com:", p[-230:].replace("\n", " "))
