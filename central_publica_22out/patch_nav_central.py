# -*- coding: utf-8 -*-
"""O acesso à Central pública no menu da home do site (22/10/2026): um item «The Central / A Central» depois de «Research Lines / Linhas
de Pesquisa», que abre o modo interativo (central/). index.html + i18n.js. Backup de BYTES; trocas conferidas; idempotente."""
import os, time
from pathlib import Path

V3 = Path(r"C:\IALD\Site\tgl\v3.0")
TS = time.strftime("%Y%m%d_%H%M%S")


def patch(p, pares, marca):
    raw = p.read_bytes()
    s = raw.decode("utf-8")
    if marca in s:
        print("já aplicado:", p.name); return
    for a, b in pares:
        assert s.count(a) == 1, (p.name, s.count(a), a[:70])
        s = s.replace(a, b)
    p.with_name(p.name + ".bak_" + TS).write_bytes(raw)
    t = p.with_name(p.name + ".tmp_nav")
    t.write_bytes(s.encode("utf-8"))
    assert t.stat().st_size > len(raw)
    os.replace(t, p)
    print("ok", p.name, len(raw), "->", p.stat().st_size)


patch(V3 / "index.html", [('<a href="linhas-de-pesquisa.html" data-i18n="nav.lines">Research Lines</a>',
                           '<a href="linhas-de-pesquisa.html" data-i18n="nav.lines">Research Lines</a><a href="central/" data-i18n="nav.central">The Central</a>')],
      'data-i18n="nav.central"')
patch(V3 / "i18n.js", [("'nav.lines':'Research Lines',", "'nav.lines':'Research Lines','nav.central':'The Central',"),
                       ("'nav.lines':'Linhas de Pesquisa',", "'nav.lines':'Linhas de Pesquisa','nav.central':'A Central',")],
      "'nav.central'")
