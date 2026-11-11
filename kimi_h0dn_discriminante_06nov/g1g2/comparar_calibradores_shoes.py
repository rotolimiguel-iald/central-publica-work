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
y = Y[2593:2648]
print("count", len(y), len(cal), "max_abs_m0_diff", float(np.max(np.abs(y - cal.m0.to_numpy()))))
for i in range(len(cal)):
    print(i, cal.iloc[i].host, cal.iloc[i].CID, float(y[i] - cal.iloc[i].m0), float(Y[2593+i]), float(cal.iloc[i].m0))
