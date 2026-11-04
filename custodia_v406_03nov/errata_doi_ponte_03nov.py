# -*- coding: utf-8 -*-
"""03/11/2026 19:0x, gerencia c1. ERRATA DO DOI DA PONTE nas fontes dos geradores do espelho the_boundary (achado do gerente central do LAR pelo orquestrador; MEDIDO por mim no DataCite
em 03/11/2026: 10.5281/zenodo.20999495 = «Um: Grande Atrator», criado 2026-06-28; 10.5281/zenodo.20630106 = «Nada pode ser puro, desde que seja mentira, porque nada e puro - A Ponte
Einstein - Cartan - Miguel», criado 2026-06-10; a casa ja' tinha a errata de 16/09 no Atlas e na memoria zenodo-um-absoluto; o site foi corrigido em 19/09; faltavam o README pinado, as
portas e o LEDGER). (1) tools/readme_pinado/readme_partes/citar.md: o DOI da entrada Miguel2026Ponte; (2) tools/gerar_portas.py: o doi do Artigo 2; (3) LEDGER.md: ERRATA AO LADO,
acrescentada no fim (o livro-razao nao se reescreve; a entrada BibTeX antiga fica como registro). Os artefatos SELADOS da versao «Um (absoluto) — Grande Atrator» nao sao tocados (a errata
deles vive ao lado, no Atlas). Troca em bytes com backup .bak_<ts>_errata_doi; temporario + os.replace; CRLF/LF preservados. Depois: gerar_portas.py, primordial.py + readme_pinado.py
--gerar e --verificar (por fora, no Bash). Escrito pelo Write."""
import os, time
TB = r"C:\IALD\Artigo\the_boundary"; TS = time.strftime("%Y%m%d_%H%M%S")
VELHO = b"10.5281/zenodo.20999495"; NOVO = b"10.5281/zenodo.20630106"


def troca(arq, o, n, esperado):
    b = open(arq, "rb").read(); assert b.count(o) == esperado, (arq, b.count(o), esperado)
    novo = b.replace(o, n); bak = arq + ".bak_%s_errata_doi" % TS; open(bak, "xb").write(b); assert open(bak, "rb").read() == b
    tmp = arq + ".tmp_" + TS; open(tmp, "xb").write(novo); assert os.path.getsize(tmp) == len(novo); os.replace(tmp, arq); assert open(arq, "rb").read() == novo
    assert b.count(b"\r\n") == novo.count(b"\r\n"); print("%s: %d -> %d B; backup %s" % (os.path.relpath(arq, TB), len(b), len(novo), os.path.basename(bak)))


# (1) a parte do README pinado (so' a entrada Miguel2026Ponte traz o DOI velho)
troca(os.path.join(TB, "tools", "readme_pinado", "readme_partes", "citar.md"), VELHO, NOVO, 1)
# (2) o gerador das portas (o doi do Artigo 2)
troca(os.path.join(TB, "tools", "gerar_portas.py"), b'doi="https://doi.org/10.5281/zenodo.20999495"', b'doi="https://doi.org/10.5281/zenodo.20630106"', 1)
# (3) o LEDGER: errata ao lado, no fim
led = os.path.join(TB, "LEDGER.md"); b = open(led, "rb").read(); nl = b"\r\n" if b.count(b"\r\n") > b.count(b"\n") // 2 else b"\n"
assert b.count(VELHO) == 1, b.count(VELHO)
txt = ("\n\n### Erratum beside the ledger (2026-11-03): the DOI of Article 2 (A Ponte)\n\n"
       "The BibTeX entry `Miguel2026Ponte` above, and the README of this mirror up to commit `ff882f81`, cited `10.5281/zenodo.20999495`. "
       "DataCite registers that DOI as **«Um: Grande Atrator»** (created 2026-06-28). The DOI of *A Ponte Einstein–Cartan–Miguel* is "
       "**`10.5281/zenodo.20630106`** («Nada pode ser puro, desde que seja mentira, porque nada é puro — A Ponte Einstein–Cartan–Miguel», registered 2026-06-10). "
       "Measured on DataCite on 2026-11-03 by the management session (c1) after the LAR manager found it through the orchestrator; the house already carried this erratum "
       "in the Atlas and in the memory `zenodo-um-absoluto` since 2026-09-16, and the site was corrected on 2026-09-19. On 2026-11-03 the sources of the generators were corrected "
       "(`tools/readme_pinado/readme_partes/citar.md`, `tools/gerar_portas.py`); the README and the portals follow at the next regeneration. The sealed artifacts of the version "
       "«Um (absoluto) — Grande Atrator» keep the old string; this erratum stands beside them. The entry above is kept as record: the ledger is not rewritten.\n")
novo = b.rstrip(b"\r\n") + txt.replace("\n", nl.decode()).encode("utf-8") + nl
bak = led + ".bak_%s_errata_doi" % TS; open(bak, "xb").write(b); assert open(bak, "rb").read() == b
tmp = led + ".tmp_" + TS; open(tmp, "xb").write(novo); assert os.path.getsize(tmp) == len(novo) > len(b); os.replace(tmp, led); assert open(led, "rb").read() == novo
print("LEDGER.md: %d -> %d B (errata ao lado no fim); backup %s" % (len(b), len(novo), os.path.basename(bak)))
