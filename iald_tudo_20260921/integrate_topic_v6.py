from pathlib import Path
from datetime import datetime
import hashlib,json,sys
from verify_reviewed_draft import verify
W=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
parent=W/'haiku_reviewed_topics_v5_20260922_140931_709157.md'
verify(parent)
raw=parent.read_bytes();result=raw
review_path=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else W/'adversarial_memory_review/topic_v6_review_20260922_141358_247824.json'
assert review_path.parent==W/'adversarial_memory_review'
review_raw=review_path.read_bytes();review=json.loads(review_raw)
assert review['status']=='APROVADA_FIDELIDADE_DOCUMENTAL'
changes=[]
for row in review['reviewed_topics']:
    old=Path(row['original_path']).read_bytes();new=Path(row['capsule_path']).read_bytes()
    assert sha(old)==row['original_sha256'] and sha(new)==row['capsule_sha256']
    assert result.count(old)==1
    result=result.replace(old,new,1)
    changes.append(row)
assert parent.read_bytes()==raw
out=W/('haiku_reviewed_topics_v6_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.md')
receipt={'topic_compaction_v6':True,'status':'REVIEWED_NOT_DEPLOYED','sha256':sha(result),
 'parent_path':str(parent),'parent_sha256':sha(raw),'review_path':str(review_path),
 'review_sha256':sha(review_raw),'changes':changes}
with out.open('xb')as f:f.write(result)
with out.with_suffix('.json').open('x',encoding='utf-8')as f:json.dump(receipt,f,ensure_ascii=False,indent=2)
print(out)
