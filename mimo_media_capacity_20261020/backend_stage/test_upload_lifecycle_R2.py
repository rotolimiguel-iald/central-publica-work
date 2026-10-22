"""Regression for independent review M1/M2; actual child-process interruption."""
from contextlib import closing
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import private_media_store as private
import iald_mimo_multimodal as media
from test_private_media import CountedCipher,small_wav

W=Path(__file__).resolve().parent

class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=W,prefix='test_lifecycle_');self.root=Path(self.temp.name)
        self.scope=private.Scope('owner','generation','c_first')
        self.store=private.PrivateMediaStore(self.root,authorize_scope=lambda _:True,validate_media=media.validate_upload,cipher=CountedCipher())
    def tearDown(self):self.temp.cleanup()
    def put(self,raw=None,scope=None):
        raw=small_wav() if raw is None else raw
        return self.store.put(io.BytesIO(raw),scope=scope or self.scope,mime='audio/wav',content_length=len(raw))
    def check_revoked(self):
        with closing(self.store._db()) as db:
            rows=db.execute('SELECT status FROM media').fetchall()
            reserved=db.execute("SELECT coalesce(sum(bytes),0) FROM media WHERE status IN ('active','uploading')").fetchone()[0]
        self.assertEqual(rows,[('revoked',)]);self.assertEqual(reserved,0)
        self.assertFalse(list(self.store.blobs.iterdir()))
    def test_conversation_delete_during_validation_no_orphan_no_success(self):
        original=self.store.validate_media
        def revoke(raw,mime):self.store.revoke_conversation(self.scope);return original(raw,mime)
        self.store.validate_media=revoke
        with self.assertRaises(private.MediaUnavailable):self.put()
        self.check_revoked()
    def test_account_delete_during_validation_no_resurrection(self):
        original=self.store.validate_media
        def revoke(raw,mime):self.store.revoke_account(self.scope,authorize_account_deletion=lambda *_:True);return original(raw,mime)
        self.store.validate_media=revoke
        with self.assertRaises(private.MediaUnavailable):self.put()
        self.check_revoked()
    def test_four_real_killed_uploads_dont_lock_other_owner(self):
        code='''import os,sys
from private_media_store import PrivateMediaStore,Scope
class Cipher:
 def seal(self,_):raise AssertionError('not reached')
 def open(self,_):raise AssertionError('not reached')
class Stream:
 def read(self,_):os._exit(21)
s=PrivateMediaStore(sys.argv[1],authorize_scope=lambda _:True,validate_media=lambda *_:None,cipher=Cipher())
s.put(Stream(),scope=Scope('interrupted','gen','c_same'),mime='audio/wav',content_length=100)
'''
        for i in range(4):
            result=subprocess.run([sys.executable,'-B','-c',code,str(self.root)],cwd=W,capture_output=True,timeout=15)
            self.assertEqual(result.returncode,21,result.stderr)
        fresh=private.PrivateMediaStore(self.root,authorize_scope=lambda _:True,validate_media=media.validate_upload,cipher=CountedCipher())
        raw=small_wav();part=fresh.put(io.BytesIO(raw),scope=private.Scope('other','gen','c_new'),mime='audio/wav',content_length=len(raw))
        self.assertEqual(part['kind'],'audio')
        with closing(fresh._db()) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM media WHERE status='uploading'").fetchone()[0],0)
            self.assertEqual(db.execute("SELECT count(*) FROM media WHERE status='abandoned'").fetchone()[0],4)
    def test_live_upload_reservation_not_reaped(self):
        raw=small_wav();source=io.BytesIO(raw);checked=[]
        class Stream:
            def read(inner,n):
                if not checked:
                    checked.append(self.store.reconcile_uploads());self.assertEqual(checked[0]['abandoned'],[])
                return source.read(n)
        self.store.put(Stream(),scope=self.scope,mime='audio/wav',content_length=len(raw))
    def test_technical_lease_expiry_no_publication(self):
        clock=[1000];self.store.clock=lambda:clock[0];original=self.store.validate_media
        def late(raw,mime):clock[0]+=private.UPLOAD_LEASE_SECONDS+1;return original(raw,mime)
        self.store.validate_media=late
        with self.assertRaises(private.MediaUnavailable):self.put()
        self.assertFalse(list(self.store.blobs.iterdir()))
    def test_abandoned_temporaries_cleaned_but_active_permanent_blob_preserved(self):
        active=self.put();ident='a'*32
        with closing(self.store._db()) as db:
            db.execute('INSERT INTO media VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(ident,'dead','g','c_dead','{}',10,None,'uploading',0,999999999,0,0))
        for suffix in ('.tmp','.bin'):(self.store.blobs/(ident+suffix)).write_bytes(b'orphan unpublished')
        result=self.store.reconcile_uploads();self.assertEqual(result['abandoned'],[ident])
        self.assertFalse((self.store.blobs/(ident+'.tmp')).exists());self.assertFalse((self.store.blobs/(ident+'.bin')).exists())
        self.assertTrue((self.store.blobs/(active['media_ref']+'.bin')).exists())

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(LifecycleTests))
    (W/'LIFECYCLE_R2_TEST_RESULTS.json').write_text(json.dumps({'passed':result.wasSuccessful(),'tests':result.testsRun,'errors':len(result.errors),'failures':len(result.failures),'actual_interrupted_child_processes':4,'provider_calls':0},indent=2),encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
