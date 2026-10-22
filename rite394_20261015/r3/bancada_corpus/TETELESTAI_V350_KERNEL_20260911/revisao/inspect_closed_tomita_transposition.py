"""Static integration comparison before final author build evidence; executes no author code."""
from pathlib import Path
import ast, datetime, difflib, hashlib, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'closed_tomita_batch_latest_run.txt').read_text(encoding='utf-8'))
DEST=RUN/('source_integration_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
def save(p,v):write(p,json.dumps(v,indent=2,ensure_ascii=False).encode())
def parse(raw):
    tree=ast.parse(raw);nodes=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_EMBEDDED_KERNEL_FILES' for t in n.targets)]
    assert len(nodes)==1
    d=ast.literal_eval(nodes[0].value);tree.body.remove(nodes[0]);return d,ast.dump(tree,include_attributes=False)
m=json.loads((RUN/'manifest.json').read_bytes());prior=json.loads((ROOT/'gns_cut_maps_custody.json').read_bytes())
oldrun=Path((REV/'gns_cut_maps_latest_run.txt').read_text(encoding='utf-8'))
oldcap=max(p for p in oldrun.glob('final_integrated_*') if (p/'verification.json').exists())
oldv=json.loads((oldcap/'verification.json').read_bytes());assert oldv['um_sha256']==prior['working_sha256']
oldum=next(p for p in sorted(ROOT.glob('um.py.bak_*'),reverse=True) if sha(p.read_bytes())==prior['working_sha256'])
old,oldast=parse(oldum.read_bytes());raw=(ROOT/'um.py').read_bytes();new,newast=parse(raw)
for f in ['integration.json','gns_cut_maps_custody.json','gate_extension.py','integrate_v350.py','compile_integrated.py','compile_lean.py','test_gate_extension.py','record_closed_tomita_progress.py']:
    write(DEST/f,(ROOT/f).read_bytes())
i=json.loads((DEST/'integration.json').read_bytes())
trans={}
for rel,r in m['sources'].items():
    name=Path(rel).stem;key='TGLExt/V350'+name+'.lean';ib=(ROOT/'kernel'/key).read_bytes();dev=Path(r['snapshot']).read_bytes()
    trans[name]={'dev_sha256':sha(dev),'integrated_sha256':sha(ib),'dev_frozen':sha(Path(r['path']).read_bytes())==r['sha256'],'only_import_prefix_rewrite_bytes':re.sub(rb'^import TGLV350\.',b'import TGLExt.V350',dev,flags=re.M)==ib,'embedded_byte_equal':new[key].encode()==ib}
    write(DEST/'sources'/key,ib)
roots={}
for root in ['TGLExt.lean','TGL/Audit.lean']:
    now=(ROOT/'kernel'/root).read_bytes();write(DEST/'sources'/root,now)
    roots[root]={'sha256':sha(now),'embedded_byte_equal':new[root].encode()==now,'imports_each_once':all(len(re.findall(r'^import TGLExt\.V350'+n+r'\s*$',now.decode(),re.M))==1 for n in trans)}
    write(DEST/(root.replace('/','_')+'.diff.txt'),'\n'.join(difflib.unified_diff(old[root].splitlines(),new[root].splitlines(),fromfile='custodied/'+root,tofile='current/'+root,lineterm='')).encode())
oldtargets=re.findall(r'^#print axioms ([\w.]+)',old['TGL/Audit.lean'],re.M);newtargets=re.findall(r'^#print axioms ([\w.]+)',new['TGL/Audit.lean'],re.M)
test_before=ast.parse((oldcap/'test_gate_extension.py').read_bytes());test_now=ast.parse((DEST/'test_gate_extension.py').read_bytes())
before_bodies=[ast.dump(n,include_attributes=False) for n in test_before.body];now_bodies=[ast.dump(n,include_attributes=False) for n in test_now.body]
added=[n for n in test_now.body if ast.dump(n,include_attributes=False) not in before_bodies]
preserved=[s for s in now_bodies if s in before_bodies]
write(DEST/'added_test_ast.py','\n\n'.join(ast.unparse(n) for n in added).encode())
for f in ['integrate_v350.py','compile_integrated.py','test_gate_extension.py']:
    write(DEST/(f+'.diff.txt'),'\n'.join(difflib.unified_diff((oldcap/f).read_text(encoding='utf-8').splitlines(),(DEST/f).read_text(encoding='utf-8').splitlines(),fromfile='custodied/'+f,tofile='current/'+f,lineterm='')).encode())
original=Path(json.loads((ROOT/'environment.json').read_bytes())['original_source']);oh=sha(original.read_bytes())
result={'timestamp':datetime.datetime.now().astimezone().isoformat(),'path':str(DEST),'mode':'STATIC_SOURCE_AST_INSPECTION__FINAL_AUTHOR_BUILD_AND_TEST_REPORTS_NOT_YET_CONSUMED','working_sha256':sha(raw),'matches_integration_hash':sha(raw)==i['working_sha256'],'embedded_count':len(new),'matches_embedded_count':len(new)==i['embedded_files'],'previous_um_path':str(oldum),'previous_um_sha256':sha(oldum.read_bytes()),'previous_capture':str(oldcap),'python_ast_outside_embedded_unchanged':newast==oldast,'gate_extension_unchanged_bytes':(ROOT/'gate_extension.py').read_bytes()==(oldcap/'gate_extension.py').read_bytes(),'added_embedded':sorted(set(new)-set(old)),'removed_embedded':sorted(set(old)-set(new)),'changed_old_embedded':sorted(k for k in old if k in new and old[k]!=new[k]),'transposition':trans,'roots':roots,'audit_added_targets_exact_99':set(newtargets)-set(oldtargets)==set(m['declarations']) and len(newtargets)-len(oldtargets)==99,'audit_old_targets_preserved':all(newtargets.count(n)==oldtargets.count(n) for n in oldtargets),'test_old_AST_preserved_in_order':preserved==before_bodies,'added_test_top_level_nodes':len(added),'original_sha256':oh,'original_equal_localbase_and_pin':oh==sha((ROOT/'fontes/um_v350_original.py').read_bytes())==i['base_sha256'],'all_previous_reviews_preserved':all(sha(Path(p).read_bytes())==h for p,h in m['previous_reviews'].items()),'artifact_sha256':{p.name:sha(p.read_bytes()) for p in DEST.iterdir() if p.is_file()},'author_scripts_executed':False}
save(DEST/'verification_source.json',result)
print(json.dumps({k:v for k,v in result.items() if k not in ['transposition','artifact_sha256']},ensure_ascii=False,indent=2))
