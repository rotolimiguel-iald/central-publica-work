from pathlib import Path
import json,re,os
R=Path(__file__).resolve().parent
def put(p,b):
    assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True)
    q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
targets=[]
for name in ['SectorFluidClosure','SectorFriedmann']:
    p=R/'kernel/TGLExt'/f'{name}.lean'
    for m in re.finditer(r'^(structure|def|theorem)\s+(\w+)',p.read_text(encoding='utf8'),re.M):
        prefix='ChatgptAudit.FLRW.'+('SectorFluid.' if name=='SectorFluidClosure' and m[1]!='structure' else '')
        targets.append(dict(kind=m[1],name=prefix+m[2],source=str(p)))
put(R/'ALVOS_B3.json',json.dumps(targets,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'kernel/TGLExt/AuditSector.lean',('import TGLExt.SectorFriedmann\n'+'\n'.join('#print axioms '+x['name'] for x in targets)+'\n').encode('utf8'))
header='''import TGLExt.SectorFriedmann
set_option autoImplicit false
open TGLExt ChatgptAudit.FLRW
noncomputable section
'''
put(R/'probes_B3/BadSectorClosure.lean',(header+'''-- Deliberate corruption: beta is subtracted from the closed density.
example {i : Type*} [Fintype i] {I : Set ℝ} {H : ℝ → ℝ}
    (F : SectorFluid i I H) (c : TGLCoupling) (t : ℝ) :
    F.correctedTotalRho c t = F.totalRho t-c.beta*F.enthalpy t := by
  exact F.corrected_closure c t
end
''').encode('utf8'))
put(R/'probes_B3/BadSectorAbs.lean',(header+'''-- Deliberate corruption: the absolute-value reading has the opposite enthalpy.
example {i : Type*} [Fintype i] {I : Set ℝ} {H : ℝ → ℝ}
    (F : SectorFluid i I H) (t : ℝ)
    (hr : 0 < F.totalRho t) (he : 0 ≤ F.enthalpy t) :
    F.totalRho t*|1+F.wEff t| = -F.enthalpy t := by
  exact F.effective_enthalpy t hr he
end
''').encode('utf8'))
s=(R/'audit_b2.py').read_text(encoding='utf8').replace('B2','B3').replace('AuditFLRW','AuditSector').replace('BadFLRW00','BadSectorClosure').replace('BadFLRWLambda','BadSectorAbs').replace("['FLRWGeometry','FLRWFieldEquations','AuditSector']","['SectorFluidClosure','SectorFriedmann','AuditSector']").replace('FLRW geometry and conditional Friedmann in the existing general chart; no physical calibration derived','Finite conserved sectors applied to B2 FLRW; H_nx, null balance and cosmological constant explicit')
put(R/'audit_b3.py',s.encode('utf8'))
print(json.dumps(dict(targets=len(targets),theorems=sum(x['kind']=='theorem' for x in targets),defs=sum(x['kind']=='def' for x in targets))))
