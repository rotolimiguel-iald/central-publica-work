from pathlib import Path
import numpy as np

path = Path(__file__).resolve().parent / "alll_shoes_ceph_topantheonwt6.0_112221.fits"
N = 3492
L = np.fromfile(path, dtype=">f4", offset=2880, count=47 * N).reshape(47, N)
for i, row in enumerate(L):
    nz = np.flatnonzero(row)
    print(i, len(nz), int(nz[0]) if len(nz) else None, int(nz[-1]) if len(nz) else None,
          "unique=", len(np.unique(row[nz])), "sum=", float(row[nz].sum()))
