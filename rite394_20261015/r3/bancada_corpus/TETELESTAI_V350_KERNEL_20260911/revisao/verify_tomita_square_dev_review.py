"""Read-only pin/type reconciliation; outputs restricted to this review tree."""
from pathlib import Path
import datetime, hashlib, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
digest=lambda b:hashlib.sha256(b).hexdigest()
hashfile=lambda p:digest(Path(p).read_bytes())
load=lambda p:json.loads(Path(p).read_bytes())
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')

def put(p,b):
    assert p.resolve().is_relative_to(REV)
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=p.read_bytes(); bk=p.with_name(p.name+'.bak_'+stamp)
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp_'+stamp)
    with tmp.open('xb') as f:f.write(b)
    assert tmp.read_bytes()==b
    tmp.replace(p)

runs=[Path((REV/(n+'_latest_run.txt')).read_text().strip()) for n in
      ['scalar_tomita_adjoint','resolvent_aux','tomita_square']]
ms=[load(p/'manifest.json') for p in runs]
cs=[load(p/'compilation.json') for p in runs]
RUN=runs[-1]; M=ms[-1]; C=cs[-1]
status=load(ROOT/'tomita_square_draft_status.json')
assert hashfile(ROOT/'tomita_square_draft_status.json')==M['draft_status_sha256']
assert hashfile(ROOT/'RELATORIO_ADJUNTO_QUADRADO_DEV.md')==M['report_sha256']==status['report_sha256']
sources={}; histories=[]; graph={}; records=[]

def extract_types(p):
    text=Path(p).read_text(encoding='utf-8')
    blocks=re.findall(r"^(TGLV350\.Regular\.\w+.*?)(?=^'TGLV350\.Regular\.)",text,re.M|re.S)
    result={re.match(r'TGLV350\.Regular\.\w+',b)[0]:' '.join(b.split()) for b in blocks}
    assert len(result)==len(blocks)
    return result

fulltypes=extract_types(C['records'][-1]['stdout'])
assert set(fulltypes)==set(M['declarations'])==set(status['targets']) and len(fulltypes)==53
for run,m,c in zip(runs,ms,cs):
    assert all(v for v in c.values() if isinstance(v,bool))
    assert m['lean_path'].split(';')[0]==str(run/'build')
    paths=m['lean_path'].split(';')
    assert len(paths)==9 and all('\\.lake\\packages\\' in p for p in paths[1:])
    assert m['compiler_sha256']==M['compiler_sha256']
    for rec in c['records']:
        assert rec['returncode']==0 and rec['axioms_allowed']
        assert hashfile(rec['command'][-1])==rec['source_sha256']
        assert hashfile(rec['command'][2])==rec['output_sha256']
        for k in ['stdout','stderr']:assert hashfile(rec[k])==rec[k+'_sha256']
        assert Path(rec['stderr']).read_bytes()==b''
        assert 'error:' not in Path(rec['stdout']).read_text(encoding='utf-8')
        assert all(set(a)=={'propext','Classical.choice','Quot.sound'} for a in rec['axioms'].values())
        records.append({'run':str(run),**rec})
    types=extract_types(c['records'][-1]['stdout'])
    assert all(fulltypes[n]==t for n,t in types.items()),'Printed inherited type changed'
    for rel,s in m['sources'].items():
        name=Path(rel).stem; pin=status['modules'][name]
        assert hashfile(s['path'])==hashfile(s['snapshot'])==s['sha256']==pin['source_sha256']
        own=next(r for r in c['records'] if r['module']==rel)
        assert hashfile(ROOT/'build'/Path(rel).with_suffix('.olean'))==own['output_sha256']==pin['output_sha256']==s['author_binary_sha256']
        assert hashfile(s['author_log'])==s['author_log_sha256']==pin['log_sha256']
        assert len(s['declarations'])==pin['targets']
        assert own['axioms']==s['author_axioms']
        assert all(set(a)==set(status['targets'][n])==set(C['records'][-1]['axioms'][n]) for n,a in own['axioms'].items())
        txt=Path(s['snapshot']).read_text(encoding='utf-8')
        stripped=re.sub(r'/\-.*?\-/', '',txt,flags=re.S)
        stripped=re.sub(r'--[^\n]*','',stripped)
        forbidden=re.findall(r'^.*(?:\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]|transparency|allowUnsafe).*$',stripped,re.M)
        assert not forbidden,(name,forbidden)
        options=re.findall(r'^set_option.*$',txt,re.M)
        assert all(o in ['set_option autoImplicit false','set_option linter.unusedSectionVars false','set_option maxHeartbeats 1000000'] for o in options)
        lines={a[1]:i for i,l in enumerate(txt.splitlines(),1) if (a:=re.match(r'^(?:def|theorem)\s+(\w+)',l))}
        sources[rel]={**s,'run':str(run),'own_record':own,'declaration_lines':lines,
          'local_instances':re.findall(r'^local instance.*$',txt,re.M),'options':options,'forbidden_tokens':forbidden}
    hs=load(run/'author_history.json')
    for h in hs:
        assert hashfile(h['log'])==h['log_sha256']
        log=load(h['log'])
        for k in ['stdout','stderr']:assert hashfile(log[k])==h[k+'_sha256']
    histories+=hs
    for p,h in m['previous_reviews'].items():assert hashfile(p)==h

