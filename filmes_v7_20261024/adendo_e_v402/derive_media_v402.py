"""Derive a new worker from v401 without modifying any historical helper."""
from pathlib import Path
import ast, json, os, runpy, time

E = Path(__file__).resolve().parent
OLD = E.parent/'adendo_c_v401'


def write_new(name, text):
    path = E/name
    if name.endswith('.py'): ast.parse(text)
    raw = text.encode('utf-8')
    if path.exists():
        previous = path.read_bytes()
        if previous == raw: return
        assert not (E/'MEDIA_START.json').exists() and not (E/'MEDIA_V402_BASELINE.json').exists(), 'Frozen worker may not be changed'
        bak = path.with_name(path.name+'.bak_'+str(time.time_ns()))
        with bak.open('xb') as f: f.write(previous)
        assert bak.read_bytes() == previous
    tmp = path.with_suffix(path.suffix+'.tmp')
    with tmp.open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes() == raw
    os.replace(tmp,path)


def main():
    source = (OLD/'media_v401_worker.py').read_text(encoding='utf-8')
    text = source.replace('ADENDO C worker','ADENDO E worker').replace('V401','V402').replace('v401','v402')
    for a,b in [('MEDIA_V400_BACKUP','MEDIA_V401_BACKUP'),('baseline_manifest_v400','baseline_manifest_v401'),
                ('media_v400_history','media_v401_history')]: text = text.replace(a,b)
    def replace(old,new):
        nonlocal text
        assert text.count(old) == 1, old[:90]
        text = text.replace(old,new)
    replace('baseline = None\naudio_binding', 'baseline = None\nprior_elapsed = 0.0\naudio_binding')
    replace("'elapsed_seconds':time.monotonic()-started", "'elapsed_seconds':prior_elapsed+time.monotonic()-started")
    replace('def initialize():', '''def duration_contract():
    for film, expected in ((1,224),(2,360)):
        _, _, actual = M['timeline'](R,film)
        assert actual == expected, 'STOP: film duration changed'


def verify_intent(intent):
    assert intent['status'] == 'INTENT_BEFORE_SINGLE_BROWSER_PIPELINE'
    for key, expected in (('data_ready',options.data_ready),('audio_ready',options.audio_ready),
                          ('numeric_review',C/'PARENT_NUMERIC_REVIEW.json'),('media_prepared',C/'MEDIA_PREPARED.json')):
        verify(intent[key])
        assert Path(intent[key].get('path',intent[key].get('file'))).resolve() == expected.resolve()


def launch_guard():
    assert options.start_authorized, 'Await explicit coordinator signal; --start-authorized required'
    path = C/'MEDIA_GO.json'
    assert path.exists(), 'Await explicit coordinator GO receipt'
    go = load(path); capture = canonical_guard()
    assert go['status'] == 'GO' and go['actor'] in (ACTOR,'codex-video-v7')
    assert go['authorization'] == 'explicit_parent_go' and go['authorization_text'].strip()
    assert go['source'] == VERSION and go['source_sha256'] == capture['source_sha256']
    for key, expected in (('worker',Path(__file__)),('render_intent',C/'RENDER_INTENT.json'),
                          ('data_ready',options.data_ready),('audio_ready',options.audio_ready)):
        verify(go[key]); assert Path(go[key].get('path',go[key].get('file'))).resolve() == expected.resolve()
    tests = load(C/'MEDIA_WORKER_TESTS.json')
    assert tests['status'] == 'PASS' and tests['worker'] == pin(Path(__file__))
    assert tests['helper'] == pin(R/'cinema/media_v7.py')
    contract_tests = load(C/'MEDIA_READY_CONTRACT_TESTS.json')
    assert contract_tests['status'] == 'PASS' and contract_tests['worker'] == pin(Path(__file__))
    intent = load(C/'RENDER_INTENT.json')
    verify_intent(intent)
    assert intent['source'] == VERSION and intent['source_sha256'] == capture['source_sha256']
    assert intent['render_closure'] == collect(R), 'STOP: GO dependency freeze changed'
    assert readiness() is not None, 'Approved DATA_READY and parent numeric review required'
    duration_contract()
    return pin(path)


def initialize():''')
    replace('global baseline, audio_binding, done, prepared, assets, timings, completed_outputs',
            'global baseline, audio_binding, done, prepared, assets, timings, completed_outputs, prior_elapsed')
    replace("        previous = load(STATE)", """        previous = load(STATE)
        prior_elapsed = previous.get('elapsed_seconds',0)
        archived = C/('MEDIA_WATCH_BEFORE_RESUME_'+str(time.time_ns())+'.json')
        M['atomic'](archived,STATE.read_bytes())
        assert sha(archived) == sha(STATE)""")
    replace("'previous_state':pin(STATE)", "'previous_state':pin(archived)")
    replace("    closure = collect(R)\n", "    duration_contract()\n    closure = collect(R)\n")
    replace("    frozen.append(pin(C/'RENDER_INTENT.json'))", "    frozen += [pin(C/'RENDER_INTENT.json'),pin(C/'MEDIA_GO.json')]" )
    replace("    assert intent['data_ready_sha256'] == sha(options.data_ready)", "    verify_intent(intent)")
    replace("    if audio_binding:\n", "    duration_contract()\n    if audio_binding:\n")
    replace("    verify(ready['receipt'])", """    verify(ready['receipt'])
    delivery_path = Path(ready['receipt'].get('path',ready['receipt'].get('file')))
    assert delivery_path.resolve() == (R/'audit/DELIVERY_D_V402.json').resolve()
    delivery = load(delivery_path)
    assert delivery['source'] == VERSION and delivery['source_sha256'] == baseline['source_sha256']
    assert delivery['status'] == 'PASS_BUILDER_READY_FOR_INDEPENDENT_REVIEW'""")
    replace("        M['read_job'](R,path,None if kind == 'loop' else int(kind[-1]))", """        expected = 16 if kind == 'loop' else M['timeline'](R,int(kind[-1]))[2]
        size = (1920,1080) if kind == 'loop' else (3840,2160)
        assert (metadata['width'],metadata['height']) == size, 'STOP: job dimensions changed'
        assert metadata['total'] == expected*60 and metadata['duration'] == expected, 'STOP: duration/frame count changed'
        M['read_job'](R,path,None if kind == 'loop' else int(kind[-1]))""")
    replace("    save(C/'DELIVERY_E.json',", "    assert not (C/'DELIVERY_E.json').exists(), 'Original E receipt is immutable'\n    save(C/'DELIVERY_E.json',")
    replace("    assert options.start_authorized, 'Await explicit coordinator signal; --start-authorized required'\n    fd =", "    launch_guard()\n    fd =")
    replace("        initialize()\n        G['jsave']", """        initialize()
        if (C/'DELIVERY_E.json').exists():
            # Reconcile terminal state, never rewrite the original delivery.
            existing = load(C/'DELIVERY_E.json')
            verify(existing['validation']); verify(existing['render_manifest'])
            assert len(done) == 3 and assets and 'validation' in completed_outputs
            state('COMPLETE'); return
        assert audio_ready(), 'Current reviewed AUDIO_READY required before exports'
        G['jsave']""")
    replace("        assert 'seal_version' in text and 'seal_pin' in text", "        assert 'seal_version' in text and 'seal_pin' in text\n        assert 'v401' not in text.lower()")
    replace("{'metadata':{'source':'v400','source_sha256':'fixture-current'}}", "{'metadata':{'source':'v401','source_sha256':'fixture-current'}}")
    write_new('media_v402_worker.py',text)
    test = (OLD/'test_media_v401_worker.py').read_text(encoding='utf-8').replace('v401','v402').replace("job('v400')","job('v401')")
    test = test.replace("'fps':60,'total':13440", "'fps':60,'total':13440,'width':3840,'height':2160,'duration':224")
    test = test.replace("patch.dict(g['M'],read_job=validator)", "patch.dict(g['M'],read_job=validator,timeline=lambda r,f:(None,None,224))")
    test = test.replace("'test':worker['pin'](Path(__file__))", "'test':worker['pin'](Path(__file__)),'helper':worker['pin'](g['R']/'cinema/media_v7.py')")
    # Add checks that exercise the new contract before any side effect.
    insertion = '''    def test_go_receipt_required_before_lock(self):
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
        job={'metadata':{'source':'v402','source_sha256':'fixture-pin','fps':60,'total':960,
             'width':3840,'height':2160,'duration':16},'render':{'encoded':960},'source_files':base['render_closure']}
        directory=Mock(); directory.glob.return_value=files
        class Root:
            def __truediv__(self,other): return directory
        with patch.dict(g,R=Root(),baseline=base,load=lambda p:job):
            with self.assertRaisesRegex(AssertionError,'dimensions changed'):
                worker['candidate']('loop')

'''
    test = test.replace('    def test_mutated_checkpoint_pin_is_rejected', insertion+'    def test_mutated_checkpoint_pin_is_rejected')
    write_new('test_media_v402_worker.py',test)
    launcher = (OLD/'start_media_v401.py').read_text(encoding='utf-8').replace('v401','v402').replace('20261025','20261027')
    launcher = launcher.replace("    preflight=m['preflight']()", """    from types import SimpleNamespace
    m['main'].__globals__['options']=SimpleNamespace(start_authorized=True,data_ready=C/'DATA_READY.json',audio_ready=C/'AUDIO_READY.json',audio_dir=m['R']/'audio')
    go=m['launch_guard']()
    preflight=m['preflight']()""")
    launcher = launcher.replace('MEDIA_SCHEMA_FIX_TESTS.json','MEDIA_WORKER_TESTS.json')
    launcher = launcher.replace("'preflight':preflight,'source'", "'go':go,'preflight':preflight,'source'")
    write_new('start_media_v402.py',launcher)
    # Final binding stays separate from the original E receipt; parent owns make/link.
    binding = (OLD/'bind_final_media_v401.py').read_text(encoding='utf-8').replace('v401','v402').replace('V401','V402')
    binding = binding.replace('MEDIA_V400_BACKUP','MEDIA_V401_BACKUP')
    binding = binding.replace("'MEDIA_SCHEMA_FIX.json','MEDIA_SCHEMA_FIX_TESTS.json','MEDIA_LIVENESS_R1.json',", "'MEDIA_PREPARED.json','MEDIA_WORKER_TESTS.json','MEDIA_READY_CONTRACT_TESTS.json',")
    write_new('bind_final_media_v402.py',binding)
    m=runpy.run_path(str(E/'media_v402_worker.py')); pin=m['pin']
    report={'status':'DERIVED_NOT_STARTED','source':'v402','predecessor':'v401',
        'inputs':[pin(OLD/name) for name in ('media_v401_worker.py','start_media_v401.py','test_media_v401_worker.py','bind_final_media_v401.py')],
        'outputs':[pin(E/name) for name in ('media_v402_worker.py','start_media_v402.py','test_media_v402_worker.py','bind_final_media_v402.py')],
        'namespace_action_repair_preserved':True,'history_unchanged':True,'renderer_or_worker_started':False}
    write_new('MEDIA_DERIVATION.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n')


if __name__ == '__main__': main()
