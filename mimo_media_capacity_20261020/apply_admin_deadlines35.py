"""Distinct review and scoped CAS of two administrative TestFlight records."""
from pathlib import Path
import hashlib,json,re
from transaction import backup,atomic
from task import W,check
D=W/'admin_deadlines35stage'
plan=json.loads((D/'UPDATE_PLAN_R1.json').read_bytes())
destination=Path(plan['destination']);source=Path(plan['source']['path'])
old=destination.read_bytes();new=source.read_bytes()
sha=lambda raw:hashlib.sha256(raw).hexdigest()
assert sha(old)==plan['baseline_sha256'] and sha(new)==plan['source']['sha256']
assert sha(Path(plan['observation_source']['path']).read_bytes())==plan['observation_source']['sha256']
keys=('testflight_internal','testflight_external')
def mask(raw):
    text=raw.decode('utf-8');ranges=[]
    for key in keys:
        found=list(re.finditer('"'+key+'"\\s*:\\s*',text))
        assert len(found)==1
        start=found[0].end();_,length=json.JSONDecoder().raw_decode(text[start:])
        ranges.append((start,start+length))
    for start,end in sorted(ranges,reverse=True):text=text[:start]+'<TESTFLIGHT>'+text[end:]
    return text.encode('utf-8')
assert mask(old)==mask(new)
parsed=json.loads(new)
for key,number in zip(keys,(1,6)):
    item=parsed['items'][key]
    assert item['build']=='4.1 (35)' and item['status']=='Em testes'
    assert item['expires_at'] is None and item['testers']==number
assert check('deploy')['ready'] is True
review=dict(status='PASS',actor='codex-app-01a094df',producer='Averroes',
 scope='Two administrative TestFlight subtrees only. Other bytes identical; key dates and global checked_at preserved; no inferred exact expiry.',
 baseline_sha256=sha(old),candidate_sha256=sha(new),provider_calls=0)
with (D/'PARENT_REVIEW_R1.json').open('xb') as f:f.write(json.dumps(review,indent=2).encode())
saved=backup(destination)
assert destination.read_bytes()==old
atomic(destination,new)
assert destination.read_bytes()==new
result=dict(status='APPLIED_ADMIN_METADATA_ONLY',destination=str(destination),sha256=sha(new),
 backup=saved,backup_sha256=sha(Path(saved).read_bytes()),other_bytes_preserved=True,
 app_chat_alerts_added=False,restart=False,provider_calls=0)
with (D/'DELIVERY_APPLIED_R1.json').open('xb') as f:f.write(json.dumps(result,indent=2).encode())
print('Two admin-only TestFlight records updated; other bytes preserved')
