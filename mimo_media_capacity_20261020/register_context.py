import task,json,hashlib
from pathlib import Path
W=task.W
old=Path(r'C:\IALD\Central de Patentes\work\mimo26_upgrade_20261020')
d=json.loads((old/'SCIENCE_BASELINE.json').read_bytes())
for x in d['files']:
 raw=Path(x['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==x['sha256']
task.new('SCIENCE_BASELINE.json',d)
task.new('REUSE.json',{'previous_delivery':str(old/'FINAL_REVIEW.json'),'previous_sha256':hashlib.sha256((old/'FINAL_REVIEW.json').read_bytes()).hexdigest(),'route':'infra.app.mimo26_upgrade_20261020','route_status':'EXAMINADA','nos_vivo':'Previous unit absent from graph; explicit primary receipt reused','scope':'Extend media capacity; no science execution or rebuild'})
route={'tipo':'ROTA','rota_id':'infra.app.mimo_media_capacity_20261020','dominio':'INFRA_IALD','titulo':'Mídia MiMo ampliada com memória TGL e custos JEV preservados','pergunta':'Como admitir mídia maior sem gastar base64 como tokens ou reduzir ciência?','dados':['Runtime MiMo validado','Documentação oficial áudio/vídeo','Recibos anteriores'], 'metodo':'Referências privadas autenticadas, limites do transporte e estimativa multimodal, staging/revisão/testes/distribuição','resultado':'Pedido registrado e ciência baseline conferida','veredito':'IN_PROGRESS','estatuto':'REAL','status':'EM_CURSO','olhou_dados':False,'nao_refazer':'Reutilizar integração MiMo, FFprobe e carteira; não executar um.py','proximo_passo':'Concluir contrato de anexos e implementações isoladas','onde':str(W),'artefatos':[str(W/'REUSE.json')],'refs':[]}
task.new('ROUTE_START.json',route)
p=task.call({'operation':'get','reference':str(task.REF)},False)
ids={'media-backend':'01a15aa9-fb97-79b2-9391-db6af761eea1','media-budget':'01a15aaa-d85e-7d01-bf9b-89747fc482d3','media-client':'01a15604-76c6-7110-9a73-2dc692d95018','media-review':'01a15607-da9a-76e2-a12f-7ce9a5ab4a54'}
r=task.call({'operation':'transition','reference':str(task.REF),'actor':{'id':task.OWNER,'kind':'agent'},'expected_revision':p['receipt']['revision'],'event_id':'media-capacity-workers-started','changes':{'flow':{'phase':'implementation_staging','next_action':'Integrar contrato privado de anexos, orçamento multimodal e cliente; revisão distinta antes de instalar.','handles':[{'id':k,'external_id':v,'provider':'codex-subagent','status':'running'} for k,v in ids.items()]}}},False)
task.new('STAGING_MEMORY.json',r)
print(json.dumps({'revision':r['revision'],'science':'v394'}))
