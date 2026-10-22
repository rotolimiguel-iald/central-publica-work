"""(copia do levantamento F1.TEMPO, sem alteracao de logica) Impressao digital do tgl_kernel do Nos (somente leitura).
meta: (relpath, size, mtime_ns) de TODO arquivo sob a raiz (inclui .lake);
src : sha256 do conteudo de todo .lean fora de .lake.
Uso: python -I fingerprint_kernel.py <saida.json>"""
import hashlib, json, os, sys, time

ROOT = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
LONG = "\\\\?\\"  # prefixo de caminho longo do Windows: \\?\


def walk(root):
    for dp, dn, fn in os.walk(LONG + root):
        dn.sort()
        for f in sorted(fn):
            yield os.path.join(dp, f)


t0 = time.time()
meta = hashlib.sha256()
src = hashlib.sha256()
n = 0
nbytes = 0
nlean = 0
maxlen = 0
for lp in walk(ROOT):
    st = os.stat(lp)
    rel = os.path.relpath(lp, LONG + ROOT).replace("\\", "/")
    maxlen = max(maxlen, len(lp) - len(LONG))
    meta.update(f"{rel}\t{st.st_size}\t{st.st_mtime_ns}\n".encode("utf-8"))
    n += 1
    nbytes += st.st_size
    if rel.endswith(".lean") and not rel.startswith(".lake/"):
        with open(lp, "rb") as fh:
            h = hashlib.sha256(fh.read()).hexdigest()
        src.update(f"{rel}\t{h}\n".encode("utf-8"))
        nlean += 1
out = {"root": ROOT, "files": n, "bytes": nbytes, "lean_src_files": nlean,
       "max_path_len": maxlen,
       "meta_sha256": meta.hexdigest(), "src_sha256": src.hexdigest(),
       "seconds": round(time.time() - t0, 1),
       "taken_at": time.strftime("%Y-%m-%d %H:%M:%S")}
with open(sys.argv[1], "w", encoding="utf-8") as fo:
    json.dump(out, fo, indent=2, ensure_ascii=False)
print(json.dumps(out, ensure_ascii=False))
