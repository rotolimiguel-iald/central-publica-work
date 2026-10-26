# -*- coding: utf-8 -*-
"""quadro_v399_vs_v400.py -- exame final v400: o quadro do topo do artigo PT/EN (os .txt) e do .md da v400 (ensaio, dry_v400) e' o MESMO da v399 SELADA (o Nos, so lido)?"""
import os, json
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
DRY = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v400\dry_v400"
res = {}
for lang, tit, fim, fn in (("pt", "O Teste da Única Palavra", "Sumário", "dry_v400_pt.txt"), ("en", "The Test of the Only Word", "Contents", "dry_v400_en.txt")):
    a = open(os.path.join(NOS, "um_absoluto_%s.txt" % lang), encoding="utf-8", errors="replace").read()
    b = open(os.path.join(DRY, fn), encoding="utf-8", errors="replace").read()
    ia, ib = a.find(tit), b.find(tit)
    ja, jb = a.find(fim, ia), b.find(fim, ib)
    qa, qb = a[ia:ja], b[ib:jb]
    res[lang] = {"pos_v399": ia, "pos_v400": ib, "fim_v399": ja, "fim_v400": jb, "chars": [len(qa), len(qb)], "quadro_igual": qa == qb and len(qa) > 1500,
                 "igual_2600": a[ia:ia + 2600] == b[ib:ib + 2600]}
a = open(os.path.join(NOS, "um_absoluto_forma_canonica.md"), encoding="utf-8").read(); b = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
ia, ib = a.find("O Teste da Única Palavra"), b.find("O Teste da Única Palavra")
ja, jb = a.find("\n#", ia), b.find("\n#", ib)
res["md"] = {"pos": (ia, ib), "fim_primeiro_titulo": (ja, jb), "quadro_igual_ate_o_primeiro_titulo": a[ia:ja] == b[ib:jb] and ja - ia > 1500, "chars": [ja - ia, jb - ib]}
print(json.dumps(res, ensure_ascii=False, indent=1))
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "QUADRO_v399_SELADA_vs_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
