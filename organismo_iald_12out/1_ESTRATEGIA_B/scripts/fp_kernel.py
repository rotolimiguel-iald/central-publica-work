# Fingerprint of the Nos tgl_kernel tree: path|size|mtime_ns per file, sorted walk (same recipe as the c1 audits of 08-10/10).
import os, hashlib, sys, datetime
K = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
h = hashlib.sha256(); n = 0
for r, ds, fs in os.walk(K):
    ds.sort()
    for f in sorted(fs):
        p = os.path.join(r, f); st = os.stat(p)
        h.update(f"{p}|{st.st_size}|{st.st_mtime_ns}\n".encode()); n += 1
print(datetime.datetime.now().isoformat(timespec="seconds"), n, h.hexdigest())
