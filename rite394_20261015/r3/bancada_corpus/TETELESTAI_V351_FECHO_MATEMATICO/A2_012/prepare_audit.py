from pathlib import Path
import re,json,hashlib,os
R=Path(__file__).resolve().parent
mods=['V354FiniteTraceSupport','V354SpectralThreshold','V354RegularMatrixCorner',
 'V354FiniteEqualSplit','V354NormalizedSplit','V354RegularSupport',
 'V354PositiveTraceReader','V354TraceReaderWall']
names=[];records=[]
def put(p,b):
 assert not p.exists() and b
 t=p.with_suffix(p.suffix+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
for m in mods:
 p=R/'src/TGLExt'/(m+'.lean');b=p.read_bytes();txt=b.decode('utf8')
 ns=re.findall(r'^(?:theorem|def)\s+(\w+)',txt,re.M)
 assert ns
 names += ['TGLV350.Regular.'+n for n in ns]
 records.append(dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),names=ns))
assert len(names)==len(set(names))
s='import TGLExt.V354TraceReaderWall\n\n'
s+='\n'.join('#print axioms '+n for n in names)+'\n'
put(R/'src/TGLExt/AuditA2RegularSupport.lean',s.encode('utf8'))
put(R/'AUDIT_NAMES.json',json.dumps(dict(names=names,sources=records),ensure_ascii=False,indent=2).encode('utf8'))
# Mutations alter propositions, keeping the source/import graph and proof bodies.
original=(R/'src/TGLExt/V354RegularSupport.lean').read_text(encoding='utf8')
mutations=[
 ('BadA2TraceZero','scalarInverseLimitWeight P (regularFiniteSupport P) = 1 :=',
  'scalarInverseLimitWeight P (regularFiniteSupport P) = 0 :='),
 ('BadA2GapTwo','    ‖regularMinimalLock P x‖ = ‖x‖ := by',
  '    ‖regularMinimalLock P x‖ = 2 * ‖x‖ := by'),
 ('BadA2ZeroProjection','    (regularMinimalLock P).ker.starProjection = (regularFiniteSupport P).val := by',
  '    (regularMinimalLock P).ker.starProjection = 0 := by')]
controls=[]
for m,old,new in mutations:
 assert original.count(old)==1
 b=original.replace(old,new).encode('utf8')
 put(R/'src/TGLExt'/(m+'.lean'),b)
 controls.append(dict(module=m,mutation=dict(old=old,new=new),expected='SEMANTIC_REJECTION'))
s='''import TGLExt.V354TraceReaderWall
open TGLExt TGLV350.Regular
example (P : SiteProfile) :
    ∀ x y : (regularCoreAlgebra P).toStarSubalgebra,
      positiveTraceReader P (x*y) = positiveTraceReader P (y*x) := by
  exact positiveTraceReader_not_cyclic P
'''
put(R/'src/TGLExt/BadA2CyclicReader.lean',s.encode('utf8'))
controls.append(dict(module='BadA2CyclicReader',expected='SEMANTIC_REJECTION',
 reason='Claim global cyclicity for a reader proved noncyclic in the same core.'))
s='''import TGLExt.V354TraceReaderWall
open TGLExt TGLV350.Regular
example (P : SiteProfile) :
    (regularContinuousCorner P).normalizedTrace (regularContinuousCorner P).Pplus = 0 := by
  exact (regularContinuousCorner_readings P).2.1
'''
put(R/'src/TGLExt/BadA2FaceZero.lean',s.encode('utf8'))
controls.append(dict(module='BadA2FaceZero',expected='SEMANTIC_REJECTION',
 reason='Replace the existing half-trace conclusion by zero.'))
put(R/'CONTROLES_AUTORAIS_PLANO.json',json.dumps(controls,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(dict(audited_names=len(names),modules=len(mods),controls=len(controls))))
