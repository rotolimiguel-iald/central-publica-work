"""Pin the root source-semantic review of the existing H1 spatial action."""
import datetime as dt,json
from diary_r1 import ROOT,new,pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
base=out/'orbital_rotation'
delivery=base/'FINAL_SPATIAL_POINCARE_RECEIPT_R1.json'
r=json.loads(delivery.read_bytes());checked={}
def verify_pins(value):
    if isinstance(value,dict):
        if {'path','sha256'}<=value.keys():
            actual=pin(value['path']);assert actual['sha256']==value['sha256']
            if 'bytes' in value:assert actual['bytes']==value['bytes']
            checked[value['path']]=actual
        for x in value.values():verify_pins(x)
    elif isinstance(value,list):
        for x in value:verify_pins(x)
verify_pins(r)
for item in r['accepted']:
    rr=json.loads(open(item['receipt']['path'],'rb').read());verify_pins(rr)
    assert rr['exit_code']==0 and rr['readonly_dependencies_unchanged']
assert r['all_local_decl_count']==52
findings=[
 {'module':'OrbitalSpatialLorentzR2','conclusion':'The actual coordinate permutation is linear and preserves orbitPairing. Its matrix is proved Lorentz by testing the exact eta form on basis vectors; time component remains unchanged.'},
 {'module':'OrbitalSpatialPoincareR2','conclusion':'The orthogonal-group homomorphism enters existing LorentzGrp and PoincareGroup. The representation uses the existing U1 and scalar rotation action; covariance supplies the exact semidirect group multiplication.'},
 {'module':'OrbitalOrientedBoostR1','conclusion':'Boosts are actual conjugates of existing B0 by spatial unitaries on original H1. Group law, continuity and covariance with the corresponding conjugate theBoost matrix are proved, not supplied as fields.'}]

new(out/'network_review/SPATIAL_POINCARE_SEMANTIC_REVIEW_ROOT_R1.json',dict(
 status='PASS_WITH_STATED_SCOPE',reviewer='codex-root',time_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
 sources_read=[pin(base/(f['module']+'.lean')) for f in findings],findings=findings,
 delivery=pin(delivery),pins_verified=len(checked),all_local_declarations=52,
 independent_rebuild=False,material_findings=[],
 limits=['Scalar orbital action, diagonal on helicity coordinates; a photon Wigner cocycle is not supplied.',
 'A spatial Poincare subgroup and each rotated one-parameter boost are constructed; full generated-group relations, photon helicity transport and global localized standard-subspace net remain separate obligations.',
 'No joint certificate, physical calibration, production installation or gate change follows.'],script=pin(__file__)))
print(json.dumps(dict(review=pin(out/'network_review/SPATIAL_POINCARE_SEMANTIC_REVIEW_ROOT_R1.json'),pins=len(checked))))
