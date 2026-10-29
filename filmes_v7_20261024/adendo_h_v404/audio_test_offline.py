"""Scope and reuse tests; no TTS/mix entry point is called."""
import copy, json, socket, subprocess, sys, tempfile
from pathlib import Path
sys.dont_write_bytecode=True
import audio_pipeline as p

results=[]
def test(name,fn):
    fn();results.append({'name':name,'status':'PASS'})
def denied(fn):
    try:fn()
    except (ValueError,FileNotFoundError):return
    raise AssertionError('EXPECTED_REFUSAL')

def main():
    b=p.builder();g=p.read(p.G/'AUDIO_SCOPE_CHECK.json')
    fixture=copy.deepcopy(p.read(p.B/'audio/NARRATION_PLAN_v402_formula_final.json'))
    for r in g['changes']:
        s=next(s for s in fixture['films'][r['film']]['segments'] if s['key']==r['segment'])
        s['cues'][r['cue_index']][r['language']]=r['after']
    test('exact_G_H_fixture_58_units_6_new',lambda:p.payload_guard(b,fixture,g))
    for field,value in [('voices',{'en':'unapproved'}),('rate','+1%'),('format','PCM')]:
        bad=copy.deepcopy(fixture);bad[field]=value
        test('refuse_'+field,lambda bad=bad:denied(lambda:p.payload_guard(b,bad,g)))
    bad=copy.deepcopy(fixture);bad['films']['film1']['segments'][0]['cues'][0]['en']+=' Extra.'
    test('seventh_unit_refused',lambda:denied(lambda:p.payload_guard(b,bad,g)))
    bad=copy.deepcopy(fixture);bad['films']['film1']['segments'][0]['cues'][0]['fr']+=' Texte.'
    test('subtitle_only_mutation_refused',lambda:denied(lambda:p.payload_guard(b,bad,g)))
    bad=copy.deepcopy(fixture);bad['films']['film1']['segments'][0]['duration']+=1
    test('timeline_mutation_refused',lambda:denied(lambda:p.payload_guard(b,bad,g)))
    bad=copy.deepcopy(g);bad['all_units'][0]['key']='0'*64
    test('altered_cache_key_refused',lambda:denied(lambda:p.payload_guard(b,fixture,bad)))
    test('52_reuses_match_original_bytes_and_payloads',lambda:p.cache_guard(b,g))
    test('template_has_no_literal_numbers',lambda:b.validate_templates(p.read(p.S/'audio/script_templates.json')))
    original=p.read(p.B/'audio/script_templates.json');current=p.read(p.S/'audio/script_templates.json')
    a=next(s for s in original['films']['film1']['segments'] if s['key']=='return')
    z=next(s for s in current['films']['film1']['segments'] if s['key']=='return')
    test('return_template_unchanged_dynamic_count',lambda:p.require(a==z,'RETURN_TEMPLATE_CHANGED'))
    test('writes_production_denied',lambda:denied(lambda:p.put_bytes(p.V/'audio/TEST.json',b'{}')))
    test('writes_shared_hud_denied',lambda:denied(lambda:p.put_bytes(p.S/'data/hud.json',b'{}')))
    test('engine_writes_production_denied',lambda:denied(lambda:b.atomic(p.V/'audio/TEST.json',b'{}')))
    with p.offline():
        test('offline_socket_denied',lambda:denied(lambda:socket.create_connection(('example.invalid',443))))
        test('offline_node_speech_denied',lambda:denied(lambda:subprocess.run([str(p.NODE),'-e',b.EDGE_JS])))
    test('bounded_authorization_exact_two',lambda:p.require(b.load_bounded_authorization(p.ctx.W/'EDGE_BOUNDED_RETRY_APPROVAL.json')['limit']==2,'RETRY_LIMIT'))
    # Simulate the transport entirely in Python: inspect the durable intent at
    # the moment the child would start, and return synthetic bytes (not speech).
    p.H.joinpath('audio_timing_measurements').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=p.H/'audio_timing_measurements') as td:
        cache=Path(td);u=g['additional_new_units'][0];original_run=b.subprocess.run
        calls=[]
        def fake_run(args,**kw):
            r=p.read(cache/(u['key']+'.json'))
            p.require(r['state']=='intent' and r['text_sha256']==u['text_sha256'],'INTENT_MISSING_BEFORE_TRANSPORT')
            payload=json.loads(kw['input']);p.require(payload['text']==u['text'] and payload['voice']==u['voice'],'PAYLOAD_CHANGED')
            calls.append(payload)
            return subprocess.CompletedProcess(args,0,b'SYNTHETIC_OFFLINE_BYTES',b'')
        b.subprocess.run=fake_run
        try:
            test('intent_durable_before_simulated_child',lambda:b.cached_tts(cache,u['voice'],u['text'],'offline-fixture',Path(td),str(p.NODE)))
            test('completed_cache_does_not_send_twice',lambda:b.cached_tts(cache,u['voice'],u['text'],'offline-fixture',Path(td),str(p.NODE)))
            test('one_simulated_call_only',lambda:p.require(len(calls)==1,'DUPLICATE_CALL'))
        finally:b.subprocess.run=original_run
    with tempfile.TemporaryDirectory(dir=p.H/'audio_timing_measurements') as td:
        cache=Path(td);u=g['additional_new_units'][0];calls=[];cached=b.cached_tts
        auth=b.load_bounded_authorization(p.ctx.W/'EDGE_BOUNDED_RETRY_APPROVAL.json')
        def failed(cache,voice,text,approval,modules,node,**kw):
            key=b.cache_key(voice,text);row={'key':key,'state':'uncertain','voice':voice,'text_sha256':b.sha(text.encode())}
            if kw.get('attempt_metadata') is not None:row['bounded_attempt']=kw['attempt_metadata']
            b.exclusive(cache/(key+'.json'),row);calls.append(key)
            raise ValueError('SIMULATED_FAILURE_NO_NETWORK')
        b.cached_tts=failed
        try:
            test('bounded_stops_after_initial_plus_two',lambda:denied(lambda:b.bounded_tts(cache,u['voice'],u['text'],'fixture',Path(td),str(p.NODE),auth)))
            test('bounded_three_distinct_attempts',lambda:p.require(len(calls)==3,'RETRY_COUNT'))
            test('bounded_exhausted_slots_not_reopened',lambda:denied(lambda:b.bounded_tts(cache,u['voice'],u['text'],'fixture',Path(td),str(p.NODE),auth)))
            test('bounded_no_fourth_call',lambda:p.require(len(calls)==3,'FOURTH_CALL'))
        finally:b.cached_tts=cached
    test('decode_wavs_separate_from_cache',lambda:p.require(b'wav = mp3.with_suffix(".wav")' not in (p.S/'audio/build_narration.py').read_bytes(),'HISTORICAL_WAV_OVERWRITE'))
    # This is a source fixture, not a v404 plan generated from DATA.
    report={'status':'PASS_OFFLINE_SCOPE_AND_REUSE','actor':p.ACTOR,'tests':results,'count':len(results),
        'real_tts_calls':0,'mix_executed':False,'fixture':'G/H authorized text applied to v402 plan in memory only',
        'limits':['No provider call, listening test or duration claim.','DATA/plan release is a separate runtime gate.']}
    p.put(p.H/'AUDIO_OFFLINE_TESTS_R2.json',report)
    print(json.dumps({'status':report['status'],'tests':len(results),'real_tts_calls':0}))

if __name__=='__main__':main()
