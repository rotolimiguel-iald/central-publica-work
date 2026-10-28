"""ORDEM 022/E: deterministic local media pipeline; no TTS or implicit encoding.


Run `discover --audio-dir PATH` to enumerate exact inputs. Producing actions require


--job-ready, supplied by coordinator only AFTER final jobs are ready. This switch


is an execution guard, not authentication or authorization by itself.


Examples (paths relative to delivery_v7 unless absolute):


  media_v7.py self-test


  media_v7.py discover --audio-dir audio


  media_v7.py captions --film 1


  media_v7.py assets --job-ready


  media_v7.py film --film 1 --job cinema/render/jobs/EXACT.json --audio-dir audio --job-ready


  media_v7.py loop --job cinema/render/jobs/EXACT_LOOP.json --job-ready


Audio contract: audio-dir/filmN/en.wav and pt-BR.wav (agent D README).


Optional --audio-map JSON: {"1":{"en":"EXACT.wav","pt-BR":"EXACT.wav"},"2":{...}};


paths are confined to --audio-dir. No latest-file or filename guessing.


Private 4K files live in render/private; public outputs in render. No source writes.


"""


from pathlib import Path


import argparse,contextlib,datetime,hashlib,io,json,math,os,re,struct,subprocess,sys,time,wave,runpy


ROOT=Path(__file__).resolve().parent.parent


FF_DEFAULT=ROOT.parent/'node_modules/@ffmpeg-installer/win32-x64/ffmpeg.exe'


LANGS=('en','pt-BR','fr','zh-Hans')


SCHEMA='iald.media.v7.1'


FPS=60





def require(ok,message):


 if not ok:raise ValueError(message)


def sha(path):


 h=hashlib.sha256()


 with Path(path).open('rb') as f:


  for chunk in iter(lambda:f.read(4<<20),b''):h.update(chunk)


 return h.hexdigest()


def pin(path):


 p=Path(path);require(p.is_file(),'Missing input: '+str(p));return {'file':str(p.resolve()),'bytes':p.stat().st_size,'sha256':sha(p)}


def load(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def stamp():return datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')


def backup(path):


 if path.exists():


  dest=path.with_name(path.name+'.bak_'+stamp())


  with path.open('rb') as a,dest.open('xb') as b:


   for chunk in iter(lambda:a.read(4<<20),b''):b.write(chunk)


   b.flush();os.fsync(b.fileno())


  require(sha(dest)==sha(path),'Backup mismatch')


def atomic(path,data):


 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)


 if isinstance(data,str):data=data.encode('utf-8')


 tmp=path.with_name(path.name+'.'+stamp()+'.tmp')


 with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())


 require(tmp.stat().st_size==len(data)>0,'Empty or short write');backup(path);os.replace(tmp,path)


def jsave(path,obj):atomic(path,json.dumps(obj,ensure_ascii=False,indent=2))


def confined(path,base):


 p=Path(path);p=(base/p if not p.is_absolute() else p).resolve();require(p.is_relative_to(base.resolve()),'Path outside allowed directory: '+str(p));return p





def seconds(s):


 parts=s.split(':');require(len(parts) in (2,3),'Invalid VTT timestamp')


 if len(parts)==2:parts=['0',*parts]


 h,m,se=map(float,parts);require(h>=0 and 0<=m<60 and 0<=se<60,'Invalid VTT clock');return h*3600+m*60+se


def validate_vtt(text,duration):


 require(text.lstrip('\ufeff').startswith('WEBVTT'),'Missing WEBVTT header');prior=0;count=0


 for block in re.split(r'\r?\n\s*\r?\n',text.strip()):


  if block.startswith(('NOTE','STYLE','REGION')):continue


  for line in block.splitlines():


   if '-->' not in line:continue


   match=re.fullmatch(r'\s*((?:\d{2,}:)?\d{2}:\d{2}\.\d{3})\s+-->\s+((?:\d{2,}:)?\d{2}:\d{2}\.\d{3})(?:\s+.*)?',line)


   require(match is not None,'Malformed caption timing');start,end=map(seconds,match.groups());require(start>=prior-1e-6 and end>start and end<=duration+.004,'Overlapping/out-of-duration caption');prior=end;count+=1


 require(count>0,'No caption cues');return {'cues':count,'nonoverlap':True,'within_duration':True}


def timeline(root,film):


 p=root/f'data/film{film}.json';d=load(p);duration=float(d.get('total_seconds',d.get('duration',0)));require(duration>0,'Missing duration');require(d.get('fps')==FPS,'Timeline must declare 60 FPS');return p,d,duration





def captions(root,film):


 t,d,duration=timeline(root,film);base=root/f'subs/filme{film}';paths=[base/f'{lang}.vtt' for lang in LANGS]+[base/'chapters.vtt']


 # Every translated cue set must match the selected narration, as specified by D.


 paths += [base/f'sync-{audio}'/f'{lang}.vtt' for audio in ('en','pt-BR') for lang in LANGS]


 return {'timeline':pin(t),'files':[{**pin(p),**validate_vtt(p.read_text(encoding='utf-8-sig'),duration)} for p in paths]}





def validate_source_pins(root,job):

 pins=job.get('source_files',{});require(len(pins)>10,'Legacy job lacks render dependency closure')

 helper=root/'cinema/render_sources.py';require(helper.is_file(),'Render closure helper missing')

 expected=runpy.run_path(str(helper),run_name='media_render_sources')['collect'](root)

 require(set(pins)==set(expected),'Job render dependency closure incomplete')

 for name,current in expected.items():require(pins[name]==current,'Stale job source: '+name)

 return pins



