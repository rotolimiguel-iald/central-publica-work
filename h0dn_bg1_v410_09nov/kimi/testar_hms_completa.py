from pathlib import Path
import json
import numpy as np

BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
HERE = Path(r"C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi")
with np.load(BASE / "network/network.npz", allow_pickle=False) as net:
    C0 = net["C"].copy()
    F_hms = net["factor_HMS"].copy()
with np.load(HERE / "y_obs.npz", allow_pickle=False) as obs:
    y = obs["y_centered"].copy()
T_hms = F_hms @ F_hms.T
C = C0 + np.diag(np.diag(T_hms))
vals = np.linalg.eigvalsh(C)
import importlib.util
spec = importlib.util.spec_from_file_location("r2_estimator", BASE / "estimator.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
with np.load(BASE / "network/network.npz", allow_pickle=False) as net:
    A = net["A"].copy()
    c = net["c_cepheid"].copy()
    h_index = int(net["h_index"])
models, metadata, null = module.geometry(A, C, c, h_index)
projection = y @ null
max_projection = float(np.max(np.abs(projection))) if null.shape[1] else 0.0
payload = {
    "status": "DIAGNOSTIC_FULL_HMS_NOT_ADMISSION",
    "rank": int(np.linalg.matrix_rank(C)),
    "eigen_min": float(vals[0]),
    "eigen_min_positive": float(vals[vals > 1e-12].min()),
    "max_abs_null_projection": max_projection,
    "tolerance": 1e-8 * max(1.0, float(np.max(np.abs(y)))),
    "pass": bool(max_projection <= 1e-8 * max(1.0, float(np.max(np.abs(y))))),
    "null_basis_shape": list(null.shape),
    "geometry_metadata": metadata,
    "caveat": "Adding the HMS diagonal is only a diagnostic. It may double-count variance already included in host mu_error and is not admitted as physical covariance.",
}
(HERE / "DIAGNOSTICO_HMS_COMPLETA.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload, indent=2))
