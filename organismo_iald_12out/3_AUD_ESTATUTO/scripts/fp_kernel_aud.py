# Impressao digital do tgl_kernel (SOMENTE LEITURA): mesma receita da construcao (metadados de todos os arquivos + conteudo das fontes fora de .lake)
import os, sys, hashlib, json, datetime
RAIZ = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/tgl_kernel"
DEST = "C:/IALD/Central de Patentes/work/organismo_iald_12out/3_AUD_ESTATUTO/medidas/IMPRESSAO_DIGITAL_KERNEL_" + sys.argv[1] + ".json"
meta, lean = [], []; n = 0; tot = 0
for dp, dns, fns in os.walk(RAIZ):
    dns.sort()
    for fn in sorted(fns):
        p = os.path.join(dp, fn); st = os.stat(p)
        rel = os.path.relpath(p, RAIZ).replace("\\", "/")
        meta.append(f"{rel}\t{st.st_size}\t{st.st_mtime_ns}"); n += 1; tot += st.st_size
        if not rel.startswith(".lake/") and (rel.endswith(".lean") or os.path.basename(rel) in ("lake-manifest.json", "lean-toolchain") or os.path.basename(rel).startswith("lakefile")):
            lean.append(f"{rel}\t{hashlib.sha256(open(p,'rb').read()).hexdigest()}")
meta.sort(); lean.sort()
out = {"quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "raiz": RAIZ, "n_arquivos": n, "bytes_total": tot,
       "sha256_metadados": hashlib.sha256("\n".join(meta).encode()).hexdigest(),
       "n_fontes_fora_lake": len(lean), "sha256_conteudo_fontes": hashlib.sha256("\n".join(lean).encode()).hexdigest()}
if n == 0: print("FALHA VISIVEL", file=sys.stderr); sys.exit(2)
json.dump(out, open(DEST, "w", encoding="utf-8"), indent=1)
print(json.dumps(out, indent=1))
