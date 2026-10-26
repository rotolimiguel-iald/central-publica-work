from pathlib import Path
import hashlib, json, os, time

root=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
changes={
 'cinema/cinema-scene.mjs':[
  ('export function sceneState(phase,data){','export function sceneState(phase,data,{closingCollapse=null}={}){'),
  ('const sample=mix(rows[i].area,rows[j].area,x-i),area=mix(sample,1,ret),depth=', 'const collapse=closingCollapse===null?ret:clamp(closingCollapse),sample=mix(rows[i].area,rows[j].area,x-i),area=mix(sample,1,ret),depth='),
  ('return {phase:p,ret,focus,area,','return {phase:p,ret,collapse,focus,area,'),
  ('*(1-.985*ret),sheet:ramp(p,58,82)*(1-ret)', '*(1-.985*collapse),sheet:ramp(p,58,82)*(1-collapse)'),
  ('render(phase,time=phase,{loop=false,jProgress=null}={}){','render(phase,time=phase,{loop=false,jProgress=null,closingCollapse=null}={}){'),
  ('sceneState(phase,this.data),angle=', 'sceneState(phase,this.data,{closingCollapse}),angle='),
  ('transition:this.state.ret>0','transition:this.state.collapse>0'),
 ],
 'cinema/cinema-composition.mjs':[
  ('{loop,jProgress:loop?0:s.jProgress}', '{loop,jProgress:loop?0:s.jProgress,closingCollapse:loop?0:ramp(time,s.total-3,s.total)}'),
  ('transition:s.transition||s.phase>169','transition:s.transition'),
 ],
 'make_v7.py':[
  ('import argparse, datetime, hashlib, json, os, re, subprocess, sys, time','import argparse, datetime, hashlib, json, math, os, re, subprocess, sys, time'),
  ("                if abs(float(measure['input_i'])+16)>1: raise ValueError('Narration loudness outside target')", "                loudness=float(measure['input_i'])\n                if not math.isfinite(loudness) or abs(loudness+16)>1: raise ValueError('Narration loudness outside target')"),
 ],
}
records=[]
for relative,replacements in changes.items():
 p=root/relative; raw=p.read_bytes(); text=raw.decode('utf-8').replace('\r\n','\n')
 for old,new in replacements:
  assert text.count(old)==1,(relative,old,text.count(old))
  text=text.replace(old,new)
 if p.suffix=='.py':compile(text,str(p),'exec')
 out=text.encode('utf-8');backup=p.with_name(p.name+'.bak_'+str(time.time_ns()));backup.write_bytes(raw)
 temp=p.with_name(p.name+'.tmp');temp.write_bytes(out);assert temp.stat().st_size==len(out);os.replace(temp,p)
 records.append({'file':str(p),'backup':str(backup),'before':hashlib.sha256(raw).hexdigest(),'sha256':hashlib.sha256(out).hexdigest()})
receipt={'scope':'Hold full-width return geometry through the explanation; collapse only the final three seconds. Reject nonfinite audio measurements. Prior renders retained.','files':records}
(Path(__file__).parent/'CLOSING_FINITE_PATCH.json').write_bytes((json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps(receipt,ensure_ascii=False))
