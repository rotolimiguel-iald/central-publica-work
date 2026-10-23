# -*- coding: utf-8 -*-
"""Deriva os scripts da custódia v396 (22/10/2026, sessão a7) dos da v395, por trocas CONTADAS (cada troca confere quantas vezes ocorre):
 - custodia_v396_passo0_backup.py  (backup da v395, que ESTÁ no espelho)
 - custodia_v396_espelho.py         (STDOUTS + v396; backup um_v395_*; diffs v396; fontes pinadas + _V396_* (os insumos da pedra
                                     TestemunhaEstatica e as 3 cunhagens de 22/10); recibos do B(n) da v396 pelos sha256 do handoff v396)"""
from pathlib import Path

T = Path(r"C:\IALD\Site\tgl\v3.0_bancada\tools")


def derivar(orig, novo, trocas):
    s = (T / orig).read_text(encoding="utf-8")
    for a, b, n in trocas:
        c = s.count(a)
        assert c == n, (novo, a[:100], c, n)
        s = s.replace(a, b)
    assert not (T / novo).exists(), ("já existe — PARAR (nada se sobrescreve)", novo)
    compile(s, str(T / novo), "exec")
    (T / novo).write_text(s, encoding="utf-8")
    print("ok", novo, len(s))


derivar("custodia_v395_passo0_backup.py", "custodia_v396_passo0_backup.py", [
    ('r"""CUSTÓDIA v395 (21/10, handoff v395; molde v394: backup da v394).',
     'r"""CUSTÓDIA v396 (22/10, handoff v396; molde v395: backup da v395). Do molde: CUSTÓDIA v395 (21/10, handoff v395; molde v394: backup da v394).', 1),
    ('for v in SEMENTES + ("v394",):', 'for v in SEMENTES + ("v395",):', 1),
    ('assert pin_esp == PIN["v394"], "o espelho não está na v394 (pin %s; diário v394 = %s) — PARAR" % (pin_esp, PIN["v394"])',
     'assert pin_esp == PIN["v395"], "o espelho não está na v395 (pin %s; diário v395 = %s) — PARAR" % (pin_esp, PIN["v395"])', 1),
    ('dest = BK / ("um_v394_" + pin_esp)', 'dest = BK / ("um_v395_" + pin_esp)', 1),
    ('man = {"versao": "v394", "um_py_sha16": pin_esp,', 'man = {"versao": "v395", "um_py_sha16": pin_esp,', 1),
    ('"regra": "backup byte a byte da versão que ESTAVA no espelho, ANTES de sobrescrever (custódia v395; molde da custódia v394)",',
     '"regra": "backup byte a byte da versão que ESTAVA no espelho, ANTES de sobrescrever (custódia v396; molde da custódia v395)",', 1),
    ('"gerador": "Site/tgl/v3.0_bancada/tools/custodia_v395_passo0_backup.py",', '"gerador": "Site/tgl/v3.0_bancada/tools/custodia_v396_passo0_backup.py",', 1),
    ('assert ok == len(SEMENTES)  # v394: nenhuma semente', 'assert ok == len(SEMENTES)  # v395: nenhuma semente', 1),
])

