from task import *
src=W/'OPERADOR.txt'
if not (W/'INIT_REQUEST.json').exists(): new('INIT_REQUEST.json',dict(operation='init',objective_file=str(src),objective_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),request_id=str(uuid.uuid4()),scope=dict(house='IALD',principal='luiz'),actor=dict(id=OWNER,kind='agent'),write_reference=str(REF)))
new('INIT_RECEIPT.json',call(json.loads((W/'INIT_REQUEST.json').read_bytes()),False))
new('CONFIGURE_RECEIPT.json',act('configure',event_id='attachments-beta-configure',requirements=[dict(id='repair',criterion='Diagnosticar e corrigir anexos de imagem e documento com testes, preservando permissões e ciência.',depends_on=[]),dict(id='waiting',criterion='Indicador beta TGL animado durante espera real, acessível, termina em conclusão ou erro.',depends_on=[]),dict(id='delivery',criterion='Integração revisada, instalação e disponibilidade web/mobile verificadas com limites explícitos.',depends_on=['repair','waiting'])],sources=[dict(path=str(src),sha256=hashlib.sha256(src.read_bytes()).hexdigest())]))
new('UNIT.json',[dict(id=UNIT,frente='F9',titulo='Corrigir anexos e espera lúdica beta TGL no app',dono=OWNER,status='PROPOSTA',criterio_de_fechado='Correções revisadas, testadas e disponibilizadas nas superfícies afetadas.',evidencia=[str(src)])])
print('Own reference initialized:',REF)
