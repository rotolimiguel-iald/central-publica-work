from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
    assert p.is_relative_to(R) and not p.exists(),p
    b=s.encode('utf8');q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
for base in ['run_tracial_extension_replay.py','audit_tracial_extension.py','validate_tracial_extension.py']:
    s=(R/base).read_text(encoding='utf8')
    for a,b in [('tracial_extension','finite_minorants'),('V351InverseLimitTracialExtension','V351InverseLimitFiniteMinorants'),('InverseLimitTracialExtension','InverseLimitFiniteMinorants'),('BadTracialCorePremiseRemoved','BadFiniteMinorantsTraceRemoved'),('AUDITORIA_SEMIFINITUDE_PESO_LIMITE_A1B','AUDITORIA_EXTENSAO_TRACIAL_A1B'),('TRACIAL_EXTENSION','FINITE_MINORANTS')]:s=s.replace(a,b)
    if base.startswith('audit_'):
        s=s.replace('len(targets)==4','len(targets)==2').replace("for t in targets)==4","for t in targets)==2")
        s=s.replace('new_theorems=4','new_theorems=2').replace('private_theorems=2','private_theorems=4')
        s=s.replace('traciality_reduced_to_existing_core=True, core_traciality_proved=False','finite_contractions_constructed=True, finite_minorants_conditional_on_traciality=True, core_traciality_proved=False')
        s=s.replace("put(R/'AUDITORIA_EXTENSAO_TRACIAL_A1B.json'","put(R/'AUDITORIA_MINORANTES_FINITOS_A1B.json'")
    put(R/base.replace('tracial_extension','finite_minorants'),s)
names=['scalarInverseLimitWeight_finite_contractions','scalarInverseLimitWeight_finite_minorants']
put(K/'TGLExt/AuditA1InverseLimitFiniteMinorants.lean','import TGLExt.V351InverseLimitFiniteMinorants\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadFiniteMinorantsTraceRemoved.lean','''import TGLExt.V351InverseLimitFiniteMinorants
open TGLExt TGLV350.Regular TGLV351
open scoped ENNReal
example (P : SiteProfile) : ∀ X : PositiveCoreInput P,
    scalarInverseLimitWeight P X =
      ⨆ (Y : PositiveCoreInput P) (_ : Y ≤ X)
        (_ : scalarInverseLimitWeight P Y < ⊤), scalarInverseLimitWeight P Y :=
  scalarInverseLimitWeight_finite_minorants P
''')
specs=[('TGLExt/V350RegularApproximation.lean','regularAverage_tendsto_identity'),('TGLExt/V350DualSemifiniteIdeal.lean','regularAverage_hasFiniteDualSquare'),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Order.lean','CStarAlgebra.star_mul_le_algebraMap_norm_sq')]
providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:theorem|lemma) '+re.escape(name)+r'(?:\s|\()',s,re.M);assert m,name
    end=s.index(' :=',m.start());providers.append(dict(name=name,source=pin(p),line=s[:m.start()].count('\n')+1,statement=s[m.start():end]))
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHE_ADDENDUM_AFTER_DEV_BEFORE_ACCEPTANCE',providers=providers,correction='A ficha previu uso direto de CFC, sem helper. A primeira execução expôs falhas de síntese das instâncias no Lp concreto. Foram necessários QUATRO helpers privados genéricos: bound quadrático de norma (API CStar), compressão, escala real da unidade e fonte de quadrado CFC dentro de N. Este último reproduz apenas a adaptação de tipos já vista no helper privado de AllPositiveWeightOrder (não exportável), não outra raiz nem outro cálculo espectral. Nenhum deles é contado entre os DOIS teoremas públicos. Operações reais ficam genéricas antes da instanciação; a tentativa de converter tudo a escala complexa gerou ciclos RCLike/SMul e foi abandonada. Não aumenta orçamento de heartbeats. Todos os DEV rc1 preservados, final000736rc0 limpo.',old_adapter=pin(K/'TGLExt/V351AllPositiveWeightOrder.lean'),exact_consumer=pin(K/'TGLExt/V351RegularCoreTraceContract.lean'),scope='The finite-positive-minorant field still requires htr explicitly. E_n are actual finite-square contractions; no top-toReal or hidden traciality. No contract inhabitant, no change to trace gate. Finiteness proved by htr twice, norm bound, monotonicity and homogeneity; no positive-minorant condition imposed on nu.')
put(R/'ADENDO_FICHA_MINORANTES_FINITOS.json',json.dumps(d,ensure_ascii=False,indent=2))
put(R/'ADENDO_FICHA_MINORANTES_FINITOS.md','[OPEN — complemento após DEV e antes do aceite]\n\n'+json.dumps(d,ensure_ascii=False,indent=2)+'\n')
