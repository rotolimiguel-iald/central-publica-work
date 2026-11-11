from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
with np.load(BASE / "network/network.npz", allow_pickle=False) as net:
    C = net["C"].copy()
    F_anchor = net["factor_anchor"].copy()
    F_mas = net["factor_MAS"].copy()
    F_hms = net["factor_HMS"].copy()
rows_metadata = pd.read_json(BASE / "network/rows.json")
source_lines = rows_metadata.iloc[:166].source_line.to_numpy(dtype=int)
errors_by_line = {}
for line_number, text in enumerate((BASE / "network/upstream/data/host_data.dat").read_text(encoding="utf-8").splitlines(), 1):
    fields = text.split("#", 1)[0].split()
    if len(fields) >= 6 and fields[0].lower() != "host":
        errors_by_line[line_number] = float(fields[2])
D = np.zeros((255, 255))
D[np.arange(166), np.arange(166)] = [errors_by_line[line] ** 2 for line in source_lines]
T_anchor = F_anchor @ F_anchor.T
T_mas = F_mas @ F_mas.T
T_hms = F_hms @ F_hms.T
T_hms -= np.diag(np.diag(T_hms))
R = D + T_anchor + T_mas + T_hms
for name, matrix in [("D", D), ("T_anchor", T_anchor), ("T_mas", T_mas), ("T_hms", T_hms), ("R", R), ("C_host", C[:166, :166])]:
    print(name, "rank", np.linalg.matrix_rank(matrix), "min_diag", np.diag(matrix).min(), "max_abs_offdiag", np.max(np.abs(matrix - np.diag(np.diag(matrix)))),
          "eig_min", np.linalg.eigvalsh(matrix)[0], "eig_max", np.linalg.eigvalsh(matrix)[-1])
print("R_minus_C_max", np.max(np.abs(R - C[:166, :166])))
print("F_anchor_minmax", F_anchor.min(), F_anchor.max())
print("F_mas_minmax", F_mas.min(), F_mas.max())
print("F_hms_minmax", F_hms.min(), F_hms.max())
