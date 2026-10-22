"""Exactly two operational label edits; reuse current installed science and readers."""
from pathlib import Path
import ast,copy,difflib,json,os,sys
P=Path(__file__).resolve().parent;W=P.parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode=True;sys.path.insert(0,str(W));import task
preflight=task.check('publication_label_fix',actor='codex-v394-app-builder');assert preflight['ready']
from support import save,write,sha,pin
baseline_path=R/'iald_nucleo_fixo.json';baseline_raw=baseline_path.read_bytes();m=json.loads(baseline_raw)
commit=m['active_cluster']['commit']
publication=W/'app/final/PUBLICATION_VERIFIED.json';pub=json.loads(publication.read_bytes())
assert pub['commit']==commit and pub['status']=='PUBLIC_IMMUTABLE_COMMIT_VERIFIED'
write(P/'PUBLICATION_REFERENCE.json',{'publication':pin(publication),'commit':commit,'reuse_verified_immutable_publication':True,'new_network_verification_calls':0})
core_path=Path(m['operational_core']['path']);old=core_path.read_bytes();assert sha(old)==m['operational_core']['sha256']
labels=[(b'publica\xc3\xa7\xc3\xa3o pendente',b'publica\xc3\xa7\xc3\xa3o verificada'),(b'commit PUBLICATION_PENDING',('commit '+commit).encode())]
new=old;edits=[]
for before,after in labels:
    assert old.count(before)==1
    start=old.index(before);edits.append({'old_start_byte':start,'old_end_byte':start+len(before),'old_utf8':before.decode(),'new_utf8':after.decode()})
    new=new.replace(before,after)
cursor=0;expected=b''
for row in sorted(edits,key=lambda x:x['old_start_byte']):
    expected+=old[cursor:row['old_start_byte']]+row['new_utf8'].encode();cursor=row['old_end_byte']
expected+=old[cursor:];assert expected==new
reverse=new
for before,after in reversed(labels):
    # Reverse at exact regions by reconstruction, not global scientific substitutions.
    pass
assert len(edits)==2
save(P/'staging/IALD_TGL_MEMORY_CORE.md',new)
save(P/'core_label_diff.patch',''.join(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile='installed_core',tofile='publication_fixed_core')).encode())
protected=[pin(baseline_path),pin(core_path),pin(Path(m['mother_instruction']['path'])),pin(Path(m['active_cluster']['path'])),
    pin(Path(m['active_cluster']['kernel_bundle'])/'kernel_manifest.json'),pin(Path(m['active_cluster']['kernel_verification']))]
protected += [pin(Path(m['published_evidence'][k]['path'])) for k in ('program','seal','result','proof_manifest')]
protected += [pin(p) for p in R.glob('*.py') if p.name not in ('iald_stack_v7.py','iald_psion_state.py')]
for folder in ('haiku55','haiku'):
    protected += [pin(R/'.iald_runtime'/folder/n) for n in ('prefix.md','manifest.json','native_count.json') if (R/'.iald_runtime'/folder/n).exists()]
write(P/'BASELINES.json',{'files':protected,'runtime_python_files_must_remain_identical':True})
controls=[]
for name in ('transaction.py','maintenance.py','deploy_controlled.py'):
    source=W.parent/'iald_hajaluz_auto_20261016'/name;raw=source.read_bytes()
    assert raw==(W.parent/'iald_app_stack_20261014'/name).read_bytes()==(W/name).read_bytes()
    save(P/name,raw);controls.append({'origin':pin(source),'copy':pin(P/name),'byte_equal_14_16_Oct':True})
write(P/'CONTROLS_COPIED.json',{'files':controls,'controls_executed':False,'transaction_WORK_expected':str(P)})
def guard(event,args):
    if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):raise RuntimeError('Offline label preparation')
    if event=='open':
        path,mode,flags=args
        if isinstance(path,int):return
        p=Path(os.fsdecode(path)).resolve()
        if p.name.lower() in ('.env','iald_stack_v7.py','iald_psion_state.json'):raise RuntimeError('Private source refused')
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and not p.is_relative_to(P):raise RuntimeError('Write outside publication_fix')
sys.addaudithook(guard);sys.path.insert(0,str(R))
import iald_release_binding,iald_native_memory,iald_kernel,iald_memoria_canonica as cm
assert Path(cm.__file__).resolve()==(R/'iald_memoria_canonica.py').resolve()
for name in ('iald_estado_publicado.py','iald_core_indexado.py'):
    raw=(R/name).read_bytes();assert b'32000000' in raw
