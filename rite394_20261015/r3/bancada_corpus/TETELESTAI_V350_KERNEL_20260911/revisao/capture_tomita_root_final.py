"""Read-only final integration inspection. No author code or Lean is executed."""
from pathlib import Path
import ast,datetime,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_tomita_root_latest_run.txt').read_text().strip())
SQUARE=Path((REV/'tomita_square_latest_run.txt').read_text().strip())
OLD=max(p for p in SQUARE.glob('integrated_*') if (p/'verification.json').exists())
STATIC=max(p for p in RUN.glob('static_integrated_*') if (p/'verification_static.json').exists())
DEST=RUN/('final_integrated_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes());load=lambda p:json.loads(Path(p).read_bytes())
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
def save(p,v):write(p,json.dumps(v,ensure_ascii=False,indent=2).encode('utf-8'))
def axioms(text):
    d={}
    for n,a in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",text,re.S):
        aa=[v.strip() for v in a.split(',') if v.strip()]
        assert n not in d or d[n]==aa
        d[n]=aa
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",text):
        assert n not in d or not d[n]
        d[n]=[]
    return d
V=load(STATIC/'verification_static.json');C=load(RUN/'compilation.json');M=load(RUN/'manifest.json');CL=load(RUN/'closure_dev.json')
previous=load(ROOT/'tomita_square_custody.json');OLDV=load(OLD/'verification.json')
assert OLDV['working_sha256']==previous['working_sha256']
for f in ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json','gate_extension.py','integrate_v350.py','compile_integrated.py','test_gate_extension.py']:
    assert hf(OLD/f)==previous['artifacts'][f],f
for f,h in V['artifacts'].items():assert hf(ROOT/f)==h,f
files=['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json',
 'gate_extension.py','integrate_v350.py','compile_integrated.py','compile_lean.py','test_gate_extension.py',
 'record_tomita_root_progress.py','verify_tomita_root_custody.py','tomita_root_draft_status.json',
 'RELATORIO_RAIZ_TOMITA_DEV.md','graph_core_draft_status.json','RELATORIO_DOMINIO_GRAFICO_DEV.md']
for f in files:write(DEST/f,(ROOT/f).read_bytes())
for f in files:
    if f.endswith('.py'):ast.parse((DEST/f).read_bytes())
B=load(DEST/'integrated_compile.json');I=load(DEST/'integration.json');G=load(DEST/'gate_tests.json');E=load(DEST/'kernel_incremental_evidence.json')
assert B['incremental_build_ok'] and not B['full_monolithic_runtime_run']
assert hf(ROOT/'um.py')==I['working_sha256']==G['working_um_sha256']==V['working_source_sha256']
assert I['embedded_files']==V['embedded_source_files']==832
assert C['complete'] and C['all_exit_zero'] and C['exact_30_targets'] and C['dependencies_preserved']
ownax=C['records'][-1]['axioms'];assert len(ownax)==30
draft=load(DEST/'tomita_root_draft_status.json');assert {n:sorted(a) for n,a in ownax.items()}==draft['targets']
newkeys={'TGLExt/V350'+n+'.lean' for n in draft['modules']}
oldrows={r['file']:r for r in OLDV['records']};rows=[];permodule={}
for r in B['records']:
    src=Path(r['source']);rel=src.relative_to(ROOT/'kernel');binary=ROOT/'build'/rel.with_suffix('.olean')
    raw=src.read_bytes();br=binary.read_bytes()
    assert r['returncode']==0 and sha(raw)==r['sha256'] and sha(br)==r['output_sha256']
    o=oldrows.get(rel.as_posix())
    row={'file':rel.as_posix(),'source_sha256':sha(raw),'binary_sha256':sha(br),'returncode':0,'timestamp':r['timestamp'],
      'same_source_binary_as_previous':bool(o and sha(raw)==o['source_sha256'] and sha(br)==o['binary_sha256']),
      'source_unchanged_during_compile':r.get('source_unchanged_during_compile')}
    write(DEST/'sources'/rel,raw)
    for k in ['stdout','stderr']:
        lp=Path(r[k]);lb=lp.read_bytes();write(DEST/'logs'/lp.name,lb);row[k+'_sha256']=sha(lb)
    lp=Path(r['stdout']).with_name(Path(r['stdout']).name.replace('.stdout.txt','.json'));lb=lp.read_bytes()
    assert json.loads(lb)==r
    write(DEST/'logs'/lp.name,lb);row['log_sha256']=sha(lb);row['log_name']=lp.name
    text=Path(r['stdout']).read_text(encoding='utf-8')
    row['warnings']=[l for l in text.splitlines() if 'warning:' in l]
    assert not any('error:' in l for l in text.splitlines())
    rows.append(row)
    if rel.as_posix() in newkeys:
        expected={n:ownax[n] for n in ownax if n.rsplit('.',1)[1] in re.findall(r'^#print axioms ([\w.]+)$',raw.decode(),re.M)}
        ax=axioms(text);assert ax==expected
        permodule[rel.as_posix()]=ax
assert len(rows)==130 and {r['file'] for r in rows}==set(I['added_kernel_files']+I['updated_kernel_files'])
newfiles=newkeys|{'TGLExt.lean','TGL/Audit.lean'}
newrows=[r for r in rows if r['file'] in newfiles]
assert len(newrows)==7 and all(r['source_unchanged_during_compile'] is True for r in newrows)
assert sum(r['same_source_binary_as_previous'] for r in rows)==123
assert sum(map(len,permodule.values()))==30
ar=next(r for r in rows if r['file']=='TGL/Audit.lean')
ax=axioms((DEST/'logs'/ar['log_name'].replace('.json','.stdout.txt')).read_text(encoding='utf-8'))
assert len(ax)==G['axiom_report_entries']==6539 and ax==E['axiom_report']
assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in ax.values())
assert all(ax[n]==a for n,a in ownax.items())
oldax=load(OLD/'axioms.json')
assert set(ax)-set(oldax)==set(ownax) and all(ax[n]==a for n,a in oldax.items())
checks={c['name']:c['passed'] for c in G['checks']};og=load(OLD/'gate_tests.json');oldchecks={c['name']:c['passed'] for c in og['checks']}
assert G['passed']==len(G['checks'])==len(checks)==78 and all(checks.values())
assert all(checks.get(n)==v for n,v in oldchecks.items())
addedchecks=sorted(set(checks)-set(oldchecks))
assert addedchecks==['bounded_Tomita_resolvent_and_exact_positive_root_does_not_discharge_KMS_trace_or_physical_frontier']
assert not G['frontier']['legacy_gate_changed'] and not G['frontier']['full_plan_complete'] and not G['full_monolithic_runtime_run']
assert G['legacy_gate']==og['legacy_gate']
flags={k:E[k] for k in previous['remaining_flags']};assert len(flags)==6 and all(v is False for v in flags.values())
assert E['incremental_build_ok'] and not E['full_monolithic_runtime_run']
assert not any((ROOT/n).exists() for n in ['tomita_root_custody.json','tomita_root_custody_verification.json','RELATORIO_RAIZ_TOMITA_INTEGRADA.md'])
for p,h in M['previous_reviews'].items():assert hf(p)==h
assert hf(CL['review_path'])==CL['review_sha256']
for rel,s in M['sources'].items():assert hf(s['path'])==s['sha256']
cfg=load(ROOT/'environment.json');oh=hf(cfg['original_source'])
assert oh==hf(ROOT/'fontes/um_v350_original.py')==I['base_sha256']==previous['original_sha256']
for p,r in V['documentary_custody_34_exact_pairs'].items():
    assert hf(p)==r['source_sha256']
