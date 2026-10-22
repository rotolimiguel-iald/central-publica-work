import copy,hashlib,json,sqlite3,tempfile,unittest,subprocess,sys
from pathlib import Path
from unittest.mock import patch
from contextlib import contextmanager
@contextmanager
def database(path):
 c=sqlite3.connect(path)
 try:
  with c:yield c
 finally:c.close()
sys.path.insert(0,str(Path(__file__).resolve().parent/'iald_orchestrator'))
import layered_retrieval as m
HERE=Path(__file__).resolve().parent
class RankingTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=HERE);self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.db=self.root/'graph.sqlite3';self.cat={'required_ids':[],'coverage':'synthetic explicit protection annotations','entries':{}}
  with database(self.db) as c:c.execute('CREATE TABLE nos(id TEXT PRIMARY KEY,tipo TEXT,titulo TEXT,texto TEXT,estatuto TEXT,status TEXT,quando TEXT,quem TEXT,caminho TEXT,sha256 TEXT,fonte TEXT)')
  self.add('a','alpha ação 😀');self.add('b','beta')
 def add(self,i,text,role='optional',protected=(),kind='pedra'):
  f=self.root/(i+'.txt');f.write_text(text,encoding='utf8')
  with database(self.db) as c:c.execute('INSERT INTO nos VALUES(?,?,?,?,?,?,?,?,?,?,?)',(i,kind,i,text,'DECLARADO','candidate','2026-01-01','synthetic',str(f),m.digest(f.read_bytes()),'synthetic'))
  self.cat['entries'][i]={'path':str(f),'role':role,'protected_ids':list(protected),'scope':'scientific','annotation_coverage':'synthetic explicit'}
 def get(self,q='alpha',budget=12000,ids=()):return m._retrieve(q,budget,ids,self.db,self.cat,(self.root,))
 def test_whole_utf8_budget_readonly(self):
  before=self.db.read_bytes();r=self.get();self.assertEqual(r['nodes'][0]['row']['texto'],'alpha ação 😀');self.assertEqual(r['budget']['serialized_bytes'],len(m.wire(r)));self.assertLessEqual(len(m.wire(r))+m.RESERVE_BYTES,12000);self.assertEqual(before,self.db.read_bytes())
 def test_exact_anchor_outranks_recency(self):
  rows=[{'id':'other','titulo':'alpha','texto':'alpha','quando':'9999','centrality':999},{'id':'alpha','titulo':'x','quando':'0001'}]
  before=copy.deepcopy(rows);self.assertEqual(m.rank_nodes(rows,'alpha')[0]['id'],'other')
  # Both exact title/id are anchors: use a nonexact distractor for strict precedence.
  rows[0]['titulo']='alpha extra';self.assertEqual(m.rank_nodes(rows,'alpha')[0]['id'],'alpha');self.assertEqual(before[0]['centrality'],999)
 def test_diversity_ties_before_recency(self):
  rows=[dict(id='a',tipo='pedra',texto='alpha',quando='2026'),dict(id='b',tipo='pedra',texto='alpha',quando='2025'),dict(id='c',tipo='entrega_doc',texto='alpha',quando='2020')]
  self.assertEqual([r['id'] for r in m.rank_nodes(rows,'alpha')],['a','c','b'])
 def test_required_even_no_relevance(self):
  self.cat['entries']['b']['role']='errata';self.assertIn('b',[n['row']['id'] for n in self.get()['nodes']])
 def test_contradiction_closure_no_lexical_detection(self):
  self.cat['entries']['a']['protected_ids']=['b'];self.assertEqual({n['row']['id'] for n in self.get()['nodes']},{'a','b'})
 def test_mandatory_overflow_refuses_whole(self):
  with database(self.db) as c:c.execute('UPDATE nos SET texto=? WHERE id=?',('😀'*3000,'a'))
  with self.assertRaisesRegex(m.Refusal,'overflow'):self.get(budget=4096,ids=['a'])
 def test_omitted_recoverable(self):
  r=self.get();self.assertEqual(r['omitted'][0]['id'],'b');r2=self.get('',ids=r['omitted'][0]['recover']['mandatory_ids']);self.assertEqual(r2['nodes'][0]['row']['id'],'b')
 def test_absence_not_claimed(self):
  r=self.get('zzzz');self.assertFalse(r['coverage']['no_hit_means_absent']);self.assertEqual(r['nodes'],[])
 def test_missing_pin_declared(self):
  with database(self.db) as c:c.execute("UPDATE nos SET sha256='' WHERE id='a'")
  self.assertEqual(self.get()['nodes'][0]['source']['status'],'MISSING_PIN')
 def test_missing_source_declared(self):
  (self.root/'a.txt').unlink();self.assertEqual(self.get()['nodes'][0]['source']['status'],'MISSING_SOURCE')
 def test_hash_mismatch_refuses(self):
  (self.root/'a.txt').write_text('changed');
  with self.assertRaisesRegex(m.Refusal,'hash_mismatch'):self.get()
 def test_protection_missing_refuses(self):
  self.cat['entries']['a']['protected_ids']=['unknown']
  with self.assertRaisesRegex(m.Refusal,'protection_outside'):self.get()
 def test_required_node_missing(self):
  with database(self.db) as c:c.execute("DELETE FROM nos WHERE id='b'")
  with self.assertRaisesRegex(m.Refusal,'mandatory_node_missing'):self.get(ids=['b'])
 def test_path_escape_denied_before_leaf_open(self):
  self.cat['entries']['a']['path']=str(self.root.parent/'outside.txt')
  with database(self.db) as c:c.execute('UPDATE nos SET caminho=? WHERE id=?',(self.cat['entries']['a']['path'],'a'))
  with self.assertRaisesRegex(m.Refusal,'source_outside_scope'):self.get()
 def test_scope_and_secrets_denied(self):
  with self.assertRaisesRegex(m.Refusal,'scope_denied'):self.get('Escritório')
  with database(self.db) as c:c.execute('UPDATE nos SET texto=? WHERE id=?',('sk-'+'A'*30,'a'))
  with self.assertRaisesRegex(m.Refusal,'node_scope_denied'):self.get()
 def test_unknown_required_not_ignored(self):
  with self.assertRaisesRegex(m.Refusal,'required_id_outside'):self.get(ids=['unknown'])
 def test_api_no_path_override(self):
  with self.assertRaises(TypeError):m.retrieve('a',dbpath=self.db)
  p=subprocess.run([sys.executable,'-B',str(HERE/'iald_orchestrator/layered_retrieval.py')],input=b'{"query":"alpha","path":"elsewhere"}',capture_output=True)
  self.assertEqual(json.loads(p.stdout)['error'],'unknown_arguments')
 def test_public_pin_failure_visible(self):
  with patch.object(m,'CATALOG_SHA256','0'*64):self.assertEqual(m.retrieve('a')['error'],'catalog_pin_mismatch')
 def test_no_unselected_leaf_read(self):
  original=Path.open;seen=[]
  def observe(p,*a,**k):
   if p.suffix=='.txt':seen.append(p.name)
   return original(p,*a,**k)
  with patch.object(Path,'open',observe):self.get('alpha')
  self.assertEqual(seen,['a.txt'])
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(RankingTests)
 result=unittest.TextTestRunner(verbosity=2).run(suite)
 report={'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,'failures':[(str(t),s) for t,s in result.failures+result.errors],'network_calls':0,'synthetic_databases_only':True}
 (HERE/'TEST_RANKING_OPTIMIZED_R2.json').write_text(json.dumps(report,indent=2),encoding='utf8');sys.exit(not result.wasSuccessful())
