"""Pin the root source-semantic review of the existing H1 spatial action."""
import datetime as dt,json
from diary_r1 import ROOT,new,pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
base=out/'orbital_rotation'
delivery=base/'FINAL_ORBITAL_ROTATION_RECEIPT_R1.json'
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
assert r['all_local_decl_count']==50
findings=[
 {'module':'OrbitalSpatialMeasureR1','conclusion':'The volume-preserving Euclidean chart is used only as coordinates. Orthogonality preserves shell energy and the actual orbital density, including m=0; withDensity invariance is proved, not imported as a hypothesis.'},
 {'module':'OrbitalSpatialUnitaryR3','conclusion':'Inverse pullback has an explicit inverse, unitary identity/composition laws, and target/source definitionally the original ImportedSQ.H1. No replacement Hilbert space is substituted.'},
 {'module':'OrbitalQuarterTurnR4','conclusion':'Explicit orthogonal quarter turn mixes longitudinal and transverse coordinates. The determinant-one displayed matrix matches the coordinate formula. Its group/spatial content is distinct from the two-dimensional angular screen reading.'},
 {'module':'OrbitalQuarterCovarianceR1','conclusion':'Orbital phase is transformed using energy invariance and coordinate identities, then the almost-everywhere L2 representatives produce exact U1 covariance and conjugation.'}]
new(out/'network_review/ORBITAL_ROTATION_SEMANTIC_REVIEW_ROOT_R1.json',dict(
 status='PASS_WITH_STATED_SCOPE',reviewer='codex-root',time_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
 sources_read=[pin(base/(f['module']+'.lean')) for f in findings],findings=findings,
 delivery=pin(delivery),pins_verified=len(checked),all_local_declarations=50,
 independent_rebuild=False,material_findings=[],
 limits=['Scalar orbital action, diagonal on helicity coordinates; a photon Wigner cocycle is not supplied.',
 'Continuity in Q, full Lorentz relations and a globally localized standard-subspace net remain separate obligations.',
 'No joint certificate, physical calibration, production installation or gate change follows.'],script=pin(__file__)))
print(json.dumps(dict(review=pin(out/'network_review/ORBITAL_ROTATION_SEMANTIC_REVIEW_ROOT_R1.json'),pins=len(checked))))
