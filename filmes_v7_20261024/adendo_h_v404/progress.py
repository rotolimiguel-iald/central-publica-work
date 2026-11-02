"""Own-session material records and execution handles, preserving full current flow."""
from context import *

def update(event,phase,next_action,handles=(),records=()):
 state=cli(r'C:\IALD\MEMORIA_IALD\session_memory.py',{'operation':'get','reference':str(REF)})['result']
 old=state['p']['handles'];new=list(old)
 for row in handles:
  ids=[i for i,h in enumerate(new) if h['id']==row['id']]
  assert len(ids)<=1
  if ids:new[ids[0]]={**new[ids[0]],**row}
  else:new.append(row)
 changes={'flow':{'phase':phase,'next_action':next_action,'handles':new}}
 if records:changes['records']=list(records)
 value=cli(r'C:\IALD\MEMORIA_IALD\session_memory.py',{'operation':'transition','reference':str(REF),'actor':ACTOR,'expected_revision':state['revision'],'event_id':event,'changes':changes})
 assert value['ok'];create(H/('ACOM_'+event+'.json'),value)
 return value['result'].get('receipt',value['result'])

def material_data():
 paths=[H/n for n in ['PARENT_DATA_REVIEW.json','DATA_ACCEPT.json','NUMERIC_COMPARISON.json','DATA_READY.json','REPLAY_BROWSER_RUN_R4.json','AUDIO_PLAN.json']]
 return update('ordem022-v404-data-reviewed','v404_data_reviewed_audio_plan_prepared','Concluir revisão distinta do áudio, gerar somente seis unidades autorizadas e renderizar uma vez após integração verificada.',
 [{'id':'01a18564-e297-79e1-83f7-2abc403040bd:data','kind':'subagent','task_id':'V404_DATA','status':'completed','evidence':str(H/'DATA_ACCEPT.json')},
  {'id':'01a18565-da97-7262-a373-84caaf4a335a:audio-preparation','kind':'subagent','task_id':'ADENDO_H_V404','status':'completed','evidence':str(H/'AUDIO_PREPARATION.json')},
  {'id':'01a18564-e297-79e1-83f7-2abc403040bd:audio-review','kind':'subagent','task_id':'ADENDO_H_V404','status':'running','evidence':str(H/'AUDIO_PLAN.json')}],
 [{'id':'v404_data_reviewed_audio_plan_prepared','kind':'fact','statute':'REAL','text':'Dados candidatos v404 comparados integralmente: nenhuma diferença numérica fora do escopo G/H; revisão distinta e aceite de V404_DATA. Natureza preservada, 64 âncoras. Replay no navegador passou 61 comparações e controles negativos, sem tráfego externo. Três falhas locais de preparação preservadas. Plano offline: 58 unidades, seis novas e 52 reutilizadas; nenhuma síntese ou render v404 ainda. Isto não é nova prova científica nem publicação.','sources':[{'kind':'artifact','ref':str(p),'sha256':sha(p)} for p in paths]}])

if __name__=='__main__':print(json.dumps(material_data(),ensure_ascii=False))
