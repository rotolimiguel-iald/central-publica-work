"""Source and receipt review of the actual screen/helicity representation."""
import datetime as dt
import json
from pathlib import Path
from diary_r1 import ROOT, new, pin

out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
delivery=out/'orbital_rotation/FINAL_SCREEN_LORENTZ_RECEIPT_R1.json'
r=json.loads(delivery.read_bytes())
checked={}
def verify(v):
    if isinstance(v,dict):
        if {'path','sha256'}<=v.keys():
            a=pin(v['path']); assert a['sha256']==v['sha256'],v['path']
            if 'bytes' in v: assert a['bytes']==v['bytes']
            checked[v['path']]=a
        for x in v.values():verify(x)
    elif isinstance(v,list):
        for x in v:verify(x)
verify(r)
for row in r['accepted']:
    b=json.loads(Path(row['receipt']['path']).read_bytes());verify(b)
    assert type(b['exit_code']) is int and b['exit_code']==0
    assert b['readonly_dependencies_unchanged']
    assert b['source']['sha256']==row['source']['sha256']
assert len(r['accepted'])==18 and r['all_local_decl_count']==188
assert len({x['name'] for x in r['all_local_declarations']})==188
assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in r['all_local_declarations'])
assert r['zero_sorry'] and r['axioms_only_trio']
target=out/'network_review/SCREEN_LORENTZ_SEMANTIC_REVIEW_ROOT_R1.json'
new(target,dict(status='PASS_WITH_STATED_SCOPE',reviewer='codex-root',
    created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),delivery=pin(delivery),
    source_files_read=[x['source'] for x in r['accepted']],pins_verified=len(checked),
    all_local_declarations_verified=188,independent_rebuild=False,material_findings=[],
    findings=[
      'The O16 real screen matrix is complexified with its actual orthogonality and composition theorems. The inverse mass-shell pullback order matches the cocycle order.',
      'The null chart axis and its inverse images are excluded only on proved measure-zero sets. Holder multiplication constructs the bounded operator and the cocycle constructs its inverse and group law.',
      'Strong continuity combines a.e. continuity of the screen away from the axis, the integrable 4*norm(f)^2 bound, dominated convergence and the earlier orbital strong continuity.',
      'Translation covariance and the exact B0 action follow from the same screen/pullback definitions. They are not assumptions on a representation field.',
      'Proper four-dimensional determinant one supplies the screen orientation through the separately reviewed root determinant construction.',
      'The normalized circular matrix is unitary; C^-1 U_screen C preserves the exact U1 and B0. Its diagonal phase formula follows from the plus/minus screen eigenvectors.',
      'The future-matrix wrapper consumes the earlier generation theorem. Its product theorem retains the explicit future-product hypothesis hLM.'
    ],limits=[
      'This is not yet a jointly localized standard-subspace net: independence of wedge transport, isotony, locality, translation/boost covariance and wedge_glue must be connected to the existing KWR.',
      'No irreducible Wigner classification or geometric J equality follows solely from this block.',
      'This review read source proofs and checked compiled receipts; it did not rerun Lean or the whole program. The two determinant modules were constructed by root and already reviewed independently by the sibling.'
    ],script=pin(__file__),production_modified=False,gate_modified=False))
print(json.dumps(dict(review=pin(target),pins=len(checked),declarations=188)))
