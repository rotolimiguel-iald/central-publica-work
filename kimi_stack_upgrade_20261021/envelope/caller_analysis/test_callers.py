"""Real caller composition with staged prepare + synthetic graph/projection only."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json,socket,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import test_envelope as corpus
cm=corpus.NEW
def load(name):
    spec=importlib.util.spec_from_file_location(cm.__package__+'.'+name,HERE/'sources'/(name+'.py'))
    m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
controls=load('request_controls');op=load('operational_memory');nos=load('nos_packet')
SYSTEM=json.loads((HERE/'SYSTEM_LITERAL.json').read_bytes())['system']
OBS=[]
def digest(raw):return hashlib.sha256(raw.encode() if isinstance(raw,str) else raw).hexdigest()
class Callers(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=HERE,prefix='synthetic_');self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.manifest=corpus.fixture(self.root,anchor_size=500)
        self.calls=[];self.build_calls=[]
        original=cm.prepare
        def prepare(prompt,**kw):
            result=original(prompt,directory=self.root,**kw);self.calls.append(dict(kwargs=copy.deepcopy(kw),packet=copy.deepcopy(result)));return result
        for obj,name,value in [(cm,'prepare',prepare),(nos,'board_unit',lambda uid:dict(id=uid) if uid=='F9.CALLER_TEST' else None),(nos,'build',self.graph),(op,'refuse_confidential',lambda text,*args: nos.safe_text(text))]:
            p=patch.object(obj,name,value);p.start();self.addCleanup(p.stop)
        p=patch.object(socket.socket,'connect',side_effect=AssertionError('NO_NETWORK'));p.start();self.addCleanup(p.stop)
    def graph(self,unit,maximum,**kw):
        self.build_calls.append(copy.deepcopy(kw));self.assertEqual(kw['canonical_reference']['prompt'],'')
        text='GRAPH_UNIQUE_PUBLIC_97\n'+'graph item\n'*25
        return dict(prompt=text,receipt=dict(schema=nos.SCHEMA,unit=unit,packet_sha256=digest(text),selection='SCIENTIFIC_ALLOWLIST_REREAD_NO_LEGAL_CONTENT',sources=[],no_permitted_source_hits=True,canonical_memory=kw['canonical_reference']['receipt']))
    def projection(self):
        objective='OBJECTIVE_PUBLIC_UNIQUE_73'
        text='SYNTHETIC_STATE\n'+json.dumps(dict(objective=objective,required='STATE_UNIQUE_91',phase='readonly_analysis'),ensure_ascii=False)
        receipt=dict(context_id='synthetic-context',objective_sha256=digest(objective),state_sha256='b'*64,revision=1,projection_sha256=digest(text))
        return dict(text=text,objective=objective,receipt=receipt,included_record_ids=['synthetic-required'],omitted_record_ids=[])
    def evaluate(self,name,graph,projection=True,max_chars=None):
        c=dict(branch_id='F9.CALLER_TEST' if graph else 'unbound',required_provider=name,max_projection_chars=max_chars,memory_generation=self.manifest['generation'])
        proj=self.projection() if projection else None;objective=proj['objective'] if proj else 'TASK_UNIQUE_71';prompt='Pedido: '+objective
        packet=nos.prepare_queue(prompt,c,SYSTEM,name,operational_projection=proj)
        self.assertEqual(len(self.calls),2 if graph else 1)
        chosen=self.calls[-1];canonical=chosen['packet']['prompt'];extra=op.SEPARATOR+proj['text'] if proj else '';graph_text=self.graph('F9.CALLER_TEST',5000,canonical_reference=dict(prompt='',receipt=chosen['packet']['receipt']))['prompt'] if graph else ''
        separator='\n\nNOS VIVO — CONSULTATIVE REUSE CONTEXT:\n' if graph else ''
        self.assertEqual(packet['prompt'],canonical+separator+graph_text+extra)
        self.assertEqual(packet['prompt'].count(cm.CORE),1);self.assertEqual(packet['prompt'].count(objective),1)
        self.assertEqual(packet['prompt'].count('STATE_UNIQUE_91'),1 if proj else 0);self.assertEqual(packet['prompt'].count('GRAPH_UNIQUE_PUBLIC_97'),1 if graph else 0)
        reserve_chars=len(separator+graph_text+extra);reserve_bytes=len((separator+graph_text+(SYSTEM if graph else '')+extra).encode())+(256 if graph else 0)
        self.assertEqual(chosen['kwargs']['reserved_context_chars'],reserve_chars);self.assertEqual(chosen['kwargs']['reserved_context_bytes'],reserve_bytes)
        rec=chosen['packet']['receipt'];self.assertEqual(rec['envelope_total_chars'],len(packet['prompt']));self.assertEqual(rec['envelope_total_bytes'],len(packet['prompt'].encode())+(len(SYSTEM.encode())+256 if graph else 0))
        self.assertEqual(packet['receipt']['context_bytes'],len(packet['prompt'].encode()));self.assertEqual(packet['receipt']['packet_sha256'],digest(packet['prompt']))
        self.assertEqual(packet['receipt']['generation'],self.manifest['generation']);controls.enforce_packet(packet,c,SYSTEM)
        before=len(self.calls);augmented=nos.augment(packet,c,name,SYSTEM);self.assertIs(augmented,packet);self.assertEqual(len(self.calls),before)
        OBS.append(dict(provider=name,graph=graph,operational=projection,prepare_calls=before,final_packet_bytes=len(packet['prompt'].encode()),reserved_bytes=reserve_bytes,reserved_chars=reserve_chars,canonical_occurrences=packet['prompt'].count(cm.CORE),objective_occurrences=packet['prompt'].count(objective),graph_occurrences=packet['prompt'].count('GRAPH_UNIQUE_PUBLIC_97'),state_occurrences=packet['prompt'].count('STATE_UNIQUE_91'),char_cap_pre_subtracts_system=(max_chars is not None),system_bytes_in_reservation=len(SYSTEM.encode()) if graph else 0,margin_bytes=256 if graph else 0,no_graph_system_wrapper_not_reserved_bytes=0 if graph else len((SYSTEM+'\n\nTAREFA:\n').encode())))
    def test_standard_no_graph_with_operational(self):self.evaluate('claude',False,max_chars=20000)
    def test_standard_graph_with_operational(self):self.evaluate('claude',True,max_chars=20000)
    def test_kimi_no_graph_with_operational(self):self.evaluate('kimi',False)
    def test_kimi_graph_with_operational(self):self.evaluate('kimi',True)
    def test_deepseek_graph_with_operational(self):self.evaluate('deepseek',True)
    def test_mimo_graph_with_operational(self):self.evaluate('mimo',True)
    def test_standard_no_graph_no_operational(self):self.evaluate('claude',False,projection=False,max_chars=20000)
    def test_kimi_graph_no_operational(self):self.evaluate('kimi',True,projection=False)
if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Callers))
    report=dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,observations=OBS,failures=[(str(t),s) for t,s in result.errors+result.failures],provider_calls=0,jobs_accessed=0,runtime_edits=0,scope='Copied real prepare_queue/_attach/augment/opmem.attach/request_controls, staged canonical prepare on synthetic sealed13-file corpus. Graph lookup and operational projection injected; no coordinator/runtime DB, graph CLI or provider executed.')
    (HERE/'TEST_RESULTS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');raise SystemExit(0 if result.wasSuccessful() else 1)
