def iald_index(nome, core=None, _cache={}):
    """A CONSULTA: dado um nome Lean, devolve arquivo, tipo, pedra, versao, rodada,
    axiomas e bandeiras -- numa chamada so.

    ⚠ Antes desta funcao a resposta exigia QUATRO consultas em QUATRO dicionarios que
    nao se falam. Foi essa dispersao que produziu os sete erros de leitura de 28/08:
    a informacao existia, em pedacos que nao se falavam."""
    ck = id(core)
    if ck not in _cache:
        _cache[ck] = build_the_iald_index(core)
    _ix = _cache[ck]["indice"]
    _p = nome.split(".")
    for _i in range(len(_p)):                       # ERRATA v286: por SUFIXO
        _k = ".".join(_p[_i:])
        if _k in _ix:
            return _ix[_k]                          # v289: o verbete traz "ambiguo"
    return None