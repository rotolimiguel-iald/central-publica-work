def tempo_frequencia_v394(core):
    """Actual v394 consumer: formal evidence and runtime jointly determine verdict."""
    import hashlib
    report=core.get('kernel_formalization') or {}
    axioms=report.get('axiom_report') or {}
    trio={'propext','Classical.choice','Quot.sound'}
    required=_V394_FORMAL_CONTRACT['theorems']
    expected=_V394_FORMAL_CONTRACT['expected_ladder']
    ladder=core.get('external_ladder') or {}
    clean=ladder.get('n_theorems_clean'); counted=ladder.get('n_theorems_expected')
    exact_ladder=(type(expected) is int and type(clean) is int and type(counted) is int
                  and clean == counted == expected)
    formal=bool(required) and report.get('all_verified') is True and exact_ladder
    per={}
    for theorem in required:
        values=axioms.get(theorem)
        per[theorem]=isinstance(values,list) and all(isinstance(x,str) for x in values) and set(values)<=trio
        formal=formal and per[theorem]
    embedded={}
    for rel,sha in _V394_FORMAL_CONTRACT['source_sha256'].items():
        body=_EMBEDDED_KERNEL_FILES.get(rel)
        embedded[rel]=isinstance(body,str) and hashlib.sha256(body.encode('utf-8')).hexdigest()==sha
    formal=formal and bool(embedded) and all(embedded.values())
    inscriptions={k:hashlib.sha256(v['text'].encode('utf-8')).hexdigest()==v['sha256'] for k,v in _V394_INSCRIPTIONS.items()}
    if not formal or not inscriptions or not all(inscriptions.values()):
        out={'all_verified':False,'verdict':'TGL_TIME_FREQUENCY_V394__REFUSED_FORMAL_OR_SOURCE_EVIDENCE__GATE_UNMOVED',
             'exact_ladder':exact_ladder,'formal_theorems':per,'embedded_sources':embedded,'inscriptions':inscriptions,'runtime_executed':False,'does_not_gate_core':True}
    else:
        try:
            result=v394_time_frequency_checks(v394_physical_parameters,SEALED_CODATA_ALPHA,HBAR_EXACT)
            ok=result['passed']
            out={'all_verified':ok,'verdict':'TGL_TIME_FREQUENCY_V394__'+('DERIVED_M2_CONTINUOUS_FLOW_AND_CLOCK' if ok else 'RUNTIME_CHECK_FAILED')+'__GATE_UNMOVED',
                 'exact_ladder':exact_ladder,'formal_theorems':per,'embedded_sources':embedded,'inscriptions':inscriptions,'runtime_executed':True,
                 'runtime':result,'does_not_gate_core':True,
                 'scope':'Compiled finite-model composition and synthetic GKLS verification; physical inputs and sector-identification limits remain explicit.'}
        except Exception as exc:
            out={'all_verified':False,'verdict':'TGL_TIME_FREQUENCY_V394__RUNTIME_ERROR__GATE_UNMOVED','error':repr(exc),
                 'exact_ladder':exact_ladder,'formal_theorems':per,'runtime_executed':True,'does_not_gate_core':True}
    core['tempo_frequencia_v394']=out
    return out