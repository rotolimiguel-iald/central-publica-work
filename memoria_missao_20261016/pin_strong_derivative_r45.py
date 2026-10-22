from pathlib import Path
import datetime, hashlib, json, os, re, subprocess

out = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
base = out / 'maxwell_global'
kernel = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
mathlib = kernel / '.lake/packages/mathlib/Mathlib'
ref = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
actor = {'kind':'agent','id':'codex-r8-strong-derivative-r2'}
request = {'operation':'project','reference':str(ref),'actor':actor,'max_chars':100000}
run = subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],input=json.dumps(request),text=True,encoding='utf-8',capture_output=True,check=True)
project = json.loads(run.stdout)
assert project['ok'], project
result = project['result']

def pin(path):
    path = Path(path)
    b = path.read_bytes()
    return {'path':str(path),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}

old = json.loads((base/'COMPACT_BOOST_STRONG_DERIVATIVE_REDUCTION_CANDIDATE_R1.json').read_text(encoding='utf-8'))
rechecked = []
for item in old['pins']:
    current = pin(item['path'])
    assert current['sha256'] == item['sha256'], current['path']
    rechecked.append(current)
assert pin(base/'CompactBoostStrongDerivativeReductionR1.lean')['sha256'] == old['source']['sha256']
sources = [base/'CompactBoostStrongDerivativeReductionR2.lean',base/'CompactBoostStrongDerivativeR1.lean']
static = []
for path in sources:
    text = path.read_text(encoding='utf-8')
    assert not re.search(r'\b(sorry|admit)\b|(?m:^\s*(axiom|opaque)\s)',text)
    static.append({'path':str(path),'lines':len(text.splitlines()),'theorem_count':len(re.findall(r'^theorem ',text,re.M)),'print_axioms_count':len(re.findall(r'^#print axioms ',text,re.M))})
extra = [
    base/'MaxwellBoostEnergyR2.lean',
    mathlib/'Analysis/Calculus/MeanValue.lean',
    mathlib/'Analysis/Normed/Group/Bounded.lean',
    mathlib/'Analysis/Normed/Group/Basic.lean',
    mathlib/'Analysis/Normed/Operator/LinearIsometry.lean',
    mathlib/'Topology/Algebra/Support.lean',
    mathlib/'MeasureTheory/Integral/IntegrableOn.lean',
    mathlib/'MeasureTheory/Function/L2Space.lean',
    out/'PROGRESS_R44_SCIENCE_CUSTODY.json',
    out/'orbital_rotation/attempts/20261016T170720_512773Z/AXIOMS.txt',
    out/'orbital_rotation/attempts/20261016T170720_512773Z/RECEIPT.json',
    out/'mission_resume_20261016/LIVE_R45_HANDOFF_R8_20261016T173803_395525Z_65f8542e_RECEIPT.json',
    base/'CompactBoostStrongDerivativeReductionR1.lean',
]
report = {
 'schema':'iald-lean-candidate/v1','status':'DECLARADO_UNCOMPILED',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'actor':actor,'reference':pin(ref),'mission_receipt':result['receipt'],
 'projection_sha256':result['projection_sha256'],'projection_chars':result['actual_chars'],
 'handle':'r45-r8-strong-derivative','sources':[pin(p) for p in sources],
 'static_checks':static,
 'repairs':['Explicit real scalar function in compact-support smul_left.',
   'Hyperbolic derivative composition at the exact point -(0 : real).',
   'Explicit real square in absolute-value rewrite.',
   'Direct L2 inner-product norm-square identity, removing unrelated NoAtoms supplier premise.',
   'Actual pinned coe_refl API instead of missing refl_apply.'],
 'extension':[
   'Joint continuity of the existing momentum boost and its parameter derivative.',
   'Compact orbit K = boost image of [-1,1] times tsupport(g).',
   'Derivative bounded on [-1,1] times K; mean-value estimate of all nonzero slopes.',
   'Squared error majorant K.indicator((2*abs(C))^2), integrable by local finiteness.',
   'Off K, the existing a.e. inverse boost and derivative support inclusion make the error zero.',
   'compactBoost_hasDerivAt: actual B0 orbit strongly differentiable in the existing H1.',
   'axisCompact_boost_strong_derivative: extracts smooth compact representative and its derivative vector.'],
 'scope':'Candidate strong H1 derivative at zero on AxisCompactProfile; no additional differentiability or majorant premise in the final theorem. Parameter differentiation only; no spatial differentiation of energy across the axis.',
 'not_claimed':['Compilation success','Independent acceptance','Charge link','Nonzero modular energy witness','Complete MaxwellCertificate','Complete R8','Kernel or production change'],
 'build_performed':False,'originals_unchanged':True,
 'pins':rechecked+[pin(p) for p in extra],
 'pin_coverage':'Direct reused suppliers, consulted mathlib APIs, failed R1 evidence and handoff. Not a transitive build custody.'
}
dst = base/'COMPACT_BOOST_STRONG_DERIVATIVE_CANDIDATE_R45.json'
data = (json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
tmp = dst.with_suffix('.json.tmp_r45')
with tmp.open('xb') as f:
    f.write(data)
assert tmp.read_bytes() == data
os.rename(tmp,dst)
print(json.dumps({'report':pin(dst),'sources':report['sources'],'static':static,'pins':len(report['pins']),'revision':result['receipt']['revision']},ensure_ascii=False))
