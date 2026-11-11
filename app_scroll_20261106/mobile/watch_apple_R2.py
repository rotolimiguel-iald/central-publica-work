"""Observe only the Xcode Cloud archive triggered by this verified commit."""
import json,subprocess,time
from pathlib import Path
from urllib.parse import urlsplit
from datetime import datetime,timezone
D=Path(__file__).parent/'release'
p=json.loads((D/'PUSH.json').read_bytes());assert p['status']=='PUSHED_VERIFIED'
for attempt in range(22):
 r=subprocess.run(['gh','api','repos/rotolimiguel-iald/iald-app/commits/'+p['commit']+'/check-runs'],capture_output=True,check=True,timeout=30)
 matches=[c for c in json.loads(r.stdout)['check_runs'] if c['head_sha']==p['commit'] and c['name']=='IALD | IALD | Archive - iOS' and urlsplit(c['details_url']).hostname=='appstoreconnect.apple.com']
 if not matches:
  if attempt<3:time.sleep(35);continue
  raise RuntimeError('No matching archive check; no build was started manually')
 assert len(matches)==1,'Ambiguous archive; stop'
 c=matches[0];done=c['status']=='completed'
 target=D/('IOS_ARCHIVE_FINAL.json' if done else 'IOS_ARCHIVE_STARTED.json')
 receipt={k:c[k] for k in ['id','name','status','conclusion','details_url','head_sha','started_at','completed_at']}
 receipt.update(observed_at=datetime.now(timezone.utc).isoformat(),source='GitHub check reported by Xcode Cloud',groups_verified=False)
 if not target.exists():
  with target.open('x',encoding='utf8') as f:json.dump(receipt,f,indent=2)
  print(json.dumps(receipt),flush=True)
 else:
  previous=json.loads(target.read_bytes())
  assert all(previous[k]==c[k] for k in ['head_sha','details_url','started_at','name']), 'Archive identity changed'
  if previous['id']!=c['id']:
   changed=D/('IOS_CHECK_'+str(c['id'])+'.json')
   if not changed.exists():
    with changed.open('x',encoding='utf8') as f:json.dump(receipt,f,indent=2)
 if done:break
 time.sleep(35)
else:print('Archive still running; same identity preserved')
