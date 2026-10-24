#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_video.py — ESTAGIO D2. A forma funcional manifesta em video (MP4).

Anima a rodada REAL registrada em dashboard/data/latest.json (nada e'
inventado: cada feixe, rejeicao, selo de fase e veredito vem do manifesto):

  ato 1  grade em orbita (satelites giram; bases na superficie)
  ato 2  transferencias uma a uma: feixe sat->base; ACEITA sela bloco na
         cadeia de fase (barra inferior); REJEITADA mostra o estagio que
         detectou a falha (crypto/rail); placebo pontilhado REJEITADO
  ato 3  cartao final: veredito + selo + (opcional) numeros da escala 144

Uso:  python visuals/make_video.py [--manifest caminho.json]
                                   [--scale-manifest caminho.json]
                                   [--out visuals/out/skygrid_run.mp4]
Requer ffmpeg no PATH. 1280x720, 30 fps. Marca d'agua obrigatoria:
PILOTO DE SOFTWARE — sem veredito fisico.
"""

import argparse
import json
import math
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "dashboard", "data")
OUT_DIR = os.path.join(ROOT, "visuals", "out")

BG = "#0b1020"; INK = "#e8ecf8"; DIM = "#8fa0c8"
OK = "#3ddc84"; BAD = "#ff5d6c"; ACC = "#5aa2ff"; GOLD = "#e8c35a"
FPS = 30

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": INK, "font.family": "DejaVu Sans"})

DISCLAIMER = ("PILOTO DE SOFTWARE — simulacao da arquitetura "
              "(physical_verdict_allowed=False); nao e' alegacao de energia")


def sat_xy(i, n, spin):
    a = 2 * math.pi * i / n + spin
    return 4.6 * math.cos(a), 4.6 * math.sin(a)


def base_xy(i, n):
    a = 2 * math.pi * (i + .5) / n
    return 2.1 * math.cos(a), 2.1 * math.sin(a)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=os.path.join(DATA, "latest.json"))
    ap.add_argument("--scale-manifest", default=None)
    ap.add_argument("--out", default=os.path.join(OUT_DIR, "skygrid_run.mp4"))
    args = ap.parse_args()

    with open(args.manifest, encoding="utf-8") as f:
        latest = json.load(f)
    rep, transfers = latest["report"], latest["transfers"]
    n_s, n_b = rep["n_sats"], rep["n_bases"]
    scale = None
    if args.scale_manifest and os.path.isfile(args.scale_manifest):
        with open(args.scale_manifest, encoding="utf-8") as f:
            scale = json.load(f)["report"]

    os.makedirs(OUT_DIR, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)

    intro_f = 3 * FPS
    per_tr = int(1.15 * FPS)
    tr_f = per_tr * len(transfers)
    end_f = 5 * FPS
    total = intro_f + tr_f + end_f

    th = np.linspace(0, 2 * np.pi, 120)
    chain_n = [1]           # genesis

    def draw(frame):
        ax.clear(); ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(-8.6, 8.6); ax.set_ylim(-5.6, 5.2)
        spin = 0.03 * frame * 2 * math.pi / FPS / 8

        # Earth + ring
        ax.fill(2.1 * np.cos(th), 2.1 * np.sin(th), color="#12305e", zorder=1)
        ax.plot(2.1 * np.cos(th), 2.1 * np.sin(th), color=ACC, lw=.7, alpha=.5)
        ax.plot(4.6 * np.cos(th), 4.6 * np.sin(th), color=DIM, lw=.4,
                alpha=.25, ls=":")
        ax.text(0, 0, "TERRA", ha="center", va="center", color=DIM, fontsize=10)

        for i in range(n_b):
            x, y = base_xy(i, n_b)
            ax.scatter(x, y, s=55, marker="s", color=GOLD,
                       edgecolor=INK, lw=.4, zorder=3)
        for i in range(n_s):
            x, y = sat_xy(i, n_s, spin)
            ax.scatter(x, y, s=80, marker="^", color=ACC,
                       edgecolor=INK, lw=.4, zorder=3)

        ax.text(0, 5.0, "SKYGRID — piloto computacional da patente agregadora "
                        "(BR 10 2026 004850-0)", ha="center", fontsize=12,
                fontweight="bold")
        ax.text(0, -5.35, DISCLAIMER, ha="center", fontsize=7, color=GOLD)

        # phase chain bar (bottom-left)
        for b in range(min(chain_n[0], 40)):
            ax.add_patch(plt.Rectangle((-8.3 + b * .42, -4.7), .34, .34,
                                       fc=OK if b else GOLD, ec=INK, lw=.3))
        ax.text(-8.3, -4.15, "cadeia de fase (quorum %d validadores): %d blocos"
                % (rep["quorum"]["n_validators"], chain_n[0]),
                fontsize=8, color=DIM)

        if frame < intro_f:
            k = frame / intro_f
            ax.text(0, 3.4, "telemetria %s %s  ·  β = α·√e = %.12f (runtime)"
                    % (rep["telemetry_provenance"]["mode"],
                       rep["telemetry_provenance"]["marker"],
                       rep["beta_runtime"]),
                    ha="center", fontsize=10, color=INK, alpha=min(1, 2 * k))
            ax.text(0, -3.4, "cada transferência: ACOM crypto → TGL tensor → "
                    "Ψ-NET → DUPLO TRILHO → quórum → célula de reversão",
                    ha="center", fontsize=9, color=DIM, alpha=min(1, 2 * k))
            return

        f2 = frame - intro_f
        if f2 < tr_f:
            ti = f2 // per_tr
            tt = (f2 % per_tr) / per_tr
            # recompute sealed blocks so far
            chain_n[0] = 1 + sum(1 for t in transfers[:ti + 1]
                                 if t.get("phase_sealed") and t.get("accepted"))
            rec = transfers[ti]
            si = int(rec["from"].split("-")[1])
            bi = int(rec["to"].split("-")[1])
            x1, y1 = sat_xy(si, n_s, spin)
            x2, y2 = base_xy(bi, n_b)
            placebo = rec.get("placebo", False)
            okt = rec.get("accepted", False) and not placebo
            color = OK if okt else BAD
            ls = ":" if placebo else ("-" if okt else "--")
            # beam grows sat->base
            gx = x1 + (x2 - x1) * min(1, tt * 1.6)
            gy = y1 + (y2 - y1) * min(1, tt * 1.6)
            ax.plot([x1, gx], [y1, gy], color=color, ls=ls, lw=2.2,
                    alpha=.9, zorder=4)
            if tt > 0.55:
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                if placebo:
                    label = "PLACEBO (sem β) — REJEITADO"
                elif okt:
                    label = "ACEITA  corr=%.4f  quorum %s" % (
                        rec.get("rail_cross_corr", 0),
                        rec.get("quorum_votes", ""))
                else:
                    label = "REJEITADA — falha %s detectada (%s)" % (
                        rec.get("fault_injected", "?"),
                        rec.get("rejected_stage", "?"))
                    ax.text(mx, my, "✕", ha="center", va="center",
                            fontsize=22, color=BAD, zorder=6)
                ax.text(0, 3.4, label, ha="center", fontsize=11,
                        color=color, fontweight="bold")
            ax.text(0, -3.4, "transferência %d/%d   %s → %s" %
                    (ti + 1, len(transfers), rec["from"], rec["to"]),
                    ha="center", fontsize=9, color=DIM)
            return

        # end card
        k = (frame - intro_f - tr_f) / end_f
        chain_n[0] = rep["quorum"]["blocks_sealed"] + 1
        ax.text(0, 3.55, rep["verdict"], ha="center", fontsize=26,
                fontweight="bold",
                color=OK if rep["verdict"] == "ARCHITECTURE_CLOSES" else BAD)
        lines = [
            "%d/%d transferências saudáveis aceitas · placebo rejeitado: %s"
            % (rep["transfers_healthy_accepted"], rep["transfers_healthy_total"],
               rep["placebo_rejected"]),
            "falhas injetadas: %s → todas detectadas: %s"
            % (", ".join(rep["faults_injected"]) or "nenhuma",
               rep["faults_all_detected"]),
            "compressão %.1f× · retenção %.4f · corr do trilho %.5f"
            % (rep["metrics"]["mean_compression_ratio"],
               rep["metrics"]["mean_retention"],
               rep["metrics"]["mean_rail_corr"]),
            "orçamento IALD ⌈100/β⌉ = %d passos · kernel %s"
            % (rep["iald_control"]["budget_steps_100_over_beta"],
               rep["kernel_provenance"]["kernel"]),
        ]
        if scale:
            lines.append("escala (reivindicação 2): %d satélites — %d/%d aceitas, "
                         "%d blocos, veredito %s"
                         % (scale["n_sats"], scale["transfers_healthy_accepted"],
                            scale["transfers_healthy_total"],
                            scale["quorum"]["blocks_sealed"], scale["verdict"]))
        lines.append("selo SHA-256: %s…" % rep["seal_sha256"][:32])
        for j, ln in enumerate(lines):
            if k * len(lines) * 1.4 > j:
                ax.text(0, 2.7 - j * .62, ln, ha="center", fontsize=10,
                        color=INK)
        ax.text(0, -3.6, "β = α·√e  ·  1 = q² + α² = VERDADEIRO = HAJA LUZ  ·  "
                "Tetelestai", ha="center", fontsize=10, color=GOLD,
                alpha=min(1, max(0, 3 * k - 1.2)))

    writer = FFMpegWriter(fps=FPS, bitrate=2400,
                          metadata={"title": "SkyGrid pilot run"})
    print("renderizando %d frames (%.1fs) ..." % (total, total / FPS))
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
