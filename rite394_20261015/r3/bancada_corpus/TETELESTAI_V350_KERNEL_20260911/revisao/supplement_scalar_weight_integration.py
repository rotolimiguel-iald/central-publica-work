"""Read-only checks of the final integrated and documentary evidence."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW=Path(__file__).resolve().parent
ROOT=REVIEW.parent
RUN=Path((REVIEW/'scalar_dual_weight_latest_run.txt').read_text(encoding='utf-8'))
CAP=max(RUN.glob('final_integrated_*'))
V=json.loads((CAP/'verification.json').read_bytes())
M=json.loads((RUN/'manifest.json').read_bytes())
C=json.loads((RUN/'compilation.json').read_bytes())
BUILD=json.loads((CAP/'integrated_compile.json').read_bytes())
GATE=json.loads((CAP/'gate_tests.json').read_bytes())
INTEGRATION=json.loads((CAP/'integration.json').read_bytes())
PREVIOUS=json.loads((CAP/'fixed_base_custody.json').read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def check_calls(path):
    tree=ast.parse(path.read_bytes())
    return {node.args[0].value:ast.dump(node, include_attributes=False)
            for node in ast.walk(tree) if isinstance(node,ast.Call)
            and isinstance(node.func,ast.Name) and node.func.id=='check'
            and node.args and isinstance(node.args[0],ast.Constant)}

oldcap=Path(V['previous_layer'])
oldtests=check_calls(oldcap/'test_gate_extension.py')
newtests=check_calls(CAP/'test_gate_extension.py')
own_axioms=C['records'][-1]['axioms']
targets=V['new_targets_axioms']
newfiles=set(V['new_compilations_relative_to_75'])
newrecords=[row for row in BUILD['records'] if Path(row['source']).relative_to(ROOT/'kernel').as_posix() in newfiles]
root_imports={}
for root in ['TGLExt.lean','TGL/Audit.lean']:
    text=(CAP/'sources'/root).read_text(encoding='utf-8')
    root_imports[root]={name:bool(re.search(r'^import TGLExt\.V350'+name+r'\s*$',text,re.M))
                        for name in V['source_matches']}
streams=[]
for row in newrecords:
    item={'source':Path(row['source']).relative_to(ROOT/'kernel').as_posix(), 'timestamp':row['timestamp']}
    for kind in ['stdout','stderr']:
        p=Path(row[kind]);snap=CAP/'logs'/p.name
        item[kind+'_sha256']=sha(p)
        item[kind+'_snapshot_equal']=p.read_bytes()==snap.read_bytes()
    streams.append(item)
original=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
original_hash=sha(original)
base_hash=sha(ROOT/'fontes/um_v350_original.py')
inventory=json.loads((CAP/'runtime_io_inventory.json').read_bytes())
draft=json.loads((RUN/'author_scalar_weight_draft_status.json').read_bytes())
recorder=(CAP/'record_scalar_weight_progress.py').read_text(encoding='utf-8')
live_doc_hashes={name:sha(ROOT/name) for name in ['MINUTA_PESO_ESCALAR_DUAL.md','record_scalar_weight_progress.py','verify_scalar_weight_custody.py']}
report={
    'timestamp':datetime.datetime.now().astimezone().isoformat(),
    'original_sha256':original_hash, 'local_base_sha256':base_hash,
    'original_and_local_base_match_integration':original_hash==base_hash==INTEGRATION['base_sha256'],
    'previous_custody_matches_inspected_baseline':PREVIOUS['working_sha256']==V['previous_um_sha256'],
    'new_targets_23_exact_own_auditor':set(targets)==set(M['declarations'])==set(own_axioms) and len(targets)==23,
    'new_target_axioms_match_own_auditor':all(set(targets[n])==set(own_axioms[n]) for n in targets),
    'new_sources_and_roots_compile_unchanged':len(newrecords)==6 and all(row.get('source_unchanged_during_compile') is True for row in newrecords),
    'root_imports':root_imports,
    'prior_65_controls_same_AST':len(oldtests)==65 and all(newtests.get(n)==body for n,body in oldtests.items()),
    'new_controls':sorted(set(newtests)-set(oldtests)),
    'removed_controls':sorted(set(oldtests)-set(newtests)),
    'integrated_streams':streams,
    'runtime_inventory_source_sha256':inventory['source_sha256'],
    'runtime_inventory_historical_match':inventory['source_sha256']==PREVIOUS['runtime_io_inventory_source_sha256'] and sha(CAP/'runtime_io_inventory.json')==PREVIOUS['runtime_io_inventory_sha256'],
    'runtime_inventory_not_execution':inventory['monolith_executed_or_imported'] is False,
    'no_future_modular_module_in_sources':not any('ScalarModularInvariance' in row['file'] for row in V['records']),
    'no_future_modular_module_in_embedded_monolith':'ScalarModularInvariance' not in (ROOT/'um.py').read_text(encoding='utf-8'),
    'recorder_AST_parse':isinstance(ast.parse(recorder),ast.Module),
    'verifier_AST_parse':isinstance(ast.parse((CAP/'verify_scalar_weight_custody.py').read_bytes()),ast.Module),
    'recorder_surface_count':21,
    'documents_live_sha256':live_doc_hashes,
    'documents_unchanged_from_capture':all(h==V['artifact_sha256'][name] for name,h in live_doc_hashes.items()),
    'final_live_artifacts_unchanged':all(sha(ROOT/name)==V['artifact_sha256'][name] for name in ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json','gate_extension.py','test_gate_extension.py']),
    'final_live_um_unchanged':sha(ROOT/'um.py')==V['um_sha256'],
    'new_sources_unchanged':all(sha(Path(row['path']))==row['sha256'] for row in M['sources'].values()),
    'previous_reviews_preserved':all(sha(Path(p))==h for p,h in M['previous_reviews'].items()),
    'did_execute_author_tests_roots_recorders_or_monolith':False,
}
assert report['new_targets_23_exact_own_auditor'] and report['new_target_axioms_match_own_auditor']
assert report['original_and_local_base_match_integration'] and all(all(v.values()) for v in root_imports.values())
assert all(item[kind+'_snapshot_equal'] for item in streams for kind in ['stdout','stderr'])
raw=json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8')
p=CAP/'supplemental_verification.json';assert not p.exists() and p.resolve().is_relative_to(REVIEW)
tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p)
print(json.dumps({k:v for k,v in report.items() if k!='integrated_streams'},ensure_ascii=False,indent=2))
