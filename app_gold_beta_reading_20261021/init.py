from task import *
src=W/'OPERADOR.txt'
new('INIT_REQUEST.json',dict(operation='init',objective_file=str(src),objective_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),request_id=str(uuid.uuid4()),scope=dict(house='IALD',principal='luiz'),actor=dict(id=OWNER,kind='agent'),write_reference=str(REF)))
new('INIT_RECEIPT.json',call(json.loads((W/'INIT_REQUEST.json').read_bytes()),False))
new('CONFIGURE.json',act('configure',event_id='gold-beta-configure',requirements=[dict(id='ui',criterion='Restaurar glifo beta dourado animado e reduzir prosa para14px com verificação visual mobile.',depends_on=[]),dict(id='delivery',criterion='Revisar e disponibilizar web/iOS/Android afetados com matriz e memória.',depends_on=['ui'])],sources=[dict(path=str(src),sha256=hashlib.sha256(src.read_bytes()).hexdigest())]))
new('CLAIM_UI.json',act('claim',task_id='ui',lease_seconds=43200,event_id='gold-beta-claim-ui'))
new('UNIT.json',[dict(id=UNIT,frente='F9',titulo='Glifo beta dourado e leitura compacta no app',dono=OWNER,status='PROPOSTA',criterio_de_fechado='Glifo dourado,prosa menor e canais afetados atualizados com evidência.',evidencia=[str(src)])])
print(REF)
