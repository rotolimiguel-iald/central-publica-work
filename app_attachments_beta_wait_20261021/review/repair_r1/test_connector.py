import ast,base64,copy,json,hashlib,threading,time,types,sys,unittest
from pathlib import Path
P=Path(__file__).resolve().parent
source=(P/'stage/iald_app_providers.py').read_text(encoding='utf-8');tree=ast.parse(source)
wanted={'admission_input_bound','output_budget','check_window','usage_cost','transport_tool_options','scoped_task_names'}
body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in wanted]
api=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Evaluation');api=next(n for n in api.body if isinstance(n,ast.FunctionDef) and n.name=='_api');body.append(api)
ns=dict(json=json,base64=base64,binascii=__import__('binascii'),time=time,WINDOW=1048576,MAX_ROUNDS=4,MAX_TOOLS=4,MAX_PARSED_TOOLS=32,TOOL_NAMES=frozenset(['search_tgl']),TASK_TOOL_NAMES=frozenset(),ProtocolError=RuntimeError,contains_media=lambda m:False)
for n in tree.body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MODELS' for t in n.targets):exec(compile(ast.Module(body=[n],type_ignores=[]),'model-constants','exec'),ns)
exec(compile(ast.Module(body=body,type_ignores=[]),'actual-api-isolated','exec'),ns)
# No installed connector import. This module is the isolated zero-provider stub.
key_reads=[];ns['adapter']=lambda p:types.SimpleNamespace(load_mimo=lambda:key_reads.append(p) or 'PUBLIC_SYNTHETIC_NOT_A_CREDENTIAL',load_key=lambda:key_reads.append(p) or 'PUBLIC_SYNTHETIC_NOT_A_CREDENTIAL')
ns['router_media_view']=types.SimpleNamespace(project_system_messages=lambda m:m)
ns['app_memory']=types.SimpleNamespace(project_messages=lambda m:copy.deepcopy(m),http_call=lambda label,fn,*a,**kw:fn(*a,**kw),call=lambda label,fn,*a:fn(*a),tool_result=lambda *a:None)
wire=[]
raw=Path('C:\\IALD\\Central de Patentes\\work\\app_attachments_beta_wait_20261021\\large_two_colors.png').read_bytes();url='data:image/png;base64,'+base64.b64encode(raw).decode()
original=[{'role':'system','content':'FIXED_KERNEL_FULL\n'+'k'*600000},{'role':'user','content':[{'type':'image_url','image_url':{'url':url}},{'type':'text','text':'Quais cores?'}]}]
class Response:
 status_code=200
 def __init__(self,n):self.n=n
 def close(self):pass
 def iter_lines(self,**kw):
  delta=({'tool_calls':[{'index':0,'id':'public_tool_1','function':{'name':'search_tgl','arguments':'{}'}}]} if self.n==1 else {'content':'Vermelho e azul.'})
  yield ('data: '+json.dumps({'model':'mimo-v2.6-pro','choices':[{'index':0,'delta':delta,'finish_reason':'tool_calls' if self.n==1 else 'stop'}],'usage':{'prompt_tokens':1,'completion_tokens':1,'total_tokens':2}})).encode()
  yield b'data: [DONE]'
def post(_url,**kw):wire.append(copy.deepcopy(kw['json']));return Response(len(wire))
class Tests(unittest.TestCase):
 def test_real_api_two_rounds_complete_final_body_no_remote(self):
  record={'calls':[],'first_text_seconds':None};messages=copy.deepcopy(original);emitted=[];settled=[]
  spending=types.SimpleNamespace(before=lambda p,b,bound:settled.append(('before',bound)),settle=lambda m:settled.append(('settle',m)),discard_undispatched=lambda:None)
  ns['_api'](types.SimpleNamespace(save=lambda r:None),'mimo',messages,[{'type':'function','function':{'name':'search_tgl','parameters':{'type':'object'}}}],lambda *a:'PUBLIC_TOOL_RESULT',emitted.append,threading.Event(),[],record,time.monotonic(),post,spending)
  self.assertEqual(len(wire),2);self.assertEqual(len(record['calls']),2);self.assertTrue(all(x['status']=='completed' for x in record['calls']))
  for final in wire:
   self.assertEqual(final['messages'][0],original[0]);self.assertEqual(final['messages'][1],original[1]);self.assertEqual(final['max_completion_tokens'],131072)
   self.assertEqual(ns['check_window'](final,131072),record['calls'][wire.index(final)]['input_bytes_bound'])
  self.assertEqual([x[0] for x in settled],['before','settle','before','settle'])
  self.assertTrue(any('choices' in x for x in emitted))
 def test_invalid_image_refuses_before_stub_key_load(self):
  before=len(key_reads);messages=copy.deepcopy(original);messages[1]['content'][0]['image_url']['url']='data:image/png;base64,!!!!'
  with self.assertRaises(ValueError):ns['_api'](types.SimpleNamespace(save=lambda r:None),'mimo',messages,[],None,lambda x:None,threading.Event(),[],{'calls':[]},time.monotonic(),lambda *a,**k:(_ for _ in()).throw(AssertionError('unexpected HTTP')))
  self.assertEqual(len(key_reads),before)
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
(P/'CONNECTOR_TESTS.json').write_text(json.dumps({'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,'failures':len(result.failures)+len(result.errors),'rounds':len(wire),'scope':'Actual staged Evaluation._api AST-isolated, real admission functions, two tool rounds and full wire preserved. Stubs for authenticated memory projection/ledger/connector/HTTP; no DB/credentials/provider; sample usage artificial, not measured model tokens.'},indent=2),encoding='utf-8')
raise SystemExit(not result.wasSuccessful())