assert len(sources)==7 and sum(len(s['declarations']) for s in sources.values())==53
assert len(records)==10 and len(histories)==18
assert sum(h['returncode']==0 for h in histories)==7
instances=[(rel,l) for rel,s in sources.items() for l in s['local_instances']]
assert instances==[('TGLV350/ClosedAntilinearResolvent.lean','local instance realHilbert : InnerProductSpace ℝ H := InnerProductSpace.complexToReal')]
for n,d in M['dependencies'].items():
    assert hashfile(d['frozen_source'])==d['source_sha256']
    assert hashfile(d['frozen_binary'])==d['sha256']
    graph[n]=re.findall(r'^import\s+([\w.]+)',Path(d['frozen_source']).read_text(encoding='utf-8'),re.M)
for rel,s in M['sources'].items():graph[rel[:-5].replace('/','.')]=s['imports']
active=set();done=set()
def visit(n):
    if n not in graph or n in done:return
    assert n not in active,n
    active.add(n)
    for dep in graph[n]:visit(dep)
    active.remove(n);done.add(n)
for n in graph:visit(n)
new={rel[:-5].replace('/','.') for rel in sources}
assert all(not(new & set(ds)) for n,ds in graph.items() if n not in new)

cfg=load(ROOT/'environment.json')
assert hashfile(cfg['lean'])==M['compiler_sha256']
custody=load(ROOT/'closed_tomita_custody.json')
assert hashfile(ROOT/'closed_tomita_custody.json')==M['custody_sha256']==status['parent_custody_sha256']
assert hashfile(cfg['original_source'])==status['original_sha256']==custody['original_sha256']
assert hashfile(ROOT/'um.py')==status['working_sha256']==custody['working_sha256']==M['initial_um_sha256']
pkg=Path(cfg['lean_path'][6]).parents[3]/'Mathlib'
refs={}
for rel in ['Analysis/InnerProductSpace/LinearPMap.lean','LinearAlgebra/LinearPMap.lean',
 'Analysis/InnerProductSpace/Projection/Basic.lean','Analysis/InnerProductSpace/ProdL2.lean',
 'Analysis/InnerProductSpace/Basic.lean']:
    p=pkg/rel; b=p.read_bytes();put(RUN/'mathlib_references'/rel,b)
    refs[rel]={'path':str(p),'sha256':digest(b)}
review=REV/'REVIEW_SCALAR_TOMITA_ADJOINT.md'
closure=load(runs[0]/'closure_dev.json')
assert hashfile(review)==closure['review_sha256']
result={'timestamp':datetime.datetime.now().astimezone().isoformat(),'status':'DEV_COMPLETE_NO_P0_P1_P2',
 'runs':[str(r) for r in runs],'sources':sources,'records':records,'history_attempts':len(histories),
 'history_rc0':sum(h['returncode']==0 for h in histories),'history_rc1':sum(h['returncode']==1 for h in histories),
 'all_history_logs_streams_preserved':True,'all_7_sources_and_bins_match_status':True,
 'all_7_own_bins_equal_author':True,'all_53_types_exact':True,'inherited_35_printed_types_unchanged':True,
 'all_53_axioms_equal_author_and_allowed':True,'printed_types':fulltypes,'findings':[],
 'dependency_count':len(M['dependencies']),'project_graph_modules':len(graph),'acyclic':True,
 'old_dependencies_do_not_import_any_of_7_new_modules':True,'dependencies_preserved':True,
 'lean_path':M['lean_path'],'no_author_project_build_in_lean_path':True,'mathlib_references':refs,
 'draft_status_sha256':M['draft_status_sha256'],'author_report_sha256':M['report_sha256'],
 'report_matches_status':True,'original_sha256':status['original_sha256'],'working_sha256':status['working_sha256'],
 'original_review_sha256':hashfile(review),'original_review_bytes':review.stat().st_size,
 'previous_reviews_preserved_before_append':True,'new_integration_inspected':False,
 'author_scripts_executed':False,'necessary_DEV_analysis_remaining':False}
put(RUN/'verification_dev.json',json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps({k:v for k,v in result.items() if k not in ['sources','records','printed_types','mathlib_references','lean_path']},ensure_ascii=False,indent=2))
