"""Synthetic adversarial checks of the current consumer, not a Lean/main run."""
import copy
import hashlib
import json
from diary_r1 import ROOT, new, pin

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
RUNTIME = OUT/'network_runtime_r2.py'
DEST = OUT/'network_runtime_tests_r3'


def fixture():
    body = 'example : True := True.intro\n'
    source = 'TGLExt/Fixture.lean'
    declaration = 'Fixture.synthetic'
    digest = hashlib.sha256(body.encode('utf-8')).hexdigest()
    contract = dict(declarations=[declaration], declaration_sources={declaration:source},
        source_sha256={source:digest}, expected_ladder=1,
        constructed_components=['synthetic fixture only'], open_joint_contract=['synthetic fixture only'])
    core = dict(kernel_formalization=dict(all_verified=True, build_returncode=0, audit_returncode=0,
        axiom_report={declaration:['propext']}, declaration_sources_v394={declaration:source},
        declaration_sources_status_v394={'ok':True}, formal_files_sha256={source:digest}),
        external_ladder=dict(n_theorems_clean=1,n_theorems_expected=1),
        regra_quadratica_v394={'all_verified':True})
    return contract, {source:body}, core


def check(name, mutate, expected):
    contract, sources, core = fixture()
    mutate(contract,sources,core)
    namespace = {'_V394_NETWORK_CONTRACT':contract,'_EMBEDDED_KERNEL_FILES':sources}
    exec(compile(RUNTIME.read_bytes(),str(RUNTIME),'exec'),namespace)
    result = namespace['rede_fock_v394'](core)
    assert result['all_verified'] is expected, name
    assert result['whole_certificate_inhabited'] is False and result['does_not_gate_core'] is True
    return dict(name=name, passed=True, expected=expected, returned=result['all_verified'])


def main():
    assert not DEST.exists()
    cases = [
        ('valid_synthetic',lambda c,s,x:None,True),
        ('missing_declaration',lambda c,s,x:x['kernel_formalization']['axiom_report'].clear(),False),
        ('forbidden_axiom',lambda c,s,x:x['kernel_formalization']['axiom_report']['Fixture.synthetic'].append('sorryAx'),False),
        ('wrong_compiler_module',lambda c,s,x:x['kernel_formalization']['declaration_sources_v394'].update({'Fixture.synthetic':'TGLExt/Wrong.lean'}),False),
        ('missing_source_hash',lambda c,s,x:x['kernel_formalization']['formal_files_sha256'].clear(),False),
        ('source_bytes_changed',lambda c,s,x:s.update({'TGLExt/Fixture.lean':'changed'}),False),
        ('build_exit_boolean',lambda c,s,x:x['kernel_formalization'].update(build_returncode=False),False),
        ('audit_exit_boolean',lambda c,s,x:x['kernel_formalization'].update(audit_returncode=False),False),
        ('failed_build',lambda c,s,x:x['kernel_formalization'].update(build_returncode=1),False),
        ('failed_audit',lambda c,s,x:x['kernel_formalization'].update(audit_returncode=1),False),
        ('unverified_provenance',lambda c,s,x:x['kernel_formalization']['declaration_sources_status_v394'].update(ok=False),False),
        ('ladder_count_boolean',lambda c,s,x:x['external_ladder'].update(n_theorems_clean=True),False),
        ('ladder_count_wrong',lambda c,s,x:x['external_ladder'].update(n_theorems_clean=2),False),
        ('quadratic_contract_failed',lambda c,s,x:x['regra_quadratica_v394'].update(all_verified=False),False),
        ('empty_declarations',lambda c,s,x:c.update(declarations=[]),False),
        ('empty_source_set',lambda c,s,x:c.update(source_sha256={}),False),
        ('missing_process_exit',lambda c,s,x:x['kernel_formalization'].pop('audit_returncode'),False),
    ]
    results = [check(*args) for args in cases]
    new(DEST/'RESULT.json',dict(status='PASS', checks=results, runtime=pin(RUNTIME),
        harness=pin(__file__), scope='Synthetic consumer checks only; no Lean proof, main invocation or joint certificate supplied.'))
    print(json.dumps(dict(checks=len(results),result=pin(DEST/'RESULT.json')),ensure_ascii=False))


if __name__ == '__main__':
    main()
