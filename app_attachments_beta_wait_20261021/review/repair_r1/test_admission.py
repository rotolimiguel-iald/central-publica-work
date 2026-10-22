import ast,base64,copy,hashlib,json,time,unittest,io
from pathlib import Path
from PIL import Image
P=Path(__file__).resolve().parent

def load(name):
 s=(P/name).read_text(encoding='utf-8'); tree=ast.parse(s)
 names={'admission_input_bound','output_budget','check_window','image_parts','wire_messages'}
 funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
 ns=dict(json=json,base64=base64,binascii=__import__('binascii'),WINDOW=1048576)
 exec(compile(ast.Module(body=funcs,type_ignores=[]),str(P/name),'exec'),ns)
 return ns
old=load('baseline/iald_app_providers.py');new=load('stage/iald_app_providers.py')
raw=Path('C:\\IALD\\Central de Patentes\\work\\app_attachments_beta_wait_20261021\\large_two_colors.png').read_bytes(); url='data:image/png;base64,'+base64.b64encode(raw).decode()
payload={'model':'mimo-v2.6-pro','messages':[{'role':'system','content':'SCIENCE_FIXED\n'+'k'*600000},{'role':'user','content':[{'type':'image_url','image_url':{'url':url}},{'type':'text','text':'Quais cores?'}]}],'tools':[]}
observations={}
class Tests(unittest.TestCase):
 def test_live_fixture_regression(self):
  before=copy.deepcopy(payload)
  with self.assertRaises(ValueError):old['output_budget'](payload,131072)
  start=time.perf_counter(); reserve=new['output_budget'](payload,131072);final={**payload,'max_completion_tokens':reserve};bound=new['check_window'](final,reserve)
  observations.update(raw_image_bytes=len(raw),old_json_bytes=len(json.dumps(payload,ensure_ascii=False).encode()),new_input_estimate=bound,reserve=reserve,cpu_ms=round((time.perf_counter()-start)*1000,3),image_geometry=Image.open(io.BytesIO(raw)).size,image_sha256=hashlib.sha256(raw).hexdigest())
  self.assertEqual(before,payload);self.assertEqual(reserve,131072);self.assertLess(bound+reserve+4096,1048576)
 def test_text_connectors_unchanged(self):
  for model in ['kimi-code/k3','deepseek-flash','mimo-v2.6-pro']:
   p={'model':model,'messages':[{'role':'user','content':'文档🙂'*1000}],'tools':[]}
   self.assertEqual(new['check_window'](p,131072),old['check_window'](p,131072))
 def test_document_not_subtracted(self):
  p={'messages':[{'role':'user','content':'[ARQUIVO: doc]\n'+'d'*1100000+'\n[FIM]'}]}
  with self.assertRaises(ValueError):new['output_budget'](p,131072)
 def test_full_final_field_still_counted(self):
  p={'messages':[{'role':'user','content':'hi'}]};f={**p,'max_completion_tokens':131072}
  self.assertEqual(new['check_window'](f,131072)-new['check_window'](p,131072),len(json.dumps(f).encode())-len(json.dumps(p).encode()))
 def test_other_fields_not_subtracted(self):
  p={'messages':[],'metadata':url};self.assertEqual(new['admission_input_bound'](p),len(json.dumps(p).encode()))
 def test_corrupt_base64(self):
  p=copy.deepcopy(payload);p['messages'][1]['content'][0]['image_url']['url']='data:image/png;base64,!!!!'
  with self.assertRaises(ValueError):new['output_budget'](p,131072)
 def test_mime_mismatch(self):
  p=copy.deepcopy(payload);p['messages'][1]['content'][0]['image_url']['url']=url.replace('image/png','image/jpeg')
  with self.assertRaises(ValueError):new['output_budget'](p,131072)
 def test_truncated_image(self):
  p=copy.deepcopy(payload);p['messages'][1]['content'][0]['image_url']['url']='data:image/png;base64,'+base64.b64encode(raw[:100]).decode()
  with self.assertRaises(ValueError):new['output_budget'](p,131072)
 def test_pixel_bomb(self):
  data=io.BytesIO();Image.new('1',(5100,5100)).save(data,format='PNG')
  p=copy.deepcopy(payload);p['messages'][1]['content'][0]['image_url']['url']='data:image/png;base64,'+base64.b64encode(data.getvalue()).decode()
  with self.assertRaises(ValueError):new['output_budget'](p,131072)
 def test_three_occurrences_counted(self):
  small=io.BytesIO();Image.new('RGB',(16,16)).save(small,format='PNG');u='data:image/png;base64,'+base64.b64encode(small.getvalue()).decode()
  part={'type':'image_url','image_url':{'url':u}};a={'messages':[{'role':'user','content':[part]}]};b={'messages':[{'role':'user','content':[part,part,part]}]}
  self.assertGreater(new['admission_input_bound'](b),2*new['admission_input_bound'](a))
  with self.assertRaises(ValueError):new['admission_input_bound']({'messages':[{'role':'user','content':[part]*4}]})
 def test_image_history_preserved(self):
  p=copy.deepcopy(payload);p['messages']+=[{'role':'assistant','content':'Answer'},{'role':'user','content':'continue'}];snap=copy.deepcopy(p)
  new['output_budget'](p,131072);self.assertEqual(p,snap)
 def test_12mp_real_jpeg_with_full_science_and_output(self):
  data=(P/'synthetic_12mp.jpg').read_bytes();p=copy.deepcopy(payload)
  p['messages'][1]['content'][0]['image_url']['url']='data:image/jpeg;base64,'+base64.b64encode(data).decode()
  before=copy.deepcopy(p);start=time.perf_counter();reserve=new['output_budget'](p,131072);bound=new['check_window']({**p,'max_completion_tokens':reserve},reserve)
  self.assertEqual(p,before);self.assertEqual(reserve,131072);self.assertLess(bound+reserve+4096,1048576)
  with self.assertRaises(ValueError):old['output_budget'](p,131072)
  observations['jpeg_12mp']={'bytes':len(data),'old_json_bytes':len(json.dumps(p,ensure_ascii=False).encode()),'new_input_estimate':bound,'output_reserved':reserve,'cpu_ms':round((time.perf_counter()-start)*1000,3),'width':4000,'height':3000}
 def test_no_provider_or_wallet_diff(self):
  a=ast.parse((P/'baseline/iald_app_providers.py').read_text());b=ast.parse((P/'stage/iald_app_providers.py').read_text());allowed={'output_budget','check_window','admission_input_bound'}
  strip=lambda t:ast.dump(ast.Module(body=[n for n in t.body if not(isinstance(n,ast.FunctionDef) and n.name in allowed)],type_ignores=[]))
  self.assertEqual(strip(a),strip(b))
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
(P/'BACKEND_TESTS.json').write_text(json.dumps({'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,'failures':len(result.failures)+len(result.errors),'observations':observations,'scope':'AST-isolated real admission functions; local PNG fixture; zero imports of runtime modules/provider/network/DB. Image tokens engineering ESTIMATE, not vendor tokenizer.'},indent=2),encoding='utf-8')
raise SystemExit(not result.wasSuccessful())
