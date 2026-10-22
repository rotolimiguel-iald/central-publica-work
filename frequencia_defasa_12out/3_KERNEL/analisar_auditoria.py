# -*- coding: utf-8 -*-
"""Analisa logs\\auditoria_SAIDA.txt (somente leitura) e grava AUDITORIA_KERNEL.json:
(1) para CADA declaracao explicita da pedra (DECLARACOES.json): a resposta do `#print axioms` e se esta contida no
    trio {propext, Classical.choice, Quot.sound}; falta de resposta e falha visivel;
(2) varredura do ambiente: todas as constantes do modulo (inclusive auxiliares) com axiomas no trio e sem sorryAx;
(3) «nome sem peso»: para cada teorema, as hipoteses de tipo Prop que nao ocorrem no termo de prova, e enunciados
    literalmente `True`."""
import hashlib, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
TRIO = {"propext", "Classical.choice", "Quot.sound"}
saida_b = open(os.path.join(AQUI, "logs", "auditoria_SAIDA.txt"), "rb").read()
t = saida_b.decode("utf-8", errors="replace")
D = json.loads(open(os.path.join(AQUI, "DECLARACOES.json"), "rb").read().decode("utf-8"))

# nomes podem conter apostrofo (ex.: psd_is_necessary'): ancorar no inicio da linha e casar ate "' depends"
dep = {m.group(1): sorted(x.strip() for x in m.group(2).split(",") if x.strip())
       for m in re.finditer(r"^'(.+?)' depends on axioms: \[([^\]]*)\]", t, re.M | re.S)}
nada = set(re.findall(r"^'(.+?)' does not depend on any axioms", t, re.M))
por_decl = []
falhas = []
for d in D["declaracoes"]:
    n = d["nome_completo"]
    if n in dep:
        ax = dep[n]
    elif n in nada:
        ax = []
    else:
        ax = None
    ok = ax is not None and set(ax) <= TRIO
    if not ok:
        falhas.append(n)
    por_decl.append({"nome": n, "tipo": d["tipo"], "linha": d["linha"], "axiomas": ax, "no_trio": ok})

ax_sweep = {}
for m in re.finditer(r"^AX\|([^|]+)\|\[(.*)\]\s*$", t, re.M):
    ax_sweep[m.group(1)] = sorted(x.strip() for x in m.group(2).split(",") if x.strip())
hyp = {}
for m in re.finditer(r"^HYP\|([^|]+)\|(\d+)\|\[(.*)\]\|(true|false)\s*$", t, re.M):
    hyp[m.group(1)] = {"n_hipoteses_prop": int(m.group(2)),
                       "hipoteses_nao_usadas": [x.strip() for x in m.group(3).split(",") if x.strip()],
                       "enunciado_True": m.group(4) == "true"}
mv = re.search(r"^VARREDURA\|(\d+)", t, re.M)
n_sweep = int(mv.group(1)) if mv else None
sweep_fora = {k: v for k, v in ax_sweep.items() if not set(v) <= TRIO}
sweep_sorry = [k for k, v in ax_sweep.items() if "sorryAx" in v]
explicitas_no_sweep = [d["nome_completo"] for d in D["declaracoes"] if d["nome_completo"] not in ax_sweep]
sem_peso = {k: v["hipoteses_nao_usadas"] for k, v in hyp.items() if v["hipoteses_nao_usadas"]}
triviais = [k for k, v in hyp.items() if v["enunciado_True"]]
contagem_ax = {}
for x in por_decl:
    key = ",".join(x["axiomas"]) if x["axiomas"] is not None else "SEM_RESPOSTA"
    contagem_ax[key] = contagem_ax.get(key, 0) + 1
res = {
    "auditoria_saida_sha256": hashlib.sha256(saida_b).hexdigest(),
    "pedra_sha256_auditada": D["pedra_sha256"],
    "declaracoes_explicitas": len(por_decl),
    "print_axioms_respondidos": sum(1 for x in por_decl if x["axiomas"] is not None),
    "todas_no_trio": not falhas,
    "falhas": falhas,
    "contagem_por_conjunto_de_axiomas": contagem_ax,
    "varredura_constantes_do_modulo": n_sweep,
    "varredura_linhas_AX": len(ax_sweep),
    "varredura_fora_do_trio": sweep_fora,
    "varredura_sorryAx": sweep_sorry,
    "explicitas_ausentes_da_varredura": explicitas_no_sweep,
    "teoremas_analisados_nome_sem_peso": len(hyp),
    "hipoteses_sem_peso": sem_peso,
    "enunciados_literalmente_True": triviais,
    "constantes_auxiliares": sorted(k for k in ax_sweep if k not in {d["nome_completo"] for d in D["declaracoes"]}),
    "por_declaracao": por_decl,
    "hipoteses_por_teorema": hyp,
}
ok = (not falhas and not sweep_fora and not sweep_sorry and n_sweep == len(ax_sweep) and not triviais)
res["veredito_auditoria"] = "AXIOMAS_NO_TRIO_ZERO_SORRY" if ok else "AUDITORIA_ACHOU"
dst = os.path.join(AQUI, "AUDITORIA_KERNEL.json")
with open(dst + ".tmp", "wb") as f:
    f.write(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8") + b"\n")
os.replace(dst + ".tmp", dst)
print(json.dumps({k: res[k] for k in ("declaracoes_explicitas", "print_axioms_respondidos", "todas_no_trio", "falhas",
                                      "contagem_por_conjunto_de_axiomas", "varredura_constantes_do_modulo",
                                      "varredura_linhas_AX", "varredura_fora_do_trio", "varredura_sorryAx",
                                      "explicitas_ausentes_da_varredura", "teoremas_analisados_nome_sem_peso",
                                      "hipoteses_sem_peso", "enunciados_literalmente_True", "constantes_auxiliares",
                                      "veredito_auditoria")}, ensure_ascii=False, indent=1))
sys.exit(0 if ok else 2)
