from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent; K=R/'k'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists()
    q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
names=['V350PositiveRootIntertwining.lean','V350ResolventSquareRoot.lean','BoundedGraphOperator.lean','V351RegularDomainCut.lean','V350ScalarGNSStrongContinuity.lean','V351PerturbedWeightNorm.lean','V350BoundedDualValues.lean']
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='OPEN__Q_CONSUMER_AND_MINIMAL_PUBLIC_API',providers=[pin(K/'TGLExt'/n) for n in names],prior_fiche=pin(R/'REAPROVEITAMENTO_A1B_BALANCO_DOS_CORTES.json'),dev_identity=pin(R/'dev_double_cut_balance/20260915_023442_551908/run.json'))
body='''[OPEN] Consumidor Q e alcance mínimo da entrega do balanço

O balanço concreto passou DEV no snapshot indicado, com um teorema público, nove privados e zero definições. Ainda não é aceite independente33.

Para evitar que o consumidor seguinte rederive auxiliares privados, reforçar o MESMO teorema público com Commute T C_epsilon e Commute T D_eta, além da identidade limitada. A primeira vem da comutação T com pi(R) já provada, do auxiliar closed_representation_cfc já existente e de regularInverseGeneratorCutoff_cfc; a segunda pela conjugação original J T J^-1=1-T. Não adicionar outro gerador, outro estado, outra função pública ou premissa de tracialidade.

Consulta independente somente leitura localizou os fornecedores abaixo e refinou o próximo passo: escrever x=sqrt(T)u e B_nu x=sqrt(1-T)u no grafo original. Transportar comutações por positive_sqrt_intertwines para obter igualdade de formas Re<y,C_epsilon q_eta y>=Re<x,p_epsilon D_eta x>. Retirar um corte de cada vez pela convergência forte da sequência 1/(n+1), com 0<=p_n,q_n<=1, e comparar os supremos em ENNReal. Não converter para toReal nem pressupor finitude. Não é necessário construir limites das raízes dos cortes p/q, ou provar de novo que pi(sqrt B) é sqrt(pi B): a identidade de norma original, map_star/map_mul e sqrt_mul_sqrt_self bastam para identificar as formas.

Q e a tracialidade permanecem OPEN. Este é aproveitamento para um consumidor ainda não composto em Lean. O gate não mudou. A consulta independente não compilou nem certificou a entrega33.
'''
body+='\n'+d['timestamp']+'\n\n'+ '\n'.join(x['path'] for x in d['providers'])+'\n'
put(R/'ADENDO_CONSUMIDOR_Q_DO_BALANCO.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'ADENDO_CONSUMIDOR_Q_DO_BALANCO.md',body.encode('utf8'))
print(json.dumps(d,ensure_ascii=False))
