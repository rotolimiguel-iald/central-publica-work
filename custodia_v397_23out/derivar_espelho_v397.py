# -*- coding: utf-8 -*-
"""Deriva custodia_v397_espelho.py do da v396 por trocas CONTADAS (23/10/2026, sessão a7; regra do operador: custodiar quando o handoff
aparecer). Os sha16 dos recibos do B(n) da v397 vêm do HANDOFF_v397_CUSTODIA.md (aplicação 776ce2ae5959867e; parada fa1fc15fcd598591;
religamento 40ba026b5735558a); os dicionários _V397_FONTES e _V397_VERBATINS2 existem no um.py (medido por sondar_v397.py)."""
from pathlib import Path

T = Path(r"C:\IALD\Site\tgl\v3.0_bancada\tools")
s = (T / "custodia_v396_espelho.py").read_text(encoding="utf-8")
T2 = [
    ('r"""CUSTÓDIA v396 (22/10/2026; handoff v396; molde v395: backup = v395; stdouts até a v396; fontes pinadas + as da v396 (os insumos da ',
     'r"""CUSTÓDIA v397 (23/10/2026; handoff v397; molde v396: backup = v396; stdouts até a v397; fontes pinadas + as da v397 (a pedra Token, o '
     'resultado do Teste da Única Palavra e os três recibos da Fase 9, as 6 cunhagens de 23/10); diffs da v397; recibos do B(n) da v397). Do molde: '
     'CUSTÓDIA v396 (22/10/2026; handoff v396; molde v395: backup = v395; stdouts até a v396; fontes pinadas + as da v396 (os insumos da ', 1),
    ('REL = BANC / "revisoes" / "custodia_v396_espelho.json"', 'REL = BANC / "revisoes" / "custodia_v397_espelho.json"', 1),
    ('VERSAO = "v396"', 'VERSAO = "v397"', 1),
    ('"v393", "v394", "v395", "v396")\n', '"v393", "v394", "v395", "v396", "v397")\n', 1),
    ('bk364 = sorted(BK.glob("um_v395_*"))   # (nome da variável herdado do molde; é o backup da v395)',
     'bk364 = sorted(BK.glob("um_v396_*"))   # (nome da variável herdado do molde; é o backup da v396)', 1),
    ('assert bm["conferido_contra_origem"] is True and bm["versao"] == "v395", "BACKUP DA v395 NÃO CONFERE — PARAR"',
     'assert bm["conferido_contra_origem"] is True and bm["versao"] == "v396", "BACKUP DA v396 NÃO CONFERE — PARAR"', 1),
    ('        pares.append((a_, ESP / "diferencas_v396" / nome, "DIFF"))\n',
     '        pares.append((a_, ESP / "diferencas_v396" / nome, "DIFF"))\n'
     '    # v397: os dois diffs da cadeia da v397 (handoff v397), conferidos entre v397 e v397_kernel quando existirem nos dois\n'
     '    for nome in ("DIFF_v396_v397.diff", "DIFF_KERNEL_v397.txt"):\n        a_, b_ = CK / "v397" / nome, CK / "v397_kernel" / nome\n'
     '        assert a_.is_file(), "v397: %s ausente — PARAR" % nome\n'
     '        if b_.is_file():\n            assert sha(a_) == sha(b_), "v397: %s diverge entre v397 e v397_kernel — PARAR" % nome\n'
     '        pares.append((a_, ESP / "diferencas_v397" / nome, "DIFF"))\n', 1),
    ('"_V396_FONTES", "_V392_VERBATINS2"', '"_V396_FONTES", "_V397_FONTES", "_V392_VERBATINS2"', 2),
    ('"_V395_VERBATINS2", "_V396_VERBATINS2"):', '"_V395_VERBATINS2", "_V396_VERBATINS2", "_V397_VERBATINS2"):', 1),
    ('"_V395_VERBATINS2", "_V396_VERBATINS2"}, sorted(_dic)', '"_V395_VERBATINS2", "_V396_VERBATINS2", "_V397_VERBATINS2"}, sorted(_dic)', 1),
    ('        pares.append((_p, ESP / "recibos_bancada_v396" / _p.name, "RECIBO"))\n',
     '        pares.append((_p, ESP / "recibos_bancada_v396" / _p.name, "RECIBO"))\n'
     '    # v397: os recibos do B(n) da v397 (aplicação, parada, religamento), localizados por sha256 do handoff v397 na cadeia de selo da v397\n'
     '    _H397 = ("776ce2ae5959867e", "fa1fc15fcd598591", "40ba026b5735558a")\n'
     '    _rec7 = {}\n'
     '    for _p in sorted((CK / "v397").rglob("RECIBO_*")):\n'
     '        if _p.is_file() and ".bak_" not in _p.name and "ensaio" not in str(_p.relative_to(CK / "v397")):\n'
     '            _h = sha(_p, 16)\n'
     '            if _h in _H397:\n'
     '                _rec7.setdefault(_h, _p)\n'
     '    assert set(_rec7) == set(_H397), ("recibos do B(n) da v397 não achados por sha256 — PARAR", sorted(_rec7))\n'
     '    for _h, _p in sorted(_rec7.items()):\n'
     '        pares.append((_p, ESP / "recibos_bancada_v397" / _p.name, "RECIBO"))\n', 1),
]
for a, b, n in T2:
    c = s.count(a)
    assert c == n, (a[:100], c, n)
    s = s.replace(a, b)
d = T / "custodia_v397_espelho.py"
assert not d.exists(), "já existe — PARAR"
compile(s, str(d), "exec")
d.write_text(s, encoding="utf-8")
print("ok", d.name, len(s))