def read_job(root,path,film=None):


 p=confined(path,root/'cinema/render/jobs');d=load(p);validate_source_pins(root,d);m=d.get('metadata',{});n=m.get('total');require(isinstance(n,int) and n>1,'Invalid frame count');require(d.get('render',{}).get('encoded')==n,'Job not completely encoded');require(m.get('fps')==FPS,'Job must be 60 FPS')


 if film:require(m.get('film')==film and m.get('kind')==f'film{film}','Wrong film job');require((m.get('width'),m.get('height'))==(3840,2160),'Expected 4K job')


 else:require(m.get('kind')=='loop','Expected explicit loop job')


 raw=confined(d.get('file',''),root/'cinema/render/jobs');require(raw.suffix=='.h264','Expected H264 elementary stream');require(d.get('sha256')==sha(raw),'Job stream SHA mismatch');require(d.get('bytes')==raw.stat().st_size,'Job stream size mismatch')


 duration=n/FPS


 if film:


  tp,_,expected=timeline(root,film);require(abs(duration-expected)<=1/FPS+.004,'Job / timeline duration mismatch')


 require(abs(float(m.get('duration',duration))-duration)<=1/FPS+.004,'Job duration mismatch')


 return p,raw,d,duration





def audio_inputs(root,directory,film,mapping=None):


 directory=directory.resolve();require(directory.is_dir(),'Audio directory absent');explicit=load(mapping).get(str(film),{}) if mapping else {lang:f'film{film}/{lang}.wav' for lang in ('en','pt-BR')}


 require(set(explicit)=={'en','pt-BR'},'Both explicit narration languages required');paths={lang:confined(name,directory) for lang,name in explicit.items()}


 require(len(set(paths.values()))==2,'Two different audio files required')


 for p in paths.values():require(p.suffix.lower()=='.wav' and p.is_file(),'Missing explicit WAV: '+str(p))


 receipt=root/f'data/film{film}_narration_timeline.json';narration=load(receipt);require(narration.get('status')=='AUDIO_MEASURED','Narration not measured by agent D');build=load(root/'audio/NARRATION_BUILD.json');require(build.get('status')=='COMPLETED' and build.get('tts') in (True,False) and build.get('tts_inflight') is False and not build.get('pending'),'Narration receipt incomplete');require(build.get('plan_sha256')==narration.get('plan_sha256'),'Audio plan mismatch')
 plans=[load(p) for p in directory.glob('NARRATION_PLAN*.json') if load(p).get('plan_sha256')==build['plan_sha256']];require(plans,'Matching narration plan absent');plan=plans[-1];body={k:v for k,v in plan.items() if k!='plan_sha256'}
 require(hashlib.sha256((json.dumps(body,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode('utf-8')).hexdigest()==build['plan_sha256'],'Narration plan content hash mismatch')
 for key,path in {'hud_sha256':root/'data/hud.json','film1_sha256':root/'data/film1.json','film2_sha256':root/'data/film2.json','builder_sha256':root/'audio/build_narration.py','template_sha256':root/'audio/script_templates.json'}.items():require(plan['pins'][key]==sha(path),'Stale narration plan: '+key)
 require(build['reports'][f'film{film}']['status']=='AUDIO_MEASURED','Film audio not measured')


 for lang,path in paths.items():require(sha(path)==narration['loudness'][lang]['sha256']==build['reports'][f'film{film}']['loudness'][lang]['sha256'],'Audio receipt SHA mismatch')


 return paths,receipt





def cache_key(inputs,parameters):


 return hashlib.sha256(json.dumps({'inputs':inputs,'parameters':parameters},sort_keys=True,separators=(',',':')).encode()).hexdigest()


def cache_valid(receipt,key):


 if receipt.get('status')!='COMPLETE' or receipt.get('key')!=key:return False


 try:return bool(receipt['outputs']) and all(pin(Path(x['file']))==x for x in receipt['outputs'])


 except (OSError,ValueError,KeyError):return False





class Pipeline:


 def __init__(self,root,ffmpeg):self.root=root;self.out=root/'render';self.ff=ffmpeg;self.current=None;self.command_seconds=0;self.toolpin=None


 def run(self,args,label):


  require(self.current is not None,'FFmpeg only inside explicit production stage');start=time.perf_counter();r=subprocess.run([str(self.ff),'-y','-nostdin','-hide_banner',*map(str,args)],capture_output=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0));elapsed=time.perf_counter()-start;self.command_seconds+=elapsed


  atomic(self.current/(label+'.log'),r.stderr or b'No stderr');require(r.returncode==0,'FFmpeg failed: '+label+'; see stage log');return r


 def stage(self,name,inputs,parameters,outputs,work):


  require(re.fullmatch(r'[a-zA-Z0-9_-]+',name) is not None,'Invalid stage name');self.out.mkdir(parents=True,exist_ok=True);base=self.out/'.pipeline';base.mkdir(exist_ok=True);lock=base/(name+'.lock');fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)


  try:


   os.write(fd,json.dumps({'pid':os.getpid(),'created':stamp()}).encode());os.fsync(fd)


   start=time.perf_counter();self.toolpin=self.toolpin or pin(self.ff);inputpins=[pin(p) for p in inputs];parameters={**parameters,'script':pin(Path(__file__)),'ffmpeg':self.toolpin};key=cache_key(inputpins,parameters);receipt=base/(name+'.json')


   if receipt.exists() and cache_valid(load(receipt),key):return {**load(receipt),'cache_hit':True,'lookup_elapsed_seconds':time.perf_counter()-start}


   directory=base/(name+'_'+key[:16]+'_'+stamp());directory.mkdir();self.current=directory;self.command_seconds=0


   tmp={k:directory/(k+Path(v).suffix) for k,v in outputs.items()};result=work(tmp) or {}


   require(all(p.is_file() and p.stat().st_size>0 for p in tmp.values()),'Incomplete stage outputs');require([pin(p) for p in inputs]==inputpins,'Inputs changed during stage')


   for k,dest in outputs.items():dest.parent.mkdir(parents=True,exist_ok=True);backup(dest);os.replace(tmp[k],dest)


   report={'schema':SCHEMA,'stage':name,'status':'COMPLETE','key':key,'inputs':inputpins,'parameters':parameters,'outputs':[pin(p) for p in outputs.values()],'result':result,'elapsed_seconds':time.perf_counter()-start,'ffmpeg_seconds':self.command_seconds,'cache_hit':False};jsave(receipt,report);return report


  except Exception as exc:


   if self.current:jsave(self.current/'FAILED.json',{'status':'FAILED','error':str(exc),'elapsed_ffmpeg_seconds':self.command_seconds})


   raise


  finally:


   self.current=None;os.close(fd);lock.unlink()


 def loudness(self,source,label):


  r=self.run(['-i',source,'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],label);matches=re.findall(r'\{\s*"input_i".*?\}',r.stderr.decode(errors='replace'),re.S);require(matches,'No loudness result');d=json.loads(matches[-1]);value=float(d['input_i']);require(math.isfinite(value) and abs(value+16)<=1,'Loudness outside -16 +/-1 LUFS');return {'integrated_lufs':value,'true_peak_dbfs':float(d['input_tp'])}





def check_mp4(path,width,height,duration,language=None,limit=None):


 d=mp4(path);video=[t for t in d['tracks'] if t['type']=='vide'];audio=[t for t in d['tracks'] if t['type']=='soun'];require(len(video)==1,'Expected one video track');v=video[0];require(v['codec'] in ('avc1','avc3'),'Not H264');require((v['width'],v['height'])==(width,height),'Wrong video size');require(abs(v['fps']-FPS)<.001,'Not 60 fps');require(abs(v['duration']-duration)<=1/FPS+.01,'Video duration mismatch')


 if language:require(len(audio)==1 and audio[0]['language']==language,'Audio track/language mismatch');require(abs(audio[0]['duration']-duration)<.1,'Audio duration mismatch')


 else:require(not audio,'Loop has audio')


 if limit:require(path.stat().st_size<=limit,'Media size budget exceeded')


 # Faststart check reads only box headers, never searches random payload bytes.


 order=[]


 with path.open('rb') as f:


  while f.tell()<path.stat().st_size:


   start=f.tell();b=f.read(8);require(len(b)==8,'Malformed MP4');size,kind=struct.unpack('>I4s',b)


   if size==1:size=struct.unpack('>Q',f.read(8))[0]


   if size==0:size=path.stat().st_size-start


   require(size>=8 and start+size<=path.stat().st_size,'Invalid box');order.append(kind);f.seek(start+size)


 require(b'moov' in order and b'mdat' in order and order.index(b'moov')<order.index(b'mdat'),'MP4 is not faststart');return d





def reuse_prepared_video(pipe,args,h264_only=False):
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

def prepare_video(pipe,args):
 reused=reuse_prepared_video(pipe,args)
 if reused:return reused
 root=pipe.root;film=args.film;j,raw,job,duration=read_job(root,args.job,film);reports=[];private=pipe.out/'private';master=private/f'filme{film}_4k_silent.mp4';inputs=[j,raw,root/'cinema/render_sources.py',*[(root/'cinema'/name).resolve() for name in job['source_files']]]
 def master_copy(tmp):
  timed=pipe.current/'timing.h264';pipe.run(['-v','warning','-r',FPS,'-i',raw,'-c:v','copy','-bsf:v','h264_metadata=tick_rate=120:fixed_frame_rate_flag=1','-f','h264',timed],'timing')
  pipe.run(['-v','warning','-fflags','+genpts','-r',FPS,'-i',timed,'-map','0:v:0','-an','-c:v','copy','-video_track_timescale','60000','-movflags','+faststart',tmp['video']],'copy4k');return {'public':False,'silent':True,'metrics':check_mp4(tmp['video'],3840,2160,duration)}
 reports.append(pipe.stage(f'film{film}_silent_4k',inputs,{'fps':FPS,'silent':True},{'video':master},master_copy))
 for label,w,h,rate in [('1080p',1920,1080,2800000),('720p',1280,720,1100000)]:
  if label=='720p' and args.no_720:continue
  dest=private/f'filme{film}_{label}_silent.mp4'
  def resize(tmp):
   pipe.run(['-v','warning','-i',master,'-map','0:v:0','-an','-vf',f'scale={w}:{h}','-c:v','libx264','-threads','8','-preset','fast','-b:v',rate,'-maxrate',rate,'-bufsize',rate*2,'-pix_fmt','yuv420p','-r',FPS,'-video_track_timescale','60000','-movflags','+faststart',tmp['video']],'encode');return {'public':False,'silent':True,'metrics':check_mp4(tmp['video'],w,h,duration,limit=24000000*duration/60 if label=='1080p' else None)}
  reports.append(pipe.stage(f'film{film}_silent_{label}',[master],{'size':[w,h],'rate':rate,'fps':FPS},{'video':dest},resize))
 h264=private/f'filme{film}_1080p_silent.mp4';measured=next(t['bitrate_bps'] for t in mp4(h264)['tracks'] if t['type']=='vide');rate=round(measured*.5);webm=private/f'filme{film}_1080p_silent.webm'
 def vp9(tmp):
  common=['-v','warning','-i',h264,'-map','0:v:0','-an','-c:v','libvpx-vp9','-b:v',rate,'-deadline','good','-cpu-used','4','-row-mt','1','-tile-columns','2','-threads','8','-g','240','-pix_fmt','yuv420p','-passlogfile',pipe.current/'vp9'];pipe.run([*common,'-pass','1','-f','webm',os.devnull],'pass1');pipe.run([*common,'-pass','2',tmp['video']],'pass2');pipe.run(['-v','error','-xerror','-i',tmp['video'],'-f','null','-'],'decode_check');return {'public':False,'silent':True,'h264_measured_video_bps':measured,'vp9_target_bps':rate,'policy':'half measured H264 video bitrate'}
 reports.append(pipe.stage(f'film{film}_silent_vp9',[h264],{'rate':rate,'fps':FPS},{'video':webm},vp9));report={'schema':SCHEMA,'status':'COMPLETE','film':film,'source_job':pin(j),'duration':duration,'fps':FPS,'stages':reports,'private':True,'audio_required':False,'preview1080':pin(h264)};jsave(pipe.out/f'PREPARE_VIDEO_FILM{film}.json',report);return report

def encode_film(pipe,args):
 root=pipe.root;film=args.film;j,raw,job,duration=read_job(root,args.job,film);audio,ar=audio_inputs(root,args.audio_dir,film,args.audio_map);captions_report=captions(root,film);h264_only=args.action=='mux-h264';prepared=reuse_prepared_video(pipe,args,True) if h264_only else prepare_video(pipe,args);require(prepared is not None,'Current prepared H264 stages not ready');reports=[]
 for lang,iso in [('en','eng'),('pt-BR','por')]:
  suffix='' if lang=='en' else '_pt-BR'
  def audio_check(tmp):
   with wave.open(str(audio[lang]),'rb') as wav:require(abs(wav.getnframes()/wav.getframerate()-duration)<=.05,'WAV duration mismatch')
   measurement=pipe.loudness(audio[lang],'wav_loudness');jsave(tmp['measurement'],measurement);return measurement
  reports.append(pipe.stage(f'film{film}_{lang}_audio_verify',[audio[lang],ar,root/'audio/NARRATION_BUILD.json'],{'duration':duration},{'measurement':pipe.out/'private'/f'film{film}_{lang}_loudness.json'},audio_check))
  for label,w,h in [('4k',3840,2160),('1080p',1920,1080),('720p',1280,720)]:
   if label=='720p' and args.no_720:continue
   silent=pipe.out/'private'/f'filme{film}_{label}_silent.mp4';dest=(pipe.out/'private' if label=='4k' else pipe.out)/f'filme{film}_{label}{suffix}.mp4'
   def mux(tmp):
    pipe.run(['-v','warning','-i',silent,'-i',audio[lang],'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','160k','-ar','48000','-t',duration,'-metadata:s:a:0','language='+iso,'-video_track_timescale','60000','-movflags','+faststart',tmp['video']],'mux')
    metrics=check_mp4(tmp['video'],w,h,duration,iso,25000000*duration/60 if label=='1080p' else None);loud=pipe.loudness(tmp['video'],'encoded_loudness')
    # Packet hashes confirm byte-identical coded video rather than just a copy flag.
    hashes=[]
    for index,src in enumerate((silent,tmp['video'])):
     result=pipe.run(['-v','error','-i',src,'-map','0:v:0','-c:v','copy','-f','hash','-hash','sha256','-'],f'video_hash_{index}');hashes.append(result.stdout.decode().strip())
    require(hashes[0]==hashes[1] and hashes[0].startswith('SHA256='),'Mux changed coded video');return {'public':label!='4k','language':lang,'video_stream_copy':True,'video_packet_hash':hashes[0],'metrics':metrics,'loudness':loud}
   reports.append(pipe.stage(f'film{film}_{lang}_{label}_mux',[silent,audio[lang],ar],{'language':lang,'video_copy':True},{'video':dest},mux))
  if not h264_only and (lang=='en' or args.vp9_pt):
   silent=pipe.out/'private'/f'filme{film}_1080p_silent.webm';dest=pipe.out/f'filme{film}_1080p{suffix}.webm'
   def web_mux(tmp):
    pipe.run(['-v','warning','-i',silent,'-i',audio[lang],'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','libopus','-b:a','96k','-t',duration,'-metadata:s:a:0','language='+iso,tmp['video']],'mux');return {'public':True,'video_stream_copy':True,'language':lang,'loudness':pipe.loudness(tmp['video'],'opus_loudness')}
   reports.append(pipe.stage(f'film{film}_{lang}_vp9_mux',[silent,audio[lang],ar],{'language':lang,'video_copy':True},{'video':dest},web_mux))
 result={'schema':SCHEMA,'status':'COMPLETE','film':film,'source_job':pin(j),'prepared_video':prepared,'captions':captions_report,'stages':reports,'public_masters':False};jsave(pipe.out/(f'MUX_H264_FILM{film}.json' if h264_only else f'ENCODE_FILM{film}.json'),result);return result

def encode_loop(pipe,args):


 j,raw,job,duration=read_job(pipe.root,args.job);n=job['metadata']['total'];rate=min(1250000,int(3000000*8/duration*.85));require(rate>=100000,'Loop too long for 3MB budget');mp=pipe.out/'filme1_loop_titulo.mp4';web=pipe.out/'filme1_loop_titulo.webm'


 def ends(p):


  r=pipe.run(['-v','error','-i',p,'-map','0:v:0','-vf',f"select='eq(n,0)+eq(n,{n-1})'",'-vsync','0','-f','framemd5','pipe:1'],p.stem+'_ends');lines=[x for x in r.stdout.decode().splitlines() if x and not x.startswith('#')];require(len(lines)==2,'Loop endpoint frame count');hashes=[x.split(',')[-1].strip() for x in lines];require(hashes[0]==hashes[1],'Loop endpoints differ');return hashes


 def build(tmp):


  encoded=pipe.current/'encoded.mp4';pipe.run(['-v','warning','-r',FPS,'-i',raw,'-an','-vf','scale=1920:1080','-c:v','libx264','-threads','8','-preset','fast','-b:v',rate,'-maxrate',rate,'-bufsize',rate*2,'-bf','0','-pix_fmt','yuv420p','-r',FPS,'-frames:v',n,encoded],'encode')


  head,body,closed=[pipe.current/x for x in ('head.h264','body.h264','closed.h264')]


  for count,dest in [(1,head),(n-1,body)]:pipe.run(['-v','error','-i',encoded,'-map','0:v:0','-c:v','copy','-frames:v',count,'-bsf:v','h264_mp4toannexb','-f','h264',dest],dest.stem)


  atomic(closed,body.read_bytes()+head.read_bytes());pipe.run(['-v','warning','-fflags','+genpts','-r',FPS,'-i',closed,'-an','-c:v','copy','-frames:v',n,'-video_track_timescale','60000','-movflags','+faststart',tmp['mp4']],'mux');check_mp4(tmp['mp4'],1920,1080,duration,limit=3000000);mp_proof=ends(tmp['mp4'])


  ivf=pipe.current/'loop.ivf';pipe.run(['-v','warning','-i',tmp['mp4'],'-an','-c:v','libvpx-vp9','-b:v',min(rate,1000000),'-deadline','good','-cpu-used','4','-row-mt','1','-threads','8','-g','240','-pix_fmt','yuv420p','-f','ivf',ivf],'vp9')


  data=ivf.read_bytes();require(data[:4]==b'DKIF','Bad IVF');at=32;packets=[]


  while at<len(data):


   require(at+12<=len(data),'Truncated IVF');length,ts=struct.unpack_from('<IQ',data,at);at+=12;require(at+length<=len(data),'Truncated packet');packets.append(data[at:at+length]);at+=length


  require(len(packets)==n,'Wrong IVF frame count');joined=bytearray(data[:32]);struct.pack_into('<I',joined,24,n)


  for i,b in enumerate(packets[:-1]+packets[:1]):joined+=struct.pack('<IQ',len(b),i)+b


  sealed=pipe.current/'closed.ivf';atomic(sealed,joined);pipe.run(['-v','warning','-i',sealed,'-an','-c:v','copy',tmp['webm']],'webm');require(tmp['webm'].stat().st_size<=3000000,'WebM loop exceeds 3MB');return {'mp4_endpoint_md5':mp_proof,'webm_endpoint_md5':ends(tmp['webm']),'public':True,'frames':n,'audio_streams':0}


 return pipe.stage('loop',[j,raw,pipe.root/'cinema/render_sources.py',*[(pipe.root/'cinema'/name).resolve() for name in job['source_files']]],{'duration':duration,'frames':n,'fps':FPS,'rate':rate,'endpoint':'repeat independently coded first frame as last'},{'mp4':mp,'webm':web},build)





def prepare_assets(pipe,args):


 # Pillow is deliberately imported only when coordinator runs the assets action.


 from PIL import Image,ImageEnhance,ImageOps


 root=pipe.root;directory=root/'cinema/render/stills';entries={};all_entries=[]


 # Operator explicitly selected newest 224/360 still batch; never fall back to V6.


 tp,t,_=timeline(root,1);chapters=t.get('scenes') or t.get('chapters');expected={c['key']:(float(c['start'])+float(c['end']))/2 for c in chapters}


 for p in sorted(directory.glob('*.json')):


  d=load(p);state=d.get('state',{})
  if p.stat().st_mtime_ns < (root/'data/hud.json').stat().st_mtime_ns:continue
  all_entries.append((p,d,state))


 clean=[]


 for key,midpoint in expected.items():


  matches=[(p,d,state) for p,d,state in all_entries if state.get('film')==1 and state.get('key')==key and state.get('clean') is True and abs(float(state.get('time',-1))-midpoint)<.01]


  require(matches,'No current midpoint still: '+key);clean.append(max(matches,key=lambda row:row[0].stat().st_mtime_ns))


 cutoff=min(row[0].stat().st_mtime_ns for row in clean)


 for p,d,state in all_entries:


  if p.stat().st_mtime_ns<cutoff:continue


  key=(state.get('film'),state.get('key'))


  if key not in entries or p.stat().st_mtime_ns>entries[key][0].stat().st_mtime_ns:entries[key]=(p,d)





 def choose(film,key,clean=None):


  require((film,key) in entries,'Missing explicit still key: '+str((film,key)));p,d=entries[(film,key)];s=d['state']


  if clean is not None:require(s.get('clean') is clean,'Still clean flag mismatch')


  require((d.get('width'),d.get('height'))==(3840,2160),'Still metadata not 4K');img=confined(d['file'],directory);require(img.suffix.lower()=='.png' and sha(img)==d['sha256'],'Still PNG hash mismatch');return p,img


 tp,t,_=timeline(root,1);chapters=t.get('scenes') or t.get('chapters');require(len(chapters)==9,'Expected nine clean film1 stills');jobs=[]


 for c in chapters:


  key=c['key'];require(re.fullmatch(r'[a-zA-Z0-9_-]+',key) is not None,'Unsafe key');jobs.append((f'film1_{key}',choose(1,key,True),pipe.out/f'stills/filme1_{key}_2560_dark.jpg','dark'))


 for film,key in sorted(entries):


  if film==2 and key and key.startswith('review_'):


   require(re.fullmatch(r'[a-zA-Z0-9_-]+',key) is not None,'Unsafe review key');jobs.append((f'film2_{key}',choose(2,key),pipe.out/f'stills/filme2_{key}_2560.jpg','normal'))


 require(any(x[0].startswith('film2_') for x in jobs),'No film2 review shots')


 jobs += [('poster1',choose(1,args.poster1_key,True),pipe.out/'filme1_poster.jpg','normal'),('poster2',choose(2,args.poster2_key),pipe.out/'filme2_poster.jpg','normal'),('og',choose(2,args.og_key),pipe.out/'og_1200x630.jpg','og')]


 reports=[]


 for name,inputs,dest,style in jobs:


  def make(tmp):


   with Image.open(inputs[1]) as src:require(src.size==(3840,2160),'PNG dimensions mismatch');im=src.convert('RGB')


   im=ImageOps.fit(im,(1200,630),method=Image.Resampling.LANCZOS) if style=='og' else im.resize((2560,1440),Image.Resampling.LANCZOS)


   if style=='dark':im=ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(.7)).enhance(.48)


   for q in (90,86,82,78,74,70,66,60,52,45):


    out=io.BytesIO();im.save(out,format='JPEG',quality=q,optimize=True,progressive=True)


    if len(out.getvalue())<=400000:atomic(tmp['image'],out.getvalue());return {'public':True,'quality':q,'width':im.width,'height':im.height,'max_bytes':400000}


   raise ValueError('JPEG exceeds 400KB at declared quality presets')


  reports.append(pipe.stage('asset_'+name,[tp,root/'data/hud.json',root/'data/PROVENANCE_PUBLIC.json',*inputs],{'style':style,'quality_presets':[90,86,82,78,74,70,66,60,52,45],'max_bytes':400000},{'image':dest},make))


 jsave(pipe.out/'ASSETS_AUDIT.json',{'schema':SCHEMA,'stages':reports});return reports





# Adapted small ISO-BMFF metrics reader, copied from previous mp4_metrics.py.


def boxes(data):


 at=0


 while at+8<=len(data):


  size,kind=struct.unpack_from('>I4s',data,at);head=8


  if size==1:size=struct.unpack_from('>Q',data,at+8)[0];head=16


  if size==0:size=len(data)-at


  if size<head or at+size>len(data):raise ValueError('Malformed box '+repr(kind))


  yield kind.decode('ascii',errors='replace'),data[at+head:at+size];at+=size





def find(data,key):


 for k,v in boxes(data):


  if k==key:return v


 raise KeyError(key)





def mp4(path):


 with path.open('rb') as f:


  moov=None


  while True:


   head=f.read(8)


   if not head:break


   if len(head)!=8:raise ValueError('Truncated top-level MP4 box')


   size,kind=struct.unpack('>I4s',head);header=8


   if size==1:size=struct.unpack('>Q',f.read(8))[0];header=16


   if size==0:size=path.stat().st_size-f.tell()+header


   if size<header or f.tell()+size-header>path.stat().st_size:raise ValueError('Invalid top-level MP4 box size')


   if kind==b'moov':moov=f.read(size-header);break


   f.seek(size-header,1)


 if moov is None:raise ValueError('Missing moov')


 mvhd=find(moov,'mvhd');v=mvhd[0];offset=20 if v else 12;timescale=struct.unpack_from('>I',mvhd,offset)[0];duration=struct.unpack_from('>Q' if v else '>I',mvhd,offset+4)[0]/timescale


 tracks=[]


 for kind,tr in boxes(moov):


  if kind!='trak':continue


  tk=find(tr,'tkhd');mdia=find(tr,'mdia');md=find(mdia,'mdhd');handler=find(mdia,'hdlr')[8:12].decode()


  v=md[0];off=20 if v else 12;scale=struct.unpack_from('>I',md,off)[0];dur=struct.unpack_from('>Q' if v else '>I',md,off+4)[0];loff=off+4+(8 if v else 4);lang=struct.unpack_from('>H',md,loff)[0];language=''.join(chr(((lang>>s)&31)+96) for s in [10,5,0])


  stbl=find(find(mdia,'minf'),'stbl');stsd=find(stbl,'stsd');codec=stsd[12:16].decode()


  stts=find(stbl,'stts');n=struct.unpack_from('>I',stts,4)[0];entries=[struct.unpack_from('>II',stts,8+i*8) for i in range(n)];samples=sum(x[0] for x in entries);ticks=sum(x[0]*x[1] for x in entries)


  track={'type':handler,'codec':codec,'language':language,'duration':dur/scale,'samples':samples,'timescale':scale}


  if handler=='vide':track.update(width=struct.unpack_from('>I',tk,len(tk)-8)[0]>>16,height=struct.unpack_from('>I',tk,len(tk)-4)[0]>>16,fps=samples/(ticks/scale))


  stsz=find(stbl,'stsz');uniform_size,count=struct.unpack_from('>II',stsz,4)


  byte_count=uniform_size*count if uniform_size else sum(struct.unpack_from('>I',stsz,12+i*4)[0] for i in range(count))


  track.update(encoded_bytes=byte_count,bitrate_bps=byte_count*8/(dur/scale))


  tracks.append(track)


 return {'file':str(path),'bytes':path.stat().st_size,'duration':duration,'tracks':tracks}





def self_test():


 tests=[]


 def case(name,fn):fn();tests.append(name)


 def refuse(fn):


  try:fn()


  except (ValueError,KeyError,struct.error):return


  raise AssertionError('Expected refusal')


 good='WEBVTT\n\n00:00:00.000 --> 00:00:01.000\na\n\n00:00:01.000 --> 00:00:02.000\nb\n'


 case('caption_nonoverlap',lambda:require(validate_vtt(good,2)['cues']==2,'cues'))


 case('caption_overlap_refused',lambda:refuse(lambda:validate_vtt(good.replace('00:00:01.000 -->','00:00:00.900 -->'),2)))


 case('caption_overrun_refused',lambda:refuse(lambda:validate_vtt(good,1.5)))


 case('caption_malformed_refused',lambda:refuse(lambda:validate_vtt('WEBVTT\n\nwrong --> wrong',3)))


 case('caption_empty_refused',lambda:refuse(lambda:validate_vtt('WEBVTT\n',3)))


 case('clock_bad_minutes_refused',lambda:refuse(lambda:seconds('00:99:00.000')))


 case('cache_changes_inputs',lambda:require(cache_key([{'sha256':'a'}],{})!=cache_key([{'sha256':'b'}],{}),'key'))


 case('cache_changes_parameters',lambda:require(cache_key([],{'fps':60})!=cache_key([],{'fps':30}),'key'))


 case('cache_requires_completion',lambda:require(not cache_valid({'status':'FAILED'},'x'),'cache'))


 case('cache_no_outputs_refused',lambda:require(not cache_valid({'status':'COMPLETE','key':'x','outputs':[]},'x'),'cache'))


 case('path_escape_refused',lambda:refuse(lambda:confined('../outside',ROOT)))


 case('path_inside',lambda:require(confined('render/a',ROOT)==ROOT/'render/a','path'))


 def synthetic_mp4():


  box=lambda name,data:struct.pack('>I4s',8+len(data),name)+data


  mvhd=box(b'mvhd',b'\0'*12+struct.pack('>II',1000,1000))


  tkhd=box(b'tkhd',b'\0'*24+struct.pack('>II',1920<<16,1080<<16))


  language=((ord('e')-96)<<10)|((ord('n')-96)<<5)|(ord('g')-96)


  mdhd=box(b'mdhd',b'\0'*12+struct.pack('>IIH',60000,60000,language))


  hdlr=box(b'hdlr',b'\0'*8+b'vide')


  stsd=box(b'stsd',b'\0'*12+b'avc1')


  stts=box(b'stts',b'\0'*4+struct.pack('>III',1,60,1000))


  stsz=box(b'stsz',b'\0'*4+struct.pack('>II',100,60))


  data=box(b'moov',mvhd+box(b'trak',tkhd+box(b'mdia',mdhd+hdlr+box(b'minf',box(b'stbl',stsd+stts+stsz)))))


  class MemoryPath:


   def open(self,mode):return io.BytesIO(data)


   def stat(self):return type('Stat',(),{'st_size':len(data)})()


   def __str__(self):return 'synthetic-in-memory.mp4'


  d=mp4(MemoryPath());v=d['tracks'][0]


  require((v['width'],v['height'],v['fps'],v['samples'],v['bitrate_bps'])==(1920,1080,60,60,48000),'MP4 metrics mismatch')


 case('copied_mp4_metrics_synthetic',synthetic_mp4)


 case('small_box_reader',lambda:require(list(boxes(struct.pack('>I4s',12,b'test')+b'abcd'))==[('test',b'abcd')],'box'))


 case('bad_box_refused',lambda:refuse(lambda:list(boxes(struct.pack('>I4s',4,b'fail')))))


 case('truncated_box_refused',lambda:refuse(lambda:list(boxes(struct.pack('>I4s',20,b'fail')+b'abcd'))))


 print(json.dumps({'status':'PASS','tests':tests,'count':len(tests),'ffmpeg_calls':0,'Pillow_imported':'PIL' in sys.modules,'media_files_opened':0}));return tests





def validate_delivery(pipe,args):


 expected=[]


 for film in (1,2):


  _,_,duration=timeline(pipe.root,film)


  for lang,suffix,iso in [('en','','eng'),('pt-BR','_pt-BR','por')]:


   expected += [(pipe.out/'private'/f'filme{film}_4k{suffix}.mp4',3840,2160,duration,iso),(pipe.out/f'filme{film}_1080p{suffix}.mp4',1920,1080,duration,iso)]


   if not args.no_720:expected.append((pipe.out/f'filme{film}_720p{suffix}.mp4',1280,720,duration,iso))


  expected.append((pipe.out/f'filme{film}_1080p.webm',1920,1080,duration,'eng'))


  if args.vp9_pt:expected.append((pipe.out/f'filme{film}_1080p_pt-BR.webm',1920,1080,duration,'por'))


 expected += [(pipe.out/'filme1_loop_titulo.mp4',1920,1080,16,None),(pipe.out/'filme1_loop_titulo.webm',1920,1080,16,None)]


 caption_reports=[captions(pipe.root,f) for f in (1,2)]


 images=load(pipe.out/'ASSETS_AUDIT.json')


 imagepaths=[]


 for stage in images['stages']:


  for item in stage['outputs']:require(pin(Path(item['file']))==item and item['bytes']<=400000,'Image altered/oversized');imagepaths.append(Path(item['file']))


 inputs=[x[0] for x in expected]+imagepaths+[pipe.root/f'data/film{f}.json' for f in (1,2)]+[Path(x['file']) for report in caption_reports for x in report['files']]


 def validate(tmp):


  outputs=[]


  for file,w,h,duration,iso in expected:


   start=time.perf_counter();metrics=check_mp4(file,w,h,duration,iso,3000000 if iso is None else 25000000*duration/60 if '_1080p' in file.name else None) if file.suffix=='.mp4' else None


   if iso is None:require(file.stat().st_size<=3000000,'Loop size exceeded')


   result=pipe.run(['-v','error','-xerror','-threads','4','-i',file,'-map','0:v:0','-map','0:a?','-progress','pipe:1','-nostats','-f','null','-'],file.stem+'_'+file.suffix[1:]+'_full_decode')


   counts=re.findall(r'^frame=(\d+)',result.stdout.decode(errors='replace'),re.M);require(counts and abs(int(counts[-1])-round(duration*FPS))<=1,'Decoded frame count mismatch: '+file.name)


   outputs.append({**pin(file),'decode_frames':int(counts[-1]),'full_decode':True,'metrics':metrics,'elapsed_seconds':time.perf_counter()-start})


  report={'status':'PASS','schema':SCHEMA,'movies':outputs,'captions':caption_reports,'images':[pin(p) for p in imagepaths],'integrated_gpu_test':False,'remote_api_calls':0};jsave(tmp['validation'],report);return {'status':'PASS','files':len(outputs),'image_count':len(imagepaths)}


 return pipe.stage('full_validation',inputs,{'full_decode':True,'fps':FPS},{'validation':pipe.out/'MEDIA_VALIDATION.json'},validate)





def watch_jobs(args):


 root=args.root;out=root/'render';out.mkdir(exist_ok=True);statusfile=out/'MEDIA_WATCH.json';lock=out/'MEDIA_WATCH.lock';fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);started=time.monotonic();done={};prepared={};rejected={};last_state=None


 try:


  os.write(fd,str(os.getpid()).encode());os.fsync(fd)


  if statusfile.exists():


   previous=load(statusfile);require(previous.get('status') not in ('FAILED','RUNNING_ENCODING'),'Previous watcher needs explicit reconciliation');done=previous.get('completed',{});prepared=previous.get('prepared',{})


  def state(status,**extra):


   nonlocal last_state


   d={'status':status,'completed':done,'prepared':prepared,'rejected':rejected,'elapsed_seconds':time.monotonic()-started,**extra};fingerprint=json.dumps({k:v for k,v in d.items() if k!='elapsed_seconds'},sort_keys=True)


   if fingerprint!=last_state:jsave(statusfile,d);last_state=fingerprint


  while len(done)<3:
   # A previous authorized preparation may still be finishing after a reanchor.
   # Preserve its inputs until its stage lock is released; never overlap jobs.
   existing_locks=list((out/'.pipeline').glob('*.lock'))
   if existing_locks:
    require(time.monotonic()-started<args.watch_timeout,'Waiting for previous media stage timed out')
    state('WAITING_EXISTING_STAGE',stage_locks=[str(p) for p in existing_locks]);time.sleep(max(2,args.poll_seconds));continue


   require(time.monotonic()-started<args.watch_timeout,'Watcher timeout; no pending encoding was retried')


   audio_ready=False;audio=root/'audio/NARRATION_BUILD.json'


   if audio.exists():


    try:b=load(audio);audio_ready=b.get('status')=='COMPLETED' and b.get('tts_inflight') is False and not b.get('pending') and all(b.get('reports',{}).get('film'+str(f),{}).get('status')=='AUDIO_MEASURED' for f in (1,2))


    except (OSError,ValueError):pass


   candidate=None


   for kind in ('film1','film2','loop'):


    if kind in done or (kind!='loop' and kind in prepared and not audio_ready):continue


    valid=[]


    for p in sorted((root/'cinema/render/jobs').glob(kind+'_*.json')):


     if '.progress.' in p.name or '.bak_' in p.name:continue


     try:


      film=int(kind[-1]) if kind!='loop' else None;j,raw,d,duration=read_job(root,p,film)


      require(duration==({1:224,2:360}[film] if film else 16),'Unexpected authorized duration');valid.append((p,d))


     except (OSError,ValueError,KeyError) as exc:rejected[str(p)]=str(exc)


    require(len(valid)<=1,'Multiple current final jobs; coordinator must select explicitly')


    if valid:candidate=(kind,*valid[0]);break


   if candidate:


    kind,p,d=candidate;action='loop' if kind=='loop' else ('film' if audio_ready else 'prepare-video');state('RUNNING_ENCODING',kind=kind,action=action,job=pin(p));command=[sys.executable,'-B','-X','utf8',str(Path(__file__)),action,'--root',str(root),'--ffmpeg',str(args.ffmpeg),'--job',str(p),'--job-ready']


    if kind!='loop':command+=['--film',kind[-1],'--audio-dir',str(args.audio_dir or root/'audio')]


    if args.no_720:command+=['--no-720']


    if args.vp9_pt:command+=['--vp9-pt']


    log=out/('WATCH_'+kind+'_'+stamp()+'.log');start=time.monotonic()


    with log.open('xb') as stream:result=subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))


    require(result.returncode==0,'Encoding failed; preserve logs, no automatic retry: '+str(log));record={'job':pin(p),'log':pin(log),'elapsed_seconds':time.monotonic()-start};(prepared if action=='prepare-video' else done)[kind]=record;state('WAITING_INPUTS',audio_ready=audio_ready)


   else:state('WAITING_INPUTS',audio_ready=audio_ready);time.sleep(max(2,args.poll_seconds))


  state('VALIDATING');result=validate_delivery(Pipeline(root,args.ffmpeg),args);state('COMPLETE',validation=result);return {'status':'COMPLETE','completed':done,'prepared':prepared,'validation':result}


 except Exception as exc:


  jsave(statusfile,{'status':'FAILED','completed':done,'prepared':prepared,'rejected':rejected,'elapsed_seconds':time.monotonic()-started,'error':str(exc)});raise


 finally:os.close(fd);lock.unlink()





