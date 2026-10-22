"""Reverse reviewed topic changes and verify the full original parent recursively."""
from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,msg):
    if not v:raise ValueError(msg)
def verify_topics(path):
    from verify_reviewed_draft import verify
    path=Path(path);raw=path.read_bytes();d=json.loads(path.with_suffix('.json').read_bytes())
    need(sha(raw)==d['sha256'],'Draft drift')
    parent=Path(d['parent_path']);need(parent.parent==W and parent!=path,'Unexpected parent')
    need(not json.loads(parent.with_suffix('.json').read_bytes()).get('topic_compaction_v4'),'Nested topics unsupported')
    verify(parent);parent_raw=parent.read_bytes();need(sha(parent_raw)==d['parent_sha256'],'Parent drift')
    review_path=Path(d['review_path']);need(review_path.parent==W/'adversarial_memory_review','Unexpected review')
    review_raw=review_path.read_bytes();need(sha(review_raw)==d['review_sha256'],'Review drift')
    review=json.loads(review_raw)
    need(review['status']=='APPROVED_DOCUMENTARY_FIDELITY_ONLY' and review['parent_sha256']==sha(parent_raw),'Review mismatch')
    approved={r['topic']:r for r in review['topics']}
    need(len(d['changes'])==len(approved) and {r['topic'] for r in d['changes']}==set(approved),'Topic set mismatch')
    reversed_bytes=raw
    for row in d['changes']:
        topic=row['topic'];a=approved[topic];old=row['before'].encode();new=row['after'].encode()
        need(sha(old)==a['original_sha256'] and sha(new)==a['capsule_sha256'],'Changed review content')
        capsule=Path(row['capsule_path']);need(capsule.parent==W/'topic_capsules_v4','Unexpected capsule')
        need(capsule.read_bytes()==new,'Capsule drift')
        need(reversed_bytes.count(new)==1,'Ambiguous capsule occurrence')
        reversed_bytes=reversed_bytes.replace(new,old,1)
    need(reversed_bytes==parent_raw,'Undeclared change outside reviewed topics')
    need(parent.read_bytes()==parent_raw and path.read_bytes()==raw,'Concurrent change')
    return {'status':'TOPIC_V4_INTEGRATION_VERIFIED_NOT_DEPLOYED','draft_sha256':sha(raw),
            'parent_sha256':sha(parent_raw),'topics':sorted(approved),'all_other_parent_bytes_preserved':True,
            'scope':'Byte fidelity and approved topic identity, not proof or API fit.'}
