"""Reconcile the three DEV modules, all 16 printed types, own builds and source/log pins."""
from pathlib import Path
import datetime,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_tomita_polar_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes())
M=load(RUN/'manifest.json');C=load(RUN/'compilation.json');STATUS=load(RUN/'tomita_polar_draft_status.json')
assert all(v for k,v in C.items() if isinstance(v,bool))
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    q=p.with_name(p.name+'.tmp_'+stamp)
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
for n,k in [('tomita_polar_draft_status.json','draft_status_sha256'),('RELATORIO_FATOR_POLAR_TOMITA_DEV.md','report_sha256'),
 ('tomita_root_custody.json','custody_sha256'),('tomita_root_custody_verification.json','custody_verification_sha256')]:
    assert hf(ROOT/n)==hf(RUN/n)==M[k]
assert hf(ROOT/'RELATORIO_FATOR_POLAR_TOMITA_DEV.md')==STATUS['report_sha256']
assert hf(ROOT/'tomita_root_custody.json')==STATUS['parent_custody_sha256']
assert hf(ROOT/'tomita_root_domain_draft_status.json')==STATUS['domain_manifest_sha256']
assert hf(REV/'REVIEW_SCALAR_TOMITA_DOMAIN.md')==STATUS['domain_review_sha256']
audit=C['records'][-1];out=Path(audit['stdout']).read_text(encoding='utf-8')
blocks=re.findall(r"^(TGLV350\.Regular\.\w+.*?)(?=^'TGLV350\.Regular\.)",out,re.M|re.S)
types={re.match(r'TGLV350\.Regular\.\w+',b)[0]:' '.join(b.split()) for b in blocks}
assert len(types)==len(blocks)==16 and set(types)==set(M['declarations'])==set(STATUS['targets'])
source_checks={};graph={};allowed={'propext','Classical.choice','Quot.sound'}
for r in C['records']:
    assert r['returncode']==0 and r['axioms_allowed']
    assert hf(r['command'][-1])==r['source_sha256'] and hf(r['command'][2])==r['output_sha256']
    for k in ['stdout','stderr']:assert hf(r[k])==r[k+'_sha256']
    assert Path(r['stderr']).read_bytes()==b''
    assert not re.search(r'error(?:\([^)]*\))?:|sorryAx|trustCompiler',Path(r['stdout']).read_text(encoding='utf-8'))
    assert all(set(a)==allowed for a in r['axioms'].values())
local_instances={}
for rel,s in M['sources'].items():
    raw=Path(s['path']).read_bytes();assert hf(s['snapshot'])==sha(raw)==s['sha256']
    r=next(r for r in C['records'] if r['module']==rel)
    binary=ROOT/'build'/Path(rel).with_suffix('.olean')
    assert binary.read_bytes()==Path(r['command'][2]).read_bytes()
    assert hf(binary)==s['author_binary_sha256']==r['output_sha256']
    assert hf(s['author_log'])==s['author_log_sha256']
    assert r['axioms']==s['author_axioms'] and all(audit['axioms'][n]==a for n,a in r['axioms'].items())
    assert all(set(a)==set(STATUS['targets'][n]) for n,a in r['axioms'].items())
    txt=raw.decode();stripped=re.sub(r'/\-.*?\-/', '',txt,flags=re.S);stripped=re.sub(r'--[^\n]*','',stripped)
    assert not re.search(r'\b(?:axiom|sorry|admit|unsafe)\b|\[(?:irreducible|reducible)\]|transparency',stripped)
    opts=re.findall(r'^set_option.*$',txt,re.M)
    assert all(v in ['set_option autoImplicit false','set_option linter.unusedSectionVars false','set_option maxHeartbeats 1000000'] for v in opts)
    inst=re.findall(r'^local instance (\w+).*?:=\s*(.*)',txt,re.M)
    if inst:
        assert all(v=='InnerProductSpace.complexToReal' for _,v in inst)
        local_instances[rel]=[n for n,v in inst]
    source_checks[rel]={'declaration_lines':{a[1]:i for i,l in enumerate(txt.splitlines(),1) if (a:=re.match(r'^(?:def|theorem)\s+(\w+)',l))},
      'no_forbidden_declarations':True,'options':opts,'local_instances':inst,'unprinted_helpers':s['unprinted_helpers'],
      'own_binary_sha256':r['output_sha256'],'source_sha256':s['sha256'],'targets':len(r['axioms'])}
    assert not s['unprinted_helpers']
    graph[rel[:-5].replace('/','.')]=s['imports']
