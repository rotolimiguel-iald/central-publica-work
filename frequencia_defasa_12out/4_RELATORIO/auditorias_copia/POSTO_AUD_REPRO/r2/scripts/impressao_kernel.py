# -*- coding: utf-8 -*-
"""Impressao digital do tgl_kernel do Nos (SOMENTE LEITURA) -- auditor REPRO, rodada 2.

Implementacao propria da MESMA definicao usada pelos construtores (para comparar com
a15d5e02d4f22bd6 / ca632c47de569952):
  (a) metadados de TODOS os arquivos: "rel<TAB>tamanho<TAB>mtime_ns", ordenados, unidos por LF -> sha256
  (b) "rel<TAB>sha256(conteudo)" de todo .lean fora de .lake, ordenados, unidos por LF -> sha256
Acrescimo do auditor (mais forte): (c) sha256 do CONTEUDO de todo .olean em .lake/build/lib/lean/TGLExt.
Grava SO em <r2>/saidas; nunca sobrescreve.
"""
import hashlib, json, os, sys, time

RAIZ = "\\\\?\\C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\tgl_kernel"
SAIDAS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas")


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def main():
    rot = sys.argv[1]
    destino = os.path.join(SAIDAS, f"IMPRESSAO_KERNEL_{rot}.json")
    if os.path.exists(destino):
        print("FALHA VISIVEL: destino ja existe: " + destino, file=sys.stderr)
        return 2
    meta, lean, olean = [], [], []
    total = 0
    for dp, dns, fns in os.walk(RAIZ):
        for fn in fns:
            p = os.path.join(dp, fn)
            st = os.stat(p)
            rel = os.path.relpath(p, RAIZ).replace("\\", "/")
            meta.append(f"{rel}\t{st.st_size}\t{st.st_mtime_ns}")
            total += st.st_size
            if rel.endswith(".lean") and not rel.startswith(".lake/"):
                lean.append(f"{rel}\t{sha_file(p)}")
            if rel.startswith(".lake/build/lib/lean/TGLExt/") and rel.endswith(".olean"):
                olean.append(f"{rel}\t{sha_file(p)}")
    if not meta:
        print("FALHA VISIVEL: nada lido", file=sys.stderr)
        return 2
    meta.sort(); lean.sort(); olean.sort()
    out = {
        "quando_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "raiz": RAIZ,
        "n_arquivos": len(meta),
        "bytes_total": total,
        "sha256_metadados": hashlib.sha256("\n".join(meta).encode("utf-8")).hexdigest(),
        "n_lean_fora_lake": len(lean),
        "sha256_conteudo_lean": hashlib.sha256("\n".join(lean).encode("utf-8")).hexdigest(),
        "n_olean_TGLExt": len(olean),
        "sha256_conteudo_olean_TGLExt": hashlib.sha256("\n".join(olean).encode("utf-8")).hexdigest(),
    }
    with open(destino, "x", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
