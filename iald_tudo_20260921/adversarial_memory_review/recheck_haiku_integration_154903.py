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
stage=W/'claude_routes_stage_20260922_154903_859968'
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
install({'api_motor','api_contexto','_haiku_selected','_haiku_client_ready'},env)
env['request']=NS(headers={'X-IALD-Context':'anthropic-native-v1'})

env.update(_motor_selection_id=lambda *a:'claude-haiku',_opcoes_de_motor=lambda *a:[],
           _consentimento_do_motor=lambda *a:{'necessario':True,'dado':False},_consentimentos_registrados=lambda *a:[])
malformed=[]
for raw in (b'[]',b'null',b'true',b'123'):
    with patch.object(Path,'read_bytes',return_value=raw):
        data,status=env['api_motor']()
    assert status==503 and data['disponivel'] is False
    assert data['consentimento']['necessario'] is True
    malformed.append({'manifest':raw.decode(),'status':status,'options_retained':'opcoes' in data,'consent_retained':'consentimento' in data})
prefix=b'fixture-only'
for invalid in ([],None,True,42):
    manifest={'schema':'iald.claude.memory.v1','model':HAIKU.model,'prefix_file':'prefix.md','prefix_sha256':hashlib.sha256(prefix).hexdigest(),'budget':invalid}
    with patch.object(Path,'read_bytes',side_effect=[json.dumps(manifest).encode(),prefix]):
        try:load_package(W/'fixture_not_read')
        except ValueError:pass
        else:raise AssertionError('Invalid budget accepted')
race=subprocess.run(['node',str(Path(__file__).parent/'probe_haiku_motor_race_154903.cjs')],capture_output=True,text=True,check=True)
for p,b in before.items():assert p.read_bytes()==b,'Source changed during audit'
report={'status':'I1_I2_CORRIGIDOS_NO_ESCOPO_REPRODUZIDO','pins':{str(p):hashlib.sha256(b).hexdigest() for p,b in before.items()},
        'I1':json.loads(race.stdout),'I2':{'malformed_manifest_route_results':malformed,'invalid_budget_types_rejected':4},
        'remaining_reproduced_findings':[],
        'limits':['SomenteW; semROOT/API/produção. Script não importa servidor; extrai AST de rotas e funções JS com mocks.','Status503 reproduzido com loaderW real e leitura de manifesto simulada; consentimento/opções permanecem na resposta.','Teste real_agent e resultadosSQLite/conversor reportados pelo pai não reexecutados nem aprovados por inferência.','Encerramento específico deI1/I2; não constitui aprovação global de implantação/ativação.']}
out=W/'adversarial_memory_review'/('integration_154903_recheck_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')+'.json')
b=json.dumps(report,ensure_ascii=False,indent=2).encode();tmp=out.with_suffix('.tmp')
with tmp.open('xb') as f:f.write(b)
assert tmp.read_bytes()==b;tmp.rename(out)
print(json.dumps({'report':str(out),'status':report['status'],'history_after':report['I1']['history_after'],'manifest503_cases':len(malformed)},ensure_ascii=False))
