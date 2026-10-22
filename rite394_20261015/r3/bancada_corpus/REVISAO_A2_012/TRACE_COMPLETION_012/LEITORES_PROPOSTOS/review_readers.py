from pathlib import Path
import ast
import copy
import datetime
import difflib
import hashlib
import json
import os
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parent
AUTHOR = Path(r'C:\IALD\Central de Patentes\Chatgpt\A2_TRACE_COMPLETION_012')
PAID = ROOT.parent / 'COMPATIBILIDADE_7'
READS = []
CHECKS = []
OBSERVATIONS = []

def pin(path, data=None):
    path = Path(path)
    if data is None:
        data = path.read_bytes()
    return dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())

def read(path, purpose):
    data = Path(path).read_bytes()
    READS.append(dict(**pin(path, data), purpose=purpose))
    return data

def write(path, data):
    path = Path(path)
    assert path.resolve().is_relative_to(ROOT.resolve())
    if isinstance(data, str):
        data = data.encode('utf-8')
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = path.with_name(path.name + '.bak_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(path.read_bytes())
        assert backup.read_bytes() == path.read_bytes()
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_bytes(data)
    assert temporary.read_bytes() == data
    os.replace(temporary, path)
    assert path.read_bytes() == data

def record(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2))

def check(name, condition, evidence=None):
    CHECKS.append(dict(name=name, passed=bool(condition), evidence=evidence))

def execute_copy(path):
    tree = ast.parse(path.read_bytes().decode('utf-8'))
    assert all(isinstance(n, (ast.Assign, ast.FunctionDef)) for n in tree.body)
    assert not any(isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(tree))
    namespace = {}
    exec(compile(tree, str(path), 'exec'), namespace)
    return tree, namespace

def parse_axioms(text):
    report = {}
    pattern = r"'([\w.']+)' (?:depends on axioms: \[([^]]*)\]|(does not depend on any axioms))"
    for name, values, _ in re.findall(pattern, text, re.S):
        assert name not in report, name
        report[name] = [re.sub(r'\.\{[^}]*\}', '', a.strip()) for a in values.replace('\n', ' ').split(',') if a.strip()]
    return report

def prepare():
    names = ['PROPOSTA_LEITORES_EXISTENTES.py', 'PROPOSTA_LEITORES_EXISTENTES.diff',
             'PROPOSTA_MAPA_CONSUMIDORES.json', 'CANONICAL_READERS_SNAPSHOT.py',
             'CANONICAL_READERS_PROVENANCE.json', 'CANONICAL_CONSUMERS_BOUNDED.txt',
             'test_reader_proposal.py', 'TESTES_LEITORES_COPIADOS.json',
             'capture_canonical_readers.py', 'prepare_reader_proposal.py']
    for name in names:
        write(ROOT/'inputs'/name, read(AUTHOR/name, 'full copied reader proposal/provenance/source read'))
    casts = read(AUTHOR/'src/TGLExt/AuditReaderContracts012.lean', 'five exact type ascriptions, fully inspected')
    write(ROOT/'src/AuditReaderContracts012.lean', casts)
    for name in ['SELO_FINAL.json', 'AUDITORIA_FINAL_INDEPENDENTE.json', 'FINAL_AUDIT.json', 'TOOLCHAIN.json']:
        write(ROOT/'inputs'/name, read(PAID/name, 'reuse sealed independent review evidence, no mathematical rebuild'))
    seal = json.loads((ROOT/'inputs/SELO_FINAL.json').read_bytes())
    for item in seal['files']:
        actual = pin(item['path'], read(item['path'], 'check prior independent review seal bytes'))
        check('prior_seal:' + Path(item['path']).name, actual == item)
    prov = json.loads((ROOT/'inputs/CANONICAL_READERS_PROVENANCE.json').read_bytes())
    for item in prov['outputs']:
        check('provenance_pin:' + Path(item['path']).name, pin(item['path']) == item)
    reconstructed = '\n\n'.join(n['source'] for n in prov['nodes'].values()) + '\n'
    snapshot = (ROOT/'inputs/CANONICAL_READERS_SNAPSHOT.py').read_bytes()
    check('snapshot_exact_reconstruction_from_provenance', reconstructed.encode('utf-8') == snapshot)
    canonical = prov['canonical_source']
    try:
        data = read(canonical['path'], 'bytes read for hash and 8 declared node ranges only; NEVER imported/executed/copied in full')
        lines = data.decode('utf-8').splitlines(keepends=True)
        check('canonical_current_hash_matches_captured_provenance', pin(canonical['path'], data) == canonical)
        for name, item in prov['nodes'].items():
            segment = ''.join(lines[item['start_line']-1:item['end_line']]).rstrip('\r\n')
            check('canonical_node_range:' + name, segment == item['source'])
        canonical_read = dict(status='REAL_READ_ONLY_HASH_AND_DECLARED_RANGES', pin=pin(canonical['path'], data))
    except OSError as error:
        canonical_read = dict(status='DECLARADO_AUTHOR_PROVENANCE_ONLY', error=str(error), declared=canonical)
    record(ROOT/'CANONICAL_COMPARISON.json', canonical_read)
    return casts.decode('utf-8')

