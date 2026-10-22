from pathlib import Path
import json,re,os
R=Path(__file__).resolve().parent
def put(p,b):
    assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True)
    q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
targets=[]
for name in ['ThermodynamicFriedmann','SectorRouteComparison']:
    p=R/'kernel/TGLExt'/f'{name}.lean';s=p.read_text(encoding='utf8')
    nested=s.find('namespace SectorFluid');end=s.find('end SectorFluid')
    for m in re.finditer(r'^(structure|def|theorem)\s+(\w+)',s,re.M):
        prefix='ChatgptAudit.FLRW.'+('SectorFluid.' if nested>=0 and nested<m.start()<end else '')
        targets.append(dict(kind=m[1],name=prefix+m[2],source=str(p)))
put(R/'ALVOS_B4.json',json.dumps(targets,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'kernel/TGLExt/AuditThermodynamics.lean',('import TGLExt.SectorRouteComparison\n'+'\n'.join('#print axioms '+x['name'] for x in targets)+'\n').encode('utf8'))
header='''import TGLExt.SectorRouteComparison
set_option autoImplicit false
open TGLExt ChatgptAudit.FLRW
noncomputable section
'''
put(R/'probes_B4/BadThermodynamicFactor.lean',(header+'''-- Deliberate corruption: discard the modified entropy factor.
example (H : ℝ → ℝ) (t G Phi enthalpy : ℝ)
    (D : HubbleHorizonInput H t G Phi enthalpy) :
    deriv H t = -4*Real.pi*G*enthalpy := by
  exact tgl_second_friedmann_from_clausius H t G Phi enthalpy D
end
''').encode('utf8'))
put(R/'probes_B4/BadVarianceSign.lean',(header+'''-- Deliberate corruption: reverse the source-difference sign.
example {i : Type*} [Fintype i] {I : Set ℝ} {H : ℝ → ℝ}
    (F : SectorFluid i I H) (c : TGLCoupling) (t : ℝ) (ht : t∈I)
    (hr : 0 < F.totalRho t) (he : 0 ≤ F.enthalpy t) :
    (F.correctedTotalRho c t+F.correctedTotalPressure c t)-
      entropyFactor c (F.wEff t)*F.enthalpy t = -c.beta*F.sectorVariance t := by
  exact (the_two_routes_differ F c t ht hr he).1
end
''').encode('utf8'))
s=(R/'audit_b3.py').read_text(encoding='utf8').replace('B3','B4').replace('AuditSector','AuditThermodynamics').replace('BadSectorClosure','BadThermodynamicFactor').replace('BadSectorAbs','BadVarianceSign').replace("['SectorFluidClosure','SectorFriedmann','AuditThermodynamics']","['ThermodynamicFriedmann','SectorRouteComparison','AuditThermodynamics']").replace('Finite conserved sectors applied to B2 FLRW; H_nx, null balance and cosmological constant explicit','Explicit horizon input, thermodynamic routes, variance and uniqueness under nonzero flux; no route selected')
put(R/'audit_b4.py',s.encode('utf8'))
print(json.dumps(dict(targets=len(targets),theorems=sum(x['kind']=='theorem' for x in targets),defs=sum(x['kind']=='def' for x in targets))))
