# -*- coding: utf-8 -*-
# Consulta o KERNEL_INDICE.json por regex (nome ou texto ou arquivo). Uso: q_kernel.py <regex> [--file <regex>] [--kind theorem]
import json, re, sys, os
AQUI = os.path.dirname(os.path.abspath(__file__))
idx = json.load(open(os.path.join(AQUI, "KERNEL_INDICE.json"), encoding="utf-8"))
args = sys.argv[1:]
pat = re.compile(args[0], re.I) if args else re.compile(".")
fpat = None
kind = None
if "--file" in args:
    fpat = re.compile(args[args.index("--file") + 1], re.I)
if "--kind" in args:
    kind = args[args.index("--kind") + 1]
n = 0
for d in idx["declaracoes"]:
    if fpat and not fpat.search(d["file"]):
        continue
    if kind and d["kind"] != kind:
        continue
    if pat.search(d["qual"]) or pat.search(d["text"]):
        sha = idx["arquivos"][d["file"]]["sha16"]
        print(f'{d["file"]}:{d["line"]} [{sha}] {d["kind"]} {d["qual"]}  ||  {d["text"][:160]}')
        n += 1
print("total", n)
