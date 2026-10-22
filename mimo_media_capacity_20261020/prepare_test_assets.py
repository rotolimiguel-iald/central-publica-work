from pathlib import Path
import hashlib,json,wave,math,array,subprocess
import task
W=task.W;D=W/'test_assets';D.mkdir(exist_ok=True)
task.project();task.check('implementation')
a=D/'tone_120s.wav';v=D/'red_30s.mp4'
assert not a.exists() and not v.exists()
samples=array.array('h',(int(6000*math.sin(2*math.pi*440*i/8000)) for i in range(8000)))
with wave.open(str(a),'wb') as f:
 f.setnchannels(1);f.setsampwidth(2);f.setframerate(8000)
 for _ in range(120):f.writeframesraw(samples.tobytes())
ff=Path(r'C:\IALD\Central de Patentes\work\mimo26_upgrade_20261020\media_dependency\ffmpeg.exe')
prior=json.loads(Path(r'C:\IALD\Central de Patentes\work\mimo26_upgrade_20261020\media_dependency\RECEIPT.json').read_bytes())
sha=hashlib.sha256(ff.read_bytes()).hexdigest()
assert sha==next(x['sha256'] for x in prior['files'] if x['name']=='ffmpeg.exe'), 'Official downloaded binary receipt mismatch'
subprocess.run([str(ff),'-v','error','-f','lavfi','-i','color=c=red:s=128x128:r=2','-t','30','-an','-c:v','libx264','-pix_fmt','yuv420p',str(v)],check=True,capture_output=True,timeout=60,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
task.new('TEST_ASSETS.json',{'synthetic_only':True,'files':[{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (a,v)],'purpose':'Representative files exceed previous duration/size limits; offline tests must separately verify maximum boundaries','data_types_previously_authorized':'Public science v394, tone audio, solid red video; no personal audio or video','test_budget_reference':'Prior explicit MiMo/JEV test authorization up toUSD1; previous measured estimate USD0.0706696812; no new model requests from this script'})
