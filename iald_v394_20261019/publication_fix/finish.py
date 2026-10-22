"""Validate the two-label fix and emit the eight-file transaction proposal only."""
from pathlib import Path
from types import SimpleNamespace
import ast,importlib.util,json,sys
P=Path(__file__).resolve().parent;W=P.parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode=True;sys.path.insert(0,str(W));import task
check=task.check('publication_label_fix',actor='codex-v394-app-builder');assert check['ready']
sys.path.insert(0,str(R))
from support import save,write,sha,pin
from iald_release_binding import load_release
from claude_memory_package import load_package
from claude_context_snapshot import load_snapshot,verify_native_tools
from claude_profiles import HAIKU
from iald_motor_claude import converter_pedido
import iald_kernel,iald_fontes_publicas,iald_core_indexado,iald_app_memory
b=json.loads((P/'PREPARED_BINDING.json').read_bytes());staged=P/'staging/manifest_staged.json'
release=load_release(staged);assert release.identity==b['deployment'];tests=[]
def passed(name):tests.append({'name':name,'status':'PASS'})
exact=json.loads((P/'EXACT_LABEL_TEST.json').read_bytes());assert exact['passed'] and exact['edit_count']==2
old=Path(exact['old_core']['path']).read_bytes();new=Path(exact['new_core']['path']).read_bytes()
cursor=0;rebuilt=b''
for edit in sorted(exact['edits'],key=lambda r:r['old_start_byte']):
    assert old[edit['old_start_byte']:edit['old_end_byte']]==edit['old_utf8'].encode()
    rebuilt+=old[cursor:edit['old_start_byte']]+edit['new_utf8'].encode();cursor=edit['old_end_byte']
rebuilt+=old[cursor:];assert rebuilt==new;passed('exactly_two_labels_no_core_bytes_outside_regions_changed')
installed=json.loads((R/'iald_nucleo_fixo.json').read_bytes());proposed=json.loads((P/'staging/manifest_install.json').read_bytes())
assert {k:v for k,v in installed.items() if k!='operational_core'}=={k:v for k,v in proposed.items() if k!='operational_core'}
assert {k:v for k,v in installed['operational_core'].items() if k not in ('path','sha256')}=={k:v for k,v in proposed['operational_core'].items() if k not in ('path','sha256')}
passed('manifest_only_operational_core_path_and_sha_change')
tools=iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
counts={}
for folder,live in [('haiku55','haiku55'),('shared','haiku')]:
    root=P/'packages'/folder;raw=(root/'prefix.md').read_bytes();oldprefix=(R/'.iald_runtime'/live/'prefix.md').read_bytes()
    assert raw==oldprefix.replace(old,new,1).replace(installed['operational_core']['sha256'].encode(),sha(new).encode(),1)
    passed(folder+'_prefix_only_two_core_labels_and_dependent_hash_changed')
    package=load_package(root,canonical_manifest=staged,expected_model=HAIKU.model)
    assert package.measurement.prefix_sha256==sha(raw);passed(folder+'_current_package_loader_accepts_binding')
    if folder=='haiku55':
        _,snapshot=load_snapshot(root,lambda path:load_package(path,canonical_manifest=staged))
        cfg=SimpleNamespace(modelo=HAIKU.model,max_saida=16384,cache_ttl='5m',esforco_claude='medium')
        wire=converter_pedido(cfg,{'model':HAIKU.model,'max_completion_tokens':16384,
            'messages':[{'role':'system','content':raw.decode()},{'role':'user','content':'.'}],'tools':tools},prefixo=raw.decode())
        verify_native_tools(wire,snapshot,trusted_tools=wire['tools']);passed('fixed_seven_and_ACOM_scoped_tool_binding_preserved')
for folder in ('haiku55','shared','sonnet_public'):
    root=P/'packages'/folder;rc=json.loads((root/'native_count.json').read_bytes())
    assert rc['budget']['ready'] and rc['prefix_sha256']==sha((root/'prefix.md').read_bytes())
    assert rc['deployment']==release.identity and rc['private_atlas_included'] is False
    counts[folder]={'receipt':pin(root/'native_count.json'),'prefix':pin(root/'prefix.md'),'budget':rc['budget']}
passed('three_public_model_correct_native_counts_ready_with_16k_output')
assert b['deployment']['operational_core_sha256'] in (P/'native_prefix.md').read_text(encoding='utf-8')
assert new.decode() in (P/'native_prefix.md').read_text(encoding='utf-8');passed('new_native_prefix_binding_and_core_present')
controls=json.loads((P/'CONTROLS_COPIED.json').read_bytes())
for row in controls['files']:
    assert Path(row['origin']['path']).read_bytes()==Path(row['copy']['path']).read_bytes()
    ast.parse(Path(row['copy']['path']).read_bytes())
