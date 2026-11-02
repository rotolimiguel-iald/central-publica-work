import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pathlib import Path

OUT = Path(__file__).resolve().parent
labels = [
    "Ringdown A — discrepância do par\n(não cega; calibração)",
    "H0DN × BG1\n(triagem; não é z_disc observado)",
    "SN Ia — deslocamento de zero\n(não é z_disc calibrado)",
    "Fase 9 R25 × BG1\n(réplica não decisória)",
    "Fase 9 P × BG2\n(diagnóstico não decisório)",
    "Ringdown D14\n(poder máximo projetado)",
    "Fase 9 primária\n(z_disc observado)",
    "Neutrino m₂ global\n(tensão; E₀ declarado)",
]
values = [13.5, 6.576, 5.4, 5.2751392678, 5.1227304882, 4.64, 4.4431235681, 2.9528540277]
colors = ["#8b5cf6", "#f59e0b", "#8b5cf6", "#8b5cf6", "#8b5cf6", "#f59e0b", "#0f766e", "#f59e0b"]

plt.rcParams["font.family"] = "DejaVu Sans"
fig, ax = plt.subplots(figsize=(12, 7.2), dpi=180)
y = list(range(len(labels)))[::-1]
ax.barh(y, values, color=colors, height=0.62)
ax.set_yticks(y, labels, fontsize=10)
ax.axvline(5, color="#b91c1c", linestyle="--", linewidth=1.8, label="limiar 5σ")
for yi, value in zip(y, values):
    offset = 0.8 if 4 < value < 5.5 else 0.18
    ax.text(value + offset, yi, f"{value:.2f}σ", va="center", fontsize=10, fontweight="bold")
ax.set_xlim(0, 15.2)
ax.set_xlabel("valor nominal de σ — o estatuto epistêmico aparece no rótulo", fontsize=11)
ax.set_title("Por que um número acima de 5σ ainda não é o teste decisivo", fontsize=16, fontweight="bold", pad=16)
ax.grid(axis="x", alpha=0.18)
ax.spines[["top", "right", "left"]].set_visible(False)
legend = [
    Patch(facecolor="#8b5cf6", label="acima de 5, mas não decisório"),
    Patch(facecolor="#f59e0b", label="planejamento ou tensão condicionada"),
    Patch(facecolor="#0f766e", label="primário observado"),
]
ax.legend(handles=legend + [plt.Line2D([0], [0], color="#b91c1c", linestyle="--", label="limiar 5σ")], loc="lower right", frameon=False, fontsize=9)
fig.text(0.01, 0.012, "Fontes: Fase 9 V2-C1, plano D, núcleo v404, Fase 5 SH0ES e triagem H0DN × BG1. Não é uma combinação estatística.", fontsize=8, color="#475569")
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(OUT / "mapa_sigma_estatuto_30out.png", bbox_inches="tight")
print(OUT / "mapa_sigma_estatuto_30out.png")
