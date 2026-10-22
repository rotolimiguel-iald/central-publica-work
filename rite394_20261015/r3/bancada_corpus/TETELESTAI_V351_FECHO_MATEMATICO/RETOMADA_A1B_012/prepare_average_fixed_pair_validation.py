from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent;K=R/'k'
def put(p,s):
 assert p.is_relative_to(R) and not p.exists()
 b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
for base in ['run_average_polar_right_replay.py','audit_average_polar_right.py','validate_average_polar_right.py']:
 s=(R/base).read_text(encoding='utf8')
 for a,b in [('average_polar_right','average_fixed_pair'),('V351AveragePolarRight','V351AverageFixedPair'),('AveragePolarRight','AverageFixedPair'),('BadAverageMembershipIsSelfAdjoint','BadFixedPairRightPremiseRemoved'),('AUDITORIA_MINORANTES_FINITOS_A1B','AUDITORIA_MEDIA_ACAO_DIREITA_A1B'),('AVERAGE_POLAR_RIGHT','AVERAGE_FIXED_PAIR')]:s=s.replace(a,b)
 if base.startswith('audit_'):
  s=s.replace('private_theorems=3','private_theorems=0')
  s=s.replace('average_fixed_pair_constructed=True, fixed_tomita_vectors_constructed=False','average_fixed_pair_constructed=True, fixed_tomita_vectors_constructed=True')
  s=s.replace("put(R/'AUDITORIA_MEDIA_ACAO_DIREITA_A1B.json'","put(R/'AUDITORIA_MEDIA_PAR_FIXO_A1B.json'")
 put(R/base.replace('average_polar_right','average_fixed_pair'),s)
names=['scalarWeightStar_fixed_pair_of_polarRight','regularAverage_square_fixed_pair']
put(K/'TGLExt/AuditA1AverageFixedPair.lean','import TGLExt.V351AverageFixedPair\n'+''.join('#check TGLV350.Regular.'+n+'\n#print axioms TGLV350.Regular.'+n+'\n' for n in names))
put(R/'probes/BadFixedPairRightPremiseRemoved.lean','''import TGLExt.V351AverageFixedPair
open TGLExt TGLV350.Regular
example (P : SiteProfile) (A : scalarWeightStarCore P) (hstar : star A = A) :
    scalarClosedTomita P ⟨scalarWeightStarEmbedding P A,
      scalarWeightStar_mem_closedTomitaDomain P A⟩ = scalarWeightStarEmbedding P A ∧
    ∃ hF : scalarWeightStarEmbedding P A ∈ scalarTomitaAdjointDomain P,
      scalarTomitaAdjoint P ⟨scalarWeightStarEmbedding P A,hF⟩ =
        scalarWeightStarEmbedding P A :=
  scalarWeightStar_fixed_pair_of_polarRight P A hstar
''')
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='ADDENDUM_AFTER_DEV_BEFORE_ACCEPTANCE',new_theorems=2,new_definitions=0,private_theorems=0,
 correction='Primeiro DEV falhou antes da elaboração por objeto antigo V350ScalarRightAdjointPair ausente. O fornecedor e seus imports foram reproduzidos de fonte em K com Lake, rc0, três objetos novos/alterados, nenhum fonte modificado. Tentativas seguintes expuseram timeouts de elaboração em existência inferida e reescritas amplas sobre B/inscrições GNS; foram substituídas por existência com tipo completo e composição explícita de igualdades dos mesmos fornecedores. Sem aumento de heartbeats, novos helpers, domínios ou hipóteses. Campo de pertinência à estrela usa star_mem\u0027 existente. Final DEV004340rc0 limpo.',
 provider_replay=pin(R/'replay_fixed_pair_provider/20260915_003318_050435/run.json'),
 final_dev=pin(R/'dev_average_fixed_pair/20260915_004340_982817/run.json'),
 scope='First theorem explicitly requires star A=A AND actual polar-right membership. Second constructs A with exact value star(e_delta)*e_delta and proves both antecedents. Simultaneous fixed S/F statements include actual domains, no unrestricted domains. Does not assert e_delta selfadjoint, vector nonzero, totality, U identity, Q or trace. Negative removes only polar-right premise from the first theorem.')
put(R/'ADENDO_FICHA_MEDIA_PAR_FIXO.json',json.dumps(d,ensure_ascii=False,indent=2))
put(R/'ADENDO_FICHA_MEDIA_PAR_FIXO.md','[OPEN — complemento após DEV e antes do aceite]\n\n'+json.dumps(d,ensure_ascii=False,indent=2)+'\n')

