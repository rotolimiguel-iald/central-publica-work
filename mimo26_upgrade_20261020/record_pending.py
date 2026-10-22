import json,hashlib
from pathlib import Path
import task
W=Path(__file__).resolve().parent
current=task.call({'operation':'get','reference':str(task.REF)},False)
sources=[]
for name in ['deployment.json','INSTALLED_VERIFICATION.json','mobile_stage/IOS34_DISTRIBUTION.json','LIVE_AUTHORIZATION_PENDING.json']:
 p=W/name;sources.append({'kind':'artifact','ref':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
changes={'records':[{'id':'mimo26-installed-distributed-awaiting-live-consents','kind':'pending','statute':'REAL','text':'21 arquivos instalados e conferidos; ciência v394 preservada. iOS4.1(34) processado e Em testes nos dois grupos, participação do operador conferida; instalação física não verificada. Android4.1(29) APK/AAB assinados/auditados. Teste real bloqueado pela revisão automática, aguardando autorizações específicas MiMo v2 e JEV v3; nenhum pedido enviado ou consentimento aceito nesta entrega. Não concluir deploy nem repetir envios incertos.','sources':sources}], 'flow':{'phase':'awaiting_specific_live_test_authorization','next_action':'Obter respostas humanas pendentes; conferir própria missão/preflight; aceitar avisos autorizados e executar cada teste sintético uma única vez; concluir revisão e disponibilidade.'}}
r=task.call({'operation':'transition','reference':str(task.REF),'actor':{'id':task.OWNER,'kind':'agent'},'expected_revision':current['receipt']['revision'],'event_id':'mimo26-installed-distributed-awaiting-live-consents','changes':changes},False)
task.new('PROGRESS_MEMORY_RECEIPT.json',r)
print(json.dumps(r,ensure_ascii=False))
