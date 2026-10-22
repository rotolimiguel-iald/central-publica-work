#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DESCRITIVO POS-VEREDITO (nao entra no veredito; escrito depois que veredito.json existe).

D1  O no gamma* da rodada de fevereiro (lido do JSON de fevereiro, somente leitura), com o MESMO instrumento
    pinado (rodar.py) e as 5 sementes; reproducao do d_folds_c3 de fevereiro com a semente 42.
D2  Onde a mediana de cada config cruza ln 2 (interpolacao em log10 gamma) e o peso do core ali.
D3  A curva em oitavas em gammas de referencia (1e-4, 1e-3, 1e-2, 1e-1, 1) para a grade principal e para N2.
Saidas: descritivo.json e descritivo.md
"""
import os
import sys
import csv
import json
import math
import statistics

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
import rodar  # noqa: E402
import veredito as V  # noqa: E402

FEV_JSON = r"C:\IALD\projetos_pyhton\acom\tgl_c3_v5_results_20260209_121836.json"
LN2 = math.log(2.0)


def load_full(path):
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.append(dict(d=int(r["d"]), nc=int(r["nc"]), seed=int(r["seed"]), gi=int(r["gi"]),
                            gamma=float(r["gamma"]), O=float(r["O"]), conv=(r["conv"] == "1"),
                            cci=float(r["cci_core"]), pur=float(r["purity"]), deff=float(r["d_eff"])))
    return out


def med_by_cell(rows, key):
    cells = {}
    for r in rows:
        if r["conv"] and math.isfinite(r[key]):
            cells.setdefault((r["d"], r["nc"], r["gi"]), []).append(r[key])
    return {k: statistics.median(v) for k, v in cells.items()}


def ols_slope(x, y):
    n = len(x)
    xm = sum(x) / n
    ym = sum(y) / n
    return sum((a - xm) * (b - ym) for a, b in zip(x, y)) / sum((a - xm) ** 2 for a in x)


def main():
    ver = json.load(open(os.path.join(HERE, "veredito.json"), encoding="utf-8"))
    main_rows = load_full(os.path.join(HERE, "dados_crus_main.csv"))
    n2_rows = load_full(os.path.join(HERE, "dados_crus_N2.csv"))
    gam = [p["gamma"] for p in ver["por_gamma_main"]]
    lg = [math.log10(g) for g in gam]
    xs = [math.log(d / nc) for (d, nc, _) in rodar.CONFIGS]
    out = {}

    # ------------------------------------------------------------------ D1
    fev = json.load(open(FEV_JSON, encoding="utf-8"))["per_dim_results"]
    d1 = []
    for (d, nc, eps), fr in zip(rodar.CONFIGS, fev):
        assert fr["dim"] == d and fr["nc"] == nc
        gstar = float(fr["gamma_star"])
        Os = []
        cci42 = None
        for seed in rodar.SEEDS:
            base = rodar.build_system(d, nc, eps, seed)
            ss = rodar.steady_state_kernel(base, gstar)
            O, _ = rodar.observable_O(ss["rho"])
            Os.append((seed, O, ss["ok"]))
            if seed == 42:
                cci42 = float(np.real(np.trace(ss["rho"] @ base["Pi"])))
        o42 = [o for s, o, _ in Os if s == 42][0]
        d1.append(dict(d=d, nc=nc, gamma_star_fevereiro=gstar, log10_gamma_star=math.log10(gstar),
                       O_fevereiro_nats=fr["M7_d_folds_c3"], O_novo_semente42_nats=o42,
                       reproducao_abs_dif=abs(o42 - fr["M7_d_folds_c3"]),
                       peso_core_fevereiro=fr["CCI"], peso_core_novo_semente42=cci42,
                       O_mediana_5_sementes_nats=statistics.median(o for _, o, _ in Os),
                       O_min_nats=min(o for _, o, _ in Os), O_max_nats=max(o for _, o, _ in Os),
                       todas_convergiram=all(k for _, _, k in Os)))
    meds = [r["O_mediana_5_sementes_nats"] for r in d1]
    o42s = [r["O_novo_semente42_nats"] for r in d1]
    fevs = [r["O_fevereiro_nats"] for r in d1]
    out["D1_gamma_estrela_de_fevereiro"] = dict(
        por_config=d1,
        reproducao_maior_dif_abs=max(r["reproducao_abs_dif"] for r in d1),
        fevereiro=dict(mediana_nats=statistics.median(fevs), media_nats=sum(fevs) / 9,
                       mediana_oitavas=statistics.median(fevs) / LN2, media_oitavas=sum(fevs) / 9 / LN2,
                       inclinacao_contra_ln_d_nc=ols_slope(xs, fevs),
                       n_na_banda=sum(1 for v in fevs if abs(v - LN2) <= V.BAND), min_oitavas=min(fevs) / LN2,
                       max_oitavas=max(fevs) / LN2),
        novo_5_sementes=dict(mediana_das_medianas_nats=statistics.median(meds), media_das_medianas_nats=sum(meds) / 9,
                             mediana_oitavas=statistics.median(meds) / LN2,
                             inclinacao_contra_ln_d_nc=ols_slope(xs, meds),
                             n_na_banda=sum(1 for v in meds if abs(v - LN2) <= V.BAND),
                             min_oitavas=min(meds) / LN2, max_oitavas=max(meds) / LN2),
        log10_gamma_estrela_min=min(r["log10_gamma_star"] for r in d1),
        log10_gamma_estrela_max=max(r["log10_gamma_star"] for r in d1))

    # ------------------------------------------------------------------ D2
    mO = med_by_cell(main_rows, "O")
    mC = med_by_cell(main_rows, "cci")
    d2 = []
    for (d, nc, _) in rodar.CONFIGS:
        curva = [mO.get((d, nc, gi)) for gi in range(len(gam))]
        cruz = []
        for k in range(len(gam) - 1):
            a, b = curva[k], curva[k + 1]
            if a is None or b is None:
                continue
            if (a - LN2) * (b - LN2) < 0:
                t = (LN2 - a) / (b - a)
                lgx = lg[k] + t * (lg[k + 1] - lg[k])
                ca, cb = mC.get((d, nc, k)), mC.get((d, nc, k + 1))
                cci = None if (ca is None or cb is None) else ca + t * (cb - ca)
                cruz.append(dict(log10_gamma=lgx, sentido="desce" if b < a else "sobe", peso_core_no_cruzamento=cci))
        d2.append(dict(d=d, nc=nc, O_em_gamma_1e4_oitavas=curva[0] / LN2 if curva[0] is not None else None,
                       O_em_gamma_1_oitavas=curva[-1] / LN2 if curva[-1] is not None else None,
                       min_oitavas=min(c for c in curva if c is not None) / LN2,
                       max_oitavas=max(c for c in curva if c is not None) / LN2, cruzamentos=cruz))
    primeiros = [c["cruzamentos"][0]["log10_gamma"] for c in d2 if c["cruzamentos"]]
    out["D2_cruzamentos_com_ln2"] = dict(
        por_config=d2, n_configs_com_cruzamento=len(primeiros),
        log10_gamma_do_primeiro_cruzamento_min=min(primeiros) if primeiros else None,
        log10_gamma_do_primeiro_cruzamento_max=max(primeiros) if primeiros else None,
        dispersao_em_decadas=(max(primeiros) - min(primeiros)) if primeiros else None)

    # ------------------------------------------------------------------ D3
    refs = [0, 6, 12, 18, 24]

    def tabela(rows):
        m = med_by_cell(rows, "O")
        t = []
        for gi in refs:
            vals = [m.get((d, nc, gi)) for (d, nc, _) in rodar.CONFIGS]
            t.append(dict(gi=gi, gamma=gam[gi], oitavas_por_config=[None if v is None else v / LN2 for v in vals]))
        return t

    out["D3_curva_em_gammas_de_referencia"] = dict(configs=[[d, nc] for (d, nc, _) in rodar.CONFIGS],
                                                   main=tabela(main_rows), N2=tabela(n2_rows))
    pesos = med_by_cell(main_rows, "cci")
    out["D3_peso_do_core_mediano"] = [dict(gi=gi, gamma=gam[gi],
                                           por_config=[pesos.get((d, nc, gi)) for (d, nc, _) in rodar.CONFIGS])
                                      for gi in refs]
    out["N3_diagnostico_rotacionado"] = json.load(open(os.path.join(HERE, "controle_N3.json"),
                                                       encoding="utf-8"))["diagnostico_rotacionado_nao_entra_no_veredito"]

    with open(os.path.join(HERE, "descritivo.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=True)

    # ------------------------------------------------------------------ markdown
    L = []
    L.append("# Descritivo pos-veredito (nao entra no veredito)\n")
    L.append("## D1. O no gamma* de fevereiro (instrumento pinado, 5 sementes)\n")
    L.append("| d | nc | gamma* | O fev (nats) | O novo s42 | dif | O med 5 sem (oit) | min-max (oit) | peso core fev | peso core novo |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in d1:
        L.append("| %d | %d | %.5f | %.6f | %.6f | %.1e | %.4f | %.3f-%.3f | %.6f | %.6f |" %
                 (r["d"], r["nc"], r["gamma_star_fevereiro"], r["O_fevereiro_nats"], r["O_novo_semente42_nats"],
                  r["reproducao_abs_dif"], r["O_mediana_5_sementes_nats"] / LN2, r["O_min_nats"] / LN2,
                  r["O_max_nats"] / LN2, r["peso_core_fevereiro"], r["peso_core_novo_semente42"]))
    D1 = out["D1_gamma_estrela_de_fevereiro"]
    L.append("\nfevereiro: mediana %.4f nats (%.4f oit), media %.4f nats (%.4f oit); inclinacao contra ln(d/nc) = %+.4f; "
             "%d de 9 na banda ln2+-0,05; min-max %.3f-%.3f oit" %
             (D1["fevereiro"]["mediana_nats"], D1["fevereiro"]["mediana_oitavas"], D1["fevereiro"]["media_nats"],
              D1["fevereiro"]["media_oitavas"], D1["fevereiro"]["inclinacao_contra_ln_d_nc"],
              D1["fevereiro"]["n_na_banda"], D1["fevereiro"]["min_oitavas"], D1["fevereiro"]["max_oitavas"]))
    L.append("novo (mediana de 5 sementes por config): mediana %.4f oit; inclinacao %+.4f; %d de 9 na banda; min-max %.3f-%.3f oit" %
             (D1["novo_5_sementes"]["mediana_oitavas"], D1["novo_5_sementes"]["inclinacao_contra_ln_d_nc"],
              D1["novo_5_sementes"]["n_na_banda"], D1["novo_5_sementes"]["min_oitavas"],
              D1["novo_5_sementes"]["max_oitavas"]))
    L.append("reproducao de fevereiro (semente 42): maior |dif| = %.3e" % D1["reproducao_maior_dif_abs"])
    L.append("log10 gamma* de fevereiro: de %.3f a %.3f\n" % (D1["log10_gamma_estrela_min"], D1["log10_gamma_estrela_max"]))

    L.append("## D2. Cruzamentos da mediana com ln 2\n")
    L.append("| d | nc | O(1e-4) oit | O(1) oit | min-max oit | cruzamentos: log10 gamma (sentido; peso core) |")
    L.append("|---|---|---|---|---|---|")
    for c in d2:
        cz = "; ".join("%.3f (%s; %s)" % (x["log10_gamma"], x["sentido"],
                                        "-" if x["peso_core_no_cruzamento"] is None else "%.4f" % x["peso_core_no_cruzamento"])
                       for x in c["cruzamentos"]) or "nenhum"
        L.append("| %d | %d | %.3f | %.3f | %.3f-%.3f | %s |" % (c["d"], c["nc"], c["O_em_gamma_1e4_oitavas"],
                                                                 c["O_em_gamma_1_oitavas"], c["min_oitavas"],
                                                                 c["max_oitavas"], cz))
    D2 = out["D2_cruzamentos_com_ln2"]
    if D2["n_configs_com_cruzamento"]:
        L.append("\nprimeiro cruzamento: %d de 9 configs; log10 gamma de %.3f a %.3f (dispersao %.3f decadas)\n" %
                 (D2["n_configs_com_cruzamento"], D2["log10_gamma_do_primeiro_cruzamento_min"],
                  D2["log10_gamma_do_primeiro_cruzamento_max"], D2["dispersao_em_decadas"]))

    L.append("## D3. Mediana de O em oitavas (O/ln 2) nos gammas de referencia; colunas = 9 configs\n")
    cab = " | ".join("%d,%d" % (d, nc) for (d, nc, _) in rodar.CONFIGS)
    for nome in ("main", "N2"):
        L.append("**%s**\n" % nome)
        L.append("| gamma | %s |" % cab)
        L.append("|---|" + "---|" * 9)
        for t in out["D3_curva_em_gammas_de_referencia"][nome]:
            L.append("| %.0e | %s |" % (t["gamma"], " | ".join("-" if v is None else "%.3f" % v for v in t["oitavas_por_config"])))
        L.append("")
    L.append("**peso do core (mediana) na grade principal**\n")
    L.append("| gamma | %s |" % cab)
    L.append("|---|" + "---|" * 9)
    for t in out["D3_peso_do_core_mediano"]:
        L.append("| %.0e | %s |" % (t["gamma"], " | ".join("-" if v is None else "%.4f" % v for v in t["por_config"])))
    rot = out["N3_diagnostico_rotacionado"]
    L.append("\nN3 rotacionado (piso de ruido do instrumento; diagnostico): maior erro = %.3e" % max(r["erro_abs"] for r in rot))
    with open(os.path.join(HERE, "descritivo.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
