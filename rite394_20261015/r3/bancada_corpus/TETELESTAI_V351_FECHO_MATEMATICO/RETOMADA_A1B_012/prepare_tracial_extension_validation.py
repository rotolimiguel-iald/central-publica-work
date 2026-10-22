from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
    assert p.is_relative_to(R) and not p.exists(),p
    b=s.encode('utf8');q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
old='inverse_limit_semifinite';new='tracial_extension'
for base in ['run_'+old+'_replay.py','audit_'+old+'.py','validate_'+old+'.py']:
    s=(R/base).read_text(encoding='utf8')
    for a,b in [(old,new),('V351InverseLimitSemifiniteness','V351InverseLimitTracialExtension'),('InverseLimitSemifiniteness','InverseLimitTracialExtension'),('BadLimitSemifiniteInfiniteCut','BadTracialCorePremiseRemoved'),('AUDITORIA_CORTE_DOMINIO_A1B','AUDITORIA_SEMIFINITUDE_PESO_LIMITE_A1B'),('AUDITORIA_SEMIFINITUDE_PESO_LIMITE_A1B.json\',json.dumps','AUDITORIA_EXTENSAO_TRACIAL_A1B.json\',json.dumps'),('INVERSE_LIMIT_SEMIFINITE','TRACIAL_EXTENSION')]:s=s.replace(a,b)
    if base.startswith('audit_'):
        s=s.replace('len(targets)==3','len(targets)==4').replace("for t in targets)==3","for t in targets)==4")
        s=s.replace('new_theorems=3','new_theorems=4').replace('private_theorems=1','private_theorems=2')
        s=s.replace('constructed_limit_weight_usual_semifinite=True, actual_cutoff_root_right_action_proved=True','traciality_reduced_to_existing_core=True, core_traciality_proved=False')
        # The output path is new; prerequisites still point to the old sealed audit.
        s=s.replace("put(R/'AUDITORIA_SEMIFINITUDE_PESO_LIMITE_A1B.json'","put(R/'AUDITORIA_EXTENSAO_TRACIAL_A1B.json'")
    put(R/base.replace(old,new),s)
names=['scalarInverseLimitWeight_square_le_of_strong','scalarInverseLimitWeight_right_average_le','scalarInverseLimitWeight_sandwich_le','scalarInverseLimitWeight_tracial_iff_core']
put(K/'TGLExt/AuditA1InverseLimitTracialExtension.lean','import TGLExt.V351InverseLimitTracialExtension\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadTracialCorePremiseRemoved.lean','''import TGLExt.V351InverseLimitTracialExtension
open TGLExt TGLV350.Regular TGLV351
example (P : SiteProfile) :
    ∀ A : (regularCoreAlgebra P).toStarSubalgebra,
      scalarInverseLimitWeight P (positiveSquare P A) =
        scalarInverseLimitWeight P (positiveSquare P (star A)) :=
  scalarInverseLimitWeight_tracial_iff_core P
''')
specs=[('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_sqrt_right'),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Order.lean','norm_le_one_iff_of_nonneg')]
providers=[]
for path,name in specs:
    p=K/path;s=p.read_text(encoding='utf8');m=re.search(r'^(?:theorem|lemma) '+re.escape(name)+r'\b',s,re.M);assert m,name
    end=s.index(' :=',m.start());providers.append(dict(name=name,source=pin(p),line=s[:m.start()].count('\n')+1,statement=s[m.start():end]))
p=K/'TGLExt/V351RegularCoreTraceContract.lean';lines=p.read_text(encoding='utf8').splitlines();line=next(i+1 for i,s in enumerate(lines) if s.startswith('  tracial :'))
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHE_ADDENDUM_AFTER_FIRST_DEV_BEFORE_ACCEPTANCE',providers=providers,consumer=dict(source=pin(p),line=line,statement=lines[line-1]),first_dev='dev_tracial_extension/20260914_235244_987632/run.json',scope='Exact missing membership supplier and generic contraction order adapter; no new root. First six-mode scan failed only at TOE/acervo by sandbox read denial. Preserved error logs. Second scan with authorized read escalation succeeded in all modes and generated the pre-code fiche. Initial tracial consumer line59 corrected to measured line58 here; no older record erased.')
put(R/'ADENDO_FICHA_EXTENSAO_TRACIAL.json',json.dumps(d,ensure_ascii=False,indent=2))
put(R/'ADENDO_FICHA_EXTENSAO_TRACIAL.md','[OPEN — complemento de fornecedores, após o primeiro DEV, antes da aceitação]\n\n'+json.dumps(d,ensure_ascii=False,indent=2)+'\n')
