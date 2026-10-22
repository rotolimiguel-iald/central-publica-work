"""Adversarial synthetic tests: no network, credentials or production mutation."""
import sys,os,socket,hashlib,json,io,unittest,tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from datetime import datetime,timezone
sys.dont_write_bytecode=True
WORK=Path(__file__).resolve().parent.parent
STAMP=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
OUT=WORK/'adversarial_memory_review'/('transport_package_'+STAMP)
OUT.mkdir();(OUT/'tmp').mkdir();tempfile.tempdir=str(OUT/'tmp')
def forbid(*a,**k):raise AssertionError('Network forbidden')
socket.create_connection=forbid;socket.socket.connect=forbid;socket.socket.connect_ex=forbid
sys.path.insert(0,str(WORK))
names=['claude_guarded_transport.py','claude_memory_package.py','test_claude_guarded_transport.py','test_claude_memory_package.py','claude_account_policy.py','claude_profile_pipeline.py','claude_request_guard.py','claude_profiles.py','claude_native_counter.py','test_claude_guard_real_converter.py']
snapshots={WORK/n:(WORK/n).read_bytes() for n in names}
real_path=Path(r'C:\IALD\projetos_pyhton\IALD\iald_motor_claude.py')
snapshots[real_path]=real_path.read_bytes()
import test_claude_guarded_transport as transport_tests
import test_claude_memory_package as package_tests
from test_claude_guard_real_converter import converter as real
from claude_guarded_transport import post_guarded
from claude_memory_package import load_package
from claude_profiles import HAIKU,SONNET,context_budget
from claude_request_guard import MemoryMeasurement
suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromModule(m) for m in (transport_tests,package_tests))
log=io.StringIO();result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
assert result.wasSuccessful()
real.definir_sdk(SimpleNamespace())
prefix='OFFLINE FIXTURE MEMORY'
memory=MemoryMeasurement(HAIKU.model,hashlib.sha256(prefix.encode()).hexdigest(),183135)
cfg=SimpleNamespace(modelo=SONNET.model,max_saida=4096,cache_ttl='5m',esforco_claude='high',chave='synthetic-not-a-credential')
policy=dict(username='testador',account_approved=True,haiku_ready=True,sonnet_ready=True)
payload={'model':HAIKU.model,'max_completion_tokens':4096,'messages':[{'role':'system','content':prefix},{'role':'user','content':'fixture'}]}

class Stream:
    response=None
    def __init__(self,fail=False):self.fail=fail
    def __iter__(self):
        yield {'type':'message_start','message':{'id':'fixture','model':HAIKU.model}}
        yield {'type':'content_block_start','index':0,'content_block':{'type':'text','text':''}}
        yield {'type':'content_block_delta','index':0,'delta':{'type':'text_delta','text':'partial'}}
        if self.fail:raise RuntimeError('synthetic interruption')
    def get_final_message(self):
        return {'id':'fixture','model':HAIKU.model,'content':[{'type':'text','text':'partial'}],'stop_reason':'end_turn','usage':{'input_tokens':184609,'output_tokens':1}}
class Manager:
    def __init__(self,stream):self.stream=stream;self.entered=0;self.exited=0
    def __enter__(self):self.entered+=1;return self.stream
    def __exit__(self,*args):self.exited+=1
class Client:
    def __init__(self,**options):
        self.options=options;self.calls=[];self.last=None;self.messages=SimpleNamespace(stream=self.start)
    def with_options(self,**kw):self.options.update(kw);return self
    def start(self,**wire):self.calls.append(wire);self.last=Manager(Stream());return self.last
def call(client=None,adapter=real,**kw):
    args=dict(requested_model=HAIKU.model,server_policy=policy,prefix=prefix,memory=memory,counter=lambda r:184609)
    if client is not None:args['client']=client
    args.update(kw)
    return post_guarded(adapter,cfg,payload,**args)

# No retries invariant fails: use actual adapter client construction with fake SDK.
created=[]
def factory(**options):
    c=Client(**options);created.append(c);return c
real._CLIENTES.clear();real.definir_sdk(SimpleNamespace(Anthropic=factory))
response,decision=call()
assert response.status_code==200 and created[-1].options['max_retries']==2
response.close();assert created[-1].last.exited==1
retry_evidence={'adapter_max_retries':real.MAX_RETRIES,'client_constructed_max_retries':created[-1].options['max_retries'],'stream_calls_at_python_boundary':len(created[-1].calls),'actual_http_calls':0,'interpretation':'A chamada Python unica nao desabilita retries internos do SDK.'}

