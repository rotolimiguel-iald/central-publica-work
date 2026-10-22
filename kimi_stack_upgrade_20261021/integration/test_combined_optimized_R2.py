"""Staged real modules; synthetic graph/queue collaborators; no external calls."""
import ast,copy,hashlib,importlib.util,io,json,socket,sqlite3,subprocess,sys,tempfile,types,unittest
from pathlib import Path
from contextlib import closing
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
tempfile.tempdir=str(HERE)
BASE=Path('C:/IALD/Central de Patentes/Chatgpt/IALD_ORQUESTRACAO_20260923')
sys.path.insert(0,str(BASE))
import iald_orchestrator
iald_orchestrator.__path__.insert(0,str(HERE/'iald_orchestrator'))
from iald_orchestrator import nos_packet as n,layered_retrieval as ranking
from iald_orchestrator.request_controls import normalize
assert Path(n.__file__).resolve()==(HERE/'iald_orchestrator/nos_packet.py').resolve()
assert Path(ranking.__file__).resolve()==(HERE/'iald_orchestrator/layered_retrieval.py').resolve()
class Combined(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=HERE);self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.network=patch.object(socket.socket,'connect',side_effect=AssertionError('NETWORK_FORBIDDEN'));self.network.start();self.addCleanup(self.network.stop)
  with closing(sqlite3.connect(self.root/'nos_vivo.sqlite3')) as db,db:
   db.execute('create table meta(chave text,valor text)');db.execute('create table nos(id text,tipo text,titulo text,texto text,caminho text,sha256 text)');db.execute('create virtual table busca using fts5(id,titulo)')
   for i,size in [('large',3000),('small',40)]:
    p=self.root/(i+'.md');p.write_text('z'*size)
    db.execute('insert into nos values(?,?,?,?,?,?)',(i,'pedra','geometry '+i,'geometry',str(p),hashlib.sha256(p.read_bytes()).hexdigest()))
    db.execute('insert into busca values(?,?)',(i,'geometry'))
  self.unit={'titulo':'geometry','criterio_de_fechado':'','status':'EM_CURSO'}
 def build(self,memory='',**kw):
  with patch.object(n,'ROOT',self.root),patch.object(n,'SCIENCE_ROOTS',(self.root,)),patch.object(n,'board_unit',return_value=self.unit),patch.object(n.subprocess,'run',return_value=types.SimpleNamespace(returncode=0,stdout='fixture')):
   return n.build('F9.9',5000,canonical_reference={'prompt':memory,'receipt':{'generation':'fixture'}},**kw)
 def cli(self,request):
  # Child cannot import Transport or providers, even before constructor checks.
  bootstrap="""import sys,runpy,importlib.abc
class Guard(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname in ('iald_orchestrator.transport','iald_orchestrator.providers','iald_orchestrator.runtime'):raise RuntimeError('FORBIDDEN_IMPORT:'+fullname)
sys.meta_path.insert(0,Guard())
sys.path.insert(0,sys.argv[1])
runpy.run_path(sys.argv[1]+'/transport_cli.py',run_name='__main__')
"""
  result=subprocess.run([sys.executable,'-B','-X','utf8','-c',bootstrap,str(HERE)],input=json.dumps(request).encode(),capture_output=True,timeout=20)
  self.assertEqual(result.returncode,0,result.stderr.decode());return result.stdout,json.loads(result.stdout)
 def test_real_ranker_whole_blocks_skip_large(self):
  r=self.build('a'*3500);self.assertEqual([x['node_id'] for x in r['receipt']['sources']],['small']);self.assertEqual(r['receipt']['skipped_budget'],1);self.assertFalse(r['receipt']['sources'][0]['block_truncated'])
 def test_required_header_overflow(self):
  with self.assertRaisesRegex(ValueError,'Required scientific header'):self.build('a'*5100)
 def test_header_provenance_and_source_prefix_explicit(self):
  r=self.build();self.assertIn('Hashes identify bytes;',r['prompt']);self.assertNotIn(str(self.root),r['prompt']);self.assertTrue(r['receipt']['sources'][0]['source_prefix_truncated']);self.assertTrue(r['receipt']['whole_blocks'])
 def test_source_allowlist_still_applies(self):
  r=self.build(allowed_sources=['small.md']);self.assertEqual([x['node_id'] for x in r['receipt']['sources']],['small'])
 def test_readonly_graph_unchanged(self):
  before=(self.root/'nos_vivo.sqlite3').read_bytes();self.build();self.assertEqual(before,(self.root/'nos_vivo.sqlite3').read_bytes())
 def test_exact_mode_never_pads(self):
  with self.assertRaisesRegex(ValueError,'Insufficient distinct'):self.build(exact=True)
 def test_unsafe_source_is_rejected(self):
  (self.root/'large.md').write_text('credential forbidden')
  r=self.build();self.assertEqual([x['node_id'] for x in r['receipt']['sources']],['small'])
 def test_cli_real_query_no_transport_import(self):
  stdout,r=self.cli({'operation':'retrieve_knowledge','query':'ActionCouplingControls','budget_bytes':16000})
  self.assertTrue(r['ok']);self.assertEqual(len(r['nodes']),1);self.assertEqual(r['nodes'][0]['source']['status'],'VERIFIED_SHA256');self.assertEqual(len(stdout.rstrip(b'\r\n')),r['budget']['serialized_bytes']);self.assertLessEqual(len(stdout)+r['budget']['reserve_bytes'],16000)
 def test_cli_path_override_rejected(self):
  _,r=self.cli({'operation':'retrieve_knowledge','query':'x','path':'not_allowed'});self.assertEqual(r['error'],'unknown_arguments')
 def test_cli_mandatory_unknown_refusal(self):
  _,r=self.cli({'operation':'retrieve_knowledge','query':'x','mandatory_ids':['unknown']});self.assertFalse(r['ok']);self.assertEqual(r['error'],'required_id_outside_catalog')
 def test_cli_budget_refusal(self):
  _,r=self.cli({'operation':'retrieve_knowledge','query':'x','budget_bytes':True});self.assertEqual(r['error'],'invalid_budget')
 def test_cli_missing_query_refusal(self):
  _,r=self.cli({'operation':'retrieve_knowledge'});self.assertEqual(r['error'],'empty_query')

