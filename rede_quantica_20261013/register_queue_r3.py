"""Record admitted next units, preserving earlier science and diary bytes."""
import datetime as dt
import json
import sys
from diary_r1 import ROOT,OUT,WORK,WHO,CLI,claim,new,pin
from register_progress_r2 import run,src

D=OUT/'orchestration_r3'
BASE=ROOT/'Chatgpt/IALD_ORQUESTRACAO_20260923'
EVENT='fock-independent-units-queued-r3-20261013'
ENTRY=D/'DIARY_ENTRY_R3.json'
CAT=D/'HANDOFF_R3.json'
MAP=D/'MAP_ENTRY_R3.json'
SNAP=OUT/'diary_events'/(EVENT+'_DIARIO_SNAPSHOT.md')
MEM=OUT/'diary_events'/(EVENT+'_RECEIPT.json')

def prepare():
 claim();units=[]
 for provider in ('MIMO','DEEPSEEK'):
  reqpath=D/f'REQUEST_{provider}_R3_1.json';req=json.loads(reqpath.read_text(encoding='utf-8'))
  recpath=D/f'SUBMIT_{provider}_R3_1.json';rec=json.loads(recpath.read_text(encoding='utf-8'))
  response=rec['response']
  # Transport returns the coordination job; do not confuse it with an execution.
  job=response.get('job',response)
  jid=job.get('id',job.get('job_id'))
  assert jid and rec['exit_code']==0 and job.get('request_id')==req['request_id']
  units.append({'provider':provider.lower(),'request_id':req['request_id'],'job_id':jid,'stage_at_submit':job['stage'],'lemma_id':req['execution_constraints']['lemma_id'],'payload':pin(reqpath),'sources':pin(D/f'SOURCES_{provider}_R3_1.json'),'preview':pin(D/f'PREVIEW_{provider}_R3_1.json'),'submission_receipt':pin(recpath),'execution_constraints':req['execution_constraints']})
 catalog={'unit':'F1.REDE','reference':'slot-followup-F1REDE-stage753-20261013','status':'TWO_INDEPENDENT_UNITS_REGISTERED','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'units':units,'dependency':pin(OUT/'RESULTADO_ETAPA_R2.json'),'scope_review':pin(D/'SCOPE_REVIEW_R3_1.json'),'scientific_memory_check':pin(D/'SCIENTIFIC_MEMORY_CHECK_R3.json'),'worker':'Existing official coordinator only; no direct execution by originating session. MiMo fresh audited process after prior process drained.','do_not_repeat':['R2 completed construction','old unsubmitted R3 drafts retained in DRAFT_SUPERSESSION_R3_1.json','terminal/uncertain units'],'kimi_takesaki':'Unchanged; specific authorization pending.','remaining_open':'Exponential vectors/totality and Gamma(J) are requests, not completed proofs; Weyl/CCR, local algebras, Tomita/KMS, full certificates, Maxwell and represented Takesaki core remain open.'}
 new(CAT,catalog)
 new(BASE/'state/handoffs'/'F1REDE_stage753_independent_units_R3_20261013.json',catalog)
 for u in units:
  new(BASE/'state/session_requests'/f'{u["request_id"]}_submission.json',u)
 body='''[REAL — preparação e inscrição na fila] Depois da entrega R2, o levantamento no Nós Vivo, no mapa e na matriz do contrato confirmou duas frentes independentes: (A1) vetores exponenciais, produto interno e totalidade no Fock concreto; (B) segunda quantização antiunitária de J, com conjugação no setor zero, involução, vácuo e inclusão de H1. Revisão independente de escopo preservou as dependências e recusou atalhos circulares.

[REAL — protocolo] A primeira prévia MiMo foi recusada localmente pelo limite de 24.000 caracteres, antes de qualquer chamada ou registro na fila. O rascunho DeepSeek original também não foi submetido. Os dois rascunhos completos permanecem imutáveis, marcados como substituídos; versões compactas de 20.586 e 23.422 caracteres conservaram literalmente as tarefas, com fontes e linhas pinadas. As novas prévias selecionaram os executores requeridos e receberam a geração científica v392 verificada, com recuperação parcial declarada.

[REAL — fila, não resultado científico] Dois pedidos foram registrados uma única vez pela entrada oficial, com max_calls=1, branch_id=F1.REDE e executor fixado. A coordenação existente conduz as transições; nenhum resultado de provedor é afirmado nesta etapa. Os IDs, payloads, hashes, previews e recibos estão no HANDOFF_R3.json. MiMo trata A1; DeepSeek trata B. A preparação não repete a R2 nem o pedido DeepSeek anterior concluído. Kimi/Takesaki conserva sua pendência específica.

[OPEN] Weyl/CCR, álgebras locais e suas propriedades modulares, certificado Fock completo, Maxwell, núcleo de Takesaki ligado à representação e localização 4D não são fechados pela inscrição desses pedidos. Respostas serão DECLARADO até verificação local. Próxima ação: recuperar os resultados pelos mesmos IDs, compilar candidatos em sandbox e revisar sua matemática. Diário, Atlas, índice e aviso recebem somente esta etapa operacional sob reivindicação755; nenhuma alteração no kernel, um.py, Bancada, dados observados ou gate.'''
 new(ENTRY,{'id':EVENT,'unit':'F1.REDE','title':'13/10/2026 — duas construções independentes encaminhadas à orquestração','body':body,'sources':[str(CAT),str(D/'SOURCE_AND_SCOPE_IDENTITY_R3_1.json'),str(D/'DRAFT_SUPERSESSION_R3_1.json'),str(D/'SCOPE_REVIEW_R3_1.json')],'link_surfaces':True,'surface_summary':'[REAL — fila] Após R2, A1 exponenciais/totalidade e B Gamma(J) preparados, pinados e registrados em duas unidades independentes (MiMo/DeepSeek). Prévia v392 verificada; resultados científicos ainda OPEN/DECLARADO. Recuperar mesmos IDs no HANDOFF_R3.json; Kimi/Takesaki inalterado.'})
 new(MAP,{'tipo':'ROTA','rota_id':'formal.f1_rede.fock_exponentials_and_antiunitary_queue','dominio':'KERNEL_FORMAL','titulo':'Próximas unidades independentes: exponenciais no Fock e segunda quantização antiunitária','pergunta':'Quais construções úteis podem prosseguir independentemente após a cinemática R2?','dados':['R2 Fock concreto e Jcandidate construídos','Memória científica v392 verificada'],'metodo':'Levantamento, revisão de dependências, seleção de trechos pinados, preview e inscrição idempotente na fila existente.','resultado':'Dois pedidos registrados; nenhuma prova nova é reivindicada nesta etapa.','veredito':'QUEUED_TWO_INDEPENDENT_UNITS__CONSTRUCTIONS_OPEN','estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,'defeito':'Os resultados matemáticos dos dois pedidos ainda precisam de construção, compilação e revisão; certificado completo continua OPEN.','nao_refazer':'R2 e pedidos terminais/incertos. Os rascunhos R3 maiores não foram enviados e foram substituídos explicitamente.','proximo_passo':'Recuperar resultados pelos request_id/job_id do catálogo; conferir matemática e compilar somente em sandbox.','onde':str(D),'artefatos':[str(CAT),str(MEM)],'refs':['formal.f1_rede.concrete_bosonic_kinematics'],'nota':'Nenhuma mudança de produção ou gate. Kimi/Takesaki mantém aprovação específica pendente.'})
 print(json.dumps({'catalog':pin(CAT),'units':[{'provider':u['provider'],'job_id':u['job_id']} for u in units]},ensure_ascii=False))

def main():
 mode=sys.argv[1]
 if mode=='prepare':prepare()
 elif mode=='diary':run('DIARY_QUEUE_R3_RUN.json',[str(WORK/'diary_r1.py'),str(ENTRY)])
 elif mode=='map':
  claim();run('MAP_QUEUE_R3.json',[r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(MAP),'--quem',WHO+' / F1.REDE'])
 elif mode=='board':
  claim();run('BOARD_QUEUE_R3.json',[CLI,'avancar','F1.REDE','--quem',WHO,'--status','EM_CURSO','--evidencia',str(CAT),str(SNAP),str(MEM),'--nota','R3: duas unidades independentes na fila, MiMo exponenciais/totalidade e DeepSeek GammaJ. Pins/previews/IDs no HANDOFF_R3. R2 preservada; diario sob755; nenhuma prova nova alegada.'])
 elif mode=='acom':
  claim();cat=json.loads(CAT.read_text(encoding='utf-8'))
  handles=[{'id':'f1-rede-deepseek','request_id':'701e5bcb-cb47-4706-a9be-9b5ed10f4a35','job_id':'4d57aa1f-2d40-43df-8f82-f16593d899a2','execution_task_id':'69dd527b-cf74-4b4d-9a15-0c51b8d191bd','provider':'deepseek','status':'completed_no_repeat','unit':'F1.REDE'}]
  for u in cat['units']:handles.append({'id':u['lemma_id'],'request_id':u['request_id'],'job_id':u['job_id'],'provider':u['provider'],'status':'queued','unit':'F1.REDE'})
  run('ACOM_QUEUE_R3.json',[r'C:\IALD\MEMORIA_IALD\session_memory.py'],{'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),'expected_revision':5,'event_id':'f1-rede-independent-fock-units-queued-r3-20261013','actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':'fock-independent-units-queued-r3','kind':'fact','statute':'REAL','text':'Duas novas unidades independentes registradas na fila: exponenciais/totalidade (MiMo) e segunda quantização antiunitária (DeepSeek). Pins e previews com memória v392 verificados. Primeira prévia MiMo recusou tamanho local antes de envio; novos rascunhos compactos substituem os não submetidos. Nenhum resultado científico novo alegado; recuperar mesmos IDs. Diário e três remissões acrescentados com backups sob755. Kimi/Takesaki permanece pendente.','sources':[src(CAT),src(MEM),src(SNAP)]}],'flow':{'phase':'independent_fock_research_units_queued','next_action':'Coordenador oficial executa as duas unidades da F1.REDE. Recuperar pelos mesmos IDs; respostas DECLARADO até compilação/revisão locais. Não repetir R2, rascunhos substituídos ou chamadas incertas; Kimi/Takesaki intocado.','handles':handles}}})
 elif mode=='release':run('RELEASE_QUEUE_R3.json',[CLI,'liberar','F1.REDE','--quem',WHO,'--nota','Duas unidades independentes registradas na fila; diario, quadro, mapa e ACOM atualizados. Coordenador oficial conduz execução; construções completas continuam OPEN.'])
 else:raise ValueError(mode)

if __name__=='__main__':main()
