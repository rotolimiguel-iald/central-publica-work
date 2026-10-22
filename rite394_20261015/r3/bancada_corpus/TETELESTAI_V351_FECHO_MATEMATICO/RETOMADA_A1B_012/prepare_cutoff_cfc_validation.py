from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parent;K=R/'k'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,s):
 assert not p.exists() and p.is_relative_to(R),p
 b=s.encode('utf8');q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='CLARIFICATION_AFTER_DEV_BEFORE_ACCEPTANCE',source=pin(K/'TGLExt/V350AntiunitaryPositiveConjugation.lean'),name='hilbertPositiveSqrt',line=15,reason='Existing generic Hilbert CFC.sqrt wrapper fixes canonical instances before specialization. Direct CFC.sqrt on the specialized Lp type caused an instance diamond in first DEV. The target uses the EXISTING wrapper, whose definition is literally CFC.sqrt, and an explicit generic real/complex CFC equality. No new square root or root hypothesis. GeneralExpectationCP was only a reuse model on a different algebra.',consult=pin(R/'revisao_consulta_acao_direita/CONSULTA_CORTE_CFC_EQUACAO_GRAFO.md'))
put(R/'ADENDO_FICHA_CFC_RAIZ_HILBERT.json',json.dumps(d,ensure_ascii=False,indent=2))
put(R/'ADENDO_FICHA_CFC_RAIZ_HILBERT.md','[REAL — esclarecimento de fornecedor após DEV, antes da aceitação]\n\n'+d['timestamp']+'\n\n'+d['reason']+'\n\nA ficha anterior cobre o alvo da raiz original e os conversores CFC; este adendo fixa o empacotamento já existente de V350AntiunitaryPositiveConjugation.lean:15. A consulta confirma a rota pelo grafo e é registrada separadamente.\n')
s=(K/'TGLExt/V351InverseCutoffCFC.lean').read_text(encoding='utf8')
names=re.findall(r'^(?:def|theorem) (\w+)',s,re.M);assert len(names)==7
put(K/'TGLExt/AuditA1CutoffCFC.lean','import TGLExt.V351InverseCutoffCFC\nset_option pp.universes true\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadCutoffCFCMirror.lean',"""import TGLExt.V351InverseCutoffCFC
open TGLExt TGLV350.Regular
example (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    regularInverseGeneratorCutoff P ε =
      cfc (inverseCutoffFunction ε) (1-regularSpectralResolvent P) := by
  exact regularInverseGeneratorCutoff_cfc P ε hε
""")
for old,new in [('run_sine_resolvent_replay.py','run_cutoff_cfc_replay.py'),('audit_sine_resolvent.py','audit_cutoff_cfc.py'),('validate_sine_resolvent.py','validate_cutoff_cfc.py')]:
 t=(R/old).read_text(encoding='utf8')
 for a,b in [('sine_resolvent','cutoff_cfc'),('V351SineResolventApprox','V351InverseCutoffCFC'),('AuditA1SineResolvent','AuditA1CutoffCFC'),('SINE_RESOLVENT','CUTOFF_CFC'),('BadSineResolventLimit','BadCutoffCFCMirror'),('AUDITORIA_APROXIMANTES_SENO_A1B','AUDITORIA_CFC_CORTES_A1B'),('AUDITORIA_ALGEBRA_ACAO_DIREITA_A1B','AUDITORIA_APROXIMANTES_SENO_A1B')]:t=t.replace(a,b)
 t=t.replace("len(targets)==11 and sum(t['kind']=='theorem' for t in targets)==9","len(targets)==7 and sum(t['kind']=='theorem' for t in targets)==6")
 t=t.replace('new_theorems=9, new_definitions=2, private_theorems=6, private_definitions=1','new_theorems=6, new_definitions=1, private_theorems=2, private_definitions=0')
 t=t.replace('new_theorems=9,new_definitions=2,private_theorems=6,private_definitions=1','new_theorems=6,new_definitions=1,private_theorems=2,private_definitions=0')
 t=t.replace('actual_resolvent_right_action_proved=True, approximating_family_constructed=True','actual_cutoff_cfc_identified=True, actual_cutoff_root_right_action_proved=True')
 put(R/new,t)
print(names)