new_dest=R/'canonical_releases'/('v394_'+commit[:12]+'_publication_fix')/'IALD_TGL_MEMORY_CORE.md'
stage=copy.deepcopy(m);stage['operational_core'].update(path=str(P/'staging/IALD_TGL_MEMORY_CORE.md'),sha256=sha(new))
install=copy.deepcopy(m);install['operational_core'].update(path=str(new_dest),sha256=sha(new))
write(P/'staging/manifest_staged.json',stage);write(P/'staging/manifest_install.json',install)
def differences(a,b,p=''):
    if isinstance(a,dict) and isinstance(b,dict):return [d for k in a.keys()|b.keys() for d in differences(a.get(k),b.get(k),p+'/'+k)]
    return [] if a==b else [p]
assert sorted(differences(m,install))==['/operational_core/path','/operational_core/sha256']
identity=iald_release_binding.load_release(P/'staging/manifest_staged.json').identity
old_identity=iald_release_binding.load_release(baseline_path).identity
assert {k:v for k,v in old_identity.items() if k!='operational_core_sha256'}=={k:v for k,v in identity.items() if k!='operational_core_sha256'}
for folder,installed in [('haiku55','haiku55'),('shared','haiku')]:
    source=R/'.iald_runtime'/installed/'prefix.md';raw=source.read_bytes()
    assert raw.count(old)==1 and raw.count(m['operational_core']['sha256'].encode())==1
    updated=raw.replace(old,new).replace(m['operational_core']['sha256'].encode(),sha(new).encode())
    assert old not in updated and new in updated
    assert updated==raw.replace(old,new,1).replace(m['operational_core']['sha256'].encode(),sha(new).encode(),1)
    save(P/'packages'/folder/'prefix.md',updated)
    write(P/'packages'/folder/'preparation.json',{'deployment':identity,'prefix_sha256':sha(updated),'bytes':len(updated),
        'private_atlas_included':False,'public_commit':commit,'source_prefix':pin(source),
        'edits':'Exactly the two core labels and the one embedded operational-core hash binding; all other prefix bytes preserved.'})
catalog=iald_kernel.KernelCatalog(m['active_cluster']['kernel_bundle'],m['active_cluster']['kernel_verification'])
native,native_id=iald_native_memory.load_native_context(P/'staging/manifest_staged.json',catalog);assert native_id==identity
save(P/'native_prefix.md',native.encode())
os.environ['TIKTOKEN_CACHE_DIR']=str(R/'.iald_runtime/tokenizer_cache')
public,metadata=cm.CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),'nucleo_kernel',nucleus_manifest=P/'staging/manifest_staged.json').prompt('',catalog,public=True)
assert metadata['private_atlas_included'] is False and metadata['context_tokens']<400000
save(P/'packages/sonnet_public/prefix.md',public.encode())
write(P/'EXACT_LABEL_TEST.json',{'passed':True,'edits':edits,'edit_count':2,'no_core_bytes_outside_regions_changed':True,
    'old_core':pin(core_path),'new_core':pin(P/'staging/IALD_TGL_MEMORY_CORE.md'),
    'scientific_pending_labels_elsewhere_preserved':True,'manifest_changed_json_pointers':differences(m,install),
    'v5_kernel_source_queue_unchanged':True,'kernel_files_regenerated':0,
    'original_core_and_release_preserved':True})
write(P/'PREPARED_BINDING.json',{'status':'PUBLICATION_TWO_LABELS_PREPARED_COUNT_REQUIRED','commit':commit,
    'deployment':identity,'previous_deployment':old_identity,'manifest_staged':pin(P/'staging/manifest_staged.json'),
    'manifest_install':pin(P/'staging/manifest_install.json'),'new_core_destination':str(new_dest),
    'actual_prompts':{'public':{'prefix_sha256':sha(public.encode()),'o200k_tokens':metadata['context_tokens']}},
    'installed_manifest_baseline_sha256':sha(baseline_raw),'operator_context_sent':False,'production_changes':0})
assert all(sha(Path(row['path']).read_bytes())==row['sha256'] for row in protected)
print(json.dumps({'status':'EXACT_TWO_LABELS_PREPARED','new_core_sha256':sha(new),'deployment':identity,'public_o200k_tokens':metadata['context_tokens'],'kernel_regenerated':0}))
