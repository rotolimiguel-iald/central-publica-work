from pathlib import Path
import ast,datetime,hashlib,json,os,re
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'right_graph_core_final_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
allowed={'propext','Classical.choice','Quot.sound'}
def create(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;os.replace(t,p)
def axmap(raw):
    text=raw.decode();out={}
    for name,a in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",text,re.S):
        v=sorted(x.strip() for x in a.split(',') if x.strip());assert name not in out or out[name]==v;out[name]=v
    for name in re.findall(r"'([\w.']+)' does not depend on any axioms",text):
        assert name not in out or not out[name];out[name]=[]
    return out
m=load(RUN/'manifest.json');c=load(RUN/'compilation.json')
for k in ['complete','all_exit_zero','exact_57_targets','all_axioms_allowed','new_binary_equals_author','inherited_sources_binaries_preserved','author_source_binary_preserved','dependencies_preserved','external_direct_pins_preserved','read_only_artifacts_preserved','author_final_log_streams_preserved']:assert c[k],k
assert len(c['records'])==2
draftpath=ROOT/'right_graph_core_draft_status.json';draft=load(draftpath)
parentpath=ROOT/'scalar_vna_custody.json';parent=load(parentpath)
assert draft['parent_custody_sha256']==hf(parentpath)
assert hf(ROOT/'um.py')==draft['integrated_working_sha256']==parent['working_sha256']
assert not draft['integrated'] and not draft['independent_review_complete'] and not draft['KMS_proved'] and not draft['modular_square_flow_identified'] and not draft['gate_changed'] and not draft['full_goal_complete']
assert hf(Path(draft['report_path']))==draft['report_sha256']
expected={'ComplexGraphProjection':12,'ScalarRightMultiplicationGraph':10,'HilbertProjectionBlocks':17,'ScalarRightProjectionPair':6,'FixedVectorGraphCore':9,'ScalarRightGraphCore':3}
assert list(draft['modules'])==list(expected) and len(draft['targets'])==57
own={};ownruns={}
for pointer in ['right_graph_partial_latest_run.txt','right_graph_blocks_latest_run.txt','right_fixed_graph_latest_run.txt','right_projection_pair_latest_run.txt','right_graph_core_final_latest_run.txt']:
    r=Path((REV/pointer).read_text().strip());rm=load(r/'manifest.json');rc=load(r/'compilation.json')
    assert rc['complete'] and rc['all_exit_zero'] and rc['all_axioms_allowed'] and rc['dependencies_preserved']
    ownruns[str(r)]={'manifest_sha256':hf(r/'manifest.json'),'compilation_sha256':hf(r/'compilation.json')}
    for rel,s in rm['sources'].items():
        row=next(x for x in rc['records'] if x['module']==rel)
        assert row['returncode']==0 and row['exact_targets'] and row['binary_equals_author']
        assert hf(s['snapshot'])==row['source_sha256']==s['sha256'] and hf(row['command'][2])==row['output_sha256']==s['author_binary_sha256']
        own[Path(rel).stem]={'source':s,'record':row,'run':str(r)}
assert set(own)==set(expected)
modules={};histories={};fullax={}
for name,count in expected.items():
    d=draft['modules'][name];src=ROOT/'kernel/TGLV350'/(name+'.lean');bin=ROOT/'build/TGLV350'/(name+'.olean');raw=src.read_bytes()
    assert d['targets']==count and hf(src)==d['source_sha256']==own[name]['source']['sha256']
    assert hf(bin)==d['binary_sha256']==own[name]['record']['output_sha256']
    stripped=re.sub(r'/\-.*?\-/','',raw.decode(),flags=re.S);stripped=re.sub(r'--[^\n]*','',stripped)
    assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]',stripped)
    targets=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\w.]+)$',raw.decode(),re.M)]
    assert len(targets)==len(set(targets))==count
    lp=Path(d['final_log']);log=load(lp);assert hf(lp)==d['final_log_sha256']
    assert log['returncode']==log['lean_returncode']==0 and log['source_unchanged_during_compile'] and log['output_exists']
    assert Path(log['source'])==src and Path(log['command'][2])==bin and log['sha256']==d['source_sha256'] and log['output_sha256']==d['binary_sha256']
    assert hf(log['stdout'])==d['stdout_sha256'] and hf(log['stderr'])==d['stderr_sha256'] and not Path(log['stderr']).read_bytes()
    ax=axmap(Path(log['stdout']).read_bytes());assert set(ax)==set(targets) and all(set(v)<=allowed for v in ax.values())
    assert ax==own[name]['record']['axioms'];fullax.update(ax)
    create(RUN/'final_author_sources'/(name+'.lean'),raw)
    hs=[]
    for hp in sorted((ROOT/'logs').glob(name+'_*.json')):
        hr=load(hp);out=Path(hr['stdout']).read_bytes();err=Path(hr['stderr']).read_bytes();ha=axmap(out)
        item={'log':str(hp),'returncode':hr['returncode'],'log_sha256':hf(hp),'source_sha256':hr['sha256'],'stdout_sha256':hf(hr['stdout']),'stderr_sha256':hf(hr['stderr']),'accepted_final':hp==lp,'empty_axiom_prints':[n for n,a in ha.items() if not a],'self_axiom_prints':[n for n,a in ha.items() if n in a],'sorryAx_prints':[n for n,a in ha.items() if 'sorryAx' in a]}
        hs.append(item)
        for pp in [hp,Path(hr['stdout']),Path(hr['stderr'])]:create(RUN/'final_author_history'/pp.name,pp.read_bytes())
    assert [h['log'] for h in hs if h['returncode']] == d['failed_attempts']
    histories[name]=hs
    modules[name]={'source_sha256':hf(src),'binary_sha256':hf(bin),'target_count':count,'own_run':own[name]['run'],'own_seconds':own[name]['record']['seconds'],'author_final_log':str(lp),'author_final_log_sha256':hf(lp),'author_stdout_sha256':d['stdout_sha256'],'failed_author_count':sum(h['returncode']!=0 for h in hs),'binary_equals_independent':True}
