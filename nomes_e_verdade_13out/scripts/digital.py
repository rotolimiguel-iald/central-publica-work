# -*- coding: utf-8 -*-
"""Nomes e Verdade (13/10): impressao digital do tgl_kernel do Nos, SOMENTE LEITURA, sem seguir juncoes nem links.
Mesma receita do digital.py da R3 do motor (sha256 dos metadados rel/tamanho/mtime_ns de todo arquivo alcancado;
sha256 do conteudo dos .lean fora de .lake + lakefile*/lake-manifest.json/lean-toolchain; sha256 do conteudo de todo
.olean de .lake/build/lib/lean/TGLExt). Uso: digital.py <rotulo>  (grava medidas/DIGITAL_KERNEL_<rotulo>.json)."""
import os, sys, hashlib, json, datetime

RAIZ = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s/tgl_kernel"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "medidas")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for ch in iter(lambda: fh.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def walk(raiz):
    pilha = [raiz]
    while pilha:
        d = pilha.pop()
        with os.scandir(d) as it:
            ents = sorted(it, key=lambda e: e.name)
        for e in ents:
            if e.is_symlink() or os.path.isjunction(e.path):
                yield ("LINK", e.path)
                continue
            if e.is_dir(follow_symlinks=False):
                pilha.append(e.path)
            else:
                yield ("F", e.path)


meta, fontes, oleans, links = [], [], [], []
n = 0
tot = 0
for kind, p in walk(RAIZ):
    rel = os.path.relpath(p, RAIZ).replace("\\", "/")
    if kind == "LINK":
        links.append(rel)
        continue
    st = os.stat(p, follow_symlinks=False)
    meta.append(f"{rel}\t{st.st_size}\t{st.st_mtime_ns}")
    n += 1
    tot += st.st_size
    b = os.path.basename(rel)
    if not rel.startswith(".lake/") and (rel.endswith(".lean") or b in ("lake-manifest.json", "lean-toolchain") or b.startswith("lakefile")):
        fontes.append(f"{rel}\t{sha(p)}")
    if rel.startswith(".lake/build/lib/lean/TGLExt/") and rel.endswith(".olean"):
        oleans.append(f"{rel}\t{sha(p)}")
if n == 0:
    print("FALHA VISIVEL: nada lido")
    sys.exit(2)
meta.sort(); fontes.sort(); oleans.sort(); links.sort()
out = {"quem": "construtor Nomes e Verdade 13/10",
       "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "raiz": RAIZ,
       "n_arquivos": n, "bytes_total": tot, "links_ou_juncoes_nao_seguidos": links,
       "sha256_metadados": hashlib.sha256("\n".join(meta).encode()).hexdigest(),
       "n_fontes_fora_lake": len(fontes), "sha256_conteudo_fontes": hashlib.sha256("\n".join(fontes).encode()).hexdigest(),
       "n_olean_TGLExt": len(oleans), "sha256_conteudo_olean_TGLExt": hashlib.sha256("\n".join(oleans).encode()).hexdigest()}
rot = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
dest = os.path.join(OUT, "DIGITAL_KERNEL_" + rot + ".json")
if os.path.exists(dest):
    print("FALHA VISIVEL: ja existe " + dest)
    sys.exit(2)
json.dump(out, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "links_ou_juncoes_nao_seguidos"}, ensure_ascii=False, indent=1))
print("links:", links)
