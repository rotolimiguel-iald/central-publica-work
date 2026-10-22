"""Build a new draft from an explicitly selected reviewed V4 topic batch."""
from pathlib import Path
from datetime import datetime
import hashlib,json,sys
from verify_reviewed_draft import verify
W=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
parent=W/'haiku_reviewed_section_20260922_130747_311801.md'
verify(parent);raw=parent.read_bytes();result=raw
review_path=(Path(sys.argv[1]).resolve() if len(sys.argv)>1 else
             W/'adversarial_memory_review/topic_v4_first3_20260922_133654_176011.json')
assert review_path.parent==W/'adversarial_memory_review'
review_raw=review_path.read_bytes();review=json.loads(review_raw)
assert review['status']=='APPROVED_DOCUMENTARY_FIDELITY_ONLY' and review['parent_sha256']==sha(raw)
changes=[]
for row in review['topics']:
    topic=row['topic'];directory=W/'topic_capsules_v4'
    old=(directory/(topic+'.original.md')).read_bytes()
    new=(directory/(topic+'.md')).read_bytes()
    assert sha(old)==row['original_sha256'] and sha(new)==row['capsule_sha256']
    assert result.count(old)==1
    result=result.replace(old,new,1)
    changes.append({'topic':topic,'before':old.decode(),'after':new.decode(),
                    'capsule_path':str(directory/(topic+'.md'))})
assert parent.read_bytes()==raw
out=W/('haiku_reviewed_topics_v4_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.md')
receipt={'status':'REVIEWED_TOPIC_DRAFT_NOT_DEPLOYED','topic_compaction_v4':True,
         'sha256':sha(result),'parent_path':str(parent),'parent_sha256':sha(raw),
         'review_path':str(review_path),'review_sha256':sha(review_raw),
         'source_sha256':review['source_sha256'],'changes':changes,
         'anthropic_tokens':None,'scope':'Focal documentary review; no global semantic or API-fit approval.'}
with out.open('xb')as f:f.write(result)
with out.with_suffix('.json').open('xb')as f:f.write(json.dumps(receipt,ensure_ascii=False,indent=2).encode())
print(json.dumps({'path':str(out),'sha256':sha(result),'topics':[r['topic'] for r in changes]}))
