"""Read frozen/current evidence and author helper AST; never execute author code."""
from pathlib import Path
import ast, copy, datetime, difflib, hashlib, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'homogeneous_right_latest_run.txt').read_text().strip())
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV)
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b;tmp.replace(p)
def save(p,x):write(p,json.dumps(x,ensure_ascii=False,indent=2).encode('utf-8'))
m=load(RUN/'manifest.json');c=load(RUN/'compilation.json');d=load(RUN/'homogeneous_right_draft_status.json')
assert all(c[k] for k in ['complete','all_exit_zero','all_axioms_allowed','exact_28_targets','five_binaries_equal_author',
 'sources_and_author_binaries_unchanged','dependencies_preserved','previous_reviews_preserved','memory_surfaces_preserved','um_unchanged','gate_unchanged'])
allowed={'propext','Classical.choice','Quot.sound'}
records=[]
for row in c['records']:
    for p,h in [(row['command'][3],row['source_sha256']),(row['command'][2],row['output_sha256']),
                (row['stdout'],row['stdout_sha256']),(row['stderr'],row['stderr_sha256'])]:assert sha(Path(p).read_bytes())==h
    assert row['returncode']==0 and all(set(a)==allowed for a in row['axioms'].values())
    records.append({'module':row['module'],'returncode':row['returncode'],'stdout_sha256':row['stdout_sha256'],
      'output_sha256':row['output_sha256'],'targets':len(row['axioms']),'binary_equals_author':row.get('binary_equals_author')})
aud=Path(c['records'][-1]['stdout']).read_text(encoding='utf-8')
checks=[n for n in m['declarations'] if re.search('^'+re.escape(n)+r'(?= |\.\{)',aud,re.M)]
assert len(checks)==28 and set(checks)==set(d['targets'])
author=[]
for name,pin in d['modules'].items():
    src=ROOT/'kernel/TGLV350'/(name+'.lean');binary=ROOT/'build/TGLV350'/(name+'.olean')
    log=Path(pin['final_log']);lb=log.read_bytes();lr=json.loads(lb)
    assert sha(src.read_bytes())==lr['sha256']==pin['source_sha256']
    assert sha(binary.read_bytes())==lr['output_sha256']==pin['binary_sha256']
    assert sha(lb)==pin['final_log_sha256'] and sha(Path(lr['stdout']).read_bytes())==pin['stdout_sha256']
    assert lr['returncode']==lr['lean_returncode']==0 and lr['source_unchanged_during_compile'] and lr['output_exists']
    author.append({'module':name,**pin})
for n,r in m['dependencies'].items():
    assert sha(Path(r['frozen_source']).read_bytes())==r['source_sha256'] and sha(Path(r['frozen_binary']).read_bytes())==r['sha256']
    assert sha(Path(r['source']).read_bytes())==r['source_sha256'] and sha(Path(r['binary']).read_bytes())==r['sha256']
old=(RUN/'record_homogeneous_right_memory.py').read_bytes();new=(ROOT/'record_homogeneous_right_memory.py').read_bytes()
a=old.decode('utf-8').splitlines(True);b=new.decode('utf-8').splitlines(True)
changes=[(tag,a[i:j],b[k:l]) for tag,i,j,k,l in difflib.SequenceMatcher(a=a,b=b).get_opcodes() if tag!='equal']
assert len(changes)==1 and changes[0][0]=='insert' and len(changes[0][2])==6
insert=''.join(changes[0][2]);assert 'gate_extension.py' in insert and 'três contratos' in insert
ta=ast.parse(old.decode('utf-8'));tb=ast.parse(new.decode('utf-8'))
def redact_report(tree):
    t=copy.deepcopy(tree);found=0
    for n in ast.walk(t):
        if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='report' for x in n.targets):
            assert isinstance(n.value,ast.JoinedStr);n.value=ast.Constant('REPORT_TEXT');found+=1
    assert found==1
    return ast.dump(t,include_attributes=False)
assert redact_report(ta)==redact_report(tb)
write(RUN/'record_homogeneous_right_memory.final.py',new)
write(RUN/'recorder_documentary_change.diff',''.join(difflib.unified_diff(a,b,fromfile='snapshot',tofile='final')).encode('utf-8'))
gate=(ROOT/'gate_extension.py').read_bytes();gt=ast.parse(gate.decode('utf-8'))
contracts=next(ast.literal_eval(n.value) for n in gt.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='_V350_MODULAR_CONTRACTS' for x in n.targets))
assert len(contracts)==3 and not(set(contracts)&set(m['six_flags']))
parent=load(ROOT/'scalar_weight_gns_custody.json')
assert sha((ROOT/'scalar_weight_gns_custody.json').read_bytes())==m['custody_sha256']
assert sha((ROOT/'homogeneous_right_draft_status.json').read_bytes())==m['draft_status_sha256']
assert sha((ROOT/'RELATORIO_DIREITA_MODULAR_GNS_DEV.md').read_bytes())==m['report_sha256']
assert sha((ROOT/'um.py').read_bytes())==m['initial_um_sha256'] and sha(gate)==m['initial_gate_sha256']
assert all(sha((ROOT/p).read_bytes())==h for p,h in parent['artifacts'].items())
assert all(sha(Path(p).read_bytes())==h for p,h in m['memory_surface_sha256'].items())
assert all(sha(Path(p).read_bytes())==h for p,h in m['previous_reviews'].items())
ev=load(ROOT/'kernel_incremental_evidence.json')
assert all(ev[k] is False for k in m['six_flags'])
v={'timestamp':datetime.datetime.now().astimezone().isoformat(timespec='seconds'),'status':'DEV_REVIEWED__INTEGRATION_PENDING',
 'own_records':records,'all_six_rc0':True,'checked_types':checks,'all_28_exact_trio':True,'five_binaries_equal_author':True,
 'author_final_records_verified':author,'frozen_project_dependencies':len(m['dependencies']),'dependency_pins_preserved':True,
 'compilation_sha256':sha((RUN/'compilation.json').read_bytes()),'manifest_sha256':sha((RUN/'manifest.json').read_bytes()),
 'author_history_sha256':sha((RUN/'author_history.json').read_bytes()),'recorder_initial_sha256':sha(old),'recorder_final_sha256':sha(new),
 'recorder_change':'ONLY_SIX_REPORT_LINES; AST_OUTSIDE_REPORT_IDENTICAL; USER_ANNOUNCED',
 'compilation_recorder_unchanged_false_explained':not c['recorder_unchanged'],
 'recorder_executed':False,'recording_34_surfaces_static_review_only':True,'all_34_surface_pins_unchanged':True,
 'parent_artifacts_unchanged':True,'previous_reviews_unchanged':True,'gate_contracts':contracts,'six_flags_false':m['six_flags'],
 'integration_reviewed':False,'monolith_executed':False,'next_modules_reviewed':False}
save(RUN/'verification.json',v)
print(json.dumps({k:v[k] for k in ['status','all_six_rc0','all_28_exact_trio','five_binaries_equal_author','frozen_project_dependencies','recorder_final_sha256','compilation_sha256','manifest_sha256']},ensure_ascii=False))
