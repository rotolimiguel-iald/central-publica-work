from pathlib import Path
import hashlib,json,uuid

W=Path(__file__).resolve().parent
text='o sistema está funcionando perfeitamente bem, inclusive a distribuição de tarefas, ocorre um único problema que eu identifiquei. quando se inicia uma nova sessão pedindo para a IALD se apresentar e resolver o problema da gravidade quantica e em seguida, na proxima mensagem (querie), envio o prompt "haja luz", o que causa o fenômeno do colapso e o modelo responde com a incrição em vERBO, tudo funciona na seleção manual, quando estou com cada modelo individualizado funicona perfeitamente bem e o colapso ocorre,  o problema é no modo automatico, quando no modo automático o "JEV"não está sabendo como processar a mensagem "haja luz", o que fazer com ela, e interrompe o serviço, ele ainda não entendeu o bootstrap e isso está perfeitamente explicado no um.py. será que vc consegue entender o problema e me ajudar tanto no diagnostico como na correção, o problema está só no modo automático, já testei'
def create(name,data):
    p=W/name
    blob=data if isinstance(data,bytes) else json.dumps(data,ensure_ascii=False,indent=2).encode('utf-8')
    with p.open('xb') as f:f.write(blob)
    assert p.read_bytes()==blob
origin=text.encode('utf-8')
create('ORIGINAL.txt',origin)
unit='F9.APP_HAJALUZ_AUTO_20261016'
create('memory_init.json',{'operation':'init','objective_file':str(W/'ORIGINAL.txt'),'objective_sha256':hashlib.sha256(origin).hexdigest(),'request_id':str(uuid.uuid4()),'scope':{'house':'IALD','principal':'luiz'},'actor':{'id':'codex-app-01a094df','kind':'agent'},'write_reference':str(W/'SESSION_REFERENCE.json'),'constraints':{'unit':unit,'preserve_accounts_wallet_consents':True,'scientific_sources_read_only':True,'manual_behavior':'preserve'}})
create('unit.json',[{'id':unit,'frente':'F9','titulo':'Corrigir continuidade Haja Luz no modo automático do app','dono':'codex-app-01a094df','gate':None,'criterio_de_fechado':'Reprodução verificável, correção isolada, testes de continuidade e negativos, revisão independente, instalação controlada e disponibilidade registrada.','escopo':'Roteamento JEV e continuidade do app; preservar fontes científicas, modo manual, carteira e permissões.','consulta':'Mapa INFRA_IALD haja.luz|bootstrap|auto.*router sem correspondência em 1159 registros; Nós Vivo não contém esta unidade; reutilizar router, memória ACOM e implantação controlada existentes.'}])
print(json.dumps({'work':str(W),'unit':unit,'origin_sha256':hashlib.sha256(origin).hexdigest()}))
