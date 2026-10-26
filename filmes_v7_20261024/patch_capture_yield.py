from pathlib import Path
import os,time,hashlib,json
p=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7\cinema\studio.mjs')
raw=p.read_bytes();text=raw.decode('utf-8')
old='status.textContent=JSON.stringify({kind,frame:i+1,total,encoded,elapsed_s:(performance.now()-started)/1000});await new Promise(requestAnimationFrame);'
new='status.textContent=JSON.stringify({kind,frame:i+1,total,encoded,elapsed_s:(performance.now()-started)/1000});await new Promise(resolve=>{const channel=new MessageChannel();channel.port1.onmessage=()=>{channel.port1.close();channel.port2.close();resolve();};channel.port2.postMessage(null);});'
assert text.count(old)==1
out=text.replace(old,new).encode('utf-8');b=p.with_name(p.name+'.bak_'+str(time.time_ns()));b.write_bytes(raw)
t=p.with_name(p.name+'.tmp');t.write_bytes(out);assert t.stat().st_size==len(out);os.replace(t,p)
receipt={'file':str(p),'backup':str(b),'sha256':hashlib.sha256(out).hexdigest(),'scope':'Yield between encoding batches via posted message rather than display refresh; fixed frame times and explicit encode/flush unchanged. No frame skipping. Performance improvement unmeasured until capture.'}
(Path(__file__).parent/'CAPTURE_YIELD_PATCH.json').write_bytes(json.dumps(receipt,indent=2).encode())
print(json.dumps(receipt))
