"""Exact staged/baseline _api AST + actual public-spend.before, injected only stubs.

No application import, key loading, ledger DB, real HTTP or model execution.
"""
import sys
sys.dont_write_bytecode=True
import ast,copy,hashlib,json,math,threading,types,unittest
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
OBS=[]
class BudgetError(ValueError):pass
class StopAtSyntheticTransport(Exception):pass
def functions(path,names,extra_nodes=()):
    tree=ast.parse(path.read_text(encoding='utf-8'))
    return [n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]+list(extra_nodes)
def compile_nodes(nodes,namespace):exec(compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),'isolated_exact_source_AST','exec'),namespace)
def spent_class():
    tree=ast.parse((HERE/'baseline/iald_app_spend.py').read_text(encoding='utf-8'))
    ns=dict(json=json,math=math,threading=threading,BudgetError=BudgetError)
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_positive']
    nodes+=[n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='PublicAccount']
    compile_nodes(nodes,ns);return ns
def provider(path,contains=False):
    tree=ast.parse(path.read_text(encoding='utf-8'));nodes=[]
    for n in tree.body:
        if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('MODELS','WINDOW','MAX_ROUNDS','TOOL_NAMES') for t in n.targets):nodes.append(n)
        if isinstance(n,ast.FunctionDef) and n.name in ('output_budget','check_window','transport_tool_options','scoped_task_names'):nodes.append(n)
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Evaluation')
    method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='_api')
    cls=ast.ClassDef(name='ExactAPI',bases=[],keywords=[],body=[method],decorator_list=[])
    identity=types.SimpleNamespace(project_system_messages=lambda m:m)
    ns=dict(json=json,threading=threading,ProtocolError=ValueError,TASK_TOOL_NAMES=frozenset(),router_media_view=identity,contains_media=lambda m:contains,MediaError=ValueError)
    compile_nodes(nodes+[cls],ns);return ns
def run(path,connector,*,spending=True,tools=False,messages=None,media=False):
    ns=provider(path,media);sp=spent_class();sp['MODELS']=ns['MODELS']
    captured=dict(reservations=[],transport=[],key_stub_calls=0,before=[],saved=[],media_admit=0,media_reserve=0)
    def key_stub():captured['key_stub_calls']+=1;return 'SYNTHETIC_NON_CREDENTIAL'
    ns['adapter']=lambda p:types.SimpleNamespace(load_key=key_stub,load_mimo=key_stub)
    def reserve(*args,**kwargs):captured['reservations'].append((args,kwargs));return 'SYNTHETIC_HOLD_NO_DB'
    account=sp['PublicAccount'].__new__(sp['PublicAccount']);account._lock=threading.RLock();account.closed=False;account.pending=None
    account.account_key_hash='a'*64;account.daily=account.group=account.total=1000;account.guard=types.SimpleNamespace(reserve=reserve)
    def before(p,body,bound):
        captured['before'].append(dict(provider=p,body=copy.deepcopy(body),bound=bound))
        return account.before(p,body,bound)
    account_wrapper=types.SimpleNamespace(before=before,discard_undispatched=lambda:None)
    def http_call(name,fn,url,**kwargs):
        captured['transport'].append(dict(body=copy.deepcopy(kwargs['json']),headers_present=True))
        raise StopAtSyntheticTransport() # Never execute fn/requests.post or provider.
    ns['app_memory']=types.SimpleNamespace(project_messages=lambda m:m,http_call=http_call)
    obj=ns['ExactAPI']();obj.save=lambda rec:captured['saved'].append(copy.deepcopy(rec))
    class Media:
        def admit(self,body,maximum,window):captured['media_admit']+=1;return dict(output_reserved_tokens=maximum,input_tokens_bound=987654)
        def reserve(self,*args):captured['media_reserve']+=1
        def expand(self,body,**kwargs):return body
    offered=[dict(type='function',function=dict(name='search_tgl',parameters=dict(type='object')))] if tools else []
    messages=messages if messages is not None else [dict(role='system',content='SYNTHETIC_SCIENCE_KERNEL_UNCHANGED'),dict(role='user',content='ação 😀 '+('fixture '*100))]
    fake_requests=types.ModuleType('requests');fake_requests.post=lambda *a,**k:(_ for _ in ()).throw(AssertionError('REAL_TRANSPORT_FORBIDDEN'))
    caught=None;record=dict(calls=[])
    with patch.dict(sys.modules,{'requests':fake_requests}):
        try:obj._api(connector,messages,offered,None,None,threading.Event(),[],record,0,None,spending=account_wrapper if spending else None,private_media=Media() if media else None)
        except (BudgetError,ValueError,StopAtSyntheticTransport) as e:caught=e
    captured.update(error=caught,namespace=ns,account=account,messages=messages,record=record)
    return captured

