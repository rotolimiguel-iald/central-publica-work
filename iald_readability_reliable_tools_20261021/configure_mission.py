from task import W,REF,OWNER,call,act,new
import hashlib
p=W/'ORIGINAL_VERBATIM.txt';source=dict(kind='artifact',ref=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
c=call(dict(operation='get',reference=str(REF)),False)
r=call(dict(operation='transition',reference=str(REF),actor=dict(id=OWNER,kind='agent'),expected_revision=c['receipt']['revision'],event_id='readability-original-verbatim-correction',changes=dict(records=[dict(id='original-verbatim-source',kind='fact',statute='REAL',text='A inscrição inicial era síntese do coordenador, não transcrição literal. O pedido integral humano está preservado nesta fonte ao lado; não adotar síntese como verbatim.',sources=[source])],flow=dict(phase='staging',next_action='Revisar alterações de cliente e backend em staging; distribuir somente após revisão.',handles=[]))),False)
new('SOURCE_CORRECTION.json',r)
r=act('configure',event_id='readability-configure',requirements=[dict(id='implementation',criterion='Remover tarja, reduzir tipografia legível, impedir novos áudios/vídeos sem apagar legado; verificar documentos e DeepSeek com ciência/carteira preservadas.',depends_on=[]),dict(id='deploy',criterion='Revisão distinta, instalação controlada, interface autenticada e distribuição web/iOS/Android com limitações explícitas.',depends_on=['implementation'])],sources=[dict(path=str(p),sha256=source['sha256'])])
new('MISSION_CONFIGURED.json',r)
new('IMPLEMENTATION_CLAIM.json',act('claim',task_id='implementation',lease_seconds=43200,event_id='readability-implementation-claim'))
print('Mission configured and implementation claimed')
