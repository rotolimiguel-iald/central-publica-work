"""Register the additive delivery by the programme/map official CLIs."""
import json, subprocess, sys
from pathlib import Path
from activate import ROOT, CORE, CENTRAL, REF, ACTOR, call, pin, source, save

UNIT='F9.MEMORIA_MISSAO_20261016'
TUNNEL=CENTRAL/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019'/UNIT

def cli(args,name):
    receipt=ROOT/(name+'.json')
    if receipt.exists():raise RuntimeError('Inspect existing result; do not repeat '+str(receipt))
    r=subprocess.run([sys.executable,'-B','-X','utf8',*map(str,args)],capture_output=True,text=True,encoding='utf-8')
    try:result=json.loads(r.stdout)
    except json.JSONDecodeError:result={'text':r.stdout}
    save(receipt.name,{'command':list(map(str,args)),'exit_code':r.returncode,'result':result,'stderr':r.stderr})
    if r.returncode:raise RuntimeError(r.stdout+r.stderr)
    return result

def main():
    entry={'tipo':'ROTA','rota_id':'infra.memoria_missao.ancoragem_e_poda_20261016','dominio':'INFRAESTRUTURA',
      'titulo':'Missão ancorada: requisitos evolutivos, sincronização de agentes e PODA no ACOM',
      'pergunta':'Como impedir que coordenação e agentes avancem com uma missão obsoleta ou reconstruam entregas existentes?',
      'dados':[],'metodo':'Mesmo banco ACOM; DAG, revisão/CAS, lease, pinos, candidato/aceite distinto, sincronização antes de ação/integração, cláusula de parada.',
      'resultado':'8 destinos instalados, 28 testes do núcleo, 8 verificações stdio em cópia, 4 ferramentas MCP em servidor real novo; revisão independente e M0 aceito tecnicamente. Missão real preserva 10 critérios e 8 decisões; 3 entregas recuperadas para revisão; 11 handles conservados.',
      'veredito':'INSTALLED_AND_INDEPENDENTLY_REVIEWED_WITH_SCOPE','estatuto':'REAL','status':'EXAMINADA',
      'olhou_dados':False,'defeito':'Clientes legados precisam aderir. Preflight não torna execução externa atômica. Não há promessa de memória infalível nem medição de redução percentual de tokens.',
      'nao_refazer':'Reutilizar controlador/CLI/MCP e a referência exata da missão. Não relançar jobs/builds incertos nem refazer R1/R2/R9 porque um resumo antigo os chama abertos.',
      'proximo_passo':'Gerência audita a unidade entregue. Toda retomada lê FECHO_MISSION_REFERENCE.json pelo CLI; integração só com revisão atual e evidência. R1/R2/R9 aguardam revisão; sete critérios ainda exigem complemento/integração.',
      'onde':str(CORE/'MISSION_PROTOCOL.md'),
      'artefatos':[str(TUNNEL/'DELIVERY.json'),str(ROOT/'MEMORY_DELIVERY.json'),str(ROOT/'ACTIVATION_ACCEPT_RECEIPT.json'),str(REF)],
      'refs':['infra.memoria_acom.core_20261010','infra.memoria_acom.integracao_20261010'],
      'nota':'Unidade '+UNIT+', reivindicação 891. Infraestrutura operacional; não aceita ciência, não muda gate nem reinicia MCPs já abertos.'}
    save('MAP_ENTRY.json',entry)
    mapped=cli([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',ROOT/'MAP_ENTRY.json','--quem',ACTOR['id']],'MAP_RECEIPT')
    board=cli([r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','ENTREGUE',
       '--evidencia',TUNNEL/'DELIVERY.json','--evidencia',ROOT/'MEMORY_DELIVERY.json','--evidencia',ROOT/'ACTIVATION_ACCEPT_RECEIPT.json',
       '--evidencia',ROOT/'MAP_RECEIPT.json','--nota','Infraestrutura instalada e revisada; M0 aceito tecnicamente por revisor distinto. 10 critérios científicos preservados, sem aceite científico. CLI/MCP em processo novo; clientes legados precisam aderir.'],'BOARD_DELIVERY')
    state=cli([r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT],'BOARD_STATE')
    if state.get('reivindicacao',{}).get('quem')==ACTOR['id']:
        cli([r'C:\IALD\PROGRAMA_IALD\iald.py','liberar',UNIT,'--quem',ACTOR['id'],'--nota','Entrega e escritas de memória concluídas; aguarda auditoria da gerência.'],'BOARD_RELEASE')
    reg=save('REGISTRATION.json',{'unit':UNIT,'map':pin(ROOT/'MAP_RECEIPT.json'),
       'board':pin(ROOT/'BOARD_DELIVERY.json'),'memory':pin(ROOT/'MEMORY_DELIVERY.json'),
       'delivery':pin(TUNNEL/'DELIVERY.json'),'technical_accept':pin(ROOT/'ACTIVATION_ACCEPT_RECEIPT.json')})
    own_record={'id':'memory-delivery-registered-v1','kind':'fact','statute':'REAL',
      'text':'Infraestrutura de sincronização instalada, testada e revisada independentemente; M0 aceito. Entrega registrada no mapa/quadro, quatro superfícies com backups. Prioridade memória atendida tecnicamente; gerência conserva ratificação. Retomada científica só pela referência exata e pelos resíduos atuais.',
      'sources':[source(reg),source(TUNNEL/'DELIVERY.json'),source(REF)]}
    call('session_memory.py',{'operation':'transition','reference':str(ROOT/'ACOM_REFERENCE.json'),
        'expected_revision':1,'event_id':'memory-delivery-registered-v1','actor':ACTOR,
        'changes':{'records':[own_record],'flow':{'phase':'technical_delivery_complete','next_action':'Retomar pelo project da FECHO_MISSION_REFERENCE.json; usar preflight e integrar somente resíduos atuais. Gerência audita unidade entregue.'}}},'OWN_DELIVERED')
    call('session_memory.py',{'operation':'verify','reference':str(ROOT/'ACOM_REFERENCE.json')},'OWN_FINAL_VERIFY')
    call('session_memory.py',{'operation':'verify','reference':str(REF)},'FECHO_FINAL_VERIFY')
    print(json.dumps({'unit':UNIT,'map_result':mapped,'board_result':board,'registration':str(reg)},ensure_ascii=False))

if __name__=='__main__':main()
