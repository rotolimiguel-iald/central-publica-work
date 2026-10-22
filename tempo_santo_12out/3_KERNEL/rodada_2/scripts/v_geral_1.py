# -*- coding: utf-8 -*-
"""V-GERAL-1 (conferência textual, para o auditor): para cada teorema da pedra com hipóteses (lista medida no termo
pela auditoria AuditR2), em que blocos da fonte ele é USADO fora da própria declaração e das linhas `#print`.
Cada uso é classificado pelo bloco em que aparece (example / theorem / def) e pela linha. A leitura de que o uso é
com argumentos CONCRETOS (habitação) é do auditor; a lista só localiza.
Uso: python -I v_geral_1.py <pedra.lean> <AUDIT_analise.json> <saida.json>
"""
import json
import re
import sys


def main(pedra, analise, out):
    src = open(pedra, "rb").read().decode("utf-8")
    lines = src.split("\n")
    an = json.load(open(analise, encoding="utf-8"))
    por = an["hipoteses"]["por_teorema"]
    # mapa linha -> bloco (último cabeçalho de declaração/example acima)
    blocos = []
    atual = ("(topo)", 0)
    for i, l in enumerate(lines, 1):
        m = re.match(r"^(?:noncomputable\s+)?(theorem|lemma|def|abbrev|example|instance)\b\s*([^\s:({\[]*)", l)
        if m:
            atual = (m.group(1) + (" " + m.group(2) if m.group(2) else ""), i)
        blocos.append(atual)
    res = {"pedra": pedra, "teoremas": []}
    for full, info in por.items():
        if info["n_hipoteses"] == 0:
            continue
        short = full.split(".")[-1]
        if short.startswith("eq_"):
            continue
        usos = []
        pat = re.compile(r"(?<![\w.'])" + re.escape(short) + r"(?![\w'])")
        for i, l in enumerate(lines, 1):
            if l.startswith("#print"):
                continue
            if pat.search(l):
                b = blocos[i - 1]
                if b[0].endswith(" " + short):
                    continue  # a própria declaração
                usos.append({"linha": i, "bloco": b[0], "bloco_linha": b[1]})
        res["teoremas"].append({"teorema": full, "n_hipoteses": info["n_hipoteses"], "n_usos": len(usos),
                                "usos_em_example": sum(1 for u in usos if u["bloco"].startswith("example")),
                                "usos": usos[:12]})
    res["sem_uso_algum"] = [t["teorema"] for t in res["teoremas"] if t["n_usos"] == 0]
    res["so_usado_em_provas"] = [t["teorema"] for t in res["teoremas"] if t["n_usos"] > 0 and t["usos_em_example"] == 0]
    with open(out, "w", encoding="utf-8") as fo:
        json.dump(res, fo, ensure_ascii=False, indent=1)
    sys.stdout.reconfigure(encoding="utf-8")
    print("teoremas com hipoteses:", len(res["teoremas"]))
    print("sem uso algum:", res["sem_uso_algum"])
    print("so usados dentro de outras provas (sem example):")
    for t in res["teoremas"]:
        if t["n_usos"] > 0 and t["usos_em_example"] == 0:
            print("  ", t["teorema"].split(".")[-1], "->", sorted({u["bloco"] for u in t["usos"]}))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
