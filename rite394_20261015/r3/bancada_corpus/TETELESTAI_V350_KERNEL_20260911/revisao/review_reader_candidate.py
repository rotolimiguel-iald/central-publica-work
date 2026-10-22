import ast
import copy
import datetime
import difflib
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911')
OUT=ROOT/'revisao'/('reader_candidate_review_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
OUT.mkdir()
names=['prove_the_assembly_and_the_single_debt','prove_the_atlas_and_the_index']
paths=[ROOT/'um.py',ROOT/'reader_correction/um.py']
raw=[p.read_bytes() for p in paths];text=[b.decode('utf-8') for b in raw];trees=[ast.parse(t) for t in text]
nodes=[{n.name:n for n in t.body if isinstance(n,ast.FunctionDef)} for t in trees]
blocks=[]
for s,ns in zip(text,nodes):
    ls=s.splitlines(keepends=True)
    blocks.append({name:''.join(ls[ns[name].lineno-1:ns[name].end_lineno]) for name in names})
roundtrip=text[1]
for name in names:
    assert roundtrip.count(blocks[1][name])==1
    roundtrip=roundtrip.replace(blocks[1][name],blocks[0][name],1)
only_two_bytes=roundtrip.encode('utf-8')==raw[0]
changed=[n for n in nodes[0] if n in nodes[1] and ast.dump(nodes[0][n],include_attributes=False)!=ast.dump(nodes[1][n],include_attributes=False)]
diff=''.join(difflib.unified_diff(text[0].splitlines(True),text[1].splitlines(True),fromfile='ROOT/um.py',tofile='reader_correction/um.py'))
(OUT/'two_readers.diff').write_bytes(diff.encode('utf-8'))
maps={}
for t in trees:
    for n in t.body:
        if isinstance(n,ast.Assign):
            for a in n.targets:
                if isinstance(a,ast.Name) and a.id in ['_REDUCTION_FLAGS','_EMBEDDED_KERNEL_FILES','_QG_CERTIFICATE_FLAGS','_QG_PHYSICS_FLAGS','_V350_MODULAR_CONTRACTS']:
                    value=ast.literal_eval(n.value)
                    if a.id in maps:assert maps[a.id]==value
                    maps[a.id]=value
# Only the two inspected pure readers are evaluated. No module imports, entry point or runtime.
selected=[nodes[1][name] for name in names]
assert not any(isinstance(n,(ast.Import,ast.ImportFrom)) for x in selected for n in ast.walk(x))
env={'math':math,'_REDUCTION_FLAGS':maps['_REDUCTION_FLAGS']}
exec(compile(ast.Module(body=selected,type_ignores=[]),'<two-inspected-readers>','exec'),env)
fresh=json.loads((ROOT/'r/completed_attempt_02/um_absoluto.json').read_bytes())['core']
old=json.loads((ROOT/'fontes/um_absoluto.json').read_bytes())['core']
tests=[]
def check(name,value):tests.append({'name':name,'passed':bool(value)});assert value,name
for label,c in [('baseline7',old),('current8',fresh)]:
    before=copy.deepcopy(c)
    for name in names:check(label+':'+name,env[name](c)['all_verified'] is True)
    check(label+':whole_core_unchanged',before==c)
c=copy.deepcopy(fresh);c['kernel_formalization']['gpf_tower_act_III_inhabitant_constructed']=False
v=env[names[0]](c)
check('8_without_flag_reported_pending',v['all_verified'] is True and 'FLAG_NOT_CONSTRUCTED' in v['verdict'])
for key in maps['_REDUCTION_FLAGS']:
    if key.startswith('clause_'):
        c=copy.deepcopy(fresh);del c['kernel_formalization']['red_'+key]
        check('missing_clause:'+key,env[names[0]](c)['all_verified'] is False)
c=copy.deepcopy(fresh);c['kernel_formalization']['red_clause_JMJ_contains']=False
check('flag_on_converse_false_rejected',env[names[0]](c)['all_verified'] is False)
own=[]
for n in nodes[1][names[1]].body:
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['_atlas','_indice'] for t in n.targets):own+=ast.literal_eval(n.value)
for key in own:
    c=copy.deepcopy(fresh);c['kernel_formalization'][key]=False
    check('missing_own_atlas:'+key,env[names[1]](c)['all_verified'] is False)
