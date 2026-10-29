"""Bounded offline checks: no browser, FFmpeg, GPU, network or scientific import."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
import json, runpy, subprocess, unittest

C = Path(__file__).resolve().parent
worker = runpy.run_path(str(C/'media_v404_worker.py'))
g = worker['main'].__globals__

class WorkerTests(unittest.TestCase):
    def test_actual_namespace_contract(self):
        self.assertEqual(worker['self_test']()['status'], 'PASS')

    def test_launch_requires_coordinator_signal(self):
        with patch.dict(g, options=SimpleNamespace(start_authorized=False)):
            with self.assertRaisesRegex(AssertionError, 'explicit coordinator signal'):
                worker['main']()
        self.assertFalse(worker['LOCK'].exists())

    def test_source_change_blocks_before_stage(self):
        original_stage = Mock()
        with patch.dict(g, guard=Mock(side_effect=RuntimeError('source changed')), original_stage=original_stage):
            with self.assertRaisesRegex(RuntimeError, 'source changed'):
                worker['guarded_stage'](None,'fixture',[],{}, {},lambda x:None)
        original_stage.assert_not_called()

    def test_change_in_flight_stops_only_own_child(self):
        child = Mock()
        child.pid = 123456; child.returncode = -1
        child.poll.return_value = None
        child.communicate.side_effect = [subprocess.TimeoutExpired('fixture',5),(b'',b'preserved failure')]
        receipts, logs = [], []
        guard = Mock(side_effect=[None,RuntimeError('source changed')])
        pipe = SimpleNamespace(ff=Path('fixture-ffmpeg'),current=C/'synthetic-stage',command_seconds=0)
        with patch.dict(g, guard=guard, save=lambda p,d:receipts.append(d)), \
             patch.dict(g['M'], atomic=lambda p,b:logs.append(b)), \
             patch.object(g['subprocess'],'Popen',return_value=child):
            with self.assertRaisesRegex(RuntimeError, 'source changed'):
                worker['guarded_run'](pipe,[], 'fixture')
        child.terminate.assert_called_once_with()
        self.assertEqual(receipts[-1]['status'],'FAILED')
        self.assertEqual(logs,[b'preserved failure'])

    def test_successful_child_records_measured_stage(self):
        child = Mock(pid=123456,returncode=0)
        child.communicate.return_value = (b'output',b'log')
        receipts = []
        pipe = SimpleNamespace(ff=Path('fixture-ffmpeg'),current=C/'synthetic-stage',command_seconds=0)
        with patch.dict(g,guard=Mock(),save=lambda p,d:receipts.append(d)), \
             patch.dict(g['M'],atomic=Mock()), patch.object(g['subprocess'],'Popen',return_value=child):
            result = worker['guarded_run'](pipe,[],'fixture')
        self.assertEqual(result.returncode,0)
        self.assertEqual(receipts[-1]['status'],'COMPLETE')
        self.assertGreaterEqual(receipts[-1]['elapsed_seconds'],0)
        child.terminate.assert_not_called()

    def test_job_selection_rejects_old_and_progress_and_partial(self):
        files = [Path('film1_old.json'),Path('film1_current.progress.json'),Path('film1_partial.json'),Path('film1_current.json')]
        base = {'source_sha256':'fixture-pin','render_closure':{str(i):'fixture' for i in range(43)}}
        def job(source='v404',encoded=13440):
            return {'metadata':{'source':source,'source_sha256':'fixture-pin','fps':60,'total':13440,'width':3840,'height':2160,'duration':224},
                    'render':{'encoded':encoded},'source_files':base['render_closure']}
        mapping = {files[0]:job('v401'),files[2]:job(encoded=540),files[3]:job()}
        directory = Mock(); directory.glob.return_value=files
        class Root:
            def __truediv__(self, other): return directory
        validator = Mock()
        with patch.dict(g,R=Root(),baseline=base,load=lambda p:mapping[p]),patch.dict(g['M'],read_job=validator,timeline=lambda r,f:(None,None,224)):
            self.assertEqual(worker['candidate']('film1'),files[3])
        validator.assert_called_once()

    def test_go_receipt_required_before_lock(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory(dir=C) as directory, patch.dict(g,C=Path(directory),options=SimpleNamespace(start_authorized=True)):
            with self.assertRaisesRegex(AssertionError,'GO receipt'):
                worker['main']()
        self.assertFalse(worker['LOCK'].exists())

    def test_changed_timeline_rejected(self):
        with patch.dict(g['M'],timeline=lambda r,f:(None,None,225)):
            with self.assertRaisesRegex(AssertionError,'duration changed'):
                worker['duration_contract']()

    def test_loop_contract_rejects_wrong_dimensions(self):
        files=[Path('loop_current.json')]
        base={'source_sha256':'fixture-pin','render_closure':{str(i):'fixture' for i in range(43)}}
        job={'metadata':{'source':'v404','source_sha256':'fixture-pin','fps':60,'total':960,
             'width':3840,'height':2160,'duration':16},'render':{'encoded':960},'source_files':base['render_closure']}
        directory=Mock(); directory.glob.return_value=files
        class Root:
            def __truediv__(self,other): return directory
        with patch.dict(g,R=Root(),baseline=base,load=lambda p:job):
            with self.assertRaisesRegex(AssertionError,'dimensions changed'):
                worker['candidate']('loop')

    def test_mutated_checkpoint_pin_is_rejected(self):
        item=worker['pin'](C/'media_v404_worker.py'); item['sha256']='0'*64
        with self.assertRaisesRegex(AssertionError,'Changed pin'): worker['verify'](item)

if __name__ == '__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(WorkerTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    report={'status':'PASS' if result.wasSuccessful() else 'FAIL','tests':result.testsRun,
            'failures':len(result.failures),'errors':len(result.errors),
            'scope':'Offline fixtures and actual helper argument contract; subprocesses mocked. No encode or decode run.',
            'worker':worker['pin'](C/'media_v404_worker.py'),'test':worker['pin'](Path(__file__)),'helper':worker['pin'](g['R']/'cinema/media_v7.py')}
    worker['save_original'](C/'MEDIA_WORKER_TESTS.json',report)
    raise SystemExit(0 if result.wasSuccessful() else 1)
