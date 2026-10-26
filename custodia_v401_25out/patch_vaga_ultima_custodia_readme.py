# -*- coding: utf-8 -*-
"""A VAGA FIXA «última custódia» na frente do README (25/10/2026, gerência a7, custódia v401; decisão estrutural L01 que o G1 deixa à
gerência no E08B). O handoff manda os parágrafos prontos «para o README do espelho e para o site», mas a frente vive a 1 byte do teto de
40.960 B e não tinha vaga: desde a v398 os parágrafos entram verbatim no ESTADO_ATUAL.md (gerar_estado_atual.py, pelo E04 do G1) e no site.

A troca: a seção «Read in this order» (638 B; a ordem medida já vive no read-brief e no ESTADO_ATUAL) vira «Latest custody», com o TÍTULO
do parágrafo pronto MAIS NOVO, lido do ESTADO_ATUAL.md por script (o bloco `<!-- INICIO_PARAGRAFO_<ID>_vNNN -->` de maior NNN), o link para
o parágrafo inteiro e a ordem de leitura em uma frase. O E08B confere exatamente esse título no README. Nada é digitado: a vaga se refaz
sozinha a cada versão. Trocas contadas; backup de bytes; py_compile; o gerador da frente roda depois (o assert do teto fica)."""
import os, py_compile, time
from pathlib import Path

G = Path(r"C:\IALD\Artigo\the_boundary\tools\gerar_readme_frente.py")
raw = G.read_bytes(); s = raw.decode("utf-8")
MARCA = "a VAGA FIXA «última custódia»"
if MARCA in s:
    raise SystemExit("já aplicado")
nl = "\r\n" if "\r\n" in s else "\n"

ANTIGA = ("## Read in this order · leia nesta ordem\n\n"
          "Smallest first; each file stands on its own. Real fetchers (measured 2026-09-19) cut documents near 100,000 characters, refuse files "
          "above 10 MB and do not read PDFs from GitHub raw — prefer the eight parts in [`secoes/`]({u_secoes}) and the TXT/TeX sources; the "
          "measured order is in [`ESTADO_ATUAL.md`]({u_estado}) and [`read-brief.md`]({site_brief}); the ledger is the **last** thing to read.\n")
NOVA = ("## Latest custody · última custódia\n\n"
        "**{_ULT}** — the ready paragraph, with its statutes, quotes and machine line, is in [`ESTADO_ATUAL.md`]({u_estado}) and on the site; "
        "the Unique Word Test panel stays at the top. Read smallest first: [`secoes/`]({u_secoes}), then `ESTADO_ATUAL.md` and "
        "[`read-brief.md`]({site_brief}); the ledger last.\n")
CODIGO = '''# 25/10/2026 (custódia v401; G1 E08B, L01): a VAGA FIXA «última custódia» — o TÍTULO do parágrafo pronto mais novo do handoff, lido do
# ESTADO_ATUAL.md (onde a custódia o embute verbatim, com os estatutos e a linha de máquina); o parágrafo inteiro fica lá e no site.
_est_txt = (RAIZ / 'ESTADO_ATUAL.md').read_text(encoding='utf-8')
_pars = [(int(m.group(2)), m.group(1)) for m in re.finditer(r'<!-- INICIO_PARAGRAFO_([A-Z0-9_]+?)_v(\\d+) -->', _est_txt)]
assert _pars, 'o ESTADO_ATUAL.md não traz parágrafo pronto — PARAR'
_nv, _nid = max(_pars)
_blc = _est_txt[_est_txt.index('<!-- INICIO_PARAGRAFO_%s_v%d -->' % (_nid, _nv)):]
_mt = re.search(r'^###\\s*(.+?)\\s*(?:\\u2014|-)\\s*par', _blc, re.M)
assert _mt, 'o parágrafo pronto mais novo não tem o título no molde «### <título> — parágrafo pronto» — PARAR'
_ULT = _mt.group(1).strip()
'''
ANCORA = "F = []\n"
a, b = ANTIGA.replace("\n", nl), NOVA.replace("\n", nl)
assert s.count(a) == 1, ("seção «Read in this order» mudou de forma — PARAR", s.count(a))
s = s.replace(a, b)
an = ANCORA.replace("\n", nl)
assert s.count(an) == 1, ("âncora F = [] não é única — PARAR", s.count(an))
s = s.replace(an, CODIGO.replace("\n", nl) + an)
G.with_name(G.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = G.with_name(G.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, G)
print("gerar_readme_frente.py: vaga «última custódia» | %d -> %d bytes" % (len(raw), G.stat().st_size))