class Regression(unittest.TestCase):
    def test_old_MiMo_plus33_reproduces_exact_refusal(self):
        r=run(HERE/'baseline/iald_app_providers.py','mimo');self.assertIsInstance(r['error'],BudgetError);self.assertIn('Entrada/preços',str(r['error']))
        attempt=r['before'][0];actual=len(json.dumps(attempt['body'],ensure_ascii=False,allow_nan=False).encode());self.assertEqual(actual-attempt['bound'],33);self.assertFalse(r['reservations']);self.assertFalse(r['transport'])
        OBS.append(dict(case='baseline_mimo',old_bound=attempt['bound'],final_bytes=actual,delta=33,refused=True))
    def test_old_DeepSeek_also_refuses_output_field_missing_in_bound(self):
        r=run(HERE/'baseline/iald_app_providers.py','deepseek');self.assertIsInstance(r['error'],BudgetError)
        attempt=r['before'][0];actual=len(json.dumps(attempt['body'],ensure_ascii=False,allow_nan=False).encode());self.assertGreater(actual,attempt['bound']);self.assertFalse(r['reservations']);self.assertFalse(r['transport'])
        OBS.append(dict(case='baseline_deepseek',old_bound=attempt['bound'],final_bytes=actual,delta=actual-attempt['bound'],refused=True))
    def test_fixed_both_connectors_full_body_cost_and_same_output(self):
        for connector in ['mimo','deepseek']:
            for offered in [False,True]:
                with self.subTest(connector=connector,tools=offered):
                    r=run(HERE/'iald_app_providers.py',connector,tools=offered);self.assertIsInstance(r['error'],StopAtSyntheticTransport)
                    attempt=r['before'][0];body=attempt['body'];self.assertEqual(attempt['bound'],len(json.dumps(body,ensure_ascii=False,allow_nan=False).encode()))
                    field='max_tokens' if connector=='deepseek' else 'max_completion_tokens';self.assertEqual(body[field],r['namespace']['MODELS'][connector]['output'])
                    self.assertEqual(len(r['reservations']),1);self.assertEqual(len(r['transport']),1);self.assertEqual(body,r['transport'][0]['body']);self.assertEqual(body['messages'],r['messages'])
                    rates=r['namespace']['MODELS'][connector]['rates'];expected=(attempt['bound']*max(rates[0],rates[1])+body[field]*rates[2])/1000000
                    self.assertAlmostEqual(r['reservations'][0][0][2],expected)
                    OBS.append(dict(case='fixed_'+connector,tools=offered,final_bound=attempt['bound'],output=body[field],synthetic_hold_usd=expected))
    def test_wallet_exempt_no_public_spend_path_unchanged(self):
        for connector in ['mimo','deepseek']:
            r=run(HERE/'iald_app_providers.py',connector,spending=False);self.assertIsInstance(r['error'],StopAtSyntheticTransport);self.assertFalse(r['reservations']);self.assertFalse(r['before']);self.assertEqual(len(r['transport']),1)
    def test_window_overflow_before_key_stub_or_reservation(self):
        messages=[dict(role='system',content='a'*1048576),dict(role='user',content='synthetic')]
        r=run(HERE/'iald_app_providers.py','mimo',messages=messages);self.assertIsInstance(r['error'],ValueError);self.assertNotIsInstance(r['error'],StopAtSyntheticTransport);self.assertFalse(r['key_stub_calls']);self.assertFalse(r['reservations']);self.assertFalse(r['transport']);self.assertEqual(r['messages'],messages)
    def test_media_plan_tokens_branch_not_replaced_by_text_bytes(self):
        r=run(HERE/'iald_app_providers.py','mimo',media=True);self.assertIsInstance(r['error'],StopAtSyntheticTransport);self.assertEqual(r['media_admit'],1);self.assertEqual(r['media_reserve'],1);self.assertFalse(r['before']);self.assertEqual(r['record']['calls'][0]['input_bytes_bound'],987654)
    def test_cost_guard_still_rejects_underestimated_final_body(self):
        ns=provider(HERE/'iald_app_providers.py');sp=spent_class();sp['MODELS']=ns['MODELS'];account=sp['PublicAccount'].__new__(sp['PublicAccount']);account._lock=threading.RLock();account.closed=False;account.pending=None
        account.guard=types.SimpleNamespace(reserve=lambda *a,**k:(_ for _ in ()).throw(AssertionError('must not reserve')))
        body=dict(model='mimo-v2.6-pro',messages=[dict(role='user',content='synthetic')],max_completion_tokens=131072)
        with self.assertRaises(BudgetError):account.before('mimo',body,1)
    def test_only_api_changed_output_selection_and_all_other_functions_identical(self):
        before=ast.parse((HERE/'baseline/iald_app_providers.py').read_text());after=ast.parse((HERE/'iald_app_providers.py').read_text())
        def normalize(tree):
            cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Evaluation');cls.body=[n for n in cls.body if not (isinstance(n,ast.FunctionDef) and n.name=='_api')];return ast.dump(tree,include_attributes=False)
        self.assertEqual(normalize(before),normalize(after))
        b=next(n for n in ast.walk(ast.parse((HERE/'baseline/iald_app_providers.py').read_text())) if isinstance(n,ast.FunctionDef) and n.name=='_api')
        a=next(n for n in ast.walk(ast.parse((HERE/'iald_app_providers.py').read_text())) if isinstance(n,ast.FunctionDef) and n.name=='_api')
        # Normalizing moved check_window proves the rest of _api is unchanged too.
        old=copy.deepcopy(b);new=copy.deepcopy(a)
        for n in ast.walk(old):
            if isinstance(n,ast.If) and any(isinstance(x,ast.Assign) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name) and x.value.func.id=='output_budget' for x in n.orelse):
                n.orelse=[x for x in n.orelse if not (isinstance(x,ast.Assign) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name) and x.value.func.id=='check_window')]
        for n in ast.walk(new):
            if hasattr(n,'body') and isinstance(n.body,list):n.body=[x for x in n.body if not (isinstance(x,ast.If) and isinstance(x.test,ast.UnaryOp) and isinstance(x.test.op,ast.Not) and isinstance(x.test.operand,ast.Call) and isinstance(x.test.operand.func,ast.Name) and x.test.operand.func.id=='contains_media')]
        self.assertEqual(ast.dump(old,include_attributes=False),ast.dump(new,include_attributes=False))

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Regression))
    report=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,observations=OBS,failures=[(str(t),s) for t,s in result.errors+result.failures],real_provider_calls=0,credential_reads=0,ledger_database_writes=0,runtime_edits=0,scope='Exact original/staged _api and unchanged public-spend.before extracted via AST. Synthetic adapter key return, reserve recorder and stop-at-transport. Whole app/provider modules never imported.')
    (HERE/'TEST_RESULTS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
