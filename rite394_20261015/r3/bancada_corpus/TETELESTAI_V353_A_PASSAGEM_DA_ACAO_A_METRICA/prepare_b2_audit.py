from pathlib import Path
import re, os, json
R=Path(__file__).resolve().parent
def put(p,b):
    assert not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True)
    q=p.with_name(p.name+'.tmp');q.write_bytes(b)
    assert q.read_bytes()==b and b;os.replace(q,p)
targets=[]
for name in ['FLRWGeometry','FLRWFieldEquations']:
    p=R/'kernel/TGLExt'/f'{name}.lean'
    for m in re.finditer(r'^(def|theorem)\s+(\w+)',p.read_text(encoding='utf8'),re.M):
        targets.append(dict(kind=m[1],name='ChatgptAudit.FLRW.'+m[2],source=str(p)))
put(R/'ALVOS_B2.json',json.dumps(targets,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'kernel/TGLExt/AuditFLRW.lean',('import TGLExt.FLRWFieldEquations\n'+
    '\n'.join('#print axioms '+t['name'] for t in targets)+'\n').encode('utf8'))
header='''import TGLExt.FLRWFieldEquations
set_option autoImplicit false
open Matrix TGLExt ChatgptAudit ChatgptAudit.GeneralMetric ChatgptAudit.FLRW
open scoped ContDiff
noncomputable section
'''
probe1=header+'''-- Deliberate corruption: the 00 Einstein coefficient is changed.
example (U : Set Coordinate4) (hU : IsOpen U) (a : ℝ → ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
    (x : Coordinate4) (hx : x∈U) :
    geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x 0 0 =
      4*(flrwHubble a (x 0))^2 := by
  exact flrw_einstein_00 U hU a ha hpos x hx
end
'''
probe2=header+'''-- Deliberate corruption: the existential constant changes sign.
example (U : Set Coordinate4) (hU : IsOpen U) (a rho pressure : ℝ → ℝ)
    (ha : ∀ y∈U, ContDiffAt ℝ ∞ a (y 0)) (hpos : ∀ y∈U, 0 < a (y 0))
    (x : Coordinate4) (hx : x∈U) (coupling cosmological : ℝ)
    (hE : geometricEinsteinTensor (flrwMetric a) (metricInverse (flrwMetric a))
      (leviCivitaField (flrwMetric a) (metricInverse (flrwMetric a))) x+
      cosmological • flrwMetric a x = coupling • flrwStress a rho pressure x) :
    (flrwHubble a (x 0))^2 = coupling/3*rho (x 0)+cosmological/3 := by
  exact flrw_friedmann_first U hU a rho pressure ha hpos x hx coupling cosmological hE
end
'''
put(R/'probes_B2/BadFLRW00.lean',probe1.encode('utf8'))
put(R/'probes_B2/BadFLRWLambda.lean',probe2.encode('utf8'))
print(json.dumps(dict(targets=len(targets),theorems=sum(t['kind']=='theorem' for t in targets)),ensure_ascii=False))
