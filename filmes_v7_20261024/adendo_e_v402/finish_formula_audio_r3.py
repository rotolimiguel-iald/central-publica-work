"""Local PCM listening excerpts and private current receipt pointer after measured mixes."""
from pathlib import Path
import datetime, json, os, sys, time, wave
import execute_formula_audio_r3 as c
import audio_v402_formula_runtime as runtime


def previews():
    pre,data,plan,review,new=c.execution_gate()
    ready=c.old.read(c.C/'AUDIO_READY.json');delivery=c.old.read(ready['receipt']['path'])
    runtime.verify_pin(c,ready['receipt'])
    assert delivery['plan_sha256']==plan['plan_sha256'] and delivery['plan_current']
    segments=plan['films']['film1']['segments']
    first=next(s for s in segments if s['key']=='boundary')
    last=next(s for s in segments if s['key']=='mirror')
    start,end=first['start'],last['end'];assert first['end']==last['start'] and end-start==48
    rows=[]
    for lang,name in [('pt-BR','preview_formula_pt.wav'),('en','preview_formula_en.wav')]:
        source=c.V/f'audio/film1/{lang}.wav'
        expected=next(r for r in delivery['media'] if r['film']=='film1' and r['language']==lang and r['path'].endswith('.wav'))
        runtime.verify_pin(c,expected)
        with wave.open(str(source),'rb') as reader:
            channels,width,rate=reader.getnchannels(),reader.getsampwidth(),reader.getframerate()
            assert reader.getcomptype()=='NONE'
            offset=round(start*rate);count=round((end-start)*rate)
            reader.setpos(offset);raw=reader.readframes(count)
            assert len(raw)==count*channels*width
        out=c.C/name
        if not out.exists():
            tmp=out.with_name(out.name+'.tmp_'+str(time.time_ns()))
            with wave.open(str(tmp),'wb') as writer:
                writer.setnchannels(channels);writer.setsampwidth(width);writer.setframerate(rate);writer.writeframes(raw)
            with wave.open(str(tmp),'rb') as reader:assert reader.readframes(count)==raw and reader.getnframes()==count
            os.rename(tmp,out)
        with wave.open(str(out),'rb') as reader:
            assert reader.readframes(count)==raw and reader.getnframes()==count
            assert (reader.getnchannels(),reader.getsampwidth(),reader.getframerate())==(channels,width,rate)
        runtime.verify_pin(c,expected)
        rows.append({'language':lang,'source':c.old.pin(source),'preview':c.old.pin(out),
                     'start_seconds':start,'end_seconds':end,'duration_seconds':count/rate,
                     'pcm_sha256':c.builder_module().sha(raw),'sample_offset':offset,'sample_count':count,
                     'sample_rate':rate,'channels':channels,'sample_width_bytes':width,'exact_source_pcm_slice':True})
    runtime.seal_guard(c)
    receipt={'status':'PASS_LOCAL_PCM_EXCERPTS','actor':c.ACTOR,'source':'v402','source_sha256':data['source_sha256'],
             'preflight':pre,'plan_sha256':plan['plan_sha256'],'audio_delivery':ready['receipt'],'previews':rows,
             'new_tts_requests':0,'normalization_applied':False,'resampling':False,'time_compression':False,
             'original_duration_changed':False,'perceptual_audition':False,'personal_voice_used':False}
    target=c.C/'FORMULA_LISTENING_PREVIEWS.json'
    if target.exists():
        old=c.old.read(target);assert old['previews']==rows and old['plan_sha256']==plan['plan_sha256']
    else:c.old.write_new(target,receipt)
    print(json.dumps({'status':receipt['status'],'receipt':c.old.pin(target),'previews':rows}),flush=True)


def pointer():
    pre,data,plan,review,new=c.execution_gate()
    complete=c.V/'audit/DELIVERY_D_V402.json';full=c.old.read(complete)
    assert full['source']=='v402' and full['source_sha256']==data['source_sha256']
    assert full['plan_current'] and full['plan_sha256']==plan['plan_sha256']
    target=c.V/'audit/DELIVERY_D.json';raw=target.read_bytes();old=c.old.read(target)
    if old.get('source')=='v402':
        assert old['receipt']['sha256']==c.old.digest(complete);print('CURRENT_POINTER_ALREADY_BOUND');return
    backup=target.with_name(target.name+'.bak_before_v402_'+str(time.time_ns()))
    with backup.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert backup.read_bytes()==raw
    body={'schema':'iald.delivery-d.pointer/v1','status':'CURRENT_RECEIPT_POINTER','source':'v402',
          'source_sha256':data['source_sha256'],'updated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'actor':c.ACTOR,'receipt':{**c.old.pin(complete),'path':complete.name,'relative_to':'this pointer directory'},
          'history_private':{**c.old.pin(backup),'path':backup.name,'relative_to':'this pointer directory',
                             'private':True,'publish':False,'scope':'Previous fixed pointer preserved byte-for-byte.'},
          'scope':'Current technical audio receipt pointer; no mission acceptance or publication.'}
    tmp=target.with_name(target.name+'.tmp_'+str(time.time_ns()))
    data_bytes=(json.dumps(body,ensure_ascii=False,indent=2)+'\n').encode()
    with tmp.open('xb') as f:f.write(data_bytes);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==data_bytes;os.replace(tmp,target)
    c.old.write_new(c.C/'AUDIO_CURRENT_POINTER.json',{'status':'PASS_CURRENT_POINTER','preflight':pre,
        'source':'v402','source_sha256':body['source_sha256'],'pointer':c.old.pin(target),'full_receipt':c.old.pin(complete),
        'previous_bytes_backup':c.old.pin(backup),'tts_requests':0,'retests':False})
    print(json.dumps({'status':'PASS_CURRENT_POINTER','pointer':c.old.pin(target)}),flush=True)


if __name__=='__main__':{'previews':previews,'pointer':pointer}[sys.argv[1]]()
