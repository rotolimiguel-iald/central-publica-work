from pathlib import Path
import json
import numpy as np

HERE = Path(__file__).resolve().parent
N = 3492
L = np.fromfile(HERE / "alll_shoes_ceph_topantheonwt6.0_112221.fits", dtype=">f4", offset=2880, count=47 * N).reshape(47, N)
Y = np.fromfile(HERE / "ally_shoes_ceph_topantheonwt6.0_112221.fits", dtype=">f4", offset=2880, count=N)
C = np.fromfile(HERE / "allc_shoes_ceph_topantheonwt6.0_112221.fits", dtype=">f4", offset=2880, count=N * N).reshape(N, N)

rows = []
for index, row in enumerate(L):
    nz = np.flatnonzero(row)
    values, counts = np.unique(row[nz], return_counts=True)
    rows.append({
        "row": index,
        "nonzero_count": len(nz),
        "first": int(nz[0]) if len(nz) else None,
        "last": int(nz[-1]) if len(nz) else None,
        "values": {str(float(v)): int(c) for v, c in zip(values, counts)},
    })
print(json.dumps({
        "L_shape": list(L.shape),
        "Y_shape": list(Y.shape),
        "C_shape": list(C.shape),
        "C_symmetry_max_abs": float(np.max(np.abs(C - C.T))),
        "C_diag_min": float(C.diagonal().min()),
        "C_diag_max": float(C.diagonal().max()),
        "rows": rows,
    }, indent=2))
