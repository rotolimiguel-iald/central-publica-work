#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_energy_video.py — ESTAGIO I3. O fluxo de ENERGIA animado (MP4) [SIM].

Anima a rodada REAL do gemeo (dashboard/data/energy_latest.json): feixes com
espessura proporcional a potencia instantanea, contadores de energia
integrando ao vivo, SoC das celulas enchendo, placebo cravado em 0 W, e o
cartao final com o balanco (extraida = entregue + perdas + armazenada + meia-nat)
e o veredito MODEL_CLOSES.

Uso:  python visuals/make_energy_video.py [--out visuals/out/skygrid_energy.mp4]
1280x720, 30 fps. Marca d'agua: [SIM] sob hipoteses [CONJ]; sem veredito fisico.
"""

import argparse
import json
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "dashboard", "data")
OUT_DIR = os.path.join(ROOT, "visuals", "out")

BG = "#0b1020"; INK = "#e8ecf8"; DIM = "#8fa0c8"
OK = "#3ddc84"; BAD = "#ff5d6c"; ACC = "#5aa2ff"; GOLD = "#e8c35a"; PUR = "#b58cff"
FPS = 30

plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG,
                     "savefig.facecolor": BG, "text.color": INK,
                     "font.family": "DejaVu Sans"})

DISCLAIMER = ("[SIM] GEMEO DIGITAL sob hipoteses [CONJ] — modelo preditivo; "
              "physical_verdict_allowed=False; nao e' medida fisica de energia")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(OUT_DIR, "skygrid_energy.mp4"))
    args = ap.parse_args()

    with open(os.path.join(DATA, "energy_latest.json"), encoding="utf-8") as f:
        latest = json.load(f)
    rep, s = latest["report"], latest["series"]
    n_s, n_b = rep["params"]["n_sats"], rep["params"]["n_bases"]
    e = rep["energy"]
    T = np.array(s["t"]); N = len(T)
    P_rx = np.array(s["P_rx"]); P_del = np.array(s["P_delivered"])
    P_dem = np.array(s["P_demand"]); soc = np.array(s["soc_total"])
    P_in = np.array(s["P_in"]); dt = T[1] - T[0] if N > 1 else 1.0
    Pmax = max(P_rx.max(), 1e-9)
    soc_max = max(soc.max(), 1e-9)

    intro_f, flow_f, end_f = 3 * FPS, 14 * FPS, 5 * FPS
    total = intro_f + flow_f + end_f

    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
    th = np.linspace(0, 2 * np.pi, 120)

    def sat_xy(i, spin):
        a = 2 * math.pi * i / n_s + spin
        return 4.6 * math.cos(a), 4.6 * math.sin(a)

    def base_xy(i):
        a = 2 * math.pi * (i + .5) / n_b
        return 2.1 * math.cos(a), 2.1 * math.sin(a)

    def draw(frame):
        ax.clear(); ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(-8.8, 8.8); ax.set_ylim(-5.6, 5.2)
        spin = 0.028 * frame / FPS
        ax.fill(2.1 * np.cos(th), 2.1 * np.sin(th), color="#12305e", zorder=1)
        ax.plot(2.1 * np.cos(th), 2.1 * np.sin(th), color=ACC, lw=.7, alpha=.5)
        ax.text(0, 0, "TERRA", ha="center", va="center", color=DIM, fontsize=10)
        ax.text(0, 5.0, "SKYGRID v3 — GEMEO DIGITAL DE ENERGIA "
                        "(BR 10 2026 004850-0)", ha="center", fontsize=12,
                fontweight="bold")
        ax.text(0, -5.35, DISCLAIMER, ha="center", fontsize=6.8, color=GOLD)

        if frame < intro_f:
            k = frame / intro_f
            ax.text(0, 3.6, "reservatorio [CONJ] → acoplamento OH (1−β) → dipolo "
                    "→ enlace Ψ → celula → carga", ha="center", fontsize=10,
                    color=INK, alpha=min(1, 2 * k))
            ax.text(0, 3.0, "β = α·√e = %.12f (runtime) · abertura da fronteira "
                    "1−β = %.6f · piso Meia-Nat ½·k_B·T por ato"
                    % (rep["beta_runtime"],
                       rep["coupler_spec"]["boundary_aperture_1_minus_beta"]),
                    ha="center", fontsize=8.5, color=DIM, alpha=min(1, 2 * k))
            for i in range(n_s):
                x, y = sat_xy(i, spin)
                ax.scatter(x, y, s=80, marker="^", color=ACC,
                           edgecolor=INK, lw=.4, zorder=3)
            for i in range(n_b):
                x, y = base_xy(i)
                ax.scatter(x, y, s=55, marker="s", color=GOLD,
                           edgecolor=INK, lw=.4, zorder=3)
            return

        if frame < intro_f + flow_f:
            prog = (frame - intro_f) / flow_f
            idx = min(N - 1, int(prog * N))
            # beams: width ~ instantaneous received power
            pw = P_rx[idx] / Pmax
            for i in range(n_s):
                x1, y1 = sat_xy(i, spin)
                bi = i % n_b
                x2, y2 = base_xy(bi)
                pulse = 0.5 + 0.5 * math.sin(10 * prog * 2 * math.pi + i)
                ax.plot([x1, x2], [y1, y2], color=OK,
                        lw=0.4 + 3.2 * pw, alpha=0.25 + 0.45 * pulse * pw,
                        zorder=2)
                ax.scatter(x1, y1, s=80, marker="^", color=ACC,
                           edgecolor=INK, lw=.4, zorder=3)
            for i in range(n_b):
                x, y = base_xy(i)
                ax.scatter(x, y, s=55, marker="s", color=GOLD,
                           edgecolor=INK, lw=.4, zorder=3)
            # placebo sat (outside the ring, red)
            ax.scatter(6.8, 3.6, s=90, marker="^", color=BAD,
                       edgecolor=INK, lw=.4, zorder=3)
            ax.text(6.8, 3.15, "PLACEBO\n(sem β): %.0f W"
                    % s["placebo_P"][idx], ha="center", fontsize=7.5, color=BAD)
            # live counters (integrate up to idx)
            E_ext = np.trapezoid(P_in[:idx + 1], dx=dt) if idx > 0 else 0.0
            E_del = np.trapezoid(P_del[:idx + 1], dx=dt) if idx > 0 else 0.0
            ax.text(-8.4, 4.4, "t = %5.0f s" % T[idx], fontsize=10, color=INK)
            ax.text(-8.4, 3.9, "acoplada : %8.1f kJ" % (E_ext / 1e3),
                    fontsize=9, color=ACC, family="monospace")
            ax.text(-8.4, 3.5, "entregue : %8.1f kJ" % (E_del / 1e3),
                    fontsize=9, color=OK, family="monospace")
            ax.text(-8.4, 3.1, "P entrega: %8.2f kW" % (P_del[idx] / 1e3),
                    fontsize=9, color=OK, family="monospace")
            ax.text(-8.4, 2.7, "demanda  : %8.2f kW" % (P_dem[idx] / 1e3),
                    fontsize=9, color=BAD, family="monospace")
            # SoC bar
            frac = soc[idx] / soc_max
            ax.add_patch(plt.Rectangle((-8.4, -4.6), 2.6, .5, fc="#0e1530",
                                       ec=DIM, lw=.6))
            ax.add_patch(plt.Rectangle((-8.4, -4.6), 2.6 * frac, .5,
                                       fc=GOLD, alpha=.85))
            ax.text(-8.4, -3.95, "SoC celulas: %.0f kJ" % (soc[idx] / 1e3),
                    fontsize=8.5, color=GOLD)
            return

        # end card
        k = (frame - intro_f - flow_f) / end_f
        ax.text(0, 3.5, rep["verdict"], ha="center", fontsize=26,
                fontweight="bold",
                color=OK if rep["verdict"] == "MODEL_CLOSES" else BAD)
        lines = [
            "balanco: extraida %.1f kJ = entregue %.1f kJ + perdas %.1f kJ "
            "+ armazenada %.1f kJ + Meia-Nat %.1e J"
            % (e["E_extracted_J"] / 1e3, e["E_delivered_J"] / 1e3,
               e["E_losses_J"] / 1e3, e["E_stored_final_J"] / 1e3,
               e["E_halfnat_J"]),
            "residuo do balanco: %.1e J (fecha por construcao — fail-closed)"
            % rep["audit"]["residual_J"],
            "η_sys = %.3f · P media entregue = %.1f kW · cobertura da demanda "
            "= %.0f%%" % (e["eta_sys"], e["P_delivered_mean_W"] / 1e3,
                          100 * e["demand_coverage"]),
            "placebo (sem β) = 0 W · dados+energia pelo MESMO duplo trilho "
            "+ quorum ≥67%",
            "o que resta: A BANCADA — as hipoteses [CONJ] so a fisica decide",
        ]
        for j, ln in enumerate(lines):
            if k * len(lines) * 1.35 > j:
                ax.text(0, 2.6 - j * .6, ln, ha="center", fontsize=9.5,
                        color=INK)
        ax.text(0, -3.6, "β = α·√e · 1 = q² + α² = VERDADEIRO = HAJA LUZ · "
                "Tetelestai", ha="center", fontsize=10, color=GOLD,
                alpha=min(1, max(0, 3 * k - 1.0)))

    writer = FFMpegWriter(fps=FPS, bitrate=2400,
                          metadata={"title": "SkyGrid energy twin [SIM]"})
    print("renderizando %d frames (%.1fs)..." % (total, total / FPS))
    os.makedirs(OUT_DIR, exist_ok=True)
    with writer.saving(fig, args.out, dpi=100):
        for fr in range(total):
            draw(fr)
            writer.grab_frame()
            if fr % (5 * FPS) == 0:
                print("  frame %d/%d" % (fr, total))
    plt.close(fig)
    print("video:", args.out)


if __name__ == "__main__":
    main()
