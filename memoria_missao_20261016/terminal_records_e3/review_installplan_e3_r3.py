"""Read-only installer plan attacks; fixtures only in a new sandbox."""
from pathlib import Path
import copy,hashlib,importlib.util,json,os,sys
BASE=Path(__file__).resolve().parent
RUN=BASE/'independent_installplan_r3';RUN.mkdir(exist_ok=False)
sys.path.insert(0,str(BASE))
spec=importlib.util.spec_from_file_location('independent_e3_installer',BASE/'install_e3_r3.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def pin(p):return {'path':str(Path(p).resolve()),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def write(p,obj):p.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())
for name in ['mission_candidate_r2.py','SOURCE_BASELINE_E3_R2.json','DOC_PLAN_E3_R3.json','verify_live_e3_r2.py','TRACKER_TEST_RESULTS_E3_R3.json']:
 (RUN/name).write_bytes((BASE/name).read_bytes())
write(RUN/'TEST_RESULTS_E3_R2.json',{'ok':True,'candidate':pin(RUN/'mission_candidate_r2.py'),'scope':'Synthetic metadata for independent install-plan tests only.'})
m.BASE=RUN
original_doc=(RUN/'DOC_PLAN_E3_R3.json').read_bytes()
original_validation=(RUN/'TEST_RESULTS_E3_R2.json').read_bytes()
docs=json.loads(original_doc)['files']
paths=[Path(m.__file__),*(RUN/n for n in ['mission_candidate_r2.py','SOURCE_BASELINE_E3_R2.json','DOC_PLAN_E3_R3.json','TEST_RESULTS_E3_R2.json','verify_live_e3_r2.py','TRACKER_TEST_RESULTS_E3_R3.json']),m.OUT/'mission_resume_20261016/track_build_r46.py',*(Path(r['candidate']['path']) for r in docs)]
def review():return {'verdict':'PASS_WITH_SCOPE','reviewed_artifacts':[pin(p) for p in paths]}
results=[]
def outcome(name,ok,call):
 try:
  call()
  assert ok,'unexpected acceptance'
 except AssertionError as e:
  if ok:raise
  assert str(e)!='unexpected acceptance',name
 results.append({'name':name,'passed':True})
r=review();plan=m.reviewed_plan(r);assert len(plan)==4
results.append({'name':'exact reviewed plan accepted read-only','passed':True})
bad=copy.deepcopy(r);bad['reviewed_artifacts'].pop(1)
outcome('missing candidate pair refuses',False,lambda:m.reviewed_plan(bad))
bad=copy.deepcopy(r);bad['reviewed_artifacts'][1]['sha256']='0'*64;bad['notes']=json.dumps(r)
outcome('hash hidden in unrelated text does not authorize',False,lambda:m.reviewed_plan(bad))
bad=copy.deepcopy(r);bad['reviewed_artifacts'].append(copy.deepcopy(bad['reviewed_artifacts'][0]))
outcome('duplicate reviewed path refuses',False,lambda:m.reviewed_plan(bad))
bad=copy.deepcopy(r);bad['verdict']='PASS_NOT_REVIEWED'
outcome('verdict prefix refuses',False,lambda:m.reviewed_plan(bad))
doc=json.loads(original_doc);doc['files'][0]['target']=str(RUN/'wrong-target.md');write(RUN/'DOC_PLAN_E3_R3.json',doc)
outcome('changed plan pin refuses',False,lambda:m.reviewed_plan(r))
outcome('even repinned foreign target refuses allowlist',False,lambda:m.reviewed_plan(review()))
doc=json.loads(original_doc);doc['files'].append(copy.deepcopy(doc['files'][0]));write(RUN/'DOC_PLAN_E3_R3.json',doc)
outcome('four docs instead of three refuses',False,lambda:m.reviewed_plan(review()))
(RUN/'DOC_PLAN_E3_R3.json').write_bytes(original_doc)
val=json.loads(original_validation);val['candidate']['sha256']='0'*64;write(RUN/'TEST_RESULTS_E3_R2.json',val)
outcome('validation must pin the candidate',False,lambda:m.reviewed_plan(review()))
(RUN/'TEST_RESULTS_E3_R2.json').write_bytes(original_validation)
doc=json.loads(original_doc);doc['files'][0]['append_only']=False;write(RUN/'DOC_PLAN_E3_R3.json',doc)
outcome('doc replacement without append-only refuses',False,lambda:m.reviewed_plan(review()))
(RUN/'DOC_PLAN_E3_R3.json').write_bytes(original_doc)
# All actual destinations were read only and retain the original pinned bytes.
assert all(pin(row['target'])['sha256']==row['before']['sha256'] for row in plan)
result={'ok':True,'tests':results,'installer':pin(Path(m.__file__)),'test_script':pin(Path(__file__)),'targets_unchanged':True,'main_invoked':False,'live_preflight_called':False,'production_writes':0,'provider_calls':0,'scope':'reviewed_plan function plus static main byte-backup/atomic replacement review; actual installation remains root action.'}
raw=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode();temp=RUN/'RESULTS.tmp'
with temp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert temp.read_bytes()==raw;os.rename(temp,RUN/'RESULTS.json')
print(json.dumps({'ok':True,'tests':len(results),'result':str(RUN/'RESULTS.json')}))
