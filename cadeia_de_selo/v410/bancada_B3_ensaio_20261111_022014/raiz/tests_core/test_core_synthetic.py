"""Canonical/HTTP/GW tests: synthetic fixtures only, no Motor or network listener."""
import sys, unittest, tempfile, hashlib, json, io, types, threading, importlib, importlib.util, math
from pathlib import Path
from unittest.mock import patch, Mock
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'candidate'))
from bancada import canonical
spec=importlib.util.spec_from_file_location('synthetic_server_under_test',ROOT/'candidate'/'um_bancada.py')
server=importlib.util.module_from_spec(spec);spec.loader.exec_module(server)
ENGINE_AFTER_IMPORT=server.B
with patch.object(canonical,'read_alpha',return_value=(.007,{'scope':'SYNTHETIC'})):
    gw=importlib.import_module('bancada.gw')
REQUIRED=('um_bancada.py','mcp_um.py','bancada/canonical.py','bancada/motor.py','bancada/evidencia.py')

class Fixture:
    def __init__(self,root):
        self.root=Path(root); self.raw={}
        def pin(name,data):
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);self.raw[name]=data
            return {'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
        self.pin=pin
        self.script=pin('source_um.py',b"UM_VERSION = 'synthetic-v1'\nALPHA_FINE_CODATA_2018 = 0.007\n")
        self.seal=pin('source_seal.json',json.dumps({'um_version':'synthetic-v1','sha256':{'um.py':self.script['sha256']}}).encode())
        self.code=[pin(n,('SYNTHETIC '+n+'\n').encode()) for n in REQUIRED]
        self.source=pin('inputs/source.txt',b'SYNTHETIC_SOURCE')
        self.man={'schema':1,'deployment_id':'synthetic','canonical':{'version':'synthetic-v1','script':self.script,'seal':self.seal},'code':self.code,'sources':[self.source]}
        self.path=self.root/'canonical_contracts.json';self.save()
    def save(self):self.path.write_text(json.dumps(self.man),encoding='utf-8')

class CanonicalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=ROOT/'tests_core');self.addCleanup(self.tmp.cleanup);self.f=Fixture(self.tmp.name)
    def test_valid_and_alpha(self):
        reg=canonical.CanonicalRegistry(self.f.root);r=reg.check('synthetic')
        self.assertTrue(r['ok']);self.assertEqual(r['canonical_version'],'synthetic-v1');self.assertAlmostEqual(r['beta_tgl'],.007*math.sqrt(math.e))
    def test_each_mutation_refused(self):
        reg=canonical.CanonicalRegistry(self.f.root)
        for name in ('source_um.py','source_seal.json',*REQUIRED,'inputs/source.txt'):
            with self.subTest(name=name):
                p=self.f.root/name;raw=p.read_bytes();p.write_bytes(bytes([raw[0]^1])+raw[1:])
                with self.assertRaises(canonical.CanonicalError):reg.check('mutation')
                p.write_bytes(raw);self.assertTrue(reg.check('restored')['ok'])
    def test_manifest_mutation_and_source_bytes_refused(self):
        reg=canonical.CanonicalRegistry(self.f.root);self.f.man['deployment_id']='changed';self.f.save()
        with self.assertRaises(canonical.CanonicalError):reg.check('mutation')
        with self.assertRaises(canonical.CanonicalError):reg.source_bytes(self.f.root/'inputs/source.txt',b'SYNTHETIC_SOURCE')
    def test_source_unknown_and_mutated_bytes(self):
        reg=canonical.CanonicalRegistry(self.f.root)
        with self.assertRaises(canonical.CanonicalError):reg.source_bytes(self.f.root/'unknown',b'a')
        with self.assertRaises(canonical.CanonicalError):reg.source_bytes(self.f.root/'inputs/source.txt',b'SYNTHETIC_SOURCF')
        self.assertEqual(reg.source_bytes(self.f.root/'inputs/source.txt',b'SYNTHETIC_SOURCE')['sha256'],self.f.source['sha256'])
    def test_required_pins(self):
        for n in REQUIRED:
            with self.subTest(missing=n):
                self.f.man['code']=[p for p in self.f.code if p['path']!=n];self.f.save()
                with self.assertRaises(canonical.CanonicalError):canonical.CanonicalRegistry(self.f.root)
        self.f.man['code']=[];self.f.save()
        with self.assertRaises(canonical.CanonicalError):canonical.CanonicalRegistry(self.f.root)
    def test_duplicate_source_refused(self):
        self.f.man['sources']*=2;self.f.save()
        with self.assertRaises(canonical.CanonicalError):canonical.CanonicalRegistry(self.f.root)
    def test_version_seal_mismatch_even_when_pinned(self):
        seal=self.f.pin('source_seal.json',json.dumps({'um_version':'other','sha256':{'um.py':self.f.script['sha256']}}).encode())
        self.f.man['canonical']['seal']=seal;self.f.save()
        with self.assertRaises(canonical.CanonicalError):canonical.CanonicalRegistry(self.f.root)
    def test_numeric_attacks(self):
        for v in (True,False,float('nan'),float('inf'),-float('inf'),'0.007',None):
            with self.subTest(v=repr(v)),self.assertRaises(canonical.CanonicalError):canonical.finite_number(v,'test')
        for v in (0,-.1):
            with self.assertRaises(canonical.CanonicalError):canonical.finite_number(v,'test',positive=True)
    def test_alpha_nonfinite_in_pinned_script(self):
        script=self.f.pin('source_um.py',b"UM_VERSION='synthetic-v1'\nALPHA_FINE_CODATA_2018=1e999\n")
        seal=self.f.pin('source_seal.json',json.dumps({'um_version':'synthetic-v1','sha256':{'um.py':script['sha256']}}).encode())
        self.f.man['canonical'].update(script=script,seal=seal);self.f.save()
        with self.assertRaises(canonical.CanonicalError):canonical.CanonicalRegistry(self.f.root)
    def test_default_root_is_bench(self):
        with patch.object(canonical,'__file__',str(self.f.root/'bancada'/'canonical.py')),patch.dict(canonical._registries,{},clear=True):
            reg=canonical.get_registry();self.assertEqual(reg.root,self.f.root.resolve());self.assertTrue(canonical.require_current('fixture')['ok'])
    def test_state_is_fail_closed(self):
        with patch.dict(canonical._registries,{},clear=True):
            self.assertTrue(canonical.canonical_state(self.f.root)['ok'])
            self.f.path.write_bytes(b'{}')
            self.assertFalse(canonical.canonical_state(self.f.root)['ok'])


