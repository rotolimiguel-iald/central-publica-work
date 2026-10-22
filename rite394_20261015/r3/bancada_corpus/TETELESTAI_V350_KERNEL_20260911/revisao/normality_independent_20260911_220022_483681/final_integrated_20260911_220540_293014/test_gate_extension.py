"""Exercise exact-type defenses and the actual isolated gate, without importing um.py."""
import ast
import copy
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
source = (ROOT / 'um.py').read_text(encoding='utf-8')
tree = ast.parse(source)
base_raw = (ROOT / 'fontes/um_v350_original.py').read_bytes()
base_tree = ast.parse(base_raw)
required_functions = {
    'verify_v350_modular_provenance', 'finalize_v350_modular_frontier',
    'v350_frontier_flag_has_proof', 'v350_gravity_flags_have_proof',
    'evaluate_v350_kernel_frontier', 'evaluate_quantum_gravity_closure',
    'prove_qg_closure_gate'}
required_constants = {'_V350_MODULAR_CONTRACTS', '_QG_CERTIFICATE_FLAGS', '_QG_PHYSICS_FLAGS'}
nodes = [n for n in tree.body if (
    isinstance(n, ast.FunctionDef) and n.name in required_functions) or (
    isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in required_constants
                                     for t in n.targets))]
namespace = {}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(ROOT / 'um.py'), 'exec'), namespace)
compiled = json.loads((ROOT / 'integrated_compile.json').read_bytes())
assert compiled['incremental_build_ok'] is True
integration = json.loads((ROOT / 'integration.json').read_bytes())
assert len(compiled['records']) == len(integration['added_kernel_files']) + len(integration['updated_kernel_files'])
source_verified = all(hashlib.sha256(Path(r['source']).read_bytes()).hexdigest() == r['sha256']
                      and r['returncode'] == 0 for r in compiled['records'])
assert source_verified
for row in compiled['records']:
    output = ROOT / 'build' / Path(row['source']).relative_to(ROOT / 'kernel').with_suffix('.olean')
    assert hashlib.sha256(output.read_bytes()).hexdigest() == row['output_sha256']
dependencies = json.loads((ROOT / 'dependency_artifacts.json').read_bytes())
assert hashlib.sha256(base_raw).hexdigest() == dependencies['base_source_sha256']
changed_outputs = {str(Path(r['source']).relative_to(ROOT / 'kernel').with_suffix('.olean')).replace('\\', '/')
                   for r in compiled['records']}
dependencies_verified = all(
    rel in changed_outputs or hashlib.sha256((ROOT / 'build' / rel).read_bytes()).hexdigest() == row['sha256']
    for rel, row in dependencies['files'].items())
assert dependencies_verified
axioms = {}
audit_record = compiled['records'][-1]
assert audit_record['source'].endswith('Audit.lean')
blob = Path(audit_record['stdout']).read_text(encoding='utf-8')
for name, body in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", blob, re.S):
    axioms[name] = [a.strip() for a in body.replace('\n', ' ').split(',') if a.strip()]
for name in re.findall(r"'([\w.']+)' does not depend on any axioms", blob):
    axioms.setdefault(name, [])
base_embedded = ast.literal_eval(next(n for n in base_tree.body if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets)).value)
audit_targets = set(re.findall(r'^#print axioms ([\w.\']+)', base_embedded['TGL/Audit.lean'], re.M))
assert audit_targets <= axioms.keys(), sorted(audit_targets - axioms.keys())
assert all(set(values) <= {'propext', 'Classical.choice', 'Quot.sound'} for values in axioms.values())
baseline_document = json.loads((ROOT / 'fontes/um_absoluto.json').read_bytes())
baseline = baseline_document['core']['kernel_formalization']
kf = copy.deepcopy(baseline)
kf.update({'lake_build_ok': False, 'build_returncode': None,
           'incremental_build_ok': True, 'dependency_hashes_verified': True,
           'changed_source_hashes_verified': True, 'audit_returncode': 0,
           'all_verified': True, 'axiom_report': axioms,
           'verification_mode': compiled['mode'],
           'full_monolithic_runtime_run': False})
finalize = namespace['finalize_v350_modular_frontier']
proofs = namespace['verify_v350_modular_provenance']
frontier = namespace['evaluate_v350_kernel_frontier']
assert all(proofs(kf).values())
finalize(kf)
checks = []


def check(name, value):
    assert value, name
    checks.append({'name': name, 'passed': True})


