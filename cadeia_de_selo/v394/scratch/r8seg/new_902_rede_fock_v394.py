def rede_fock_v394(core):
    """Verify the constructed components on the same canonical Fock.

    The contract enumerates what this particular embedded bundle proves.
    Remaining global-net, trace/PF and physical-source obligations stay explicit.
    Success here never supplies an inhabitant of the whole remaining record.
    """
    import hashlib
    contract = _V394_NETWORK_CONTRACT
    report = core.get('kernel_formalization') or {}
    ladder = core.get('external_ladder') or {}
    axioms = report.get('axiom_report') or {}
    provenance = report.get('declaration_sources_v394') or {}
    actual_source_hashes = report.get('formal_files_sha256') or {}
    trio = {'propext', 'Classical.choice', 'Quot.sound'}
    declarations = {}
    for name in contract['declarations']:
        values = axioms.get(name)
        expected_source = contract['declaration_sources'].get(name)
        declarations[name] = (
            isinstance(values, list)
            and all(isinstance(v, str) for v in values)
            and set(values) <= trio
            and isinstance(expected_source, str)
            and provenance.get(name) == expected_source
            and expected_source in contract['source_sha256'])
    sources = {}
    for path, expected in contract['source_sha256'].items():
        body = _EMBEDDED_KERNEL_FILES.get(path)
        sources[path] = (
            isinstance(body, str)
            and hashlib.sha256(body.encode('utf-8')).hexdigest() == expected
            and actual_source_hashes.get(path) == expected)
    counts = [ladder.get('n_theorems_clean'), ladder.get('n_theorems_expected'),
              contract['expected_ladder']]
    exact = all(type(v) is int for v in counts) and len(set(counts)) == 1
    process_ok = all(type(report.get(k)) is int and report[k] == 0
                     for k in ('build_returncode', 'audit_returncode'))
    passed = (
        report.get('all_verified') is True and process_ok and exact
        and (report.get('declaration_sources_status_v394') or {}).get('ok') is True
        and bool(declarations) and all(declarations.values())
        and bool(sources) and all(sources.values())
        and (core.get('regra_quadratica_v394') or {}).get('all_verified') is True)
    result = dict(all_verified=passed, formal_declarations=declarations,
        embedded_sources=sources, exact_ladder=exact, actual_processes_ok=process_ok,
        constructed_components=contract['constructed_components'],
        open_joint_contract=contract['open_joint_contract'],
        whole_certificate_inhabited=False,
        scope='Current compiled components on the same Fock; the remaining joint contract is explicit.',
        does_not_gate_core=True)
    result['verdict'] = (
        'TGL_FOCK_NETWORK_V394__DERIVED_COMPONENTS__JOINT_CONTRACT_OPEN__GATE_UNMOVED'
        if passed else
        'TGL_FOCK_NETWORK_V394__REFUSED_FORMAL_OR_SOURCE_EVIDENCE__GATE_UNMOVED')
    core['rede_fock_v394'] = result
    return result