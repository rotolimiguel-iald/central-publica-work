from pathlib import Path
import ast, runpy

r=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
p=r/'cinema/media_v7.py';m=runpy.run_path(str(p));s=p.read_text(encoding='utf-8')
old="require(build.get('tts') is True and build.get('status')=='COMPLETED','TTS receipt incomplete');require(build.get('plan_sha256')==narration.get('plan_sha256'),'Audio plan mismatch')"
new="""require(build.get('status')=='COMPLETED' and build.get('tts') in (True,False) and build.get('tts_inflight') is False and not build.get('pending'),'Narration receipt incomplete');require(build.get('plan_sha256')==narration.get('plan_sha256'),'Audio plan mismatch')
 plans=[load(p) for p in directory.glob('NARRATION_PLAN*.json') if load(p).get('plan_sha256')==build['plan_sha256']];require(plans,'Matching narration plan absent');plan=plans[-1];body={k:v for k,v in plan.items() if k!='plan_sha256'}
 require(hashlib.sha256((json.dumps(body,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\\n').encode('utf-8')).hexdigest()==build['plan_sha256'],'Narration plan content hash mismatch')
 for key,path in {'hud_sha256':root/'data/hud.json','film1_sha256':root/'data/film1.json','film2_sha256':root/'data/film2.json','builder_sha256':root/'audio/build_narration.py','template_sha256':root/'audio/script_templates.json'}.items():require(plan['pins'][key]==sha(path),'Stale narration plan: '+key)
 require(build['reports'][f'film{film}']['status']=='AUDIO_MEASURED','Film audio not measured')"""
assert s.count(old)==1;s=s.replace(old,new)
helper="""def reuse_prepared_video(pipe,args,h264_only=False):
 # Reuse verified media even when unrelated mux/audio code changed. The original
 # producer script pin remains in every stage receipt; never rewrite provenance.
 j,raw,job,duration=read_job(pipe.root,args.job,args.film);labels=['4k','1080p']+([] if args.no_720 else ['720p'])+([] if h264_only else ['vp9']);reports=[]
 for label in labels:
  path=pipe.out/'.pipeline'/f'film{args.film}_silent_{label}.json'
  if not path.exists():return None
  d=load(path)
  if d.get('status')!='COMPLETE' or not cache_valid(d,d.get('key')):return None
  if any(not Path(p['file']).is_file() or pin(Path(p['file']))!=p for p in d['inputs']):return None
  if label=='4k' and (not d['inputs'] or d['inputs'][0]!=pin(j)):return None
  producer=d['parameters']['script'];producer_path=Path(producer['file'])
  candidates=[producer_path,*producer_path.parent.glob(producer_path.name+'.bak_*')]
  require(any(p.is_file() and sha(p)==producer['sha256'] for p in candidates),'Prepared video producer script not recoverable')
  reports.append({**d,'cache_hit':True,'reuse_basis':'unchanged source job, input and output SHA; original producer retained'})
 return {'schema':SCHEMA,'status':'H264_READY' if h264_only else 'COMPLETE','film':args.film,'source_job':pin(j),'duration':duration,'fps':FPS,'stages':reports,'private':True,'audio_required':False,'reused_without_encoding':True}

"""
assert s.count('def prepare_video(pipe,args):')==1
s=s.replace('def prepare_video(pipe,args):',helper+"def prepare_video(pipe,args):\n reused=reuse_prepared_video(pipe,args)\n if reused:return reused")
old="captions_report=captions(root,film);prepared=prepare_video(pipe,args);reports=[]"
new="captions_report=captions(root,film);h264_only=args.action=='mux-h264';prepared=reuse_prepared_video(pipe,args,True) if h264_only else prepare_video(pipe,args);require(prepared is not None,'Current prepared H264 stages not ready');reports=[]"
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace("  if lang=='en' or args.vp9_pt:","  if not h264_only and (lang=='en' or args.vp9_pt):")
s=s.replace("jsave(pipe.out/f'ENCODE_FILM{film}.json',result);return result", "jsave(pipe.out/(f'MUX_H264_FILM{film}.json' if h264_only else f'ENCODE_FILM{film}.json'),result);return result")
s=s.replace("b.get('status')=='COMPLETED' and b.get('tts') is True", "b.get('status')=='COMPLETED' and b.get('tts_inflight') is False and not b.get('pending')")
s=s.replace("'validate','prepare-video']);", "'validate','prepare-video','mux-h264']);")
s=s.replace("elif a.action=='film':require", "elif a.action in ('film','mux-h264'):require")
ast.parse(s);m['atomic'](p,s.encode('utf-8'));print(m['pin'](p))
