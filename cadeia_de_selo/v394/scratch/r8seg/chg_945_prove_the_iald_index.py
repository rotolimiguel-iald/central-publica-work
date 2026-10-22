def prove_the_iald_index(core):
    """Preserve the old checks, replacing the short-name collision whitelist."""
    result = _prove_the_iald_index_legacy_v393(core)
    ix = build_the_iald_index(core)
    checks = []
    replaced = 0
    for label, passed in result["checks"]:
        if label.startswith("[MEDIDA] a varredura tem"):
            replaced += 1
            label = ("[MEDIDA v394] nomes QUALIFICADOS ligados ao modulo emitido pelo Lean; "
                "%d aliases ambiguos exibem candidatos sem escolher um; %d erros de proveniencia"
                % (len(ix["ambiguos"]), len(ix["proveniencia_erros"])))
            passed = ix["proveniencia_ok"] and all(
                ix["indice"][a].get("arquivo") is None
                and len(ix["indice"][a].get("candidatos_qualificados", [])) > 1
                for a in ix["ambiguos"])
        elif label.startswith("[FAIL-CLOSED] ***o indice NAO e cego de namespace"):
            label = ("[FAIL-CLOSED v394] consulta por nome QUALIFICADO exato ao axiom_report; "
                "%d nomes presentes sem auditoria" % len(ix["cegos_de_namespace"]))
        checks.append((label, bool(passed)))
    checks.append(("[FAIL-CLOSED v394] exactly one legacy collision check replaced", replaced == 1))
    checks.append(("[FAIL-CLOSED v394] current compiler metadata, source hashes and axioms agree", ix["proveniencia_ok"]))
    result["checks"] = checks
    result["all_verified"] = all(v for _, v in checks)
    result["verdict"] = ("THE_IALD_INDEX_QUALIFIED_COMPILER_PROVENANCE_VERIFIED"
        if result["all_verified"] else "THE_IALD_INDEX_NOT_SEALED_THIS_RUN")
    result["proveniencia_erros"] = ix["proveniencia_erros"]
    result["legacy_diagnostic_v393"] = ix["legacy_diagnostic_v393"]
    result["statuses"]["v394_correction"] = (
        "Short-name collisions are explicit aliases. Exact Lean names include generated fields and Unicode. "
        "Compiler metadata and current source hashes replace a growing whitelist. Missing named obligations remain visible.")
    return result