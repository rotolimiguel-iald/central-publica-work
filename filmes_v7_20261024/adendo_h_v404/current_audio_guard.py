"""Read-only binding of the independently reviewed six-unit audio result."""
from pathlib import Path
import importlib.util,json,wave,math
from finalizer_guards import read,sha,verify_pin,narration_units

def validate_audio(c,v,source):
 r=read(c/'AUDIO_RESULT_REVIEW.json');assert r['status']=='PASS_WITH_SCOPE' and r['actor']=='codex-video-v404-data'
 ready=read(c/'MEDIA_AUDIO_READY.json');d=read(verify_pin(ready['receipt'],v/'audit/DELIVERY_D_V404.json'))
 assert ready['source']==d['source']=='v404' and ready['source_sha256']==d['source_sha256']==source
 assert ready['status']=='AUDIO_READY' and d['status']=='PASS_BUILDER_READY_FOR_INDEPENDENT_REVIEW'
 verify_pin(d['candidate_receipt']);verify_pin(d['integration'],c/'INTEGRATION.json')
 for row in d['media']+d['subtitles']:verify_pin(row)
 assert len(d['media'])==8 and len(d['subtitles'])==26
 plan=read(v/'audio/NARRATION_PLAN_v404.json');assert plan['seal_version']=='v404' and plan['seal_pin']==source
 assert plan['plan_sha256']==ready['plan_sha256']==d['plan_sha256']
 units=narration_units(plan);prepared=read(c/'AUDIO_PLAN.json')
 assert len(units)==58 and sum(len(u['occurrences']) for u in units.values())==76
 assert len(prepared['new_units'])==6 and prepared['reused_units']==52
 assert set(units)=={u['key'] for u in prepared['units']}
 build=read(v/'audio/NARRATION_BUILD.json');assert build['status']=='COMPLETED' and not build['pending'] and not build['tts_inflight'] and not build['tts'] and build['plan_sha256']==plan['plan_sha256']
 spec=importlib.util.spec_from_file_location('v404_narration_guard',v/'audio/build_narration.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
 assert b.make_plan(v,v/'audio/script_templates.json')==plan
 for name,film in plan['films'].items():
  tl=read(v/f'data/{name}_narration_timeline.json');assert tl['status']=='AUDIO_MEASURED' and not tl['speedup'] and not tl['music'] and tl['plan_sha256']==plan['plan_sha256']
  assert tl['segments']==film['segments'] and tl['loudness']==build['reports'][name]['loudness']
  for lang in plan['voices']:
   levels=tl['loudness'][lang]
   assert sha(v/f'audio/{name}/{lang}.wav')==levels['sha256'] and sha(v/f'audio/{name}/{lang}.m4a')==levels['aac']['sha256']
   for measure in [levels['after'],levels['aac']['measurement']]:
    i=float(measure['input_i']);tp=float(measure['input_tp']);assert math.isfinite(i) and abs(i+16)<=1 and math.isfinite(tp) and tp<0
   with wave.open(str(v/f'audio/{name}/{lang}.wav'),'rb') as w:assert w.getframerate()==48000 and w.getnchannels()==1 and w.getnframes()/48000==film['total_seconds']
  for lang in b.LANGS:
   paths=[(v/'subs'/name.replace('film','filme')/(lang+'.vtt'),tl['cues']['pt-BR' if lang=='pt-BR' else 'en'])]
   paths += [(v/'subs'/name.replace('film','filme')/('sync-'+voice)/(lang+'.vtt'),tl['cues'][voice]) for voice in plan['voices']]
   for path,cues in paths:assert path.read_bytes()==b.vtt([{**cue,'text':cue['translations'][lang]} for cue in cues],lang)
 return d
