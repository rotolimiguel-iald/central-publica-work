"""Real isolated SQLite ledgers and wallet; zero provider modules or HTTP."""
import ast,base64,copy,hashlib,importlib.util,json,math,sqlite3,sys,types,unittest,uuid
from pathlib import Path
from decimal import Decimal
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'baseline'))
# Pure installed admission implementation; do not import runtime/provider dependencies.
tree=ast.parse((R/'baseline/iald_app_providers.py').read_text(encoding='utf-8'))
selected=[n for n in tree.body if (isinstance(n,ast.FunctionDef) and n.name in {'admission_input_bound','output_budget','check_window','usage_cost'}) or (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'MODELS','WINDOW'} for t in n.targets))]
providers=types.ModuleType('iald_app_providers');providers.__dict__.update(json=json,base64=base64,binascii=__import__('binascii'))
exec(compile(ast.Module(body=selected,type_ignores=[]),'installed-pure-admission','exec'),providers.__dict__);sys.modules[providers.__name__]=providers
m=types.ModuleType('iald_memoria_canonica');m.payload_tokens=lambda *a:(_ for _ in ()).throw(AssertionError('unexpected tokenizer path'));sys.modules[m.__name__]=m
m=types.ModuleType('iald_motores');m.CPT=2.91;sys.modules[m.__name__]=m
import iald_orcamento as budget
import iald_wallet_runtime as runtime
from iald_monthly_wallet import Wallet

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
old=load('spend_baseline',R/'baseline/iald_app_spend.py');new=load('spend_staged',R/'stage/iald_app_spend.py')
raw=(R.parent.parent/'large_two_colors.png').read_bytes()
body={'model':'mimo-v2.6-pro','messages':[{'role':'system','content':'FIXED_SCIENCE\n'+'k'*600000},{'role':'user','content':[{'type':'image_url','image_url':{'url':'data:image/png;base64,'+base64.b64encode(raw).decode()}},{'type':'text','text':'[ARQUIVO: fixture.pdf]\nPUBLIC_SYNTHETIC_PDF_RED_BLUE\n[FIM]\nQuais cores?'}]}],'stream':True,'max_completion_tokens':131072}
owner='a'*64;observations=[]
def fixture(module=new,exempt=False,limit=10):
 folder=R/'isolated'/uuid.uuid4().hex;folder.mkdir(parents=True)
 wallet=Wallet(folder/'wallet.sqlite3');wallet.ensure_account(owner,exempt=exempt)
 receipt=wallet.begin_task(owner,'synthetic_attachment_job');assert receipt['may_dispatch']
 task=runtime.Task(wallet,owner,'synthetic_attachment_job','synthetic_user')
 with runtime.bind(task):account=module.PublicAccount(folder,owner,limit,limit,limit)
 return account,wallet,task,folder

def rows(account):
 with sqlite3.connect(account.guard.original.path if isinstance(account.guard,runtime.Guard) else account.guard.path) as db:
  return db.execute('SELECT id,model,cap,actual,status FROM calls ORDER BY rowid').fetchall()

