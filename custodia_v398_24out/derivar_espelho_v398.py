# -*- coding: utf-8 -*-
"""Deriva custodia_v398_espelho.py do da v397 por trocas CONTADAS (24/10/2026, sessão a7; regra do operador de 23/10: custodiar quando o
handoff aparecer). Os sha16 dos recibos do B(n) da v398 vêm do HANDOFF_v398_CUSTODIA.md (aplicação 0f306c551a2ccbee; parada
a3339191387ad9df; religamento 12354ad5c5ac52f2) e foram conferidos contra a cadeia de selo (work\\cadeia_de_selo\\v398); os dicionários
_V398_FONTES e _V398_VERBATINS2 existem no um.py (medido por sondar_v398.py: dicionarios_v398)."""
import json, re
from pathlib import Path

T = Path(r"C:\IALD\Site\tgl\v3.0_bancada\tools")
HO = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\HANDOFF_v398_CUSTODIA.md").read_text(encoding="utf-8")
m = re.search(r"recibo da aplicação `RECIBO_SINCRONIZACAO_v398_\d{8}_\d{6}\.json` \(sha256 `([0-9a-f]{16})`.*?parada do serviço sha256 `([0-9a-f]{16})`; recibo do religamento sha256 `([0-9a-f]{16})`", HO, re.S)
assert m, "os três sha16 dos recibos do B(n) não estão no handoff v398 — PARAR"
H398 = m.groups()
F = json.loads(Path(r"C:\IALD\Central de Patentes\work\custodia_v398_24out\fatos_v398.json").read_text(encoding="utf-8"))
assert "_V398_FONTES" in F["dicionarios_v398"] and "_V398_VERBATINS2" in F["dicionarios_v398"], F["dicionarios_v398"]
s = (T / "custodia_v397_espelho.py").read_text(encoding="utf-8")
T2 = [
    ('r"""CUSTÓDIA v397 (23/10/2026; handoff v397; molde v396: backup = v396; stdouts até a v397; fontes pinadas + as da v397 (',
     'r"""CUSTÓDIA v398 (24/10/2026; handoff v398; molde v397: backup = v397; stdouts até a v398; fontes pinadas + as da v398 (as pedras Sonico e '
     'AfinacaoDasCordas, a medida KH-N1 da v398, as 6 inscrições de 23/10); diffs da v398; recibos do B(n) da v398). Do molde: '
     'CUSTÓDIA v397 (23/10/2026; handoff v397; molde v396: backup = v396; stdouts até a v397; fontes pinadas + as da v397 (', 1),
    ('REL = BANC / "revisoes" / "custodia_v397_espelho.json"', 'REL = BANC / "revisoes" / "custodia_v398_espelho.json"', 1),
    ('VERSAO = "v397"', 'VERSAO = "v398"', 1),
    ('"v394", "v395", "v396", "v397")\n', '"v394", "v395", "v396", "v397", "v398")\n', 1),
    ('bk364 = sorted(BK.glob("um_v396_*"))   # (nome da variável herdado do molde; é o backup da v396)',
     'bk364 = sorted(BK.glob("um_v397_*"))   # (nome da variável herdado do molde; é o backup da v397)', 1),
    ('assert bm["conferido_contra_origem"] is True and bm["versao"] == "v396", "BACKUP DA v396 NÃO CONFERE — PARAR"',
     'assert bm["conferido_contra_origem"] is True and bm["versao"] == "v397", "BACKUP DA v397 NÃO CONFERE — PARAR"', 1),
    ('        pares.append((a_, ESP / "diferencas_v397" / nome, "DIFF"))\n',
     '        pares.append((a_, ESP / "diferencas_v397" / nome, "DIFF"))\n'
     '    # v398: os dois diffs da cadeia da v398 (handoff v398), conferidos entre v398 e v398_kernel quando existirem nos dois\n'
     '    for nome in ("DIFF_v397_v398.diff", "DIFF_KERNEL_v398.txt"):\n        a_, b_ = CK / "v398" / nome, CK / "v398_kernel" / nome\n'
     '        assert a_.is_file(), "v398: %s ausente — PARAR" % nome\n'
     '        if b_.is_file():\n            assert sha(a_) == sha(b_), "v398: %s diverge entre v398 e v398_kernel — PARAR" % nome\n'
     '        pares.append((a_, ESP / "diferencas_v398" / nome, "DIFF"))\n', 1),
    ('"_V396_FONTES", "_V397_FONTES", "_V392_VERBATINS2"', '"_V396_FONTES", "_V397_FONTES", "_V398_FONTES", "_V392_VERBATINS2"', 2),
    ('"_V396_VERBATINS2", "_V397_VERBATINS2"):', '"_V396_VERBATINS2", "_V397_VERBATINS2", "_V398_VERBATINS2"):', 1),
    ('"_V396_VERBATINS2", "_V397_VERBATINS2"}, sorted(_dic)', '"_V396_VERBATINS2", "_V397_VERBATINS2", "_V398_VERBATINS2"}, sorted(_dic)', 1),
    ('        pares.append((_p, ESP / "recibos_bancada_v397" / _p.name, "RECIBO"))\n',
     '        pares.append((_p, ESP / "recibos_bancada_v397" / _p.name, "RECIBO"))\n'
     '    # v398: os recibos do B(n) da v398 (aplicação, parada, religamento), localizados por sha256 do handoff v398 na cadeia de selo da v398\n'
     '    _H398 = %r\n'
     '    _rec8 = {}\n'
     '    for _p in sorted((CK / "v398").rglob("RECIBO_*")):\n'
     '        if _p.is_file() and ".bak_" not in _p.name and "ensaio" not in str(_p.relative_to(CK / "v398")) and "bateria_pre_selo" not in str(_p.relative_to(CK / "v398")):\n'
     '            _h = sha(_p, 16)\n'
     '            if _h in _H398:\n'
     '                _rec8.setdefault(_h, _p)\n'
     '    assert set(_rec8) == set(_H398), ("recibos do B(n) da v398 não achados por sha256 — PARAR", sorted(_rec8))\n'
     '    for _h, _p in sorted(_rec8.items()):\n'
     '        pares.append((_p, ESP / "recibos_bancada_v398" / _p.name, "RECIBO"))\n' % (tuple(H398),), 1),
]
for a, b, n in T2:
    c = s.count(a)
    assert c == n, (a[:100], c, n)
    s = s.replace(a, b)
d = T / "custodia_v398_espelho.py"
assert not d.exists(), "já existe — PARAR"
compile(s, str(d), "exec")
d.write_text(s, encoding="utf-8")
print("ok", d.name, len(s), "| recibos B(n) v398:", H398)
