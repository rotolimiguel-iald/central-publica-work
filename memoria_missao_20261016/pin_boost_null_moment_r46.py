from pathlib import Path
import datetime, hashlib, json, os, re, subprocess
out=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
base=out/'maxwell_global'
kernel=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
mathlib=kernel/'.lake/packages/mathlib/Mathlib'
ref=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\FECHO_MISSION_REFERENCE.json')
actor={'kind':'agent','id':'codex-r8-boost-moment-link'}
request={'operation':'project','reference':str(ref),'actor':actor,'max_chars':100000}
run=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],input=json.dumps(request),text=True,encoding='utf-8',capture_output=True,check=True)
response=json.loads(run.stdout)
assert response['ok'],response
p=response['result']
def pin(path):
    path=Path(path); b=path.read_bytes()
    return {'path':str(path),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
source=base/'CompactBoostNullMomentLinkR1.lean'
s=source.read_text(encoding='utf-8')
assert not re.search(r'\b(sorry|admit)\b|(?m:^\s*(axiom|opaque)\s)',s)
files=[base/f for f in [
 'CompactBoostStrongDerivativeReductionR3.lean','CompactBoostStrongDerivativeR2.lean',
 'NullFrequencyBochnerR2.lean','MaxwellNullSchwartzConsumerR2.lean',
 'ConstructedNullSchwartzConsumerR1.lean','ConstructedRealNullStressMomentR1.lean',
 'UnitaryFourierRealStressR2.lean','NullSchwartzDomainConstructionR2.lean',
 'MaxwellNullSchwartzCoreTransportR3.lean','MaxwellNullPlaneAlgebraR2.lean',
 'MaxwellNullPlaneWaveR2.lean','MaxwellScreenEnergyKernelR3.lean','MaxwellMomentTransportR3.lean']]
files += [kernel/'TGLExt/ContratoQG_v31.lean',kernel/'TGLExt/TheImportedSecondQuantization.lean']
files += [mathlib/f for f in ['Analysis/InnerProductSpace/Calculus.lean',
 'Analysis/InnerProductSpace/Basic.lean','Analysis/InnerProductSpace/LinearMap.lean',
 'Analysis/Normed/Lp/PiLp.lean','Analysis/Calculus/FDeriv/Linear.lean',
 'Topology/DenseEmbedding.lean','Topology/Algebra/Order/Archimedean.lean',
 'Topology/Instances/Rat.lean','MeasureTheory/Function/L2Space.lean',
 'Analysis/Distribution/SchwartzSpace/Basic.lean']]
files += [out/'mission_resume_20261016/LIVE_R46_HANDOFF_R8_20261016T175440_543436Z_dc27c6f3_RECEIPT.json',
 out/'orbital_rotation/attempts/20261016T175543_590282Z/RECEIPT.json',
 out/'orbital_rotation/attempts/20261016T175543_590282Z/AXIOMS.txt',
 out/'orbital_rotation/attempts/20261016T175125_726518Z/RECEIPT.json']
attempt_source=out/'orbital_rotation/attempts/20261016T175543_590282Z/CompactBoostStrongDerivativeR2.lean'
assert attempt_source.read_bytes()==(base/'CompactBoostStrongDerivativeR2.lean').read_bytes()
report={
 'schema':'iald-lean-candidate/v1','status':'DECLARADO_UNCOMPILED',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'actor':actor,'reference':pin(ref),'mission_receipt':p['receipt'],
 'projection_sha256':p['projection_sha256'],'projection_chars':p['actual_chars'],
 'handle':'r46-r8-boost-moment-link','source':pin(source),
 'lines':len(s.splitlines()),'theorem_count':len(re.findall(r'^theorem ',s,re.M)),
 'print_axioms_count':len(re.findall(r'^#print axioms ',s,re.M)),
 'chain':[
 'Existing real transverse polarization preserves the Fib complex inner product off its measure-zero axis.',
 'Orbital representative equality for each rational boost parameter; countable intersection then continuity gives equality of the whole smooth orbit.',
 'Uniqueness of pointwise derivatives derives nullScreenCLM(generator) = shellNullFrequency * lineDeriv(profile); it is not a field or a premise.',
 'The actual H1 inner product is an integrable Bochner integral of the compact representatives.',
 'Existing null-frequency Jacobian cancels u against du/u, yielding the two unweighted profile/line-derivative integrals.',
 'Unitarity of the same B0 and strong differentiation force the generator expectation real part to vanish.',
 'Normalized real null moment equals Im(inner(h,d)); HasBoostEnergy follows with the contract sign i*b.'
 ],
 'final_statement':'axisCompact_hasBoostEnergy_normalized_moment (h : H1) (hh : AxisCompactProfile h) : HasBoostEnergy B0 h (integral x, x 0 * unitaryFourierRealNullStress h x)',
 'premises':'Only the existing AxisCompactProfile domain in the final theorem. No majorant, strong derivative, profile derivative or charge-equality premise.',
 'not_claimed':['Compilation or independent acceptance of this candidate','Finite coherent Fock extension','Nonzero modular energy','Full MaxwellCertificate','Complete R8','Gate change'],
 'build_performed':False,'pins':[pin(f) for f in files],
 'pin_coverage':'Consulted direct suppliers and pinned mathlib APIs, prior strong-derivative build evidence, exact handoff. Not a transitive build custody.'
}
dst=base/'COMPACT_BOOST_NULL_MOMENT_LINK_CANDIDATE_R46.json'
data=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
tmp=dst.with_suffix('.json.tmp_r46')
with tmp.open('xb') as f:f.write(data)
assert tmp.read_bytes()==data
os.rename(tmp,dst)
print(json.dumps({'source':report['source'],'manifest':pin(dst),'lines':report['lines'],'theorems':report['theorem_count'],'pins':len(files),'revision':p['receipt']['revision']},ensure_ascii=False))
