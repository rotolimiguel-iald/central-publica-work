import json, sys
sys.stdout.reconfigure(encoding="utf-8")
RV = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/revisao_terceiro/"
d = json.load(open(RV + "REVISAO_TERCEIRO_v409.json", encoding="utf-8"))
ap = d["aprovada"]
L = ["# REVISAO DE TERCEIRO v409 -- R3, a ULTIMA (Claude Sonnet; nao construi a v409)", "",
     "**%s** -- candidato `%s` (%d bytes; no inicio da R3 `%s`; mudou durante a revisao: %s; o da R2 era `%s`, o da R1 `%s`). ALTO %d | MEDIO %d | BAIXO %d." % ("APROVADA" if ap else "NAO APROVADA", d["candidato_sha16"], d["candidato_bytes"], d["candidato_sha16_no_inicio"], "sim" if d["candidato_mudou_durante_a_revisao"] else "nao", d["candidato_da_R2"]["sha16"], d["candidato_da_R1"]["sha16"], d["n_alto"], d["n_medio"], d["n_baixo"]), "",
     "aprovada: true so' com 0 ALTO e 0 MEDIO e o candidato integro do inicio ao fim. Os BAIXOS ficam escritos e nao travam. R1 e R2 guardadas em bytes ao lado (`.R1`/`.R2` `.json`/`.md`, `PEDIDO_CORRECAO_R1/R2_v409.md`, `r1_saidas/`, `r2_saidas/`). Se qualquer arquivo de `arquivos_revisados` mudar, esta revisao nao vale para ele.", "",
     "## Condicoes da aprovacao (calculadas)", ""] + ["- %s: %s" % (k, v) for k, v in d["condicoes_da_aprovacao_calculadas"].items()]
L += ["", "## Situacao dos achados da R1 e da R2", ""] + ["- **%s:** %s" % (k, v) for k, v in d["situacao_dos_achados_da_R1_e_R2"].items()]
L += ["", "## O que passou na R3 (por script, nesta pasta)", "", "- **Lean:** %s" % json.dumps(d["lean"], ensure_ascii=False)]
for k, v in d["conferencias"].items(): L.append("- **%s:** %s" % (k, json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v))
L += ["", "## Achados abertos (todos BAIXOS)", ""]
for i, a in enumerate(d["achados"], 1):
    L += ["### %d. %s -- %s" % (i, a["sev"], a["onde"]), "", "**Achado.** " + a["achado"], "", "**Evidencia.** " + a["evidencia"], "", "**Correcao.** " + a["correcao"], "", "**Estado na R3.** " + a.get("estado_na_R3", ""), ""]
L += ["## Ressalvas", ""] + ["- " + r for r in d["ressalvas"]] + ["", "## Rotas examinadas (para a gerencia registrar no Mapa)", ""] + ["- " + r for r in d["rotas_examinadas"]]
L += ["", "## arquivos_revisados (sha16 lidos agora)", ""] + ["- `%s` `%s`" % (k, v) for k, v in d["arquivos_revisados"].items()]
open(RV + "REVISAO_TERCEIRO_v409.md", "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("md R3 gravado | aprovada:", ap)
