from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
    assert p.is_relative_to(R) and not p.exists(),p
    b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
runs=sorted((R/'dev_modular_implementation').glob('*/run.json'))
good=[p for p in runs if json.loads(p.read_text(encoding='utf8'))['returncode']==0 and json.loads(p.read_text(encoding='utf8'))['source']==pin(K/'TGLExt/V351ModularImplementation.lean')]
assert good,'Final unchanged DEV rc0 required'
for base in ['run_modular_fixed_vectors_replay.py','audit_modular_fixed_vectors.py','validate_modular_fixed_vectors.py']:
    s=(R/base).read_text(encoding='utf8')
    for a,b in [('modular_fixed_vectors','modular_implementation'),('V351ModularFixedVectors','V351ModularImplementation'),('ModularFixedVectors','ModularImplementation'),('BadModularFixedAdjointEqualityRemoved','BadModularImplementationRightSignChanged'),('MODULAR_FIXED_VECTORS','MODULAR_IMPLEMENTATION')]:
        s=s.replace(a,b)
    if base.startswith('audit_'):
        s=s.replace('private_theorems=1','private_theorems=0').replace('new_theorems=2','new_theorems=1')
        s=s.replace("len(targets)==2 and sum(t['kind']=='theorem' for t in targets)==2","len(targets)==1 and sum(t['kind']=='theorem' for t in targets)==1")
        s=s.replace('AUDITORIA_VETORES_FIXOS_MODULARES_A1B','AUDITORIA_IMPLEMENTADOR_MODULAR_A1B')
        s=s.replace('modular_implementation_constructed=True,','modular_implementation_constructed=True, implementator_equality_proved=True,')
    else:
        s=s.replace('AUDITORIA_MEDIA_PAR_FIXO_A1B','AUDITORIA_VETORES_FIXOS_MODULARES_A1B')
    put(R/base.replace('modular_fixed_vectors','modular_implementation'),s)
name='scalarTomitaImaginaryPower_eq_regular_implementation'
put(K/'TGLExt/AuditA1ModularImplementation.lean','import TGLExt.V351ModularImplementation\n#check TGLV350.Regular.'+name+'\n#print axioms TGLV350.Regular.'+name+'\n')
put(R/'probes/BadModularImplementationRightSignChanged.lean','''import TGLExt.V351ModularImplementation
open TGLExt TGLV350.Regular
example (P : SiteProfile) (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t x =
      scalarGNSRepresentation P (regularRightCoreElement P t) (regularRightGNS P t x) :=
  scalarTomitaImaginaryPower_eq_regular_implementation P t x
''')
p=K/'TGLExt/V350StrongOperatorIntegral.lean';s=p.read_text(encoding='utf8');start=s.index('theorem operatorIntegral_commutes');end=s.index(' := by',start)
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='ADDENDUM_AFTER_DEV_BEFORE_ACCEPTANCE',new_theorems=1,new_definitions=0,private_theorems=0,
    correction='A extração automática da ficha truncou operatorIntegral_commutes num argumento (H := H); assinatura integral relida antes do código e registrada aqui. Primeiro DEV falhou por objeto antigo V350ScalarRegularPolarCommutation ausente; replay de fonte autoral rc0, um objeto novo, fontes intactas. Seguintes ajustaram associatividade/coerção e reescrita ampla que esgotava elaborador; substituída por congrArg/trans de map_mul e das igualdades de ação já disponíveis. Heartbeats permanecem2200000. Sem helper ou definição global adicional.',
    corrected_provider=dict(source=pin(p),line=s[:start].count('\n')+1,statement=s[start:end]),
    provider_replay=pin(R/'replay_modular_implementation_provider/20260915_010739_765642/run.json'),
    final_dev=pin(good[-1]),dev_history=[pin(p) for p in runs],
    scope='Equality of SAME U_t=pi(lambda_t)R_-t on ALL original scalar GNS vectors, not inferred from covariance alone. Chosen Z_n has exact ambient star(e_n)*e_n independent of t, is fixed by U; direct left/right product and commutation show W fixes same vector. Strong star convergence of contractions gives Z_n->I; bounded strong continuity of existing pi and original J transport to rho(Z_n)->I. Original right identity makes pi(a)Lambda(Z_n)=rho(Z_n)Lambda(a), giving approximation of every original ideal vector; density extends to all H. No assertion any one Lambda(Z_n) is cyclic. No h=Delta_nu, no Q equality, trace contract or gate. Negative changes right sign -t to +t and tests refusal of that application only.')
put(R/'ADENDO_FICHA_IMPLEMENTADOR_MODULAR.json',json.dumps(d,ensure_ascii=False,indent=2))
put(R/'ADENDO_FICHA_IMPLEMENTADOR_MODULAR.md','[OPEN — complemento após DEV e antes do aceite]\n\n'+json.dumps(d,ensure_ascii=False,indent=2)+'\n')
