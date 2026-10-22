"""Actual staged functions, fake HTTP/credentials/wallet; no remote calls."""
import ast
import base64
import binascii
import copy
from contextlib import closing
import io
import json
from pathlib import Path
import sys
import tempfile
import threading
import types
import unittest
from unittest.mock import patch

from test_private_media import CountedCipher,HOST_RATES,small_wav
import private_media_store as private
import iald_mimo_multimodal as multimodal
import iald_media_budget as budget

W=Path(__file__).resolve().parent;R=Path('C:/IALD/projetos_pyhton/IALD')
tree=ast.parse((W/'iald_app_providers.py').read_text(encoding='utf-8'))
names={'image_parts','wire_messages','transport_tool_options','output_budget','check_window','scoped_task_names'}
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
nodes.append(next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='_api'))

class BoundaryReached(BaseException):pass
class WalletRefused(ValueError):pass

class ProviderBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=W,prefix='test_provider_')
        self.scope=private.Scope('owner','gen','c_first')
        self.cipher=CountedCipher()
        self.store=private.PrivateMediaStore(self.temp.name,authorize_scope=lambda _:True,validate_media=multimodal.validate_upload,cipher=self.cipher)
        self.runtime=private.PrivateMediaRuntime(self.store,self.scope,authorize_dispatch=lambda:True,rates=HOST_RATES)
        raw=(W.parent/'test_assets/tone_120s.wav').read_bytes()
        self.part=self.store.put(io.BytesIO(raw),scope=self.scope,mime='audio/wav',content_length=len(raw))
        self.raw=raw;self.captured={};self.spending_calls=[];self.keys=0
        def project(messages):
            self.assertNotIn('base64,',json.dumps(messages));return copy.deepcopy(messages)
        def http(label,fn,*args,**kwargs):
            self.captured.update(kwargs['json']);raise BoundaryReached()
        memory=types.SimpleNamespace(project_messages=project,http_call=http)
        def key():self.keys+=1;return 'OFFLINE_TEST_ONLY'
        self.ns=dict(base64=base64,binascii=binascii,json=json,app_memory=memory,
            router_media_view=types.SimpleNamespace(project_system_messages=project),
            contains_refs=private.contains_refs,contains_media=private.contains_media,reject_worker_media=private.reject_worker_media,MediaError=private.MediaError,
            MODELS={'mimo':{'model':'mimo-v2.6-pro','url':'https://api.xiaomimimo.com/v1/chat/completions','output':131072}},
            WINDOW=1048576,MAX_ROUNDS=4,MAX_TOOLS=4,MAX_PARSED_TOOLS=32,TOOL_NAMES=frozenset(),TASK_TOOL_NAMES=frozenset(),
            adapter=lambda _:types.SimpleNamespace(load_mimo=key))
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'staged provider actual functions','exec'),self.ns)
        self.module_stub=types.ModuleType('iald_motor_claude');self.module_stub._tipo_pelos_bytes=lambda _:None
        self.stub=patch.dict(sys.modules,{'iald_motor_claude':self.module_stub});self.stub.start()
        self.reqstub=types.ModuleType('requests');self.reqstub.post=lambda *_a,**_k:self.fail('network forbidden')
        self.reqpatch=patch.dict(sys.modules,{'requests':self.reqstub});self.reqpatch.start()
    def tearDown(self):self.reqpatch.stop();self.stub.stop();self.temp.cleanup()
    def messages(self):return [{'role':'user','content':[self.part,{'type':'text','text':'tone?'}]}]
    def spending(self,refuse=False):
        def before(provider,body,bound,*,media_plan):
            self.assertNotIn('base64,',json.dumps(body));self.assertEqual(bound,media_plan['input_tokens_bound'])
            self.spending_calls.append(media_plan)
            if refuse:raise WalletRefused()
        return types.SimpleNamespace(before=before,discard_undispatched=lambda:None)
    def api(self,messages,spending=None):
        self.last_record={'calls':[]}
        return self.ns['_api'](types.SimpleNamespace(save=lambda _:None),'mimo',messages,[],None,None,
            threading.Event(),[],self.last_record,0,None,spending=spending,private_media=self.runtime)
    def test_actual_api_only_final_http_copy_expanded(self):
        prefix=(R/'.iald_runtime/haiku/prefix.md').read_text(encoding='utf-8')
        messages=self.ns['wire_messages'](self.messages(),prefix,provider='mimo',images_authorized=True,media_authorized=True,private_media=self.runtime)
        self.assertEqual(self.cipher.reads,0)
        with self.assertRaises(BoundaryReached):self.api(messages,self.spending())
        uri=self.captured['messages'][1]['content'][0]['input_audio']['data']
        self.assertEqual(base64.b64decode(uri.split(',',1)[1]),self.raw)
        self.assertTrue(self.captured['messages'][0]['content'].startswith(prefix))
        self.assertEqual(len(self.spending_calls),1);self.assertEqual(self.cipher.reads,1)
        self.assertEqual(messages[1]['content'][0]['type'],'iald_media')
    def test_wallet_rejection_no_blob_decrypt(self):
        with self.assertRaises(WalletRefused):self.api(self.messages(),self.spending(refuse=True))
        self.assertEqual(self.cipher.reads,0);self.assertFalse(self.captured)
    def test_wrong_user_before_credentials_or_bytes(self):
        self.runtime.scope=private.Scope('wrong','gen','c_first')
        with self.assertRaises(private.MediaUnavailable):self.api(self.messages(),self.spending())
        self.assertEqual(self.keys,0);self.assertEqual(self.cipher.reads,0)
    def test_local_resolution_failure_releases_hold_and_not_dispatched(self):
        self.runtime.authorize_dispatch=lambda:False
        spending=self.spending();discarded=[]
        spending.discard_undispatched=lambda:discarded.append(True)
        with self.assertRaises(private.MediaUnavailable):self.api(self.messages(),spending)
        self.assertEqual(discarded,[True]);self.assertEqual(self.last_record['calls'],[])
        self.assertEqual(self.cipher.reads,0)
    def test_wire_nonmimo_rejects_before_bytes(self):
        with self.assertRaises(private.MediaError):self.ns['wire_messages'](self.messages(),'SCIENCE',provider='kimi',private_media=self.runtime)
        self.assertEqual(self.cipher.reads,0)
    def test_scoped_metrics_compatibility(self):
        out=self.runtime.metrics_view(self.messages())
        self.assertEqual(out[0]['content'][0]['type'],'input_audio')
        self.assertNotIn('base64',json.dumps(out));self.assertEqual(self.cipher.reads,0)
    def test_unified_plan_and_legacy_without_reingestion(self):
        uri='data:audio/wav;base64,'+base64.b64encode(small_wav(2)).decode()
        messages=[{'role':'user','content':[{'type':'input_audio','input_audio':{'data':uri}}]}]
        with closing(self.store._db()) as db:before=db.execute('SELECT count(*) FROM media').fetchone()[0]
        plans=self.runtime.routing_options({'messages':messages})
        self.runtime.select_routing_policy('default')
        self.assertEqual(plans['default']['items'][0]['duration_seconds'],2)
        with closing(self.store._db()) as db:self.assertEqual(db.execute('SELECT count(*) FROM media').fetchone()[0],before)
        projected=budget.routing_options(plans);self.assertNotIn('base64',json.dumps(projected))
    def test_three_legacy_512k_mixed_refs_full_science_prefix(self):
        raw=small_wav(32) #512044 bytes, matching the v34 small-media history.
        self.assertGreater(len(raw),512000)
        uri='data:audio/wav;base64,'+base64.b64encode(raw).decode()
        prefix=(R/'.iald_runtime/haiku/prefix.md').read_text(encoding='utf-8')
        messages=[{'role':'system','content':prefix}]
        for i in range(3):
            messages.append({'role':'user','content':[{'type':'input_audio','input_audio':{'data':uri}},{'type':'text','text':'old'+str(i)}]})
            messages.append({'role':'assistant','content':'historical answer'})
        messages.append({'role':'user','content':[self.part,{'type':'text','text':'compare'}]})
        self.assertGreater(len(json.dumps(messages)),private.MAX_CHAT_JSON_BYTES)
        canonical=self.runtime.canonicalize(messages)
        self.assertEqual(canonical,messages)
        body={'model':'mimo-v2.6-pro','messages':canonical}
        plan=self.runtime.admit(body,131072)
        self.assertEqual(len(plan['items']),4)
        body['max_completion_tokens']=plan['output_reserved_tokens']
        final=self.runtime.expand(body,provider='mimo',plan=plan)
        self.assertEqual(final['messages'][0]['content'],prefix)
        for index in (1,3,5):self.assertEqual(final['messages'][index]['content'][0]['input_audio']['data'],uri)
        self.assertEqual(messages,canonical)
    def test_video_plan_exact_wire_policy(self):
        fact=dict(kind='video',duration_seconds=30,width=32,height=32,has_audio=False)
        original=self.store.validate_media;self.store.validate_media=lambda *_:fact
        part=self.store.put(io.BytesIO(b'\0\0\0\x18ftypisom'),scope=self.scope,mime='video/mp4',content_length=12)
        self.store.validate_media=original
        body={'messages':[{'role':'user','content':[part]}]}
        plans=self.runtime.routing_options(body,proposals={'low':{'fps':.5,'media_resolution':'max'}})
        self.runtime.select_routing_policy('low');plan=self.runtime.admit(body,131072)
        body['max_completion_tokens']=plan['output_reserved_tokens']
        final=self.runtime.expand(body,provider='mimo',plan=plan)
        self.assertEqual(final['messages'][0]['content'][0]['fps'],.5)
        self.assertEqual(final['messages'][0]['content'][0]['media_resolution'],'max')
    def test_no_hidden_frame_cap_coverage(self):
        original=self.store.validate_media;self.store.validate_media=lambda *_:dict(kind='video',duration_seconds=30000,width=32,height=32,has_audio=False)
        part=self.store.put(io.BytesIO(b'\0\0\0\x18ftypisom'),scope=self.scope,mime='video/mp4',content_length=12)
        self.store.validate_media=original
        body={'messages':[{'role':'user','content':[part]}]}
        with self.assertRaises(ValueError):self.runtime.routing_options(body,proposals={'low':{'fps':.1,'media_resolution':'default'}})
        self.assertEqual(self.cipher.reads,0)
    def test_storage_partition_not_bearer(self):
        other=private.Scope('owner2','gen','c_first')
        self.assertNotEqual(private.media_scope_token(self.scope),private.media_scope_token(other))
        self.assertNotEqual(private.media_scope_token(self.scope),private.media_scope_token(private.Scope('owner','gen2','c_first')))
        self.assertNotIn('owner',private.media_scope_token(self.scope))

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ProviderBoundaryTests))
    (W/'PROVIDER_TEST_RESULTS.json').write_text(json.dumps({'passed':result.wasSuccessful(),'tests':result.testsRun,'errors':len(result.errors),'failures':len(result.failures),'network_calls':0},indent=2),encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
