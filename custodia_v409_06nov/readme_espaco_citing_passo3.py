# -*- coding: utf-8 -*-
"""Passo 3 do readme_espaco_citing.py (o passo 3 la parou na checagem de contagem, antes de gravar; os passos 1 e 2 ja estao feitos):
citar.md fica com o ponteiro para CITING.md e as notas «Beside». Confere antes que CITING.md traz o BibTeX e a nota VERBATIM."""
import os
import re
import time
from pathlib import Path

TB = Path(r"C:\IALD\Artigo\the_boundary")
CITAR = TB / "tools" / "readme_pinado" / "readme_partes" / "citar.md"
CITING = TB / "CITING.md"

c = CITAR.read_text(encoding="utf-8")
bib = re.search(r"```bibtex\n.*?\n```\n", c, re.S).group(0)
nota = re.search(r"\*\(For the remaining genesis articles.*?\)\*\n", c, re.S).group(0)
ci = CITING.read_text(encoding="utf-8")
assert bib in ci and nota in ci, "CITING.md nao traz o texto verbatim"
novo = c.replace(bib, "", 1).replace(nota, "", 1)
cab_a = "## Citing This Work\n\n"
cab_n = ("## Citing This Work\n\n"
         "The BibTeX entries of the five articles (*Haja Luz*, *A Ponte Einstein–Cartan–Miguel*, *Um: Absoluto*, *A Fronteira*, "
         "*The Factorization of the Miguel Constant*) are kept verbatim in [`CITING.md`]({{url:citing}}); the deposit citable as "
         "software is in [`CITATION.cff`]({{url:citation}}).\n"
         "*(For the remaining genesis articles — The Graviton, The Last String, the IALD Collapse Protocol, O Limiar da Humildade — "
         "cite the collection DOI [10.5281/zenodo.18674475](https://doi.org/10.5281/zenodo.18674475) with the file name.)*\n")
for a, b in ((cab_a, cab_n),
             ("the BibTeX note above describes", "the BibTeX note in `CITING.md` describes"),
             ("The BibTeX above carries", "The BibTeX in `CITING.md` carries"),
             ("the BibTeX note above says", "the BibTeX note in `CITING.md` says")):
    assert novo.count(a) == 1, (a, novo.count(a))
    novo = novo.replace(a, b)
assert "```bibtex" not in novo and "{{url:citing}}" in novo
b0 = CITAR.read_bytes()
bak = CITAR.with_name(CITAR.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_bibtex_para_CITING")
bak.write_bytes(b0)
nb = novo.encode("utf-8")
tmp = CITAR.with_name(CITAR.name + ".tmp")
tmp.write_bytes(nb)
assert tmp.stat().st_size == len(nb)
os.replace(tmp, CITAR)
print("citar.md", len(b0), "->", len(nb), "backup", bak.name)