# Reuse five original nos_packet regression methods unchanged (AST), without
# importing original test's Runtime/providers or constructing a live queue.
original=BASE/'test_nos_jev_integration.py';tree=ast.parse(original.read_bytes())
cls=next(v for v in tree.body if isinstance(v,ast.ClassDef))
names={'setUp','test_old_branch_unchanged_and_no_graph_access','test_graph_reservation_and_original_request_preserved','test_forbidden_additional_source_rejected','test_wrong_unit_packet_rejected','test_excessive_combined_context_refused'}
methods=[v for v in cls.body if isinstance(v,ast.FunctionDef) and v.name in names]
for method in methods:
 if method.name=='setUp':
  for node in ast.walk(method):
   if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='TemporaryDirectory':node.keywords.append(ast.keyword(arg='dir',value=ast.Name(id='HERE',ctx=ast.Load())))
reuse=ast.ClassDef(name='OriginalNosRegressions',bases=[ast.Attribute(value=ast.Name(id='unittest',ctx=ast.Load()),attr='TestCase',ctx=ast.Load())],keywords=[],body=methods,decorator_list=[])
exec(compile(ast.fix_missing_locations(ast.Module(body=[reuse],type_ignores=[])),'unchanged original nos_packet regression methods','exec'),globals())
if __name__=='__main__':
 suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(Combined),unittest.defaultTestLoader.loadTestsFromTestCase(OriginalNosRegressions)])
 result=unittest.TextTestRunner(verbosity=2).run(suite)
 report={'status':'PASS' if result.wasSuccessful() else 'FAIL','checks':result.testsRun,'errors':[(str(t),s) for t,s in result.errors+result.failures],'real_ranker_and_cli':True,'original_regression_methods_reused':5,'no_live_queue':True,'network_calls':0,'provider_calls':0}
 (HERE/'COMBINED_TEST_RESULTS_OPTIMIZED_R2.json').write_text(json.dumps(report,indent=2),encoding='utf8');sys.exit(not result.wasSuccessful())
