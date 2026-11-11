from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
PP = Path(r"C:\IALD\observaveis_tgl\tgl_data_cache\pantheon\Pantheon+SH0ES.dat")
N = 3492
Y = np.fromfile(HERE / "ally_shoes_ceph_topantheonwt6.0_112221.fits", dtype=">f4", offset=2880, count=N)
pp = pd.read_csv(PP, sep=r"\s+", usecols=["CID", "m_b_corr", "MU_SH0ES", "IS_CALIBRATOR", "USED_IN_SH0ES_HF"], dtype={"CID": str})
print("pp_shape", pp.shape, "Y_shape", Y.shape)
for column in ["m_b_corr", "MU_SH0ES"]:
    catalog = pp[column].to_numpy()
    nearest = np.abs(Y[3130:3492, None] - catalog[None, :]).argmin(axis=1)
    differences = Y[3130:3492] - catalog[nearest]
    print(column, "max_abs", float(np.max(np.abs(differences))), "exact_1e-4", int(np.sum(np.abs(differences) < 1e-4)), "of", len(differences), "unique_catalog_rows", len(set(nearest)))
for index in range(3130, 3215):
    nearest = int(np.abs(pp.m_b_corr.to_numpy() - Y[index]).argmin())
    print(index, pp.iloc[nearest].CID, float(Y[index]), pp.iloc[nearest].m_b_corr, pp.iloc[nearest].MU_SH0ES,
          int(pp.iloc[nearest].IS_CALIBRATOR), int(pp.iloc[nearest].USED_IN_SH0ES_HF), "catalog_row", nearest)