c=copy.deepcopy(fresh);c['kernel_formalization']['qgf_unrelated_test_flag']=True
check('atlas_independent_of_unrelated_flag',env[names[1]](c)['all_verified'] is True)

# Boundary observation: these readers consume flags, not an independent kernel verifier.
c=copy.deepcopy(fresh)
for pair in maps['_V350_MODULAR_CONTRACTS'].values():c['kernel_formalization']['axiom_report'].pop(pair[1],None)
trust_boundary={'synthetic_stale_flags_without_bridges_accepted_by_reader':env[names[0]](c)['all_verified'],
 'interpretation':'Reader trusts finalized kf. Upstream provenance is mandatory; this is not standalone proof validation.',
 'upstream_finalize_call_present':'return finalize_v350_modular_frontier(res)' in text[1],
 'upstream_functions_unchanged':all(ast.dump(nodes[0][n],include_attributes=False)==ast.dump(nodes[1][n],include_attributes=False)
      for n in ['verify_tgl_kernel_formalization','verify_v350_modular_provenance','finalize_v350_modular_frontier','evaluate_quantum_gravity_closure'])}
def pinfo(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
staged_results=ROOT/'runtime_inputs_pending/results.json'
manifest_results=ROOT/'runtime_inputs_pending/manifest_results.json'
result_info=pinfo(staged_results)
expected=json.loads((ROOT/'revisao/runtime_seals_preliminary_20260913_100700_656494/final_inspection.json').read_bytes())['external_providers'][0]
check('staged_results_matches_read_external_provider',result_info['sha256']==expected['sha256'])
author_v=json.loads((ROOT/'reader_correction/verification.json').read_bytes())
archive_p=ROOT/'r/completed_attempt_02/verification.json'
checks={'only_two_function_bytes_changed':only_two_bytes,'changed_functions_exact':set(changed)==set(names),
    'no_functions_added_or_removed':set(nodes[0])==set(nodes[1]),
    'same_922_embedded_files':len(maps['_EMBEDDED_KERNEL_FILES'])==922,
    'author_candidate_pin_matches':hashlib.sha256(raw[1]).hexdigest()==author_v['candidate_sha256'],
    'author_parent_pin_matches':hashlib.sha256(raw[0]).hexdigest()==author_v['source_sha256'],
    'all_own_tests_passed':all(x['passed'] for x in tests)}
assert all(checks.values())
report={'timestamp':datetime.datetime.now().astimezone().isoformat(),'checks':checks,
    'pins':{'source':pinfo(paths[0]),'candidate':pinfo(paths[1]),'author_verification':pinfo(ROOT/'reader_correction/verification.json'),
      'preparer':pinfo(ROOT/'prepare_reader_correction.py'),'staged_results':result_info,'results_manifest':pinfo(manifest_results),
      'archive_verification':pinfo(archive_p)},
    'changed_functions':changed,'own_tests':tests,'tests_count':len(tests),
    'trust_boundary':trust_boundary,
    'scope':'TWO_PURE_READERS_EXTRACTED_ONLY__NO_MONOLITH_OR_AUTHOR_PREPARER_EXECUTED',
    'candidate_not_installed_by_reviewer':True,'author_runtime_not_restarted':True}
(OUT/'verification.json').write_bytes(json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps({'out':str(OUT),'checks':checks,'tests_count':len(tests),'trust_boundary':trust_boundary,'pins':report['pins']},ensure_ascii=False,indent=2))
