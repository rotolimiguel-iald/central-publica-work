"""Synthetic adversarial preflight of the consumer; not a full kernel run."""
import copy
import json
from pathlib import Path
from diary_r1 import ROOT, new, pin

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
BUNDLE = OUT/'network_bundle_r4'


def main():
    plan = json.loads((BUNDLE/'PLAN_R2.json').read_bytes())
    sources = {r['relative']:Path(r['transposed_source']['path']).read_text(encoding='utf-8') for r in plan['modules']}
    sources[plan['audit_relative']] = Path(plan['audit']['path']).read_text(encoding='utf-8')
    hashes = {r['relative']:r['transposed_source']['sha256'] for r in plan['modules']}
    hashes[plan['audit_relative']] = plan['audit']['sha256']
    declarations = plan['theorems']
    count = 7171+len(declarations)
    contract = dict(declarations=declarations, source_sha256=hashes, expected_ladder=count,
                    constructed_components=['synthetic preflight'], open_joint_contract=['OPEN'])
    namespace = dict(_V394_NETWORK_CONTRACT=contract, _EMBEDDED_KERNEL_FILES=sources)
    runtime = OUT/'network_runtime_r1.py'
    exec(compile(runtime.read_text(encoding='utf-8'), str(runtime), 'exec'), namespace)
    valid = dict(kernel_formalization=dict(all_verified=True, axiom_report={n:['propext','Classical.choice','Quot.sound'] for n in declarations}),
                 external_ladder=dict(n_theorems_clean=count, n_theorems_expected=count),
                 regra_quadratica_v394=dict(all_verified=True), existing_gate='UNCHANGED_FIXTURE')
    checks = []

    def run(name, mutate=None, accepted=False):
        core = copy.deepcopy(valid)
        if mutate:
            mutate(core)
        before = copy.deepcopy(core)
        result = namespace['rede_fock_v394'](core)
        after = dict(core)
        del after['rede_fock_v394']
        checks.append(dict(name=name, passed=(result['all_verified'] is accepted and after == before
            and result['whole_certificate_inhabited'] is False and result['does_not_gate_core'] is True),
            accepted=result['all_verified'], verdict=result['verdict']))

    first = declarations[0]
    run('complete_synthetic_evidence', accepted=True)
    run('missing_declaration', lambda c:c['kernel_formalization']['axiom_report'].pop(first))
    run('sorry_injected', lambda c:c['kernel_formalization']['axiom_report'].__setitem__(first, ['sorryAx']))
    run('non_string_axiom', lambda c:c['kernel_formalization']['axiom_report'].__setitem__(first, [True]))
    run('missing_global_verified', lambda c:c['kernel_formalization'].pop('all_verified'))
    run('integer_is_not_true', lambda c:c['kernel_formalization'].__setitem__('all_verified', 1))
    run('wrong_ladder', lambda c:c['external_ladder'].__setitem__('n_theorems_clean', count-1))
    run('boolean_ladder', lambda c:c['external_ladder'].__setitem__('n_theorems_clean', True))
    run('nan_ladder', lambda c:c['external_ladder'].__setitem__('n_theorems_clean', float('nan')))
    run('quadratic_consumer_refused', lambda c:c['regra_quadratica_v394'].__setitem__('all_verified', False))
    path = next(iter(sources))
    original = sources[path]
    sources[path] = original+'\n-- changed source\n'
    run('source_mutation_refused')
    sources.pop(path)
    run('source_missing_refused')
    sources[path] = original
    run('restored_synthetic_evidence', accepted=True)
    result = dict(passed=all(c['passed'] for c in checks), checks=checks,
                  runtime=pin(runtime), plan=pin(BUNDLE/'PLAN_R2.json'), script=pin(__file__),
                  scope='Synthetic evidence fixtures only; no um.py import, kernel execution, full rite or empirical inference.')
    new(OUT/'NETWORK_CONSUMER_PREFLIGHT_R1.json', result)
    print(json.dumps(dict(passed=result['passed'], checks=len(checks), receipt=pin(OUT/'NETWORK_CONSUMER_PREFLIGHT_R1.json')), ensure_ascii=False))
    assert result['passed']


if __name__ == '__main__':
    main()
