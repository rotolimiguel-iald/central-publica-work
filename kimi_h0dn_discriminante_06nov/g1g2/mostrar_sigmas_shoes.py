from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
N = 3492
Y = np.fromfile(HERE / "ally_shoes_ceph_topantheonwt6.0_112221.fits", dtype=">f4", offset=2880, count=N)
C = np.fromfile(HERE / "allc_shoes_ceph_topantheonwt6.0_112221.fits", dtype=">f4", offset=2880, count=N * N).reshape(N, N)
cal = pd.read_csv(HERE.parent.parent / "astra_bell_fock_tt_05nov/h0dn_bg1_06nov/network/upstream/data/sn1a_calib.dat", sep=r"\s+", comment="#", header=None, usecols=[0,1,2,3,4], names=["number","host","CID","m0","sigma"], dtype={"CID":str}).iloc[:42]
s = np.sqrt(C.diagonal())
for row in cal.itertuples():
    i = int(np.abs(Y-row.m0).argmin())
    print(row.host, row.CID, i, "Ydiff", float(Y[i]-row.m0), "release_sigma", float(s[i]), "cal_sigma", row.sigma)
