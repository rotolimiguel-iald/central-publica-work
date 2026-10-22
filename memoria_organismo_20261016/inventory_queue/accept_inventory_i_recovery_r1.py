"""Recover only authorized local I acceptance; preserve initial refusal."""
from pathlib import Path
import hashlib, importlib.util, json
W=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('i_accept_recovery_io',W/'mission_io.py')
io=importlib.util.module_from_spec(spec);spec.loader.exec_module(io)
A={'id':'codex-mission-memory-review','kind':'agent'}
ref=W/'SESSION_REFERENCE.json'
def project(label):
 return io.call('mission_cli.py',{'operation':'project','reference':str(ref),'actor':A,'max_chars':125000},label)
p,before_path=project('inventory_I_accept_recovery_fresh')
t=next(x for x in p['projection']['active']+p['projection']['settled'] if x['id']=='I')
old=json.loads((W/'I_ACCEPT_REQUEST_R1.json').read_bytes())
review=W/'REVIEW_INVENTORY_I_R1.json'
assert old['review_evidence']==[io.pin(review)]
if t['status']=='satisfied':
 assert t['reviewed_by']==A['id'] and t['review_evidence']==old['review_evidence']
 result={'already_applied':True,'receipt':p['receipt']};accept_path=before_path
else:
 assert t['status']=='review_pending' and t['submitted_by']!=A['id']
 request={**old,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256']}
 io.save(W/'I_ACCEPT_REQUEST_RECOVERY_R1.json',request)
 result,accept_path=io.call('mission_cli.py',request,'inventory_I_accept_recovery')
io.save(W/'I_ACCEPT_RECEIPT_RECOVERY_R1.json',{'result':result,'receipt_file':str(accept_path)})
after,after_path=project('inventory_I_accept_recovery_verify')
row=next(x for x in after['projection']['settled'] if x['id']=='I')
assert row['status']=='satisfied' and row['reviewed_by']==A['id']
def rest(v):
 return {x['id']:{k:x[k] for k in ['status','epoch','criterion','depends_on','evidence','review_evidence','lease']}
  for x in v['projection']['active']+v['projection']['settled'] if x['id']!='I'}
assert rest(p)==rest(after)
report={'review':io.pin(review),'accept':io.pin(W/'I_ACCEPT_RECEIPT_RECOVERY_R1.json'),
 'original_refusal':io.pin(W/'receipts'/'20261016T224041_501329Z_inventory_I_accept_own_actor.receipt.json'),
 'before':io.pin(before_path),'after':io.pin(after_path),
 'revision_before':p['receipt']['revision'],'revision_after':after['receipt']['revision'],
 'I_status':row['status'],'reviewer':row['reviewed_by'],'other_requirements_unchanged':True,
 'tetelestai':after['projection']['tetelestai']}
io.save(W/'I_ACCEPT_VERIFIED_R1.json',report)
print(json.dumps(report,ensure_ascii=False,indent=2))
