"""CPU/read-only production probes and in-memory negative controls; no finalizer call."""
from pathlib import Path
from unittest.mock import patch
import copy
import datetime
import hashlib
import json
import tempfile
import sys
import finalizer_guards as g
from coverage_validation import validate_samples

C = Path(__file__).resolve().parent
V = Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/video_um/delivery_v7')
N = V.parent.parent / 'Nós'
results = []


def test(name, callback, rejected=False):
    try:
        callback()
    except (AssertionError, KeyError, ValueError, FileNotFoundError) as exc:
        assert rejected, (name, type(exc).__name__, str(exc))
        results.append({'name':name, 'passed':True, 'expected':'reject', 'observed':type(exc).__name__, 'detail':str(exc)[:220]})
    else:
        assert not rejected, 'Unexpected acceptance: ' + name
        results.append({'name':name, 'passed':True, 'expected':'accept', 'observed':'accepted'})


def altered_read(path, mutate, callback):
    original = g.read
    def read(p):
        value = original(p)
        if Path(p).resolve() == Path(path).resolve(): mutate(value)
        return value
    with patch.object(g, 'read', read): callback()


def main():
    source = g.read(C/'SOURCE_CAPTURE.json')['source_sha256']
    frozen = [C/name for name in ['DATA_READY.json','NUMERIC_COMPARISON.json','PARENT_NUMERIC_REVIEW.json','SOURCE_CAPTURE.json','DELIVERY_DATA.json']]
    ready = g.read(C/'DATA_READY.json')
    frozen += [Path(x['path']) for x in ready['data_files']+ready['source_files']]
    frozen += [V/x for x in g.read(V/'replay/DELIVERY_C.json')['public_files']]
    frozen += [V/'replay'/x for x in ['DELIVERY_C.json','DELIVERY_ADENDO_E_V402.json','TEST_BROWSER.json','TEST_OFFLINE.json']]
    before = {str(p):g.sha(p) for p in frozen}
    test('frozen_data_actual_v402', lambda:g.validate_frozen_data(C,V,N))
    test('replay_actual_13_offline_61_browser', lambda:g.validate_replay(V,source))
    test('audio_actual_v402_schema_counts_and_pins', lambda:g.validate_audio(C,V,source))
    original_sha = g.sha
    with patch.object(g,'sha',lambda p:'0'*64 if Path(p).resolve()==(N/'um_absoluto_selo.json').resolve() else original_sha(p)):
        test('changed_current_seal_same_version_rejected',lambda:g.validate_frozen_data(C,V,N),True)
    with patch.object(g,'sha',lambda p:'0'*64 if Path(p).resolve()==(V/'data/hud.json').resolve() else original_sha(p)):
        test('changed_hud_bytes_after_ready_rejected',lambda:g.validate_frozen_data(C,V,N),True)
    test('replay_stale_manifest_rejected',lambda:altered_read(V/'replay/TEST_BROWSER.json',lambda d:d.__setitem__('manifest_sha256','0'*64),lambda:g.validate_replay(V,source)),True)
    test('replay_empty_rows_rejected',lambda:altered_read(V/'replay/TEST_BROWSER.json',lambda d:d['result'].__setitem__('rows',[]),lambda:g.validate_replay(V,source)),True)
    test('replay_missing_tamper_control_rejected',lambda:altered_read(V/'replay/TEST_BROWSER.json',lambda d:d.__setitem__('checks',[r for r in d['checks'] if r['name']!='excerpt_tamper_visible']),lambda:g.validate_replay(V,source)),True)
    test('offline_error_rejected',lambda:altered_read(V/'replay/TEST_OFFLINE.json',lambda d:d.__setitem__('errors',1),lambda:g.validate_replay(V,source)),True)
    test('audio_pending_rejected',lambda:altered_read(C/'AUDIO_READY.json',lambda d:d.__setitem__('status','PENDING'),lambda:g.validate_audio(C,V,source)),True)
    for field in ['new_v402_units','reused_v401_units','subtitle_files','wav_aac_files']:
        original = g.read
        def read(p, field=field):
            d=original(p)
            if Path(p).resolve() in {(C/'AUDIO_READY.json').resolve(),(V/'audit/DELIVERY_D_V402.json').resolve()}:
                d['counts'][field]+=1
            return d
        with patch.object(g,'read',read):test('wrong_'+field+'_rejected',lambda:g.validate_audio(C,V,source),True)
    manifest=g.read(V/'PUBLIC_DELIVERY_V7.json');pointer=g.read(V.parent/'PUBLIC_DELIVERY_V7.json')
    test('existing_public_pointer_schema_only',lambda:g.validate_public_pointer(manifest,pointer,V))
    mismatched=copy.deepcopy(pointer);mismatched['public_files'].append({'path':'delivery_v7/render/voice_test_pt.mp4','sha256':'0'*64,'bytes':1})
    test('root_pointer_extra_voice_entry_rejected',lambda:g.validate_public_pointer(manifest,mismatched,V),True)
    mismatched=copy.deepcopy(pointer);mismatched['public_files'][0]['sha256']='0'*64
    test('root_pointer_old_pin_rejected',lambda:g.validate_public_pointer(manifest,mismatched,V),True)
    historical=g.read(V/'render/MEDIA_VALIDATION.json')
    # This existing receipt is still v401 while the v402 captures are running.
    if historical['source']!='v402':test('real_historical_media_PASS_rejected',lambda:g.require_current(historical,source,{'PASS'}),True)
    with tempfile.TemporaryDirectory(prefix='finalizer_control_',dir=C) as folder:
        f=Path(folder)/'artifact.txt';f.write_bytes(b'original')
        entry={'path':str(f),'sha256':g.sha(f),'bytes':f.stat().st_size}
        test('pin_positive_fixture',lambda:g.verify_pin(entry,f))
        f.write_bytes(b'changed!')
        test('pin_same_size_tamper_rejected',lambda:g.verify_pin(entry,f),True)
    render=g.read(V/'RENDER_MANIFEST.json');coverage=[]
    for kind,job in render['jobs'].items():
        timeline=g.read(V/f"data/film{job['metadata']['film']}.json")
        duration=timeline['total_seconds'] if job['metadata']['film']==1 else timeline['duration']
        test('coverage_recorded_'+kind,lambda k=kind,j=job,d=duration:coverage.append({'kind':k,**validate_samples(k,j['metadata'],j['render']['samples'],d)}))
    job=render['jobs']['film1'];rows=job['render']['samples'];meta=job['metadata'];duration=224
    for label,mutate in [
        ('duplicate_timestamp',lambda r:r[3].__setitem__('time',r[2]['time'])),
        ('transition_interior',lambda r:r[3].__setitem__('transition',True)),
        ('nan_width',lambda r:r[3].__setitem__('width_fraction',float('nan'))),
        ('low_width',lambda r:r[3].__setitem__('width_fraction',.59)),
        ('missing_sample',lambda r:r.pop())]:
        changed=copy.deepcopy(rows);mutate(changed)
        test('coverage_'+label+'_rejected',lambda r=changed:validate_samples('film1',meta,r,duration),True)
    job=render['jobs']['loop'];changed=copy.deepcopy(job['render']['samples'])
    for i,row in enumerate(changed):row['time']=i
    test('loop_incorrect_0_to_15_grid_rejected',lambda:validate_samples('loop',job['metadata'],changed,224),True)
    for name in ['finalizer_guards.py','finalize_make.py','finish_v402.py','parent_numeric_review.py','coverage_validation.py']:
        test('syntax_'+name,lambda n=name:compile((C/n).read_bytes(),str(C/n),'exec'))
    assert before=={str(p):g.sha(p) for p in frozen},'Frozen bytes changed during review'
    report={'status':'PASS','source':'v402','source_sha256':source,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'tests':len(results),'results':results,'frozen_files_unchanged':len(before),'frozen_pins':before,
            'coverage_fixture_source':render['source'],'coverage_fixture_manifest_sha256':g.sha(V/'RENDER_MANIFEST.json'),
            'coverage':coverage,'scope':'Only read-only guards and pure coverage validators executed. Finalizers/main, render, browser, TTS and full pipeline were not executed. Negative fixtures are in-memory or in a private temporary C directory. Coverage validates recorded masks, not video pixels.'}
    path=C/'FINALIZER_CONTROLS.json';assert not path.exists()
    raw=(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode();tmp=path.with_suffix('.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(path)
    print(json.dumps({'status':'PASS','tests':len(results),'frozen_files_unchanged':len(before),'coverage_fixture_source':render['source']}))


if __name__=='__main__':main()
