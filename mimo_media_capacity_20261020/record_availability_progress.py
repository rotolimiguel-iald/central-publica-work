"""Record verified surfaces and only tool-confirmed completed local executors."""
import hashlib,json
from task import W,REF,OWNER,call,new
current=call({'operation':'get','reference':str(REF)},False)
tool=json.loads((W/'AGENT_TERMINAL_TOOL_RESULTS_R1.json').read_bytes())['result']['status']
flow=dict(current['p']);handles=[dict(x) for x in flow.get('handles',[])]
for handle in handles:
    state=tool.get(handle.get('external_id'))
    if isinstance(state,dict) and 'completed' in state:
        handle['status']='completed'
        handle['terminal_source']=str(W/'AGENT_TERMINAL_TOOL_RESULTS_R1.json')
flow.update(handles=handles,phase='closeout_with_documented_provider_limits',
 next_action='Concluir revisão/apêndices de memória e matriz. Teste adicional pago permanece em AGUARDA_OPERADOR; não repetir vídeo incerto.')
sources=[]
for name in ('FINAL_RUNTIME_PINS_R8.json','WEB_LIVE_SCOPE.json','mobile_stage/IOS35_DISTRIBUTION.json',
 'mobile_stage/ANDROID30_AUTHENTICATED_DOWNLOAD.json','mobile_stage/ANDROID30_ANONYMOUS_DOWNLOAD.json',
 'live_stage/TEST_COST_ROLLUP_R1.json','AGENT_TERMINAL_TOOL_RESULTS_R1.json'):
    p=W/name;sources.append(dict(kind='artifact',ref=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
record=dict(id='media-capacity-availability-with-provider-limits-r1',kind='fact',statute='REAL',sources=sources,
 text='Capacidade local de37.499.904bytes implantada; núcleo científico v394 preservado. Web pronta; iOS4.1(35) Em testes nos dois grupos; APK30 publicado e download autenticado/hash conferido, anônimo bloqueado. Testes reais preservam áudio completed com PERCEPTION_FAILURE e vídeo failed/stream incerto; não são validação geral de percepção. Custo combinado contabilizado0.6712981122USD inclui teto pessimista do vídeo, não fatura. Novo teste extra0.50USD aguarda resposta humana na unidade própria; nenhuma repetição do vídeo.')
result=call(dict(operation='transition',reference=str(REF),actor=dict(id=OWNER,kind='agent'),
 expected_revision=current['receipt']['revision'],event_id='media-capacity-surfaces-available-r1',
 changes=dict(records=[record],flow=flow)),False)
new('AVAILABILITY_PROGRESS_MEMORY.json',result)
print(json.dumps(dict(revision=result['revision'],completed_local_handles=3)))
