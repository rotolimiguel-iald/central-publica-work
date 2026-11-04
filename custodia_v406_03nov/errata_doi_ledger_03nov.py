# -*- coding: utf-8 -*-
"""03/11/2026 19:0x, gerencia c1. A parte (3) da errata do DOI da Ponte: o LEDGER.md do espelho cita o DOI velho TRES vezes (a linha dos depositos independentes, a entrada BibTeX e mais uma);
o livro-razao nao se reescreve: a errata vai AO LADO, no fim, e diz que as tres mencoes acima ficam como registro. Bytes com backup; CRLF/LF preservados. Escrito pelo Write."""
import os, time
TB = r"C:\IALD\Artigo\the_boundary"; TS = time.strftime("%Y%m%d_%H%M%S"); VELHO = b"10.5281/zenodo.20999495"
led = os.path.join(TB, "LEDGER.md"); b = open(led, "rb").read(); nl = b"\r\n" if b.count(b"\r\n") > b.count(b"\n") // 2 else b"\n"
n_velho = b.count(VELHO); assert n_velho >= 1 and b"Erratum beside the ledger (2026-11-03)" not in b, n_velho
txt = ("\n\n### Erratum beside the ledger (2026-11-03): the DOI of Article 2 (A Ponte)\n\n"
       "This ledger cites `10.5281/zenodo.20999495` %d times above (the line of the independent deposits, the BibTeX entry `Miguel2026Ponte` and its copies), and the README of this mirror "
       "did the same up to commit `ff882f81`. DataCite registers that DOI as **«Um: Grande Atrator»** (created 2026-06-28). The DOI of *A Ponte Einstein–Cartan–Miguel* is "
       "**`10.5281/zenodo.20630106`** («Nada pode ser puro, desde que seja mentira, porque nada é puro — A Ponte Einstein–Cartan–Miguel», registered 2026-06-10). "
       "Measured on DataCite on 2026-11-03 by the management session (c1) after the LAR manager found it through the orchestrator; the house already carried this erratum in the Atlas and in the "
       "memory `zenodo-um-absoluto` since 2026-09-16, and the site was corrected on 2026-09-19. On 2026-11-03 the sources of the generators were corrected (`tools/readme_pinado/readme_partes/citar.md`, "
       "`tools/gerar_portas.py`); the README and the portals follow from the regeneration. The sealed artifacts of the version «Um (absoluto) — Grande Atrator» keep the old string; this erratum stands "
       "beside them. The mentions above are kept as record: the ledger is not rewritten.\n" % n_velho)
novo = b.rstrip(b"\r\n") + txt.replace("\n", nl.decode()).encode("utf-8") + nl
bak = led + ".bak_%s_errata_doi" % TS; open(bak, "xb").write(b); assert open(bak, "rb").read() == b
tmp = led + ".tmp_" + TS; open(tmp, "xb").write(novo); assert os.path.getsize(tmp) == len(novo) > len(b); os.replace(tmp, led); assert open(led, "rb").read() == novo
print("LEDGER.md: %d -> %d B (errata ao lado no fim; %d mencoes antigas ficam); backup %s" % (len(b), len(novo), n_velho, os.path.basename(bak)))
