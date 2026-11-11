# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala, 10/11/2026 — conferência SENSÍVEL À CAIXA das aspas angulares da pedra contra os arquivos OPERADOR_*.txt
(a conferência usual ignora a caixa; o painel apontou «A Escala», PAR-11). Só lê. uso: python conferir_aspas_caixa.py [arquivo.lean]"""
import re, sys
from pathlib import Path
CUN = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
arq = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_09nov\R6_a_constante_da_escala\AEscala.lean")
norm = lambda s: re.sub(r"\s+", " ", s)
t = arq.read_text(encoding="utf-8")
corpus = norm("\n".join(p.read_text(encoding="utf-8", errors="replace") for p in sorted(CUN.glob("OPERADOR_*.txt"))))
corpus_low = corpus.lower()
def partes(q):
    n = norm(q).strip().rstrip(".,;: ")
    return [x.strip(" .,;:") for x in re.split(r"…|\[\.\.\.\]|\.\.\.", n) if x.strip(" .,;:")]
ang = re.findall("\u00ab([^\u00bb]*)\u00bb", t)
so_caixa, nao = [], []
for q in ang:
    ps = partes(q)
    if not ps:
        nao.append(q); continue
    if all(p in corpus for p in ps):
        continue
    if all(p.lower() in corpus_low for p in ps):
        so_caixa.append(q)
    else:
        nao.append(q)
print("arquivo:", arq.name, "| aspas angulares:", len(ang), "| verbatim exato:", len(ang) - len(so_caixa) - len(nao),
      "| so' a caixa difere:", len(so_caixa), "| nao verbatim:", len(nao))
from collections import Counter
for q, k in Counter(norm(x) for x in so_caixa).most_common():
    # onde, no corpus, está a forma em outra caixa
    p0 = partes(q)[0]
    i = corpus_low.find(p0.lower())
    print(f"  CAIXA x{k}: «{q[:110]}»  | no arquivo de fala: «{corpus[i:i+min(len(p0),110)]}»")
for q in nao:
    print("  NAO VERBATIM:", norm(q)[:140])
