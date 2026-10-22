def build_the_iald_index(core=None):
    """v394: exact compiler names, pinned source bytes and current axiom report."""
    kf = (core or {}).get("kernel_formalization") or {}
    families = (("", _LEAN_THEOREM_FLAGS), ("qgc_", _QG_CERTIFICATE_FLAGS),
        ("qgp_", _QG_PHYSICS_FLAGS), ("qgf_", _QG_FRONTIER_FLAGS),
        ("gpf_", _GRAVITY_PRICE_FLAGS), ("red_", _REDUCTION_FLAGS),
        ("gpi_", _GRAVITY_IMPORT_FLAGS), ("gpc_", _GRAVITY_CITATION_FLAGS))
    result = build_iald_qualified_index_v394(core,
        kf.get("declaration_sources_v394") or {}, _EMBEDDED_KERNEL_FILES,
        _ESQUELETO_STONES, families)
    legacy = _build_the_iald_index_legacy_v393(core)
    result["n_ausentes_regra_v285"] = legacy["n_ausentes_regra_v285"]
    result["legacy_diagnostic_v393"] = {k: legacy[k] for k in
        ("n_nomes", "n_ausentes", "ambiguos", "violacoes", "cegos_de_namespace")}
    meta = kf.get("declaration_sources_status_v394") or {}
    if meta.get("ok") is not True:
        result["proveniencia_erros"].append("CURRENT_AUDIT_METADATA_NOT_VERIFIED")
        result["proveniencia_ok"] = False
    return result