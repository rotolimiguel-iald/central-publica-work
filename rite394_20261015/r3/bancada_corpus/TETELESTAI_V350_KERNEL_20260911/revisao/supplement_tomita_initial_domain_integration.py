"""Static final integration inspection. No author scripts are executed."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW=Path(__file__).resolve().parent;ROOT=REVIEW.parent
RUN=Path((REVIEW/'tomita_initial_domain_latest_run.txt').read_text(encoding='utf-8'))
CAP=max(RUN.glob('final_integrated_*'))
V=json.loads((CAP/'verification.json').read_bytes())
M=json.loads((RUN/'manifest.json').read_bytes())
C=json.loads((RUN/'compilation.json').read_bytes())
B=json.loads((CAP/'integrated_compile.json').read_bytes())
I=json.loads((CAP/'integration.json').read_bytes())
P=json.loads((CAP/'gns_representation_custody.json').read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def tests(path):
    t=ast.parse(path.read_bytes())
    return t,{n.args[0].value:ast.dump(n,include_attributes=False) for n in ast.walk(t)
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='check'
        and n.args and isinstance(n.args[0],ast.Constant)}

oldtree,oldcalls=tests(Path(V['previous_layer'])/'test_gate_extension.py')
newtree,newcalls=tests(CAP/'test_gate_extension.py')
added=set(newcalls)-set(oldcalls)
def is_added(n):
    return (isinstance(n,ast.Expr) and isinstance(n.value,ast.Call)
        and isinstance(n.value.func,ast.Name) and n.value.func.id=='check'
        and n.value.args and isinstance(n.value.args[0],ast.Constant)
        and n.value.args[0].value in added)
newtree.body=[n for n in newtree.body if not is_added(n)]
newfiles=set(V['new_compilations_relative_to_92'])
newrows=[r for r in B['records'] if Path(r['source']).relative_to(ROOT/'kernel').as_posix() in newfiles]
streams=[]
for row in newrows:
    record={'source':Path(row['source']).relative_to(ROOT/'kernel').as_posix(),'timestamp':row['timestamp']}
    for kind in ['stdout','stderr']:
        p=Path(row[kind]);record[kind+'_sha256']=sha(p)
        record[kind+'_frozen_identical']=p.read_bytes()==(CAP/'logs'/p.name).read_bytes()
    streams.append(record)
imports={}
for root in ['TGLExt.lean','TGL/Audit.lean']:
    raw=(CAP/'sources'/root).read_text(encoding='utf-8')
    imports[root]={name:bool(re.search(r'^import TGLExt\.V350'+name+r'\s*$',raw,re.M)) for name in V['source_matches']}
original=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
original_sha=sha(original)
base_sha=sha(ROOT/'fontes/um_v350_original.py')
inventory=json.loads((CAP/'runtime_io_inventory.json').read_bytes())
aud=C['records'][-1]['axioms']
all_live_names=['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json',
    'gate_extension.py','test_gate_extension.py','MINUTA_DOMINIO_INICIAL_TOMITA.md']
result={
    'timestamp':datetime.datetime.now().astimezone().isoformat(),
    'original_sha256':original_sha,'local_base_sha256':base_sha,
    'original_local_base_equal_integration_pin':original_sha==base_sha==I['base_sha256'],
    'previous_custody_matches_AST_baseline':P['working_sha256']==V['previous_um_sha256'],
    'new_targets_exact':set(aud)==set(V['new_targets_axioms'])==set(M['declarations']),
    'new_target_axioms_match_own_auditor':all(set(aud[n])==set(V['new_targets_axioms'][n]) for n in aud),
    'root_imports':imports,
    'six_new_compiles_source_unchanged':len(newrows)==6 and all(r['source_unchanged_during_compile'] is True for r in newrows),
    'new_compilation_streams':streams,
    'new_stdout_warnings':{Path(row['source']).name:[l for l in Path(row['stdout']).read_text(encoding='utf-8').splitlines() if 'warning:' in l] for row in newrows},
    'reused_source_and_binary_count':len(V['reused_same_binary_and_source_as_92']),
    'old_literal_check_calls':len(oldcalls),'new_literal_check_calls':len(newcalls),
    'added_controls':sorted(added),'removed_controls':sorted(set(oldcalls)-set(newcalls)),
    'all_previous_literal_control_calls_identical_AST':all(newcalls.get(n)==t for n,t in oldcalls.items()),
    'entire_test_AST_unchanged_after_only_added_controls_removed':ast.dump(oldtree,include_attributes=False)==ast.dump(newtree,include_attributes=False),
    'runtime_inventory_sha256':sha(CAP/'runtime_io_inventory.json'),
    'runtime_inventory_historical_source_sha256':inventory['source_sha256'],
    'runtime_inventory_pinned_to_history':sha(CAP/'runtime_io_inventory.json')==P['runtime_io_inventory_sha256'] and inventory['source_sha256']==P['runtime_io_inventory_source_sha256'],
    'no_runtime_inventory_execution':inventory['monolith_executed_or_imported'] is False,
    'posterior_modules_absent_from_embedded':V['posterior_modules_absent_from_embedded'],
    'all_final_artifacts_live_hashes_unchanged':all(sha(ROOT/n)==V['artifact_sha256'][n] for n in all_live_names),
    'working_um_unchanged':sha(ROOT/'um.py')==V['um_sha256'],
    'four_DEV_sources_unchanged':all(sha(Path(r['path']))==r['sha256'] for r in M['sources'].values()),
    'previous_reviews_preserved':all(sha(Path(p))==h for p,h in M['previous_reviews'].items()),
    'sealed_GNS_review_matches_custody':sha(REVIEW/'REVIEW_GNS_REPRESENTATION.md')==P['review_sha256'],
    'author_roots_tests_recorders_monolith_executed_by_reviewer':False,
}
assert result['new_targets_exact'] and result['new_target_axioms_match_own_auditor']
assert all(all(x.values()) for x in imports.values()) and result['six_new_compiles_source_unchanged']
assert result['original_local_base_equal_integration_pin']
raw=json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8');p=CAP/'supplemental_verification.json'
assert not p.exists() and p.resolve().is_relative_to(REVIEW)
tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p)
print(json.dumps({k:v for k,v in result.items() if k!='new_compilation_streams'},ensure_ascii=False,indent=2))
