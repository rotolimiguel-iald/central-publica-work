"""Record the specifically approved submissions; keep prior refusal intact."""
import datetime as dt
import json
import sys
from diary_r1 import ROOT,OUT,WORK,WHO,CLI,claim,new,pin
from register_progress_r2 import run,src

D=OUT/'orchestration_r3'
BASE=ROOT/'Chatgpt/IALD_ORQUESTRACAO_20260923'
EVENT='fock-two-submissions-authorized-r3-20261014'
AUTH=D/'OPERADOR_AUTORIZACAO_R3_20261014.json'
CAT=D/'HANDOFF_SUBMITTED_R3_20261014.json'
ENTRY=D/'DIARY_ENTRY_SUBMITTED_R3_20261014.json'
MAP=D/'MAP_ENTRY_SUBMITTED_R3_20261014.json'
SNAP=OUT/'diary_events'/(EVENT+'_DIARIO_SNAPSHOT.md')
MEM=OUT/'diary_events'/(EVENT+'_RECEIPT.json')

def prepare():
 active=claim();units=[]
 for provider in ('MIMO','DEEPSEEK'):
  path=D/f'REQUEST_{provider}_R3_1.json';req=json.loads(path.read_text(encoding='utf-8'))
  receipt=D/f'SUBMIT_{provider}_R3_1.json';rec=json.loads(receipt.read_text(encoding='utf-8'));job=rec['response']
  assert rec['exit_code']==0 and job['request_id']==req['request_id']
  assert job['execution_constraints']==req['execution_constraints']
  assert job['prompt']==req['prompt']
  memory=job['canonical_memory'].get('receipt',job['canonical_memory'])
  assert memory['generation']==req['execution_constraints']['memory_generation']
  units.append({'provider':provider.lower(),'request_id':req['request_id'],'job_id':job['id'],'stage_at_submit':job['stage'],'execution_task_id_at_submit':job['execution_task_id'],'lemma_id':req['execution_constraints']['lemma_id'],'payload':pin(path),'submission_receipt':pin(receipt),'sources':pin(D/f'SOURCES_{provider}_R3_1.json'),'fresh_preview':pin(D/f'PREVIEW_{provider}_APPROVED_20261014.json'),'execution_constraints':req['execution_constraints'],'received_memory_generation':memory['generation']})
 catalog={'unit':'F1.REDE','status':'AUTHORIZED_AND_REGISTERED_WITH_OFFICIAL_COORDINATOR','user_date':'2026-10-14','registered_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'claim':active,'authorization':pin(AUTH),'preflight':pin(D/'PREFLIGHT_APPROVED_20261014.json'),'units':units,'supersedes_pending_state_only':pin(D/'HANDOFF_PENDING_APPROVAL_R3.json'),'execution_owner':'Existing official coordinator; originating session has only submitted. MiMo uses fresh audited process after prior process drained.','honest_scope':'Job registration is not a provider response or a scientific result. Mathematical constructions remain OPEN; provider outputs DECLARADO until local verification.','preserved':['Prior automatic-review refusal and unsubmitted drafts','All R2 evidence and science','Kimi/Takesaki specific approval pending','Production um.py/kernel/Bancada/data/gate']}
 new(CAT,catalog)
 new(BASE/'state/handoffs/F1REDE_R3_SUBMITTED_20261014.json',catalog)
 for u in units:new(BASE/'state/session_requests'/f'{u["request_id"]}_submission.json',{'authorization':pin(AUTH),**u})
 body='''[INPUT — operador, resposta direta de 14/10/2026] À pergunta que identificava os pacotes MiMo (20.586 caracteres + memória canônica de cerca de909KB) e DeepSeek (23.422 caracteres + cerca de646KB), o operador respondeu, verbatim: «Autorizar os dois envios». Pergunta e resposta integrais estão custodiadas com hash. Essa resposta resolve a pendência específica registrada em13/10; a recusa automática anterior permanece intacta como história.

[REAL — verificação e submissão] Sob a reivindicação758, relidos os hashes dos mesmos payloads e suas fontes, conferida a ausência prévia dos IDs na fila, consultado o Nós Vivo e repetidas as prévias locais. A memória científica continua CURRENT/v392 e os dois pedidos receberam a geração fixada. Nenhum conteúdo nem execution_constraints foi alterado. Ambos foram registrados uma única vez no cliente oficial: MiMo para vetores exponenciais/produto interno/totalidade; DeepSeek para Gamma(J), involução, vácuo e inclusão H1.

[REAL — estado observado] Os recibos de registro dizem awaiting_dispatch, execution_task_id=null. Isso confirma a inscrição na fila; não confirma chamada ao provedor nem resposta científica. A coordenação existente conduz a execução. IDs e recibos completos estão no HANDOFF_SUBMITTED_R3_20261014.json, que sucede somente o estado pendente do catálogo anterior. Não há segundo trabalhador, mensagem a outra sessão, repetição da R2 ou nova autorização inferida para Kimi/Takesaki.

[OPEN] As duas construções continuam abertas até recepção, compilação em sandbox e revisão matemática. Weyl/CCR, álgebras locais, Tomita/KMS, certificados completos e Maxwell conservam seus estatutos. Próxima ação: recuperar os resultados pelos mesmos request_id/job_id; nunca repetir uma execução incerta. Diário, Atlas, índice e aviso recebem este registro com backup imediato de bytes. Nenhum arquivo de produção, dado observado ou gate é alterado.'''
 new(ENTRY,{'id':EVENT,'unit':'F1.REDE','title':'14/10/2026 — autorização específica recebida; dois pedidos inscritos na fila','body':body,'sources':[str(AUTH),str(CAT),str(D/'PREFLIGHT_APPROVED_20261014.json'),*[u['submission_receipt']['path'] for u in units]],'link_surfaces':True,'surface_summary':'[INPUT] Operador autorizou expressamente os dois pacotes em14out. [REAL — fila] Mesmos payloads/IDs e memória v392 conferidos; MiMo A1 exponenciais/totalidade e DeepSeek Gamma(J) registrados uma vez, ambos awaiting_dispatch no recibo. Pendência específica destes dois resolvida; Kimi/Takesaki inalterado. Resultados científicos ainda OPEN.'})
 new(MAP,{'tipo':'ANOTACAO','rota_id':'formal.f1_rede.fock_exponentials_and_antiunitary_preparation','dominio':'KERNEL_FORMAL','titulo':'Autorização humana específica e inscrição dos dois pedidos da F1.REDE','pergunta':'A pendência específica dos envios MiMo/DeepSeek foi resolvida?','dados':['Resposta humana direta de14/10','Payloads e IDs preservados','Memória v392 CURRENT'],'metodo':'Custódia da resposta, preflight de hashes/IDs, novas prévias locais e submissão única pela fila oficial.','resultado':'Dois jobs criados com awaiting_dispatch e sem execution_task_id no recibo. Aprovação específica dos dois pacotes registrada; nenhuma resposta científica alegada.','veredito':'SPECIFIC_APPROVAL_RECEIVED__TWO_JOBS_REGISTERED','estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,'defeito':'Registro na fila não significa execução remota ou construção concluída.','nao_refazer':'Preservar R2 e os mesmos IDs; nunca reenviar unidade terminal/incerta.','proximo_passo':'Coordenador oficial despacha; recuperar resultados pelos IDs e verificar em sandbox.','onde':str(D),'artefatos':[str(AUTH),str(CAT),str(MEM)],'refs':['formal.f1_rede.concrete_bosonic_kinematics'],'nota':'Ao lado da seq1100. Resolução específica dos dois pedidos; Kimi/Takesaki permanece separado. Nada move gate.'})
 print(json.dumps({'catalog':pin(CAT),'jobs':[{'provider':u['provider'],'job_id':u['job_id'],'stage':u['stage_at_submit']} for u in units]},ensure_ascii=False))

def main():
 mode=sys.argv[1]
 if mode=='prepare':prepare()
 elif mode=='diary':run('DIARY_APPROVED_R3_20261014.json',[str(WORK/'diary_r1.py'),str(ENTRY)])
 elif mode=='map':
  claim();run('MAP_APPROVED_R3_20261014.json',[r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(MAP),'--quem',WHO+' / F1.REDE'])
 elif mode=='board':
  claim();run('BOARD_APPROVED_R3_20261014.json',[CLI,'avancar','F1.REDE','--quem',WHO,'--status','EM_CURSO','--evidencia',str(CAT),str(AUTH),str(SNAP),str(MEM),'--nota','Autorizacao humana especifica dos dois envios recebida em14out; payloads/IDs preservados. MiMo e DeepSeek registrados uma vez na fila, awaiting_dispatch. Diario e remissoes sob758; nenhuma resposta cientifica alegada.'])
 elif mode=='acom':
  claim();cat=json.loads(CAT.read_text(encoding='utf-8'))
  handles=[{'id':'f1-rede-deepseek','request_id':'701e5bcb-cb47-4706-a9be-9b5ed10f4a35','job_id':'4d57aa1f-2d40-43df-8f82-f16593d899a2','execution_task_id':'69dd527b-cf74-4b4d-9a15-0c51b8d191bd','provider':'deepseek','status':'completed_no_repeat','unit':'F1.REDE'}]
  handles.extend({'id':u['lemma_id'],'request_id':u['request_id'],'job_id':u['job_id'],'provider':u['provider'],'status':u['stage_at_submit'],'unit':'F1.REDE'} for u in cat['units'])
  run('ACOM_APPROVED_R3_20261014.json',[r'C:\IALD\MEMORIA_IALD\session_memory.py'],{'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),'expected_revision':6,'event_id':'f1-rede-specific-consent-and-two-submissions-r3-20261014','actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':'specific-consent-r3-20261014','kind':'decision','statute':'INPUT','text':'Resposta humana direta à pergunta específica dos pacotes MiMo A1 e DeepSeek Gamma(J): Autorizar os dois envios. Resolve a pendência anterior somente desses dois payloads.','sources':[src(AUTH)]},{'id':'two-submissions-r3-20261014','kind':'fact','statute':'REAL','text':'Mesmos payloads/IDs, fontes e memória v392 conferidos; dois jobs inscritos uma única vez pela fila oficial. Recibos awaiting_dispatch/execution_task_id null. Inscrição não afirma execução remota ou prova nova. Diário e remissões acrescentados com backups sob758. Kimi/Takesaki inalterado.','sources':[src(CAT),src(SNAP),src(MEM)]}],'flow':{'phase':'two_fock_units_authorized_and_queued','next_action':'Coordenador oficial executa MiMo A1 e DeepSeek Gamma(J). Recuperar os mesmos IDs; respostas DECLARADO até compilação/revisão locais. Não repetir R2 nem terminais/incertos. Kimi/Takesaki conserva pendência própria.','handles':handles}}})
 elif mode=='release':run('RELEASE_APPROVED_R3_20261014.json',[CLI,'liberar','F1.REDE','--quem',WHO,'--nota','Dois pedidos autorizados e inscritos na fila oficial; diario/mapa/quadro/ACOM atualizados. Coordenador conduz despacho; resultados ainda pendentes.'])
 else:raise ValueError(mode)

if __name__=='__main__':main()
