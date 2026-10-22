import io
import json
from pathlib import Path
import tempfile
import unittest
from flask import Flask,Request,request

import private_media_store as private
import iald_mimo_multimodal as media
from private_media_routes import register_private_media
from test_private_media import CountedCipher,small_wav

W=Path(__file__).resolve().parent
class RouteTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=W,prefix='test_routes_')
        self.app=Flask('private-media-offline');self.app.config['MAX_CONTENT_LENGTH']=1024
        # Parent-owned readonly property glue, reproduced in test only.
        class HostRequest(Request):
            @property
            def max_content_length(self):
                if self.path=='/api/private-media' and self.method=='POST':return private.MAX_RAW_BYTES
                return super().max_content_length
        self.app.request_class=HostRequest
        self.store=private.PrivateMediaStore(self.temp.name,authorize_scope=lambda _:True,validate_media=media.validate_upload,cipher=CountedCipher())
        def scope(cid):return private.Scope(request.headers.get('X-Owner','one'),'g1',cid)
        register_private_media(self.app,self.store,host_scope=scope,
            authenticate_csrf=lambda:request.headers.get('X-Test-Auth')=='ok',upload_eligible=lambda _:True)
        @self.app.post('/ordinary')
        def ordinary():return str(len(request.get_data()))
        self.client=self.app.test_client();self.headers={'Content-Type':'audio/wav','X-Test-Auth':'ok'}
    def tearDown(self):self.temp.cleanup()
    def upload(self):return self.client.post('/api/private-media?conversation_id=c_first',data=small_wav(),headers=self.headers)
    def test_readonly_property_route_upload_exceeds_unchanged_global(self):
        result=self.upload();self.assertEqual(result.status_code,201)
        self.assertGreater(result.json['bytes'],1024);self.assertEqual(self.app.config['MAX_CONTENT_LENGTH'],1024)
        self.assertEqual(self.client.post('/ordinary',data=b'x'*2048).status_code,413)
    def test_auth_before_body(self):
        result=self.client.post('/api/private-media?conversation_id=c_first',data=small_wav(),content_type='audio/wav')
        self.assertEqual(result.status_code,403)
    def test_forged_size_before_body(self):
        with self.app.test_request_context('/api/private-media?conversation_id=c_first',method='POST',headers=self.headers,environ_overrides={'CONTENT_LENGTH':str(private.MAX_RAW_BYTES+1)}):
            result=self.app.preprocess_request();self.assertEqual(result[1],413)
    def test_wrong_owner_metadata_nondisclosure(self):
        part=self.upload().json
        result=self.client.get('/api/private-media/'+part['media_ref']+'?conversation_id=c_first',headers={'X-Test-Auth':'ok','X-Owner':'two'})
        self.assertEqual(result.status_code,404);self.assertNotIn('sha256',result.json)
    def test_no_raw_download_url(self):
        part=self.upload().json
        result=self.client.get('/api/private-media/'+part['media_ref']+'?conversation_id=c_first',headers=self.headers)
        self.assertEqual(result.status_code,200);self.assertEqual(result.json['type'],'iald_media')
        self.assertNotIn('base64',json.dumps(result.json));self.assertIsNone(result.json['expires_at'])
        self.assertEqual(self.client.get('/api/private-media/'+part['media_ref']+'/raw',headers=self.headers).status_code,404)
    def test_absent_parent_property_refuses(self):
        self.app.request_class=Request
        result=self.upload();self.assertEqual(result.status_code,503)

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(RouteTests))
    (W/'ROUTE_TEST_RESULTS.json').write_text(json.dumps({'passed':result.wasSuccessful(),'tests':result.testsRun,'errors':len(result.errors),'failures':len(result.failures),'network_calls':0},indent=2),encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