# After successful HTTP stream entry, local setup errors are mislabeled uncharged.
c=Client()
with patch.object(real,'_Fluxo',side_effect=ValueError('synthetic setup after stream entry')):
    response,decision=call(c)
error=response.json()['error'];free=real.recusa_sem_cobranca(response.status_code,error['code'])
assert c.last.entered==1 and c.last.exited==1 and free
postsend={'entered_stream':1,'closed_stream':1,'response_status':response.status_code,'error_code':error['code'],'adapter_says_certainly_no_charge':free,'decision':decision}

# Reduced declared reserves pass package loader yet disagree with transport reserve.
fixture=OUT/'package_fixture';fixture.mkdir();pb=b'fixture-only'
(fixture/'prefix.md').write_bytes(pb)
budget=context_budget(HAIKU.model,counted_model=HAIKU.model,permanent_tokens=188000,request_input_tokens=189000,reserved_output_tokens=1,margin_tokens=0)
manifest={'schema':'iald.claude.memory.v1','model':HAIKU.model,'prefix_file':'prefix.md','prefix_sha256':hashlib.sha256(pb).hexdigest(),'tools_sha256':'a'*64,'budget':budget}
(fixture/'manifest.json').write_text(json.dumps(manifest),encoding='utf-8')
package=load_package(fixture)
actual=context_budget(HAIKU.model,counted_model=HAIKU.model,permanent_tokens=188000,request_input_tokens=189000,reserved_output_tokens=4096,margin_tokens=1024)
assert package.available_dynamic_tokens==10999 and actual['remaining_tokens']==5880
reserve={'loader_accepted':True,'declared_output':1,'declared_margin':0,'reported_dynamic_tokens':package.available_dynamic_tokens,'dynamic_at_output4096_margin1024':actual['remaining_tokens'],'permanent_tokens':188000}

# Payload model mismatch remains fail-closed but incorrectly becomes generic 500.
bad_payload=dict(payload,model=SONNET.model);c=Client();count_calls=[]
response,_=post_guarded(real,cfg,bad_payload,requested_model=HAIKU.model,server_policy=policy,prefix=prefix,memory=memory,client=c,counter=lambda r:count_calls.append(r) or 184609)
assert response.status_code==500 and not c.calls and not count_calls
auth={'status':response.status_code,'code':response.json()['error']['code'],'count_calls':0,'generation_calls':0,'bypass':False}

# Verify real SSE adapter consumption, partial failure and close, not only mock flow.
stream_results=[]
for fails in (False,True):
    c=Client();manager=Manager(Stream(fails));c.messages.stream=lambda **kw:manager
    response,decision=call(c);lines=list(response.iter_lines());response.close()
    assert manager.entered==1 and manager.exited==1 and lines[-1]==b'data: [DONE]'
    has_error=any(b'"error"' in line for line in lines)
    assert has_error==fails
    assert any(b'partial' in line for line in lines)
    stream_results.append({'midstream_error':fails,'sse_error_visible':has_error,'done_emitted':True,'manager_closed_once':True,'usage_line_present':any(b'"usage"' in line for line in lines)})

