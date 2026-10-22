# -*- coding: utf-8 -*-
"""Deriva os scripts da custódia v395 (21/10/2026, sessão a7) dos da v394, por trocas CONTADAS (cada troca confere quantas vezes ocorre):
 - custodia_v395_passo0_backup.py  (backup da v394, que ESTÁ no espelho)
 - custodia_v395_espelho.py         (STDOUTS + v395; backup um_v394_*; diffs v395; fontes pinadas + _V395_*; recibos do B(n) da v395)"""
from pathlib import Path

T = Path(r"C:\IALD\Site\tgl\v3.0_bancada\tools")


def derivar(orig, novo, trocas):
    s = (T / orig).read_text(encoding="utf-8")
    for a, b, n in trocas:
        c = s.count(a)
        assert c == n, (novo, a[:100], c, n)
        s = s.replace(a, b)
    (T / novo).write_text(s, encoding="utf-8")
    compile(s, str(T / novo), "exec")
    print("ok", novo, len(s))


derivar("custodia_v394_passo0_backup.py", "custodia_v395_passo0_backup.py", [
    ('r"""CUSTÓDIA CONJUNTA v393+v394 (19/10, handoffs v393/v394; molde v392)',
     'r"""CUSTÓDIA v395 (21/10, handoff v395; molde v394: backup da v394). Do molde: CUSTÓDIA CONJUNTA v393+v394 (19/10, handoffs v393/v394; molde v392)', 1),
    ('for v in SEMENTES + ("v392",):', 'for v in SEMENTES + ("v394",):', 1),
    ('assert pin_esp == PIN["v392"], "o espelho não está na v392 (pin %s; diário v392 = %s) — PARAR" % (pin_esp, PIN["v392"])',
     'assert pin_esp == PIN["v394"], "o espelho não está na v394 (pin %s; diário v394 = %s) — PARAR" % (pin_esp, PIN["v394"])', 1),
    ('dest = BK / ("um_v392_" + pin_esp)', 'dest = BK / ("um_v394_" + pin_esp)', 1),
    ('man = {"versao": "v392", "um_py_sha16": pin_esp,', 'man = {"versao": "v394", "um_py_sha16": pin_esp,', 1),
    ('"regra": "backup byte a byte da versão que ESTAVA no espelho, ANTES de sobrescrever (custódia conjunta v393+v394; molde da custódia v392)",',
     '"regra": "backup byte a byte da versão que ESTAVA no espelho, ANTES de sobrescrever (custódia v395; molde da custódia v394)",', 1),
    ('"gerador": "Site/tgl/v3.0_bancada/tools/custodia_v394_passo0_backup.py",', '"gerador": "Site/tgl/v3.0_bancada/tools/custodia_v395_passo0_backup.py",', 1),
])

derivar("custodia_v394_espelho.py", "custodia_v395_espelho.py", [
    ('r"""CUSTÓDIA CONJUNTA v393+v394 (19/10/2026;', 'r"""CUSTÓDIA v395 (21/10/2026; handoff v395; molde v394: backup = v394; stdouts até a v395; fontes pinadas + as da v395; diffs da v395; recibos do B(n) da v395). Do molde: CUSTÓDIA CONJUNTA v393+v394 (19/10/2026;', 1),
    ('REL = BANC / "revisoes" / "custodia_v394_espelho.json"', 'REL = BANC / "revisoes" / "custodia_v395_espelho.json"', 1),
    ('VERSAO = "v394"', 'VERSAO = "v395"', 1),
    ('"v392", "v393", "v394")', '"v392", "v393", "v394", "v395")', 1),
    ('bk364 = sorted(BK.glob("um_v392_*"))   # (nome da variável herdado do molde; é o backup da v392)',
     'bk364 = sorted(BK.glob("um_v394_*"))   # (nome da variável herdado do molde; é o backup da v394)', 1),
    ('assert bm["conferido_contra_origem"] is True and bm["versao"] == "v392", "BACKUP DA v392 NÃO CONFERE — PARAR"',
     'assert bm["conferido_contra_origem"] is True and bm["versao"] == "v394", "BACKUP DA v394 NÃO CONFERE — PARAR"', 1),
    ('    for nome in ("DIFF_v393_v394.diff", "DIFF_KERNEL_v394.txt"):\n        a_, b_ = CK / "v394" / nome, CK / "v394_kernel" / nome\n'
     '        assert a_.is_file() and b_.is_file() and sha(a_) == sha(b_), "v394: %s diverge entre v394 e v394_kernel — PARAR" % nome\n'
     '        pares.append((a_, ESP / "diferencas_v394" / nome, "DIFF"))\n',
     '    for nome in ("DIFF_v393_v394.diff", "DIFF_KERNEL_v394.txt"):\n        a_, b_ = CK / "v394" / nome, CK / "v394_kernel" / nome\n'
     '        assert a_.is_file() and b_.is_file() and sha(a_) == sha(b_), "v394: %s diverge entre v394 e v394_kernel — PARAR" % nome\n'
     '        pares.append((a_, ESP / "diferencas_v394" / nome, "DIFF"))\n'
     '    # v395: os dois diffs da cadeia da v395 (handoff v395), conferidos entre v395 e v395_kernel quando existirem nos dois\n'
     '    for nome in ("DIFF_v394_v395.diff", "DIFF_KERNEL_v395.txt"):\n        a_, b_ = CK / "v395" / nome, CK / "v395_kernel" / nome\n'
     '        assert a_.is_file(), "v395: %s ausente — PARAR" % nome\n'
     '        if b_.is_file():\n            assert sha(a_) == sha(b_), "v395: %s diverge entre v395 e v395_kernel — PARAR" % nome\n'
     '        pares.append((a_, ESP / "diferencas_v395" / nome, "DIFF"))\n', 1),
    ('"_V392_FONTES", "_V393_FONTES", "_V394_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2"):',
     '"_V392_FONTES", "_V393_FONTES", "_V394_FONTES", "_V395_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2", "_V395_VERBATINS2"):', 1),
    ('    assert set(_dic) == {"_V392_FONTES", "_V393_FONTES", "_V394_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2"}, sorted(_dic)',
     '    assert set(_dic) == {"_V392_FONTES", "_V393_FONTES", "_V394_FONTES", "_V395_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2", "_V395_VERBATINS2"}, sorted(_dic)', 1),
    ('        pares.append((_p, ESP / "recibos_bancada_v394" / _p.name, "RECIBO"))\n',
     '        pares.append((_p, ESP / "recibos_bancada_v394" / _p.name, "RECIBO"))\n'
     '    # v395: os recibos do B(n) da v395 (aplicação, parada, religamento), localizados por sha256 do handoff v395 na cadeia de selo da v395\n'
     '    _H395 = ("50edf88581dadb1b", "6b1810bfaf2a89e3", "312b019af6ab260a")\n'
     '    _rec5 = {}\n'
     '    for _p in sorted((CK / "v395").rglob("RECIBO_*")):\n'
     '        if _p.is_file() and ".bak_" not in _p.name and "ensaio" not in str(_p.relative_to(CK / "v395")):\n'
     '            _h = sha(_p, 16)\n'
     '            if _h in _H395:\n'
     '                _rec5.setdefault(_h, _p)\n'
     '    assert set(_rec5) == set(_H395), ("recibos do B(n) da v395 não achados por sha256 — PARAR", sorted(_rec5))\n'
     '    for _h, _p in sorted(_rec5.items()):\n'
     '        pares.append((_p, ESP / "recibos_bancada_v395" / _p.name, "RECIBO"))\n', 1),
])
