from pathlib import Path
import hashlib,json,subprocess,uuid
W=Path(__file__).resolve().parent
old=Path(r'C:\IALD\Central de Patentes\work\iald_v394_20261019\task.py').read_text(encoding='utf-8')
helper=old[:old.index('def init():')].replace('F9.APP_V394_20261019','F9.APP_JEV_KIMI_20261020')
(W/'task.py').write_text(helper,encoding='utf-8')
exec(compile(helper,str(W/'task.py'),'exec'))
source='Eu pedi ao KIMI que melhorasse o Jev e a memória integrado, ele criou uma série de coisas e os comandos e os implantou (ou está implantando e falta do ajuste final). O fato é que a IALD no app não está funcionado perfeitamente bem como vc pode ver das imagens abaixo. Corrija, por favor, e implemente o que o Kimi fez'.encode()
new('ORIGINAL.txt',source)
d=call({'operation':'init','objective_file':str(W/'ORIGINAL.txt'),'objective_sha256':hashlib.sha256(source).hexdigest(),'request_id':str(uuid.uuid4()),'scope':{'house':'IALD','principal':'luiz'},'actor':{'id':OWNER,'kind':'agent'},'write_reference':str(REF),'constraints':{'unit':UNIT,'no_retry_uncertain_requests':True,'preserve_science_accounts_wallet_consents':True}},False)
new('init_receipt.json',d)
req=[{'id':'diagnose','criterion':'Localizar falha real e inventariar alterações Kimi por evidência, sem reenvio dos pedidos existentes.','depends_on':[]},{'id':'repair','criterion':'Preparar integração e correção reproduzível com testes e integridade das guardas de memória, direitos e idempotência.','depends_on':['diagnose']},{'id':'deploy','criterion':'Revisão real independente, instalação controlada com backups e verificação efetiva; matriz de clientes e registro final.','depends_on':['repair']}]
new('mission_configured.json',act('configure',requirements=req,sources=[{'path':str(W/'ORIGINAL.txt'),'sha256':hashlib.sha256(source).hexdigest()}],event_id='jev-kimi-configure'))
new('unit.json',[{'id':UNIT,'frente':'F9','titulo':'Correção do app e integração JEV/memória do Kimi','dono':OWNER,'gate':None,'criterio_de_fechado':'Causa reproduzida, integração revisada, implantação verificada e matriz real.','escopo':'App/JEV/memória operacional; ciência readonly; sem retry de pedidos incertos.','consulta':'Reutilizar entrega v394 e memória de atividade; diagnosticar mudanças Kimi de20out.'}])
for args in [['nova','--json',str(W/'unit.json'),'--quem',OWNER],['reivindicar',UNIT,'--quem',OWNER,'--horas','12']]:
 p=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py',*args],capture_output=True);assert p.returncode==0,p.stdout.decode()+p.stderr.decode()
new('diagnose_claim.json',act('claim',task_id='diagnose',lease_seconds=43200,event_id='jev-kimi-diagnose-claim'))
print(json.dumps({'reference':str(REF),'receipt':project()['receipt']}))
