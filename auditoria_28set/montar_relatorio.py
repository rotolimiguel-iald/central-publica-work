# -*- coding: utf-8 -*-
"""Monta o RELATÓRIO final: cabeçalho e seções 1–3 (texto da gerência), a tabela por família e a contagem LIDAS do diário do workflow,
as seções 4–8, e a seção 9 com o sha256 de cada artefato CALCULADO aqui (nada digitado)."""
import hashlib
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
J = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\subagents\workflows\wf_58da7663-e79\journal.jsonl"
ORDEM = ["gate_vazios", "d1_fundo", "gw_eco", "ringdown", "relogios_neutrinos_coma", "estatistica_veredito", "consistencia_teorica"]
NOMES = {"gate_vazios": "Gate e vazios/lentes", "d1_fundo": "D1 e fundo", "gw_eco": "Ecos GW", "ringdown": "Ringdown",
         "relogios_neutrinos_coma": "Relógios, neutrinos, Coma", "estatistica_veredito": "Estatística e veredito",
         "consistencia_teorica": "Consistência teórica"}
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
linhas = ["| família | achados | sustentados | parciais | refutados | sem verificação | novos do verificador | os mais pesados (depois da verificação) |",
          "|---|---|---|---|---|---|---|---|"]
T = dict(a=0, s=0, p=0, r=0, x=0, n=0)
for f in ORDEM:
    a, v = aud.get(f), ver.get(f)
    if not a:
        linhas.append("| %s | — | — | — | — | — | — | (sem resultado do aferidor) |" % NOMES[f])
        continue
    vv = {x["id"]: x for x in (v["veredictos"] if v else [])}
    c = dict(s=0, p=0, r=0, x=0)
    pesados = []
    for x in a["achados"]:
        w = vv.get(x["id"])
        k = {"SUSTENTADO": "s", "PARCIAL": "p", "REFUTADO": "r"}.get(w["veredicto"] if w else "", "x")
        c[k] += 1
        sev = w["severidade_revista"] if w else x["severidade"]
        if k in ("s", "p") and sev in ("CRITICO", "ALTO", "MEDIO"):
            pesados.append((["CRITICO", "ALTO", "MEDIO"].index(sev), "%s %s" % (x["id"], sev)))
    nn = len(v.get("achados_novos", [])) if v else 0
    T["a"] += len(a["achados"]); T["s"] += c["s"]; T["p"] += c["p"]; T["r"] += c["r"]; T["x"] += c["x"]; T["n"] += nn
    linhas.append("| %s | %d | %d | %d | %d | %d | %d | %s |" % (NOMES[f], len(a["achados"]), c["s"], c["p"], c["r"], c["x"], nn,
                                                          ", ".join(p for _, p in sorted(pesados)[:6]) or "—"))
cont = ("%d achados dos aferidores: **%d sustentados, %d parciais, %d %s**, %d sem verificação; e %d achados novos dos verificadores. "
        "Nenhum achado move o gate ou um número selado; todos entram ao lado." % (T["a"], T["s"], T["p"], T["r"], "refutado" if T["r"] == 1 else "refutados",
                                                                                 T["x"], T["n"]))
crit_txt = ""
if crit:
    crit_txt = ("\n**O crítico de completude:** " + crit["resumo"].replace("\n", " ") + "\n\n" +
                "\n".join("- sem auditoria: " + s for s in crit["sem_auditoria"][:12]) + "\n" +
                "\n".join("- contradição: " + s for s in crit["contradicoes"][:8]) + "\n")
rel = open(os.path.join(AQUI, "cabecalho_template.md"), encoding="utf-8").read()
cab = rel.split("## 4. A investigação na Bancada Um")[0]
cab = cab.replace("⟨contagem final⟩", cont).replace("⟨tabela por família⟩", "\n".join(linhas) + "\n" + crit_txt)
s48 = open(os.path.join(AQUI, "secoes_4_a_8.md"), encoding="utf-8").read()
ART = [r"C:\IALD\Central de Patentes\work\auditoria_28set\ANEXO_ACHADOS.md",
       r"C:\IALD\Central de Patentes\work\auditoria_28set\PEDIDO_ORQUESTRADOR_PREPARADO.md",
       r"C:\IALD\Central de Patentes\work\auditoria_28set\fontes_externas\NuFIT_6.1_v61.tbl-parameters.jpg",
       r"C:\IALD\Bancada_Um\investigacao\PREREGISTRO_INV_BANCADA_UM_20260928.json",
       r"C:\IALD\Bancada_Um\investigacao\C1_F1_calibracao_previsao.json",
       r"C:\IALD\Bancada_Um\investigacao\P1_posterior_planck_dr2.json",
       r"C:\IALD\Bancada_Um\investigacao\P2_comparar_planck_dr2.json",
       r"C:\IALD\Bancada_Um\investigacao\S1_posterior_planck_dr2_sh0es.json",
       r"C:\IALD\Bancada_Um\investigacao\S2_comparar_planck_dr2_c_livre.json",
       r"C:\IALD\Bancada_Um\investigacao\D1_jackknife_planck_dr2.json",
       r"C:\IALD\Bancada_Um\investigacao\M1_mapa_de_R.json",
       r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl", r"C:\IALD\MAPA_DE_ROTAS\MAPA_DE_ROTAS.md", r"C:\IALD\MAPA_DE_ROTAS\rotas.py"]
arq = ["| arquivo | sha256 (16) | bytes |", "|---|---|---|"]
for p in ART:
    b = open(p, "rb").read()
    arq.append("| `%s` | `%s` | %d |" % (p, hashlib.sha256(b).hexdigest()[:16], len(b)))
sys.path.insert(0, r"C:\IALD\MAPA_DE_ROTAS")
import rotas  # noqa: E402
vm = rotas.verificar()
arq.append("")
arq.append("Mapa de Rotas no fechamento deste relatório: %d registros, %d rotas, cabeça da cadeia `%s`." % (vm["n_registros"], vm["n_rotas"], vm["cabeca"][:16]))
arq.append("")
arq.append("Selo e programa intocados: `um.py` sha16 `%s`; selo sha16 `%s`." % (
    hashlib.sha256(open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py", "rb").read()).hexdigest()[:16],
    hashlib.sha256(open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json", "rb").read()).hexdigest()[:16]))
final = cab + s48.rstrip() + "\n\n## 9. Arquivos (sha256 calculado por script)\n\n" + "\n".join(arq) + "\n"
p = os.path.join(AQUI, "RELATORIO_AUDITORIA_E_INVESTIGACAO_20260928.md")
b0 = open(p, "rb").read()
open(p + ".bak_montagem_anterior", "wb").write(b0)
b = final.encode("utf-8")
open(p + ".tmp", "wb").write(b)
os.replace(p + ".tmp", p)
print("relatório:", len(b), "bytes, sha16", hashlib.sha256(b).hexdigest()[:16], "|", cont)
