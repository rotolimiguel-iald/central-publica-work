import importlib.util,json,sqlite3,sys,tempfile,types,unittest
from pathlib import Path
from unittest.mock import patch
from contextlib import closing
BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.path.insert(0,str(BASE))
STAGE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('iald_orchestrator.nos_packet_candidate',STAGE/'iald_orchestrator/nos_packet.py')
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)

class Integration(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=STAGE);self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  with closing(sqlite3.connect(self.root/'nos_vivo.sqlite3')) as db,db:
   db.execute('create table meta(chave text,valor text)')
   db.execute('create table nos(id text,tipo text,titulo text,caminho text)')
   db.execute('create virtual table busca using fts5(id,titulo)')
   for i,size in [('large',2400),('small',40)]:
    p=self.root/(i+'.md');p.write_text('z'*size)
    db.execute('insert into nos values(?,?,?,?)',(i,'pedra','geometry '+i,str(p)))
    db.execute('insert into busca values(?,?)',(i,'geometry'))
  self.unit={'titulo':'geometry','criterio_de_fechado':'','status':'EM_CURSO'}
  self.ranker=types.ModuleType('iald_orchestrator.layered_retrieval')
  self.ranker.rank_nodes=lambda rows,q:sorted(rows,key=lambda x:x['id'])
 def build(self,memory):
  with patch.object(n,'ROOT',self.root),patch.object(n,'SCIENCE_ROOTS',(self.root,)),patch.object(n,'board_unit',return_value=self.unit),patch.object(n.subprocess,'run',return_value=types.SimpleNamespace(returncode=0,stdout='fixture')),patch.dict(sys.modules,{'iald_orchestrator.layered_retrieval':self.ranker}):
   return n.build('F9.9',5000,canonical_reference={'prompt':memory,'receipt':{'generation':'fixture'}})
 def test_whole_blocks_skip_large_without_losing_small(self):
  r=self.build('a'*3500)
  self.assertLessEqual(len(r['prompt']),5000)
  self.assertEqual(len(r['receipt']['sources']),1)
  self.assertEqual(r['receipt']['sources'][0]['node_id'],'small')
  self.assertFalse(r['receipt']['sources'][0]['block_truncated'])
  self.assertEqual(r['receipt']['skipped_budget'],1)
 def test_required_header_refuses(self):
  with self.assertRaisesRegex(ValueError,'Required scientific header'):self.build('a'*5100)
 def test_cli_read_does_not_construct_transport(self):
  spec=importlib.util.spec_from_file_location('candidate_cli',STAGE/'transport_cli.py');cli=importlib.util.module_from_spec(spec);spec.loader.exec_module(cli)
  self.ranker.retrieve=lambda *a,**k:{'status':'fixture'}
  import io
  with patch.dict(sys.modules,{'iald_orchestrator.layered_retrieval':self.ranker}),patch.object(cli,'Transport',side_effect=AssertionError('Must not construct queue')),patch.object(sys,'stdin',io.StringIO(json.dumps({'operation':'retrieve_knowledge','query':'geometry'}))),patch.object(sys,'stdout',io.StringIO()) as out:
   cli.main();self.assertEqual(json.loads(out.getvalue()),{'status':'fixture'})
 def test_cli_refuses_arbitrary_path(self):
  spec=importlib.util.spec_from_file_location('candidate_cli',STAGE/'transport_cli.py');cli=importlib.util.module_from_spec(spec);spec.loader.exec_module(cli)
  self.ranker.retrieve=lambda *a,**k:None
  import io
  with patch.dict(sys.modules,{'iald_orchestrator.layered_retrieval':self.ranker}),patch.object(sys,'stdin',io.StringIO(json.dumps({'operation':'retrieve_knowledge','query':'x','path':'arbitrary'}))):
   with self.assertRaises(ValueError):cli.main()
if __name__=='__main__':unittest.main()