spec=importlib.util.spec_from_file_location('publication_fix_transaction',P/'transaction.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
assert module.WORK.resolve()==P.resolve();passed('audited_controls_byte_identical_and_transaction_WORK_is_P')
baselines=json.loads((P/'BASELINES.json').read_bytes())['files']
assert all(sha(Path(row['path']).read_bytes())==row['sha256'] for row in baselines)
passed('original_core_release_runtime_v5_kernel_source_and_readers_unchanged')
rows=[]
def item(source,destination):
    source=Path(source).resolve();destination=Path(destination).resolve()
    assert source.is_relative_to(P.resolve()) and destination.is_relative_to(R.resolve())
    rows.append({'source':str(source),'destination':str(destination),'sha256':sha(source.read_bytes()),
        'baseline':sha(destination.read_bytes()) if destination.is_file() else None})
item(P/'staging/IALD_TGL_MEMORY_CORE.md',b['new_core_destination'])
for folder,live in [('haiku55','haiku55'),('shared','haiku')]:
    root=P/'packages'/folder;dest=R/'.iald_runtime'/live
    manifest=json.loads((root/'manifest.json').read_bytes());manifest['measurement_receipt']=str(dest/'native_count.json')
    write(root/'manifest_install.json',manifest)
    for src,name in [(root/'prefix.md','prefix.md'),(root/'manifest_install.json','manifest.json'),(root/'native_count.json','native_count.json')]:item(src,dest/name)
item(P/'staging/manifest_install.json',R/'iald_nucleo_fixo.json')
assert len(rows)==8 and not any(Path(row['destination']).suffix=='.py' for row in rows)
plan={'schema':'IALD_TRANSACTION_SOURCE_DEST_SHA_BASELINE','files':rows,
    'scope':'Two operational publication labels plus dependent core/prefix/measurement bindings only.',
    'old_core_and_release_retained':True,'source_paths_within_WORK':str(P),'requires_distinct_review':True}
write(P/'install_plan.json',plan);passed('eight_file_transaction_sources_inside_P_and_correct_live_baselines')
plan_sha=sha((P/'install_plan.json').read_bytes())
write(P/'validation/final_checks.json',{'passed':True,'plan_sha256':plan_sha,'test_count':len(tests),'tests':tests,
    'transaction_sha256':sha((P/'transaction.py').read_bytes()),'maintenance_sha256':sha((P/'maintenance.py').read_bytes()),
    'deploy_controlled_sha256':sha((P/'deploy_controlled.py').read_bytes()),
    'independent_review_not_created':True,'production_actions':0})
assert not (P/'validation/review_final.json').exists();assert not (P/'deployment.json').exists()
delivery={'status':'PREPARED_TWO_PUBLICATION_LABELS_FIXED_REVIEW_REQUIRED_NOT_INSTALLED','reference':str(task.REF),
    'task_id':'publication_label_fix','actor':'codex-v394-app-builder','lease_id':check['lease_id'],'commit':b['commit'],
    'old_deployment':b['previous_deployment'],'new_deployment':b['deployment'],
    'exact_two_label_test':pin(P/'EXACT_LABEL_TEST.json'),'core_diff':pin(P/'core_label_diff.patch'),
    'new_core':pin(P/'staging/IALD_TGL_MEMORY_CORE.md'),'native_prefix':pin(P/'native_prefix.md'),
    'bindings':pin(P/'PREPARED_BINDING.json'),'counts':counts,'public_count_receipts':pin(P/'NATIVE_COUNTS_COMPLETE.json'),
    'plan':pin(P/'install_plan.json'),'validation':pin(P/'validation/final_checks.json'),
    'controls':pin(P/'CONTROLS_COPIED.json'),'baselines':pin(P/'BASELINES.json'),
    'plan_files':8,'tests_passed':len(tests),'core_only_label_edits':2,'kernel_files_regenerated':0,
    'scientific_pending_labels_unchanged':True,'readers_already_32MB_unchanged':True,
    'provider_count_requests':6,'provider_generation_calls':0,'operator_context_egress':False,
    'runtime_files_changed':0,'installation_executed':False,'reviewer':'Real distinct reviewer required; no self-acceptance.',
    'application_owner':'Main controls publication_label_apply, maintenance/deployment and live verification.'}
write(P/'DELIVERY_PREPARED.json',delivery)
print(json.dumps({'status':delivery['status'],'plan_files':8,'tests_passed':len(tests),'new_core_sha256':b['deployment']['operational_core_sha256']}))
