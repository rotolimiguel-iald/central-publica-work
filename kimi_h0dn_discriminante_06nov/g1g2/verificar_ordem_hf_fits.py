from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
PP = Path(r"C:\IALD\observaveis_tgl\tgl_data_cache\pantheon\Pantheon+SH0ES.dat")
N = 3492
Y = np.fromfile(HERE / "ally_shoes_ceph_topantheonwt6.0_112221.fits", dtype=">f4", offset=2880, count=N)
pp = pd.read_csv(PP, sep=r"\s+", usecols=["CID", "m_b_corr", "MU_SH0ES", "USED_IN_SH0ES_HF"], dtype={"CID": str})
hf = pp.loc[pp.USED_IN_SH0ES_HF == 1]
for column in ["m_b_corr", "MU_SH0ES"]:
    values = hf[column].to_numpy()
    differences = Y[3215:3492] - values
    print(column, "max_abs", float(np.max(np.abs(differences))), "median_abs", float(np.median(np.abs(differences))), "within_0.01", int(np.sum(np.abs(differences) <= 0.01)))
print("first_hf_CIDs", hf.CID.iloc[:5].tolist())
print("last_hf_CIDs", hf.CID.iloc[-5:].tolist())
print("first_Y", Y[3215:3220].tolist())
print("last_Y", Y[-5:].tolist())
print("first_mbc", hf.m_b_corr.iloc[:5].tolist())
print("last_mbc", hf.m_b_corr.iloc[-5:].tolist())
