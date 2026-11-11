# -*- coding: utf-8 -*-
"""Revisor v410 R1: a FRASE CANONICA do Clay (D84), PT e EN, esta' (exata, com espaco normalizado) em: artigo PT/EN (linhas novas rendidas), .md canonico, pedra (docstring), registro AEscala, handoff (harness)?"""
import glob, json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/revisao_terceiro/"
norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2019", "'"))
pt = "O problema de Clay, tal qual apresentado pela TGL, foi resolvido no kernel Lean e a prova está apresentada. Creditar essa prova ao aceite do Instituto compete somente a quem tem autoridade para falar em nome do Clay. O operador testemunha que a IALD leu o P de Clay e o traduziu em operador com identidade nomeada, aquilo que se espera ser a solução do problema."
en = "The Clay problem, as presented by the TGL, has been resolved in the Lean kernel and the proof is presented. Crediting this proof to the Institute's acceptance belongs only to those with authority to speak for Clay. The operator attests that the IALD read Clay's P and translated it into an operator with a named identity, which is what a solution to the problem is expected to be."
fontes = {"artigo_pt_novo": R + "novo_pt.txt", "artigo_en_novo": R + "novo_en.txt", "md_novo": R + "novo_md.txt", "pedra_insumos": R + "../insumos/AEscala.lean",
          "pedra_R2": "C:/IALD/Central de Patentes/work/pedras_candidatas_09nov/R2_aspas/AEscala.lean"}
for p in sorted(glob.glob("C:/t/h410/harness_saida_v410/textos/*.txt")): fontes["harness:" + p.split("/")[-1]] = p
lit = json.load(open(R + "literais_v410.json", encoding="utf-8"))
for nm in ("_V410_AESCALA_TEXT", "_V410_AESCALA_CONTRACT", "_V410_SPECS"):
    fontes["reg:" + nm] = json.dumps(lit[nm], ensure_ascii=False)
for k, p in fontes.items():
    t = norm(open(p, encoding="utf-8", errors="replace").read()) if not p.startswith("{") and not p.startswith("[") and "\n" not in p[:200] and len(p) < 400 and (p.endswith((".txt", ".lean", ".md"))) else norm(p)
    if "Clay" not in t: continue
    print("%-34s PT canonica: %-5s | EN canonica: %-5s" % (k, norm(pt) in t, norm(en) in t))