def python_tests():
    old_tree, old = execute_copy(ROOT/'inputs/CANONICAL_READERS_SNAPSHOT.py')
    new_tree, new = execute_copy(ROOT/'inputs/PROPOSTA_LEITORES_EXISTENTES.py')
    mapping = json.loads((ROOT/'inputs/PROPOSTA_MAPA_CONSUMIDORES.json').read_bytes())
    for key in ['candidate', 'diff']:
        check('proposal_map_pin:' + key, pin(mapping[key]['path']) == mapping[key])
    before = (ROOT/'inputs/CANONICAL_READERS_SNAPSHOT.py').read_text(encoding='utf-8')
    after = (ROOT/'inputs/PROPOSTA_LEITORES_EXISTENTES.py').read_text(encoding='utf-8')
    expected_diff = ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
        fromfile='CANONICAL_READERS_SNAPSHOT.py', tofile='PROPOSTA_LEITORES_EXISTENTES.py'))
    check('diff_exactly_describes_copied_proposal', expected_diff == (ROOT/'inputs/PROPOSTA_LEITORES_EXISTENTES.diff').read_text(encoding='utf-8'))
    old_functions = {n.name:n for n in old_tree.body if isinstance(n, ast.FunctionDef)}
    new_functions = {n.name:n for n in new_tree.body if isinstance(n, ast.FunctionDef)}
    check('same_five_python_functions', set(old_functions) == set(new_functions) and len(new_functions) == 5)
    for name in ['verify_v350_modular_provenance', 'v350_frontier_flag_has_proof', 'v350_gravity_flags_have_proof']:
        a, b = copy.deepcopy(old_functions[name]), copy.deepcopy(new_functions[name])
        for node in [a,b]:
            if isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                node.body.pop(0)
        check('existing_helper_logic_unchanged:' + name, ast.dump(a) == ast.dump(b))
    for name, changes in [('_QG_FRONTIER_FLAGS','frontier_updates'),('_GRAVITY_PRICE_FLAGS','price_updates')]:
        expected = dict(old[name]); expected.update(mapping[changes])
        check('only_requested_map_delta:' + name, new[name] == expected)
    old_contracts = old['_V350_MODULAR_CONTRACTS']
    contracts = new['_V350_MODULAR_CONTRACTS']
    new_flags = set(mapping['typed_contracts'])
    check('old_three_contracts_unchanged', len(old_contracts) == 3 and all(contracts[k] == v for k,v in old_contracts.items()))
    check('four_new_contracts_match_map', len(new_flags)==4 and set(contracts)==set(old_contracts)|new_flags and all(tuple(mapping['typed_contracts'][k]) == contracts[k] for k in new_flags))
    audit = json.loads((ROOT/'inputs/FINAL_AUDIT.json').read_bytes())
    facts = json.loads((ROOT/'inputs/AUDITORIA_FINAL_INDEPENDENTE.json').read_bytes())
    log_info = audit['result']['stdout']
    blob = read(log_info['path'], 'parse actual independent 60-name axiom stdout; no synthetic new suppliers')
    check('actual_axiom_log_hash', pin(log_info['path'], blob)==log_info)
    report = parse_axioms(blob.decode('utf-8'))
    check('actual_report_all_60_names', set(report)==set(audit['names']) and len(report)==60)
    base = dict(axiom_report=report, lake_build_ok=all(m['returncode']==0 for m in facts['modules'].values()),
        audit_returncode=audit['result']['returncode'], all_verified=all(facts['gates'].values()))
    verify = new['verify_v350_modular_provenance']
    evaluate = new['evaluate_v350_kernel_frontier']
    finalize = new['finalize_v350_modular_frontier']
    flag_check = new['v350_frontier_flag_has_proof']
    check('real_new_evidence_accepts_only_four_new_contracts', {k for k,v in verify(base).items() if v}==new_flags)
    # Grouped supplier removal: every impacted contract must fail and unrelated contracts keep their value.
    suppliers = set().union(*(set(contracts[f]) for f in new_flags))
    for supplier in sorted(suppliers):
        missing = copy.deepcopy(base); missing['axiom_report'].pop(supplier)
        expected = {f:not(supplier in contracts[f]) for f in new_flags}
        check('missing_supplier_exact_dependency:' + supplier, all(verify(missing)[f]==v for f,v in expected.items()))
    bad_values = [['sorryAx'], ['Lean.trustCompiler'], ['Other.unpaid'], [42], None, 'propext', ('propext',)]
    for flag in sorted(new_flags):
        refused=[]
        for bad in bad_values:
            altered=copy.deepcopy(base); altered['axiom_report'][contracts[flag][0]]=bad; altered[flag]=True
            refused.append(not verify(altered)[flag] and not flag_check(altered,flag))
        check('bad_or_malformed_axioms_and_forged_flag:' + flag, all(refused), dict(cases=bad_values, refused=refused))
    for field, value in [('lake_build_ok',False), ('all_verified',False), ('audit_returncode',1), ('audit_returncode',None)]:
        altered=copy.deepcopy(base); altered[field]=value
        check('failed_build_or_audit:' + field + ':' + str(value), not any(verify(altered).values()))
    incremental=copy.deepcopy(base); incremental.update(lake_build_ok=False,incremental_build_ok=True,dependency_hashes_verified=True,changed_source_hashes_verified=True)
    check('accepted_incremental_metadata', all(verify(incremental)[f] for f in new_flags))
    for field in ['incremental_build_ok','dependency_hashes_verified','changed_source_hashes_verified']:
        altered=copy.deepcopy(incremental); altered[field]=False
        check('incremental_requires:' + field, not any(verify(altered).values()))
    # Synthetic six-name historical fixture ONLY tests separation/regression of the old three scopes.
    old_fixture={name:['propext','Classical.choice','Quot.sound'] for values in old_contracts.values() for name in values}
    for modular in [False,True]:
        for continuous in [False,True]:
            for susy in [False,True]:
                trial=copy.deepcopy(base); trial['axiom_report']={}
                if modular: trial['axiom_report'].update(old_fixture)
                for f in new_flags:
                    if (f.startswith('qgf_') and continuous) or (f.startswith('gpf_') and susy):
                        trial['axiom_report'].update({n:report[n] for n in contracts[f]})
                value=evaluate(trial)
                observed=(value['modular_duality_constructed'],value['continuous_minimal_realization_constructed'],value['susy_minimal_representative_constructed'])
                limits=(not value['legacy_gate_changed'] and not value['full_plan_complete'] and len(value['physical_identifications_open'])==2)
                check('independent_scopes:' + str((modular,continuous,susy)), observed==(modular,continuous,susy) and limits)
    state=finalize(copy.deepcopy(base))
    check('finalize_recomputes_proofs', all(state[f] is True for f in new_flags) and state['red_clause_JMJ_contains'] is False)
    stale=copy.deepcopy(base); stale['axiom_report']={}; stale.update({f:True for f in contracts})
    check('finalize_clears_forged_managed_flags', not any(finalize(stale)[f] for f in contracts))
    check('H2_H3_map_unchanged_and_not_produced', all(not state.get('gpf_'+k) and new['_GRAVITY_PRICE_FLAGS'][k]==old['_GRAVITY_PRICE_FLAGS'][k] for k in ['H2_smooth_modular_four_frame_discharged','H3_local_horizon_equilibrium_discharged']))
    for key in ['gpf_H2_smooth_modular_four_frame_discharged','gpf_H3_local_horizon_equilibrium_discharged','gpf_unknown']:
        trial=copy.deepcopy(state); trial[key]=True
        check('gravity_helper_refuses_unpaid_flag:' + key, not new['v350_gravity_flags_have_proof'](trial))
    # Evaluate the two concrete proposed expressions, preserving their other conjuncts.
    replacements=mapping['existing_checks_replacements']
    for row in replacements:
        check('replacement_uses_existing_helper:' + str(row['canonical_line']), 'v350_frontier_flag_has_proof' in row['new'])
    full='qgf_full_TGL_witness_constructed'; cont='qgf_continuous_modular_realization_constructed'
    for label, trial, expected in [
        ('real',copy.deepcopy(state),True),
        ('absent',{},True),
        ('forged',{full:True,cont:True},False)]:
        trial.update(red_atermation_is_irreversible=True)
        context=dict(kf=trial,v350_frontier_flag_has_proof=flag_check)
        first='bool(kf.get("red_atermation_is_irreversible") and kf.get("red_bell_is_the_corner") is None '+replacements[0]['new']+')'
        check('two_false_only_replacements:' + label, eval(first,context) is expected and eval(replacements[1]['new'],context) is expected)
        trial['red_bell_is_the_corner']=True
        check('Bell_conjunct_preserved:' + label, eval(first,context) is False)
    # Test a narrow inherited metadata type boundary; do not fix author's copied implementation.
    malformed=copy.deepcopy(base); malformed['audit_returncode']=False
    bad_accepted={f:verify(malformed)[f] for f in new_flags}
    inherited=old['verify_v350_modular_provenance'](dict(malformed,axiom_report=old_fixture))
    OBSERVATIONS.append(dict(id='P2-READERS-01', title='audit_returncode False compares equal to zero',
        malformed_value=False, accepted_new=bad_accepted, reproduced_in_snapshot=all(inherited.values()),
        cause='Python bool is a subclass of int; inherited helper uses == 0 without exact int type check.',
        scope='Malformed metadata boundary only. Actual audited subprocess return code is integer 0; no observed false certificate in this batch.',
        suggested_minimal_delta='type(kf.get("audit_returncode")) is int and kf.get("audit_returncode") == 0'))
    check('metadata_observation_reproduced_not_introduced', all(bad_accepted.values()) and all(inherited.values()))
    record(ROOT/'PYTHON_TESTS.json',dict(checks=CHECKS, count=len(CHECKS), all_passed=all(c['passed'] for c in CHECKS),
        observations=OBSERVATIONS, historical_fixture='SYNTHETIC ONLY old six supplier names, regression of three scopes; never new Lean proof',
        build_metadata='Translated from sealed independent 11/60 review; no canonical runtime invocation',
        author_tests='Source and reported 61 checks inspected, not executed or counted as independent tests'))

