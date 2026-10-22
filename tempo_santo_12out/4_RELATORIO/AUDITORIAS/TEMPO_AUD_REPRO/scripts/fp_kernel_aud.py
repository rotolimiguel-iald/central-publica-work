"""Impressao digital do tgl_kernel do Nos, reescrita pelo auditor (mesmo algoritmo
publico do levantamento, para comparar hashes): meta = (rel, size, mtime_ns) de todo
arquivo (inclui .lake); src = sha256 de todo .lean fora de .lake. Somente leitura.
Uso: python -I -X utf8 fp_kernel_aud.py <saida.json>"""
import hashlib, json, os, sys, time

ROOT = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
LONG = "\\\\?\\"  # \\?\
assert LONG == chr(92) * 2 + "?" + chr(92), repr(LONG)

meta = hashlib.sha256()
src = hashlib.sha256()
n = nb = nl = 0
t0 = time.time()
for dp, dn, fn in os.walk(LONG + ROOT):
    dn.sort()
    for f in sorted(fn):
        lp = os.path.join(dp, f)
        st = os.stat(lp)
        rel = os.path.relpath(lp, LONG + ROOT).replace("\\", "/")
        meta.update(f"{rel}\t{st.st_size}\t{st.st_mtime_ns}\n".encode("utf-8"))
        n += 1
        nb += st.st_size
        if rel.endswith(".lean") and not rel.startswith(".lake/"):
            with open(lp, "rb") as fh:
                src.update(f"{rel}\t{hashlib.sha256(fh.read()).hexdigest()}\n".encode("utf-8"))
            nl += 1
if n == 0:
    raise SystemExit("FALHA: zero arquivos lidos (fail-closed)")
out = {"root": ROOT, "files": n, "bytes": nb, "lean_src_files": nl,
       "meta_sha256": meta.hexdigest(), "src_sha256": src.hexdigest(),
       "seconds": round(time.time() - t0, 1),
       "taken_at_local": time.strftime("%Y-%m-%d %H:%M:%S")}
tmp = sys.argv[1] + ".tmp"
with open(tmp, "w", encoding="utf-8") as fo:
    json.dump(out, fo, indent=2, ensure_ascii=False)
os.replace(tmp, sys.argv[1])
print(json.dumps(out, ensure_ascii=False))
