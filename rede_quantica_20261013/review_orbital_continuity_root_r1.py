"""Pin the root source-semantic review of the existing H1 spatial action."""
import datetime as dt,json
from diary_r1 import ROOT,new,pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
base=out/'orbital_rotation'
delivery=base/'FINAL_ORBITAL_CONTINUITY_RECEIPT_R1.json'
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
assert r['all_local_decl_count']==33
findings=[
 {'module':'OrbitalLocalFinitenessR2','conclusion':'The sup/product momentum norm is bounded by Euclidean shell energy. Density inverse energy is dominated by inverse momentum norm; singularity at zero is locally integrable in dimension three. Local finiteness/regularity of orbitalMeasure zero are derived, not postulated.'},
 {'module':'OrbitalSpatialContinuityR1','conclusion':'The orthogonal group carries operator-norm topology. Continuous inverse pullback on original momentum coordinates and proved measure preservation feed compMeasurePreservingLp; original H1 receives the strongly continuous scalar action. Identity/composition follow from the same inverse-pullback action.'},
 {'module':'OrbitalSpatialCovarianceR2','conclusion':'The Minkowski orbital pairing is decomposed as energy minus Euclidean dot product with the actual coordinate permutation. Orthogonality proves phase intertwining for every Q; ae pullback then proves U1 covariance on original H1.'}]

new(out/'network_review/ORBITAL_CONTINUITY_SEMANTIC_REVIEW_ROOT_R1.json',dict(
 status='PASS_WITH_STATED_SCOPE',reviewer='codex-root',time_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
 sources_read=[pin(base/(f['module']+'.lean')) for f in findings],findings=findings,
 delivery=pin(delivery),pins_verified=len(checked),all_local_declarations=33,
 independent_rebuild=False,material_findings=[],
 limits=['Scalar orbital action, diagonal on helicity coordinates; a photon Wigner cocycle is not supplied.',
 'Strong continuity in Q and U1 covariance are now derived; full Lorentz/Poincare relations and globally localized standard-subspace net remain separate obligations.',
 'No joint certificate, physical calibration, production installation or gate change follows.'],script=pin(__file__)))
print(json.dumps(dict(review=pin(out/'network_review/ORBITAL_CONTINUITY_SEMANTIC_REVIEW_ROOT_R1.json'),pins=len(checked))))