def main():


 p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter);p.add_argument('action',choices=['discover','captions','assets','film','loop','self-test','watch','validate','prepare-video','mux-h264']);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--ffmpeg',type=Path,default=FF_DEFAULT);p.add_argument('--audio-dir',type=Path);p.add_argument('--audio-map',type=Path);p.add_argument('--film',type=int,choices=[1,2]);p.add_argument('--job',type=Path);p.add_argument('--job-ready',action='store_true');p.add_argument('--watch-timeout',type=float,default=14400);p.add_argument('--poll-seconds',type=float,default=10);p.add_argument('--no-720',action='store_true');p.add_argument('--vp9-pt',action='store_true');p.add_argument('--poster1-key',default='gravity');p.add_argument('--poster2-key',default='review_240');p.add_argument('--og-key',default='review_0');a=p.parse_args();a.root=a.root.resolve()


 if a.action=='self-test':self_test();return


 if a.audio_dir and not a.audio_dir.is_absolute():a.audio_dir=a.root/a.audio_dir


 if a.audio_map and not a.audio_map.is_absolute():a.audio_map=a.root/a.audio_map


 if a.job and not a.job.is_absolute():a.job=a.root/a.job


 if a.action=='discover':


  result={'status':'DISCOVERY_ONLY_NO_ENCODING','jobs':[str(x) for x in sorted((a.root/'cinema/render/jobs').glob('*.json')) if '.progress.' not in x.name],'audio_contract':{'film1':{'en':'film1/en.wav','pt-BR':'film1/pt-BR.wav'},'film2':{'en':'film2/en.wav','pt-BR':'film2/pt-BR.wav'}},'audio_found':[str(x) for x in sorted(a.audio_dir.rglob('*.wav'))] if a.audio_dir and a.audio_dir.exists() else [],'explicit_job_required':True};print(json.dumps(result,ensure_ascii=False,indent=2));return


 if a.action=='captions':require(a.film,'--film required');print(json.dumps(captions(a.root,a.film),ensure_ascii=False,indent=2));return


 require(a.job_ready,'No encoding/image work before coordinator jobready: explicit --job-ready required');require(a.ffmpeg.is_file(),'FFmpeg executable missing');pipe=Pipeline(a.root,a.ffmpeg)


 if a.action=='watch':result=watch_jobs(a);


 elif a.action=='validate':result=validate_delivery(pipe,a)


 elif a.action=='assets':result=prepare_assets(pipe,a)


 elif a.action=='prepare-video':require(a.film and a.job,'--film and --job required');result=prepare_video(pipe,a)
 elif a.action in ('film','mux-h264'):require(a.film and a.job and a.audio_dir,'--film, --job and --audio-dir required');result=encode_film(pipe,a)


 else:require(a.job,'--job required');result=encode_loop(pipe,a)


 print(json.dumps({'status':'COMPLETE','action':a.action,'result':result},ensure_ascii=False,indent=2))


if __name__=='__main__':


 try:main()


 except Exception as e:print(json.dumps({'status':'FAILED','error':str(e)},ensure_ascii=False),file=sys.stderr);sys.exit(1)


