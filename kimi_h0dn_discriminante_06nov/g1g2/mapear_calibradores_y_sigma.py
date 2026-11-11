from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
N = 3492
L = np.fromfile(HERE / "alll_shoes_ceph_topantheonwt6.0_112221.fits", dtype=">f4", offset=2880, count=47 * N).reshape(47, N)
Y = np.fromfile(HERE / "ally_shoes_ceph_topantheonwt6.0_112221.fits", dtype=">f4", offset=2880, count=N)
C = np.fromfile(HERE / "allc_shoes_ceph_topantheonwt6.0_112221.fits", dtype=">f4", offset=2880, count=N * N).reshape(N, N)
cal = pd.read_csv(
    HERE.parent.parent / "astra_bell_fock_tt_05nov/h0dn_bg1_06nov/network/upstream/data/sn1a_calib.dat",
    sep=r"\s+", comment="#", header=None,
    usecols=[0, 1, 2, 3, 4], names=["number", "host", "CID", "m0", "sigma"],
    dtype={"CID": str},
).iloc[:42]
sigma_release = np.sqrt(C.diagonal())
for row in cal.itertuples():
    candidates = np.flatnonzero((np.abs(Y - row.m0) <= 0.06) & (np.abs(sigma_release - row.sigma) <= 0.003))
    best = sorted(
        candidates,
        key=lambda i: abs(float(Y[i] - row.m0)) + abs(float(sigma_release[i] - row.sigma)),
    )
    print(row.host, row.CID, "candidates", [(int(i), float(Y[i]), float(sigma_release[i])) for i in best])
