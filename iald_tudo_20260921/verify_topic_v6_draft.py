from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def verify_topics(path):
    from verify_reviewed_draft import verify
    path=Path(path);raw=path.read_bytes();d=json.loads(path.with_suffix('.json').read_bytes())
    assert sha(raw)==d['sha256']
    parent=Path(d['parent_path']);assert parent.parent==W and parent!=path
    assert json.loads(parent.with_suffix('.json').read_bytes()).get('topic_compaction_v5') is True
    verify(parent);original=parent.read_bytes();assert sha(original)==d['parent_sha256']
    rp=Path(d['review_path']);assert rp.parent==W/'adversarial_memory_review'
    rr=rp.read_bytes();assert sha(rr)==d['review_sha256']
    review=json.loads(rr);assert review['status']=='APROVADA_FIDELIDADE_DOCUMENTAL'
    assert d['changes']==review['reviewed_topics']
    base=W/'haiku_reviewed_section_20260922_130747_311801.md'
    assert sha(base.read_bytes())==review['source_sha256']
    restored=raw;seen=set()
    for row in d['changes']:
        assert row['topic'] not in seen
        seen.add(row['topic'])
        oldpath,newpath=Path(row['original_path']),Path(row['capsule_path'])
        assert oldpath.parent==newpath.parent==W/'topic_capsules_v6'
        old,new=oldpath.read_bytes(),newpath.read_bytes()
        assert sha(old)==row['original_sha256'] and sha(new)==row['capsule_sha256']
        assert restored.count(new)==1
        restored=restored.replace(new,old,1)
    assert restored==original
    assert path.read_bytes()==raw and parent.read_bytes()==original
    return {'status':'TOPIC_V6_VERIFIED_NOT_DEPLOYED','draft_sha256':sha(raw),'topics':sorted(seen),
            'all_other_parent_bytes_preserved':True,'scope':'Documentary integration only; not proof or provider fit.'}
