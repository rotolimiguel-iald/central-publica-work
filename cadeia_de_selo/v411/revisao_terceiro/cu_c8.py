"""CU-C8: B-04 (fecho do estatuto e do coracao), B-09 (rotulos, hers, datas), caracteres especiais do TeX nos textos novos, ultima frase de cada texto novo no PDF."""
import os, re, unicodedata, sys, json
D = r"C:\t\k411c\dry_v411"
F = r"C:\t\k411c\falso_nos_v411"
OUT = r"C:\t\k411c\revisao_CU"
rd = lambda p: open(p, "rb").read().decode("utf-8").replace("\r\n", "\n")
R = {}
fecho = {"pt": "Retrodição sem ajuste, teste não cego; as sete ressalvas estão no quadro do topo.", "en": "Retrodiction without fit, test not blind; the seven reservations are in the box at the top."}
for lang in ("pt", "en"):
    for ext in ("txt", "tex"):
        tx = rd(os.path.join(D, "dry_v411_%s.%s" % (lang, ext)))
        flat = re.sub(r"\s+", " ", tx)
        marc = "(v411, ao lado)" if lang == "pt" else "(v411, beside)"
        pos = [m.start() for m in re.finditer(re.escape(marc), flat)]
        com = [p for p in pos if fecho[lang] in flat[p:p + 1800]]
        # o fecho vem logo depois da frase ao lado (a primeira frase dos dois blocos termina antes)
        print(lang, ext, "ocorrencias de", marc, ":", len(pos), "| com o fecho depois (<=1800 chars):", len(com), "| ocorrencias do fecho:", flat.count(fecho[lang]))
        R["b04_%s_%s" % (lang, ext)] = (len(pos), len(com), flat.count(fecho[lang]))
        if lang == "pt" and ext == "txt":
            for p in pos:
                print("   contexto:", flat[p:p + 420])
        if lang == "en" and ext == "txt":
            for p in pos:
                print("   contexto:", flat[p:p + 520])
# B-09
for lang, rots, hers in (("pt", ["primário (modelo publicado, 13 fora)", "Cefeidas livres (13 fora)", "âncora única N4258", "âncora única LMC", "âncora única MW"], None),
                          ("en", ["primary (published model, 13 excluded)", "free Cepheids (13 excluded)", "single anchor N4258", "single anchor LMC", "single anchor MW"], "hers")):
    for ext in ("txt", "tex"):
        tx = rd(os.path.join(D, "dry_v411_%s.%s" % (lang, ext)))
        print(lang, ext, "rotulos:", {r: tx.count(r) for r in rots}, "| chaves de maquina:", {k: tx.count(k) for k in ("primario_publicado_13_fora", "cefeidas_livres_13_fora", "ancora_unica_N4258_publicado", "primario\\_publicado", "ancora\\_unica")})
        if lang == "en":
            flat = re.sub(r"\s+", " ", tx)
            i = flat.find("The support finding and the amendment")
            seg = flat[i:i + 1500]
            print("   EN secao 'hers':", len(re.findall(r"\bhers\b", seg)), "| 'its (the collaboration's)':", seg.count("its (the collaboration's)"), "| '6 Nov':", seg.count("6 Nov"), "| '11 Nov':", seg.count("11 Nov"), "| dd/mm no trecho:", re.findall(r"\b\d\d/\d\d\b", seg))
            if ext == "txt":
                j = seg.find("its (the collaboration")
                print("   contexto:", seg[max(0, j - 140):j + 100])
                k = seg.find("On 11 Nov")
                print("   contexto 2:", seg[max(0, k - 120):k + 160])
    # as datas em dd/mm na secao nova no EN inteiro
tx = rd(os.path.join(D, "dry_v411_en.txt"))
i = tx.find("The support finding and the amendment")
print("EN: dd/mm remanescentes no paragrafo inteiro do achado do suporte:", re.findall(r"\b\d\d/\d\d\b", re.match(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", tx[i:]).group(0)))
json.dump(R, open(os.path.join(OUT, "c8_b04_b09.json"), "w"), indent=1)
