"""Static stage only: helpers, source transpose and documentary reexamination custody."""
from pathlib import Path
import ast,datetime,difflib,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_tomita_root_latest_run.txt').read_text().strip())
SQUARE=Path((REV/'tomita_square_latest_run.txt').read_text().strip())
OLD=max(p for p in SQUARE.glob('integrated_*') if (p/'verification.json').exists())
DEST=RUN/('static_integrated_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes());load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
def save(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))
def embedded(raw):
    t=ast.parse(raw);ns=[n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='_EMBEDDED_KERNEL_FILES' for x in n.targets)];assert len(ns)==1
    d=ast.literal_eval(ns[0].value);ns[0].value=ast.Constant('EMBEDDED_EXCLUDED');return d,ast.dump(t,include_attributes=False)
files=['integrate_v350.py','compile_integrated.py','test_gate_extension.py','record_tomita_root_progress.py','verify_tomita_root_custody.py',
 'tomita_root_draft_status.json','tomita_square_custody.json','integration.json','gate_extension.py',
 'REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md','REEXAME_CHATGPT_20260912/source_evidence.json',
 'REEXAME_CHATGPT_20260912/custody.json','REEXAME_CHATGPT_20260912/inventory.json','REEXAME_CHATGPT_20260912/verification.json']
for f in files:write(DEST/f,(ROOT/f).read_bytes())
for f in files:
    if f.endswith('.py'):ast.parse((DEST/f).read_bytes())
mathparent=load(DEST/'tomita_square_custody.json');docparent=load(DEST/'REEXAME_CHATGPT_20260912/custody.json')
status=load(DEST/'tomita_root_draft_status.json');devM=load(RUN/'manifest.json');close=load(RUN/'closure_dev.json')
assert docparent['parent_sha256']==hf(DEST/'tomita_square_custody.json')
assert status['integrated_working_sha256']==mathparent['working_sha256']==docparent['working_sha256']
assert status==load(RUN/'tomita_root_draft_status.json')
rec=(DEST/'record_tomita_root_progress.py').read_text(encoding='utf-8')
assert "draft['parent_custody_sha256']" not in rec
assert "draft['integrated_working_sha256'] == square['working_sha256'] == parent['working_sha256']" in rec
assert "parent['parent_sha256'] == sha(square_path)" in rec
oldum=next(p for p in sorted(ROOT.glob('um.py.bak_*'),reverse=True) if hf(p)==docparent['working_sha256'])
before,oldast=embedded(oldum.read_bytes());now,newast=embedded((ROOT/'um.py').read_bytes())
I=load(DEST/'integration.json');assert hf(ROOT/'um.py')==I['working_sha256'] and len(now)==I['embedded_files']
assert oldast==newast and (ROOT/'gate_extension.py').read_bytes()==(OLD/'gate_extension.py').read_bytes()
trans={}
for rel,s in devM['sources'].items():
    name=Path(rel).stem;key='TGLExt/V350'+name+'.lean';raw=Path(s['path']).read_bytes();out=(ROOT/'kernel'/key).read_bytes()
    assert sha(raw)==s['sha256'] and re.sub(rb'^import TGLV350\.',b'import TGLExt.V350',raw,flags=re.M)==out and now[key].encode()==out
    write(DEST/'sources'/key,out);trans[name]={'dev_sha256':sha(raw),'integrated_sha256':sha(out),'literal_import_rewrite_only':True,'embedded_equal':True}
assert set(now)-set(before)=={'TGLExt/V350'+n+'.lean' for n in trans}
assert not(set(before)-set(now)) and {k for k in before if before[k]!=now[k]}=={'TGLExt.lean','TGL/Audit.lean'}
for root in ['TGLExt.lean','TGL/Audit.lean']:
    raw=(ROOT/'kernel'/root).read_bytes();assert now[root].encode()==raw;write(DEST/'sources'/root,raw)
    assert all(len(re.findall(r'^import TGLExt\.V350'+n+r'\s*$',raw.decode(),re.M))==1 for n in trans)
    write(DEST/(root.replace('/','_')+'.diff.txt'),'\n'.join(difflib.unified_diff(before[root].splitlines(),now[root].splitlines(),lineterm='')).encode())
