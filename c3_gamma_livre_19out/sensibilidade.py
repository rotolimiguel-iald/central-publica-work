#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SENSIBILIDADE POS-VEREDITO (descritivo; nao muda o veredito pre-registrado).
Mede QUAO LONGE o piso de uma oitava ficou de valer:
  S1  por semente isolada: o maior numero de configs (de 9) na banda ln 2 +- 0,05 em algum gamma;
  S2  a menor meia-largura de banda h (nats) para a qual existiria uma janela de >= 7 pontos (1 decada) com as 9
      medianas dentro de ln 2 +- h, sem e com a condicao de inclinacao < 0,05;
  S3  a queda de O (oitavas) por decada de gamma ao redor do cruzamento com ln 2.
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
import veredito as V  # noqa: E402

LN2 = math.log(2.0)


def main():
    rows = V.load_rows(os.path.join(HERE, "dados_crus_main.csv"))
    gam = V.check_complete(rows, "main")
    lg = [math.log10(g) for g in gam]
    xs = [math.log(d / nc) for (d, nc) in V.CONFIGS]
    out = {}

    # S1: semente isolada
    s1 = {}
    for s in V.SEEDS:
        best, at = 0, None
        for gi in range(len(gam)):
            n = 0
            for (d, nc) in V.CONFIGS:
                v = [r["O"] for r in rows if r["seed"] == s and r["d"] == d and r["nc"] == nc and r["gi"] == gi][0]
                n += abs(v - LN2) <= V.BAND
            if n > best:
                best, at = n, lg[gi]
        s1[str(s)] = dict(max_configs_na_banda=best, log10_gamma_do_maximo=at)
    out["S1_semente_isolada"] = s1

    # medianas por celula
    cells = {}
    for r in rows:
        cells.setdefault((r["d"], r["nc"], r["gi"]), []).append(r["O"])
    med = {k: statistics.median(v) for k, v in cells.items()}
    dev, slope_ok = [], []
    for gi in range(len(gam)):
        ms = [med[(d, nc, gi)] for (d, nc) in V.CONFIGS]
        dev.append(max(abs(m - LN2) for m in ms))
        slope_ok.append(abs(V.ols_slope(xs, ms)) < V.SLOPE_MAX)

    def menor_meia_largura(exigir_inclinacao):
        melhor, onde = None, None
        for i in range(0, len(gam) - 6):
            j = i + 6
            if exigir_inclinacao and not all(slope_ok[i:j + 1]):
                continue
            h = max(dev[i:j + 1])
            if melhor is None or h < melhor:
                melhor, onde = h, (lg[i], lg[j])
        return melhor, onde

    h0, w0 = menor_meia_largura(False)
    h1, w1 = menor_meia_largura(True)
    out["S2_menor_meia_largura_para_uma_janela_de_1_decada"] = dict(
        sem_condicao_de_inclinacao=dict(h_nats=h0, h_oitavas=h0 / LN2, janela_log10_gamma=w0),
        com_condicao_de_inclinacao=dict(h_nats=h1, h_oitavas=h1 / LN2, janela_log10_gamma=w1) if h1 is not None else None,
        banda_pre_registrada_nats=V.BAND)
    out["S2_desvio_maximo_entre_as_9_configs_por_gamma_nats"] = [dict(log10_gamma=lg[i], desvio_max_nats=dev[i],
                                                                     inclinacao_ok=slope_ok[i]) for i in range(len(gam))]

    # S3: queda por decada ao redor do cruzamento (media das 9 configs, oitavas por decada)
    quedas = []
    for gi in range(len(gam) - 1):
        q = []
        for (d, nc) in V.CONFIGS:
            a, b = med[(d, nc, gi)] / LN2, med[(d, nc, gi + 1)] / LN2
            q.append((b - a) / (lg[gi + 1] - lg[gi]))
        quedas.append(dict(log10_gamma_medio=(lg[gi] + lg[gi + 1]) / 2, oitavas_por_decada_media=sum(q) / len(q),
                           min=min(q), max=max(q)))
    out["S3_inclinacao_de_O_contra_log10_gamma_oitavas_por_decada"] = quedas
    alvo = [q for q in quedas if -2.6 <= q["log10_gamma_medio"] <= -2.0]
    out["S3_resumo_perto_do_cruzamento"] = dict(
        faixa_log10_gamma=[-2.6, -2.0], oitavas_por_decada_media=sum(q["oitavas_por_decada_media"] for q in alvo) / len(alvo),
        min=min(q["min"] for q in alvo), max=max(q["max"] for q in alvo))

    with open(os.path.join(HERE, "sensibilidade.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=True)
    print("S1 (semente isolada: maior numero de configs na banda em algum gamma):")
    for s, v in s1.items():
        print("  semente %s: %d de 9 (log10 gamma = %.3f)" % (s, v["max_configs_na_banda"], v["log10_gamma_do_maximo"]))
    print("S2 menor meia-largura de banda para uma janela de 1 decada com as 9 configs dentro:")
    print("  sem condicao de inclinacao: h = %.4f nats (%.3f oit), janela log10 gamma %s" % (h0, h0 / LN2, w0))
    if h1 is not None:
        print("  com inclinacao < 0,05:      h = %.4f nats (%.3f oit), janela log10 gamma %s" % (h1, h1 / LN2, w1))
    else:
        print("  com inclinacao < 0,05: nenhuma janela de 1 decada")
    print("  (banda pre-registrada: 0,05 nats = %.3f oit)" % (V.BAND / LN2))
    r = out["S3_resumo_perto_do_cruzamento"]
    print("S3 perto do cruzamento (log10 gamma de -2,6 a -2,0): O cai %.3f oit por decada (min %.3f, max %.3f entre configs)"
          % (r["oitavas_por_decada_media"], r["min"], r["max"]))


if __name__ == "__main__":
    main()
