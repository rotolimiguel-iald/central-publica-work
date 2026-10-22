"""Register this delivery with existing tools; no inference about deployment or scientific closure."""
import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path
from mission_io import WORK, REFERENCE, ACTOR, PYTHON, call, check, pin, project, save

UNIT = 'F9.MEMORIA_ORGANISMO_20261016'
ROUTE = 'infra.memoria_organismo.atividade_20261016'
OUT = WORK / 'memory_final'

def run_once(label, args):
    intent, result = OUT/(label+'_INTENT_R1.json'), OUT/(label+'_RESULT_R1.json')
    if intent.exists() or result.exists():
        raise RuntimeError('Existing attempt; recover receipt without repeating: '+label)
    save(intent, {'args':args,'time_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    cp = subprocess.run(args, capture_output=True, text=True, encoding='utf-8')
    save(result, {'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr,
                  'time_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    if cp.returncode:
        raise RuntimeError('Failed; inspect '+str(result))
    return result

def prepare():
    check('M')
    p, receipt = project()
    accepted = next(x for x in p['projection']['settled'] if x['id']=='D')
    assert accepted['status']=='satisfied'
    d = json.loads((WORK/'DELIVERY_D_R1.json').read_text(encoding='utf-8'))
    applied = json.loads((OUT/'APPLIED_R1.json').read_text(encoding='utf-8'))
    assert applied['status']=='APPLIED_VERIFIED'
    evidences = [WORK/'DELIVERY_D_R1.json', WORK/'validation_final/V_DELIVERY_R1.json',
                 WORK/'review_deployment_r2/D_FINAL_REVIEW_R1.json',
                 WORK/'review_deployment_r2/D_ACCEPTED_R1.json',
                 WORK/'review_deployment_r2/GIT_BYTES_DIAGNOSTIC_R1.json',
                 OUT/'PLAN_R1.json',OUT/'REVIEW_R1.json',OUT/'APPLIED_R1.json',
                 OUT/'ACTIVITY_PROTOCOL_R2.md']
    report = {'status':'DELIVERED_FOR_MANAGEMENT_REVIEW', 'unit':UNIT,'author':ACTOR['id'],
              'time_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'reference':pin(REFERENCE),
              'mission_revision':p['receipt']['revision'],'technical_D_independently_accepted':True,
              'memory_surfaces_appended':len(applied['surfaces']),
              'new_protocol':applied['new_document'],'files_installed':d['installed_files'],
              'tests':{'distinct_local':170,'mcp_checks':7,'real_JEV_calls':1},
              'availability':d['availability'],'scope_variance':d['scope_variance'],
              'scientific_scope':d['scientific_memory_scope'],
              'physical_device':'Separate F1.FECHO reference and evidence; memory does not supply the physical-device/model/clock bridge.',
              'open_checks':d['open_checks'], 'evidence':[pin(x) for x in evidences],
              'memory_review':'Append plan reviewed independently before application. Final M acceptance recorded separately after map/board registration.',
              'map_route':ROUTE,'no_gate_change':True}
    save(WORK/'DELIVERY_R1.json',report)
    text = '''# Memória de atividade da IALD — entrega de 16/10/2026

## Resultado

[REAL] Instalados 31 arquivos, com 20 backups de bytes. ACOM, controlador de missão, app, JEV, nativa/holografia, fila, CLI/MCP e o chamador externo da Bancada compartilham o acompanhamento da atividade. O protocolo conserva a inscrição, os critérios e a evolução da tarefa; resultados ficam candidatos até revisão, e envios incertos não são repetidos.

170 casos locais distintos passaram, além de sete verificações MCP. Uma chamada real ao JEV recebeu HTTP 200: pacote de 56.582 bytes, 12.764 tokens de entrada, 39 de saída, 0,737 s. Esses números não medem ganho cognitivo nem contexto ilimitado.

Dez superfícies de memória/instruções receberam apêndices com backups imediatos; o novo ACTIVITY_PROTOCOL.md liga as instruções à implementação. Os recibos em memory_final registram cada hash e o prefixo preservado.

## Disponibilidade

| Superfície | Estado e limite |
|---|---|
| App/web | Processo novo e HTTP 200; interação autenticada e revisão aguardam login. |
| Nativa/holografia | Instalada, imports e testes locais; sem inferência real do modelo nesta entrega. |
| Fila/CLI/MCP | Código instalado e novo MCP com 20 ferramentas; clientes antigos não recarregados. |
| Bancada | Chamador instalado; serviço na porta 18777 indisponível. Falha custodiada sem repetição. |
| Android 4.1 (28) | APK/AAB assinados e auditados, somente locais; nenhum Play/download ou aparelho atualizado. |
| iOS | Recursos enviados ao repositório privado; login/build/grupos Equipe e Piloto ainda pendentes. |

O push privado dos dois recursos ocorreu apesar da expressão “ou publicar” no plano inicial; o recibo registra o desvio de redação e sua relação com a ordem permanente de atualização conjunta, sem presumir ratificação. Git normalizou CRLF para LF; a revisão conferiu equivalência normalizada, não identidade de bytes entre blob e worktree.

A ciência instalada no app permanece v392, e a fila científica tem geração independente. Nada nesta entrega resolve por si a ponte física da F1.FECHO, altera o kernel científico ou move o gate. Sessões legadas precisam cumprir explicitamente o protocolo; não se promete eliminação de toda perda ou alucinação.

## Recuperação

Recibo principal: DELIVERY_R1.json. Implantação e disponibilidade: DELIVERY_D_R1.json. Referência desta missão: SESSION_REFERENCE.json; uma nova sessão não deve adotá-la como sua inscrição. O resultado final de M e o estado do quadro/mapa ficam em memory_final/CLOSURE_R1.json quando concluídos.
'''
    with (WORK/'ENTREGA_MEMORIA.md').open('xb') as f:
        f.write(text.encode('utf-8'))
    save(OUT/'MAP_ENTRY_R1.json', {'tipo':'ROTA','rota_id':ROUTE,'dominio':'INFRAESTRUTURA',
        'titulo':'Memória de atividade integrada ao organismo IALD com revisão e custódia',
        'pergunta':'Como manter objetivo, critérios e avanços sincronizados entre consumidores sem repetir trabalho encerrado?',
        'metodo':'Reaproveitamento ACOM/mission, identidade e CAS, custódia antes de integração, revisão independente e deploy por hash.',
        'resultado':'31 arquivos instalados,20 backups;170 casos locais distintos e7 verificações MCP; JEV real HTTP200 com56582bytes e12764tokens de entrada;10 apêndices de memória e protocolo novo.',
        'veredito':'INSTALLED_WITH_VERIFIED_LIMITS','estatuto':'REAL','status':'EXAMINADA_COM_DEFEITO',
        'olhou_dados':False,'dados':['Casos sintéticos de software; um transporte real JEV com conteúdo público/sintético'],
        'defeito':'Login app/TestFlight pendentes; Bancada18777 indisponível; clientes MCP antigos sem recarga; nativa sem inferência real; APK/AAB locais. Contexto finito. Push privado registrado como variação da redação inicial.',
        'nao_refazer':'Reutilizar a implementação e os recibos; não repetir chamadas incertas nem inventário ou testes já aceitos sem achado novo.',
        'proximo_passo':'Gerência audita entrega; completar login, disponibilidade iOS e serviço Bancada sob os atos respectivos, preservando IDs. Física segue referência separada.',
        'onde':str(WORK),'artefatos':[str(WORK/'DELIVERY_R1.json'),str(WORK/'ENTREGA_MEMORIA.md'),str(OUT/'APPLIED_R1.json')],
        'refs':['infra.memoria_missao.ancoragem_e_poda_20261016']})
    print(json.dumps({'report':pin(WORK/'DELIVERY_R1.json')},ensure_ascii=False))

def register():
    check('M')
    mr=run_once('MAP_REGISTER',[PYTHON,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(OUT/'MAP_ENTRY_R1.json'),'--quem',ACTOR['id']])
    br=run_once('BOARD_DELIVER',[PYTHON,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','ENTREGUE','--evidencia',str(WORK/'DELIVERY_R1.json')])
    save(OUT/'REGISTRATION_R1.json',{'map':pin(mr),'board':pin(br),'delivery':pin(WORK/'DELIVERY_R1.json')})
    print(json.dumps({'registration':pin(OUT/'REGISTRATION_R1.json')},ensure_ascii=False))

def close():
    p, rp = project()
    assert not p['projection']['active']
    assert p['projection']['tetelestai'] is True
    before, _ = call('session_memory.py',{'operation':'get','reference':str(REFERENCE)},'close_get')
    sources=[]
    for f in (WORK/'DELIVERY_R1.json',OUT/'REGISTRATION_R1.json',OUT/'M_FINAL_REVIEW_R1.json',OUT/'M_ACCEPTED_R1.json'):
        v=pin(f);sources.append({'kind':'artifact','ref':v['path'],'sha256':v['sha256']})
    result, tr = call('session_memory.py', {'operation':'transition','reference':str(REFERENCE),'actor':ACTOR,
        'expected_revision':before['revision'],'event_id':'organism-delivered-material-r1',
        'changes':{'records':[{'id':'organism-memory-delivery-r1','kind':'fact','statute':'REAL','sources':sources,
        'text':'Integração operacional instalada e aceita tecnicamente no escopo dos recibos:31 arquivos,20 backups,170 casos locais,7 verificações MCP,um JEV real e10 apêndices. Quadro ENTREGUE para c1. Login app/TestFlight,Bancada indisponível e recarga dos clientes antigos permanecem verificações externas. Android28 local; nenhuma afirmação de ciência ou implantação física.'}],
        'flow':{'phase':'delivered_with_external_checks','next_action':'Gerência audita; após login conferir app/TestFlight. Serviço Bancada e clientes MCP exigem disponibilidade/recarga explícita. Não repetir IDs incertos. Física usa sua própria referência.'}}},'delivery_material')
    verified, vr=call('session_memory.py',{'operation':'verify','reference':str(REFERENCE)},'delivery_verify')
    after, ar=project()
    save(OUT/'CLOSURE_R1.json',{'status':'TECHNICAL_REQUIREMENTS_ACCEPTED_WITH_EXTERNAL_CHECKS','revision':after['receipt']['revision'],
        'tetelestai':after['projection']['tetelestai'],'board_status':'ENTREGUE','management_acceptance_not_claimed':True,
        'delivery':pin(WORK/'DELIVERY_R1.json'),'registration':pin(OUT/'REGISTRATION_R1.json'),
        'evidence':[pin(x) for x in (rp,tr,vr,ar,OUT/'M_FINAL_REVIEW_R1.json',OUT/'M_ACCEPTED_R1.json')],
        'external_checks':json.loads((WORK/'DELIVERY_D_R1.json').read_text(encoding='utf-8'))['open_checks']})
    print(json.dumps({'closure':pin(OUT/'CLOSURE_R1.json'),'revision':after['receipt']['revision'],'tetelestai':after['projection']['tetelestai']},ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('operation',choices=['prepare','register','close'])
    globals()[parser.parse_args().operation]()
