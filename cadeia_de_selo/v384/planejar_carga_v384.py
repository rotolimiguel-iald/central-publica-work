# -*- coding: utf-8 -*-
"""Planejador da carga do pilar quantico da v384 (so contas sobre os custos MEDIDOS na sonda 2; nenhum calculo dos testes).
Custo por instancia: T2/T3/T4 = pipeline inteiro (espectro + estacionario + propagador + trajetoria + Choi); T1 = sem espectro e sem Choi
(a injecao precisa do estacionario, do propagador e da trajetoria). d=128 estimado por n^3 a partir de d=64 [DERIVED]. Margem declarada x1,25
para a disputa de CPU com o lake build (o eig da GPU e' hibrido). O rito v383 lido do arquivo de horarios e do selo."""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
p = json.load(open(os.path.join(HERE, "sonda_pipeline_gpu_v384.json"), encoding="utf-8"))["por_d"]
full = {d: p["d%d" % d]["total"] for d in (8, 16, 32, 64)}
inj = {d: sum(p["d%d" % d][k] for k in ("montar", "estacionario_lu", "propagador_expm", "trajetoria_64x3_e_entropias")) for d in (8, 16, 32, 64)}
full128 = full[64] * 64.0
MARGEM = 1.25
NIVEIS = {
    "A_cabe_no_rito": {"T4": {8: 10000, 16: 3000, 32: 600, 64: 30}, "T1": {8: 1000, 16: 1000, 32: 200, 64: 10},
                       "T2": {8: 96, 16: 96, 32: 96, 64: 48}, "T3": {8: 10, 16: 10, 32: 10, 64: 10}, "d128": 0},
    "B_robusto": {"T4": {8: 20000, 16: 5000, 32: 1000, 64: 100}, "T1": {8: 2000, 16: 2000, 32: 1000, 64: 100},
                  "T2": {8: 192, 16: 192, 32: 192, 64: 96}, "T3": {8: 10, 16: 10, 32: 10, 64: 10}, "d128": 1},
}
out = {"custos_s": {"pipeline": full, "injecao": inj, "pipeline_d128_estimado": full128}, "margem": MARGEM, "niveis": {}}
for nome, n in NIVEIS.items():
    t = {}
    for T in ("T4", "T2", "T3"):
        t[T] = sum(cnt * full[d] for d, cnt in n[T].items())
    t["T1"] = sum(cnt * inj[d] for d, cnt in n["T1"].items())
    t["d128"] = n["d128"] * full128
    tot = sum(t.values())
    lim = {T: {d: round(3.0 / cnt * 100, 3) for d, cnt in n[T].items()} for T in ("T4", "T1")}
    out["niveis"][nome] = {"min_por_teste": {k: round(v / 60, 1) for k, v in t.items()}, "total_min": round(tot / 60, 1),
                           "total_com_margem_min": round(tot * MARGEM / 60, 1), "limite_95pct_de_falha_pct_se_zero_falhas": lim, "contagens": n}
    print(nome, "| total %.1f min | com margem %.1f min |" % (tot / 60, tot * MARGEM / 60), {k: round(v / 60, 1) for k, v in t.items()})
    print("   limite superior 95%% da taxa de violacao (zero falhas), T4:", lim["T4"], "| T1:", lim["T1"])
hor = open(os.path.join(os.path.dirname(HERE), "v383", "rito_horarios_v383.txt"), encoding="utf-8").read().split()
ts = json.load(open(os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "um_absoluto_selo.json"), encoding="utf-8"))["timestamp"]
def seg(h):
    a, b, c = (int(x) for x in h.split(":")); return a * 3600 + b * 60 + c
ate = (seg(ts.split()[1]) - seg(hor[0])) / 60; auto = (seg(hor[1]) - seg(ts.split()[1])) / 60
out["rito_v383_min"] = {"ate_o_selo": round(ate, 1), "autoteste": round(auto, 1), "total": round(ate + auto, 1)}
for nome in NIVEIS:
    g = out["niveis"][nome]["total_com_margem_min"]
    # a GPU comeca junto com o rito; o artigo e o selo esperam a GPU se ela passar do ponto do selo; o autoteste continua no fim
    out["niveis"][nome]["rito_estimado_min"] = round(max(ate, g + 3) + auto, 1)
    print(nome, "-> rito estimado %.0f min (hoje %.0f)" % (out["niveis"][nome]["rito_estimado_min"], ate + auto))
open(os.path.join(HERE, "planejar_carga_v384.json") + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
os.replace(os.path.join(HERE, "planejar_carga_v384.json") + ".tmp", os.path.join(HERE, "planejar_carga_v384.json"))
print("custo por instancia (s):", {d: round(v, 3) for d, v in full.items()}, "| injecao:", {d: round(v, 3) for d, v in inj.items()}, "| d128 ~%.1f min" % (full128 / 60))
