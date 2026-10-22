"""Source and receipt review of the actual screen/helicity representation."""
import datetime as dt
import json
from pathlib import Path
from diary_r1 import ROOT, new, pin

out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
delivery=out/'orbital_rotation/FINAL_SCREEN_REFLECTION_RECEIPT_R1.json'
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
assert len(r['accepted'])==4 and r['all_local_decl_count']==39
assert len({x['name'] for x in r['all_local_declarations']})==39
assert all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in r['all_local_declarations'])
assert r['zero_sorry'] and r['axioms_only_trio']
target=out/'network_review/SCREEN_REFLECTION_SEMANTIC_REVIEW_ROOT_R1.json'
new(target,dict(status='PASS_WITH_STATED_SCOPE',reviewer='codex-root',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),delivery=pin(delivery),source_files_read=[x['source'] for x in r['accepted']],pins_verified=len(checked),all_local_declarations_verified=39,independent_rebuild=False,material_findings=[],findings=[
 'Theta is the pointwise existing helicity-swapping conjugation; involutivity and norm preservation are proved in the original H1.',
 'The proper-Lorentz commutation uses the actual paired circular phases, with determinant-one retained; translation conjugation changes the sign explicitly.',
 'The half turn is the genuine rotation around the longitudinal axis: its screen cocycle is identity and its action is the transverse pullback. It is not an angular homonym from the finite screen alone.',
 'The existing Fourier/geometric identification of Jcandidate is reused to prove Jcandidate=U(halfTurn)Theta. The conjugation of Lorentz actions then follows by the group law.'
 ],limits=['No wedge localization, isotony, causal locality or wedge_glue follows solely from these representation identities.','This review checks source proofs, hashes and compiled receipts; it does not claim independent Lean recompilation.'],script=pin(__file__),production_modified=False,gate_modified=False))
print(json.dumps(dict(review=pin(target),pins=len(checked),declarations=39)))