assert not local_instances
for n,d in M['dependencies'].items():
    assert hf(d['frozen_source'])==d['source_sha256'] and hf(d['frozen_binary'])==d['sha256']
    assert hf(d['source'])==d['source_sha256'] and hf(d['binary'])==d['sha256']
    graph[n]=d['imports']
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
    assert hf(h['log'])==h['log_sha256'];log=load(h['log'])
    for k in ['stdout','stderr']:assert hf(log[k])==h[k+'_sha256']
    out=Path(log['stdout']).read_text(encoding='utf-8')
    attempts.append({**h,'sorryAx_in_stream':'sorryAx' in out,'excluded_from_accepted_evidence':not h['accepted_final']})
    if h['accepted_final']:assert h['returncode']==0 and 'sorryAx' not in out
for n,pin in STATUS['modules'].items():
    assert {h['log'] for h in history if h['module']==n and h['returncode']!=0}==set(pin['failed_attempts'])
assert len(history)==5 and sum(h['returncode']==0 for h in history)==3 and sum(h['accepted_final'] for h in history)==3
custody=load(ROOT/'tomita_root_custody.json');cfg=load(ROOT/'environment.json')
original=hf(cfg['original_source']);working=hf(ROOT/'um.py')
assert original==custody['original_sha256'] and working==custody['working_sha256']==M['initial_um_sha256']
assert all(hf(p)==h for p,h in M['previous_reviews'].items())
assert all(hf(p)==h for p,h in custody['review_sha256'].items())
assert hf(cfg['lean'])==M['compiler_sha256']
lp=M['lean_path'].split(';');assert len(lp)==9 and lp[0]==str(RUN/'build') and all('\\.lake\\packages\\' in p for p in lp[1:])
# No declaration in this DEV package was present in the still-current integrated Audit.
E=load(ROOT/'kernel_incremental_evidence.json');assert not(set(M['declarations']) & set(E['axiom_report']))
# Read-only source pins for the two Mathlib APIs inspected in this review.
package_base=next(Path(p).parents[3] for p in lp[1:] if '\\mathlib\\' in p)
mathlib_pins={}
for rel in ['Mathlib/Analysis/Normed/Operator/Extend.lean','Mathlib/Analysis/InnerProductSpace/LinearPMap.lean']:
    p=package_base/rel
    mathlib_pins[str(p)]={'sha256':hf(p),'bytes':p.stat().st_size}
result={'timestamp':datetime.datetime.now().astimezone().isoformat(),'status':'THREE_DEV_MODULES_16_TARGETS_VERIFIED',
 'sources':source_checks,'printed_types':types,'all_16_types_printed':True,'all_axioms_trio':True,
 'all_3_own_binaries_byte_equal_author':True,'all_log_stream_pins_preserved':True,'history_attempts':len(history),
 'history_rc0':3,'accepted_final_rc0':3,'superseded_rc0':0,'history_rc1':2,'attempts':attempts,
 'project_import_graph_modules':len(graph),'acyclic':True,'no_old_dependency_imports_new_modules':True,
 'dependencies_count':len(M['dependencies']),'own_dependency_origins_preserved':True,'no_author_project_build_in_LEAN_PATH':True,
 'real_local_instances':local_instances,'original_sha256':original,'working_sha256':working,'previous_reviews_preserved':True,
 'custody_sha256':M['custody_sha256'],'custody_verification_sha256':M['custody_verification_sha256'],
 'draft_status_sha256':M['draft_status_sha256'],'report_sha256':M['report_sha256'],
 'Mathlib_API_source_pins':mathlib_pins,'new_targets_absent_from_current_integrated_Audit':True,'new_integration_inspected':False,'author_programs_executed':False}
write(RUN/'verification_dev.json',json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps({k:v for k,v in result.items() if k not in ['sources','printed_types','attempts']},ensure_ascii=False,indent=2))
