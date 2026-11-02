"""Aritmética de tensões públicas para m2 TGL; não ajusta nem combina dados."""
from pathlib import Path
import json
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
M2_PRED_MEV = 8.507414099900329
DELTA_PRED = (M2_PRED_MEV / 1000) ** 2 / 1e-5  # em 1e-5 eV^2

# mu e erros em 1e-5 eV^2. side_to_pred escolhe o erro do lado da previsão.
rows = [
    dict(id="JUNO_207d", grupo="autônomo", mu=7.388, err_m=0.078, err_p=0.078, side_to_pred="up", exposure_days=207.2,
         fonte="arXiv:2609.37895", url="https://arxiv.org/abs/2609.37895"),
    dict(id="SNO_plus", grupo="autônomo", mu=7.91, err_m=0.25, err_p=0.22, side_to_pred="down", exposure_days=685.0,
         fonte="PRL 137, 101807 (2026); arXiv:2511.11856", url="https://doi.org/10.1103/mv5z-pfb7"),
    dict(id="SK_Gd_reator", grupo="autônomo", mu=9.08, err_m=0.54, err_p=0.55, side_to_pred="down", exposure_days=411.52,
         fonte="arXiv:2610.03143", url="https://arxiv.org/abs/2610.03143"),
    dict(id="KamLAND", grupo="autônomo", mu=7.54, err_m=0.18, err_p=0.19, side_to_pred="down", exposure_days=2991.0,
         fonte="PRD 88, 033001; arXiv:1303.4667", url="https://arxiv.org/abs/1303.4667"),
    dict(id="Solares_sem_KamLAND", grupo="autônomo (uma família)", mu=6.10, err_m=0.81, err_p=0.95, side_to_pred="up", exposure_days=None,
         fonte="PRD 109, 092001; arXiv:2312.12907", url="https://arxiv.org/abs/2312.12907"),
    dict(id="JUNO_59d_subset", grupo="subconjunto JUNO", mu=7.50, err_m=0.12, err_p=0.12, side_to_pred="up", exposure_days=59.1,
         fonte="Nature 654, 343; arXiv:2511.14593", url="https://arxiv.org/abs/2511.14593"),
    dict(id="NuFIT_6_1", grupo="global não autônomo", mu=7.537, err_m=0.094, err_p=0.100, side_to_pred="down", exposure_days=None,
         fonte="NuFIT 6.1", url="https://arxiv.org/abs/2601.09791"),
    dict(id="Capozzi_2025", grupo="global não autônomo", mu=7.48, err_m=0.10, err_p=0.10, side_to_pred="down", exposure_days=None,
         fonte="PRD 114, 016026; arXiv:2511.21650", url="https://doi.org/10.1103/cxqw-1bty"),
    dict(id="Bari_2026a_NO", grupo="global preliminar não autônomo", mu=7.465, err_m=0.080, err_p=0.072, side_to_pred="down", exposure_days=None,
         fonte="Global-nu release 2026.a", url="https://global-nu.org/results.html"),
    dict(id="SK_Gd_solar_reator", grupo="combinação não adicional", mu=8.94, err_m=0.47, err_p=0.46, side_to_pred="down", exposure_days=None,
         fonte="arXiv:2610.03143", url="https://arxiv.org/abs/2610.03143"),
]

results = []
for row in rows:
    sigma_delta = row["err_p"] if row["side_to_pred"] == "up" else row["err_m"]
    m2_obs = (10 * row["mu"]) ** 0.5  # meV, com mu em 1e-5 eV²
    sigma_m2 = 0.5 * (sigma_delta / row["mu"]) * m2_obs
    z = abs(m2_obs - M2_PRED_MEV) / sigma_m2
    # Convenção congelada: sigma_m2 = (sigma_Delta/Delta) * m2/2.
    sigma5 = 2 * row["mu"] * abs(m2_obs - M2_PRED_MEV) / (5 * m2_obs)
    item = {**row, "delta_pred_1e-5_eV2": DELTA_PRED,
            "m2_obs_meV": m2_obs, "sigma_m2_meV": sigma_m2,
            "sigma_delta_usado_1e-5_eV2": sigma_delta,
            "z_sigma": z, "sigma_necessario_5sigma_1e-5_eV2": sigma5}
    if row["exposure_days"] is not None:
        total = row["exposure_days"] * (sigma_delta / sigma5) ** 2
        item["exposicao_equivalente_total_dias"] = total
        item["exposicao_adicional_dias"] = total - row["exposure_days"]
        item["exposicao_adicional_anos"] = (total - row["exposure_days"]) / 365.25
        item["escala_condicional"] = "centro e forma dos erros fixos; sigma ~ 1/sqrt(t); não é cronograma"
    results.append(item)

payload = {
    "data_corte": "2026-10-30",
    "m2_pred_meV": M2_PRED_MEV,
    "delta_pred_1e-5_eV2": DELTA_PRED,
    "regra": "m2=sqrt(10*mu) meV; sigma_m2=0.5*(sigma_delta/mu)*m2; z=|m2-m2_pred|/sigma_m2",
    "veredito": "zero determinações autônomas >=5 sigma; medidas históricas <=1 sigma não são par prospectivo automático",
    "resultados": results,
}
(OUT / "determinacoes_m2_30out.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

plot_rows = results[:5] + [results[6]]
labels = [r["id"].replace("_", " ") for r in plot_rows]
zvals = [r["z_sigma"] for r in plot_rows]
colors = ["#0f766e" if r["grupo"].startswith("autônomo") else "#f59e0b" for r in plot_rows]
fig, ax = plt.subplots(figsize=(11, 5.8), dpi=180)
x = list(range(len(labels)))
ax.bar(x, zvals, color=colors, width=0.66)
ax.axhline(5, color="#b91c1c", linestyle="--", linewidth=1.8, label="limiar 5σ")
for xi, z in zip(x, zvals):
    ax.text(xi, z + 0.09, f"{z:.2f}σ", ha="center", fontsize=10, fontweight="bold")
ax.set_xticks(x, labels, rotation=22, ha="right")
ax.set_ylim(0, 5.8)
ax.set_ylabel("distância da previsão m₂ = 8,507414 meV (σ)")
ax.set_title("Determinações públicas de Δm²₂₁ — nenhuma autônoma atinge 5σ", fontweight="bold")
ax.grid(axis="y", alpha=0.18)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig(OUT / "determinacoes_m2_30out.png", bbox_inches="tight")

print(f"delta_pred={DELTA_PRED:.12f} em 1e-5 eV^2")
for item in results:
    print(f"{item['id']}: z={item['z_sigma']:.6f}; sigma5={item['sigma_necessario_5sigma_1e-5_eV2']:.7f}")
print(OUT / "determinacoes_m2_30out.json")
print(OUT / "determinacoes_m2_30out.png")
