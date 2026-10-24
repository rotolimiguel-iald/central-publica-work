#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_figures.py — ESTAGIO D1. Imagens da forma funcional manifesta (PNG).

Gera, a partir dos MANIFESTOS REAIS da rodada (dashboard/data/latest.json +
history.jsonl — nada e' desenhado de imaginacao, tudo vem dos dados rodados):

  fig1_topologia.png    grafo satelites x bases com as transferencias reais
  fig2_pipeline.png     o duplo trilho ponta-a-ponta (estagios do pipeline)
  fig3_metricas.png     curvas das metricas por rodada (historico)
  fig4_enderecos.png    mapa angular Psi-NET (enderecos theta reais dos nos)

Uso:  python visuals/make_figures.py     (da raiz; requer uma rodada previa)
Marca d'agua obrigatoria: PILOTO DE SOFTWARE — sem veredito fisico.
"""

import json
import math
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
from skygrid_sim.psi_net import AngularAddress      # noqa: E402
from skygrid_sim import tgl_core                    # noqa: E402

DATA = os.path.join(ROOT, "dashboard", "data")
OUT = os.path.join(ROOT, "visuals", "out")

BG = "#0b1020"; PANEL = "#121a33"; INK = "#e8ecf8"; DIM = "#8fa0c8"
OK = "#3ddc84"; BAD = "#ff5d6c"; ACC = "#5aa2ff"; GOLD = "#e8c35a"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": INK, "axes.edgecolor": DIM, "axes.labelcolor": DIM,
    "xtick.color": DIM, "ytick.color": DIM, "font.size": 10,
    "font.family": "DejaVu Sans"})

DISCLAIMER = ("PILOTO DE SOFTWARE — simulacao da arquitetura "
              "(physical_verdict_allowed=False); nao e' alegacao de energia")


def _load():
    with open(os.path.join(DATA, "latest.json"), encoding="utf-8") as f:
        latest = json.load(f)
    hist = []
    hp = os.path.join(DATA, "history.jsonl")
    if os.path.isfile(hp):
        with open(hp, encoding="utf-8") as f:
            hist = [json.loads(l) for l in f if l.strip()]
    return latest, hist


def _stamp(fig, title):
    fig.suptitle(title, fontsize=14, fontweight="bold", color=INK, y=0.985)
    fig.text(0.5, 0.012, DISCLAIMER, ha="center", fontsize=7.5, color=GOLD)


def fig1_topologia(latest):
    rep, tr = latest["report"], latest["transfers"]
    n_s, n_b = rep["n_sats"], rep["n_bases"]
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_aspect("equal"); ax.axis("off")

    # Earth + orbital ring
    th = np.linspace(0, 2 * np.pi, 200)
    ax.fill(2.1 * np.cos(th), 2.1 * np.sin(th), color="#12305e", alpha=.9, zorder=1)
    ax.plot(2.1 * np.cos(th), 2.1 * np.sin(th), color=ACC, lw=.8, alpha=.6)
    ax.text(0, 0, "TERRA", ha="center", va="center", color=DIM, fontsize=9)

    sat_pos, base_pos = {}, {}
    for i in range(n_s):
        a = 2 * np.pi * i / n_s
        sat_pos["SAT-%03d" % i] = (4.6 * np.cos(a), 4.6 * np.sin(a))
    for i in range(n_b):
        a = 2 * np.pi * (i + .5) / n_b
        base_pos["BASE-%04d" % i] = (2.1 * np.cos(a), 2.1 * np.sin(a))

    for rec in tr:
        p1 = sat_pos.get(rec["from"]); p2 = base_pos.get(rec["to"])
        if not p1 or not p2:
            continue
        if rec.get("placebo"):
            color, ls, lw = BAD, ":", 1.6
        elif rec.get("accepted"):
            color, ls, lw = OK, "-", 1.1
        else:
            color, ls, lw = BAD, "--", 1.4
        ax.annotate("", xy=p2, xytext=p1, zorder=2,
                    arrowprops=dict(arrowstyle="-|>", color=color, ls=ls,
                                    lw=lw, alpha=.85, shrinkA=8, shrinkB=8))
    for nid, (x, y) in sat_pos.items():
        ax.scatter(x, y, s=90, marker="^", color=ACC, edgecolor=INK,
                   linewidth=.5, zorder=3)
        if n_s <= 24:
            ax.annotate(nid.replace("SAT-0", "S"), (x, y),
                        textcoords="offset points", xytext=(0, 9),
                        ha="center", fontsize=7, color=DIM)
    for nid, (x, y) in base_pos.items():
        ax.scatter(x, y, s=70, marker="s", color=GOLD, edgecolor=INK,
                   linewidth=.5, zorder=3)

    m = rep["metrics"]
    ax.text(0, -5.6,
            "veredito: %s   |   %d/%d aceitas   |   placebo rejeitado: %s   |   "
            "quorum %d validadores   |   beta=%.12f (runtime)"
            % (rep["verdict"], rep["transfers_healthy_accepted"],
               rep["transfers_healthy_total"], rep["placebo_rejected"],
               rep["quorum"]["n_validators"], rep["beta_runtime"]),
            ha="center", fontsize=8.5, color=INK)
    handles = [plt.Line2D([], [], color=OK, lw=2, label="transferencia aceita"),
               plt.Line2D([], [], color=BAD, ls="--", lw=2, label="rejeitada (falha detectada)"),
               plt.Line2D([], [], color=BAD, ls=":", lw=2, label="placebo (rejeitado)"),
               plt.Line2D([], [], marker="^", color=ACC, lw=0, label="ExtractorSat (no 100)"),
               plt.Line2D([], [], marker="s", color=GOLD, lw=0, label="GroundBase (no 200)")]
    ax.legend(handles=handles, loc="upper left", fontsize=7.5,
              facecolor=PANEL, edgecolor=DIM, labelcolor=INK)
    ax.set_xlim(-6.4, 6.4); ax.set_ylim(-6.2, 6.0)
    _stamp(fig, "SkyGrid — topologia do grafo (%d satelites x %d bases) — rodada real %s"
           % (n_s, n_b, rep["timestamp"]))
    fig.savefig(os.path.join(OUT, "fig1_topologia.png"), dpi=160,
                bbox_inches="tight")
    plt.close(fig)


def fig2_pipeline(latest):
    rep = latest["report"]
    m = rep["metrics"]
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    ax.axis("off")

    stages = [
        ("TELEMETRIA\n%s" % rep["telemetry_provenance"]["marker"], ACC),
        ("ACOM CRYPTO\n3 shares\nfail-closed", GOLD),
        ("TGL TENSOR\nVerb Floor 1-β\n%.1fx" % m["mean_compression_ratio"], ACC),
        ("Ψ-NET\nendereço angular\n+ hops", GOLD),
        ("DUPLO TRILHO\nΨ×E corr\n%.5f" % m["mean_rail_corr"], OK),
        ("QUÓRUM PoP\n%d validadores\n≥67%%" % rep["quorum"]["n_validators"], GOLD),
        ("CÉLULA REV.\nretenção\n%.4f" % m["mean_retention"], ACC),
        ("BASE\ndistribuição\n[PILOTO]", OK),
    ]
    n = len(stages)
    w, h, y0 = 1.25, 1.15, 2.2
    xs = np.linspace(0.8, 12.1 - w, n)
    for (label, col), x in zip(stages, xs):
        ax.add_patch(FancyBboxPatch((x, y0), w, h, boxstyle="round,pad=0.06",
                                    fc=PANEL, ec=col, lw=1.6))
        ax.text(x + w / 2, y0 + h / 2, label, ha="center", va="center",
                fontsize=7.6, color=INK)
        if x != xs[-1]:
            ax.add_patch(FancyArrowPatch((x + w + .02, y0 + h / 2),
                                         (x + (xs[1] - xs[0]) - .02, y0 + h / 2),
                                         arrowstyle="-|>", mutation_scale=13,
                                         color=DIM))
    # the two rails split & rejoin around the double-rail box
    xm = xs[4] + w / 2
    ax.annotate("Trilha-Ψ (portadora holográfica REFLECT→MANIFEST)",
                xy=(xm, y0 + h + .55), ha="center", fontsize=8, color=ACC)
    ax.annotate("Trilha-E (serialização convencional de bytes)",
                xy=(xm, y0 - .55), ha="center", fontsize=8, color=GOLD)
    ax.add_patch(FancyArrowPatch((xs[3] + w, y0 + h), (xs[4] + w / 2, y0 + h + .4),
                                 arrowstyle="-|>", mutation_scale=11, color=ACC,
                                 connectionstyle="arc3,rad=.25"))
    ax.add_patch(FancyArrowPatch((xs[3] + w, y0), (xs[4] + w / 2, y0 - .4),
                                 arrowstyle="-|>", mutation_scale=11, color=GOLD,
                                 connectionstyle="arc3,rad=-.25"))
    ax.add_patch(FancyArrowPatch((xs[4] + w / 2, y0 + h + .4), (xs[5], y0 + h),
                                 arrowstyle="-|>", mutation_scale=11, color=ACC,
                                 connectionstyle="arc3,rad=.25"))
    ax.add_patch(FancyArrowPatch((xs[4] + w / 2, y0 - .4), (xs[5], y0),
                                 arrowstyle="-|>", mutation_scale=11, color=GOLD,
                                 connectionstyle="arc3,rad=-.25"))

    ax.text(6.4, 0.62, "aceita SOMENTE se: corr(Ψ,E) > 0.999  E  bloco de fase sela no quórum "
            "— placebo (sem acoplamento β) rejeitado por construção",
            ha="center", fontsize=8.5, color=INK)
    ax.text(6.4, 4.4, "controle IALD/GKSL: orçamento ⌈100/β⌉ = %d passos · kernel %s · "
            "memória psiônica sessão #%d"
            % (rep["iald_control"]["budget_steps_100_over_beta"],
               rep["kernel_provenance"]["kernel"], rep["memory"]["sessions"]),
            ha="center", fontsize=8.5, color=DIM)
    ax.set_xlim(0, 12.8); ax.set_ylim(0, 5.0)
    _stamp(fig, "SkyGrid — pipeline ponta-a-ponta com validação por duplo trilho")
    fig.savefig(os.path.join(OUT, "fig2_pipeline.png"), dpi=160,
                bbox_inches="tight")
    plt.close(fig)


def fig3_metricas(hist):
    if not hist:
        return
    fig, axes = plt.subplots(2, 2, figsize=(12, 7))
    xs = np.arange(1, len(hist) + 1)

    def series(key):
        return np.array([h.get(key, np.nan) for h in hist], dtype=float)

    a = axes[0, 0]
    a.plot(xs, series("acceptance") * 100, "-o", color=OK, ms=4)
    a.set_title("aceitação (%)", color=INK); a.set_ylim(-5, 105)
    a = axes[0, 1]
    a.plot(xs, series("mean_rail_corr"), "-o", color=ACC, ms=4)
    a.set_title("correlação do duplo trilho Ψ×E", color=INK)
    a = axes[1, 0]
    a.plot(xs, series("compression"), "-o", color=GOLD, ms=4, label="compressão (×)")
    a.plot(xs, series("retention"), "-s", color=OK, ms=4, label="retenção")
    a.legend(fontsize=8, facecolor=PANEL, edgecolor=DIM, labelcolor=INK)
    a.set_title("compressão TGL e retenção da célula", color=INK)
    a = axes[1, 1]
    a.plot(xs, series("throughput_Bps") / 1e6, "-o", color=BAD, ms=4)
    a.set_title("throughput (MB/s, simulação)", color=INK)
    for a in axes.ravel():
        a.grid(color="#1e2a4d", lw=.6); a.set_xlabel("rodada")
    verd = ["ARCHITECTURE_CLOSES" == h.get("verdict") for h in hist]
    _stamp(fig, "SkyGrid — métricas por rodada (histórico real; %d/%d rodadas fecham)"
           % (sum(verd), len(verd)))
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(os.path.join(OUT, "fig3_metricas.png"), dpi=160)
    plt.close(fig)


def fig4_enderecos(latest):
    rep = latest["report"]
    n_s, n_b = rep["n_sats"], rep["n_bases"]
    theta_m = tgl_core.theta_m()
    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={"projection": "polar"})
    ax.set_facecolor(BG)

    ths, thb = [], []
    for i in range(n_s):
        ths.append(AngularAddress.from_key(("SAT-%03d" % i).encode()).theta)
    for i in range(n_b):
        thb.append(AngularAddress.from_key(("BASE-%04d" % i).encode()).theta)
    ax.scatter(ths, [1.0] * len(ths), s=80, marker="^", color=ACC,
               label="satélites (θ real do endereço)", zorder=3)
    ax.scatter(thb, [0.62] * len(thb), s=60, marker="s", color=GOLD,
               label="bases", zorder=3)
    # theta_M sector wedge (hop quantum)
    ax.bar(theta_m / 2, 0.18, width=theta_m, bottom=1.12, color=OK, alpha=.75)
    ax.text(theta_m / 2, 1.42, "θ_M = %.4f rad (%.3f°)\n1 hop angular"
            % (theta_m, math.degrees(theta_m)), ha="center", fontsize=8,
            color=OK)
    ax.set_rticks([]); ax.set_rlim(0, 1.5)
    ax.grid(color="#1e2a4d", lw=.5)
    ax.legend(loc="lower left", bbox_to_anchor=(-.08, -.12), fontsize=8,
              facecolor=PANEL, edgecolor=DIM, labelcolor=INK)
    _stamp(fig, "SkyGrid — endereçamento angular Ψ-NET (θ = SHA-256 da chave, hop = θ_M)")
    fig.savefig(os.path.join(OUT, "fig4_enderecos.png"), dpi=160,
                bbox_inches="tight")
    plt.close(fig)


def main():
    os.makedirs(OUT, exist_ok=True)
    latest, hist = _load()
    fig1_topologia(latest)
    fig2_pipeline(latest)
    fig3_metricas(hist)
    fig4_enderecos(latest)
    print("figuras geradas em", OUT)
    for f in sorted(os.listdir(OUT)):
        print("  ", f)


if __name__ == "__main__":
    main()
