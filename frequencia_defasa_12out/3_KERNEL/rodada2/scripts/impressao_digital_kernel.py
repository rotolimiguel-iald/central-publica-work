# -*- coding: utf-8 -*-
# Impressao digital do tgl_kernel do Nos (SOMENTE LEITURA) -- mesmo metodo do levantamento
# (0_LEVANTAMENTO\impressao_digital_kernel.py), para que os numeros sejam comparaveis.
# (a) metadados de TODOS os arquivos: (caminho relativo, tamanho, mtime_ns) -> sha256 da listagem ordenada
# (b) sha256 do CONTEUDO de todo .lean fora de .lake -> sha256 da listagem ordenada
# Grava SO dentro de 3_KERNEL\rodada2 (copia do script da rodada 1, so com a pasta de saida trocada).
import os, sys, hashlib, json, time
RAIZ = "\\\\?\\C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\tgl_kernel"
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # rodada2 (saida na raiz da rodada)
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
                h = hashlib.sha256(fh.read()).hexdigest()
            lean.append(f"{rel}\t{h}")
meta.sort()
lean.sort()
out = {
    "quando_local": time.strftime("%Y-%m-%d %H:%M:%S"),
    "raiz": RAIZ,
    "n_arquivos": nfiles,
    "bytes_total": total,
    "sha256_metadados": hashlib.sha256("\n".join(meta).encode("utf-8")).hexdigest(),
    "n_lean_fora_lake": len(lean),
    "sha256_conteudo_lean": hashlib.sha256("\n".join(lean).encode("utf-8")).hexdigest(),
}
if nfiles == 0:
    print("FALHA VISIVEL: nenhum arquivo lido na raiz do kernel", file=sys.stderr)
    sys.exit(2)
rot = sys.argv[1] if len(sys.argv) > 1 else "x"
destino = os.path.join(AQUI, f"IMPRESSAO_DIGITAL_KERNEL_{rot}.json")
if os.path.exists(destino):
    print("FALHA VISIVEL: destino ja existe (nao sobrescrevo): " + destino, file=sys.stderr)
    sys.exit(2)
with open(destino, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
