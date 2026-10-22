"""Offline reviewer tests against a frozen copy; never import a live store."""
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'snapshot_R1'))
import private_media_store as media
import private_media_routes as routes


def network_guard(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo'):
        raise AssertionError('No network permitted in reviewer tests')


sys.addaudithook(network_guard)


class SyntheticCipher:
    """Only lifecycle logic here; builder replay separately tests real DPAPI."""
    def __init__(self): self.opens = 0
    def seal(self, raw): return raw
    def open(self, raw):
        self.opens += 1
        return raw


def facts(raw, mime):
    return dict(kind='audio', duration_seconds=1, has_audio=True)


def store_at(root):
    return media.PrivateMediaStore(root, authorize_scope=lambda s: True,
                                  validate_media=facts, cipher=SyntheticCipher())


SCOPE = media.Scope('synthetic-a', 'generation-1', 'draft_before_job')


if len(sys.argv) > 1 and sys.argv[1] == 'crash':
    child_store = store_at(Path(sys.argv[2]))
    class InterruptedStream:
        def read(self, length): os._exit(21)
    child_store.put(InterruptedStream(), scope=SCOPE, mime='audio/wav', content_length=8)
    raise AssertionError('Crash fixture did not exit')


class Independent(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT, prefix='r1_')
        self.store = store_at(Path(self.tmp.name) / 'private')
        self.runtime = media.PrivateMediaRuntime(self.store, SCOPE, authorize_dispatch=lambda: True)
    def tearDown(self): self.tmp.cleanup()
    def put(self):
        return self.store.put(io.BytesIO(b'fixture!'), scope=SCOPE, mime='audio/wav', content_length=8)
    def test_roundtrip_and_metadata_only(self):
        part = self.put()
        view = media.resolve_media_metadata([{'role':'user','content':[part]}],store=self.store,scope=SCOPE)
        self.assertEqual(self.store.cipher.opens, 0)
        self.assertEqual(view[0]['sha256'], part['sha256'])
        self.assertEqual(self.store.read(part['media_ref'], SCOPE, part['sha256'])[0], b'fixture!')
    def test_scope_partition_and_pins_before_blob_io(self):
        part = self.put()
        others = [media.Scope('synthetic-b', SCOPE.generation, SCOPE.conversation),
                  media.Scope(SCOPE.owner, 'generation-2', SCOPE.conversation),
                  media.Scope(SCOPE.owner, SCOPE.generation, 'other')]
        with patch.object(Path, 'read_bytes', side_effect=AssertionError('No blob reads')):
            for scope in others:
                with self.assertRaises(media.MediaUnavailable):
                    self.store.read(part['media_ref'], scope, part['sha256'])
            with self.assertRaises(media.MediaUnavailable):
                self.store.read(part['media_ref'], SCOPE, '0'*64)
    def test_deleted_ref_cannot_expand(self):
        part = self.put();self.store.revoke_conversation(SCOPE)
        with self.assertRaises(media.MediaUnavailable):
            self.runtime.expand({'messages':[{'role':'user','content':[part]}]}, provider='mimo')
        self.assertEqual(self.store.cipher.opens, 0)
    def test_upload_delete_interleaving_reproduces_orphan(self):
        def delete_during_probe(raw, mime):
            receipt = self.store.revoke_conversation(SCOPE)
            self.assertEqual(receipt['blobs_removed'], 0)
            return facts(raw, mime)
        self.store.validate_media = delete_during_probe
        part = self.put()
        with closing(self.store._db()) as db:
            status = db.execute('SELECT status FROM media WHERE id=?',(part['media_ref'],)).fetchone()[0]
            accounted = db.execute("SELECT coalesce(sum(bytes),0) FROM media WHERE status IN ('active','uploading')").fetchone()[0]
        proof = dict(returned_success=True, row_status=status, active_quota_bytes=accounted,
                     blob_exists=(self.store.blobs/(part['media_ref']+'.bin')).exists())
        RESULTS['upload_delete_race'] = proof
        self.assertEqual(proof,dict(returned_success=True,row_status='revoked',active_quota_bytes=0,blob_exists=True))
    def test_process_crash_reservations_exhaust_global_slots(self):
        for _ in range(self.store.max_active_uploads):
            result = subprocess.run([sys.executable,'-B',str(Path(__file__)), 'crash', str(self.store.root)],capture_output=True)
            self.assertEqual(result.returncode, 21, result.stderr.decode(errors='replace'))
        fresh = store_at(self.store.root)
        with closing(fresh._db()) as db:
            count = db.execute("SELECT count(*) FROM media WHERE status='uploading'").fetchone()[0]
        with self.assertRaisesRegex(media.MediaError, 'concurrency'):
            fresh.put(io.BytesIO(b'fixture!'),scope=media.Scope('other-user','g','new'),mime='audio/wav',content_length=8)
        RESULTS['crash_recovery'] = dict(real_child_crashes=4, stale_uploading_rows=count,
                                        fresh_store_other_user_refused=True)
    def flask_client(self):
        from flask import Flask, Request, request
        app=Flask(__name__)
        class BoundedRequest(Request):
            @property
            def max_content_length(self):
                return media.MAX_RAW_BYTES if self.path=='/api/private-media' else super().max_content_length
        app.request_class=BoundedRequest
        def auth(): return request.headers.get('X-Test-Session')=='valid'
        def host_scope(cid):
            if cid!='draft_before_job': raise media.MediaUnavailable('Denied namespace')
            return SCOPE
        routes.register_private_media(app,self.store,host_scope=host_scope,authenticate_csrf=auth,upload_eligible=lambda s:True)
        return app.test_client()
    def test_endpoint_positive_host_bound_draft_before_first_job(self):
        c=self.flask_client()
        response=c.post('/api/private-media?conversation_id=draft_before_job',data=b'fixture!',content_type='audio/wav',headers={'X-Test-Session':'valid'})
        self.assertEqual(response.status_code,201)
        part=response.get_json()
        self.assertEqual(c.get('/api/private-media/'+part['media_ref']+'?conversation_id=draft_before_job',headers={'X-Test-Session':'valid'}).status_code,200)
    def test_endpoint_auth_and_namespace_negatives(self):
        c=self.flask_client()
        self.assertEqual(c.post('/api/private-media?conversation_id=draft_before_job',data=b'fixture!',content_type='audio/wav').status_code,403)
        self.assertEqual(c.post('/api/private-media?conversation_id=forged',data=b'fixture!',content_type='audio/wav',headers={'X-Test-Session':'valid'}).status_code,404)
        self.assertEqual(list(self.store.blobs.iterdir()),[])
    def test_endpoint_no_raw_download(self):
        c=self.flask_client();part=self.put()
        response=c.get('/api/private-media/'+part['media_ref']+'?conversation_id=draft_before_job',headers={'X-Test-Session':'valid'})
        self.assertNotIn(b'fixture!',response.data)
        self.assertEqual(c.get('/api/private-media/'+part['media_ref']+'/raw',headers={'X-Test-Session':'valid'}).status_code,404)


if __name__ == '__main__':
    RESULTS={}
    output=io.StringIO()
    result=unittest.TextTestRunner(stream=output,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Independent))
    RESULTS.update(tests=result.testsRun,passed=result.wasSuccessful(),failures=len(result.failures),errors=len(result.errors),
                   detail=output.getvalue(),provider_calls=0,production_changes=False,
                   host_bindings='synthetic callback contract tested; actual server integration not yet delivered')
    target=ROOT/'INDEPENDENT_TESTS_R1.json';raw=json.dumps(RESULTS,indent=2).encode()
    temp=target.with_suffix('.tmp');temp.write_bytes(raw);assert temp.read_bytes()==raw;temp.replace(target)
    print(json.dumps(RESULTS,ensure_ascii=False))
