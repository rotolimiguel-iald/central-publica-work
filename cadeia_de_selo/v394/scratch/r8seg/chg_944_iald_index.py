def iald_index(nome, core=None):
    """Exact full name or explicitly indexed suffix; unknown prefix is refused.

    No object-id cache: a mutable core may acquire a later audit in the same
    process. Ambiguous aliases return their full list without selecting one.
    """
    return build_the_iald_index(core)["indice"].get(nome)