derivar("custodia_v395_espelho.py", "custodia_v396_espelho.py", [
    ('r"""CUSTÓDIA v395 (21/10/2026; handoff v395; molde v394:',
     'r"""CUSTÓDIA v396 (22/10/2026; handoff v396; molde v395: backup = v395; stdouts até a v396; fontes pinadas + as da v396 (os insumos da '
     'pedra TestemunhaEstatica e as 3 cunhagens de 22/10); diffs da v396; recibos do B(n) da v396). Do molde: CUSTÓDIA v395 (21/10/2026; handoff v395; molde v394:', 1),
    ('REL = BANC / "revisoes" / "custodia_v395_espelho.json"', 'REL = BANC / "revisoes" / "custodia_v396_espelho.json"', 1),
    ('VERSAO = "v395"', 'VERSAO = "v396"', 1),
    ('"v393", "v394", "v395")\n', '"v393", "v394", "v395", "v396")\n', 1),
    ('bk364 = sorted(BK.glob("um_v394_*"))   # (nome da variável herdado do molde; é o backup da v394)',
     'bk364 = sorted(BK.glob("um_v395_*"))   # (nome da variável herdado do molde; é o backup da v395)', 1),
    ('assert bm["conferido_contra_origem"] is True and bm["versao"] == "v394", "BACKUP DA v394 NÃO CONFERE — PARAR"',
     'assert bm["conferido_contra_origem"] is True and bm["versao"] == "v395", "BACKUP DA v395 NÃO CONFERE — PARAR"', 1),
    ('        pares.append((a_, ESP / "diferencas_v395" / nome, "DIFF"))\n',
     '        pares.append((a_, ESP / "diferencas_v395" / nome, "DIFF"))\n'
     '    # v396: os dois diffs da cadeia da v396 (handoff v396), conferidos entre v396 e v396_kernel quando existirem nos dois\n'
     '    for nome in ("DIFF_v395_v396.diff", "DIFF_KERNEL_v396.txt"):\n        a_, b_ = CK / "v396" / nome, CK / "v396_kernel" / nome\n'
     '        assert a_.is_file(), "v396: %s ausente — PARAR" % nome\n'
     '        if b_.is_file():\n            assert sha(a_) == sha(b_), "v396: %s diverge entre v396 e v396_kernel — PARAR" % nome\n'
     '        pares.append((a_, ESP / "diferencas_v396" / nome, "DIFF"))\n', 1),
    ('"_V392_FONTES", "_V393_FONTES", "_V394_FONTES", "_V395_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2", "_V395_VERBATINS2"):',
     '"_V392_FONTES", "_V393_FONTES", "_V394_FONTES", "_V395_FONTES", "_V396_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2", '
     '"_V395_VERBATINS2", "_V396_VERBATINS2"):', 1),
    ('    assert set(_dic) == {"_V392_FONTES", "_V393_FONTES", "_V394_FONTES", "_V395_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", "_V394_VERBATINS2", "_V395_VERBATINS2"}, sorted(_dic)',
     '    assert set(_dic) == {"_V392_FONTES", "_V393_FONTES", "_V394_FONTES", "_V395_FONTES", "_V396_FONTES", "_V392_VERBATINS2", "_V393_VERBATINS2", '
     '"_V394_VERBATINS2", "_V395_VERBATINS2", "_V396_VERBATINS2"}, sorted(_dic)', 1),
    ('        pares.append((_p, ESP / "recibos_bancada_v395" / _p.name, "RECIBO"))\n',
     '        pares.append((_p, ESP / "recibos_bancada_v395" / _p.name, "RECIBO"))\n'
     '    # v396: os recibos do B(n) da v396 (aplicação, parada, religamento), localizados por sha256 do handoff v396 na cadeia de selo da v396\n'
     '    _H396 = ("49e723b412fcdb11", "7a9cacaddc7744f1", "0a594bac20bf5874")\n'
     '    _rec6 = {}\n'
     '    for _p in sorted((CK / "v396").rglob("RECIBO_*")):\n'
     '        if _p.is_file() and ".bak_" not in _p.name and "ensaio" not in str(_p.relative_to(CK / "v396")):\n'
     '            _h = sha(_p, 16)\n'
     '            if _h in _H396:\n'
     '                _rec6.setdefault(_h, _p)\n'
     '    assert set(_rec6) == set(_H396), ("recibos do B(n) da v396 não achados por sha256 — PARAR", sorted(_rec6))\n'
     '    for _h, _p in sorted(_rec6.items()):\n'
     '        pares.append((_p, ESP / "recibos_bancada_v396" / _p.name, "RECIBO"))\n', 1),
])
