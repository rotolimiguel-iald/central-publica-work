from pathlib import Path
import json,hashlib,os
R=Path(__file__).resolve().parent
p=R/'author_controls/20260915_125804_093873/RESULT.json'
d=json.loads(p.read_text(encoding='utf8'))
for row in d['controls']:
    result=json.loads(Path(row['run']['path']).read_text(encoding='utf8'))
    txt=Path(result['stdout']['path']).read_text(encoding='utf8')
    if row['module']=='BadA2GapTwo':
        assert "'change' tactic failed" in txt and 'is not definitionally equal to target' in txt
        assert '2 * ‖x‖' in txt and result['returncode']==1 and result['source_unchanged']
        row['semantic_rejection']=True
        row['classification_correction']='The classifier omitted the valid Lean diagnostic change tactic failed. No source or build was changed or rerun.'
assert all(r['semantic_rejection'] for r in d['controls'])
d['all_rejected_semantically']=True
d['original_result_preserved']=dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
out=R/'author_controls/20260915_125804_093873/SEMANTIC_RECLASSIFICATION.json'
assert not out.exists()
b=json.dumps(d,ensure_ascii=False,indent=2).encode('utf8')
t=out.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,out)
print(json.dumps(dict(path=str(out),sha256=hashlib.sha256(b).hexdigest(),all_rejected_semantically=True)))
