import task,json,hashlib,subprocess
W=task.W
unit=[{'id':task.UNIT,'frente':'F9','titulo':'Ampliar mídia MiMo com admissão multimodal e custos JEV','dono':task.OWNER,'gate':None,'criterio_de_fechado':'Capacidade ampliada revisada; memória preservada; custos e contexto controlados; clientes e distribuição verificados.','escopo':'Mídia app MiMo/JEV; preservar ciência, contas, carteira e consentimentos.','consulta':'Reutiliza F9.MIMO26_UPGRADE_20261020/FINAL_REVIEW e código implantado; Nós Vivo não indexa unidade anterior; Atlas adendo39050 consultado, sem reconstruir ciência.'}]
task.new('unit.json',unit)
source={'path':str(W/'ORIGINAL.txt'),'sha256':hashlib.sha256((W/'ORIGINAL.txt').read_bytes()).hexdigest()}
r=task.act('configure',requirements=[{'id':'implementation','criterion':'Ampliar mídia até transporte oficial, contar mídia por modalidade, preservar memória e carteira, validar limites com controles negativos.','depends_on':[]},{'id':'deploy','criterion':'Revisão distinta, instalação controlada, testes proporcionais e distribuição coordenada web/iOS/Android.','depends_on':['implementation']}],sources=[source],event_id='media-capacity-configure')
task.new('mission_configured.json',r)
r=task.act('claim',task_id='implementation',lease_seconds=43200,event_id='media-capacity-implementation-claim');task.new('implementation_claim.json',r)
print(json.dumps({'reference':str(task.REF),'revision':r['receipt']['revision']}))