later_status=load(DEST/'graph_core_draft_status.json')
# Only status metadata/segregation: no source, binary, proof or DEV log of later modules is read.
later_modules=list(later_status['modules'])
assert len(later_modules)==2 and len(later_status['targets'])==10
assert not any('TGLExt/V350'+n+'.lean' in set(I['added_kernel_files']) for n in later_modules)
assert not(set(later_status['targets']) & set(ax))
rec=(DEST/'record_tomita_root_progress.py').read_text(encoding='utf-8')
assert all(n in rec for n in ['graph_core_draft_status.json','RELATORIO_DOMINIO_GRAFICO_DEV.md','sem revisão/integração','Não entra nos 30 alvos'])
legacy={k:{'stored':E[k],'same_as_parent':E[k]==load(OLD/'kernel_incremental_evidence.json')[k],
  'equals_final_Audit_stdout':E[k]==ar['stdout_sha256']} for k in ['audit_stdout_sha256','audit_capture_sha256_full']}
data={'timestamp':datetime.datetime.now().astimezone().isoformat(),'path':str(DEST),
 'mode':'INDEPENDENT_STATIC_TRANSPOSE_AST_AND_AUTHOR_LOG_PIN_INSPECTION__NO_NEW_LEAN_EXECUTIONS',
 'working_sha256':I['working_sha256'],'original_sha256':oh,'parent_working_sha256':previous['working_sha256'],
 'embedded_files':832,'static_verification_path':str(STATIC/'verification_static.json'),'static_verification_sha256':hf(STATIC/'verification_static.json'),
 'transposition':V['transposition'],'records':rows,'new_records':newrows,'all_source_binary_log_pins_match':True,
 'integrated_records':130,'reused_identical_source_binary_records':123,'new_author_compilations':7,
 'audit_distinct':6539,'audit_all_axioms_allowed':True,'audit_30_equal_own_DEV':True,'old_audit_targets_preserved':True,
 'final_Audit_stdout_sha256':ar['stdout_sha256'],'inherited_Audit_summary_hash_fields':legacy,
 'gate_controls':78,'gate_passed':G['passed'],'added_controls':addedchecks,'old_controls_AST_preserved':True,
 'six_flags':flags,'legacy_gate_changed':False,'full_plan_complete':False,'full_runtime':False,
 'recorder_and_verifier_syntax_valid':True,'recorder_surface_count':34,'new_custody_report_and_verification_absent':True,
 'later_DEV_note_segregated':True,'later_DEV_sources_or_logs_inspected':False,'later_DEV_proofs_certified':False,
 'findings':V['findings'],'own_DEV_closure':CL,'previous_reviews_preserved':True,
 'artifacts':{f:hf(DEST/f) for f in files},'source_bin_PIN_scope':'130 integrated records; external packages and remaining base inherited',
 'author_programs_executed_by_reviewer':False,'Lean_executions_this_review':0}
save(DEST/'verification.json',data);save(DEST/'axioms.json',ax);save(DEST/'module_axioms.json',permodule)
print(json.dumps({k:v for k,v in data.items() if k not in ['transposition','records','own_DEV_closure','artifacts','new_records']},ensure_ascii=False,indent=2))