def receipt(op,root=None):return dict(ok=True,canonical_manifest_sha256='synthetic',um_py_sha256='synthetic-script',seal_sha256='synthetic-seal')
def bench():
    b=object.__new__(server.Bancada);b.activity_lock=threading.RLock();b.active_requests=0;b.quiescing=False;b.pronta=True;b.erro=None
    b.ev=Mock();b.ev.tarefas={};b.ev.avaliar.return_value={'synthetic':True}
    b.gw=Mock();b.gw.tarefas={};b.gw.estado={'estado':'pronto'}
    b.lago_res=types.SimpleNamespace(estado={'estado':'pronto'})
    return b

def handler(body=b'{}',path='/api/avaliar'):
    h=object.__new__(server.H);h.path=path;h.headers={'Host':'127.0.0.1:18777','Content-Length':str(len(body))}
    h.connection=Mock();h.rfile=io.BytesIO(body);h.wfile=io.BytesIO();h.send_response=Mock();h.send_header=Mock();h.end_headers=Mock();h._request_receipt=None
    return h
class HTTPTests(unittest.TestCase):
    def setUp(self):
        self.b=bench();self.pb=patch.object(server,'B',self.b);self.pb.start();self.addCleanup(self.pb.stop)
        self.pg=patch.object(server,'require_current',side_effect=receipt);self.pg.start();self.addCleanup(self.pg.stop)
    def post(self,obj,path='/api/avaliar'):
        h=handler(json.dumps(obj).encode(),path);h.do_POST();return h
    def test_import_does_not_start_motor(self):
        self.assertIsNone(ENGINE_AFTER_IMPORT)
        self.assertNotIn('bancada.motor',sys.modules)
    def test_invalid_flags_and_options(self):
        for k in ('curvas','c_livre','controle','series','log'):
            for v in ('false',0,1,None):
                h=self.post({k:v});self.assertEqual(h.send_response.call_args.args[0],422)
        for v in (False,[],0,'tgl',None):
            h=self.post({'opcoes':v});self.assertEqual(h.send_response.call_args.args[0],422)
        self.b.ev.avaliar.assert_not_called()
    def test_valid_request_keeps_types(self):
        h=self.post({'curvas':False,'opcoes':{'modo':'tgl'}})
        self.assertEqual(h.send_response.call_args.args[0],200)
        args=self.b.ev.avaliar.call_args.args;self.assertIs(args[2],False);self.assertEqual(args[3],{'modo':'tgl'})
        self.assertEqual(self.b.active_requests,0)
    def test_bad_length_is_json_400(self):
        h=handler();h.headers['Content-Length']='bad';h.do_POST()
        self.assertEqual(h.send_response.call_args.args[0],400);self.assertIn('erro',json.loads(h.wfile.getvalue()))
    def test_short_body_refused(self):
        h=handler(b'{}');h.headers['Content-Length']='9';h.do_POST()
        self.assertEqual(h.send_response.call_args.args[0],400);self.b.ev.avaliar.assert_not_called()
    def test_read_timeout_refused(self):
        h=handler();h.rfile=Mock();h.rfile.read.side_effect=TimeoutError("synthetic timeout");h.do_POST()
        self.assertEqual(h.send_response.call_args.args[0],400);self.assertEqual(self.b.active_requests,0)
        h.connection.settimeout.assert_called()
    def test_nonfinite_json_refused(self):
        for token in ('NaN','Infinity','-Infinity'):
            h=handler(('{"theta":{"H0":'+token+'}}').encode());h.do_POST();self.assertEqual(h.send_response.call_args.args[0],400)
    def test_activity_counts_loads(self):
        self.b.pronta=False;self.b.gw.estado['estado']='carregando';self.b.lago_res.estado['estado']='carregando'
        r=self.b.atividades();self.assertFalse(r['idle']);self.assertEqual({x['kind'] for x in r['active']},{'engine','gw','lago_res'})
    def test_activity_terminal_states_and_running(self):
        self.b.ev.tarefas={k:{'estado':k} for k in ('pronta','falhou','concluida','cancelada')};self.assertTrue(self.b.atividades()['idle'])
        self.b.ev.tarefas['r']={'estado':'rodando'};self.assertFalse(self.b.atividades()['idle'])
    def test_sync_counter_and_exception_cleanup(self):
        h=handler()
        def work():
            self.assertEqual(self.b.active_requests,1);self.assertFalse(self.b.atividades()['idle']);raise RuntimeError('synthetic')
        with self.assertRaises(RuntimeError):h._dispatch(work)
        self.assertEqual(self.b.active_requests,0);self.assertTrue(self.b.atividades()['idle'])
    def test_quiesce_blocks_science(self):
        h=self.post({},'/api/maintenance/quiesce');self.assertTrue(self.b.quiescing)
        h=self.post({});self.assertEqual(h.send_response.call_args.args[0],503);self.b.ev.avaliar.assert_not_called()
    def test_response_rechecks_identity(self):
        self.pg.stop();self.pg=patch.object(server,'require_current',side_effect=[receipt('before'),canonical.CanonicalError('changed')]);self.pg.start()
        h=self.post({});self.assertEqual(h.send_response.call_args.args[0],409)
    def test_gw_execution_blocked(self):
        h=self.post({},'/api/gw/rodar');self.assertEqual(h.send_response.call_args.args[0],409);self.b.gw.rodar.assert_not_called()
    def test_ui_escape_refused(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'tests_core') as td:
            p=Path(td);ui=p/'ui';ui.mkdir();neighbor=p/'ui_neighbor';neighbor.mkdir();(neighbor/'probe.txt').write_text('SYNTHETIC')
            h=handler()
            with patch.object(server,'UI',str(ui)):h._arquivo('../ui_neighbor/probe.txt')
            self.assertEqual(h.send_response.call_args.args[0],404);self.assertNotIn(b'SYNTHETIC',h.wfile.getvalue())