class Tests(unittest.TestCase):
 def test_baseline_exact_failure_zero_ledger_and_wallet_calls(self):
  account,wallet,task,_=fixture(old);bound=providers.check_window(body,131072)
  with self.assertRaisesRegex(budget.BudgetError,'Entrada/preços não verificáveis'):account.before('mimo',body,bound)
  self.assertEqual(rows(account),[]);self.assertEqual(wallet.pending_calls(owner)['calls'],[])
 def test_image_pdf_real_ledger_wallet_reservation_and_settlement(self):
  account,wallet,task,folder=fixture();before=copy.deepcopy(body);bound=providers.check_window(body,131072)
  key=account.before('mimo',body,bound);ledger=rows(account);self.assertEqual(len(ledger),1);self.assertEqual(ledger[0][4],'reserved')
  expected=(bound*.435+131072*.87)/1e6;self.assertAlmostEqual(ledger[0][2],expected)
  pending=wallet.pending_calls(owner);self.assertEqual(len(pending['calls']),1)
  measured=providers.usage_cost('mimo',{'prompt_tokens':2000,'completion_tokens':20,'total_tokens':2020,'prompt_tokens_details':{'cached_tokens':1000}})
  balance_before=Decimal(str(wallet.snapshot(owner)['balance_usd']));account.settle(measured)
  self.assertEqual(rows(account)[0][4],'settled');self.assertAlmostEqual(rows(account)[0][3],measured['cost_estimate_usd']);self.assertEqual(wallet.pending_calls(owner)['calls'],[])
  balance_after=Decimal(str(wallet.snapshot(owner)['balance_usd']));self.assertEqual(balance_before-balance_after,Decimal(str(measured['cost_estimate_usd'])).quantize(Decimal('.000000001')))
  self.assertEqual(body,before);self.assertTrue(task.release())
  observations.append({'scenario':'image_png1592884_plus_extracted_pdf','input_estimate':bound,'raw_final_json_bytes':len(json.dumps(body,ensure_ascii=False).encode()),'reservation_usd':ledger[0][2],'settled_usd':rows(account)[0][3],'ledger':str(Path(account.guard.original.path)),'wallet':str(folder/'wallet.sqlite3'),'provider_dispatches':0})
 def test_uncertainty_consumes_full_cap_no_free_call(self):
  account,wallet,task,_=fixture();account.before('mimo',body,providers.check_window(body,131072));cap=rows(account)[0][2];account.close()
  row=rows(account)[0];self.assertEqual(row[4],'estimated_upper_bound');self.assertEqual(row[3],cap);self.assertEqual(wallet.pending_calls(owner)['calls'],[])
 def test_underestimate_refused_no_reservation(self):
  account,wallet,_,_=fixture()
  with self.assertRaises(budget.BudgetError):account.before('mimo',body,providers.check_window(body,131072)-1)
  self.assertEqual(rows(account),[]);self.assertEqual(wallet.pending_calls(owner)['calls'],[])
 def test_tampered_image_revalidated_no_reservation(self):
  account,wallet,_,_=fixture();bad=copy.deepcopy(body);bad['messages'][1]['content'][0]['image_url']['url']='data:image/png;base64,!!!!'
  with self.assertRaises(budget.BudgetError):account.before('mimo',bad,99999999)
  self.assertEqual(rows(account),[])
 def test_prices_must_still_be_finite_positive(self):
  account,_,_,_=fixture();rates=providers.MODELS['mimo']['rates']
  try:
   providers.MODELS['mimo']['rates']=(float('nan'),.0036,.87)
   with self.assertRaises(budget.BudgetError):account.before('mimo',body,providers.admission_input_bound(body))
  finally:providers.MODELS['mimo']['rates']=rates
  self.assertEqual(rows(account),[])
 def test_model_and_output_field_checks_preserved(self):
  for change in [{'model':'wrong'},{'max_tokens':131072},{'max_completion_tokens':131073},{'n':2}]:
   account,_,_,_=fixture();p={**body,**change}
   with self.assertRaises(budget.BudgetError):account.before('mimo',p,99999999)
   self.assertEqual(rows(account),[])
 def test_text_deepseek_cost_and_maximum_output_unchanged(self):
  account,_,_,_=fixture();p={'model':'deepseek-flash','messages':[{'role':'user','content':'PUBLIC_DOCUMENT🙂'*100}],'max_tokens':16384};size=len(json.dumps(p,ensure_ascii=False,allow_nan=False).encode());self.assertEqual(providers.admission_input_bound(p),size)
  account.before('deepseek',p,size);self.assertAlmostEqual(rows(account)[0][2],(size*.30+393216*1.20)/1e6);account.discard_undispatched();self.assertEqual(rows(account)[0][3],0)
 def test_global_ceiling_preserved(self):
  account,wallet,_,_=fixture(limit=.001)
  with self.assertRaises(budget.BudgetError):account.before('mimo',body,providers.check_window(body,131072))
  self.assertEqual(rows(account),[]);self.assertEqual(wallet.pending_calls(owner)['calls'],[])
 def test_pending_call_cannot_reserve_again(self):
  account,_,_,_=fixture();bound=providers.check_window(body,131072);account.before('mimo',body,bound)
  with self.assertRaises(budget.BudgetError):account.before('mimo',body,bound)
  self.assertEqual(len(rows(account)),1)
 def test_exempt_account_keeps_global_ceiling(self):
  account,wallet,_,_=fixture(exempt=True,limit=.001);self.assertTrue(wallet.snapshot(owner)['exempt'])
  with self.assertRaises(budget.BudgetError):account.before('mimo',body,providers.check_window(body,131072))
  self.assertEqual(rows(account),[])
 def test_only_before_calculation_changed(self):
  a=ast.parse((R/'baseline/iald_app_spend.py').read_text());b=ast.parse((R/'stage/iald_app_spend.py').read_text())
  for t in [a,b]:
   for n in t.body:
    if isinstance(n,ast.ImportFrom) and n.module=='iald_app_providers':n.names=[ast.alias(name='MODELS')]
    if isinstance(n,ast.ClassDef):n.body=[x for x in n.body if not(isinstance(x,ast.FunctionDef) and x.name=='before')]
  self.assertEqual(ast.dump(a),ast.dump(b))
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
(R/'TESTS.json').write_text(json.dumps({'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,'failures':len(result.failures)+len(result.errors),'observations':observations,'scope':'Full copied PublicAccount and SpendingGuard plus real wallet_runtime.Guard/Task/Wallet; actual SQLite inserts/settlements in isolated workspace dirs. Actual installed admission_input_bound AST loaded. No provider connector/HTTP/model/secrets imported or called. Remote execution zero.'},indent=2),encoding='utf-8')
raise SystemExit(not result.wasSuccessful())