assert fullax==draft['targets']==c['records'][-1]['axioms']
assert axmap(Path(c['records'][-1]['stdout']).read_bytes())==fullax
pair=Path((REV/'right_projection_pair_latest_run.txt').read_text().strip());prevhelper=load(pair/'helper_static_inspection.json');helpers={}
for name,d in prevhelper['helpers'].items():
    p=ROOT/name;b=p.read_bytes();ast.parse(b);assert hf(p)==d['sha256']
    create(RUN/'final_helpers'/name,b);helpers[name]={'sha256':hf(p),'unchanged_from_partial_read':True,'bytes':len(b),'ast_parses':True}
for p in [draftpath,Path(draft['report_path']),parentpath]:create(RUN/'final_documents'/p.name,p.read_bytes())
surfaces={}
assert len(parent['surface_sha256'])==34
for p,h in parent['surface_sha256'].items():
    measured=hf(p);assert measured==h;surfaces[p]=measured
assert all(v is False for v in parent['remaining_flags'].values())
assert hf(ROOT/'gate_extension.py')==parent['artifacts']['gate_extension.py']
assert all(hf(p)==h for p,h in m['artifacts_readonly'].items())
assert hf(draftpath)==hf(RUN/'final_documents'/draftpath.name)
for name,d in modules.items():assert hf(ROOT/'kernel/TGLV350'/(name+'.lean'))==d['source_sha256'] and hf(ROOT/'build/TGLV350'/(name+'.olean'))==d['binary_sha256']
result={'timestamp':datetime.datetime.now().astimezone().isoformat(),'status':'SIX_MODULES_57_TARGETS_DEV_VERIFIED','module_count':6,'target_count':57,'modules':modules,'draft_sha256':hf(draftpath),'report_sha256':draft['report_sha256'],'parent_custody_sha256':hf(parentpath),'working_um_sha256':hf(ROOT/'um.py'),'own_runs':ownruns,'final_compile_sha256':hf(RUN/'compilation.json'),'audit_exactly_matches_draft_and_six_final_author_logs':True,'all_six_binaries_equal_independent':True,'all_axioms_allowed':True,'helpers':helpers,'author_history':histories,'failed_wrapper_count':modules['ScalarRightGraphCore']['failed_author_count'],'failed_total_count':sum(d['failed_author_count'] for d in modules.values()),'parent_memory_surfaces_unchanged':surfaces,'gate_extension_unchanged':True,'six_remaining_flags_inherited_false':True,'integrated_review_performed':False,'author_helpers_executed_by_reviewer':False,'memory_writes':False,'P0':[],'P1':[],'P2':[]}
create(RUN/'verification.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({k:v for k,v in result.items() if k not in ['modules','own_runs','helpers','author_history','parent_memory_surfaces_unchanged']},ensure_ascii=False))
