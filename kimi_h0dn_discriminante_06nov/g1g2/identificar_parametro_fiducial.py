from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
N = 3492
L = np.fromfile(HERE / "alll_shoes_ceph_topantheonwt6.0_112221.fits", dtype=">f4", offset=2880, count=47 * N).reshape(47, N)
Y = np.fromfile(HERE / "ally_shoes_ceph_topantheonwt6.0_112221.fits", dtype=">f4", offset=2880, count=N)
cal = pd.read_csv(
    HERE.parent.parent / "astra_bell_fock_tt_05nov/h0dn_bg1_06nov/network/upstream/data/sn1a_calib.dat",
    sep=r"\s+", comment="#", header=None,
    usecols=[0, 1, 2, 3, 4], names=["number", "host", "CID", "m0", "sigma"],
    dtype={"CID": str},
).iloc[:42]
indices = np.array([int(np.abs(Y - value).argmin()) for value in cal.m0])
print("unique_R22_nearest_indices", len(set(indices)), "of", len(indices))
for i, row in enumerate(L):
    values = row[indices]
    if np.all(values != 0):
        print("row", i, "nonzero_at_all_R22", "unique_values", np.unique(values)[:20], "row_nonzero", np.count_nonzero(row))
print("index_min_max", indices.min(), indices.max())
print("indices", indices.tolist())
