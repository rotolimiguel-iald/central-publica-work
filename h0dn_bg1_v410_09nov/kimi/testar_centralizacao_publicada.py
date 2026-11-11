from pathlib import Path
import json
import numpy as np

BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
HERE = Path(r"C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi")

with np.load(BASE / "network/network.npz", allow_pickle=False) as net:
    A = net["A"].copy()
    names = net["param_names"].copy()
with np.load(BASE / "estimator_frozen.npz", allow_pickle=False) as est:
    null = est["null_basis"].copy()
with np.load(HERE / "y_obs.npz", allow_pickle=False) as obs:
    y = obs["y_centered"].copy()
rows = json.loads((HERE / "PARAMETROS_PUBLICADOS_TABELAS.json").read_text(encoding="utf-8"))["A6.T12.2"]


def host_code(name: str) -> str:
    if name.startswith("NGC "):
        return "N" + name.split()[1].zfill(4)
    if name.startswith("UGC "):
        return "U" + name.split()[1].zfill(4)
    if name == "Mrk 1337":
        return "M1337"
    if name.startswith("M "):
        return "M" + name.split()[1]
    if name.startswith("IC "):
        return "IC" + name.split()[1]
    return name


published = {}
for row in rows:
    try:
        published[host_code(row[0])] = float(row[1])
    except (ValueError, TypeError):
        continue
published.update({
    "Fornax": 31.455,
    "Virgo": 31.060,
    "SNe Ia M_B": -19.252,
    "SBF M_offset": -0.023,
    "log_10(H0)": float(np.log10(73.499)),
})
missing = [name for name in names if name not in published]
assert not missing, missing
x = np.array([published[name] for name in names])
y_centered = y - A @ x
max_abs = float(np.max(np.abs(y_centered @ null)))
tolerance = 1e-8 * max(1.0, float(np.max(np.abs(y_centered))))
residual = (y_centered @ null) @ null.T
payload = {
    "status": "PUBLISHED_CENTERING_TEST__NO_FIT",
    "published_parameters": {name: float(published[name]) for name in names},
    "max_abs_null_projection": max_abs,
    "tolerance": tolerance,
    "pass": max_abs <= tolerance,
    "largest_projected_rows": [
        {"row": int(i), "abs_residual": float(abs(residual[i])), "description": str(rows_metadata[i]["description"])}
        for i, rows_metadata in []
    ],
}
rows_metadata = json.loads((BASE / "network/rows.json").read_text(encoding="utf-8"))
payload["largest_projected_rows"] = [
    {"row": int(i), "abs_residual": float(abs(residual[i])), "description": rows_metadata[i]["description"]}
    for i in np.argsort(np.abs(residual))[::-1][:20]
]
(HERE / "TESTE_CENTRALIZACAO_PUBLICADA.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload, ensure_ascii=False, indent=2))
