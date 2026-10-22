"""Accept reviewed Q transport and require safe legacy migration before D."""
import json
from mission_io import WORK,REFERENCE,ACTOR,call,pin,project,save
from advance import action
review=WORK/'review_queue/Q_REVIEW_R2.json'
assert json.loads(review.read_bytes())['status']=='PASS_WITH_LEGACY_MIGRATION_REQUIREMENT'
p,_=project()
if next(t for t in p['projection']['active']+p['projection']['settled'] if t['id']=='Q')['status']=='review_pending':
    r,_=action('accept','Q',{'review_evidence':[pin(review)],'note':'Transporte Q R2 revisado; continuidade de pedidos legados será coberta por Q2 explícita antes de V/D.'})
    save(WORK/'review_queue/Q_ACCEPTED_R2.json',r)
p,_=project()
known=p['projection']['active']+p['projection']['settled']
if not any(t['id']=='Q2' for t in known):
    call('mission_cli.py',{'operation':'extend','reference':str(REFERENCE),'actor':ACTOR,
        'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
        'event_id':'organism-Q2-legacy-migration-r1','requirements':[{'id':'Q2','depends_on':['Q'],'criterion':
            'CLI local privilegiado de migração explícita de pedidos legados nunca despachados: UUID, versão/digest de linha e revisão/hash ACOM esperados, lock/CAS, intenção durável, retomada idempotente só local. Preservar IDs, contexto, prompts, restrições, geração, suplemento e estágio. Recusar tentativas, threads, filhos/handles externos, incerteza, encerrados e premissas alteradas. Testar concorrência/crash/recusas; não expor como ferramenta de modelo, não migrar pedidos reais, não iniciar worker/provedor.'}],
        'reason':'Dois jobs legados ainda pendentes em leitura real; bloquear avanço sem oferecer migração retiraria capacidade existente. Reparar a continuidade faz parte da integração autorizada.',
        'sources':[pin(review),pin(WORK/'OPERADOR_VERBATIM.txt')]},'extend_Q2')
p,_=project();v=next(t for t in p['projection']['active'] if t['id']=='V')
if 'Q2' not in v['criterion']:
    action('amend','V',{'criterion':v['criterion']+' Exigir também Q2 satisfeita, preservando continuidade legada sem despacho ou migração implícita.',
        'reason':'Integrar migração explícita e testada antes da ativação, preservando pedidos antigos.',
        'sources':[pin(review)]})
print('Q aceita; Q2 adicionada à revisão final.')
