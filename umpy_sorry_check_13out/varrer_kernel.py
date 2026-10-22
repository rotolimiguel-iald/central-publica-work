# -*- coding: utf-8 -*-
"""Mede (so leitura) a cobertura da varredura lexical do um.py (_lean_source_forbidden_tokens,
os.listdir NAO recursivo em TGL/ e TGLExt/) contra a arvore inteira do kernel em disco, e procura
os tokens proibidos fora de comentarios/strings em TODOS os .lean (recursivo)."""
import json, os, re, sys
from pathlib import Path

def strip_comments(src):
    # remove comentarios de bloco /- ... -/ (aninhados) e de linha -- ; e strings "..."
    out, i, depth, n = [], 0, 0, len(src)
    while i < n:
        if src.startswith("/-", i):
            depth += 1; i += 2; continue
        if depth and src.startswith("-/", i):
            depth -= 1; i += 2; continue
        if depth:
            out.append("\n" if src[i] == "\n" else " "); i += 1; continue
        if src.startswith("--", i):
            while i < n and src[i] != "\n":
                i += 1
            continue
        if src[i] == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            out.append('""'); i = j + 1; continue
        out.append(src[i]); i += 1
    return "".join(out)


K = Path(r"C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel")
OUT = Path(r"C:/IALD/Central de Patentes/work/umpy_sorry_check_13out")
TOK = ["sorry", "admit", "axiom", "native_decide", "unsafe"]
covered, all_files = set(), []
for lib in ("TGL", "TGLExt"):
    d = K / lib
    for nm in sorted(os.listdir(d)):
        if nm.endswith(".lean") and not nm.startswith("Probe"):
            covered.add((d / nm).resolve())
for lib in ("TGL", "TGLExt"):
    for p in sorted((K / lib).rglob("*.lean")):
        all_files.append(p.resolve())
not_cov = [p for p in all_files if p not in covered and not p.name.startswith("Probe")]
hits = []
for p in all_files:
    code = strip_comments(p.read_text(encoding="utf-8"))
    for t in TOK:
        if re.search(r"\b%s\b" % re.escape(t), code):
            hits.append([str(p.relative_to(K)), t, p in covered])
res = {"kernel_dir": str(K), "n_lean_recursive": len(all_files), "n_covered_by_lexical_scan": len(covered),
       "n_not_covered": len(not_cov), "not_covered_dirs": sorted({str(p.parent.relative_to(K)) for p in not_cov}),
       "forbidden_hits_recursive": hits}
(OUT / "cobertura_varredura_lexical.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in res.items()}, ensure_ascii=False, indent=1)[:3000])
