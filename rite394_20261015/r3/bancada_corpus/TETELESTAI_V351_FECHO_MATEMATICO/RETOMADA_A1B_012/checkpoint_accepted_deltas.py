from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent
stamp=datetime.datetime.now().astimezone().isoformat();suffix=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b,memory=False):
 assert p.is_relative_to(R) and b
 if p.exists():
  assert memory
  old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+suffix);bak.write_bytes(old);assert bak.read_bytes()==old and len(b)>=len(old)
 t=p.with_name(p.name+'.tmp_'+suffix);t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
rows=[]
for key in ['CORE','ABSORPTION','FOURIER','GRAPH']:
 p=R/('RECIBO_DELTA_'+key+'.json');rows.append(dict(key=key,receipt=pin(p),contents=json.loads(p.read_text(encoding='utf8'))))
record=dict(timestamp=stamp,sealed=rows,author_affiliation=pin(R/'AUDITORIA_AFILIACAO_REGULAR_A1B.json'),pending_reviews=['spectral graph','scalar multiplier calculus','regular imaginary powers','regular generator affiliation'],next='six-mode reuse fiche, dual scaling of the same regular generator, then inverse-generator trace',full_trace_constructed=False,gate_changed=False)
p=R/('CHECKPOINT_ACCEPTED_'+suffix+'.json');put(p,json.dumps(record,ensure_ascii=False,indent=2).encode('utf8'))
text=f'''\n\n## Adendo {stamp} — quatro deltas entregues; afiliação compilada

Corrige o estado transitório de 19:35 sem apagar seu registro: core5, absorção6, Fourier3 e grafo15 já receberam revisão independente, aceite, manifesto, recibo e ENTREGA no túnel. Arquivos efetivos dos pareceres: revisao_core/REVIEW_A1_CORE_FINAL, revisao_absorcao/REVIEW_A1_ABSORCAO_FINAL, revisao_fourier/REVIEW_A1_FOURIER_FINAL e revisao_grafo/REVIEW_A1_GRAFO_POSITIVO_FINAL. Conferir recibos neste snapshot, não nomes presumidos.

O grafo espectral3, o cálculo funcional5, as potências4 e a afiliação3 passaram no autor (lake rc0, axiomas no trio, controles adulterados recusados); suas revisões independentes continuam pendentes neste checkpoint. V351RegularGeneratorAffiliation prova R∈N e preservação do mesmo grafo por todo B∈N′, sem nova definição de operador. Nenhum build autoral permanece em execução; todas as sessões antigas foram consumidas. Não repeti-las.

deliver_reviewed_delta.py e deliver_reviewed_delta_v2.py estão selados; não editar. Para novo delta usar v2 com configuração nova em delivery_configs, após leitura efetiva do parecer. Não repetir chaves já entregues. Próxima ponte: escala dual θ_s(h)=e^(-s)h do MESMO gerador, seguida pela construção do traço de Pedersen–Takesaki. O traço completo permanece aberto. Sem mudanças de gate, D1 ou canônico.

Snapshot: {p.name}. Os scripts checkpoint_retornada.py e checkpoint_chain_progress.py não devem ser repetidos: contêm retratos antigos. Novas atualizações por append, com backup imediato de bytes.
'''
md=R/'MEMORIA_RETOMADA_A1B_012.md';put(md,md.read_bytes()+text.encode('utf8'),True)
jp=R/'MEMORIA_RETOMADA_A1B_012.json';d=json.loads(jp.read_text(encoding='utf8'));d.setdefault('append_only_checkpoints',[]).append(pin(p));put(jp,json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'),True)
print(json.dumps(dict(checkpoint=pin(p),memory=pin(md)),ensure_ascii=False))
