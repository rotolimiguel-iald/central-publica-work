"""ADENDO E audio: immutable v401 baseline and offline v402 plan comparison."""
from pathlib import Path
import contextlib, datetime, importlib.util, io, json, os, re, runpy, subprocess, sys, time, wave

C = Path(__file__).resolve().parent
W = C.parent
spec = importlib.util.spec_from_file_location('audio_v401_tools', W/'adendo_a/rebind_audio_v400.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
V = old.R
ACTOR = 'codex-video-audio'
TASK = 'V402_AUDIO'

def check():
    p = old.mission.call({'operation':'project','max_chars':190000})
    task = next(t for t in p['projection']['active'] if t['id']==TASK)
    assert task['lease']['owner']==ACTOR
    result = old.mission.call({'operation':'check','actor':{'id':ACTOR,'kind':'agent'},
        'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
        'task_id':TASK,'lease_id':task['lease']['id'],'max_chars':190000})
    assert result['ready']
    return result

def baseline():
    preflight = check()
    target = C/'baseline_audio_v401'
    receipt = target/'BASELINE.json'
    if receipt.exists():
        saved = old.read(receipt)
        for item in saved['files']:
            assert old.digest(item['backup']['path'])==item['original']['sha256']
        print(json.dumps({'status':'BASELINE_REUSED','files':len(saved['files'])}))
        return
    plan = old.read(V/'audio/NARRATION_PLAN_v401_final.json')
    assert plan['seal_version']=='v401'
    files = []
    for folder in [V/'audio',V/'subs']:
        files += [Path(str(p).removeprefix('\\\\?\\')) for p in old.ep(folder).rglob('*')
                  if p.is_file() and '.bak_' not in p.name and '__pycache__' not in p.parts]
    files += [V/f'data/film{i}_narration_timeline.json' for i in (1,2)]
    files += [V/'audit/DELIVERY_D.json',V/'audit/DELIVERY_D_V401.json']
    if old.read(V/'data/hud.json')['seal_version']=='v401':
        files += [V/f'data/{n}.json' for n in ('hud','film1','film2')]
    rows = []
    for src in sorted(set(files),key=str):
        dst = target/src.relative_to(V)
        data = old.ep(src).read_bytes()
        old.ep(dst.parent).mkdir(parents=True,exist_ok=True)
        if old.ep(dst).exists():
            assert old.ep(dst).read_bytes()==data
        else:
            temp = old.ep(dst.with_name(dst.name+'.tmp'))
            with temp.open('xb') as stream:
                stream.write(data);stream.flush();os.fsync(stream.fileno())
            assert old.digest(temp)==old.digest(src)
            os.rename(temp,old.ep(dst))
        assert old.digest(dst)==old.digest(src)
        rows.append({'original':old.pin(src),'backup':old.pin(dst)})
    old.write_new(receipt,{'status':'PASS_BYTES_PRESERVED','source':'v401','source_sha256':plan['seal_pin'],
        'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'preflight':preflight,'files':rows,'personal_voice_excluded':True})
    print(json.dumps({'status':'BASELINE_SAVED','files':len(rows),'bytes':sum(x['original']['bytes'] for x in rows),'receipt':old.pin(receipt)}))

def prepare(isolated=False):
    return revision.prepare(sys.modules[__name__],isolated)

def builder_module():
    spec=importlib.util.spec_from_file_location('audio_builder_current',old.BUILDER)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def execution_gate():
    return revision.execution_gate(sys.modules[__name__])

def synthesize():
    return revision.synthesize(sys.modules[__name__])


def mix():
    return revision.mix(sys.modules[__name__], '--timeline-write-authorized' in sys.argv)


def validate():
    preflight,data,plan,review,new=execution_gate()
    build=old.read(V/'audio/NARRATION_BUILD.json');progress=old.read(V/'audio/NARRATION_PROGRESS.json')
    assert build['status']=='COMPLETED' and not build['tts'] and not build['tts_inflight'] and not build['pending']
    assert build['plan_sha256']==progress['plan_sha256']==plan['plan_sha256']
    assert progress['cache_only'] and progress['completed']==progress['total_unique_units']==review['counts']['unique_units'] and not progress['pending']
    assert progress['authorization_sha256'] is None
    assert plan==old.read(V/'audio/NARRATION_PLAN_v402_formula_final.json')
    execution=old.read(C/'AUDIO_CACHE_ONLY_EXECUTION.json');assert not execution['tts_requested']
    transport=old.read(C/'AUDIO_TRANSPORT_VALIDATION.json')
    assert transport['status']=='PASS_NEW_UNITS_RECEIVED' and transport['completed_units']==len(new)
    for row in transport['units']:
        assert old.digest(row['transport']['path'])==row['transport']['sha256']
    for unit in execution['cache_bindings']:
        for key in ('audio','receipt'):assert old.digest(unit[key]['path'])==unit[key]['sha256']
        cache_receipt=old.read(unit['receipt']['path'])
        assert cache_receipt['state']=='completed' and cache_receipt['audio_sha256']==unit['audio']['sha256']
        assert cache_receipt['voice']==unit['voice'] and cache_receipt['text_sha256']==unit['text_sha256']
    preserved=[]
    baseline=old.read(C/'baseline_audio_v401/BASELINE.json')
    for row in baseline['files']:
        assert old.digest(row['backup']['path'])==row['original']['sha256']
        rel=Path(row['original']['path']).relative_to(V)
        if rel.parts[:2]==('audio','cache') and rel.suffix!='.wav':
            assert old.digest(row['original']['path'])==row['original']['sha256'];preserved.append(row['original'])
    media=[];timelines=[];subtitles=[]
    builder=builder_module()
    for film in ('film1','film2'):
        tp=V/f'data/{film}_narration_timeline.json';tl=old.read(tp)
        assert tl['status']==build['reports'][film]['status']=='AUDIO_MEASURED'
        assert tl['segments']==plan['films'][film]['segments'] and tl['plan_sha256']==plan['plan_sha256']
        assert tl['loudness']==build['reports'][film]['loudness']
        assert not tl['music'] and not tl['speedup'] and tl['voices']==plan['voices']
        for lang in ('en','pt-BR'):
            last=0
            for cue in tl['cues'][lang]:
                assert cue['start']>=last and cue['end']>cue['start'] and cue['end']<=tl['total_seconds']
                last=cue['end']
            measured=tl['loudness'][lang]
            for ext,h,m in [('wav',measured['sha256'],measured['after']),('m4a',measured['aac']['sha256'],measured['aac']['measurement'])]:
                path=V/f'audio/{film}/{lang}.{ext}';assert old.digest(path)==h
                assert abs(float(m['input_i'])+16)<=1 and float(m['input_tp'])<0
                media.append({**old.pin(path),'film':film,'language':lang,'lufs':float(m['input_i']),'true_peak_dbtp':float(m['input_tp'])})
            with wave.open(str(V/f'audio/{film}/{lang}.wav'),'rb') as wav:
                assert wav.getnframes()/wav.getframerate()==tl['total_seconds']==plan['films'][film]['total_seconds']
                assert wav.getframerate()==48000 and wav.getnchannels()==1
        subdir=V/'subs'/film.replace('film','filme')
        for lang in builder.LANGS:
            base=tl['cues']['pt-BR' if lang=='pt-BR' else 'en']
            variants=[(subdir/(lang+'.vtt'),base)]
            variants += [(subdir/('sync-'+voice)/(lang+'.vtt'),tl['cues'][voice]) for voice in ('en','pt-BR')]
            for path,cues in variants:
                expected=builder.vtt([{**cue,'text':cue['translations'][lang]} for cue in cues],lang)
                assert path.read_bytes()==expected
                subtitles.append({**old.pin(path),'language':lang,'cues':len(cues)})
        chapters=subdir/'chapters.vtt'
        assert chapters.read_bytes()==builder.vtt([{'start':s['start'],'end':s['end'],'text':s['title']['en']} for s in tl['segments']],'en')
        subtitles.append({**old.pin(chapters),'language':'en','cues':len(tl['segments'])})
        timelines.append(old.pin(tp))
    assert len(media)==8 and len(subtitles)==26
    new_attempts=[]
    for u in new:
        paths=[V/'audio/cache'/(u['key']+'.json')]
        paths+=list(old.ep(V/'audio/cache/bounded').rglob(u['key']+'.json'))
        for path in paths:
            if old.ep(path).exists():
                r=old.read(path);new_attempts.append({'key':u['key'],'state':r['state'],'receipt':old.pin(path),
                    'transport':old.pin(path.with_suffix('.transport.jsonl')) if old.ep(path.with_suffix('.transport.jsonl')).exists() else None})
    receipt={'schema':'iald.delivery-d.v402/v1','status':'PASS_BUILDER_READY_FOR_INDEPENDENT_REVIEW',
        'actor':ACTOR,'source':data['source'],'source_sha256':data['source_sha256'],
        'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'preflight':preflight,
        'plan_current':True,'plan_sha256':plan['plan_sha256'],'plan':old.pin(V/'audio/NARRATION_PLAN_v402_formula_final.json'),
        'builder':old.pin(old.BUILDER),'helper':old.pin(Path(__file__)),'templates':old.pin(V/'audio/script_templates.json'),
        'source_files':data['source_files'],'data_ready':old.pin(C/'DATA_READY.json'),
        'parent_numeric_review':revision.optional_pin(sys.modules[__name__],C/'PARENT_NUMERIC_REVIEW.json'),'parent_payload_review':revision.optional_pin(sys.modules[__name__],C/'PARENT_AUDIO_PLAN_REVIEW.json'),
        'human_authorizations_private':[old.pin(W/'EDGE_RETRY_HUMAN_APPROVAL.json'),old.pin(W/'EDGE_BOUNDED_RETRY_APPROVAL.json')],
        'counts':{**{k:review['counts'][k] for k in ('unique_units','cue_occurrences','reused_v401_units','new_v402_units')},'subtitle_files':26,'wav_aac_files':8},
        'new_synthesis_attempts':new_attempts,'cache_bindings':execution['cache_bindings'],
        'transport_validation':old.pin(C/'AUDIO_TRANSPORT_VALIDATION.json'),
        'synthesis_summary':{k:transport[k] for k in ('speech_requests','completed_units','retry_attempts','new_uncertain_units')},
        'build':old.pin(V/'audio/NARRATION_BUILD.json'),'progress':old.pin(V/'audio/NARRATION_PROGRESS.json'),
        'cache_only_execution':old.pin(C/'AUDIO_CACHE_ONLY_EXECUTION.json'),
        'baseline':old.pin(C/'baseline_audio_v401/BASELINE.json'),'old_cache_evidence_preserved':len(preserved),
        'media':media,'subtitles':subtitles,'timelines':timelines,'music':False,'speedup':False,
        'formula_parent_review':old.pin(C/'FORMULA_NARRATION_PARENT_REVIEW.json'),
        'formula_review':old.pin(C/'FORMULA_NARRATION_REVIEW.json'),
        'scope':'Real Microsoft Edge EN/PT speech, measured mixes and four subtitle languages. Parent payload review is not human consent; original human authorizations remain separate.',
        'limitations':['No perceptual audition in this mode.','No personal voice used.','No new scientific proof or unrestricted physical conclusion.','Final integration and acceptance belong to an independent reviewer.'],
        'private_receipt_do_not_publish':True}
    revision.seal_guard(sys.modules[__name__])
    receipt['version_guard']=revision.seal_guard(sys.modules[__name__])
    receipt['revision_helper']=old.pin(C/'audio_v402_formula_runtime.py')
    target=V/'audit/DELIVERY_D_V402.json';old.write_new(target,receipt)
    old.write_new(C/'DELIVERY_AUDIO.json',receipt)
    old.write_new(C/'AUDIO_READY.json',{'status':'AUDIO_READY','actor':ACTOR,'source':data['source'],
        'source_sha256':data['source_sha256'],'plan_sha256':plan['plan_sha256'],'receipt':old.pin(target),
        'counts':receipt['counts'],'media':media,'subtitles':subtitles,'timelines':timelines,
        'perceptual_audition':False,'acceptance':'BUILDER_CANDIDATE_ONLY'})
    print(json.dumps({'status':'AUDIO_READY','receipt':old.pin(target),'media':media,'attempt_states':[x['state'] for x in new_attempts]}),flush=True)

def submit():
    preflight=check();ready=old.read(C/'AUDIO_READY.json')
    assert old.digest(ready['receipt']['path'])==ready['receipt']['sha256']
    p=old.mission.call({'operation':'project','max_chars':190000})
    result=old.mission.call({'operation':'submit','actor':{'id':ACTOR,'kind':'agent'},
        'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
        'task_id':TASK,'lease_id':preflight['lease_id'],'event_id':'ordem022-adendo-e-v402-audio-submit',
        'evidence':[{'path':e['path'],'sha256':e['sha256']} for e in [old.pin(C/'AUDIO_READY.json'),old.pin(V/'audit/DELIVERY_D_V402.json')]]})
    old.write_new(C/'AUDIO_SUBMIT.json',result)
    print(json.dumps(result),flush=True)

import audio_v402_formula_runtime as revision

if __name__=='__main__':
    actions={'check':execution_gate,'synthesize':synthesize,
             'transport':lambda:revision.transport(sys.modules[__name__]),
             'timing':lambda:revision.timing(sys.modules[__name__]),
             'mix':mix,'validate':validate,'submit':submit}
    assert sys.argv[1] in actions,'UNKNOWN_FORMULA_ACTION'
    result=actions[sys.argv[1]]()
    if sys.argv[1]=='check':
        print(json.dumps({'status':'EXACT_FORMULA_PLAN_REVIEWED','revision':result[0]['receipt']['revision'],
                         'lease_id':result[0]['lease_id'],'plan_sha256':result[2]['plan_sha256'],
                         'counts':result[3]['counts']}),flush=True)
