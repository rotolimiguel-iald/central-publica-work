from pathlib import Path
import json
import numpy as np

BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
with np.load(BASE / "network/network.npz", allow_pickle=False) as net:
    C = net["C"].copy()
rows = json.loads((BASE / "network/rows.json").read_text(encoding="utf-8"))
diag = np.diag(C)
zero = np.flatnonzero(diag == 0)
print("zero_diag_count", len(zero))
print("zero_diag_rows", [(int(i), rows[i]["kind"], rows[i]["description"]) for i in zero[:100]])
for name, indices in {
    "hosts": np.arange(0, 166),
    "groups": np.arange(166, 179),
    "sn1a_calib": np.arange(179, 234),
    "sn1a_hf": np.array([248]),
    "sbf_calib": np.arange(234, 248),
    "sbf_hf": np.array([249]),
    "megamasers": np.arange(250, 255),
}.items():
    block = C[np.ix_(indices, indices)]
    print(name, "shape", block.shape, "rank", np.linalg.matrix_rank(block), "zero_diag", int(np.sum(np.diag(block) == 0)))
