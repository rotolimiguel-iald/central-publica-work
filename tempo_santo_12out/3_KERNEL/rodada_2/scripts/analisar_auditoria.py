# -*- coding: utf-8 -*-
"""Lê a saída da auditoria do construtor (AuditR2.lean) e a fonte da pedra; resume, por script:
constantes do namespace × declarações com #print; perfil de axiomas; uso de hipóteses no termo de prova.
Uso: python -I analisar_auditoria.py <saida_audit.txt> <pedra.lean> <saida.json>
"""
import json
import re
import sys


def main(audit, pedra, out):
    txt = open(audit, "rb").read().decode("utf-8")
    src = open(pedra, "rb").read().decode("utf-8")
    dec = [l.split("\t") for l in txt.splitlines() if l.startswith("AUDIT_DECL\t")]
    names = {d[1]: {"tipo": d[2], "axiomas": [a for a in d[3].split(",") if a]} for d in dec}
    prints = set(re.findall(r"^#print axioms\s+(\S+)", src, re.M))
    extra = sorted(set(names) - prints)
    hyp = [l.split("\t") for l in txt.splitlines() if l.startswith("HYP_USE\t")]
    trio = {"propext", "Classical.choice", "Quot.sound"}
    res = {
        "n_constantes_no_namespace": len(names),
        "n_declaracoes_com_print": len(prints),
        "constantes_alem_das_declaradas": [{"nome": e, **names[e]} for e in extra],
        "prints_sem_constante": sorted(prints - set(names)),
        "fora_do_trio": [n for n, v in names.items() if not set(v["axiomas"]) <= trio],
        "perfil_de_axiomas": {},
        "hipoteses": {
            "n_teoremas": len(hyp),
            "n_teoremas_com_hipoteses": sum(1 for h in hyp if int(h[2]) > 0),
            "n_hipoteses_medidas": sum(int(h[2]) for h in hyp),
            "nao_usadas": [{"teorema": h[1], "hipoteses": h[3]} for h in hyp if h[3] != "todas_usadas"],
            "por_teorema": {h[1]: {"n_hipoteses": int(h[2]), "uso": h[3]} for h in hyp},
        },
    }
    for n, v in names.items():
        k = ",".join(v["axiomas"]) or "(nenhum)"
        res["perfil_de_axiomas"].setdefault(k, []).append(n)
    res["perfil_de_axiomas_contagem"] = {k: len(v) for k, v in res["perfil_de_axiomas"].items()}
    with open(out, "w", encoding="utf-8") as fo:
        json.dump(res, fo, ensure_ascii=False, indent=1)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("n_constantes_no_namespace", "n_declaracoes_com_print", "prints_sem_constante",
                                          "fora_do_trio", "perfil_de_axiomas_contagem")}, ensure_ascii=False))
    for e in res["constantes_alem_das_declaradas"]:
        print("  alem:", e["nome"], e["tipo"], ",".join(e["axiomas"]))
    for k, v in res["perfil_de_axiomas"].items():
        if k != "propext,Classical.choice,Quot.sound":
            print("  perfil", k, v)
    h = res["hipoteses"]
    print("  teoremas:", h["n_teoremas"], "com hipoteses:", h["n_teoremas_com_hipoteses"], "hipoteses medidas:",
          h["n_hipoteses_medidas"], "nao usadas:", h["nao_usadas"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
