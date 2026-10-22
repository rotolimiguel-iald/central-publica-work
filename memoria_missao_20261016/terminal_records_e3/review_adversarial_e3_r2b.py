from pathlib import Path
import copy,hashlib,importlib.util,json,sys,datetime
BASE=Path(__file__).resolve().parent
ROOT=BASE/'independent_review_r2b';ROOT.mkdir(exist_ok=False)
sys.path.insert(0,r'C:\IALD\MEMORIA_IALD\lib')
src=BASE/'mission_candidate_r2.py';raw=src.read_bytes();snap=ROOT/'mission_snapshot.py';snap.write_bytes(raw)
spec=importlib.util.spec_from_file_location('iald_memory.e3_independent_snapshot',snap);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
trackpath=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\mission_resume_20261016\track_build_r45.py')
sys.path.insert(0,str(trackpath.parent));spec=importlib.util.spec_from_file_location('e3_tracker_review',trackpath);tr=importlib.util.module_from_spec(spec);spec.loader.exec_module(tr)
STAMP='20261016T170000_123456Z';fixture=ROOT/STAMP;fixture.mkdir()
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def fixture_pair(status='completed',receipt_raw=None,terminal_pin=True):
 p=fixture/('START_RECEIPT.json'if status=='running'else'RECEIPT.json');p.write_bytes(receipt_raw if receipt_raw is not None else (b'{"pid":123}' if status=='running' else b'{"exit_code":0}'));pinned=pin(p)
 h=dict(id='build-'+STAMP,kind='lean_build',task_id='R7',status='completed',no_repeat=True)
 h['start_receipt'if status=='running'else'receipt']=pinned
 if status=='running'and terminal_pin:
  term=fixture/'RECEIPT.json';term.write_bytes(b'{"exit_code":0}');h['receipt']=pin(term)
 r=dict(id='track-build-'+STAMP+'-'+status,kind='fact',statute='REAL',text=f'R7 sandbox build {STAMP} {status}. Full requirement remains open.',sources=[dict(kind='artifact',ref=str(p),sha256=pinned['sha256'])])
 return r,h
results=[]
def test(name,expect_visible,mutate=lambda r,h:None,**kw):
 r,h=fixture_pair(**kw);mutate(r,h);before=copy.deepcopy((r,h));v,i=m._legacy_terminal_build_records([r],[h],{'R7':{}})
 results.append(dict(name=name,expected_visible=expect_visible,visible=len(v),indexed=len(i),passed=(bool(v)==expect_visible),inputs_unchanged=(r,h)==before))
test('valid_exact_record',False)
test('valid_running_history',False,status='running')
for name,raw in [('array',b'[]'),('duplicate_exit',b'{"exit_code":0,"exit_code":0}'),('nan',b'{"exit_code":0,"x":NaN}'),('bool_exit',b'{"exit_code":false}'),('float_exit',b'{"exit_code":0.0}'),('null_exit',b'{"exit_code":null}'),('missing_exit',b'{}'),('deep_json',b'['*2000+b']'*2000)]:
 test('receipt_'+name,True,receipt_raw=raw)
for name,raw in [('zero_pid',b'{"pid":0}'),('missing_pid',b'{}'),('terminal_start',b'{"pid":1,"exit_code":0}')]:
 test('start_'+name,True,status='running',receipt_raw=raw)
test('no_repeat_not_bool',True,lambda r,h:h.update(no_repeat=1))
test('record_with_newline',True,lambda r,h:r.update(text=r['text']+'\n'))
test('record_statute_declared',True,lambda r,h:r.update(statute='DECLARADO'))
test('receipt_pin_extra',True,lambda r,h:h['receipt'].update(note='extra'))

test('invalid_json_receipt_with_valid_hash',True,receipt_raw=b'not a JSON receipt')
test('receipt_exit_one_vs_completed_handle',True,receipt_raw=b'{"exit_code":1}')
test('running_record_no_terminal_receipt',True,status='running',terminal_pin=False)
test('extra_scientific_record_field',True,lambda r,h:r.update(science='trace proved'))
test('scientific_text_suffix',True,lambda r,h:r.update(text=r['text']+' trace proved'))
test('decision_kind',True,lambda r,h:r.update(kind='decision'))
test('erratum_kind',True,lambda r,h:r.update(kind='correction'))
test('active_handle',True,lambda r,h:h.update(status='running'))
test('conflicting_phase',True,lambda r,h:h.update(phase='running'))
test('wrong_task',True,lambda r,h:h.update(task_id='R8'))
test('wrong_hash',True,lambda r,h:r['sources'][0].update(sha256='0'*64))
test('extra_source_field',True,lambda r,h:r['sources'][0].update(extra='scientific'))
r,h=fixture_pair();v,i=m._legacy_terminal_build_records([r,copy.deepcopy(r)],[h],{'R7':{}});results.append(dict(name='duplicate_record_id',passed=len(v)==2 and not i))
r,h=fixture_pair();v,i=m._legacy_terminal_build_records([r],[h,copy.deepcopy(h)],{'R7':{}});results.append(dict(name='duplicate_handle_id',passed=len(v)==1 and not i))
tracker=[]
for state in ['done','cancelled','closed','accepted','returned','consumed','uncertain','unknown',None]:
 old=[dict(id='build-'+STAMP,kind='lean_build',task_id='R7',status=state,no_repeat=True)]
 try:
  new=tr.update_handles(old,STAMP,'R7','running',{'path':'fixture','sha256':'a'*64})
  tracker.append(dict(name='reopen_'+str(state),passed=False,observed_status=new[0]['status']))
 except ValueError:tracker.append(dict(name='reopen_'+str(state),passed=True))
old=[dict(id='build-'+STAMP,kind='lean_build',task_id='R7',status='running',phase='running',no_repeat=True)]
try:
 new=tr.update_handles(old,STAMP,'R7','completed',{'path':'fixture','sha256':'a'*64});tracker.append(dict(name='phase_transition_consistency',passed=new[0].get('phase')==new[0]['status'],observed=new[0]))
except ValueError:tracker.append(dict(name='phase_transition_consistency',passed=True))
result=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=pin(snap),candidate_original=str(src),tracker=pin(trackpath),classifier_results=results,tracker_results=tracker,real_state_calls=0,provider_calls=0)
result['ok']=all(x['passed'] and x.get('inputs_unchanged',True) for x in results+tracker)
out=ROOT/'RESULTS.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'output':str(out),'candidate_sha256':result['candidate']['sha256'],'classifier_failed':[x['name']for x in results if not x['passed']],'tracker_failed':[x['name']for x in tracker if not x['passed']],'source_inputs_unchanged':all(x.get('inputs_unchanged',True)for x in results)},ensure_ascii=False))
