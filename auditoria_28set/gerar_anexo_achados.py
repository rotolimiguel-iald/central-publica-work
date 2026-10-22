# -*- coding: utf-8 -*-
"""Gera ANEXO_ACHADOS.md direto do diário do workflow da auditoria de 28/09 (nada transcrito à mão): por família, cada achado do aferidor com o
veredicto do verificador adversarial, a severidade revista, a evidência e a correção proposta; os achados novos dos verificadores; os conferidos OK."""
import hashlib
import json
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
J = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\subagents\workflows\wf_58da7663-e79\journal.jsonl"
AQUI = os.path.dirname(os.path.abspath(__file__))
ORDEM = ["gate_vazios", "d1_fundo", "gw_eco", "ringdown", "relogios_neutrinos_coma", "estatistica_veredito", "consistencia_teorica"]
NOMES = {"gate_vazios": "Gate e piso dos vazios / lenteamento", "d1_fundo": "D1 e fundo cosmológico", "gw_eco": "Ecos de ondas gravitacionais",
         "ringdown": "Ringdown", "relogios_neutrinos_coma": "Relógios, dephasing, neutrinos e Coma",
         "estatistica_veredito": "Estatística conjunta, máquina do veredito e checagens transversais",
         "consistencia_teorica": "Consistência com a formulação da QG fechada"}
SEV = ["CRITICO", "ALTO", "MEDIO", "BAIXO", "INFO"]
aud, ver, crit = {}, {}, None
for l in open(J, encoding="utf-8"):
    try:
        e = json.loads(l)
    except Exception:
        continue
    if e.get("type") != "result":
        continue
    r = e.get("result") or e.get("value") or e.get("output")
    if isinstance(r, str):
        try:
            r = json.loads(r)
        except Exception:
            continue
    if not isinstance(r, dict):
        continue
    if "veredictos" in r:
        ver[r["familia"].split(" ")[0]] = r
    elif "achados" in r:
        aud[r["familia"]] = r
    elif "sem_auditoria" in r:
        crit = r
L = ["# ANEXO — os achados da auditoria de 28/09/2026, família por família", "",
     "> Gerado por script (`gerar_anexo_achados.py`) a partir do diário do workflow `wf_58da7663-e79`, em %s. Nada foi transcrito à mão." % time.strftime("%d/%m/%Y %H:%M"),
     "> Cada achado traz o veredicto do **verificador adversarial** (um agente distinto do aferidor, instruído a refutar): SUSTENTADO, PARCIAL, "
     "REFUTADO ou NAO_VERIFICAVEL, com a severidade revista. Achado sem verificação está marcado como tal.", ""]
