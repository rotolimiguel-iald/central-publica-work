from task import *
p=project()
handles=p['projection']['flow']['handles']
source=W/'release/IOS38_STARTED.json'
handles.append(dict(id='ios38-cloud',kind='build',status='running',ref=str(source),url=json.loads(source.read_bytes())['url']))
r=call(dict(operation='transition',reference=str(REF),actor=dict(id=OWNER,kind='agent'),expected_revision=p['receipt']['revision'],event_id='attachments-installed-ios38-running',changes=dict(records=[dict(id='attachments-installed-initial',kind='fact',statute='REAL',text='Onze arquivos instalados e verificados, ciência preservada. Android33 assinado/publicado e download autenticado conferido. Teste live recuperou pedido após reload e beta animou/encerrou, mas reserva de custo recusou antes do executor; patch complementar em preparação. Nenhum retry do pedido recusado.',sources=[dict(kind='artifact',ref=str(W/'release/CHECK_INSTALLED_R1.json'),sha256=hashlib.sha256((W/'release/CHECK_INSTALLED_R1.json').read_bytes()).hexdigest())])],flow=dict(phase='validation',next_action='Revisar e aplicar correção da reserva visual; novo teste live; acompanhar iOS38 já iniciado e distribuir ambos grupos.',handles=handles))),False)
new('PROGRESS_MEMORY_RECEIPT.json',r)
print('Recorded progress')
