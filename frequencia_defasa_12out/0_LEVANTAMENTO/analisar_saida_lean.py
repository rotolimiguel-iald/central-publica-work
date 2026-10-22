# -*- coding: utf-8 -*-
# Analisa a saida das sondas Lean: cada '#print axioms' deve resultar em conjunto de axiomas contido no trio
# {propext, Classical.choice, Quot.sound} (ou em nenhum axioma). Lista nomes ausentes/erros. Somente leitura.
import re, json, os, sys, hashlib
AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "lean_check")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
res = {}
for src, out in (("LevantamentoF1FrequenciaCheck.lean", "LevantamentoF1FrequenciaCheck_SAIDA.txt"),
                 ("LevantamentoF1FrequenciaCheck2.lean", "LevantamentoF1FrequenciaCheck2_SAIDA.txt")):
    if not os.path.exists(os.path.join(D, out)):
        continue
    s = open(os.path.join(D, src), encoding="utf-8").read()
    pedidos = re.findall(r"^#print axioms (\S+)", s, re.M)
    t = open(os.path.join(D, out), encoding="utf-8", errors="replace").read()
    dep = {m.group(1): sorted(x.strip() for x in m.group(2).split(",") if x.strip())
           for m in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]*)\]", t, re.S)}
    nada = set(re.findall(r"'([^']+)' does not depend on any axioms", t))
    linhas = []
    ok = True
    for nome in pedidos:
        if nome in dep:
            ax = dep[nome]
            dentro = set(ax) <= TRIO
            ok = ok and dentro
            linhas.append({"teorema": nome, "axiomas": ax, "no_trio": dentro})
        elif nome in nada:
            linhas.append({"teorema": nome, "axiomas": [], "no_trio": True})
        else:
            ok = False
            linhas.append({"teorema": nome, "axiomas": None, "no_trio": False, "nota": "sem linha de axiomas na saida"})
    res[src] = {"n_pedidos": len(pedidos), "n_com_resposta": sum(1 for x in linhas if x["axiomas"] is not None),
                "todos_no_trio": ok, "sorryAx": t.count("sorryAx"), "erros": t.count("error"), "linhas": linhas}
# sonda Mathlib: quais nomes existem
pm = os.path.join(D, "LevantamentoF1FrequenciaMathlibProbe_SAIDA.txt")
if os.path.exists(pm):
    s = open(os.path.join(D, "LevantamentoF1FrequenciaMathlibProbe.lean"), encoding="utf-8").read()
    nomes = re.findall(r"^#check @(\S+)", s, re.M)
    t = open(pm, encoding="utf-8", errors="replace").read()
    desconhecidos = set(re.findall(r"[Uu]nknown (?:constant|identifier) '([^']+)'", t))
    existe = {n: (n not in desconhecidos and ("@" + n) not in desconhecidos) for n in nomes}
    # assinatura impressa (primeira linha apos o nome)
    res["mathlib_probe"] = {"existe": existe, "desconhecidos": sorted(desconhecidos)}
print(json.dumps({k: ({kk: vv for kk, vv in v.items() if kk != "linhas"} if isinstance(v, dict) and "linhas" in v else v) for k, v in res.items()}, ensure_ascii=False, indent=1))
with open(os.path.join(D, "ANALISE_SAIDA_LEAN.json"), "w", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)
