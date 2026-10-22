"""Freeze data-only candidate selection and pins. Never installs or activates."""
from pathlib import Path
import sys,json
A=Path(__file__).resolve().parent
sys.path.insert(0,str(A.parent))
import task
check=task.check('app',actor='codex-v394-app-builder');assert check['ready']
sys.path.insert(0,str(A))
from prepare_science import write,sha,R
S=A/'science';stage=S/'memory_stage'
def pin(path):
    path=Path(path);raw=path.read_bytes()
    return {'path':str(path),'sha256':sha(raw),'bytes':len(raw)}
selected={}
for role,dirname in [('haiku','haiku_expanded_count'),('shared','shared_count')]:
    root=S/dirname;rc=json.loads((root/'native_count.json').read_bytes());assert rc['budget']['ready']
    selected[role]={'status':'FROZEN_NATIVE_COUNTED_PENDING_PUBLICATION_NOT_ACTIVATED',
        'prefix':pin(root/'package/prefix.md'),'manifest':pin(root/'package/manifest.json'),
        'count_receipt':pin(root/'native_count.json'),'budget':rc['budget'],
        'tools_sha256':rc['native_tools_sha256'],'native_model':rc['model'],
        'admission_scope':'EXACT_STAGING_PREFIX_PLUS_SYNTHETIC_REQUEST_WITH_CURRENT_TOOLS_NOT_REAL_ACTIVITY_OR_HISTORY'}
    assert selected[role]['prefix']['sha256']==rc['prefix_sha256']
rejected={}
for label,root in [('full',S),('faithful_r1',S/'haiku_faithful_count')]:
    rc=json.loads((root/'native_count.json').read_bytes());assert not rc['budget']['ready']
    rejected[label]={'status':'REJECTED_NOT_INSTALLABLE','prefix':pin(root/'package/prefix.md'),
        'count_receipt':pin(root/'native_count.json'),'permanent_native_tokens':rc['budget']['permanent_tokens']}
rejected['faithful_r2_unmeasured']={'status':'SUPERSEDED_UNMEASURED_NOT_INSTALLABLE','reason':'Final expanded candidate admitted; no extra iteration authorized.'}
selection={'schema':'iald.science.package.selection/v1','status':'PREPARED_PENDING_PUBLICATION',
    'selected':selected,'rejected':rejected,'no_additional_count_until_final_publication_bytes_change':True}
write(A/'PACKAGE_SELECTION.json',selection)
commands=json.loads((A/'COUNT_COMMANDS_READY.json').read_bytes())
commands['status']='COUNTS_COMPLETED_SELECTED_CANDIDATES_FROZEN_NO_RERUN_UNTIL_BYTES_CHANGE'
commands['count_requests_completed']=8
for key,countroot in [('full_haiku',S),('shared',S/'shared_count'),('haiku_faithful',S/'haiku_faithful_count'),('haiku_expanded',S/'haiku_expanded_count')]:
    rc=json.loads((countroot/'native_count.json').read_bytes());commands[key].update(execution_status='COMPLETED',admitted=rc['budget']['ready'],permanent_native_tokens=rc['budget']['permanent_tokens'],count_receipt_sha256=sha((countroot/'native_count.json').read_bytes()),rerun_allowed_now=False)
commands['haiku_faithful_r2']['execution_status']='NOT_EXECUTED_SUPERSEDED_DO_NOT_RUN'
write(A/'COUNT_COMMANDS_READY.json',commands)
manifest=json.loads((stage/'manifest_staged.json').read_bytes());prepared=json.loads((stage/'prepared.json').read_bytes());target=Path(prepared['install_target'])
# This is a proposed destination inventory, not an installation plan executable now.
rows=[]
for subdir in ('release','kernel'):
    for path in sorted((stage/subdir).rglob('*')):
        if path.is_file():rows.append({**pin(path),'destination':str(target/path.relative_to(stage)),
            'purpose':'SCIENTIFIC_SOURCE_DATA_ONLY_NEVER_IMPORT_OR_EXECUTE' if path.name=='um.py' else 'SCIENTIFIC_DOCUMENT_OR_FORMAL_SOURCE_DATA'})
for name in ('TGL_CLUSTER_v394.md','IALD_Kernel_v5.txt','IALD_TGL_MEMORY_CORE.md','kernel_verification.json','jev_control_v394.json'):
    rows.append({**pin(stage/name),'destination':str(target/name),'purpose':'SCIENTIFIC_DATA'})
