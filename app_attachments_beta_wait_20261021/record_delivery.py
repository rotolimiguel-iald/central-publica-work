from task import *
p=project(); handles=p['projection']['flow']['handles']
source=W/'delivery.json'; ios=W/'release/IOS38_DISTRIBUTION.json'
for h in handles:
    if h['id']=='ios38-cloud':h.update(status='completed',ref=str(ios),sha256=hashlib.sha256(ios.read_bytes()).hexdigest())
r=call(dict(operation='transition',reference=str(REF),actor=dict(id=OWNER,kind='agent'),expected_revision=p['receipt']['revision'],event_id='attachments-final-live-and-distribution',changes=dict(records=[dict(id='attachments-delivered-technical',kind='fact',statute='REAL',text='Correção12arquivos/63testes. Teste final imagem1.59MB+PDF emmodoautomático respondeu vermelho|azul|ANEXO-73 e persistiu após reload durante/depois. Beta3.6s encerrou. iOS38 ambosgruposEmtestes; Android33APK autenticadohashigual. Ciência5pinos intactos; GooglePlay e instalaçãofísica nãoverificados. Falhas anteriores preservadas.',sources=[dict(kind='artifact',ref=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest())])],flow=dict(phase='final_review',next_action='Aplicar memória operacional revisada e encerrar com revisão independente da entrega.',handles=handles))),False)
new('DELIVERY_MEMORY_RECEIPT.json',r)
p=project();t=next(t for t in p['projection']['active'] if t['id']=='delivery')
r=act('submit',task_id='delivery',lease_id=t['lease']['id'],event_id='attachments-delivery-submit',evidence=[dict(path=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest())])
new('DELIVERY_SUBMIT.json',r)
print('Submitted delivery; cloud handle terminal')
