from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
    assert p.is_relative_to(R) and not p.exists(),p
    b=s.encode('utf8');q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
for base in ['run_finite_minorants_replay.py','audit_finite_minorants.py','validate_finite_minorants.py']:
    s=(R/base).read_text(encoding='utf8')
    for a,b in [('finite_minorants','average_polar_right'),('V351InverseLimitFiniteMinorants','V351AveragePolarRight'),('InverseLimitFiniteMinorants','AveragePolarRight'),('BadFiniteMinorantsTraceRemoved','BadAverageMembershipIsSelfAdjoint'),('AUDITORIA_EXTENSAO_TRACIAL_A1B','AUDITORIA_MINORANTES_FINITOS_A1B'),('FINITE_MINORANTS','AVERAGE_POLAR_RIGHT')]:s=s.replace(a,b)
    if base.startswith('audit_'):
        s=s.replace('private_theorems=4','private_theorems=3')
        s=s.replace('finite_contractions_constructed=True, average_polar_right_conditional_on_traciality=True','average_polar_right_constructed=True, fixed_tomita_vectors_constructed=False')
        s=s.replace("put(R/'AUDITORIA_MINORANTES_FINITOS_A1B.json'","put(R/'AUDITORIA_MEDIA_ACAO_DIREITA_A1B.json'")
    put(R/base.replace('finite_minorants','average_polar_right'),s)
names=['regularAverage_polar_approximants','regularAverage_mem_scalarPolarRightAlgebra']
put(K/'TGLExt/AuditA1AveragePolarRight.lean','import TGLExt.V351AveragePolarRight\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadAverageMembershipIsSelfAdjoint.lean','''import TGLExt.V351AveragePolarRight
open TGLExt TGLV350.Regular
example (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    star (regularAverage P δ) = regularAverage P δ :=
  regularAverage_mem_scalarPolarRightAlgebra P δ hδ
''')
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='ADDENDUM_AFTER_DEV_BEFORE_ACCEPTANCE',
    decision='Exact partition replaces a generic Riemann-sum framework as proposed before coding. Two public theorems, three private helpers, no global definitions. The contraction-bound argument is local within the approximation theorem.',
    corrections='First DEV timeouts from incomplete scalar coercions and broad ext descending into Lp; explicit real-to-complex casts and ext1 resolve without raising heartbeats. Second DEV had unresolved measure/filter/metavariables and fixed with actual volume, atTop and typed limits. Third DEV rc0 clean. Original operatorIntegral commutation provider remains adequate mathematically; its concrete instance wrapper needed the already used vector-integral transport shape from V351CutoffAverageCommutation, not another integral.',
    adapter=pin(K/'TGLExt/V351CutoffAverageCommutation.lean'),
    final_dev=pin(R/'dev_average_polar_right/20260915_002754_463277/run.json'),
    limitations='The average is one-sided and is not claimed selfadjoint. Negative control deliberately confuses algebra membership with selfadjointness. No fixed S/F vector, U=pi(lambda)R_-t, Q, traciality or trace contract is proved in this delta.')
put(R/'ADENDO_FICHA_MEDIA_ACAO_DIREITA.json',json.dumps(d,ensure_ascii=False,indent=2))
put(R/'ADENDO_FICHA_MEDIA_ACAO_DIREITA.md','[OPEN — complemento posterior ao DEV e anterior ao aceite]\n\n'+json.dumps(d,ensure_ascii=False,indent=2)+'\n')

