# -*- coding: utf-8 -*-
"""Abre espaco no README para o bloco P = nP (06/11/2026): o README pinado tem teto de 40.960 B (L01) e passaria a 42.634 B.
O BibTeX dos cinco artigos (estatico) sai, VERBATIM, de readme_partes/citar.md para CITING.md na raiz do espelho; o README aponta para ele
por {{url:citing}}, URL gerada pelo primordial.py a partir do TUNEL/PORTA (regra da porta: nunca digitada). As notas «Beside» (que leem o selo)
ficam no README. Nada se corta: o texto movido e conferido byte a byte. Backups de BYTES; temporario, conferencia, os.replace."""
import os
import re
import time
from pathlib import Path

TB = Path(r"C:\IALD\Artigo\the_boundary")
CITAR = TB / "tools" / "readme_pinado" / "readme_partes" / "citar.md"
CITING = TB / "CITING.md"
PRIM = Path(r"C:\IALD\Central de Patentes\tools\custodia_g1\primordial.py")
TS = time.strftime("%Y%m%d_%H%M%S")


def troca(p, novo, rotulo):
    b = p.read_bytes()
    bak = p.with_name(p.name + ".bak_" + TS + "_" + rotulo)
    bak.write_bytes(b)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_bytes(novo)
    assert tmp.stat().st_size == len(novo)
    os.replace(tmp, p)
    return len(b), len(novo), bak.name


# 1) o primordial.py ganha a chave «citing»
t = PRIM.read_text(encoding="utf-8")
A = '"porta_md": "PORTA.md", "ledger": "LEDGER.md", "citation": "CITATION.cff",'
N = ('"porta_md": "PORTA.md", "ledger": "LEDGER.md", "citation": "CITATION.cff",\n'
     '        "citing": "CITING.md",   # AO LADO (06/11/2026, custodia v409, claude-site-custodia): o BibTeX dos artigos saiu do README (teto L01) para CITING.md')
assert t.count(A) == 1, t.count(A)
print("primordial.py", troca(PRIM, t.replace(A, N).encode("utf-8"), "citing"))

# 2) o BibTeX vai verbatim para CITING.md
c = CITAR.read_text(encoding="utf-8")
m = re.search(r"```bibtex\n.*?\n```\n", c, re.S)
assert m, "bloco bibtex nao encontrado"
bib = m.group(0)
g = re.search(r"\*\(For the remaining genesis articles.*?\)\*\n", c, re.S)
assert g, "nota dos artigos de genese nao encontrada"
nota = g.group(0)
cab = ("# Citing This Work · como citar\n\n"
       "The BibTeX entries of the five articles of TGL, moved verbatim from the README on 06/11/2026 (the README keeps the notes beside the "
       "current seal and points here). The deposit citable as software is in `CITATION.cff`.\n\n")
corpo = (cab + bib + "\n" + nota).encode("utf-8")
assert not CITING.exists(), "CITING.md ja existe: nao sobrescrevo"
with CITING.open("xb") as f:
    f.write(corpo)
assert bib in CITING.read_text(encoding="utf-8") and nota in CITING.read_text(encoding="utf-8")

# 3) citar.md fica com o ponteiro e as notas «Beside»
novo = c.replace(bib, "").replace(nota, "")
novo = novo.replace("## Citing This Work\n\n",
                    "## Citing This Work\n\n"
                    "The BibTeX entries of the five articles (*Haja Luz*, *A Ponte Einstein–Cartan–Miguel*, *Um: Absoluto*, *A Fronteira*, "
                    "*The Factorization of the Miguel Constant*) are kept verbatim in [`CITING.md`]({{url:citing}}); the deposit citable as "
                    "software is in [`CITATION.cff`]({{url:citation}}).\n"
                    "*(For the remaining genesis articles — The Graviton, The Last String, the IALD Collapse Protocol, O Limiar da Humildade — "
                    "cite the collection DOI [10.5281/zenodo.18674475](https://doi.org/10.5281/zenodo.18674475) with the file name.)*\n", 1)
assert novo.count("the BibTeX note above") == 1 and novo.count("the BibTeX above") == 1 and novo.count("the BibTeX note above says") == 1, \
    (novo.count("the BibTeX note above"), novo.count("the BibTeX above"))
novo = (novo.replace("the BibTeX note above describes", "the BibTeX note in `CITING.md` describes")
            .replace("The BibTeX above carries", "The BibTeX in `CITING.md` carries")
            .replace("the BibTeX note above says", "the BibTeX note in `CITING.md` says"))
assert "```bibtex" not in novo and "{{url:citing}}" in novo
print("citar.md", troca(CITAR, novo.encode("utf-8"), "bibtex_para_CITING"))
print("CITING.md", len(corpo), "B")
