# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411] leitor de trechos do um.py BASE (a v410 selada, copia de bytes em base_v410\um.py): devolve funcoes e constantes de topo por NOME, sem importar o programa inteiro
"""base_um_v410.py -- extrai do um.py da v410 selada (base_v410\\um.py, conferido por sha256 contra o selo) os trechos de TOPO pedidos por nome (def NOME / NOME = ...) e os executa num namespace isolado, resolvendo as
dependencias por NameError (so' entre os trechos de topo do proprio um.py). Serve aos ensaios offline da preparacao da v411 (o teste do registro h0dn_bg1_v411 usa a funcao congelada da v410, o contrato dela, os insumos
que ela embute e as guardas de texto herdadas, EXATAMENTE como estao no um.py selado). Nada e' escrito; o um.py nao roda."""
import hashlib, json, math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
UM = os.path.join(HERE, "base_v410", "um.py")
_T = None
_IDX = None


def texto():
    global _T, _IDX
    if _T is None:
        b = open(UM, "rb").read()
        selo = json.load(open(os.path.join(HERE, "base_v410", "um_absoluto_selo.json"), encoding="utf-8"))
        assert hashlib.sha256(b).hexdigest() == selo["sha256"]["um.py"] and selo["um_version"] == "v410", "base_v410\\um.py nao e' a v410 selada"
        _T = b.decode("utf-8").replace("\r\n", "\n")
        _IDX = {}
        for m in re.finditer(r"^(?:def ([A-Za-z_][A-Za-z_0-9]*)\(|([A-Za-z_][A-Za-z_0-9]*) = )", _T, re.M):
            _IDX.setdefault(m.group(1) or m.group(2), []).append(m.start())
    return _T


def trecho(nome):
    t = texto()
    ps = _IDX.get(nome) or []
    assert len(ps) == 1, ("nome de topo ausente ou repetido no um.py base", nome, len(ps))
    i = ps[0]
    m = re.compile(r"^(?=[^\s#)\]}])", re.M).search(t, t.index("\n", i) + 1)
    while m and t[m.start():m.start() + 1] in ("'", '"'):
        m = re.compile(r"^(?=[^\s#)\]}])", re.M).search(t, m.start() + 1)
    return t[i:m.start() if m else len(t)].rstrip("\n") + "\n"


def carregar(nomes, ns=None, max_rodadas=60):
    """executa os trechos pedidos num namespace (com re, os, math, json, hashlib); resolve NameError trazendo o trecho de topo com o nome que faltou. Devolve o namespace."""
    ns = ns if ns is not None else {"re": re, "os": os, "math": math, "json": json, "hashlib": hashlib, "__name__": "base_um_v410"}
    feitos = set()
    pend = list(nomes)
    while pend:
        n = pend.pop(0)
        if n in feitos:
            continue
        exec(compile(trecho(n), "<base_v410:um.py:%s>" % n, "exec"), ns)
        feitos.add(n)
    return ns


def chamar_resolvendo(ns, fn_nome, *a, **k):
    """chama ns[fn_nome](*a) e, a cada NameError de nome de topo do um.py, carrega o trecho que faltou e tenta de novo."""
    for _ in range(80):
        try:
            return ns[fn_nome](*a, **k)
        except NameError as e:
            m = re.search(r"name '([A-Za-z_0-9]+)' is not defined", str(e))
            assert m and m.group(1) in (_IDX or {}), ("NameError que nao e' de topo do um.py", str(e))
            carregar([m.group(1)], ns)
    raise RuntimeError("dependencias demais")
