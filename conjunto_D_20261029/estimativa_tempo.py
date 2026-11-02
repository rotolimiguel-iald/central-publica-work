# -*- coding: utf-8 -*-
# Estimativa de tempo/CPU do conjunto D a partir de recibos MEDIDOS da bancada (GW250114, calibracao NOT_BLIND) e de numeros meus de hoje.
# Todas as entradas sao lidas dos recibos por script; as hipoteses sobre "chamadas ate convergir" sao CENARIOS, nao medidas.
import json, math

R = "C:/IALD/Central de Patentes/Chatgpt/ORDEM_013_RINGDOWN/cache/"
W = "C:/IALD/Central de Patentes/work/conjunto_D_20261029"


def rd(p):
    return json.load(open(p, encoding="utf-8"))


a_c = rd(R + "E3_PSEOB_PILOT_V2_S220/CONTROLLER.json")
a_v = rd(R + "E3_PSEOB_PILOT_V2_S220/PRIVATE_CONVERGENCE.json")
b_c = rd(R + "E3_PSEOB_PILOT_V2_S220_C1/CONTROLLER.json")
b_v = rd(R + "E3_PSEOB_PILOT_V2_S220_C1/PRIVATE_CONVERGENCE.json")
runs = []
for nome, c, v, workers in [("S220", a_c, a_v, 24), ("S220_C1", b_c, b_v, 24)]:
    cpu = c["children_user_cpu_seconds"] + c["children_system_cpu_seconds"]
    wall = c["wall_seconds"]
    runs.append(dict(job=nome, ncall=v["ncall"], wall_s=wall, cpu_s=cpu, cpu_por_call=cpu / v["ncall"], cores_efetivos=cpu / wall,
                     eficiencia=cpu / wall / workers, delta_logz=v["delta_logz"], ess=v["ess"],
                     source_s_por_call=v["cost"]["source_seconds_per_call"], workers=workers))
cpu_call = (min(r["cpu_por_call"] for r in runs), max(r["cpu_por_call"] for r in runs))
cores1 = (min(r["cores_efetivos"] for r in runs), max(r["cores_efetivos"] for r in runs))
# 48 nucleos: 2 PEs de 24 workers em paralelo
cores_total = (2 * cores1[0], 2 * cores1[1])
cen = {"otimista (3e6 chamadas)": 3e6, "central (1e7 chamadas)": 1e7, "pessimista (3e7 chamadas)": 3e7}
etapas = {"F4.1 (2 PE sinteticas)": 2, "D10 PE cega (10 PE)": 10, "C2 minima (10 PE)": 10, "C2 media (20 PE)": 20, "C2 ampla (50 PE)": 50}
out = dict(execucoes_medidas=runs, cpu_s_por_chamada_faixa=cpu_call, cores_efetivos_por_PE_24workers=cores1, cores_efetivos_2PE_paralelas=cores_total, cenarios={})
lines = ["| cenario | CPU-h por PE | wall de 1 PE (24 workers) | " + " | ".join(etapas.keys()) + " |", "|---|---|---|" + "---|" * len(etapas)]
for nome, n in cen.items():
    cpuh = (n * cpu_call[0] / 3600, n * cpu_call[1] / 3600)
    wall1 = (cpuh[0] * 3600 / cores1[1] / 3600, cpuh[1] * 3600 / cores1[0] / 3600)
    cols = []
    for et, k in etapas.items():
        tot = (k * cpuh[0], k * cpuh[1])
        w = (tot[0] / cores_total[1], tot[1] / cores_total[0])
        cols.append("%.0f-%.0f CPU-h; %.1f-%.1f h" % (tot[0], tot[1], w[0], w[1]))
    lines.append("| %s | %.0f-%.0f | %.1f-%.1f h | %s |" % (nome, cpuh[0], cpuh[1], wall1[0], wall1[1], " | ".join(cols)))
    out["cenarios"][nome] = dict(calls=n, cpu_h_por_PE=cpuh, wall_h_1PE=wall1)
tot_lines = ["| cenario | F4.1 + D10 + C2 minima (22 PE) | F4.1 + D10 + C2 media (32 PE) | F4.1 + D10 + C2 ampla (62 PE) |", "|---|---|---|---|"]
for nome, n in cen.items():
    cpuh = (n * cpu_call[0] / 3600, n * cpu_call[1] / 3600)
    row = []
    for k in (22, 32, 62):
        tot = (k * cpuh[0], k * cpuh[1])
        w = (tot[0] / cores_total[1], tot[1] / cores_total[0])
        row.append("%.0f-%.0f CPU-h; %.0f-%.0f h (%.1f-%.1f dias)" % (tot[0], tot[1], w[0], w[1], w[0] / 24, w[1] / 24))
    tot_lines.append("| %s | %s | %s | %s |" % (nome, row[0], row[1], row[2]))
open(W + "/_tabela_tempo.md", "w", encoding="utf-8").write("\n".join(lines) + "\n\nTotais:\n\n" + "\n".join(tot_lines) + "\n")
json.dump(out, open(W + "/ESTIMATIVA_TEMPO_D.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(runs, indent=1))
print("cpu_s/chamada", cpu_call, "cores efetivos/PE", cores1, "2 PE", cores_total)
print(open(W + "/_tabela_tempo.md", encoding="utf-8").read())