for path,b in snapshots.items():assert path.read_bytes()==b,'Source changed during audit: '+str(path)
def sha(b):return hashlib.sha256(b).hexdigest()
findings=[
 {'id':'F1','priority':'P1','file':str(WORK/'claude_guarded_transport.py'),'line':27,'title':'Cliente herdado ainda permite retries do SDK','evidence':retry_evidence,'impact':'Contradiz contrato no-retry do transporte; erros retryable podem reenviar geracao automaticamente apesar de messages.stream ser chamado uma vez no wrapper.','fix':'Criar cliente derivado com max_retries=0 explicitamente, preservando timeout, inclusive cliente injetado; nao alterar cliente compartilhado. Testar opcoes reais,nao apenas call_count do mock.','dependency':{'file':str(real_path),'lines':[110,317,323]}},
 {'id':'F2','priority':'P1','file':str(WORK/'claude_guarded_transport.py'),'line':65,'title':'Falha local apos abertura do stream e classificada sem cobranca','evidence':postsend,'impact':'_resposta_de_excecao converte ValueError/RuntimeError local em claude_erro_local; recusa_sem_cobranca aceita esse codigo, embora geracao ja tenha sido iniciada. Integracao pode liberar reserva de pedido possivelmente cobrado.','fix':'Distinguir erro apos tentativa de geracao com codigo nao liberavel/estado de cobranca ambiguo e conservar decisao de contexto; testar real recusa_sem_cobranca apos manager.__enter__.','dependency':{'file':str(real_path),'lines':[181,188,828]}},
 {'id':'F3','priority':'P2','file':str(WORK/'claude_memory_package.py'),'line':39,'title':'Reserva planejada pode ser validada com margem e saida menores','evidence':reserve,'impact':'Manifesto aritmeticamente consistente com margem0/saida1 e aceito como >=10k dinamico,mas transporte usa margem1024 e pode pedir4096,restando5880. Hash do prefixo e igualdade de budget nao garantem perfil de reserva exigido.','fix':'Validar perfil reservado explicitamente (saida4096,margem1024,ou politica de minimo equivalente) antes de testar >=10000; nao usar so os valores declarados no proprio manifesto.'},
 {'id':'F4','priority':'P2','file':str(WORK/'claude_guarded_transport.py'),'line':69,'title':'Selecao divergente no payload vira erro interno em vez de recusa de autorizacao','evidence':auth,'impact':'profile_call levanta PermissionError para payload model diferente; excecao cai no handler generico,produz HTTP500 claude_erro_local. Nao ha bypass nem envio,mas o cliente recebe falha de servidor em vez de403.','fix':'Tratar PermissionError de preflight como403 claude_model_forbidden e preferir validar divergencia antes de construir cliente.'}
]
report={'status':'MUDANCAS_NECESSARIAS','created_utc':datetime.now(timezone.utc).isoformat(),'scope':'Revisao de claude_guarded_transport.py e claude_memory_package.py/testes,dependencias diretas e adaptador real lidos para fundamentar contrato; sem servidor ou credenciais.','pins':{str(p):sha(b) for p,b in snapshots.items()},'provided_tests':{'run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'passed':result.wasSuccessful()},'findings':findings,'real_adapter_sse_checks':stream_results,'positive_checks':['Politica conta/modelo recusa antes de count/send quando requested_model proibido.','Guard conta snapshot final,checa SHA do primeiro bloco e modelo,rejeita falha/overflow/mutacao antes de gerar;tool results passam pela mesma contagem.','Fluxo real em sucesso/erro parcial emite DONE e fecha gerente uma vez;close antes de consumo tambem testado.','Pacote usa caminho fixo,prefix SHA,comparacao do manifesto/prefixo ao fim e tipos inteiros de budget via context_budget.'],'integration_limits':['Autenticacao de sessao,consentimento e reserva financeira sao precondicoes EXPLICITAS do chamador; nao auditadas no servidor nem tratadas como bypass dos modulos.','tools_sha256 apenas validado como string e retornado; estes modulos nao comparam schema de ferramentas com esse hash. Integração deve definir/validar identidade se pretende exigir o pacote de ferramentas medido;contagem final continua protegendo janela.','Sem nova chamada API/rede ou teste de retries HTTP reais;F1 prova configuracao herdada2,nao custo incorrido nesta auditoria.','Streaming com tool_use/refusal e contabilizacao de uso parcial nao auditados exaustivamente;testes respectivos so mockavam _Fluxo.','Nenhuma fonte/codigo/producao modificado;somente script,fixtures sinteticas e parecer na subpasta de auditoria.']}
def save(name,data):
    dest=OUT/name;temp=OUT/(name+'.tmp');b=data.encode('utf-8');assert not dest.exists()
    with temp.open('xb') as f:f.write(b)
    assert temp.read_bytes()==b and b;temp.rename(dest)
save('review.json',json.dumps(report,ensure_ascii=False,indent=2))
save('provided_tests.txt',log.getvalue())
md='# Revisao transporte/pacote — mudancas necessarias\n\n'+ '\n\n'.join(f"## {f['priority']} {f['id']} — {f['title']}\n\n{f['file']}:{f['line']}\n\n{f['impact']}\n\nCorrecao proposta: {f['fix']}\n\nEvidencia: `{json.dumps(f['evidence'],ensure_ascii=False)}`" for f in findings)
md+='\n\n13 testes fornecidos passaram,mas nao cobriam essas fronteiras. Testes adicionais offline exercitaram configuracao real do adaptador,recusa_sem_cobranca,manifesto com reserva reduzida,mismatch de modelo e SSE real sucesso/falha parcial. Sem API/credenciais/producao. tools_sha256 nao e comparado com ferramentas por estes modulos; autenticacao/consentimento/reserva sao obrigacoes do chamador,nao auditadas aqui.\n'
save('REVIEW.md',md)
print(json.dumps({'report':str(OUT/'review.json'),'markdown':str(OUT/'REVIEW.md'),'provided_tests':report['provided_tests'],'finding_ids':[f['id'] for f in findings],'stream_checks':stream_results},ensure_ascii=False,indent=2))
