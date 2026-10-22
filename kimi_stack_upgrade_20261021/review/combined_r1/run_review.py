import sys
sys.dont_write_bytecode=True
import contextlib,hashlib,importlib.util,io,json,os,sqlite3,tempfile,types,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parent
def guard(event,args):
    if event in ('socket.connect','socket.getaddrinfo'):raise RuntimeError('NETWORK_FORBIDDEN')
    if event=='open':
        path,mode,flags=args
        writing=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and isinstance(path,(str,bytes,os.PathLike)) and not Path(path).resolve().is_relative_to(ROOT):raise RuntimeError('WRITE_OUTSIDE_REVIEW')
sys.addaudithook(guard)
import test_envelope as envelope
import test_layered_retrieval as ranking_tests
def mod(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
rank=mod('isolated_stage.layered_retrieval',ROOT/'stage/iald_orchestrator/layered_retrieval.py')
nos=mod('isolated_stage.nos_packet',ROOT/'stage/iald_orchestrator/nos_packet.py')
op=mod('isolated_stage.operational_memory',ROOT/'stage/iald_orchestrator/operational_memory.py')
OBS=[]
class Combined(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT);self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.canonical=self.root/'canonical';self.canonical.mkdir();self.manifest=envelope.fixture(self.canonical,anchor_size=100)
        with contextlib.closing(sqlite3.connect(self.root/'nos_vivo.sqlite3')) as db,db:
            db.execute('create table meta(chave text,valor text)')
            db.execute('create table nos(id text,tipo text,titulo text,texto text,caminho text,sha256 text)')
            db.execute('create virtual table busca using fts5(id,titulo)')
            for ident,size in [('geometry',2400),('small',40)]:
                p=self.root/(ident+'.md');p.write_text('z'*size)
                db.execute('insert into nos values(?,?,?,?,?,?)',(ident,'pedra',ident,'geometry',str(p),hashlib.sha256(p.read_bytes()).hexdigest()))
                db.execute('insert into busca values(?,?)',(ident,'geometry'))
        self.unit={'titulo':'geometry','criterio_de_fechado':'','status':'EM_CURSO'}
        self.stack=contextlib.ExitStack();self.addCleanup(self.stack.close)
        for name,value in [('ROOT',self.root),('SCIENCE_ROOTS',(self.root,))]:self.stack.enter_context(patch.object(nos,name,value))
        self.stack.enter_context(patch.object(nos,'board_unit',return_value=self.unit))
        self.stack.enter_context(patch.object(nos.subprocess,'run',return_value=types.SimpleNamespace(returncode=0,stdout='synthetic')))
    def test_real_rank_whole_small_after_oversized_anchor(self):
        p=nos.build('F9.9',5000,canonical_reference={'prompt':'a'*3500,'receipt':{'generation':'fixture'}})
        self.assertEqual([x['node_id'] for x in p['receipt']['sources']],['small'])
        self.assertEqual(p['receipt']['skipped_budget'],1);self.assertLessEqual(len(p['prompt']),5000)
        self.assertFalse(p['receipt']['sources'][0]['block_truncated'])
    def test_real_rank_no_row_mutation_or_omission(self):
        rows=[{'id':'b','titulo':'other','tipo':'pedra'},{'id':'geometry','titulo':'geometry','tipo':'entrega_doc'}]
        before=json.dumps(rows);out=rank.rank_nodes(rows,'geometry')
        self.assertEqual(out[0]['id'],'geometry');self.assertEqual(len(out),len(rows));self.assertEqual(json.dumps(rows),before)
    def projection(self,size):
        text='OBJECTIVE keep identity; pending P; decision D; '+'x'*size
        return {'text':text,'objective':'keep identity','receipt':{'projection_sha256':hashlib.sha256(text.encode()).hexdigest(),'context_id':'fixture','objective_sha256':'synthetic','state_sha256':'synthetic','revision':1},'included_record_ids':['P','D'],'omitted_record_ids':[]}
    def queue(self,size,cap=None,provider='mimo'):
        projection=self.projection(size)
        original=nos.canonical_memory.prepare
        def prepared(prompt,**kw):return original(prompt,self.canonical,**kw)
        c={'branch_id':'F9.9','mission_id':'SYNTHETIC','required_provider':provider,'max_projection_chars':cap}
        with patch.object(nos.canonical_memory,'prepare',side_effect=prepared):
            return nos.prepare_queue('keep identity',c,'SYSTEM',provider,operational_projection=projection),projection
    def test_joint_envelope_graph_state_and_identity(self):
        for provider,cap in [('mimo',909312),('deepseek',647168),('claude',39000)]:
            p,projection=self.queue(5000,provider=provider)
            self.assertEqual(p['prompt'].count(projection['objective']),1)
            self.assertIn(projection['text'],p['prompt']);self.assertIn('NOS VIVO',p['prompt'])
            self.assertIn(envelope.NEW.CORE,p['prompt']);op.verify_packet(p)
            self.assertLessEqual(len(('SYSTEM'+p['prompt']).encode()),cap)
            self.assertLessEqual(len(p['prompt']),24000)
            OBS.append({'provider':provider,'combined_chars':len(p['prompt']),'combined_bytes_with_system':len(('SYSTEM'+p['prompt']).encode()),'byte_cap':cap,'state_included_integrally':True})
    def test_joint_20911_over_12000_refuses(self):
        with self.assertRaises(ValueError):self.queue(20911,12000)
    def test_joint_generation_change_refuses(self):
        original=nos.build
        def changed(*a,**kw):
            result=original(*a,**kw);result['receipt']['canonical_memory']=dict(result['receipt']['canonical_memory'],generation='other');return result
        with patch.object(nos,'build',side_effect=changed):
            with self.assertRaisesRegex(ValueError,'generation changed'):self.queue(5000)
    def test_cli_real_retrieval_without_transport(self):
        cat={'required_ids':[],'coverage':'SYNTHETIC','entries':{}}
        for ident in ['geometry','small']:
            cat['entries'][ident]={'path':str(self.root/(ident+'.md')),'scope':'scientific','role':'optional','protected_ids':[],'annotation_coverage':'synthetic'}
        path=self.root/'catalog.json';path.write_text(json.dumps(cat),encoding='utf8')
        transport=types.ModuleType('iald_orchestrator.transport');transport.Transport=lambda:(_ for _ in ()).throw(AssertionError('TRANSPORT_CREATED'))
        package=types.ModuleType('iald_orchestrator');package.__path__=[]
        with patch.dict(sys.modules,{'iald_orchestrator':package,'iald_orchestrator.transport':transport,'iald_orchestrator.layered_retrieval':rank}),patch.object(rank,'DB',self.root/'nos_vivo.sqlite3'),patch.object(rank,'CATALOG',path),patch.object(rank,'CATALOG_SHA256',hashlib.sha256(path.read_bytes()).hexdigest()),patch.object(rank,'SCIENCE_ROOTS',(self.root,)):
            cli=mod('review_cli',ROOT/'transport_cli.py')
            with patch.object(sys,'stdin',io.StringIO(json.dumps({'operation':'retrieve_knowledge','query':'geometry','budget_bytes':4096}))),patch.object(sys,'stdout',io.StringIO()) as output:cli.main()
            raw=output.getvalue().encode();out=json.loads(raw);self.assertTrue(out['ok']);self.assertLessEqual(len(raw),4096)
            self.assertEqual(out['nodes'][0]['source']['status'],'VERIFIED_SHA256')
            self.assertFalse(out['coverage']['complete_protection_coverage'])

suite=unittest.defaultTestLoader.loadTestsFromTestCase(Combined)
# Ranking's one child CLI is the copied module, with a deliberately invalid request.
result=unittest.TextTestRunner(verbosity=1).run(suite)
out=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,failures=[(str(t),s) for t,s in result.failures+result.errors],joint=OBS,envelope_reproductions=envelope.OBS,provider_calls=0,network_calls=0,scope='Copied frozen code, synthetic DB/sources/state, real ranking/canonical/nos/operational attach; no installed module changed')
(ROOT/'REVIEW_TEST_RESULTS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'status':out['status'],'tests':out['tests'],'joint':OBS},ensure_ascii=False))
raise SystemExit(0 if result.wasSuccessful() else 1)
