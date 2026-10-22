"""W-only independent integration probes. No server import or network."""
import ast,copy,hashlib,json,socket,sys,subprocess
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch
from datetime import datetime,timezone
sys.dont_write_bytecode=True
def forbidden(*a,**k):raise AssertionError('Network forbidden')
socket.create_connection=forbidden;socket.socket.connect=forbidden
W=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(W))
stage=W/'claude_routes_stage_20260922_153758_878683'
files=[stage/'iald_web_server.py',stage/'iald.js',W/'integrate_haiku_context.py',W/'claude_route_bridge.py',W/'claude_memory_package.py',W/'claude_context_snapshot.py',W/'claude_native_account.py']
before={p:p.read_bytes() for p in files};tree=ast.parse(before[stage/'iald_web_server.py'].decode('utf-8-sig'))
def install(names,env):
    nodes=copy.deepcopy([n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names])
    assert len(nodes)==len(names)
    for n in nodes:n.decorator_list=[]
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(stage/'iald_web_server.py'),'exec'),env)
from claude_route_bridge import RouteBridge
from claude_memory_package import load_package
from claude_profiles import HAIKU
motors=NS(CLAUDE='claude',EXTERNOS=('claude','openai'),PROVEDORES={'claude':'Anthropic'},plano_de=lambda r:'gratuito',claude_configurado=lambda cfg:True)
cfg=NS(contas={'luiz'},cota_global_usd=15,cache_ttl='5m',precos=lambda m:(1,.1,5,1.25))
bridge=RouteBridge(motors=motors,base_config=cfg,package_loader=lambda:load_package(W/'fixture_not_read'),enabled=True,public_daily_usd=1,public_group_daily_usd=5)
record={'motor':'claude','modelo_claude':HAIKU.model,'plano':'gratuito'}
env={'session':{'username':'fixture'},'_motor_do_usuario':lambda u:('claude',record),'iald_motores':motors,'jsonify':lambda v:v,'CLAUDE_ROUTES':bridge,'_HAIKU_PROFILE':HAIKU}
env['_cfg_do_motor']=lambda *a:bridge.configuration(record,'fixture')
install({'api_motor','api_contexto','_haiku_selected'},env)
with patch.object(Path,'read_bytes',return_value=b'[]'):
    try:env['api_motor']()
    except AttributeError as exc:status_error=type(exc).__name__
    else:raise AssertionError('Expected malformed-manifest failure')
with patch.object(Path,'read_bytes',return_value=b'[]'):
    context_data,context_status=env['api_contexto']()
assert context_status==503
race=subprocess.run(['node',str(Path(__file__).parent/'probe_haiku_motor_race.cjs')],capture_output=True,text=True,check=True)
race_evidence=json.loads(race.stdout)
# Exact send closure: reservation precedes guard on the final none payload.
chat=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_chat_externo')
send=copy.deepcopy(next(n for n in ast.walk(chat) if isinstance(n,ast.FunctionDef) and n.name=='enviar'))
calls=[]
def begin(p):calls.append(('reserve',copy.deepcopy(p)));p['max_completion_tokens']=512
def guard(adapter,cfg,payload,**kw):calls.append(('send',copy.deepcopy(payload)));return 'response',{}
envsend={'haiku':True,'_haiku_attach_tools':lambda p,d:dict(copy.deepcopy(p),tools=d),'permitidas':[{'fixture':i} for i in range(7)],'conta':NS(iniciar_chamada=begin),'post_guarded':guard,'haiku_adapter':object(),'cfg':cfg,'modelo':HAIKU.model,'registro':record,'user':'fixture','_claude_policy':lambda *a:{},'prompt_externo':'fixture','haiku_package':NS(measurement=object()),'estado_claude':object(),'count_haiku_wire':lambda w:184609}
exec(compile(ast.Module(body=[send],type_ignores=[]),'<exact closure>','exec'),envsend)
envsend['enviar']({'tool_choice':'none','max_completion_tokens':4096})
assert [a for a,_ in calls]==['reserve','send'] and calls[0][1]['tool_choice']=='none' and calls[1][1]['max_completion_tokens']==512
for p,b in before.items():assert p.read_bytes()==b,'Source changed during review: '+str(p)
report={'status':'MUDANCAS_NECESSARIAS_INTEGRACAO','pins':{str(p):hashlib.sha256(b).hexdigest() for p,b in before.items()},
'findings':[{'id':'I1','priority':'P2','file':str(stage/'iald.js'),'function':'lerMotor/contextoNativo','title':'Resposta antiga de motor vence a seleção nova e reativa CPT sobre contexto Haiku','evidence':race_evidence,'fix':'Versionar também requisições lerMotor, conferindo ticket após fetch e após json; vincular contexto à seleção vigente e impedir uso de CPT quando metadados/unidades divergem. Só contextoRequest não protege S.motor.'},
 {'id':'I2','priority':'P2','file':str(stage/'iald_web_server.py'),'function':'api_motor / RouteBridge.flags','title':'Manifesto JSON com tipo inválido escapa como erro500 em status de motor','evidence':{'manifest_fixture':'[]','api_motor_uncaught_exception':status_error,'api_contexto_status':context_status},'fix':'Normalizar TypeError/AttributeError de schema para indisponibilidade no loader/flags e cobrir também /api/motor; manter503 com opções/consentimento sem revelar erro interno.'}],
'positive_checks':['Closure enviar extraída: uma reserva seguida de um envio, recebe tool_choice none e passa teto ajustado pela conta ao guard. Não substitui teste real do contador/SQLite/conversor do pai.','Leitura: estado criado antes das closures; count_haiku_wire compartilhado pela reserva e post_guarded.','Leitura: loader confere ferramentas nativas antes de retornar; proxy confere conversão final; Haiku agente não passa pela heurística CPT.','Leitura: contexto200k,metadata sem receipt privado, pensarFalse e sete schemas; marcador de contagem protege caminho cliente quando seleção está coerente.'],
'separate_pending':['Capability do app20 antigo informada pelo pai; não implementada nem tratada como falha nova desta revisão. Necessária antes de ativar.','Snapshot/context module foi construído por este revisor; esta revisão não aprova sua própria semântica nem a integração final de produção.'],
'limits':['SomenteW; semROOT/API/segredos. Testes pais com importsROOT não reexecutados.','Node executa somente funções extraídas com fetch simulado; não browser/device real.','Tool hash real e SQLite foram reportados pelo pai, não reverificados emROOT aqui.','Nenhum stage, app, módulo existente ou produção foi editado.']}
out=W/'adversarial_memory_review'/('integration_153758_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')+'.json')
b=json.dumps(report,ensure_ascii=False,indent=2).encode();tmp=out.with_suffix('.tmp')
with tmp.open('xb') as f:f.write(b)
assert tmp.read_bytes()==b;tmp.rename(out)
print(json.dumps({'report':str(out),'race':race_evidence,'malformed_manifest_api_motor':status_error,'send_order':[x for x,_ in calls]},ensure_ascii=False))
