"""Real transport/account plumbing exercised with local fake HTTP responses."""
import sys,unittest,tempfile,hashlib,types,json,threading,ast
from pathlib import Path
from unittest.mock import patch
W=Path(__file__).resolve().parent
sys.path[:0]=[str(W/'integration'),r'C:/IALD/projetos_pyhton/IALD',r'C:/Users/rotol/AppData/Roaming/Python/Python314/site-packages']
import iald_wallet_runtime as rt
import iald_app_providers as providers
import iald_app_memory as app_memory
from iald_monthly_wallet import Wallet
from iald_orcamento import SpendingGuard,ReservedAccount
OWNER=hashlib.sha256(b'provider-test-owner').hexdigest()

class ProviderTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  self.wallet=Wallet(self.root/'wallet.db');self.wallet.ensure_account(OWNER)
  self.wallet.begin_task(OWNER,'task');self.task=rt.Task(self.wallet,OWNER,'task','tester')
 def tearDown(self):self.tmp.cleanup()
 def test_mimo_tool_rounds_remain_under_one_wallet_after_overrun(self):
  self.wallet.record_cost(OWNER,'task','warmup','3.499999','test','test','measured')
  spec=providers.MODELS['mimo'];calls=[]
  tool={'type':'function','function':{'name':'search_tgl','description':'test','parameters':{'type':'object','properties':{}}}}
  class FakeResponse:
   status_code=200
   def __init__(self,iteration):self.iteration=iteration
   def close(self):pass
   def iter_lines(self,**kw):
    delta=({'tool_calls':[{'index':0,'id':'t1','function':{'name':'search_tgl','arguments':'{}'}}]} if self.iteration==1 else {'content':'concluído'})
    yield ('data: '+json.dumps({'model':spec['model'],'choices':[{'index':0,'delta':delta,'finish_reason':'tool_calls' if self.iteration==1 else 'stop'}],'usage':{'prompt_tokens':100,'completion_tokens':10,'total_tokens':110}})).encode()
    yield b'data: [DONE]'
  def post(*a,**kw):calls.append(rt.current().id);return FakeResponse(len(calls))
  with rt.bind(self.task):
   spending=rt.provider_account(self.root,'mimo',15)
   flow=providers.Evaluation(self.root).stream('mimo',[{'role':'system','content':'science-test'},{'role':'user','content':'consulta'}],[tool],
       lambda name,args:'found',memory_sha256='0'*64,http_post=post,spending=spending,authorize=lambda:True)
   with patch.object(providers,'adapter',return_value=types.SimpleNamespace(load_mimo=lambda:'synthetic-only')):
    frames=list(flow)
  self.task.release()
  self.assertEqual(calls,['task','task'])
  self.assertTrue(any('conclu' in x for x in frames))
  self.assertGreater(self.wallet.snapshot(OWNER)['debt_nano_usd'],0)
  self.assertFalse(self.wallet.begin_task(OWNER,'next')['may_dispatch'])
 def test_claude_cache_creation_settles_at_native_prices(self):
  class Legacy:
   def iniciar_chamada(self,p):pass
   def uso(self,u):pass
   def texto(self,t):pass
   def fechar(self):pass
   def descartar_ultima_chamada(self):pass
  cfg=types.SimpleNamespace(provedor='claude',precos=lambda m:(1.0,.1,5.0,1.25),janela=100000,cota_operador_usd=15,cota_usuario_usd=.000001,cota_global_usd=15,fator_tokens=1)
  guard=rt.Guard(SpendingGuard(self.root/'native.db'),self.task,'claude')
  account=ReservedAccount(guard,Legacy(),cfg,'tester',False,'claude-test')
  with patch('iald_orcamento.input_estimates',return_value=(1000,1000)):
   account.iniciar_chamada({'messages':[],'max_completion_tokens':100})
  account.uso({'prompt_tokens':1000,'completion_tokens':10,'prompt_tokens_details':{'cached_tokens':600,'cache_write_tokens':100}})
  account.fechar();self.task.release()
  # 300 regular + 600 read + 100 write + 10 output, each at its own rate.
  self.assertEqual(self.wallet.snapshot(OWNER)['balance_usd'],'3.499465000')
 def test_server_keepalive_thread_retains_wallet(self):
  source=(W/'integration/iald_web_server.py').read_text(encoding='utf-8')
  tree=ast.parse(source)
  node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='_com_keepalive')
  env={'wallet_runtime':rt,'app_memory':app_memory,'threading':threading,'AGENT_KEEPALIVE_SEC':.01}
  exec(compile(ast.Module(body=[node],type_ignores=[]),'server_helper','exec'),env)
  seen=[]
  def child():
   seen.append(rt.current().id)
   ev=rt.routing_begin(.01);rt.routing_end(ev,{'input_tokens':100})
   return 42
  with rt.bind(self.task):
   gen=env['_com_keepalive'](child)
   while True:
    try:next(gen)
    except StopIteration as result:self.assertEqual(result.value,42);break
  self.task.release();self.assertEqual(seen,['task'])
  self.assertEqual(self.wallet.snapshot(OWNER)['pending_call_count'],0)
 def test_estimated_sandbox_component_is_not_labeled_measured(self):
  guard=rt.sandbox_guard(rt.Guard(SpendingGuard(self.root/'sandbox.db'),self.task,'claude'))
  key=guard.reserve('tester','claude-haiku',1,15,15);guard.settle(key,.026)
  self.task.release()
  self.assertEqual(self.wallet.snapshot(OWNER)['balance_usd'],'3.474000000')

if __name__=='__main__':unittest.main(verbosity=2)
