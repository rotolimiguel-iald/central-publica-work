# -*- coding: utf-8 -*-
"""_fix_quadro_do_pacote_parte2_v410.py -- ACHADO (A) do harness dos textos (09/11, 21:11, reproduzido em 32 s com --sem-negativos): os textos do pos-rito liam o quadro_v397 da pasta da v409 (e, por ele, o delta_v409): um modulo herdado poe a pasta da versao anterior na frente do sys.path,
e la' ha' outra copia de quadro_v397.py (so' a linha do import do delta difere). A assercao de _dl() caia, com razao (fail-closed); no pos-rito REAL cairia igual. Conserto na causa: o quadro e' carregado pelo CAMINHO do pacote (nunca pela ordem do sys.path), nos textos, na leitura e no harness.
Backup de BYTES; temporario -> conferir tamanho -> substituir; ast.parse. Nao muda o candidato nem o delta."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")
FUNC = ('def _quadro_do_pacote(pk_):\n'
        '    """O quadro_v397 DESTE pacote, carregado pelo CAMINHO (nunca pela ordem do sys.path: um modulo herdado poe a pasta da versao anterior na frente, e la\' ha\' outra copia de quadro_v397.py, que importa o delta dela)."""\n'
        '    import importlib.util as _ilu_q\n'
        '    alvo_ = os.path.normcase(os.path.abspath(os.path.join(pk_, "quadro_v397.py")))\n'
        '    for nome_ in ("quadro_v397", "quadro_v397__pacote_v410"):\n'
        '        m_ = sys.modules.get(nome_)\n'
        '        if m_ is not None and os.path.normcase(os.path.abspath(getattr(m_, "__file__", "") or "")) == alvo_:\n'
        '            return m_\n'
        '    if pk_ not in sys.path:\n'
        '        sys.path.insert(0, pk_)\n'
        '    sp_ = _ilu_q.spec_from_file_location("quadro_v397__pacote_v410", alvo_); m_ = _ilu_q.module_from_spec(sp_); sp_.loader.exec_module(m_)\n'
        '    assert getattr(m_.DL, "UM_VERSION", None) == "v410", ("o quadro do pacote nao importou o delta da v410", getattr(m_.DL, "__file__", None))\n'
        '    sys.modules["quadro_v397__pacote_v410"] = m_\n'
        '    return m_\n'
        '\n'
        '\n')


def aplicar(nome, trocas):
    p = os.path.join(HERE, "pos_rito", nome); b0 = open(p, "rb").read(); crlf = b0.count(b"\r\n") > 0; t = b0.decode("utf-8").replace("\r\n", "\n")
    for a, b, n in trocas:
        c = t.count(a); assert c == n, (nome, c, n, a[:140]); t = t.replace(a, b)
    nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8"); ast.parse(nb)
    open(p + ".bak_" + TS + "_pre_quadro_do_pacote", "wb").write(b0)
    open(p + ".tmp", "wb").write(nb); assert os.path.getsize(p + ".tmp") == len(nb); os.replace(p + ".tmp", p)
    print(nome, len(b0), "->", len(nb), "| sha16", hashlib.sha256(b0).hexdigest()[:16], "->", hashlib.sha256(nb).hexdigest()[:16])


aplicar("textos_v410.py", [
    ('def _qd():\n', FUNC + 'def _qd():\n', 1),
    ('        if PK not in sys.path:\n            sys.path.insert(0, PK)\n        import quadro_v397 as QD\n        _CACHE["qd"] = QD\n', '        _CACHE["qd"] = _quadro_do_pacote(PK)   # (09/11: pelo caminho do pacote, nunca pela ordem do sys.path)\n', 1),
])
aplicar("leitura_v410.py", [
    ('def _esp_rf(ESP, curto, completo):\n', FUNC + 'def _esp_rf(ESP, curto, completo):\n', 1),
    ('        import quadro_v397 as QV_\n', '        QV_ = _quadro_do_pacote(PK)   # (09/11: o quadro DESTE pacote, pelo caminho; antes vinha pela ordem do sys.path e podia ser o da versao anterior)\n', 1),
])
aplicar("harness_textos_ensaio_v410.py", [
    ('import quadro_v397 as QD  # noqa: E402\n', 'QD = T._qd()   # (09/11: o quadro do PACOTE, pelo caminho; o import pelo sys.path trazia o da pasta da v409)\n', 1),
])
