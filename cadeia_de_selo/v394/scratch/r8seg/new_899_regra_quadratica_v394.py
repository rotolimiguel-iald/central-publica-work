def regra_quadratica_v394(core):
    """Require actual compiled evidence before running the quadratic consumer."""
    import hashlib
    report = core.get('kernel_formalization') or {}
    axioms = report.get('axiom_report') or {}
    ladder = core.get('external_ladder') or {}
    contract = _V394_QUADRATIC_CONTRACT
    trio = {'propext', 'Classical.choice', 'Quot.sound'}
    per = {}
    for theorem in contract['theorems']:
        values = axioms.get(theorem)
        per[theorem] = isinstance(values, list) and all(isinstance(v, str) for v in values) and set(values) <= trio
    embedded = {}
    for path, sha in contract['source_sha256'].items():
        body = _EMBEDDED_KERNEL_FILES.get(path)
        embedded[path] = isinstance(body, str) and hashlib.sha256(body.encode('utf-8')).hexdigest() == sha
    counts = [ladder.get('n_theorems_clean'), ladder.get('n_theorems_expected'), contract['expected_ladder']]
    exact = all(type(x) is int for x in counts) and len(set(counts)) == 1
    formal = (report.get('all_verified') is True and exact and bool(per) and all(per.values())
              and bool(embedded) and all(embedded.values())
              and (core.get('tempo_frequencia_v394') or {}).get('all_verified') is True)
    out = {'all_verified': False, 'formal_theorems': per, 'embedded_sources': embedded,
           'exact_ladder': exact, 'runtime_executed': False, 'does_not_gate_core': True,
           'scope': 'M2 residual of Eg(X) against a fixed anchor; no injectivity of Eg on raw states.'}
    if not formal:
        out['verdict'] = 'TGL_QUADRATIC_RULE_V394__REFUSED_FORMAL_OR_SOURCE_EVIDENCE__GATE_UNMOVED'
    else:
        try:
            runtime = v394_quadratic_checks()
            out.update(runtime=runtime, runtime_executed=True, all_verified=runtime['passed'])
            status = 'DERIVED_READING_RESIDUAL' if runtime['passed'] else 'RUNTIME_CHECK_FAILED'
            out['verdict'] = 'TGL_QUADRATIC_RULE_V394__' + status + '__GATE_UNMOVED'
        except Exception as exc:
            out.update(runtime_executed=True, error=repr(exc),
                       verdict='TGL_QUADRATIC_RULE_V394__RUNTIME_ERROR__GATE_UNMOVED')
    core['regra_quadratica_v394'] = out
    return out