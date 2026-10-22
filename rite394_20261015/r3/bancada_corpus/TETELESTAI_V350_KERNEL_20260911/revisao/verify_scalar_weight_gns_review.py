"""Read-only reconciliation of nine independent DEV builds and 60 types/axioms."""
from pathlib import Path
import ast, datetime, hashlib, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
RUN=Path((REV/'scalar_weight_gns_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
M=load(RUN/'manifest.json'); C=load(RUN/'compilation.json')
D=load(RUN/'scalar_weight_gns_draft_status.json')
assert all(v for k,v in C.items() if isinstance(v,bool))
for n,k in [('scalar_weight_gns_draft_status.json','draft_status_sha256'),
 ('RELATORIO_GNS_PESO_COMPLETO_DEV.md','report_sha256'),
 ('tomita_involution_custody.json','custody_sha256'),
 ('tomita_involution_custody_verification.json','custody_verification_sha256')]:
    assert hf(ROOT/n)==hf(RUN/n)==M[k]
assert D['parent_custody_sha256']==M['custody_sha256'] and D['report_sha256']==M['report_sha256']
audit=C['records'][-1]; audittext=Path(audit['stdout']).read_text(encoding='utf-8')
blocks=re.findall(r"^(TGLV350\.Regular\..*?)(?=^'TGLV350\.Regular\.)",audittext,re.M|re.S)
types={re.match(r'TGLV350\.Regular\.[\w.]+',b)[0].rstrip('.'):' '.join(b.split()) for b in blocks}
assert len(types)==len(blocks)==60 and set(types)==set(M['declarations'])==set(D['targets'])
allowed={'propext','Classical.choice','Quot.sound'}
for r in C['records']:
    assert r['returncode']==0 and r['axioms_allowed']
    assert hf(r['command'][-1])==r['source_sha256'] and hf(r['command'][2])==r['output_sha256']
    for k in ['stdout','stderr']:assert hf(r[k])==r[k+'_sha256']
    assert not Path(r['stderr']).read_bytes()
    assert not re.search(r'error(?:\([^)]*\))?:|sorryAx|trustCompiler',Path(r['stdout']).read_text(encoding='utf-8'))
    assert all(set(a)==allowed for a in r['axioms'].values())
checks={};graph={};warnings=[]
for rel,s in M['sources'].items():
    r=next(r for r in C['records'] if r['module']==rel)
    raw=Path(s['path']).read_bytes()
    assert hf(s['snapshot'])==hf(s['path'])==s['sha256']
    binary=ROOT/'build'/Path(rel).with_suffix('.olean')
    assert binary.read_bytes()==Path(r['command'][2]).read_bytes()
    assert hf(binary)==s['author_binary_sha256']==r['output_sha256']
    assert hf(s['author_log'])==s['author_log_sha256']
    author=load(s['author_log'])
    assert author['returncode']==author['lean_returncode']==0 and author['source_unchanged_during_compile']
    pin=D['modules'][Path(rel).stem]
    assert hf(author['stdout'])==pin['stdout_sha256']
    assert r['axioms']==s['author_axioms']
    assert all(audit['axioms'][n]==a and set(a)==set(D['targets'][n]) for n,a in r['axioms'].items())
    txt=raw.decode('utf-8'); stripped=re.sub(r'/\-.*?\-/','',txt,flags=re.S);stripped=re.sub(r'--[^\n]*','',stripped)
    assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]|transparency',stripped)
    opts=re.findall(r'^set_option.*$',txt,re.M)
    assert opts==['set_option autoImplicit false','set_option linter.unusedSectionVars false','set_option maxHeartbeats 1000000']
    assert not re.findall(r'^(?:local )?instance\b',txt,re.M) and not s['unprinted_helpers']
    checks[rel]={'source_sha256':s['sha256'],'binary_sha256':r['output_sha256'],'targets':len(r['axioms']),
     'declaration_lines':{a[1]:i for i,l in enumerate(txt.splitlines(),1) if (a:=re.match(r'^(?:def|theorem)\s+([\w.]+)',l))},
     'options':opts,'no_new_instances':True,'no_unprinted_helpers':True,'no_forbidden_declarations':True}
    warnings += [l for l in Path(r['stdout']).read_text(encoding='utf-8').splitlines() if 'warning:' in l]
    graph[rel[:-5].replace('/','.')]=s['imports']
for n,d in M['dependencies'].items():
    assert hf(d['frozen_source'])==hf(d['source'])==d['source_sha256']
    assert hf(d['frozen_binary'])==hf(d['binary'])==d['sha256']
    graph[n]=d['imports']
for n,d in M['secondary_catalog'].items():
    for p in ['manifest','compilation']:assert hf(Path(d['run'])/(p+'.json'))==d[p+'_sha256']
visiting=set();done=set()
def visit(n):
    if n not in graph or n in done:return
    assert n not in visiting
    visiting.add(n)
    for d in graph[n]:visit(d)
    visiting.remove(n);done.add(n)
for n in graph:visit(n)
new={rel[:-5].replace('/','.') for rel in M['sources']}
assert all(not(new & set(ds)) for n,ds in graph.items() if n not in new)
history=load(RUN/'author_history.json');attempts=[]
for h in history:
    assert hf(h['log'])==h['log_sha256']; log=load(h['log'])
    for k in ['stdout','stderr']:assert hf(log[k])==h[k+'_sha256']
    out=Path(log['stdout']).read_text(encoding='utf-8')
    attempts.append({**h,'sorryAx_in_stream':'sorryAx' in out,'excluded_from_accepted_evidence':not h['accepted_final']})
    if h['accepted_final']:assert h['returncode']==0 and 'sorryAx' not in out
for n,pin in D['modules'].items():
    assert {h['log'] for h in history if h['module']==n and h['returncode']!=0}==set(pin['failed_attempts'])
assert len(history)==14 and sum(h['accepted_final'] for h in history)==9
assert sum(h['returncode']!=0 for h in history)==4
custody=load(ROOT/'tomita_involution_custody.json');cfg=load(ROOT/'environment.json')
original=hf(cfg['original_source']);working=hf(ROOT/'um.py')
assert original==custody['original_sha256'] and working==custody['working_sha256']==M['initial_um_sha256']
assert all(hf(p)==h for p,h in M['previous_reviews'].items())
assert all(hf(p)==h for p,h in custody['review_sha256'].items())
assert hf(cfg['lean'])==M['compiler_sha256']
lp=M['lean_path'].split(';')
assert len(lp)==9 and lp[0]==str(RUN/'build') and all('\\.lake\\packages\\' in p for p in lp[1:])
E=load(ROOT/'kernel_incremental_evidence.json');G=load(ROOT/'gate_tests.json')
assert not(set(M['declarations']) & set(E['axiom_report']))
flags={n:E[n] for n in custody['remaining_flags']}
assert len(flags)==6 and all(v is False for v in flags.values())
assert G['frontier']['legacy_gate_changed'] is False and G['frontier']['full_plan_complete'] is False
assert G['full_monolithic_runtime_run'] is False
assert hf(ROOT/'gate_extension.py')==custody['artifacts']['gate_extension.py']
lib=next(Path(p).parents[3] for p in lp[1:] if '\\mathlib\\' in p)
api=lib/'Mathlib/MeasureTheory/Integral/DominatedConvergence.lean'
result={'timestamp':datetime.datetime.now().astimezone().isoformat(),'status':'NINE_DEV_MODULES_60_TARGETS_VERIFIED',
 'sources':checks,'printed_types':types,'all_60_types_printed':True,'all_axioms_trio':True,
 'all_9_own_binaries_byte_equal_author':True,'all_log_stream_pins_preserved':True,
 'history_attempts':14,'accepted_final_rc0':9,'superseded_rc0':1,'history_rc1':4,'attempts':attempts,'warnings':warnings,
 'project_import_graph_modules':len(graph),'acyclic':True,'no_old_dependency_imports_new_modules':True,
 'dependencies_count':len(M['dependencies']),'own_dependency_origins_preserved':True,'no_author_project_build_in_LEAN_PATH':True,
 'original_sha256':original,'working_sha256':working,'previous_reviews_preserved':True,
 'custody_sha256':M['custody_sha256'],'custody_verification_sha256':M['custody_verification_sha256'],
 'draft_status_sha256':M['draft_status_sha256'],'report_sha256':M['report_sha256'],
 'Mathlib_API_source_pins':{str(api):hf(api)},'new_targets_absent_from_current_integrated_Audit':True,
 'remaining_flags':flags,'gate_extension_sha256':hf(ROOT/'gate_extension.py'),'legacy_gate_unchanged_in_read_record':True,
 'full_plan_complete_in_read_record':False,'full_runtime_in_read_record':False,
 'new_integration_inspected':False,'author_programs_executed':False}
dest=RUN/'verification_dev.json';assert not dest.exists()
data=json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8');tmp=dest.with_name(dest.name+'.tmp')
with tmp.open('xb') as f:f.write(data)
assert tmp.read_bytes()==data;tmp.replace(dest)
print(json.dumps({k:v for k,v in result.items() if k not in ['sources','printed_types','attempts']},ensure_ascii=False,indent=2))
