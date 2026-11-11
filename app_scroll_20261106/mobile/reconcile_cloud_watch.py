"""Preserve the initial check; Apple recreated the check ID for the same action."""
import json
from pathlib import Path
from prepare_mobile import put,report,sha,HERE
original=HERE/'watch_apple.py'
s=original.read_text()
old="else:assert json.loads(target.read_bytes())['id']==c['id']"
new="""else:
  previous=json.loads(target.read_bytes())
  assert all(previous[k]==c[k] for k in ['head_sha','details_url','started_at','name']), 'Archive identity changed'
  if previous['id']!=c['id']:
   changed=D/('IOS_CHECK_'+str(c['id'])+'.json')
   if not changed.exists():
    with changed.open('x',encoding='utf8') as f:json.dump(receipt,f,indent=2)"""
assert s.count(old)==1
put(HERE/'watch_apple_R2.py',s.replace(old,new).encode())
report(HERE/'CLOUD_CHECK_RECONCILIATION.json',{'status':'SAME_ARCHIVE_ACTION_CHECK_ID_RECREATED','initial_check':127894921988,'observed_check':127895265761,'identity_fields':['head_sha','details_url','started_at','name'],'new_build_started':False,'initial_receipt_preserved':True,'watcher_sha256':sha((HERE/'watch_apple_R2.py').read_bytes())})