def run_lean(casts):
    config=json.loads((ROOT/'inputs/TOOLCHAIN.json').read_bytes())
    assert pin(config['lean']['path'])==config['lean']
    env=os.environ.copy(); env['LEAN_PATH']=';'.join(config['lean_path'])
    env['TMP']=env['TEMP']=str(ROOT/'tmp'); (ROOT/'tmp').mkdir(exist_ok=True)
    # No provider source is compiled; only the five #checks and a same-type rejection control.
    prelude=casts.split('-- Add these casts')[0]
    checks=casts[casts.index('#check '):casts.index('#print axioms')]
    terms=['regularLegacyCore','regularLegacyThreeLocks','regularModularRealization','regularFullWitness','regularSusyData']
    for term in terms:
        checks=checks.replace('#check ('+term+' :','#check (True.intro :')
    write(ROOT/'src/RejectTrueReaderContracts.lean',prelude+checks)
    results=[]
    for name in ['AuditReaderContracts012','RejectTrueReaderContracts']:
        path=ROOT/'src'/f'{name}.lean'
        output=ROOT/'lean_logs'/name; output.mkdir(parents=True,exist_ok=True)
        command=[config['lean']['path'],'-R',str(ROOT/'src'),str(path)]
        started=time.monotonic()
        result=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,timeout=90)
        write(output/'stdout.txt',result.stdout); write(output/'stderr.txt',result.stderr)
        item=dict(name=name,command=command,source=pin(path),returncode=result.returncode,
            seconds=time.monotonic()-started,stdout=pin(output/'stdout.txt'),stderr=pin(output/'stderr.txt'))
        results.append(item)
        print(json.dumps(dict(name=name,rc=result.returncode,seconds=item['seconds'])),flush=True)
    positive_text=(ROOT/'lean_logs/AuditReaderContracts012/stdout.txt').read_text(encoding='utf-8')
    negative_text=(ROOT/'lean_logs/RejectTrueReaderContracts/stdout.txt').read_text(encoding='utf-8')
    positive_axioms=parse_axioms(positive_text)
    allowed={'propext','Classical.choice','Quot.sound'}
    valid=(results[0]['returncode']==0 and len(positive_axioms)==5 and all(set(v)<=allowed for v in positive_axioms.values())
        and results[1]['returncode']!=0 and negative_text.count('Type mismatch')==5)
    record(ROOT/'LEAN_CAST_TESTS.json',dict(results=results,positive_axioms=positive_axioms,
        five_true_terms_rejected=negative_text.count('Type mismatch')==5,all_passed=valid,
        provider_policy='11 modules and A1/Mathlib read from existing sealed cache; zero provider rebuilds, no new Lean declarations or aliases'))

if __name__=='__main__':
    casts=prepare()
    python_tests()
    record(ROOT/'READS.json',READS)
    print(json.dumps(dict(python_checks=len(CHECKS),all_passed=all(c['passed'] for c in CHECKS),observations=len(OBSERVATIONS))),flush=True)
    run_lean(casts)