check('real_compiled_exact_type_bridges', all(proofs(kf).values()))
check('v350_baseline_does_not_inherit_new_proofs', not any(proofs(baseline).values()))
check('empty_inputs_fail_closed', not any(proofs({}).values()))
for control in ('all_verified', 'incremental_build_ok', 'dependency_hashes_verified',
                'changed_source_hashes_verified'):
    candidate = copy.deepcopy(kf)
    candidate[control] = False
    check('missing_' + control, not any(proofs(candidate).values()))
candidate = copy.deepcopy(kf)
candidate['audit_returncode'] = 1
check('audit_failure_with_valid_prints_is_rejected', not any(proofs(candidate).values()))
for flag, names in namespace['_V350_MODULAR_CONTRACTS'].items():
    for name in names:
        candidate = copy.deepcopy(kf)
        candidate['axiom_report'].pop(name)
        check('missing_declaration_' + name, not proofs(candidate)[flag])
    for bad_axioms in (['sorryAx'], ['Lean.trustCompiler'], ['Foreign.hiddenPremise'], 'propext'):
        candidate = copy.deepcopy(kf)
        candidate['axiom_report'][names[1]] = bad_axioms
        check('reject_' + flag + '_' + str(bad_axioms), not proofs(candidate)[flag])

old_evaluator = next(n for n in base_tree.body if isinstance(n, ast.FunctionDef)
                     and n.name == 'evaluate_quantum_gravity_closure')
new_evaluator = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                     and n.name == 'evaluate_quantum_gravity_closure')
check('legacy_evaluator_AST_unchanged', ast.dump(old_evaluator) == ast.dump(new_evaluator))
evaluate = namespace['evaluate_quantum_gravity_closure']
formal = {key: kf.get('qgc_' + key) is True for key in namespace['_QG_CERTIFICATE_FLAGS']}
physics = {key: kf.get('qgp_' + key) is True for key in namespace['_QG_PHYSICS_FLAGS']}
experiment = {key: True for key in ('independent_v3_profiles_unblinded',
    'independent_v3_survey_mocks_passed', 'independent_v3_systematics_passed',
    'independent_v3_powered_verdict_emitted')}
for key in formal:
    candidate = {**formal, key: False}
    check('drop_formal_' + key, not evaluate(candidate, physics, experiment)['mathematical_model_constructed'])
for key in physics:
    candidate = {**physics, key: False}
    check('drop_physics_' + key, not evaluate(formal, candidate, experiment)['physical_quantum_gravity_constructed'])
check('perfect_experiment_does_not_supply_kernel', not evaluate({}, physics, experiment)['mathematical_model_constructed'])
gate = namespace['prove_qg_closure_gate'](1, kf,
    independent_rite=baseline_document['core']['void_floor_v11'])
check('legacy_gate_reproduces_sealed_v350_inputs',
      gate['gate']['verdict'] == baseline_document['core']['qg_closure']['gate']['verdict'])
check('extension_consumed_by_actual_gate_function', gate['gate']['kernel_frontier'] == frontier(kf))
check('historical_probe_accepts_only_typed_modular_proof',
      namespace['v350_frontier_flag_has_proof'](kf, 'red_clause_JMJ_contains'))
candidate = copy.deepcopy(kf)
candidate['gpf_H1_internal_susy_relative_gap_discharged'] = True
check('invented_H1_is_rejected', not namespace['v350_gravity_flags_have_proof'](candidate))
check('modular_does_not_discharge_later_fronts', not frontier(kf)['full_plan_complete'])
check('normality_does_not_discharge_continuous_core',
      'TGLV350.Regular.regularCoreEmbedding_preserves_positive_directed_isLUB' in axioms
      and kf.get('qgf_continuous_modular_realization_constructed') is False)
check('zero_trace_countermodel_does_not_discharge_corner_or_full_witness',
      'TGLV350.ContractAudit.zeroTraceLegacyCore_has_no_threeLocks' in axioms
      and kf.get('qgf_unconditional_continuous_corner_proved') is False
      and kf.get('qgf_full_TGL_witness_constructed') is False)
report = {'checks': checks, 'passed': len(checks), 'axiom_report_entries': len(axioms),
          'verification_mode': compiled['mode'], 'full_monolithic_runtime_run': False,
          'working_um_sha256': hashlib.sha256((ROOT / 'um.py').read_bytes()).hexdigest(),
          'frontier': frontier(kf), 'legacy_gate': gate['gate']['verdict']}
for name, value in [('gate_tests.json', report), ('kernel_incremental_evidence.json', kf)]:
    target = ROOT / name
    if target.exists():
        before = target.read_bytes()
        backup = target.with_name(target.name + '.bak_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    temporary = target.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')
    assert temporary.stat().st_size > 0
    temporary.replace(target)
print(json.dumps({k: v for k, v in report.items() if k != 'checks'}, ensure_ascii=False))
