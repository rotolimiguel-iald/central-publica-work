# -*- coding: utf-8 -*-
"""A frente do espelho no teto de 40 KB (ordem de 11/09; LIMITE = 40*1024). Com o item do 4,44 a frente passou a 41.542 B.
Apertos editoriais na PROSA do gerador (tools/gerar_readme_frente.py) — a frente é regenerada inteira a cada custódia, não é
superfície append-only; nenhum número, URL, estatuto, errata ou verbatim muda; os guardas (termos proibidos, URLs do TUNEL/PORTA,
marcas, CONFIRMED/NOT_FALSIFIED presentes) seguem rodando. Trocas contadas (==1); backup de bytes; py_compile antes de substituir."""
import os, py_compile, re, time
from pathlib import Path

P = Path("C:/IALD/Artigo/the_boundary/tools/gerar_readme_frente.py")
TS = time.strftime("%Y%m%d_%H%M%S")
raw = P.read_bytes()
s = raw.decode("utf-8")
MARCA = "The full paragraph, verbatim: [`ESTADO_ATUAL.md`]"
if MARCA in s:
    raise SystemExit("já aplicado")


def troca(old, new, rot):
    global s
    n = s.count(old)
    assert n == 1, (rot, n, old[:80])
    s = s.replace(old, new)
    print("  ok  %-28s %+d" % (rot, len(new.encode("utf-8")) - len(old.encode("utf-8"))))


troca("# the rite: materializes the Lean kernel, builds it, audits every theorem, re-derives the chain, emits the article",
      "# the rite: builds the Lean kernel, audits every theorem, re-derives the chain, emits the article", "comentário do rito")
troca("GitHub does **not render** files above 5 MB — the blob page looks empty; the raw URL serves the whole file, byte-exact. To reproduce",
      "GitHub does **not render** files above 5 MB (the blob page looks empty; the raw URL serves the whole file). To reproduce", "nota do Range")
troca("the single entry point: the theory in eight short parts, each with its verbatim sources, in [`secoes/`]({u_secoes}) (the answer sits in the first 2 KB of each part) · then [`ESTADO_ATUAL.md`]({u_estado}) (one page from the seal: pin, gate, what is PROVED, what is not, how to reproduce) · the site: {site}",
      "the single entry point: the theory in eight short parts with their verbatim sources, in [`secoes/`]({u_secoes}) (the answer sits in the first 2 KB of each part) · then [`ESTADO_ATUAL.md`]({u_estado}) (one page from the seal: pin, gate, what is PROVED and what is not) · the site: {site}", "comece aqui")
troca("Every folder has a `PORTA.md` + `PORTA.json` (the rule of the door: no door is a dead end); the flat index of every file, with URL, size and hash, is",
      "Every folder has a `PORTA.md` + `PORTA.json` (no door is a dead end); the flat index of every file (URL, size, hash) is", "regra da porta")
troca("Smallest first; each file stands on its own. Measured on 2026-09-19 with one real fetcher: documents are cut near 100,000 characters, files above 10 MB are refused, and PDFs served by GitHub raw as `application/octet-stream` are not read — prefer the eight parts in [`secoes/`]({u_secoes}) and the TXT/TeX sources. The measured order is in [`ESTADO_ATUAL.md`]({u_estado}) (*Reading order*) and in [`read-brief.md`]({site_brief}). The full ledger below is the **last** thing to read.",
      "Smallest first; each file stands on its own. Real fetchers (measured 2026-09-19) cut documents near 100,000 characters, refuse files above 10 MB and do not read PDFs from GitHub raw — prefer the eight parts in [`secoes/`]({u_secoes}) and the TXT/TeX sources; the measured order is in [`ESTADO_ATUAL.md`]({u_estado}) and [`read-brief.md`]({site_brief}); the ledger is the **last** thing to read.", "leia nesta ordem")
troca(r"""F.append('\n> **Read the Abstract below under the current ruler.** It is copied verbatim from the ledger (append-only), so it keeps older sentences such as *Never "quantum gravity proved."*. The current status is the line at the top of this page.\n')""",
      r"""F.append('\n> **Read the Abstract below under the current ruler.** It is copied verbatim from the append-only ledger, so it keeps older sentences; the current status is the line at the top of this page.\n')""", "nota do Abstract")
troca(" — the atlas of the boundary: every claim with its status, every status with the file where it is read, the seals, the refutations and the false positives that did not pass, the reading protocol, the thematic atlas and the raw file index (now ",
      " — the atlas of the boundary: claims with status and source file, seals, refutations and false positives, reading protocol, thematic atlas, raw file index (now ", "o livro-razão (a)")
troca("). It is kept **byte-exact** and append-only: nothing was removed when this front page was generated. The raw file index it carries is superseded by [`TUNEL.json`]({raw_base}TUNEL.json) / [`TUNEL.md`]({raw_base}TUNEL.md), which are regenerated at every custody.",
      "). Byte-exact, append-only; its raw file index is superseded by [`TUNEL.json`]({raw_base}TUNEL.json) / [`TUNEL.md`]({raw_base}TUNEL.md), regenerated at every custody.", "o livro-razão (b)")

# o item do 4,44, mais curto — e inteiro na regra: z_disc com o p calibrado e a linha dos 5σ no MESMO item
rx = re.compile(r"    F\.append\('\\n> \*\*The Unique Word Test.*?u_estado\)\)\n", re.S)
ms = rx.findall(s)
assert len(ms) == 1, len(ms)
novo = ("    F.append('\\n> **The Unique Word Test (%s, %s) `[REAL: read from the sealed registry %s]`:** z_disc = %.2f (calibrated; one-sided p %.1e), '\n"
        "             'below the 5σ step of accreditation, which was not reached (%.2f < 5); z_δ = %.2f (two-sided p %.2f; prior power %.2fσ): '\n"
        "             '`NOT_FALSIFIED_POWERED`; ln B(TGL/ΛCDM) = %.2f (not a σ). `NOT_FALSIFIED` is not accreditation; not blind to the data; the gate does not move. '\n"
        "             'The full paragraph, verbatim: [`ESTADO_ATUAL.md`](%s).\\n'\n"
        "             % (versao, data, _k, _l['z_disc_calibrado'], _l['p_disc_unilateral'], _l['z_disc_calibrado'], _l['z_delta_calibrado'],\n"
        "                _l['p_delta_bilateral'], _l['poder_previo'], _l['lnB_lcdm'], u_estado))\n")
print("  ok  %-28s %+d" % ("item do 4,44", len(novo.encode("utf-8")) - len(ms[0].encode("utf-8"))))
s = s.replace(ms[0], novo)
assert MARCA in s

P.with_name(P.name + ".bak_" + TS).write_bytes(raw)
t = P.with_name(P.name + ".tmp")
t.write_bytes(s.encode("utf-8"))
py_compile.compile(str(t), doraise=True)
os.replace(t, P)
print("gerar_readme_frente.py: apertos aplicados | %d -> %d bytes | backup .bak_%s" % (len(raw), P.stat().st_size, TS))
