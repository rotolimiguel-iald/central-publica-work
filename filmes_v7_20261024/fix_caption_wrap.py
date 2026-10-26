from pathlib import Path
import hashlib, json, datetime
base=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7\web')
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
old="""function captions(){for(const t of video.textTracks){
 if(t.kind==='subtitles')for(const cue of t.cues??[]){cue.snapToLines=false;cue.line=55;cue.position=50;cue.size=92;cue.align='center';}
 t.mode=t.kind==='subtitles'&&t.language===$('#language').value?'showing':'disabled';
}}"""
new="""const originalCaptions=new WeakMap(),captionMeasure=document.createElement('canvas').getContext('2d');
// Explicit line breaks avoid native cue clipping after custom font sizing.
function wrapCaption(value,width){
 const lines=[];let line='';
 for(const character of value){
  if(character==='\\n'){lines.push(line);line='';continue;}
  if(line&&captionMeasure.measureText(line+character).width>width){
   const space=line.lastIndexOf(' ');
   if(space>0){lines.push(line.slice(0,space));line=line.slice(space+1)+character;}
   else{lines.push(line);line=character;}
  }else line+=character;
 }
 if(line)lines.push(line);return lines.join('\\n');
}
function captions(){
 const width=Math.max(100,video.getBoundingClientRect().width*.86);
 captionMeasure.font=`${Math.min(28,Math.max(10,innerWidth*.017))}px Outfit`;
 for(const t of video.textTracks){
  if(t.kind==='subtitles')for(const cue of t.cues??[]){
   if(!originalCaptions.has(cue))originalCaptions.set(cue,cue.text);
   cue.text=wrapCaption(originalCaptions.get(cue),width);
   cue.snapToLines=false;cue.line=cue.text.split('\\n').length>3?32:48;
   cue.position=50;cue.size=92;cue.align='center';
  }
  t.mode=t.kind==='subtitles'&&t.language===$('#language').value?'showing':'disabled';
 }
}
const captionResize=new ResizeObserver(captions);captionResize.observe(video);
document.fonts.ready.then(captions);
document.addEventListener('fullscreenchange',captions);"""
changes={}
p=base/'filmes.mjs';raw=p.read_bytes();s=raw.decode('utf-8');assert old in s
s=s.replace(old,new).replace("cancelAnimationFrame(raf);replayController?.destroy?.();","cancelAnimationFrame(raf);captionResize.disconnect();replayController?.destroy?.();")
changes[p]=(raw,s.encode('utf-8'))
p=base/'filmes.css';raw=p.read_bytes();s=raw.decode('utf-8');assert 'clamp(14px,1.7vw,28px)' in s
changes[p]=(raw,s.replace('clamp(14px,1.7vw,28px)','clamp(10px,1.7vw,28px)').encode('utf-8'))
out=[]
for p,(before,after) in changes.items():
 bak=p.with_name(p.name+'.bak_'+stamp);bak.write_bytes(before)
 tmp=p.with_name(p.name+'.tmp_'+stamp);tmp.write_bytes(after);assert tmp.read_bytes()==after;tmp.replace(p)
 out.append({'path':str(p),'backup':str(bak),'before_sha256':hashlib.sha256(before).hexdigest(),'sha256':hashlib.sha256(after).hexdigest()})
receipt={'status':'PATCHED_AWAITING_UI','changes':out,'scope':'Player typography only; original VTT, audio and frozen render sources unchanged.'}
Path(__file__).with_name('CAPTION_WRAP_PATCH.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps(receipt))
