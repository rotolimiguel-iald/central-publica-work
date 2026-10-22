from pathlib import Path
import ast, datetime, hashlib, json, os, re
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_vna_final_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
def save(p,d):
    assert p.resolve().is_relative_to(REV)
    raw=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
    if p.exists():
        old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        with bk.open('xb') as f:f.write(old)
        assert bk.read_bytes()==old
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw;os.replace(tmp,p)
def fn(tree,name):return ast.dump(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name),include_attributes=False)
names=['make_scalar_vna_helpers.py','record_scalar_vna_draft.py','prepare_scalar_vna_stage.py','record_scalar_vna_progress.py','verify_scalar_vna_custody.py']
trees={n:ast.parse((ROOT/n).read_bytes()) for n in names}
m=load(RUN/'manifest.json');d=load(ROOT/'scalar_vna_draft_status.json');parent=load(ROOT/'right_vector_custody.json')
assert all(hf(ROOT/n)==m['cumulative_draft_pins'][n] for n in names)
assert d['parent_custody_sha256']==hf(ROOT/'right_vector_custody.json') and d['report_sha256']==hf(d['report_path'])
surfaces={p:{'expected':h,'actual':hf(p)} for p,h in parent['surface_sha256'].items()}
assert len(surfaces)==34 and all(x['expected']==x['actual'] for x in surfaces.values())
rec=(ROOT/'record_scalar_vna_progress.py').read_text(encoding='utf-8')
pre=(ROOT/'prepare_scalar_vna_stage.py').read_text(encoding='utf-8')
ver=(ROOT/'verify_scalar_vna_custody.py').read_text(encoding='utf-8')
assert "len(surfaces) == 34" in rec and "len(modules) == 4 and len(targets) == 27" in rec
assert "'== 598', '== 625'" in pre
assert "raw.startswith(before)" in rec and "backup.open('xb')" in rec and 'temp.replace(path)' in rec
assert "row['output_sha256']" in rec and "row['output_sha256']" in ver
assert "surface.read_bytes().startswith(backup.read_bytes())" in ver
assert "audit_stdout_sha256" in rec and 'historical_v350_audit_metadata' in rec
assert "'SCALAR_VNA_DEV_REVIEW'" in pre and "'SCALAR_VNA_INTEGRATED_REVIEW'" in rec
unchanged={}
for n,f,old in [('prepare_scalar_vna_stage.py','save','prepare_right_vector_stage.py'),('record_scalar_vna_progress.py','write','record_right_vector_progress.py'),('record_scalar_vna_progress.py','body','record_right_vector_progress.py')]:
    unchanged[n+':'+f]=fn(trees[n],f)==fn(ast.parse((ROOT/old).read_bytes()),f)
assert all(unchanged.values())
scripts={n:{'sha256':hf(ROOT/n),'syntax_parse_ok':True,'lines':len((ROOT/n).read_text(encoding='utf-8').splitlines()),'executed_by_reviewer':False} for n in names}
integration=load(ROOT/'integration.json');ev=load(ROOT/'kernel_incremental_evidence.json')
assert hf(ROOT/'um.py')==parent['working_sha256']==d['integrated_working_sha256']
assert hf(ROOT/'gate_extension.py')==parent['artifacts']['gate_extension.py']
assert all(ev[k] is False for k in parent['remaining_flags'])
decl_lines={}
for name in d['modules']:
    src=ROOT/'kernel/TGLV350'/(name+'.lean');s=src.read_text(encoding='utf-8')
    decl_lines[name]={n:i for i,line in enumerate(s.splitlines(),1) if (mm:=re.match(r'(?:private )?(?:theorem|def) ([\w]+)',line)) for n in [mm.group(1)]}
own_partial=Path((REV/'scalar_vna_partial_latest_run.txt').read_text().strip())
history=load(own_partial/'author_history.json')+load(RUN/'author_history.json')
failures=[x for x in history if x['returncode']!=0]
assert len(failures)==4
static={
 'timestamp':datetime.datetime.now().astimezone().isoformat(),'scope':'STATIC_HELPERS_AND_DEV_PINS_ONLY',
 'scripts':scripts,'manifest_sha256':hf(ROOT/'scalar_vna_draft_status.json'),'report_sha256':hf(d['report_path']),
 'parent_custody_sha256':hf(ROOT/'right_vector_custody.json'),'parent_full_reaudit':False,
 'surface_count':len(surfaces),'surfaces_current_match_parent':True,'surface_pins':surfaces,
 'same_audited_byte_backup_functions':unchanged,'planned_modules':4,'planned_targets':27,'batch_transition':[598,625],
 'expected_future_counts_not_measured':{'records':201,'controls':101,'audit':6982,'embedded':903},
 'working_sha256':hf(ROOT/'um.py'),'gate_sha256':hf(ROOT/'gate_extension.py'),'working_and_gate_preserved':True,
 'remaining_flags':{k:ev[k] for k in parent['remaining_flags']},'new_integration_certified':False,
 'prepare_progress_verifier_executed_by_reviewer':False,'new_custody_exists':(ROOT/'scalar_vna_custody.json').exists(),
 'readonly_parent_artifacts':{str(ROOT/n):hf(ROOT/n) for n in ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json']},
 'declaration_lines':decl_lines,'author_failed_attempts_excluded':failures,
 'assessment':{'P0':[],'P1':[],'P2':[],
 'backup_scope':'34 parent surfaces, immediate bytes backup and append-prefix assertions; per-file temp replacement, no runtime certification',
 'stage_scope':'bounded bicommutant lift, separating reducing restriction, actual scalar GNS image equality',
 'math_open':'original F graph-core, inverse J inclusion, KMS, modular-flow identification, trace and flags remain open'}}
save(RUN/'helper_static_inspection.json',static)
print(json.dumps({k:v for k,v in static.items() if k in ['surface_count','surfaces_current_match_parent','working_and_gate_preserved','new_custody_exists','manifest_sha256','report_sha256','assessment']}))
