# -*- coding: utf-8 -*-
"""Mede (SÓ LEITURA) quanto do work/ e da bancada Chatgpt/ é CÓDIGO e RESULTADO publicável num repositório git (22/10/2026).
Regra de seleção (rascunho): extensões de código/texto/resultado; arquivo <= 25 MB; fora .bak_/.tmp, venvs, builds, caches binários
(fits/npy/npz/h5/sqlite/db/zip/tar/7z), e-mails; dados pessoais são varridos DEPOIS, arquivo a arquivo."""
import json, os, sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
C = Path(r"C:\IALD\Central de Patentes")
TXT = {".py", ".lean", ".md", ".json", ".jsonl", ".txt", ".tex", ".csv", ".tsv", ".toml", ".yaml", ".yml", ".js", ".mjs", ".ts", ".tsx",
       ".html", ".css", ".ipynb", ".sh", ".ps1", ".bat", ".cfg", ".ini", ".sql", ".bib", ".sty", ".cls", ".r", ".jl", ".c", ".h", ".cpp",
       ".rs", ".go", ".java", ".svg", ".xml", ".dat", ".log", ".out", ".diff", ".patch", ".lean4", ".pysnip", ".spec"}
FIG = {".png", ".pdf", ".jpg", ".jpeg", ".gif", ".webp"}
EXCL_DIR = {".git", ".venv", "venv", "node_modules", "__pycache__", ".lake", "tex_environment", ".wheels_ipv4", "unsloth_compiled_cache",
            "site-packages", "dist-packages", ".mypy_cache", ".pytest_cache", "build", ".cache"}
LIM = 25 * 1024 * 1024


def medir(base, it=None):
    sel_n = sel_b = 0; fig_n = fig_b = 0; fora = Counter(); fora_b = Counter()
    for dp, dns, fns in (it if it is not None else os.walk(base)):
        dns[:] = [d for d in dns if d not in EXCL_DIR]
        for f in fns:
            e = os.path.splitext(f)[1].lower()
            p = os.path.join(dp, f)
            try:
                s = os.path.getsize(p)
            except OSError:
                continue
            if ".bak_" in f or ".tmp" in f:
                fora["backup/tmp"] += 1; fora_b["backup/tmp"] += s; continue
            if s > LIM:
                fora[">25MB"] += 1; fora_b[">25MB"] += s; continue
            if e in TXT:
                sel_n += 1; sel_b += s
            elif e in FIG:
                fig_n += 1; fig_b += s
            else:
                fora["outros:" + (e or "(sem)")] += 1; fora_b["outros:" + (e or "(sem)")] += s
    return sel_n, sel_b, fig_n, fig_b, fora, fora_b


for nome in ("work", "Chatgpt"):
    sn, sb, fn, fb, fo, fob = medir(C / nome)
    print("%-8s texto/código: %d arquivos, %.2f GB | figuras/pdf: %d, %.2f GB | fora: %s" % (
        nome, sn, sb / 2**30, fn, fb / 2**30, ", ".join("%s %d (%.1f GB)" % (k, fo[k], fob[k] / 2**30) for k, _ in fob.most_common(6))))
