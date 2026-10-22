from pathlib import Path
import hashlib, os
base = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\maxwell_global')

def write_new(name, text):
    path=base/name
    data=text.encode('utf-8')
    tmp=path.with_suffix('.lean.tmp_r45b')
    with tmp.open('xb') as f:
        f.write(data)
    assert tmp.read_bytes()==data
    os.rename(tmp,path)
    print({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':len(data)})

s=(base/'CompactBoostStrongDerivativeReductionR2.lean').read_text(encoding='utf-8')
old='''  simpa only [compactBoostGenerator, Pi.smul_apply] using
    (hc.fderiv_apply ℝ momentumLongitudinalDirection).smul_left
      (f := fun y : MomentumCoordinates => -shellEnergy y)'''
new='''  change HasCompactSupport ((fun y : MomentumCoordinates => -shellEnergy y) •
    (fun y : MomentumCoordinates => fderiv ℝ g y momentumLongitudinalDirection))
  exact (hc.fderiv_apply ℝ momentumLongitudinalDirection).smul_left
    (f := fun y : MomentumCoordinates => -shellEnergy y)'''
assert s.count(old)==1
s=s.replace(old,new)
assert s.count('    simpa using (Real.hasDerivAt_')==2
s=s.replace('    simpa using (Real.hasDerivAt_','    simpa [Function.comp_def] using (Real.hasDerivAt_')
write_new('CompactBoostStrongDerivativeReductionR3.lean',s)

s=(base/'CompactBoostStrongDerivativeR1.lean').read_text(encoding='utf-8')
assert s.count('import CompactBoostStrongDerivativeReductionR2')==1
s=s.replace('import CompactBoostStrongDerivativeReductionR2','import CompactBoostStrongDerivativeReductionR3')
assert s.count('    simpa using (Real.hasDerivAt_')==2
s=s.replace('    simpa using (Real.hasDerivAt_','    simpa [Function.comp_def] using (Real.hasDerivAt_')
write_new('CompactBoostStrongDerivativeR2.lean',s)
