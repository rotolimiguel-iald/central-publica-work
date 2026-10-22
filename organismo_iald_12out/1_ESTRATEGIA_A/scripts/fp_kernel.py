"""Impressao digital do tgl_kernel (receita da frente H): caminho|tamanho|mtime de todo arquivo, sha256 do rol."""
import os, hashlib, sys, pathlib, datetime
ROOT = pathlib.Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
rows = []
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        p = pathlib.Path(dp) / f
        st = p.stat()
        rows.append(f"{p.relative_to(ROOT).as_posix()}|{st.st_size}|{int(st.st_mtime)}")
rows.sort()
h = hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()
out = pathlib.Path(sys.argv[1])
out.write_text(f"{len(rows)} {h} {datetime.datetime.now().isoformat(timespec='seconds')}\n", encoding="utf-8")
print(out.read_text())
