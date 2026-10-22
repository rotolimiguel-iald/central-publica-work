"""Offline context/spend regression on the frozen v380 prefix; no provider clients."""
import ast, copy, hashlib, io, json, math, sys, tempfile, threading, time, unittest
from pathlib import Path
from types import SimpleNamespace as NS
from datetime import datetime, timezone
from unittest.mock import patch
sys.dont_write_bytecode=True
B=Path(__file__).resolve().parent;W=B.parent;S=W/'memory_stage';R=Path('C:/IALD/projetos_pyhton/IALD')
sys.path[:0]=[str(R),str(B)]
import iald_app_providers as providers
import iald_app_spend as spend
import iald_orcamento as budget
import iald_kernel,iald_core_indexado,iald_fontes_publicas,iald_task_session,iald_task_artifacts,iald_motores
from claude_haiku_messages import assemble as assemble_haiku
import claude_native_account as native
from claude_memory_package import load_package
from claude_context_snapshot import snapshot_from_manifest
from claude_route_bridge import HAIKU_PRICES_5M
from claude_profiles import HAIKU
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(Path(p).read_bytes())
METRICS={}
SERVER=W/'app_patch/iald_web_server.py'
SERVER_RAW=SERVER.read_bytes()
tree=ast.parse(SERVER_RAW)
ROUTING_INSTRUCTION='DIRETIVA_SINTETICA_JEV: preserve hipóteses e estatutos; responda sem task_scope.'

def routing_note(name,variable,scope=None):
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    expected=ast.parse(f"if routing_instruction and task_scope is None: {variable} += '\\n'+routing_instruction").body[0]
    nodes=[n for n in ast.walk(function) if isinstance(n,ast.If) and ast.dump(n,include_attributes=False)==ast.dump(expected,include_attributes=False)]
    assert len(nodes)==1
    ns={variable:'BASE_SERVICE_NOTE', 'routing_instruction':ROUTING_INSTRUCTION,'task_scope':scope}
    exec(compile(ast.Module(body=[copy.deepcopy(nodes[0])],type_ignores=[]),'actual_routing_note','exec'),ns)
    return ns[variable]

public_tools=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='PUBLIC_TOOLS' for x in n.targets)))
tools=iald_kernel.tool_definitions()+iald_core_indexado.tool_definitions()+iald_fontes_publicas.tool_definitions()+public_tools
tools=list({t['function']['name']:t for t in tools if t['function']['name'] in providers.TOOL_NAMES}.values())
tools+=iald_task_session.definitions(iald_task_artifacts.TOOL_DEFINITION)
task_names=iald_task_session.NAMES

class StopDispatch(Exception):pass
class ProbeGuard:
    def __init__(self):self.rows=[]
    def check(self,*a):pass
    def reserve(self,*a,**kw):self.rows.append((a,kw));return 'synthetic-hold'

class ProviderChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package=load_package(S/'haiku_runtime',canonical_manifest=S/'manifest_staged.json')
        cls.snapshot=snapshot_from_manifest(read(S/'haiku_runtime/manifest.json'),cls.package)
        cls.prefix=cls.package.prefix
        cls.note=routing_note('_chat_avaliacao','note')
        cls.messages=providers.wire_messages([{'role':'user','content':'Teste sintético de orçamento e contexto.'}],cls.prefix,cls.note)

    def api(self,provider,messages,account=None,post=None,defs=None):
        evaluation=providers.Evaluation.__new__(providers.Evaluation);evaluation.save=lambda record:None
        fake=NS(load_key=lambda:'synthetic-test-key',load_mimo=lambda:'synthetic-test-key')
        with patch.object(providers,'adapter',lambda _:fake):
            evaluation._api(provider,messages,defs if defs is not None else tools,lambda *a:None,
                lambda value:None,threading.Event(),[],{'calls':[]},time.monotonic(),post,
                spending=account,authorize=lambda:True,task_tool_names=task_names)

    def test_01_chinese_real_body_bound_and_hold(self):
        for provider in ('mimo','deepseek'):
            guard=ProbeGuard();account=spend.PublicAccount.__new__(spend.PublicAccount)
            account._lock=threading.RLock();account.pending=None;account.closed=False;account.guard=guard
            account.account_key_hash='a'*64;account.daily=10;account.group=20;account.total=30
            captured=[]
            def fake_post(url,**kwargs):
                self.assertEqual(len(guard.rows),1);captured.append(copy.deepcopy(kwargs['json']));raise StopDispatch()
            with self.assertRaises(StopDispatch):self.api(provider,self.messages,account,fake_post)
            body=captured[0];spec=providers.MODELS[provider];bound=providers.check_window(body,spec['output'])
            self.assertEqual(body['messages'][0]['content'],self.prefix+'\n\n'+self.note)
            self.assertIn(ROUTING_INSTRUCTION,body['messages'][0]['content'])
            without=copy.deepcopy(body);without['messages'][0]['content']=without['messages'][0]['content'].replace('\n'+ROUTING_INSTRUCTION,'')
            baseline_bound=providers.check_window(without,spec['output'])
            self.assertGreater(bound,baseline_bound)
            expected=(bound*max(spec['rates'][:2])+spec['output']*spec['rates'][2])/1e6
            self.assertAlmostEqual(guard.rows[0][0][2],expected)
            self.assertEqual(guard.rows[0][1]['group'],'mimo_public')
            METRICS[provider]={'input_json_utf8_bound':bound,'output_reserve':spec['output'],'structural_margin':4096,
                'remaining_conservative_bound':providers.WINDOW-bound-spec['output']-4096,
                'cold_hold_usd_reference':expected,'window':providers.WINDOW,'tools':len(body['tools']),
                'routing_instruction_included':True,'directive_extra_json_bytes':bound-baseline_bound}

    def test_02_kimi_nested_wire_with_retrieval_margin(self):
        messages=copy.deepcopy(self.messages);messages[0]['content']+='\nFONTES RECUPERADAS:\n'+('é'*24000)
        prompt=json.dumps({'instructions':messages[0]['content'],'conversation':messages[1:]},ensure_ascii=False)
        bound=providers.check_window({'prompt':prompt},providers.MODELS['kimi']['output'])
        METRICS['kimi']={'input_json_utf8_bound':bound,'output_reserve':providers.MODELS['kimi']['output'],
            'structural_margin':4096,'remaining_conservative_bound':providers.WINDOW-bound-providers.MODELS['kimi']['output']-4096,
            'retrieval_fixture_characters':24000,'routing_instruction_included':ROUTING_INSTRUCTION in prompt,'window':providers.WINDOW,'marginal_spend':'SUBSCRIPTION_POLICY_UNCHANGED'}

    def test_03_oversize_denies_before_key_or_transport(self):
        fake=NS(load_key=lambda:self.fail('key read after overflow'),load_mimo=lambda:self.fail('key read after overflow'))
        evaluation=providers.Evaluation.__new__(providers.Evaluation);evaluation.save=lambda r:None
        with patch.object(providers,'adapter',lambda _:fake):
            for provider in ('mimo','deepseek'):
                with self.assertRaises(ValueError):evaluation._api(provider,[{'role':'system','content':self.prefix},{'role':'user','content':'x'*providers.WINDOW}],[],lambda *a:None,lambda *a:None,threading.Event(),[],{'calls':[]},time.monotonic(),lambda *a,**k:self.fail('transport called'))

    def test_04_real_guard_blocks_insufficient_public_budget(self):
        for provider in ('mimo','deepseek'):
            with tempfile.TemporaryDirectory(prefix='spend_',dir=B) as directory:
                account=spend.PublicAccount(directory,'b'*64,0.001,0.01,1)
                with self.assertRaises(budget.BudgetError):self.api(provider,self.messages,account,lambda *a,**k:self.fail('transport called without hold'))
                self.assertIsNone(account.pending);account.close()

    def test_05_uncertain_hold_retained_and_exhaustion_filter(self):
        router_tree=ast.parse((W/'app_patch/iald_auto_router.py').read_bytes())
        node=next(n for n in router_tree.body if isinstance(n,ast.FunctionDef) and n.name=='budget_remaining')
        ns={'math':math,'datetime':datetime,'timezone':timezone};exec(compile(ast.Module(body=[node],type_ignores=[]),'budget_remaining_ast','exec'),ns)
        spec=providers.MODELS['mimo'];body={'model':spec['model'],'messages':self.messages,'max_completion_tokens':spec['output']}
        bound=providers.check_window(body,spec['output']);cap=(bound*max(spec['rates'][:2])+spec['output']*spec['rates'][2])/1e6
        with tempfile.TemporaryDirectory(prefix='spend_',dir=B) as directory:
            account=spend.PublicAccount(directory,'c'*64,cap,cap,cap)
            account.before('mimo',body,bound);key=account.pending['key'];account.close()
            with account.guard._connect() as db:row=db.execute('SELECT cap,actual FROM calls WHERE id=?',(key,)).fetchone()
            self.assertEqual(row,(cap,cap))
            self.assertFalse(ns['budget_remaining'](account.guard,'c'*64,cap,cap,quota_key='c'*64,group='mimo_public',group_limit=cap))

    def test_06_genuine_haiku_measurement_budget_path(self):
        guard=ProbeGuard();cfg=NS(janela=200000,precos=lambda _:HAIKU_PRICES_5M,cota_usuario_usd=1,cota_operador_usd=1,cota_global_usd=10,cota_global_gratuito_usd=5,haiku_public_group_limit=5)
        counter_calls=[]
        def count(payload):
            self.assertIn(ROUTING_INSTRUCTION,payload['messages'][0]['content'])
            counter_calls.append(payload);return self.snapshot.reference_input+37  # Synthetic counter delta; no new native measurement.
        account=native.NativeAccount(motors=NS(GRATUITO='gratuito'),budget=budget,guard=guard,ledger=NS(),cfg=cfg,
            user='synthetic',admin=False,model=HAIKU.model,quota_key='synthetic',plan='gratuito',prefix_tokens=self.snapshot.permanent,count_request=count)
        assembled,_=assemble_haiku(iald_motores,[{'role':'user','content':'Teste sintético.'}],self.prefix,HAIKU.model,[],routing_note('_chat_externo','instrucao'))
        self.assertTrue(assembled[0]['content'].startswith(self.prefix))
        payload={'model':HAIKU.model,'messages':assembled,'max_completion_tokens':4096}
        account.iniciar_chamada(payload)
        self.assertEqual(len(counter_calls),1);self.assertEqual(guard.rows[0][1]['group'],'haiku_public')
        expected=(math.ceil((self.snapshot.reference_input+37)*budget.RESERVATION_MARGIN)*max(HAIKU_PRICES_5M[0],HAIKU_PRICES_5M[1],HAIKU_PRICES_5M[3])+4096*HAIKU_PRICES_5M[2])/1e6
        self.assertAlmostEqual(guard.rows[0][0][2],expected)
        account.pending=None;account.counter=lambda _:200000
        with self.assertRaises(budget.WindowError):account.iniciar_chamada(payload)
        self.assertEqual(len(guard.rows),1)
        METRICS['haiku']={'permanent_tokens':self.snapshot.permanent,'reference_native_tokens':self.snapshot.reference_input,
            'remaining_native_tokens':self.snapshot.reference_remaining,'synthetic_directive_delta_tokens':37,'cold_hold_usd_synthetic_counter_default_5m_rates':expected,
            'native_count_calls_in_test':'INJECTED_FAKE_COUNTER_ONLY; real main receipt is read-only'}

    def test_07_only_reviewed_directive_changes_keep_downstream_guards(self):
        old=ast.parse((R/'iald_web_server.py').read_bytes())
        for name,variable in (('_chat_avaliacao','note'),('_chat_externo','instrucao')):
            left=next(n for n in old.body if isinstance(n,ast.FunctionDef) and n.name==name)
            original=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
            right=copy.deepcopy(original)
            positions=[i for i,arg in enumerate(right.args.kwonlyargs) if arg.arg=='routing_instruction']
            self.assertEqual(len(positions),1);position=positions[0]
            self.assertIsInstance(right.args.kw_defaults[position],ast.Constant)
            self.assertIsNone(right.args.kw_defaults[position].value)
            del right.args.kwonlyargs[position];del right.args.kw_defaults[position]
            expected=ast.parse(f"if routing_instruction and task_scope is None: {variable} += '\\n'+routing_instruction").body[0]
            class RemoveReviewedDirective(ast.NodeTransformer):
                removed=0
                def visit_If(self,node):
                    if ast.dump(node,include_attributes=False)==ast.dump(expected,include_attributes=False):
                        self.removed+=1;return None
                    return self.generic_visit(node)
            remover=RemoveReviewedDirective();right=remover.visit(right)
            self.assertEqual(remover.removed,1)
            self.assertEqual(ast.dump(left,include_attributes=False),ast.dump(right,include_attributes=False),name)
            self.assertEqual(routing_note(name,variable),'BASE_SERVICE_NOTE\n'+ROUTING_INSTRUCTION)
            self.assertEqual(routing_note(name,variable,scope=object()),'BASE_SERVICE_NOTE')
        messages=[{'role':'user','content':'Teste sintético de montagem.'}]
        for provider,model in (('OpenAI','gpt-5.6-luna'),('Anthropic','claude-sonnet-5-5')):
            assembled,_=iald_motores.montar_mensagens(messages,self.prefix,model,[],1000000,4096,
                routing_note('_chat_externo','instrucao'),provedor=provider)
            self.assertTrue(assembled[0]['content'].startswith(self.prefix))
            self.assertEqual(assembled[0]['content'].count(ROUTING_INSTRUCTION),1)
        METRICS['routing_directive']={'only_diff':'keyword routing_instruction=None plus one guarded append before message assembly in each function',
            'functions':['_chat_avaliacao','_chat_externo'],'scope_none_inserts':True,'existing_scope_does_not_duplicate':True,
            'all_other_function_ast_unchanged':True,'openai_sonnet_haiku_real_message_assemblers_keep_directive':True}

if __name__=='__main__':
    output=io.StringIO();result=unittest.TextTestRunner(stream=output,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ProviderChecks));print(output.getvalue())
    assert SERVER.read_bytes()==SERVER_RAW,'Server changed during review'
    report={'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
        'prefix_sha256':sha((S/'haiku_prefix.md').read_bytes()),'provider_reference_checks':METRICS,'network_calls':0,
        'production_ledger_reads_or_writes':0,'actual_current_spend_or_secret_config_read':False,
        'scope':'Synthetic budget values verify fail-closed reservation, not current account availability. Reference fits do not guarantee an arbitrary history/tool output fits.',
        'source_pins':{str(p):sha(p.read_bytes()) for p in [Path(__file__),SERVER,R/'iald_web_server.py',W/'app_patch/iald_auto_router.py',R/'iald_app_providers.py',R/'iald_app_spend.py',R/'iald_orcamento.py',R/'claude_native_account.py']}}
    target=B/('provider_checks_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json');raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();temp=target.with_suffix('.tmp');temp.write_bytes(raw);assert temp.read_bytes()==raw;temp.rename(target)
    print(json.dumps({'receipt':str(target),**report}));sys.exit(0 if result.wasSuccessful() else 1)