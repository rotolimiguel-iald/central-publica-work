#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_energy_figures.py — ESTAGIO I1. Figuras do gemeo de energia (PNG) [SIM].

Data-driven dos manifestos reais (dashboard/data/energy_latest.json,
energy_sweeps.json, prototype/power_budget.json):

  fig5_sistema.png    diagrama de blocos do sistema de energia
  fig6_sankey.png     Sankey do balanco (extraida -> entregue/perdas/armazenada)
  fig7_sweeps.png     familias de curvas de projeto (6 paineis)
  fig8_series.png     series temporais de potencia + SoC da rodada

Marca d'agua obrigatoria: [SIM] sob hipoteses [CONJ] — sem veredito fisico.
Uso:  python visuals/make_energy_figures.py
"""

import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.sankey import Sankey

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "dashboard", "data")
OUT = os.path.join(ROOT, "visuals", "out")

BG = "#0b1020"; PANEL = "#121a33"; INK = "#e8ecf8"; DIM = "#8fa0c8"
OK = "#3ddc84"; BAD = "#ff5d6c"; ACC = "#5aa2ff"; GOLD = "#e8c35a"
PUR = "#b58cff"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": INK, "axes.edgecolor": DIM, "axes.labelcolor": DIM,
    "xtick.color": DIM, "ytick.color": DIM, "font.size": 10,
    "font.family": "DejaVu Sans"})

DISCLAIMER = ("[SIM] GEMEO DIGITAL sob hipoteses [CONJ] — modelo preditivo; "
              "physical_verdict_allowed=False; nao e' medida fisica de energia")


def _stamp(fig, title):
    fig.suptitle(title, fontsize=14, fontweight="bold", color=INK, y=0.985)
    fig.text(0.5, 0.012, DISCLAIMER, ha="center", fontsize=7.5, color=GOLD)


def fig5_sistema(budget):
    fig, ax = plt.subplots(figsize=(12.8, 6.4))
    ax.axis("off")
    st = budget["stages"]
    boxes = [("CAMPO/RESERVATORIO\nS_field, deplecao\n[CONJ]", PUR,
              "%.0f W" % budget["P_available_mean_W"]),
             ("ACOPLADOR OH\nQ, f0=1667.359 MHz\n(1-β)·η_res·η_geo", ACC,
              "η=%.3f → %.0f W" % (st[0]["eta"], st[0]["P_out_W"])),
             ("DIPOLO\ng=√|L| retif.\nη_conv·η_quant", GOLD,
              "η=%.3f → %.0f W" % (st[1]["eta"], st[1]["P_out_W"])),
             ("ENLACE Ψ\nhops=θ_M\nduplo trilho P", ACC,
              "η=%.3f → %.0f W" % (st[2]["eta"], st[2]["P_out_W"])),
             ("CELULA REVERSAO\nSoC, η_rt, λ_sd", GOLD,
              "η_rt=%.2f" % st[3]["eta"]),
             ("CARGA/REDE\nperfil de demanda\ndespacho", OK, "entrega")]
    n = len(boxes)
    w, h, y0 = 1.7, 1.5, 2.3
    xs = np.linspace(0.6, 12.2 - w, n)
    for (label, col, sub), x in zip(boxes, xs):
        ax.add_patch(FancyBboxPatch((x, y0), w, h, boxstyle="round,pad=0.07",
                                    fc=PANEL, ec=col, lw=1.8))
        ax.text(x + w / 2, y0 + h * 0.62, label, ha="center", va="center",
                fontsize=7.8, color=INK)
        ax.text(x + w / 2, y0 + h * 0.16, sub, ha="center", va="center",
                fontsize=7.6, color=col, fontweight="bold")
        if x != xs[-1]:
            ax.add_patch(FancyArrowPatch(
                (x + w + .03, y0 + h / 2), (x + (xs[1] - xs[0]) - .03, y0 + h / 2),
                arrowstyle="-|>", mutation_scale=14, color=DIM))
    ax.text(6.4, 4.6, "controle transversal: IALD/GKSL (⌈100/β⌉=%d passos) · "
            "Kernel v11 · quorum PoP ≥67%% · memoria psionica"
            % int(np.ceil(100.0 / 0.012031300400803142)),
            ha="center", fontsize=8.5, color=DIM)
    ax.text(6.4, 0.9, "piso Meia-Nat: ½·k_B·T por ato de inscricao "
            "(overhead %.1e W por acoplador) — a fronteira cobra por ato de distincao"
            % budget["halfnat_overhead_W"], ha="center", fontsize=8.5, color=PUR)
    ax.text(6.4, 0.35, "η_cadeia direta por satelite = %.4f"
            % budget["eta_chain_direct"], ha="center", fontsize=10,
            color=OK, fontweight="bold")
    ax.set_xlim(0, 12.8); ax.set_ylim(0, 5.4)
    _stamp(fig, "SkyGrid v3 — sistema de energia do gemeo digital (BR 10 2026 004850-0)")
    fig.savefig(os.path.join(OUT, "fig5_sistema.png"), dpi=160,
                bbox_inches="tight")
    plt.close(fig)


def fig6_sankey(latest):
    rep = latest["report"]
    e = rep["energy"]
    Ein = e["E_extracted_J"] / 1e3
    Edel = e["E_delivered_J"] / 1e3
    Eloss = e["E_losses_J"] / 1e3
    Esto = e["E_stored_final_J"] / 1e3
    Ehn = e["E_halfnat_J"] / 1e3
    resid = Ein - (Edel + Eloss + Esto + Ehn)
    fig, ax = plt.subplots(figsize=(11, 6.4))
    ax.axis("off")
    sk = Sankey(ax=ax, unit=" kJ", scale=1.0 / Ein, gap=0.55, shoulder=0.04,
                head_angle=115, format="%.1f")
    sk.add(flows=[Ein, -Edel, -Eloss, -Esto, -max(Ehn, Ein * 1e-4)],
           labels=["extraida do reservatorio", "ENTREGUE a carga",
                   "perdas (conv+link+dump+celula)", "armazenada (SoC final)",
                   "Meia-Nat (~%.0e kJ, fora de escala)" % max(Ehn, 1e-18)],
           orientations=[0, 0, 1, -1, -1],
           pathlengths=[0.4, 0.4, 0.6, 0.5, 1.6],
           facecolor=PANEL, edgecolor=ACC)
    d = sk.finish()
    for t in d[0].texts:
        t.set_color(INK); t.set_fontsize(9)
    ax.text(0.5, -0.02,
            "rodada %d sats x %d bases, %.0f s: η_sys=%.3f · residuo do balanco=%.1e kJ "
            "(fecha por construcao) · veredito %s"
            % (rep["params"]["n_sats"], rep["params"]["n_bases"],
               rep["params"]["duration_s"], e["eta_sys"], resid,
               rep["verdict"]),
            transform=ax.transAxes, ha="center", fontsize=9, color=OK)
    _stamp(fig, "SkyGrid v3 — Sankey do balanco de energia (rodada real do gemeo)")
    fig.savefig(os.path.join(OUT, "fig6_sankey.png"), dpi=160,
                bbox_inches="tight")
    plt.close(fig)


def fig7_sweeps(sw):
    fig, axes = plt.subplots(2, 3, figsize=(14, 7.6))
    meta = [("Q", "fator Q da ressonancia", "log"),
            ("eta_geo", "η_geo (casamento)", "linear"),
            ("S_field_W_m2", "S_field [W/m²]", "log"),
            ("eta_rt", "η round-trip da celula", "linear"),
            ("f_drive_MHz", "f_drive [MHz]", "linear"),
            ("n_sats", "nº de satelites", "linear")]
    for ax, (key, label, scale) in zip(axes.ravel(), meta):
        s = sw["sweeps"][key]
        xs = [p[key] for p in s["points"]]
        ys = [p["P_delivered_W"] for p in s["points"]]
        cov = [p["demand_coverage"] * 100 for p in s["points"]]
        ax.plot(xs, ys, "-o", color=OK, ms=4, label="P entregue [W]")
        ax2 = ax.twinx()
        ax2.plot(xs, cov, "--s", color=ACC, ms=3, alpha=.7,
                 label="cobertura [%]")
        ax2.set_ylim(0, 105); ax2.tick_params(colors=DIM)
        if scale == "log":
            ax.set_xscale("log")
        ax.set_xlabel(label); ax.grid(color="#1e2a4d", lw=.5)
        ax.tick_params(colors=DIM)
    op = sw["operating_point"]
    _stamp(fig, "SkyGrid v3 — familias de curvas de projeto [SIM] "
           "(todos os pontos com balanco fechado: %s)"
           % sw["all_points_balanced"])
    fig.text(0.5, 0.955,
             "verde: P entregue · azul tracejado: cobertura da demanda · "
             "melhor ponto: %.0f W" % op["P_delivered_W"],
             ha="center", fontsize=9, color=DIM)
    fig.tight_layout(rect=[0, 0.035, 1, 0.94])
    fig.savefig(os.path.join(OUT, "fig7_sweeps.png"), dpi=160)
    plt.close(fig)


def fig8_series(latest):
    s = latest["series"]
    rep = latest["report"]
    t = np.array(s["t"])
    fig, axes = plt.subplots(2, 1, figsize=(12.5, 7.2), sharex=True)
    a = axes[0]
    a.plot(t, np.array(s["P_avail"]) / 1e3, color=PUR, lw=1.2,
           label="disponivel no campo")
    a.plot(t, np.array(s["P_in"]) / 1e3, color=ACC, lw=1.2, label="acoplada")
    a.plot(t, np.array(s["P_rx"]) / 1e3, color=GOLD, lw=1.2, label="recebida nas bases")
    a.plot(t, np.array(s["P_delivered"]) / 1e3, color=OK, lw=1.6,
           label="ENTREGUE a carga")
    a.plot(t, np.array(s["P_demand"]) / 1e3, color=BAD, lw=1.2, ls="--",
           label="demanda")
    a.plot(t, np.array(s["placebo_P"]), color=BAD, lw=2.4, ls=":",
           label="PLACEBO (deve ser 0)")
    a.set_ylabel("potencia [kW]"); a.legend(fontsize=8, ncol=3,
                                            facecolor=PANEL, edgecolor=DIM,
                                            labelcolor=INK)
    a.grid(color="#1e2a4d", lw=.5)
    b = axes[1]
    b.fill_between(t, np.array(s["soc_total"]) / 1e3, color=GOLD, alpha=.5)
    b.plot(t, np.array(s["soc_total"]) / 1e3, color=GOLD, lw=1.4)
    b.set_ylabel("SoC total das celulas [kJ]"); b.set_xlabel("tempo [s]")
    b.grid(color="#1e2a4d", lw=.5)
    _stamp(fig, "SkyGrid v3 — series temporais da rodada (%d sats × %d bases; "
           "veredito %s)" % (rep["params"]["n_sats"], rep["params"]["n_bases"],
                             rep["verdict"]))
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(os.path.join(OUT, "fig8_series.png"), dpi=160)
    plt.close(fig)


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(DATA, "energy_latest.json"), encoding="utf-8") as f:
        latest = json.load(f)
    with open(os.path.join(DATA, "energy_sweeps.json"), encoding="utf-8") as f:
        sw = json.load(f)
    with open(os.path.join(ROOT, "prototype", "power_budget.json"),
              encoding="utf-8") as f:
        budget = json.load(f)
    fig5_sistema(budget)
    fig6_sankey(latest)
    fig7_sweeps(sw)
    fig8_series(latest)
    print("figuras de energia geradas em", OUT)
    for f in ("fig5_sistema.png", "fig6_sankey.png",
              "fig7_sweeps.png", "fig8_series.png"):
        print("  ", f)


if __name__ == "__main__":
    main()