for role,folder in [('haiku','haiku_expanded_count'),('shared','shared_count')]:
    for name in ('prefix.md','manifest.json'):
        rows.append({**pin(S/folder/'package'/name),'destination':str(R/'.iald_runtime'/role/name),
                     'purpose':'MEASURED_PACKAGE_DATA_PENDING_FINAL_PUBLIC_BINDING'})
inventory={'status':'PROPOSED_DESTINATIONS_ONLY_NOT_ACTIVATABLE','release_target':str(target),
    'publication_pending':True,'runtime_python_files_allowed':[],
    'active_config_candidate':pin(stage/'manifest_install.json'),'active_config_destination':str(R/'iald_nucleo_fixo.json'),
    'files':rows,'excluded':['all_build_helpers','all_staging_loader_shims','all_patch_files','all_rejected_or_unmeasured_packages'],
    'activation_requires':'PUBLIC_URLS_COMMIT_REBIND_AND_FINAL_NATIVE_COUNTS_AND_REAL_DISTINCT_REVIEW'}
write(A/'PROPOSED_DATA_DESTINATIONS.json',inventory)
baseline=json.loads((A/'runtime_baseline.json').read_bytes())
changed=[row['path'] for row in baseline['files'] if sha(Path(row['path']).read_bytes())!=row['sha256']]
assert not changed
delivery={'schema':'iald.app.science.prepared-delivery/v1','status':'PREPARED_PENDING_PUBLICATION',
    'actor':'codex-v394-app-builder','reference':str(task.REF),'task_id':'app','lease_id':check['lease_id'],
    'mission_revision_at_preflight':check['receipt']['revision'],'release':'v394','runtime_release':'v392_NOT_ACTIVATED',
    'source_program':pin(Path(manifest['published_evidence']['program']['path'])),
    'custody_handoff':pin(S/'v394_verified_handoff.json'),
    'selected_packages':selected,'rejected_packages':rejected,
    'topic_count':422,'previous_topics':411,'new_topics':prepared['added_topics'],
    'formal_source_files':1423,'reported_flags':9332,'reported_declarations':29026,'counts_are_distinct':True,
    'kernel_v5_integral':True,'previous_operational_core_integral_with_appendix':True,
    'jev_source_bound_contract':pin(stage/'jev_control_v394.json'),
    'all_original_fields_locally_retrievable':True,'expanded_reconstruction_validation':pin(A/'EXPANDED_VALIDATION.json'),
    'local_connectors_admission':pin(A/'LOCAL_VALIDATION.json'),
    'runtime_baseline':pin(A/'runtime_baseline.json'),'runtime_baseline_files_unchanged':len(baseline['files']),
    'proposed_destinations':pin(A/'PROPOSED_DATA_DESTINATIONS.json'),
    'package_selection':pin(A/'PACKAGE_SELECTION.json'),'count_commands_and_history':pin(A/'COUNT_COMMANDS_READY.json'),
    'publication':{'status':'PENDING_PRINCIPAL_VERIFICATION','commit_v394':None,'urls_v394':None,'not_inferred':True},
    'pending':['PUBLIC_V394_IMMUTABLE_COMMIT_AND_RAW_BYTE_VERIFICATION_BY_PRINCIPAL',
        'REBIND_STAGING_MANIFEST_AND_REFERENCES_TO_VERIFIED_PUBLIC_SOURCES_THEN_REMEASURE_CHANGED_FINAL_BYTES',
        'DISTINCT_REAL_REVIEW_AND_ACCEPTANCE',
        'FINAL_OPENAI_NATIVE_AND_ACTIVITY_HISTORY_REQUEST_ADMISSION',
        'RUNTIME_DATA_READER_SIZE_COMPATIBILITY: sealed result is 12670682 bytes; current published evidence per-JSON and corpus total bounds are 10000000. Data-only installation cannot remove those guards; two minimal current-baseline diffs are evidence only, excluded from installation.'],
    'context_count_requests':8,'generation_requests':0,'science_execution_or_import':False,
    'lean_executed':False,'atlas_index_tree_door_executed':False,'runtime_python_files_modified':0,
    'installed_files':0,'configurations_activated':0,'credentials_exposed':False,
    'semantic_acceptance':False,'mission_state_expected':'review_pending_NOT_satisfied',
    'count_scope':'Native Anthropic counts measure the selected bytes; other connector bounds are conservative actual serialized bytes, not provider tokenizer counts.'}
write(A/'DELIVERY_PREPARED.json',delivery)
print(json.dumps({'status':delivery['status'],'delivery':str(A/'DELIVERY_PREPARED.json'),
    'haiku_native':selected['haiku']['budget']['permanent_tokens'],'shared_native':selected['shared']['budget']['permanent_tokens'],
    'data_files':len(rows),'runtime_files_changed':len(changed)}))