oldtargets=re.findall(r'^#print axioms ([\w.]+)',before['TGL/Audit.lean'],re.M);newtargets=re.findall(r'^#print axioms ([\w.]+)',now['TGL/Audit.lean'],re.M)
assert set(newtargets)-set(oldtargets)==set(status['targets']) and len(newtargets)-len(oldtargets)==30
assert all(newtargets.count(n)==oldtargets.count(n) for n in oldtargets)
for f in ['integrate_v350.py','compile_integrated.py','test_gate_extension.py']:
    diff='\n'.join(difflib.unified_diff((OLD/f).read_text(encoding='utf-8').splitlines(),(DEST/f).read_text(encoding='utf-8').splitlines(),fromfile='square/'+f,tofile='root/'+f,lineterm=''))
    write(DEST/(f+'.diff.txt'),diff.encode())
itree=ast.parse((DEST/'integrate_v350.py').read_bytes())
batch=next(ast.literal_eval(n.value) for n in itree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='tomita_batch' for t in n.targets))
batchtargets=[]
for n in batch:
    raw=(ROOT/'kernel/TGLV350'/(n+'.lean')).read_text(encoding='utf-8')
    batchtargets+=re.findall(r'^#print axioms ([\w.]+)',raw,re.M)
assert len(batch)==27 and len(batchtargets)==len(set(batchtargets))==182
ctree=ast.parse((DEST/'compile_integrated.py').read_bytes())
clist=next(ast.literal_eval(n.iter) for n in ctree.body if isinstance(n,ast.For) and isinstance(n.iter,ast.List) and any(isinstance(x,ast.Constant) and x.value=='TGL/Audit.lean' for x in n.iter.elts))
assert clist[-7:]==['TGLExt/V350'+n+'.lean' for n in status['modules']]+['TGLExt.lean','TGL/Audit.lean']
t=ast.parse((DEST/'test_gate_extension.py').read_bytes());old=ast.parse((OLD/'test_gate_extension.py').read_bytes());added={}
for n in ast.walk(t):
    if not isinstance(n,ast.Dict):continue
    keep=[]
    for k,v in zip(n.keys,n.values):
        if isinstance(k,ast.Constant) and k.value=='bounded_Tomita_resolvent_and_exact_positive_root':added[k.value]=ast.literal_eval(v)
        else:keep.append((k,v))
    n.keys=[k for k,v in keep];n.values=[v for k,v in keep]
assert len(added)==1 and ast.dump(t,include_attributes=False)==ast.dump(old,include_attributes=False)
save(DEST/'added_control.json',added)

R=DEST/'REEXAME_CHATGPT_20260912';SE=load(R/'source_evidence.json');INV=load(R/'inventory.json')
assert hf(R/'RELATORIO_REAPROVEITAMENTO.md')==docparent['report_sha256']
assert hf(R/'source_evidence.json')==docparent['source_evidence_sha256']
assert hf(R/'inventory.json')==docparent['inventory_sha256']==SE['inventory_sha256']
assert len((ROOT/'REEXAME_CHATGPT_20260912/rg_stdout.txt').read_bytes().splitlines())==SE['listed_paths']==73711
assert len(INV['rows'])==SE['selected_source_paths']==339
assert len({r['sha256'] for r in INV['rows']})==SE['selected_distinct_byte_hashes']==159
assert sum(bool(r['v350_normalized_imports_equal']) for r in INV['rows'])==SE['normalized_matching_paths']==261
assert len({Path(r['path']).name for r in INV['rows'] if r['v350_normalized_imports_equal']})==SE['normalized_matching_basenames']==99
selected_pins={r['path']:hf(r['path'])==r['sha256'] and Path(r['path']).stat().st_size==r['bytes'] for r in INV['rows']}
assert all(selected_pins.values())
sourcepins={n:hf(p['path'])==p['sha256'] and Path(p['path']).stat().st_size==p['bytes'] for n,p in SE['source_pins'].items()};assert all(sourcepins.values())
assert hf(OLD/'kernel_incremental_evidence.json')==SE['existing_audit_sha256']
oldE=load(OLD/'kernel_incremental_evidence.json');entries={}
original_embedded,_=embedded((ROOT/'fontes/um_v350_original.py').read_bytes())
for r in SE['theorems']:
    matches=[f for f,txt in original_embedded.items() if re.search(r'^(?:noncomputable )?(?:def|theorem|lemma) '+re.escape(r['name'])+r'\b',txt,re.M)]
    assert sorted(matches)==sorted(r['v350_embedded_files'])
    for n,a in r['existing_audit_entries'].items():assert oldE['axiom_report'][n]==a;entries[n]=a
