from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
    assert p.is_relative_to(R) and not p.exists(),p
    b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
for base in ['run_average_fixed_pair_replay.py','audit_average_fixed_pair.py','validate_average_fixed_pair.py']:
    s=(R/base).read_text(encoding='utf8')
    for a,b in [('average_fixed_pair','modular_fixed_vectors'),('V351AverageFixedPair','V351ModularFixedVectors'),('AverageFixedPair','ModularFixedVectors'),('BadFixedPairRightPremiseRemoved','BadModularFixedAdjointEqualityRemoved'),('AVERAGE_FIXED_PAIR','MODULAR_FIXED_VECTORS')]:
        s=s.replace(a,b)
    if base.startswith('audit_'):
        s=s.replace('private_theorems=0','private_theorems=1')
        s=s.replace('AUDITORIA_MEDIA_PAR_FIXO_A1B','AUDITORIA_VETORES_FIXOS_MODULARES_A1B')
    else:
        s=s.replace('AUDITORIA_MEDIA_ACAO_DIREITA_A1B','AUDITORIA_MEDIA_PAR_FIXO_A1B')
    put(R/base.replace('average_fixed_pair','modular_fixed_vectors'),s)
names=['scalarTomitaImaginaryPower_fixed_of_fixed_pair','regularAverage_square_modular_fixed']
put(K/'TGLExt/AuditA1ModularFixedVectors.lean','import TGLExt.V351ModularFixedVectors\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadModularFixedAdjointEqualityRemoved.lean','''import TGLExt.V351ModularFixedVectors
open TGLExt TGLV350.Regular
example (P : SiteProfile) (x : ScalarGNSHilbert P)
    (hS : x ∈ scalarClosedTomitaDomain P) (hF : x ∈ scalarTomitaAdjointDomain P)
    (hxS : scalarClosedTomita P ⟨x,hS⟩ = x) (t : ℝ) :
    scalarTomitaImaginaryPower P t x = x :=
  scalarTomitaImaginaryPower_fixed_of_fixed_pair P x hS hF hxS
''')
extra=[]
for path,needle in [('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/LinearMap.lean','@[simp] lemma rankOne_apply'),('.lake/packages/mathlib/Mathlib/Algebra/Star/Module.lean','theorem algebraMap_star_comm')]:
    p=K/path;ls=p.read_text(encoding='utf8').splitlines();line=next(i+1 for i,s in enumerate(ls) if needle in s)
    extra.append(dict(source=pin(p),line=line,statement=ls[line-1]))
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='ADDENDUM_AFTER_DEV_BEFORE_ACCEPTANCE',new_theorems=2,new_definitions=0,private_theorems=1,
    correction='A consulta preliminar chamou rankOne de ContinuousLinearMap.rankOne; a fonte lida registra namespace InnerProductSpace. Primeiro DEV expôs esse erro e o nome incorreto star_algebraMap; corrigidos para InnerProductSpace.rankOne e algebraMap_star_comm, sem reimplementar fornecedores. Duas tentativas seguintes ajustaram reescrita escalar redundante e redução de lambda. Final DEV010047rc0, mesmo limite de heartbeats.',
    extra_providers=extra,final_dev=pin(R/'dev_modular_fixed_vectors/20260915_010047_543598/run.json'),
    scope='Same original S/F domains, Delta_nu, T_nu and U_t. Explicit fixed pair implies Delta_nu*x=x and T_nu*x=(1/2)*x. Private adapter uses existing damped CFC intertwiner and rankOne; zero vector handled separately before cancelling inner(x,x). No assumption of cyclicity or new imaginary group. Second theorem consumes delta30 and supplies exact average square. No full implementator equality, Q compatibility or trace yet. Negative omits the adjoint fixed equality, so the supplied theorem remains a function and fails the required result type.')
put(R/'ADENDO_FICHA_VETORES_FIXOS_MODULARES.json',json.dumps(d,ensure_ascii=False,indent=2))
put(R/'ADENDO_FICHA_VETORES_FIXOS_MODULARES.md','[OPEN — complemento após DEV e antes do aceite]\n\n'+json.dumps(d,ensure_ascii=False,indent=2)+'\n')
