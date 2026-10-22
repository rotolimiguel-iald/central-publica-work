from pathlib import Path
import os,re,json
R=Path(__file__).resolve().parent
def put(p,b):
    assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True)
    q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
p=R/'kernel/TGLExt/TheAngleReachesTheMetric.lean'
targets=[dict(kind='theorem',name='ChatgptAudit.FLRW.'+m[1],source=str(p)) for m in re.finditer(r'^theorem (\w+)',p.read_text(encoding='utf8'),re.M)]
put(R/'ALVOS_B5.json',json.dumps(targets,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'kernel/TGLExt/AuditMetricAngle.lean',('import TGLExt.TheAngleReachesTheMetric\n'+'\n'.join('#print axioms '+x['name'] for x in targets)+'\n').encode('utf8'))
head='''import TGLExt.TheAngleReachesTheMetric
set_option autoImplicit false
open TGLExt ChatgptAudit.FLRW
'''
put(R/'probes_B5/BadAngleAmplitude.lean',(head+'''-- Deliberate corruption: amplitude is mistaken for probability.
example (c : TGLCoupling) : c.beta = Real.sin (thetaMiguel c.beta) := by
  exact coupling_eq_sin_sq c
''').encode('utf8'))
put(R/'probes_B5/BadAngleFactor.lean',(head+'''-- Deliberate corruption: discard the unit term of the factor.
example (c : TGLCoupling) (w : ℝ) :
    entropyFactor c w = Real.sin (thetaMiguel c.beta)^2*|1+w| := by
  exact the_angle_reaches_the_metric c w
''').encode('utf8'))
s=(R/'audit_b4.py').read_text(encoding='utf8').replace('B4','B5').replace('AuditThermodynamics','AuditMetricAngle').replace('BadThermodynamicFactor','BadAngleAmplitude').replace('BadVarianceSign','BadAngleFactor').replace("['ThermodynamicFriedmann','SectorRouteComparison','AuditMetricAngle']","['TheAngleReachesTheMetric','AuditMetricAngle']").replace('Explicit horizon input, thermodynamic routes, variance and uniqueness under nonzero flux; no route selected','Angular rewrites only; unchanged metric and horizon hypotheses; no angle in runtime')
put(R/'audit_b5.py',s.encode('utf8'))
print(len(targets))
