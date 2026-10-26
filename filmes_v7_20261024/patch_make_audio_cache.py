from pathlib import Path
import os,time,hashlib

p=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7\make_v7.py')
raw=p.read_bytes(); text=raw.decode('utf-8').replace('\r\n','\n')
old="""    if build.get('status')!='COMPLETED' or build.get('tts') is not True: raise ValueError('Audio build incomplete')
    verified=set()"""
new="""    # tts records whether this invocation contacted the service; cached audio is valid.
    if build.get('status')!='COMPLETED' or build.get('pending') or build.get('tts_inflight'): raise ValueError('Audio build incomplete')
    current_plan=run('audio/build_narration.py','plan',capture=True)
    if build.get('plan_sha256')!=current_plan['plan_sha256']: raise ValueError('Audio plan is stale')
    if any(build.get('reports',{}).get(f'film{n}',{}).get('status')!='AUDIO_MEASURED' for n in [1,2]): raise ValueError('Measured audio missing')
    verified=set()"""
assert old in text; text=text.replace(old,new)
old="""            if sha(ROOT/f'audio/film{n}/{lang}.wav')!=tl['loudness'][lang]['sha256']: raise ValueError('Narration audio mismatch')"""
new="""            if tl['loudness'][lang]!=build['reports'][f'film{n}']['loudness'][lang]: raise ValueError('Audio measurement differs from build')
            for extension,expected in [('wav',tl['loudness'][lang]['sha256']),('m4a',tl['loudness'][lang]['aac']['sha256'])]:
                if sha(ROOT/f'audio/film{n}/{lang}.{extension}')!=expected: raise ValueError('Narration audio mismatch')
            for measure in [tl['loudness'][lang]['after'],tl['loudness'][lang]['aac']['measurement']]:
                if abs(float(measure['input_i'])+16)>1: raise ValueError('Narration loudness outside target')"""
assert old in text;text=text.replace(old,new)
old="""    a=p.parse_args()
    if a.data_only and a.finalize_only:"""
new="""    narration=p.add_mutually_exclusive_group()
    narration.add_argument('--narration-cache-only',action='store_true',help='Rebuild narration from verified successful clips without network')
    narration.add_argument('--bounded-retry-authorization',type=Path,help='Explicit human authorization receipt for bounded failed-utterance retries')
    a=p.parse_args()
    if a.data_only and a.finalize_only:"""
assert old in text;text=text.replace(old,new)
old="""        run('audio/build_narration.py','build','--tts','--approved-plan-sha256',plan['plan_sha256'])"""
new="""        if a.narration_cache_only:
            run('audio/build_narration.py','build','--cache-only')
        else:
            narration_args=['--tts','--approved-plan-sha256',plan['plan_sha256']]
            if a.bounded_retry_authorization: narration_args.extend(['--bounded-retry-authorization',a.bounded_retry_authorization])
            run('audio/build_narration.py','build',*narration_args)"""
assert old in text;text=text.replace(old,new)
compile(text,str(p),'exec');out=text.encode('utf-8')
bak=p.with_name(p.name+'.bak_'+str(time.time_ns()));bak.write_bytes(raw)
temp=p.with_name(p.name+'.tmp');temp.write_bytes(out);assert temp.stat().st_size==len(out);os.replace(temp,p)
print({'file':str(p),'sha256':hashlib.sha256(out).hexdigest(),'backup':str(bak)})
