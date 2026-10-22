"""Pin the root source-semantic review of the existing H1 spatial action."""
import datetime as dt,json
from diary_r1 import ROOT,new,pin
out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
base=out/'orbital_rotation'
delivery=base/'FINAL_FUTURE_LORENTZ_RECEIPT_R1.json'
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
assert r['all_local_decl_count']==43
findings=[
 {'module':'LorentzTimeStabilizerR4','conclusion':'A Lorentz matrix fixing e0 preserves the spatial norm and is exactly its constructed spatial orthogonal restriction.'},
 {'module':'LorentzFutureGenerationR6','conclusion':'For a future time column, arsinh(norm(v)) and a constructed spatial reflection reproduce that column. The remaining factor fixes e0, proving membership in the previously represented generated subgroup.'},
 {'module':'LorentzFutureRepresentationR1','conclusion':'The canonical inclusion in the generated subgroup is continuous, giving strong continuity on every future Lorentz matrix and exact U1 covariance. The product identity has explicit future-column witnesses for L, M and their product; closure of the future subtype is not separately packaged here.'}]



new(out/'network_review/FUTURE_LORENTZ_SEMANTIC_REVIEW_ROOT_R1.json',dict(
 status='PASS_WITH_STATED_SCOPE',reviewer='codex-root',time_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
 sources_read=[pin(base/(f['module']+'.lean')) for f in findings],findings=findings,
 delivery=pin(delivery),pins_verified=len(checked),all_local_declarations=43,
 independent_rebuild=False,material_findings=[],
 limits=['The represented action is scalar on the two fiber coordinates, including spatial reflections. No photon helicity or global standard-subspace net is supplied.',
 'Every future-time-column matrix belongs to the represented subgroup. The converse and an autonomous FutureLorentz group instance are not claimed.',
 'CanonicalNetInput and physical Maxwell/stress obligations remain separate. No production or gate change.'],script=pin(__file__)))
print(json.dumps(dict(review=pin(out/'network_review/FUTURE_LORENTZ_SEMANTIC_REVIEW_ROOT_R1.json'),pins=len(checked))))
