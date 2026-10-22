# -*- coding: utf-8 -*-
# Auditor REPRO: impressao digital do tgl_kernel do Nos (SO LEITURA), mesmo metodo do pre-registrador
# (metadados de todos os arquivos + sha256 do conteudo de todo .lean fora de .lake). Grava so na pasta do auditor.
import os, sys, hashlib, json, time
RAIZ = "\\\\?\\C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\tgl_kernel"
SAIDA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas")
meta, lean = [], []
nfiles = 0
total = 0
for dp, dns, fns in os.walk(RAIZ):
    dns.sort()
    for fn in sorted(fns):
        p = os.path.join(dp, fn)
        st = os.stat(p)
        rel = os.path.relpath(p, RAIZ).replace("\\", "/")
        meta.append(f"{rel}\t{st.st_size}\t{st.st_mtime_ns}")
        nfiles += 1
        total += st.st_size
        if rel.endswith(".lean") and not rel.startswith(".lake/"):
            with open(p, "rb") as fh:
                lean.append(f"{rel}\t{hashlib.sha256(fh.read()).hexdigest()}")
meta.sort()
lean.sort()
out = {"quando_local": time.strftime("%Y-%m-%d %H:%M:%S"), "n_arquivos": nfiles, "bytes_total": total,
       "sha256_metadados": hashlib.sha256("\n".join(meta).encode("utf-8")).hexdigest(),
       "n_lean_fora_lake": len(lean),
       "sha256_conteudo_lean": hashlib.sha256("\n".join(lean).encode("utf-8")).hexdigest()}
if nfiles == 0:
    print("FALHA VISIVEL: nenhum arquivo", file=sys.stderr)
    sys.exit(2)
rot = sys.argv[1]
dest = os.path.join(SAIDA, f"IMPRESSAO_KERNEL_{rot}.json")
if os.path.exists(dest):
    print("FALHA VISIVEL: destino existe", file=sys.stderr)
    sys.exit(2)
with open(dest, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
