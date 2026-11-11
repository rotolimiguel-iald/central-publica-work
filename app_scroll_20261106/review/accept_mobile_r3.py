from pathlib import Path
import json,hashlib,subprocess,datetime
W=Path(r'C:\IALD\Central de Patentes\work\app_scroll_20261106');R=W/'review';A=W/'mobile/release/admin47';actor='codex-scroll-independent-reviewer';ref=str(W/'SESSION_REFERENCE.json')
def pin(p):
 p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def read(p):return json.loads(Path(p).read_bytes())
def verify(p):assert pin(p['path'])['sha256']==p['sha256'],p['path']
def save(p,v):
 with p.open('xb') as f:f.write((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
def call(q):
 p=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],input=json.dumps(q).encode(),capture_output=True)
 d=json.loads(p.stdout)
 if p.returncode or not d.get('ok'):raise RuntimeError(d)
 return d['result']
pr=call({'operation':'project','reference':ref,'max_chars':30000});task=next(t for t in pr['projection']['active'] if t['id']=='mobile');assert task['status']=='review_pending' and task['submitted_by']!=actor
for p in task['evidence']:verify(p)
final=read(W/'FINAL_DELIVERY_R3.json');previous=read(R/'MOBILE_REVIEW_R2.json')
for p in final['sources']:verify(p)
verify(final['previous_progress'])
for p in previous['pins']:verify(p)
plan=read(A/'ADMIN_PLAN.json');review=read(A/'ADMIN_REVIEW.json');receipt=read(A/'TESTFLIGHT47_INTERNAL_DEADLINES.json');staged=read(A/'STAGED_OBJECTS.json')
assert review['status']==receipt['status']=='PASS' and review['reviewer']!=review['author']
assert pin(A/'ADMIN_PLAN.json')['sha256']==review['plan_sha256']==receipt['plan_sha256']
assert pin(A/'ADMIN_REVIEW.json')['sha256']==receipt['review_sha256']
assert pin(A/'update_testflight47_deadlines.py')['sha256']==review['script_sha256']==plan['script_sha256']
assert pin(A/'STAGED_OBJECTS.json')['sha256']==plan['staged_objects_sha256']
assert pin(plan['distribution_receipt'])['sha256']==plan['distribution_sha256']==receipt['distribution_sha256']
target=Path(plan['target']);backup=Path(receipt['backup'])
assert target.parent==backup.parent and pin(target)['sha256']==plan['after_sha256']==receipt['after_sha256']
assert pin(backup)['sha256']==plan['baseline_sha256']==receipt['baseline_sha256']
before=backup.read_bytes();after=target.read_bytes();old=json.loads(before);new=json.loads(after)
keys={'testflight_internal','testflight_external'}
assert set(plan['only_keys'])==keys and set(staged)==keys
assert set(old)==set(new) and set(old['items'])==set(new['items'])
assert {k for k in old['items'] if old['items'][k]!=new['items'][k]}==keys
assert {k:v for k,v in old.items() if k!='items'}=={k:v for k,v in new.items() if k!='items'}
for k in keys:assert new['items'][k]==staged[k] and staged[k]['expires_at'] is None and staged[k]['build']=='4.1 (47)'
# Independently compare exact original text outside the two JSON object value spans.
dec=json.JSONDecoder()
def span(text,start,wanted):
 i=start
 while text[i].isspace():i+=1
 assert text[i]=='{';i+=1
 while True:
  while text[i].isspace() or text[i]==',':i+=1
  if text[i]=='}':raise KeyError(wanted)
  key,end=dec.raw_decode(text,i);i=end
  while text[i].isspace():i+=1
  assert text[i]==':';i+=1
  while text[i].isspace():i+=1
  value,end=dec.raw_decode(text,i)
  if key==wanted:return i,end
  i=end

def mask(raw):
 text=raw.decode('utf-8');items,_=span(text,0,'items');spans=[span(text,items,k) for k in sorted(keys)]
 for a,b in sorted(spans,reverse=True):text=text[:a]+'<REVIEWED_TESTFLIGHT_OBJECT>'+text[b:]
 return text.encode('utf-8')
assert mask(before)==mask(after)
ip=read(W/'INSTALL_PLAN.json');assert str(target) not in {p['path'] for p in ip['preserve']}
for p in ip['preserve']:verify(p)
assert len(ip['preserve'])==1797
assert final['installed_files']==10 and final['preserved_files']==1797
assert 'unverified' in final['availability']['android'].lower() and 'Not inspected'==final['availability']['physical_devices']
report={'status':'PASS','reviewer':actor,'task_id':'mobile','submission_revision':pr['receipt']['revision'],'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'supplements':pin(R/'MOBILE_REVIEW_R2.json'),'checks':{'submission_and_final_delivery_source_pins':True,'prior_mobile_review_96_pins_unchanged':len(previous['pins']),'admin_plan_review_writer_distribution_pins':True,'admin_current_target_and_byte_backup_match_receipts':True,'only_two_existing_testflight_objects_changed':True,'strict_bytes_outside_two_values_identical':True,'checked_at_and_other_entries_unchanged':True,'expiry_remains_unknown':True,'protected_pins_unchanged':1797,'deadline_json_outside_protected_inventory':True},'pins':[pin(W/'FINAL_DELIVERY_R3.json'),pin(W/'MOBILE_SUBMIT_R3.json'),pin(A/'ADMIN_REVIEW.json'),pin(A/'ADMIN_PLAN.json'),pin(A/'STAGED_OBJECTS.json'),pin(A/'TESTFLIGHT47_INTERNAL_DEADLINES.json'),pin(target),pin(backup)],'findings':[],'scope':'Documentary and byte verification supplement. Criterion met: synchronized/published clients and both TestFlight groups reported with evidence scope/remaining limits explicit. R2 Equipe observation provenance retained. Administrative update completes previous pending item. No runtime edits, new tests, browser/API calls, builds or publication by reviewer.','remaining_limits':['Authenticated Android42 download unverified','Physical installation and iPhone/Android scrolling tests unverified','Google Play not published','Exact TestFlight expiration unknown'],'acceptance_basis':'Actual distinct reviewer; accept mobile requirement only after submitted candidate verified. No claim of device validation or new science.'}
save(R/'MOBILE_REVIEW_SUPPLEMENT_R3.json',report)
a=call({'operation':'accept','reference':ref,'task_id':'mobile','actor':{'id':actor,'kind':'agent'},'expected_revision':pr['receipt']['revision'],'projection_sha256':pr['projection_sha256'],'event_id':'scroll-mobile-independent-accept-r3','review_evidence':[pin(R/'MOBILE_REVIEW_R2.json'),pin(R/'MOBILE_REVIEW_SUPPLEMENT_R3.json')],'note':'Independent mobile review and administrative supplement PASS within criterion; APK authenticated download and physical tests remain explicitly unverified.'})
save(R/'MOBILE_FINAL_ACCEPT_R3.json',a)
post=call({'operation':'project','reference':ref,'max_chars':30000})
print(json.dumps({'status':'PASS','revision':a['receipt']['revision'],'tetelestai':post['projection']['tetelestai'],'reviewer':actor,'receipt':str(R/'MOBILE_FINAL_ACCEPT_R3.json')}))
