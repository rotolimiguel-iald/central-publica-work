from pathlib import Path
import ast, copy, datetime, hashlib, json, os, re
root=Path(__file__).resolve().parent
review=root.parent/'REVISAO_A2_012/TRACE_COMPLETION_012/COMPATIBILIDADE_7'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load_copy(p):
    # Only the inspected, extracted reader definitions: never import canonical um.py.
    code=p.read_text(encoding='utf8');tree=ast.parse(code)
    assert all(isinstance(n,(ast.Assign,ast.FunctionDef)) for n in tree.body)
    namespace={};exec(compile(tree,str(p),'exec'),namespace);return namespace
ns=load_copy(root/'PROPOSTA_LEITORES_EXISTENTES_V2.py')
old=load_copy(root/'CANONICAL_READERS_SNAPSHOT.py')
review_data=json.loads((review/'AUDITORIA_FINAL_INDEPENDENTE.json').read_bytes())
assert all(review_data['gates'].values()) and not any(review_data['counts'].values())
audit=json.loads((review/'FINAL_AUDIT.json').read_bytes())
assert audit['result']['returncode']==0
stdout=Path(audit['result']['stdout']['path']);assert pin(stdout)==audit['result']['stdout']
report={}
for name,ax,none in re.findall(r"'([\w.']+)' (?:depends on axioms: \[([^]]*)\]|(does not depend on any axioms))",stdout.read_text(encoding='utf8'),re.S):
    report[name]=[re.sub(r'\.\{[^}]*\}','',a.strip()) for a in ax.replace('\n',' ').split(',') if a.strip()]
assert set(audit['names'])<=set(report)
mapping=json.loads((root/'PROPOSTA_MAPA_CONSUMIDORES_V2.json').read_bytes())
new_flags=list(mapping['typed_contracts'])
base={'axiom_report':report,'lake_build_ok':all(x['returncode']==0 for x in review_data['modules'].values()),
      'audit_returncode':audit['result']['returncode'],'all_verified':all(review_data['gates'].values())}
checks=[]
def check(name,value):
    checks.append({'name':name,'pass':bool(value)});assert value,name
proofs=ns['verify_v350_modular_provenance'](base)
check('four_new_contracts_read_actual_review',all(proofs[f] for f in new_flags))
check('old_table_did_not_read_the_new_contracts',all(f not in old['verify_v350_modular_provenance'](base) for f in new_flags))
for flag in new_flags:
    for name in mapping['typed_contracts'][flag]:
        m=copy.deepcopy(base);m['axiom_report'].pop(name)
        check('missing_supplier:'+flag+':'+name,not ns['verify_v350_modular_provenance'](m)[flag])
        m[flag]=True
        check('forged_flag_without_supplier:'+flag+':'+name,not ns['v350_frontier_flag_has_proof'](m,flag))
    for bad_ax in ['sorryAx','Lean.trustCompiler','NewNamespace.customAxiom',42]:
        m=copy.deepcopy(base);m['axiom_report'][mapping['typed_contracts'][flag][0]]=[bad_ax]
        check('bad_axiom:'+flag+':'+str(bad_ax),not ns['verify_v350_modular_provenance'](m)[flag])
for field,value in [('lake_build_ok',False),('audit_returncode',1),('all_verified',False)]:
    m=copy.deepcopy(base);m[field]=value
    check('failed_evidence:'+field,not any(ns['verify_v350_modular_provenance'](m)[f] for f in new_flags))
for malformed in [False, True, '0', 0.0, None]:
    m=copy.deepcopy(base);m['audit_returncode']=malformed
    check('P2_READERS_01_exact_returncode_type:'+repr(malformed),not any(ns['verify_v350_modular_provenance'](m)[f] for f in new_flags))
m=copy.deepcopy(base);m['lake_build_ok']=False;m.update(incremental_build_ok=True,dependency_hashes_verified=True,changed_source_hashes_verified=True)
check('existing_verified_incremental_path',all(ns['verify_v350_modular_provenance'](m)[f] for f in new_flags))
for field in ['dependency_hashes_verified','changed_source_hashes_verified']:
    bad=copy.deepcopy(m);bad[field]=False
    check('incremental_requires:'+field,not any(ns['verify_v350_modular_provenance'](bad)[f] for f in new_flags))
state=ns['finalize_v350_modular_frontier'](copy.deepcopy(base))
state['red_atermation_is_irreversible']=True
check('old_false_only_full_check_rejects_real_scope',not(bool(state.get('red_atermation_is_irreversible') and state.get('red_bell_is_the_corner') is None and not state.get('qgf_full_TGL_witness_constructed'))))
check('replacement_preserves_bell_separation_and_accepts_typed_full',bool(state.get('red_atermation_is_irreversible') and state.get('red_bell_is_the_corner') is None and ns['v350_frontier_flag_has_proof'](state,'qgf_full_TGL_witness_constructed')))
check('replacement_accepts_typed_continuous',ns['v350_frontier_flag_has_proof'](state,'qgf_continuous_modular_realization_constructed'))
check('H2_H3_not_lit',not state.get('gpf_H2_smooth_modular_four_frame_discharged') and not state.get('gpf_H3_local_horizon_equilibrium_discharged'))
# Historical modular regression is a named synthetic fixture, not a new proof of those six names.
historical=copy.deepcopy(base)
for names in old['_V350_MODULAR_CONTRACTS'].values():
    for n in names:historical['axiom_report'][n]=['propext','Classical.choice','Quot.sound']
check('all_constructed_scopes_reported',all(ns['evaluate_v350_kernel_frontier'](historical)[k] for k in ['modular_duality_constructed','continuous_minimal_realization_constructed','susy_minimal_representative_constructed']))
for n in report:historical['axiom_report'].pop(n,None)
scopes=ns['evaluate_v350_kernel_frontier'](historical)
check('missing_A2_does_not_erase_old_modular_scope',scopes['modular_duality_constructed'] and not scopes['continuous_minimal_realization_constructed'] and not scopes['susy_minimal_representative_constructed'])
check('legacy_gate_and_full_physical_plan_unchanged',not scopes['legacy_gate_changed'] and not scopes['full_plan_complete'])
data={'timestamp':datetime.datetime.now().astimezone().isoformat(),'status':'COPIED_READER_UNIT_TESTS_PASSED_NOT_FULL_RUNTIME',
      'proposal':pin(root/'PROPOSTA_LEITORES_EXISTENTES_V2.py'),'review_audit':pin(review/'FINAL_AUDIT.json'),
      'checks':checks,'count':len(checks),'all_passed':all(c['pass'] for c in checks),
      'scope':'Actual new proof axiom report consumed by copied readers. Build metadata translated from independent Lean review. Historical modular entries use explicitly synthetic fixtures solely for regression.',
      'not_proved':'No um.py execution, embedding, source materialization or canonical flag change. Exact-type Lean casts must be retained in the canonical audit.'}
p=root/'TESTES_LEITORES_COPIADOS_V2.json';assert not p.exists()
b=json.dumps(data,ensure_ascii=False,indent=2).encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
print(json.dumps({'path':str(p),'checks':len(checks),'all_passed':data['all_passed']}))
