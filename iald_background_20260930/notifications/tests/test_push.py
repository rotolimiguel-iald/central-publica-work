import importlib.util
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import unittest
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from iald_chat_push import PushStore, PushError, WindowsCipher, APNs, FCM


class FakeCipher:
    # Reversible fake for store contract tests only; never used by the default constructor.
    def seal(self,raw): return bytes(v ^ 0xA5 for v in raw)
    def open(self,raw): return bytes(v ^ 0xA5 for v in raw)


class FakeAPNs:
    def bearer(self): return 'fake-test-bearer'


class FakeTransport:
    def __init__(self): self.calls=[]; self.code=200; self.body=b''; self.error=False; self.before=None
    def prepare(self): pass
    def send(self,**request):
        self.calls.append(request)
        if self.before: self.before()
        if self.error: raise RuntimeError('SECRET_PROVIDER_TOKEN_DO_NOT_EXPOSE')
        return self.code,self.body


class PushTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=ROOT)
        self.transport=FakeTransport()
        self.store=PushStore(self.tmp.name,cipher=FakeCipher(),apns=FakeAPNs(),
                            fcm=FCM('example-project',lambda:'fake-bearer-for-tests'),transport=self.transport)
        self.job=str(uuid.uuid4())
        self.binding=self.bind('alice','session-a')
        self.token='abcdef0123456789'*4
        self.store.save_token('alice','session-a',self.binding,self.token,'apns')

    def tearDown(self): self.tmp.cleanup()

    def bind(self,owner,sid,platform='ios',environment='production',installation=None):
        return self.store.bind(owner,sid,installation or str(uuid.uuid4()),platform,environment)['id']

    def test_cipher_and_owner_are_not_plaintext(self):
        raw=self.store.path.read_bytes()
        self.assertNotIn(self.token.encode(),raw)
        self.assertNotIn(b'alice',raw)
        self.assertNotIn(b'session-a',raw)

    def test_owner_and_session_cannot_cross_bindings(self):
        for owner,sid in [('bob','session-a'),('alice','session-b')]:
            with self.assertRaises(PushError) as e:
                self.store.save_token(owner,sid,self.binding,self.token,'apns')
            self.assertEqual(e.exception.status,404)

    def test_tombstone_rejects_late_write(self):
        self.store.revoke('alice','session-a',self.binding)
        with self.assertRaises(PushError) as e:
            self.store.save_token('alice','session-a',self.binding,self.token,'apns')
        self.assertEqual(e.exception.status,409)
        self.assertEqual(self.store.notify('alice',self.job),{'attempts':[]})

    def test_same_device_token_switch_revokes_previous_owner(self):
        other=self.bind('bob','session-b')
        self.store.save_token('bob','session-b',other,self.token.upper(),'apns')
        self.assertEqual(self.store.notify('alice',self.job),{'attempts':[]})
        self.assertEqual(len(self.store.notify('bob',self.job)['attempts']),1)

    def test_idempotent_binding_and_notify(self):
        iid=str(uuid.uuid4())
        a=self.bind('bob','session-b',installation=iid)
        self.assertEqual(a,self.bind('bob','session-b',installation=iid))
        self.store.notify('alice',self.job); self.store.notify('alice',self.job)
        self.assertEqual(len(self.transport.calls),1)

    def test_started_receipt_before_send(self):
        def check():
            with closing(sqlite3.connect(self.store.path)) as db:
                self.assertEqual(db.execute('SELECT state FROM receipts').fetchone()[0],'dispatching')
        self.transport.before=check
        self.store.notify('alice',self.job)
        self.assertEqual(self.store.receipts('alice',self.job)[0]['state'],'accepted')
        self.assertEqual(self.store.receipts('bob',self.job),[])

    def test_apns_payload_and_fixed_host(self):
        self.store.notify('alice',self.job)
        sent=self.transport.calls[0]
        self.assertTrue(sent['url'].startswith('https://api.push.apple.com/3/device/'))
        self.assertEqual(sent['headers']['apns-topic'],'br.ia.IALD')
        self.assertEqual(sent['headers']['apns-push-type'],'alert')
        self.assertEqual(sent['payload']['job_id'],self.job)
        self.assertEqual(sent['payload']['aps']['alert']['body'],'Sua resposta está pronta.')
        self.assertNotIn('username',sent['payload']); self.assertNotIn('content-available',sent['payload']['aps'])

    def test_development_uses_sandbox(self):
        self.store.revoke_session('alice','session-a')
        b=self.bind('alice','session-a',environment='development')
        self.store.save_token('alice','session-a',b,self.token,'apns')
        self.store.notify('alice',self.job)
        self.assertIn('api.sandbox.push.apple.com',self.transport.calls[0]['url'])

    def test_exception_is_uncertain_without_body_and_no_retry(self):
        self.transport.error=True
        result=self.store.notify('alice',self.job)
        self.assertEqual(result['attempts'],[{'state':'uncertain','http_status':None}])
        self.store.notify('alice',self.job)
        self.assertEqual(len(self.transport.calls),1)
        self.assertNotIn(b'SECRET_PROVIDER',self.store.path.read_bytes())

    def test_http_rejection_status_only(self):
        self.transport.code=400; self.transport.body=b'SECRET_PROVIDER_BODY'
        result=self.store.notify('alice',self.job)
        self.assertEqual(result['attempts'],[{'state':'rejected','http_status':400}])
        self.assertNotIn(b'SECRET_PROVIDER',self.store.path.read_bytes())

    def test_configuration_blocks_before_send(self):
        self.store.apns=None
        self.assertEqual(self.store.notify('alice',self.job)['attempts'],[{'state':'blocked_configuration'}])
        self.assertEqual(self.transport.calls,[])

    def test_apns_invalid_token_revokes(self):
        self.transport.code=410
        self.store.notify('alice',self.job)
        self.assertEqual(self.store.notify('alice',str(uuid.uuid4())),{'attempts':[]})

    def test_fcm_notification_data_and_invalid_token(self):
        b=self.bind('bob','session-b','android','fcm')
        self.store.save_token('bob','session-b',b,'fake:android-token-1234567890','fcm')
        self.transport.code=404
        self.transport.body=json.dumps({'error':{'details':[{
            '@type':'type.googleapis.com/google.firebase.fcm.v1.FcmError','errorCode':'UNREGISTERED'}]}}).encode()
        self.assertEqual(self.store.notify('bob',self.job)['attempts'][0]['state'],'invalid_token')
        msg=self.transport.calls[0]['payload']['message']
        self.assertIn('notification',msg); self.assertIn('data',msg)
        self.assertEqual(msg['android']['notification']['channel_id'],'iald_responses_v1')
        self.assertEqual(self.store.notify('bob',str(uuid.uuid4())),{'attempts':[]})

    def test_rotation_during_inflight_error_keeps_new_token(self):
        self.transport.code=410
        self.transport.before=lambda:self.store.save_token('alice','session-a',self.binding,'A'*64,'apns')
        self.store.notify('alice',self.job)
        with self.store.db() as db:
            row=db.execute('SELECT revoked,token FROM bindings WHERE id=?',(self.binding,)).fetchone()
        self.assertEqual(row['revoked'],0)
        self.assertEqual(self.store.cipher.open(row['token']),b'a'*64)

    def test_restart_does_not_repeat_dispatching(self):
        with self.store.db() as db:
            db.execute('INSERT INTO receipts VALUES(?,?,?,?,?,?,?)',(self.binding,self.job,str(uuid.uuid4()),'dispatching',None,1,1))
        restarted=PushStore(self.tmp.name,cipher=FakeCipher(),apns=FakeAPNs(),transport=self.transport)
        self.assertEqual(restarted.receipts('alice',self.job)[0]['state'],'uncertain')
        restarted.notify('alice',self.job)
        self.assertEqual(self.transport.calls,[])

    def test_concurrent_notify_claims_once(self):
        threads=[threading.Thread(target=self.store.notify,args=('alice',self.job)) for _ in range(6)]
        for t in threads:t.start()
        for t in threads:t.join()
        self.assertEqual(len(self.transport.calls),1)

    def test_bad_token_and_missing_auth_fail_closed(self):
        with self.assertRaises(PushError): self.store.save_token('alice','session-a',self.binding,'https://host/token','apns')
        with self.assertRaises(PushError): self.store.bind('','',str(uuid.uuid4()),'ios','production')

    def test_purge_removes_tokens_and_receipts(self):
        self.store.notify('alice',self.job); self.store.purge('alice')
        self.assertEqual(self.store.receipts('alice',self.job),[])
        self.assertEqual(self.store.notify('alice',str(uuid.uuid4())),{'attempts':[]})

    def test_dpapi_roundtrip_uses_no_real_secret(self):
        if sys.platform!='win32': self.skipTest('DPAPI requires Windows')
        cipher=WindowsCipher(); sample=b'synthetic-notification-test-only'
        sealed=cipher.seal(sample)
        self.assertNotEqual(sealed,sample); self.assertNotIn(sample,sealed)
        self.assertEqual(cipher.open(sealed),sample)


if __name__=='__main__': unittest.main(verbosity=2)
