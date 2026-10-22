import ast
import base64
import ctypes
from ctypes import wintypes
from contextlib import closing
import io
import json
import math
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import wave

import private_media_store as private
import iald_mimo_multimodal as multimodal

W=Path(__file__).resolve().parent
R=Path('C:/IALD/projetos_pyhton/IALD')
sys.path.insert(0,str(W.parent/'routing_stage'))
HOST_RATES={'input':.435,'cache_read':.0036,'output':.87}
t=ast.parse((R/'iald_chat_jobs.py').read_text(encoding='utf-8'))
node=next(n for n in t.body if isinstance(n,ast.ClassDef) and n.name=='WindowsCipher')
ns=dict(ctypes=ctypes,wintypes=wintypes,os=os)
exec(compile(ast.Module(body=[node],type_ignores=[]),'existing DPAPI primitive','exec'),ns)


class CountedCipher:
    def __init__(self):self.real=ns['WindowsCipher']();self.reads=0
    def seal(self,raw):return self.real.seal(raw)
    def open(self,raw):self.reads+=1;return self.real.open(raw)


def small_wav(seconds=1):
    file=io.BytesIO()
    with wave.open(file,'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(8000);w.writeframes(b'\0\0'*(8000*seconds))
    return file.getvalue()


class MediaTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=W,prefix='test_media_');self.root=Path(self.temp.name)
        self.cipher=CountedCipher();self.scope=private.Scope('owner-a','generation1','c_same')
        self.store=private.PrivateMediaStore(self.root/'store',authorize_scope=lambda s:True,validate_media=multimodal.validate_upload,cipher=self.cipher)
        self.runtime=private.PrivateMediaRuntime(self.store,self.scope,authorize_dispatch=lambda:True,rates=HOST_RATES)
    def tearDown(self):self.temp.cleanup()
    def put(self,raw=None,scope=None,mime='audio/wav'):
        raw=small_wav() if raw is None else raw
        return self.store.put(io.BytesIO(raw),scope=scope or self.scope,mime=mime,content_length=len(raw))
    def messages(self,part):return [{'role':'system','content':'SCIENCE_UNCHANGED'}, {'role':'user','content':[part,{'type':'text','text':'describe'}]}]
    def test_large_audio_no_30s_cap(self):
        raw=(W.parent/'test_assets/tone_120s.wav').read_bytes();part=self.put(raw)
        self.assertGreater(len(raw),512000);self.assertEqual(part['duration_seconds'],120)
        metadata=private.resolve_media_metadata(self.messages(part),store=self.store,scope=self.scope)
        self.assertEqual(metadata[0]['duration_seconds'],120);self.assertEqual(self.cipher.reads,0)
        compact=self.messages(part);body={'model':'mimo-v2.6-pro','messages':compact}
        bound=self.runtime.admit(body,131072)
        self.assertLess(bound['input_tokens_bound'],10000)
        self.assertNotIn('base64',json.dumps(compact));self.assertIsNone(part['expires_at'])
        body['max_completion_tokens']=bound['output_reserved_tokens']
        final=self.runtime.expand(body,provider='mimo',plan=bound)
        actual=base64.b64decode(final['messages'][1]['content'][0]['input_audio']['data'].split(',',1)[1])
        self.assertEqual(actual,raw);self.assertEqual(final['messages'][0],compact[0])
        blob=(self.store.blobs/(part['media_ref']+'.bin')).read_bytes()
        self.assertNotIn(raw[:64],blob)
    def test_wrong_owner_zero_payload_reads(self):
        part=self.put();other=private.Scope('owner-b','generation1','c_same')
        original_open=Path.open
        def guarded_open(path,*args,**kwargs):
            if path.parent==self.store.blobs:self.fail('Wrong owner attempted blob I/O')
            return original_open(path,*args,**kwargs)
        with patch.object(Path,'open',guarded_open),patch.object(self.store.cipher,'open',side_effect=AssertionError('decrypt forbidden')):
            with self.assertRaises(private.MediaUnavailable):self.store.read(part['media_ref'],other,part['sha256'])
            with self.assertRaises(private.MediaUnavailable):private.resolve_media_metadata(self.messages(part),store=self.store,scope=other)
    def test_wrong_generation_and_conversation(self):
        part=self.put()
        for scope in (private.Scope('owner-a','generation2','c_same'),private.Scope('owner-a','generation1','c_other')):
            with self.assertRaises(private.MediaUnavailable):self.store.read(part['media_ref'],scope,part['sha256'])
        self.assertEqual(self.cipher.reads,0)
    def test_ciphertext_tamper_fails_closed(self):
        part=self.put();path=self.store.blobs/(part['media_ref']+'.bin')
        data=bytearray(path.read_bytes());data[-1]^=1;path.write_bytes(data)
        with self.assertRaises((OSError,private.MediaUnavailable)):
            self.store.read(part['media_ref'],self.scope,part['sha256'])
    def test_first_upload_same_cid_distinct_owner_namespace(self):
        a=self.put();b=self.put(scope=private.Scope('owner-b','generation1','c_same'))
        self.assertNotEqual(a['media_ref'],b['media_ref'])
        with self.assertRaises(private.MediaUnavailable):self.store.metadata(b['media_ref'],self.scope)
    def test_forged_client_metadata(self):
        part=self.put()
        for key,value in [('duration_seconds',float('nan')),('duration_seconds',10000),('width',99999),('sha256','0'*64)]:
            with self.subTest(key=key),self.assertRaises(private.MediaError):self.runtime.canonicalize(self.messages({**part,key:value}))
        self.assertEqual(self.cipher.reads,0)
    def test_invalid_stored_facts_refuse(self):
        part=self.put();part['duration_seconds']=float('nan')
        with closing(self.store._db()) as db:db.execute('UPDATE media SET metadata=? WHERE id=?',(json.dumps(part),part['media_ref']))
        with self.assertRaises(private.MediaUnavailable):self.store.metadata(part['media_ref'],self.scope)
    def test_hash_failure_before_blob_read(self):
        part=self.put()
        with self.assertRaises(private.MediaUnavailable):self.store.read(part['media_ref'],self.scope,'0'*64)
        self.assertEqual(self.cipher.reads,0)
    def test_signature_and_container_refuse(self):
        for raw in (b'http://127.0.0.1/private',b'RIFF0000WAVEinvalid'):
            with self.assertRaises((private.MediaError,ValueError,EOFError,wave.Error)):self.put(raw)
    def test_http_size_guard_zero_body_reads(self):
        stream=types.SimpleNamespace(read=lambda *_:self.fail('body read forbidden'))
        for size in (None,0,private.MAX_RAW_BYTES+1):
            with self.assertRaises(private.MediaError):self.store.put(stream,scope=self.scope,mime='audio/wav',content_length=size)
    def test_unauthorized_upload_zero_body_reads(self):
        self.store.authorize_scope=lambda _:False
        with self.assertRaises(private.MediaUnavailable):self.store.put(types.SimpleNamespace(read=lambda *_:self.fail('body read forbidden')),scope=self.scope,mime='audio/wav',content_length=100)
    def test_incomplete_and_extra_body(self):
        raw=small_wav()
        for size in (len(raw)-1,len(raw)+1):
            with self.assertRaises(private.MediaError):self.store.put(io.BytesIO(raw),scope=self.scope,mime='audio/wav',content_length=size)
    def test_disk_and_rate_refuse_before_body(self):
        stream=types.SimpleNamespace(read=lambda *_:self.fail('body read forbidden'))
        with patch.object(private.shutil,'disk_usage',return_value=types.SimpleNamespace(free=0)):
            with self.assertRaises(private.MediaError):self.store.put(stream,scope=self.scope,mime='audio/wav',content_length=100)
        self.store.uploads_per_minute=0
        with self.assertRaises(private.MediaError):self.store.put(stream,scope=self.scope,mime='audio/wav',content_length=100)
    def test_quota_before_body(self):
        self.store.owner_quota=1
        with self.assertRaises(private.MediaError):self.store.put(types.SimpleNamespace(read=lambda *_:self.fail('read forbidden')),scope=self.scope,mime='audio/wav',content_length=100)
    def test_nonmimo_worker_block_before_decrypt(self):
        part=self.put()
        for provider,worker in [('kimi',False),('openai',False),('mimo',True)]:
            with self.assertRaises(private.MediaError):private.resolve_media_metadata(self.messages(part),store=self.store,scope=self.scope,provider=provider,worker=worker)
        self.assertEqual(self.cipher.reads,0)
    def test_dispatch_revoked_zero_decrypt(self):
        part=self.put();self.runtime.authorize_dispatch=lambda:False
        with self.assertRaises(private.MediaUnavailable):self.runtime.expand({'messages':self.messages(part)},provider='mimo',plan={})
        self.assertEqual(self.cipher.reads,0)
    def test_retention_no_automatic_expiry_or_history_delete(self):
        part=self.put();self.store.clock=lambda:10**15
        self.assertEqual(self.store.metadata(part['media_ref'],self.scope),part)
        revoked=self.store.revoke_conversation(self.scope)
        self.assertFalse(revoked['conversation_history_modified'])
        with self.assertRaises(private.MediaUnavailable):self.store.metadata(part['media_ref'],self.scope)
    def test_account_delete_requires_distinct_guard(self):
        part=self.put()
        with self.assertRaises(private.MediaUnavailable):self.store.revoke_account(self.scope,authorize_account_deletion=lambda *_:False)
        self.store.revoke_account(self.scope,authorize_account_deletion=lambda *_:True)
        with self.assertRaises(private.MediaUnavailable):self.store.metadata(part['media_ref'],self.scope)
    def test_context_refusal_preserves_input(self):
        part=self.put();messages=self.messages(part);messages[0]['content']='S'*1048576
        original=json.dumps(messages)
        with self.assertRaises(ValueError):self.runtime.admit({'messages':messages},131072)
        self.assertEqual(json.dumps(messages),original);self.assertEqual(self.cipher.reads,0)
    def test_decoder_pin_missing_refuses_video(self):
        with patch.object(multimodal,'VENDOR',self.root/'missing'):
            raw=(W.parent/'test_assets/red_30s.mp4').read_bytes()
            with self.assertRaises(ValueError):self.put(raw,mime='video/mp4')
    def test_fake_probe_nan_and_dimensions_bomb(self):
        raw=(W.parent/'test_assets/red_30s.mp4').read_bytes()
        for d,w,h in [(float('nan'),100,100),(30,2**31,100),(30,0,100)]:
            with patch.object(multimodal,'probe_media',return_value=dict(duration=d,width=w,height=h,types=['video'])):
                with self.assertRaises(ValueError):multimodal.validate_upload(raw,'video/mp4')
    def test_real_video_30s_pin_and_metadata(self):
        original_factory=tempfile.TemporaryDirectory
        def local_temp(*args,**kwargs):kwargs['dir']=self.root;return original_factory(*args,**kwargs)
        with patch.object(multimodal,'VENDOR',R/'vendor/ffmpeg'),patch.object(multimodal.tempfile,'TemporaryDirectory',local_temp):
            part=self.put((W.parent/'test_assets/red_30s.mp4').read_bytes(),mime='video/mp4')
        self.assertAlmostEqual(part['duration_seconds'],30,places=1)
        self.assertGreater(part['width'],0);self.assertGreater(part['height'],0)
        bound=self.runtime.admit({'messages':self.messages(part)},131072)
        self.assertGreater(bound['media_tokens_estimate'],0)
    def test_full_encoded_envelope_arithmetic(self):
        self.assertEqual(private.MAX_RAW_BYTES,37_499_904)
        self.assertLessEqual(4*((private.MAX_RAW_BYTES+2)//3)+128,50_000_000)


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(MediaTests))
    report={'passed':result.wasSuccessful(),'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'real_dpapi':True,'real_verified_ffprobe_video':True,'provider_calls':0,'runtime_changes':0}
    (W/'TEST_RESULTS.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
