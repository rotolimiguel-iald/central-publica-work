from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
N = 3492
Y = np.fromfile(HERE / "ally_shoes_ceph_topantheonwt6.0_112221.fits", dtype=">f4", offset=2880, count=N)
cal = pd.read_csv(
    HERE.parent.parent / "astra_bell_fock_tt_05nov/h0dn_bg1_06nov/network/upstream/data/sn1a_calib.dat",
    sep=r"\s+", comment="#", header=None,
    usecols=[0, 1, 2, 3, 4], names=["number", "host", "CID", "m0", "sigma"],
    dtype={"CID": str},
)
indices = []
for row in cal.itertuples():
    distance = np.abs(Y - row.m0)
    index = int(distance.argmin())
    indices.append(index)
    print(row.host, row.CID, "nearest_index", index, "diff", float(distance[index]), "Y", float(Y[index]), "m0", row.m0)
print("unique_indices", len(set(indices)), "max_nearest_diff", float(np.max(np.abs(Y[np.array(indices)] - cal.m0.to_numpy()))))