assert len(entries)==6
surfaces={}
assert len(docparent['surface_sha256'])==len(docparent['backups'])==len(docparent['surface_before_sha256'])==34
for p,h in docparent['surface_sha256'].items():
    current=Path(p).read_bytes();backup=Path(docparent['backups'][p]);b=backup.read_bytes()
    assert sha(current)==h and sha(b)==docparent['surface_before_sha256'][p] and current.startswith(b) and len(current)>len(b)
    assert backup.parent==Path(p).parent
    surfaces[p]={'source_sha256':sha(current),'backup_sha256':sha(b),'exact_prefix':True,'new_bytes':len(current)-len(b)}
assert all(v is False for v in docparent['remaining_flags'].values()) and len(docparent['remaining_flags'])==6
assert docparent['memory_note_only'] and not docparent['compilation_run_for_reexamination'] and not docparent['gate_changed']
cfg=load(ROOT/'environment.json');assert hf(cfg['original_source'])==docparent['original_sha256']==I['base_sha256']
assert all(hf(p)==h for p,h in devM['previous_reviews'].items()) and hf(close['review_path'])==close['review_sha256']
verifier=(DEST/'verify_tomita_root_custody.py').read_text(encoding='utf-8')
bincheck='.olean' in verifier and 'output_sha256' in verifier
findings=[] if bincheck else [{'priority':'P2','file':str(ROOT/'verify_tomita_root_custody.py'),'line':19,
 'end_line':31,'title':'Verifier does not recheck compiled binaries',
 'detail':'Artifacts JSON and sources are hashed, but no .olean is read. A later binary change with sources/JSON unchanged leaves all verifier observations unchanged. Recorder checks binaries once; restore a read-only record/source/output hash loop in verifier.'}]
data={'timestamp':datetime.datetime.now().astimezone().isoformat(),'path':str(DEST),'mode':'STATIC_ONLY__FINAL_AUTHOR_BUILD_AND_TEST_RESULTS_NOT_CONSUMED',
 'working_source_sha256':I['working_sha256'],'embedded_source_files':I['embedded_files'],'source_AST_unchanged':True,'gate_extension_bytes_unchanged':True,
 'transposition':trans,'batch_modules':len(batch),'batch_targets':182,'new_targets':30,'compile_list_last_seven':clist[-7:],
 'new_test_entries':added,'old_test_AST_preserved':True,'corrected_recorder_parent_relation_valid':True,
 'documentary_parent_sha256':hf(R/'custody.json'),'mathematical_parent_sha256':hf(DEST/'tomita_square_custody.json'),
 'reexamination_counts':{'listed_paths':73711,'selected':339,'distinct_hashes':159,'normalized_paths':261,'normalized_basenames':99},
 'selected_339_source_pins_match':True,'source_pins':sourcepins,'six_existing_audit_entries_match':True,
 'normalization_not_independently_rerun':True,'archive_mathematics_not_recertified':True,
 'documentary_custody_34_exact_pairs':surfaces,'prospective_recorder_surface_count':34,'findings':findings,
 'final_integrated_verdict_pending':True,'Lean_or_author_programs_executed':False,'artifacts':{f:hf(DEST/f) for f in files}}
save(DEST/'verification_static.json',data)
print(json.dumps({k:v for k,v in data.items() if k not in ['transposition','documentary_custody_34_exact_pairs','source_pins','artifacts']},ensure_ascii=False,indent=2))
