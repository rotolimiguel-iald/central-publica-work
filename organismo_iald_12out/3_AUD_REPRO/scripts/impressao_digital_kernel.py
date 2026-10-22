# -*- coding: utf-8 -*-
"""Impressao digital do tgl_kernel do Nos (SOMENTE LEITURA), mesmo metodo do levantamento do organismo:
sha256 da listagem ordenada (caminho\tsha256) de todo .lean fora de .lake + lakefile*/lake-manifest.json/lean-toolchain.
Tambem sha256 dos metadados (caminho, tamanho, mtime_ns) de TODOS os arquivos. Grava IMPRESSAO_DIGITAL_KERNEL_<rot>.json."""
import os, sys, hashlib, json, time, datetime
RAIZ = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/tgl_kernel"
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
meta, lean = [], []; nfiles = 0; total = 0
for dp, dns, fns in os.walk(RAIZ):
    dns.sort()
    for fn in sorted(fns):
        p = os.path.join(dp, fn); st = os.stat(p)
        rel = os.path.relpath(p, RAIZ).replace("\\", "/")
        meta.append(f"{rel}\t{st.st_size}\t{st.st_mtime_ns}"); nfiles += 1; total += st.st_size
        if not rel.startswith(".lake/") and (rel.endswith(".lean") or os.path.basename(rel) in ("lake-manifest.json", "lean-toolchain") or os.path.basename(rel).startswith("lakefile")):
            lean.append(f"{rel}\t{hashlib.sha256(open(p,'rb').read()).hexdigest()}")
meta.sort(); lean.sort()
out = {"quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "raiz": RAIZ, "n_arquivos": nfiles, "bytes_total": total,
       "sha256_metadados": hashlib.sha256("\n".join(meta).encode()).hexdigest(),
       "n_fontes_fora_lake": len(lean), "sha256_conteudo_fontes": hashlib.sha256("\n".join(lean).encode()).hexdigest()}
if nfiles == 0: print("FALHA VISIVEL: nenhum arquivo lido", file=sys.stderr); sys.exit(2)
rot = sys.argv[1] if len(sys.argv) > 1 else "x"
dest = os.path.join(AQUI, f"IMPRESSAO_DIGITAL_KERNEL_{rot}.json")
if os.path.exists(dest): print("FALHA VISIVEL: destino ja existe: "+dest, file=sys.stderr); sys.exit(2)
json.dump(out, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
