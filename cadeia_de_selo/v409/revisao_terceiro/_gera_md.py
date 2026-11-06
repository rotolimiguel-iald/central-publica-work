import json, sys
sys.stdout.reconfigure(encoding="utf-8")
RV = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/revisao_terceiro/"
d = json.load(open(RV + "REVISAO_TERCEIRO_v409.json", encoding="utf-8"))
L = ["# REVISAO DE TERCEIRO v409 -- R1 (Claude Sonnet; nao construi a v409)", "",
     "**NAO APROVADA** -- candidato `%s` (%d bytes; no inicio `%s`; mudou durante a revisao: %s). ALTO %d | MEDIO %d | BAIXO %d." % (d["candidato_sha16"], d["candidato_bytes"], d["candidato_sha16_no_inicio"], "sim" if d["candidato_mudou_durante_a_revisao"] else "nao", d["n_alto"], d["n_medio"], d["n_baixo"]), "",
     "aprovada: true so' com 0 ALTO e 0 MEDIO e o candidato integro do inicio ao fim. R1 de ate tres rodadas (D58). O MEDIO e' de TEXTO (estatuto errado em texto novo), nao de kernel; a correcao pedida esta' em `PEDIDO_CORRECAO_R1_v409.md`.", "",
     "## O que passou (por script, nesta pasta)", ""]
L.append("- **Lean:** %s" % json.dumps(d["lean_r1"], ensure_ascii=False))
for k, v in d["conferencias"].items(): L.append("- **%s:** %s" % (k, json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v))
L += ["", "## Achados", ""]
for i, a in enumerate(d["achados"], 1):
    L += ["### %d. %s -- %s" % (i, a["sev"], a["onde"]), "", "**Achado.** " + a["achado"], "", "**Evidencia.** " + a["evidencia"], "", "**Correcao.** " + a["correcao"], ""]
L += ["## Ressalvas", ""] + ["- " + r for r in d["ressalvas"]] + ["", "## Rotas examinadas (para a gerencia registrar no Mapa)", ""] + ["- " + r for r in d["rotas_examinadas"]]
L += ["", "## arquivos_revisados (sha16 lidos agora)", ""] + ["- `%s` `%s`" % (k, v) for k, v in d["arquivos_revisados"].items()]
open(RV + "REVISAO_TERCEIRO_v409.md", "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("md gravado", sum(len(x) for x in L))