tot = dict(achados=0, sustentados=0, parciais=0, refutados=0, nao_verif=0, sem_verif=0, novos=0)
por_sev = {s: 0 for s in SEV}
for fam in ORDEM:
    a = aud.get(fam)
    v = ver.get(fam)
    L += ["## %s (`%s`)" % (NOMES[fam], fam), ""]
    if not a:
        L += ["*(o aferidor desta família não devolveu resultado)*", ""]
        continue
    L += ["**Resumo do aferidor:** " + a["resumo"].replace("\n", " ")[:3500], ""]
    if v:
        L += ["**Resumo do verificador:** " + v["resumo"].replace("\n", " ")[:2500], ""]
    else:
        L += ["**Verificação adversarial: ainda não concluída.**", ""]
    vv = {x["id"]: x for x in (v["veredictos"] if v else [])}
    itens = sorted(a["achados"], key=lambda x: SEV.index((vv.get(x["id"], {}).get("severidade_revista") or x["severidade"])))
    L += ["| id | severidade (revista) | classe | verificador | achado |", "|---|---|---|---|---|"]
    for x in itens:
        tot["achados"] += 1
        w = vv.get(x["id"])
        vered = w["veredicto"] if w else "SEM VERIFICAÇÃO"
        sev = w["severidade_revista"] if w else x["severidade"]
        key = {"SUSTENTADO": "sustentados", "PARCIAL": "parciais", "REFUTADO": "refutados", "NAO_VERIFICAVEL": "nao_verif"}.get(vered, "sem_verif")
        tot[key] += 1
        if vered in ("SUSTENTADO", "PARCIAL"):
            por_sev[sev] += 1
        L.append("| %s | %s%s | %s | %s | %s (rota `%s`) |" % (x["id"], sev, "" if sev == x["severidade"] else " (era %s)" % x["severidade"], x["classe"], vered,
                                                           x["titulo"].replace("|", "/"), x["rota_id"]))
    L.append("")
    for x in itens:
        w = vv.get(x["id"])
        L += ["**%s — %s**" % (x["id"], x["titulo"]), "",
              "- afirmação auditada: " + x["afirmacao_auditada"].replace("\n", " ")[:900],
              "- evidência: " + " · ".join(e.replace("\n", " ")[:400] for e in x["evidencia"][:6])]
        if x.get("recomputo"):
            L.append("- recomputo: " + x["recomputo"].replace("\n", " ")[:900])
        if x.get("consulta_de_ausencia"):
            L.append("- consulta de ausência: " + x["consulta_de_ausencia"].replace("\n", " ")[:500])
        L.append("- correção proposta: " + x["correcao_proposta"].replace("\n", " ")[:1200])
        if w:
            L.append("- **verificador (%s, %s):** %s" % (w["veredicto"], w["severidade_revista"], w["razao"].replace("\n", " ")[:1400]))
        L.append("")
    if v and v.get("achados_novos"):
        L += ["**Achados novos do verificador:**", ""]
        for x in v["achados_novos"]:
            tot["novos"] += 1
            por_sev[x["severidade"]] += 1
            L += ["- **%s (%s, %s)** — %s. %s Correção: %s" % (x["id"], x["severidade"], x["classe"], x["titulo"], x["afirmacao_auditada"].replace("\n", " ")[:600],
                                                              x["correcao_proposta"].replace("\n", " ")[:700])]
        L.append("")
    if a.get("conferidos_ok"):
        L += ["**Conferido OK (negativo honesto é resultado):**", ""]
        for x in a["conferidos_ok"]:
            L.append("- `%s` — %s — %s" % (x["rota_id"], x["o_que"].replace("\n", " ")[:300], x["evidencia"].replace("\n", " ")[:300]))
        if v and v.get("conferidos_ok_contestados"):
            L += ["", "**Conferidos OK contestados pelo verificador:**", ""] + ["- " + c.replace("\n", " ")[:700] for c in v["conferidos_ok_contestados"]]
        L.append("")
if crit:
    L += ["## O crítico de completude", "", crit["resumo"].replace("\n", " "), "", "**Sem auditoria:**", ""] + ["- " + s for s in crit["sem_auditoria"]] + \
         ["", "**Perguntas sem resposta:**", ""] + ["- " + s for s in crit["perguntas_sem_resposta"]] + ["", "**Contradições entre famílias:**", ""] + \
         ["- " + s for s in crit["contradicoes"]] + ["", "**Recomendações:**", ""] + ["- " + s for s in crit["recomendacoes"]] + [""]
else:
    L += ["## O crítico de completude", "", "*(ainda não concluído)*", ""]
L.insert(4, "**Contagem:** %d achados dos aferidores — %d sustentados, %d parciais, %d refutados, %d não verificáveis, %d sem verificação; %d achados novos "
            "dos verificadores. Sustentados ou parciais por severidade revista (com os novos): %s." % (
                tot["achados"], tot["sustentados"], tot["parciais"], tot["refutados"], tot["nao_verif"], tot["sem_verif"], tot["novos"],
                ", ".join("%s %d" % (s, n) for s, n in por_sev.items())))
L.insert(5, "")
b = ("\n".join(L).rstrip() + "\n").encode("utf-8")
p = os.path.join(AQUI, "ANEXO_ACHADOS.md")
open(p + ".tmp", "wb").write(b)
os.replace(p + ".tmp", p)
print(json.dumps(dict(tot, por_sev=por_sev, familias_auditadas=sorted(aud), verificadas=sorted(ver), critico=bool(crit), bytes=len(b),
                      sha16=hashlib.sha256(b).hexdigest()[:16]), ensure_ascii=False))
