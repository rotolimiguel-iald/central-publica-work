"""Record an actual automatic-review refusal; never dispatch indirectly."""
import datetime as dt
import json
import sqlite3
import sys
from diary_r1 import ROOT,OUT,WORK,WHO,CLI,claim,new,pin
from register_progress_r2 import run,src

D=OUT/'orchestration_r3'
BASE=ROOT/'Chatgpt/IALD_ORQUESTRACAO_20260923'
EVENT='fock-next-units-awaiting-specific-consent-r3-20261013'
ENTRY=D/'DIARY_ENTRY_PENDING_R3.json'
CAT=D/'HANDOFF_PENDING_APPROVAL_R3.json'
MAP=D/'MAP_ENTRY_PENDING_APPROVAL_R3.json'
SNAP=OUT/'diary_events'/(EVENT+'_DIARIO_SNAPSHOT.md')
MEM=OUT/'diary_events'/(EVENT+'_RECEIPT.json')

def prepare():
 claim()
 db=sqlite3.connect((BASE/'state/tasks.sqlite3').as_uri()+'?mode=ro',uri=True)
 rows=[]
 for p in ('MIMO','DEEPSEEK'):
  reqpath=D/f'REQUEST_{p}_R3_1.json';req=json.loads(reqpath.read_text(encoding='utf-8'))
  assert not any(db.execute(f'SELECT id FROM {t} WHERE request_id=?',(req['request_id'],)).fetchone() for t in ('coordination_jobs','tasks'))
  assert not (D/f'SUBMIT_{p}_R3_1_INTENT.json').exists()
  prev=json.loads((D/f'PREVIEW_{p}_R3_1.json').read_text(encoding='utf-8'))['response']
  rows.append({'provider':p.lower(),'request_id':req['request_id'],'payload':pin(reqpath),'sources':pin(D/f'SOURCES_{p}_R3_1.json'),'preview':pin(D/f'PREVIEW_{p}_R3_1.json'),'selected':prev['selected'],'generation':prev['canonical_memory']['generation'],'context_bytes':prev['canonical_memory']['context_bytes'],'status':'NOT_SUBMITTED_AWAITING_SPECIFIC_APPROVAL','lemma_id':req['execution_constraints']['lemma_id']})
 db.close()
 new(D/'COMPACT_SCOPE_REVIEW_TRANSCRIPT_R3_1.json',{'kind':'Coordinator transcript of returned independent review','reviewer':'/root/takesaki_local_lemmas','verdict':'PASS_SCOPE','content':'APROVADOS quanto às definições necessárias e ao escopo; sem achado material. MiMo preserva os setores concretos, soma ℓ², vácuo e produto interno tensorial necessários a A1. DeepSeek preserva Jcandidate, setores e extensão semilinear; conjugação no setor zero continua exigida, sem depender de A1. Resíduo baixo: completar a assinatura truncada de extendOfIsometry_eq e incluir inner_tmul no DeepSeek ajudaria a implementação. Nenhuma escrita, compilação ou chamada a provedor.','scope':'Source excerpts/independence only; no new proof validated.'})
 rejection='This submits a new payload containing extensive internal TGL memory and scientific material to the external MiMo service; the available approvals authorize other/specific submissions but do not clearly authorize this exact sensitive payload and destination.'
 new(D/'AUTO_REVIEW_REFUSAL_R3.json',{'at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'action':'queue_requests_r3.py submit mimo R3_1','rejection_reason_verbatim':rejection,'process_started':False,'provider_called':False,'queue_job_created':False,'response':'No workaround or indirect dispatch. Specific user approval requested for the two named current payloads. DeepSeek was not attempted.','sources':rows})
 catalog={'unit':'F1.REDE','reference':'slot-followup-F1REDE-stage753-20261013','status':'PREPARED_PREVIEWED_AWAITING_OPERATOR','requests':rows,'previous_stage':pin(OUT/'RESULTADO_ETAPA_R2.json'),'refusal':pin(D/'AUTO_REVIEW_REFUSAL_R3.json'),'scope_review':pin(D/'COMPACT_SCOPE_REVIEW_TRANSCRIPT_R3_1.json'),'operator_question':'Autorizar os dois envios únicos: MiMo exponenciais/totalidade e DeepSeek Gamma(J), com fontes científicas e memória interna canônica v392.','no_dispatch':'Do not submit, execute or indirectly dispatch until specific approval is recorded. No old request or uncertain result may be repeated.','kimi_takesaki':'Original specific approval pending; unchanged.'}
 new(CAT,catalog)
 new(BASE/'state/handoffs'/'F1REDE_stage753_units_AWAITING_OPERATOR_R3_20261013.json',catalog)
 body='''[REAL — preparação] Levantamento no mapa, Nós Vivo e matriz R2 identificou duas construções independentes ainda abertas: A1, vetores exponenciais e totalidade no Fock concreto; B, segunda quantização antiunitária do J existente. MiMo foi selecionado para A1 e DeepSeek para B. Revisão independente de escopo não encontrou circularidade ou dependência entre as unidades. O resíduo baixo sobre assinaturas de APIs está registrado ao lado e não significa prova construída.

[REAL — prévias locais] Um pacote inicial foi recusado pelo limite de 24.000 caracteres antes de registro ou chamada. Os rascunhos iniciais foram preservados e substituídos explicitamente por pedidos compactos de 20.586 e 23.422 caracteres. As duas prévias passaram com a geração v392 verificada, contextos de 908.522 e 646.413 bytes e cobertura parcial declarada. Payloads, fontes, linhas, hashes e IDs foram gravados antes da tentativa de submissão.

[REAL — bloqueio de processo] A revisão automática rejeitou o comando de submissão MiMo antes de iniciar o processo: considerou insuficiente a autorização disponível para este pacote específico de material interno. Nenhum job foi criado; nenhum provedor foi chamado. O pedido DeepSeek não foi tentado. Foi apresentada ao operador uma pergunta explícita para os dois envios únicos. A coordenação recebe catálogo marcado PREPARED_PREVIEWED_AWAITING_OPERATOR, com proibição de envio indireto até autorização registrada. A pendência específica Kimi/Takesaki permanece inalterada.

[OPEN] As construções A1 e B continuam abertas. Nenhum resultado científico novo é reivindicado por esta preparação. A próxima ação é registrar a resposta humana e, se autorizada, submeter os mesmos payloads/IDs uma vez pelo cliente oficial; depois recuperar os resultados sem duplicação e verificar em sandbox. A R2 continua íntegra. Diário e remissões são acrescentados sob reivindicação755, com backups de bytes; nenhum um.py, kernel, Bancada, dado observado ou gate muda.'''
 new(ENTRY,{'id':EVENT,'unit':'F1.REDE','title':'13/10/2026 — próximas unidades preparadas; envio aguardando autorização específica','body':body,'sources':[str(CAT),str(D/'AUTO_REVIEW_REFUSAL_R3.json'),str(D/'COMPACT_SCOPE_REVIEW_TRANSCRIPT_R3_1.json'),str(D/'SOURCE_AND_SCOPE_IDENTITY_R3_1.json'),str(D/'DRAFT_SUPERSESSION_R3_1.json')],'link_surfaces':True,'surface_summary':'[REAL — preparação] Dois pedidos independentes pinados e com preview v392 aprovado: MiMo A1 exponenciais/totalidade e DeepSeek Gamma(J). Auto-review bloqueou a submissão MiMo antes de processo; nenhum job/chamada. Operador recebeu pergunta específica para ambos. Catálogo HANDOFF_PENDING_APPROVAL_R3.json impede envio indireto. Construções OPEN; R2 preservada.'})
 new(MAP,{'tipo':'ROTA','rota_id':'formal.f1_rede.fock_exponentials_and_antiunitary_preparation','dominio':'KERNEL_FORMAL','titulo':'Exponenciais no Fock e Gamma(J): duas unidades independentes preparadas','pergunta':'Quais construções podem prosseguir após a R2 sem repetir ou pressupor resultados abertos?','dados':['R2 Fock e Jcandidate','Memória v392 verificada'],'metodo':'Levantamento, recorte de fontes por linha/hash, revisão de escopo e preview da fila.','resultado':'Duas prévias aprovadas; submissão MiMo bloqueada pela revisão automática antes de iniciar processo. Nenhum job ou provedor. Pergunta específica ao operador registrada.','veredito':'PREPARED_PREVIEWED__AWAITING_SPECIFIC_OPERATOR_APPROVAL','estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,'defeito':'A1 e B permanecem construções abertas. O bloqueio de envio não é um resultado matemático.','nao_refazer':'R2, rascunhos substituídos e unidades terminais/incertas.','proximo_passo':'Registrar resposta humana; se autorizada, submeter uma vez os payloads e IDs persistidos.','onde':str(D),'artefatos':[str(CAT),str(MEM)],'refs':['formal.f1_rede.concrete_bosonic_kinematics'],'nota':'Nada é enviado indiretamente. Kimi/Takesaki conserva pendência específica; produção/gate intactos.'})
 print(json.dumps({'catalog':pin(CAT),'requests':[{'provider':r['provider'],'request_id':r['request_id']} for r in rows]},ensure_ascii=False))

def main():
 mode=sys.argv[1]
 if mode=='prepare':prepare()
 elif mode=='diary':run('DIARY_PENDING_R3_RUN.json',[str(WORK/'diary_r1.py'),str(ENTRY)])
 elif mode=='map':
  claim();run('MAP_PENDING_R3.json',[r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(MAP),'--quem',WHO+' / F1.REDE'])
 elif mode=='board':
  claim();run('BOARD_PENDING_R3.json',[CLI,'avancar','F1.REDE','--quem',WHO,'--status','AGUARDA_OPERADOR','--evidencia',str(CAT),str(SNAP),str(MEM),'--nota','Dois pedidos independentes preparados e preview v392 aprovado. Auto-review recusou submissao MiMo antes de iniciar processo por autorizacao especifica insuficiente; pergunta ao operador para MiMo/DeepSeek. Nenhum job/provedor; diario sob755; nao despachar indiretamente.'])
 elif mode=='acom':
  claim();cat=json.loads(CAT.read_text(encoding='utf-8'))
  handles=[{'id':'f1-rede-deepseek','request_id':'701e5bcb-cb47-4706-a9be-9b5ed10f4a35','job_id':'4d57aa1f-2d40-43df-8f82-f16593d899a2','execution_task_id':'69dd527b-cf74-4b4d-9a15-0c51b8d191bd','provider':'deepseek','status':'completed_no_repeat','unit':'F1.REDE'}]
  for u in cat['requests']:handles.append({'id':u['lemma_id'],'request_id':u['request_id'],'provider':u['provider'],'status':'prepared_awaiting_specific_approval','unit':'F1.REDE'})
  run('ACOM_PENDING_R3.json',[r'C:\IALD\MEMORIA_IALD\session_memory.py'],{'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),'expected_revision':5,'event_id':'f1-rede-next-units-awaiting-specific-consent-r3-20261013','actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':'fock-next-units-awaiting-specific-consent-r3','kind':'fact','statute':'REAL','text':'Duas unidades independentes preparadas: A1 exponenciais/totalidade MiMo e B Gamma(J) DeepSeek. Fontes/pins/IDs e previews v392 conferidos. Auto-review recusou submissao MiMo antes de processo por autorização específica insuficiente; DeepSeek não tentado. Nenhum job criado ou provedor chamado. Pergunta humana explícita pendente para ambos; nenhum envio indireto. Diário e remissões com backup sob755.','sources':[src(CAT),src(MEM),src(SNAP)]}],'flow':{'phase':'next_fock_units_prepared_awaiting_specific_consent','next_action':'Aguardar resposta humana à pergunta específica dos dois payloads; se autorizada, usar os mesmos IDs e cliente oficial uma vez. Não contornar revisão automática, não repetir R2, não tocar Kimi/Takesaki. Trabalho matemático das duas unidades ainda OPEN.','handles':handles}}})
 elif mode=='release':run('RELEASE_PENDING_R3.json',[CLI,'liberar','F1.REDE','--quem',WHO,'--nota','Pedidos preparados e pendência específica inscrita; diario, mapa, quadro e ACOM atualizados. Nada enviado.'])
 else:raise ValueError(mode)

if __name__=='__main__':main()
