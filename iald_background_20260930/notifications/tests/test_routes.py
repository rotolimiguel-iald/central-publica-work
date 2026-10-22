"""Route contract tests with a minimal Flask facade; no Flask install or HTTP server."""
from contextlib import contextmanager
import io
import json
import logging
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import uuid

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from iald_chat_push import register, APNs, PushError, _private_transport_logs


class Response:
    def __init__(self,body): self.body=body; self.status_code=200; self.headers={}


class App:
    def __init__(self): self.extensions={}; self.routes={}
    def route(self,path,methods):
        def decorate(fn): self.routes[(path,methods[0])]=fn; return fn
        return decorate


class Cipher:
    def seal(self,value): return b'TEST:'+bytes(x^91 for x in value)
    def open(self,value): return bytes(x^91 for x in value[5:])


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT)
        self.path=Path(self.temp.name)/'lazy'
        self.request=SimpleNamespace()
        self.identity=('alice','session-hash'); self.csrf=True
        fake=SimpleNamespace(request=self.request,jsonify=lambda obj=None,**kw:Response(obj if obj is not None else kw))
        self.app=App()
        with patch.dict(sys.modules,{'flask':fake}):
            self.store=register(self.app,self.path,authenticate=lambda:self.identity,
                                csrf_check=lambda:self.csrf,cipher=Cipher())

    def tearDown(self): self.temp.cleanup()

    def invoke(self,path,method,body,**kw):
        raw=json.dumps(body).encode()
        self.request.stream=io.BytesIO(raw); self.request.content_length=len(raw); self.request.is_json=True
        return self.app.routes[(path,method)](**kw)

    def bind(self):
        return self.invoke('/api/native-push/bindings','POST',
                           {'platform':'ios','installation_id':str(uuid.uuid4()),'consent':True})

    def test_auth_rejection_does_not_construct_store(self):
        for identity in [None,('','session'),('alice','')]:
            self.identity=identity
            response=self.bind()
            self.assertEqual(response.status_code,401)
            self.assertFalse(self.path.exists())
            self.assertEqual(response.headers['Cache-Control'],'private, no-store')

    def test_csrf_must_be_exact_true_before_storage(self):
        for value in [False,None,1,'true']:
            self.csrf=value
            self.assertEqual(self.bind().status_code,403)
            self.assertFalse(self.path.exists())

    def test_consent_and_payload_owner_cannot_override_auth(self):
        response=self.invoke('/api/native-push/bindings','POST',{
            'platform':'ios','installation_id':str(uuid.uuid4()),'consent':True,'username':'bob'})
        self.assertEqual(response.status_code,400); self.assertFalse(self.path.exists())
        response=self.invoke('/api/native-push/bindings','POST',{
            'platform':'ios','installation_id':str(uuid.uuid4()),'consent':False})
        self.assertEqual(response.status_code,400)

    def test_native_register_save_revoke_and_cross_user(self):
        binding=self.bind().body['id']
        path='/api/native-push/bindings/<binding>/token'
        body={'provider':'apns','token':'a'*64}
        self.assertEqual(self.invoke(path,'PUT',body,binding=binding).status_code,200)
        self.identity=('bob','session-hash')
        self.assertEqual(self.invoke(path,'PUT',body,binding=binding).status_code,404)
        self.identity=('alice','session-hash')
        self.assertEqual(self.invoke('/api/native-push/bindings/<binding>','DELETE',{},binding=binding).status_code,200)
        self.assertEqual(self.invoke(path,'PUT',body,binding=binding).status_code,409)

    def test_revoke_session_is_authenticated_scoped_and_idempotent(self):
        binding=self.bind().body['id']
        path='/api/native-push/bindings/<binding>/token'
        body={'provider':'apns','token':'a'*64}
        self.identity=('bob','session-hash')
        self.assertEqual(self.invoke('/api/native-push/revoke-session','POST',{}).body,{'revoked':True})
        self.identity=('alice','session-hash')
        self.assertEqual(self.invoke(path,'PUT',body,binding=binding).status_code,200)
        self.assertEqual(self.invoke('/api/native-push/revoke-session','POST',{'owner':'bob'}).status_code,400)
        for _ in range(2):
            self.assertEqual(self.invoke('/api/native-push/revoke-session','POST',{}).body,{'revoked':True})
        self.assertEqual(self.invoke(path,'PUT',body,binding=binding).status_code,409)
        self.identity=None
        self.assertEqual(self.invoke('/api/native-push/revoke-session','POST',{}).status_code,401)

    def test_request_limit_and_no_raw_exception_body(self):
        self.assertEqual(self.invoke('/api/native-push/bindings','POST',{'data':'x'*9000}).status_code,413)
        self.assertFalse(self.path.exists())
        self.request.stream=io.BytesIO(b'{SECRET'); self.request.content_length=None; self.request.is_json=True
        response=self.app.routes[('/api/native-push/bindings','POST')]()
        self.assertEqual(response.body,{'error':'invalid_json'})
        self.assertFalse(self.path.exists())

    def test_apns_signing_contract_cached_and_secrets_not_in_repr(self):
        calls=[]
        signer=SimpleNamespace(encode=lambda body,key,**kw:(calls.append((body,key,kw)) or 'fake.jwt.test'))
        secret=lambda:b'SYNTHETIC-TEST-KEY'
        config=APNs('ABCDEFGHIJ','0123456789',secret)
        with patch.dict(sys.modules,{'jwt':signer}):
            self.assertEqual(config.bearer(),config.bearer())
        self.assertEqual(len(calls),1)
        self.assertEqual(calls[0][2]['algorithm'],'ES256')
        self.assertEqual(calls[0][2]['headers'],{'kid':'ABCDEFGHIJ'})
        self.assertNotIn('SYNTHETIC',repr(config)); self.assertNotIn('fake.jwt',repr(config))

    def test_apns_signing_failure_masks_details(self):
        def broken(): raise RuntimeError('SECRET_KEY_BODY')
        config=APNs('ABCDEFGHIJ','0123456789',broken)
        with self.assertRaises(PushError) as caught: config.bearer()
        self.assertEqual(str(caught.exception),'apns_signing_unavailable')

    def test_provider_library_logs_are_suppressed_only_during_send(self):
        for name in ('httpx','httpcore.http2','hpack.hpack'):
            logger=logging.getLogger(name)
            output=io.StringIO(); handler=logging.StreamHandler(output)
            level,propagate=logger.level,logger.propagate
            logger.addHandler(handler); logger.setLevel(logging.DEBUG); logger.propagate=False
            try:
                with _private_transport_logs(): logger.info('SYNTHETIC_PRIVATE_TOKEN')
                logger.info('public-after')
                self.assertEqual(output.getvalue(),'public-after\n')
            finally:
                logger.removeHandler(handler); logger.setLevel(level); logger.propagate=propagate


if __name__=='__main__': unittest.main(verbosity=2)
