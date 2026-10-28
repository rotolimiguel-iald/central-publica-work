"""READY consumer contract fixtures only; no TTS, encode, capture or real data writes."""
from pathlib import Path
from types import SimpleNamespace
from tempfile import TemporaryDirectory
from unittest.mock import patch
import json, runpy, unittest

E = Path(__file__).resolve().parent
m = runpy.run_path(str(E/'media_v402_worker.py'))
g = m['main'].__globals__


class ReadyTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(dir=E)
        self.c = Path(self.temp.name)/'E'; self.r = Path(self.temp.name)/'V'
        self.c.mkdir(); self.r.mkdir()
        self.source = 'fixture-v402-source'
        self.write(self.c/'canonical_seal.json',{'um_version':'v402','sha256':{'um.py':self.source}})
        self.write(self.c/'SOURCE_CAPTURE.json',{'source':'v402','source_sha256':self.source,
            'canonical_seal':m['pin'](self.c/'canonical_seal.json')})
        self.write(self.c/'NUMERIC_COMPARISON.json',{'status':'PASS','source':'v402',
            'source_sha256':self.source,'unexpected_differences':[]})
        self.write(self.r/'data/hud.json',{'seal_version':'v402','seal_pin':self.source})
        self.write(self.c/'fixture.json',{'fixture':True})
        small=m['pin'](self.c/'fixture.json')
        self.ready={'status':'DATA_READY','source':'v402','source_sha256':self.source,
            'unexpected_scientific_differences':0,'anchors':{'total':64,'all_ok':True},
            'comparison':m['pin'](self.c/'NUMERIC_COMPARISON.json'),'data_files':[m['pin'](self.r/'data/hud.json')],
            'source_files':[small],'seal':small,'integration':small,'root_provenance':small}
        self.write(self.c/'DATA_READY.json',self.ready)
        self.parent={'status':'PASS_WITH_SCOPE','actor':'codex-video-v7','source':'v402','source_sha256':self.source,
            'unexpected_differences':[],'anchors_all_ok':True,'anchors':64,'data_ready_sha256':m['sha'](self.c/'DATA_READY.json')}
        self.write(self.c/'PARENT_NUMERIC_REVIEW.json',self.parent)
        self.options=SimpleNamespace(data_ready=self.c/'DATA_READY.json',audio_ready=self.c/'AUDIO_READY.json',audio_dir=self.r/'audio')
        self.config=patch.dict(g,C=self.c,R=self.r,options=self.options,baseline={'source_sha256':self.source},audio_binding=None)
        self.config.start()

    def tearDown(self):
        self.config.stop(); self.temp.cleanup()

    def write(self,p,obj):
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes((json.dumps(obj,sort_keys=True)+'\n').encode())

    def test_approved_data_schema_consumed(self):
        ready,frozen=m['readiness']()
        self.assertEqual(ready['status'],'DATA_READY')
        self.assertTrue(any(Path(x['file']).name=='PARENT_NUMERIC_REVIEW.json' for x in frozen))

    def test_parent_review_pins_different_data_rejected(self):
        self.parent['data_ready_sha256']='0'*64;self.write(self.c/'PARENT_NUMERIC_REVIEW.json',self.parent)
        with self.assertRaisesRegex(AssertionError,'pins another'):m['readiness']()

    def test_unexpected_scientific_difference_rejected(self):
        comparison=m['load'](self.c/'NUMERIC_COMPARISON.json'); comparison['unexpected_differences']=[{'fixture':'forbidden'}]
        self.write(self.c/'NUMERIC_COMPARISON.json',comparison)
        self.ready['comparison']=m['pin'](self.c/'NUMERIC_COMPARISON.json');self.write(self.c/'DATA_READY.json',self.ready)
        with self.assertRaisesRegex(AssertionError,'unauthorized numeric difference'):m['readiness']()

    def test_stale_canonical_version_rejected(self):
        self.write(self.c/'canonical_seal.json',{'um_version':'v403','sha256':{'um.py':self.source}})
        with self.assertRaisesRegex(AssertionError,'Changed pin'):m['readiness']()

    def test_missing_parent_review_waits(self):
        (self.c/'PARENT_NUMERIC_REVIEW.json').unlink()
        self.assertIsNone(m['readiness']())

    def test_current_parent_intent_uses_nested_pins(self):
        self.write(self.c/'AUDIO_READY.json',{'fixture':True})
        self.write(self.c/'MEDIA_PREPARED.json',{'source':'v402'})
        intent={'status':'INTENT_BEFORE_SINGLE_BROWSER_PIPELINE',
            'data_ready':m['pin'](self.c/'DATA_READY.json'),'audio_ready':m['pin'](self.c/'AUDIO_READY.json'),
            'numeric_review':m['pin'](self.c/'PARENT_NUMERIC_REVIEW.json'),
            'media_prepared':m['pin'](self.c/'MEDIA_PREPARED.json')}
        m['verify_intent'](intent)
        intent['data_ready']['sha256']='0'*64
        with self.assertRaisesRegex(AssertionError,'Changed pin'):m['verify_intent'](intent)

    def test_old_scalar_intent_schema_rejected(self):
        with self.assertRaises(KeyError):
            m['verify_intent']({'status':'INTENT_BEFORE_SINGLE_BROWSER_PIPELINE','data_ready_sha256':'fixture'})

    def audio_fixture(self,delivery_source='v402',inflight=False):
        d=self.r/'audit/DELIVERY_D_V402.json'
        self.write(d,{'status':'PASS_BUILDER_READY_FOR_INDEPENDENT_REVIEW','source':delivery_source,'source_sha256':self.source})
        self.write(self.c/'AUDIO_READY.json',{'status':'AUDIO_READY','actor':'codex-video-audio',
            'source':'v402','source_sha256':self.source,'plan_sha256':'fixture-plan','receipt':m['pin'](d)})
        self.write(self.r/'audio/NARRATION_BUILD.json',{'status':'COMPLETED','plan_sha256':'fixture-plan','tts':False,
            'tts_inflight':inflight,'pending':[]})
        self.write(self.r/'audio/NARRATION_PLAN.json',{'plan_sha256':'fixture-plan'})

    def test_current_audio_ready_accepts_cache_only_mode(self):
        self.audio_fixture()
        small=self.c/'fixture.json'
        with patch.dict(g['M'],audio_inputs=lambda r,a,f:({'en':small,'pt-BR':small},small),captions=lambda r,f:{'files':[m['pin'](small)]}),\
             patch.dict(g,save=lambda p,v:None):
            self.assertTrue(m['audio_ready']())
            self.assertEqual(g['audio_binding']['plan_sha256'],'fixture-plan')

    def test_stale_delivery_d_rejected(self):
        self.audio_fixture(delivery_source='v401')
        with self.assertRaises(AssertionError):m['audio_ready']()

    def test_tts_inflight_rejected(self):
        self.audio_fixture(inflight=True)
        with self.assertRaises(AssertionError):m['audio_ready']()


if __name__ == '__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ReadyTests))
    report={'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,
        'failures':len(result.failures),'errors':len(result.errors),'source':'v402',
        'worker':m['pin'](E/'media_v402_worker.py'),'helper':m['pin'](m['R']/'cinema/media_v7.py'),
        'test':m['pin'](Path(__file__)),
        'scope':'Synthetic DATA_READY/AUDIO_READY schemas and pin/source controls. Audio helper mocked; actual audio/text review remains pending. No encode/render/TTS.'}
    m['save_original'](E/'MEDIA_READY_CONTRACT_TESTS.json',report)
    raise SystemExit(0 if result.wasSuccessful() else 1)
