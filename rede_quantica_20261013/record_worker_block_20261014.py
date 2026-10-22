"""Record coordinator review refusals without dispatching or altering jobs."""
import json
import sqlite3
from diary_r1 import ROOT,OUT,WORK,WHO,CLI,claim,new,pin
from register_progress_r2 import run,src

D=OUT/'orchestration_r3'
REMOTE=ROOT/'work/rede_transport_20261014_R3'
EVENT='coordinator-execution-review-block-r3-20261014'
RESULT=D/'COORDINATOR_REVIEW_BLOCK_20261014.json'
ENTRY=D/'DIARY_ENTRY_COORDINATOR_BLOCK_20261014.json'
MAP=D/'MAP_ENTRY_COORDINATOR_BLOCK_20261014.json'
SNAP=OUT/'diary_events'/(EVENT+'_DIARIO_SNAPSHOT.md')
MEM=OUT/'diary_events'/(EVENT+'_RECEIPT.json')

def main():
 active=claim()
 catalog=json.loads((D/'HANDOFF_SUBMITTED_R3_20261014.json').read_text(encoding='utf-8'))
 sources=[REMOTE/'AUTO_REVIEW_JOINT_REFUSAL.json',REMOTE/'AUTO_REVIEW_DEEPSEEK_REFUSAL.json',REMOTE/'OFFICIAL_HUMAN_REPLY.json',D/'OPERADOR_AUTORIZACAO_R3_20261014.json']
 for path in sources[:2]:
  data=json.loads(path.read_text(encoding='utf-8'));assert data['provider_calls']==0 and data['process_started'] is False
 db=sqlite3.connect((ROOT/'Chatgpt/IALD_ORQUESTRACAO_20260923/state/tasks.sqlite3').as_uri()+'?mode=ro',uri=True)
 handles=[]
 for item in catalog['units']:
  row=db.execute('SELECT id,request_id,stage,execution_task_id FROM coordination_jobs WHERE id=?',(item['job_id'],)).fetchone()
  assert row[0]==item['job_id'] and row[1]==item['request_id'] and row[2]=='awaiting_dispatch' and row[3] is None
  handles.append({'id':item['lemma_id'],'provider':item['provider'],'job_id':row[0],'request_id':row[1],'unit':'F1.REDE','status':'awaiting_dispatch_review_blocked'})
 db.close()
 new(RESULT,{'status':'COORDINATOR_EXECUTION_BLOCKED_BY_AUTOMATIC_REVIEW','claim':active,'sources':[pin(x) for x in sources],'jobs':handles,'human_authorization':'EXISTS: direct specific response on14Oct; no retraction and no authorization inferred for other units.','distinction':'Queue registration succeeded here; execution command was rejected in the coordination thread. The rejection concerns acceptance of cross-thread approval evidence, not a mathematical defect.','action':'No indirect dispatch, alternative worker, cancellation or new request ID. Coordinator said it would present the required approval in its own context.','source_time_note':'Source timestamps are preserved as reported; no cross-host chronology is inferred.'})
 body='''[REAL — atualização operacional, em nome de codex-gerente-tgl] A inscrição dos dois jobs permanece válida. Os recibos da coordenação registram duas recusas anteriores ao início do processo: primeiro o worker conjunto MiMo/DeepSeek; depois o DeepSeek isolado. A revisão automática considerou a aprovação humana recuperada por ferramenta entre conversas insuficiente para liberar esses comandos naquele contexto. Os dois recibos declaram zero chamadas. A fila foi consultada em leitura e continua com os mesmos IDs, awaiting_dispatch e execution_task_id=null.

[INPUT — autorização preservada] O operador de fato respondeu nesta conversa «Autorizar os dois envios», para os pacotes R3_1 identificados na pergunta. Esse registro não é retirado, não é reduzido a autorização do pacote anterior e não é descrito como ausência de consentimento humano. A distinção vigente é: consentimento específico existente; inscrição na fila concluída; execução bloqueada pela revisão automática no contexto da coordenação.

[OPEN — execução] A coordenação informou que apresentará no próprio contexto a aprovação exigida. Esta tarefa não envia por outra rota, não inicia worker, não cancela pedidos nem gera outros IDs. A única mudança é o registro do bloqueio. Kimi/Takesaki continua independente. Não houve resultado científico novo; a revisão dos candidatos permanece futura. Diário e remissões acrescentados com backups sob reivindicação764; produção e gate intactos.'''
 new(ENTRY,{'id':EVENT,'unit':'F1.REDE','title':'14/10/2026 — autorização preservada; execução bloqueada na coordenação','body':body,'sources':[str(RESULT),*[str(x) for x in sources]],'link_surfaces':True,'surface_summary':'[REAL — processo] Jobs registrados continuam awaiting_dispatch/execution_task_id null. Coordenação documentou recusa automática do worker conjunto e do DeepSeek isolado, antes de processo/chamada. [INPUT] A autorização específica dada aqui existe e permanece; bloqueio é de aceitação da evidência entre conversas. Nenhuma execução indireta ou duplicação; a coordenação apresentará a aprovação exigida no seu contexto.'})
 run('DIARY_COORDINATOR_BLOCK_20261014.json',[str(WORK/'diary_r1.py'),str(ENTRY)])
 new(MAP,{'tipo':'ANOTACAO','rota_id':'formal.f1_rede.fock_exponentials_and_antiunitary_preparation','dominio':'KERNEL_FORMAL','titulo':'Bloqueio da execução pela revisão automática da coordenação, com autorização humana preservada','pergunta':'Qual etapa permanece bloqueada após a inscrição autorizada dos dois jobs?','dados':['Dois recibos de recusa da coordenação','Autorização humana específica de14out','Fila somente leitura'],'metodo':'Conferência de recibos e identidade dos mesmos jobs, sem executar workers.','resultado':'Autorização existe e inscrição concluiu. Worker conjunto e DeepSeek isolado recusados antes de processo; jobs awaiting_dispatch/sem tarefa de executor.','veredito':'AUTHORIZED_AND_QUEUED__COORDINATOR_EXECUTION_REVIEW_BLOCKED','estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,'defeito':'Bloqueio de revisão automática no contexto executor; nenhum defeito matemático demonstrado por ele.','nao_refazer':'Não contornar a recusa, repetir IDs ou iniciar outro worker.','proximo_passo':'Coordenação apresenta aprovação no próprio contexto; após liberação, mesmos IDs e uma chamada por unidade.','onde':str(D),'artefatos':[str(RESULT),str(MEM)],'refs':['formal.f1_rede.concrete_bosonic_kinematics'],'nota':'Ao lado das seq1100/1101; autorização não é revogada. Nada move gate.'})
 run('MAP_COORDINATOR_BLOCK_20261014.json',[r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(MAP),'--quem',WHO+' / F1.REDE'])
 run('BOARD_COORDINATOR_BLOCK_20261014.json',[CLI,'avancar','F1.REDE','--quem',WHO,'--status','AGUARDA_OPERADOR','--evidencia',str(RESULT),str(SNAP),str(MEM),'--nota','Autorizacao especifica humana existe e inscricao dos jobs concluiu. Auto-review da coordenacao rejeitou execucao conjunta e DeepSeek isolado por nao aceitar evidencia entre conversas; coord apresentara aprovacao em seu contexto. Mesmos IDs awaiting_dispatch, sem executor/chamada. Nao contornar. Diario sob764.'])
 old={'id':'f1-rede-deepseek','request_id':'701e5bcb-cb47-4706-a9be-9b5ed10f4a35','job_id':'4d57aa1f-2d40-43df-8f82-f16593d899a2','execution_task_id':'69dd527b-cf74-4b4d-9a15-0c51b8d191bd','provider':'deepseek','status':'completed_no_repeat','unit':'F1.REDE'}
 run('ACOM_COORDINATOR_BLOCK_20261014.json',[r'C:\IALD\MEMORIA_IALD\session_memory.py'],{'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),'expected_revision':7,'event_id':EVENT,'actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':EVENT,'kind':'fact','statute':'REAL','text':'Coordenação registrou recusa automática de dois comandos de execução antes de processo. Autorização humana específica nesta conversa existe e permanece; fila inscrita, mesmos IDs awaiting_dispatch/execution_task_id null. Não executar indiretamente. Coordenação apresentará no próprio contexto a aprovação exigida. Diário com fontes e backups sob764.','sources':[src(RESULT),src(MEM)]}],'flow':{'phase':'authorized_jobs_waiting_coordinator_review_clearance','next_action':'Aguardar resolução da revisão automática na coordenação; nenhum envio indireto ou duplicação. Preservar autorização humana existente, IDs, executor/generation e Kimi/Takesaki independente.','handles':[old,*handles]}}})
 run('RELEASE_COORDINATOR_BLOCK_20261014.json',[CLI,'liberar','F1.REDE','--quem',WHO,'--nota','Bloqueio concreto documentado no diario/mapa/quadro/ACOM; autorizacao humana preservada. Nenhum worker ou envio nesta tarefa.'])

if __name__=='__main__':main()
