"""ORDEM 019 regression tests: local fixtures only, never invoke providers."""
import hashlib
import json
from pathlib import Path
import tempfile
import threading
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from iald_orchestrator import canonical_memory as m, providers as p, program_controls as board
from iald_orchestrator.request_controls import normalize, enforce_packet
from iald_orchestrator.runtime import Runtime, now
from iald_orchestrator.policy import route


class VersionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.releases = self.root/'releases'
        self.releases.mkdir()
        self.active = self.root/'ACTIVE.json'
        self.a = self.release('v901', 'Cartan fixture A')
        self.b = self.release('v902', 'Cartan fixture B')
        self.patches = [patch.object(m,'ACTIVE',self.active), patch.object(m,'RELEASES',self.releases)]
        for x in self.patches: x.start()
        self.activate(self.a)

    def tearDown(self):
        for x in reversed(self.patches): x.stop()
        self.tmp.cleanup()

    def release(self, version, text):
        bodies = {name:(text+'\n').encode() for name in sorted(m.SNAPSHOT_NAMES)}
        bodies['tgl_kernel_proof_manifest.json'] = json.dumps({'formal_source_hash':'fixture'}).encode()
        seal = {'um_version':version, 'formal_source_hash':'fixture',
            'fail_closed_selftest':'FAIL_CLOSED_SELFTEST_PASSED',
            'sha256':{n:m.digest(bodies[n]) for n in ('um.py','um_absoluto.json','tgl_kernel_proof_manifest.json')}}
        bodies['um_absoluto_selo.json'] = json.dumps(seal).encode()
        gen = m.digest(json.dumps([(n,m.digest(b)) for n,b in bodies.items()],ensure_ascii=False).encode())
        directory = self.releases/(version+'_'+gen[:16])
        snap = directory/'snapshots'/directory.name
        snap.mkdir(parents=True)
        files=[]
        for name,body in bodies.items():
            path=snap/name;path.write_bytes(body)
            files.append({'source':str(path),'sha256':m.digest(body)})
        catalog=self.root/(version+'.json')
        catalog.write_bytes(json.dumps({'files':files}).encode())
        manifest=m.build(directory,catalog)
        self.assertEqual(manifest['generation'],gen)
        binding={'schema':1,'source_mode':m.SNAPSHOT_MODE,'release':version,
            'generation':gen,'index_sha256':manifest['index_sha256'],
            'documents':[{k:d[k] for k in ('name','sha256','bytes')} for d in manifest['documents']],
            'formal_source_hash':'fixture'}
        desc=snap/'SEALED_SNAPSHOT.json';desc.write_bytes(json.dumps(binding).encode())
        manifest.update(source_mode=m.SNAPSHOT_MODE,snapshot_root=str(snap),
            snapshot_manifest_sha256=m.digest(desc.read_bytes()))
        (directory/'manifest.json').write_bytes(json.dumps(manifest).encode())
        return directory

    def activate(self, directory):
        manifest=json.loads((directory/'manifest.json').read_bytes())
        self.active.write_bytes(json.dumps({'schema':1,'release':directory.name.split('_')[0],
            'epoch':directory.name,'generation':manifest['generation'],
            'manifest_sha256':m.digest((directory/'manifest.json').read_bytes())}).encode())

    def test_long_lived_process_follows_new_epoch_and_keeps_old_pin(self):
        first=m.prepare('Cartan')
        self.activate(self.b)
        second=m.prepare('Cartan')
        self.assertNotEqual(first['receipt']['generation'],second['receipt']['generation'])
        self.assertEqual(m.status()['epoch'],self.b.name)
        c=normalize({'mission_id':'TGL_BANCADA_OFICIAL','branch_id':'F1.3','lemma_id':'fixture',
                     'role':'draft','required_provider':'kimi','max_calls':1,
                     'memory_generation':first['receipt']['generation']})
        with self.assertRaisesRegex(ValueError,'Geração'):
            enforce_packet(second,c,'')
        self.assertEqual(m.prepare('Cartan',self.a)['receipt']['generation'],first['receipt']['generation'])

    def test_switch_during_prepare_cannot_mix_index_and_manifest(self):
        original=m.load
        def switch(directory, **kwargs):
            self.activate(self.b)
            return original(directory,**kwargs)
        with patch.object(m,'load',side_effect=switch):
            packet=m.prepare('Cartan')
        self.assertIn('fixture A',packet['prompt'])
        self.assertNotIn('fixture B',packet['prompt'])

    def test_missing_pointer_fails_closed(self):
        self.active.unlink()
        self.assertEqual(m.status()['status'],'unavailable')
        with self.assertRaises(ValueError): m.prepare('Cartan')

    def test_invalid_pointer_path_and_manifest_pin_rejected(self):
        value=json.loads(self.active.read_bytes())
        value['epoch']='../elsewhere'
        self.active.write_bytes(json.dumps(value).encode())
        with self.assertRaises(ValueError): m.resolve_directory()
        self.activate(self.a)
        value=json.loads(self.active.read_bytes());value['manifest_sha256']='0'*64
        self.active.write_bytes(json.dumps(value).encode())
        with self.assertRaises(ValueError): m.resolve_directory()

    def test_source_and_index_tampering_refused_and_no_rebuild(self):
        with self.assertRaises(ValueError): m.build(self.a)
        manifest=json.loads((self.a/'manifest.json').read_bytes())
        source=Path(manifest['documents'][0]['path'])
        source.write_bytes(b'tampered')
        with self.assertRaises(ValueError): m.load(self.a)
        (self.b/'index.sqlite3').write_bytes(b'tampered')
        with self.assertRaises(ValueError): m.load(self.b)

    def test_duplicate_fields_rejected(self):
        self.active.write_bytes(b'{"schema":1,"schema":1}')
        with self.assertRaises(ValueError): m.resolve_directory()


class ClaimTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.unit={'id':'F9.2','status':'EM_CURSO','gate':None,
            'reivindicacao':{'quem':'codex-coordenadora',
                'vence_em':(datetime.now().astimezone()+timedelta(hours=1)).isoformat()}}
        self.write()
    def tearDown(self):self.tmp.cleanup()
    def write(self, extra=()):
        (self.root/'PROGRAMA.json').write_bytes(json.dumps({'unidades':[self.unit,*extra]}).encode())
    def test_missing_wrong_expired_and_operator_gate_claim_refused(self):
        for change in ({'reivindicacao':None},{'status':'AGUARDA_OPERADOR'},
                       {'gate':'OPERADOR: autorização específica'}):
            old=self.unit.copy();self.unit.update(change);self.write()
            with self.assertRaises(ValueError):board.require_claim('F9.2','codex-coordenadora',self.root)
            self.unit=old
        self.unit['reivindicacao']['vence_em']='2000-01-01T00:00:00+00:00';self.write()
        with self.assertRaises(ValueError):board.require_claim('F9.2','codex-coordenadora',self.root)
    def test_new_approval_is_pending_and_written_through_official_cli(self):
        question={'id':'F9.2.A1','title':'Fixture approval','question':'Autorizar escopo?',
                  'scope':'Fixture local','source':'fixture'}
        with patch.object(board,'_run',return_value='ok') as call:
            result=board.register_approval(question,unit='F9.2',member='codex-coordenadora',root=self.root)
        self.assertEqual(result['status'],'AGUARDA_OPERADOR')
        self.assertEqual(call.call_args_list[0].args[2],'nova')
        self.assertEqual(call.call_args_list[1].args[2],'quadro')
    def test_approval_dedup_and_no_scope_overwrite(self):
        question={'id':'F9.2.A1','title':'Fixture approval','question':'Autorizar escopo?',
                  'scope':'Fixture local','source':'fixture'}
        self.write([{'id':question['id'],'status':'AGUARDA_OPERADOR','approval_request':question}])
        with patch.object(board,'_run') as call:
            result=board.register_approval(question,unit='F9.2',member='codex-coordenadora',root=self.root)
            self.assertFalse(result['created']);call.assert_not_called()
            with self.assertRaises(ValueError):
                board.register_approval(dict(question,scope='changed'),unit='F9.2',member='codex-coordenadora',root=self.root)
    def test_local_map_requires_claim_and_uses_only_map_cli(self):
        with patch.object(board,'_run',return_value='ok') as call:
            board.record_route(self.root/'fixture.json',unit='F9.2',member='codex-coordenadora',root=self.root)
            self.assertEqual(call.call_args.args[0],board.MAP)
            self.assertEqual(call.call_args.args[1],Path('rotas.py'))
            with self.assertRaises(ValueError):
                board.record_route(self.root/'fixture.json',unit='F9.2',member='other',root=self.root)
            self.assertEqual(call.call_count,1)


class RiteTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.runtime=Runtime(self.root/'state',recover=False)
    def tearDown(self):self.tmp.cleanup()
    def add(self):
        c={'mission_id':'TGL_BANCADA_OFICIAL','branch_id':'F9.2','lemma_id':'fixture',
           'role':'draft','required_provider':'local','max_calls':1}
        with self.runtime.db() as db:
            db.execute('INSERT INTO tasks(id,request_id,prompt,created_at,updated_at,status,execution_constraints) VALUES(?,?,?,?,?,?,?)',
                ('00000000-0000-4000-8000-000000000019','00000000-0000-4000-8000-000000000019','fixture',now(),now(),'queued',json.dumps(c)))
        return c
    def test_marker_discovery_and_no_http_dispatch(self):
        work=self.root/'work';marker=work/'v999_pacote'/'.servidor_parado_pelo_rito'
        marker.parent.mkdir(parents=True);marker.write_bytes(b'fixture')
        with patch.object(p,'RITE_ROOTS',(work,)), patch.object(p.urllib.request,'urlopen') as net:
            self.assertEqual(p.rite_markers(),[str(marker)])
            with self.assertRaises(p.ProviderPausedByRite):
                p.execute('local','fixture',self.root)
            net.assert_not_called()
            marker.unlink()
            self.assertEqual(p.rite_markers(),[])
    def test_status_excludes_qwen_without_health_probe(self):
        # Stub non-local discovery paths to avoid any provider subprocess or network.
        with patch.object(p,'rite_markers',return_value=['fixture']), \
             patch.object(p,'client_command',return_value=None), \
             patch('iald_orchestrator.deepseek.connection_status',return_value='unavailable'), \
             patch('iald_orchestrator.deepseek.authorization',return_value={}), \
             patch('iald_orchestrator.deepseek_secret_store.key_metadata',return_value={}), \
             patch('iald_orchestrator.mimo.connection_status',return_value='unavailable'), \
             patch('iald_orchestrator.mimo.authorization',return_value={}), \
             patch('iald_orchestrator.secret_store.key_metadata',return_value={}), \
             patch.object(p.urllib.request,'urlopen') as net:
            rows=p.discover()
            self.assertEqual(rows[0]['status'],'paused_by_rite')
            self.assertIsNone(route('fixture',rows,{})['selected'])
            net.assert_not_called()
    def test_queue_paused_without_attempt_and_resumes_only_when_marker_gone(self):
        self.add()
        with patch.object(p,'rite_markers',return_value=['fixture']), patch.object(self.runtime,'_perform') as execute:
            self.runtime._drain()
            execute.assert_not_called()
        self.assertEqual(self.runtime.task('00000000-0000-4000-8000-000000000019')['status'],'queued')
        with self.runtime.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM attempts').fetchone()[0],0)
        def finish(*args):self.runtime._update('00000000-0000-4000-8000-000000000019',status='result_ready')
        with patch.object(p,'rite_markers',return_value=[]), patch.object(self.runtime,'_perform',side_effect=finish) as execute:
            self.runtime._drain()
            self.assertEqual(execute.call_count,1)
    def test_pause_race_before_attempt_is_not_failed(self):
        self.add()
        self.runtime._update('00000000-0000-4000-8000-000000000019',status='running')
        with patch.object(self.runtime,'source_status',return_value={'ok':True}), \
             patch.object(p,'rite_markers',return_value=['fixture']):
            self.runtime._perform('00000000-0000-4000-8000-000000000019','fixture')
        self.assertEqual(self.runtime.task('00000000-0000-4000-8000-000000000019')['status'],'queued')
        self.assertIn('paused_by_rite',self.runtime.task('00000000-0000-4000-8000-000000000019')['error'])
        with self.runtime.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM attempts').fetchone()[0],0)


if __name__=='__main__':unittest.main(verbosity=2)