class GWTests(unittest.TestCase):
    def setUp(self):self.t=1e9+np.arange(131072,dtype=float)/4096.;self.x=np.sin(np.arange(131072)/100.)*1e-22
    def packet(self,t=None,x=None,fs=4096.):
        buf=io.BytesIO();np.savez(buf,t=self.t if t is None else t,strain=self.x if x is None else x,fs=fs);return buf.getvalue()
    def test_valid_hashed_bytes(self):
        t,x,fs=gw.read_strain_bytes(self.packet());np.testing.assert_array_equal(t,self.t);np.testing.assert_array_equal(x,self.x);self.assertEqual(fs,4096.)
    def test_fs_type_shape_value(self):
        for fs in (True,'4096',np.array([4096.]),np.nan,np.inf,2048.):
            with self.subTest(fs=repr(fs)),self.assertRaises(ValueError):gw.read_strain_bytes(self.packet(fs=fs))
    def test_shape_dtype(self):
        for t,x in ((self.t[:-1],self.x),(self.t,self.x[:-1]),(self.t.reshape(-1,1),self.x),(self.t,self.x.astype(complex)),(self.t.astype(bool),self.x)):
            with self.assertRaises(ValueError):gw.read_strain_bytes(self.packet(t=t,x=x))
    def test_nonfinite_series(self):
        for v in (np.nan,np.inf,-np.inf):
            for field in ('t','x'):
                t=self.t.copy();x=self.x.copy();(t if field=='t' else x)[42]=v
                with self.subTest(v=v,field=field),self.assertRaises(ValueError):gw.read_strain_bytes(self.packet(t=t,x=x))
    def test_nonuniform_time(self):
        t=self.t.copy();t[200]+=1e-4
        with self.assertRaises(ValueError):gw.read_strain_bytes(self.packet(t=t))
    def test_accumulated_time_drift_refused(self):
        t=1e9+np.arange(131072)*(1./4096+4e-7)
        with self.assertRaises(ValueError):gw.read_strain_bytes(self.packet(t=t))

if __name__=='__main__':
    runner=unittest.TextTestRunner(verbosity=2)
    result=runner.run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    sys.exit(not result.wasSuccessful())
