# -*- coding: utf-8 -*-
"""_r5ag_lib_v410.py -- ajuda dos scripts de edicao do agente de adaptacao da rodada R5 (D100 e D101; ADENDOS 5 e 6): troca de texto com contagem esperada,
backup de BYTES (`<arquivo>.bak_<AAAAMMDD_HHMMSS>_r5`), temporario -> substituir, preserva CRLF/LF, ast.parse nos .py. Molde: _r2ag_lib_v410.py.
Rodar duas vezes o mesmo script falha na contagem (o texto antigo ja' nao existe): a guarda de idempotencia e' essa, antes de gravar qualquer coisa."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")


def sha16(b):
    return hashlib.sha256(b).hexdigest()[:16]


def aplicar(rel, trocas, base=None, parse=None):
    """trocas = [(antigo, novo, n_esperado ou None)]; n None = pelo menos uma. Devolve (sha16 antes, sha16 depois)."""
    p = os.path.join(base or HERE, rel)
    b0 = open(p, "rb").read()
    crlf = b0.count(b"\r\n") > 0
    t = b0.decode("utf-8").replace("\r\n", "\n")
    for a, b, n in trocas:
        c = t.count(a)
        assert (c >= 1 if n is None else c == n), (rel, "contagem", c, "esperada", n, a[:160])
        t = t.replace(a, b)
    nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8")
    if (parse is None and rel.endswith(".py")) or parse:
        ast.parse(nb.decode("utf-8").replace("\r\n", "\n"))
    open(p + ".bak_" + TS + "_r5", "wb").write(b0)
    open(p + ".tmp", "wb").write(nb)
    assert os.path.getsize(p + ".tmp") == len(nb)
    os.replace(p + ".tmp", p)
    print("%-48s %d -> %d | %s -> %s" % (rel, len(b0), len(nb), sha16(b0), sha16(nb)))
    return sha16(b0), sha16(nb)
