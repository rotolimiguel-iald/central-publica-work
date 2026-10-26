from pathlib import Path
import hashlib,json,os,sys,time
W=Path(__file__).resolve().parent
V=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
sys.path.insert(0,str(W.parent));import mission
pr=mission.project();task=next(t for t in pr['projection']['active']+pr['projection']['settled'] if t['id']=='ADENDO_A')
assert mission.call({'operation':'check',**mission.current('codex-video-v7'),'task_id':'ADENDO_A','lease_id':task['lease']['id'],'max_chars':100000})['ready']
p=V/'cinema/studio.mjs';raw=p.read_bytes();text=raw.decode('utf-8')
replacements=[
 ('version:"delivery_v7",subtitleMode:', 'version:"delivery_v7",source:data.H.seal_version,source_sha256:data.H.seal_pin,subtitleMode:'),
 ('JSON.stringify({film,time,coverage})', 'JSON.stringify({film,time,coverage,source:data.H.seal_version,source_sha256:data.H.seal_pin})'),
 ('JSON.stringify(shot)', 'JSON.stringify({...shot,source:data.H.seal_version,source_sha256:data.H.seal_pin})'),
]
for old,new in replacements:
 assert text.count(old)==1,old
 text=text.replace(old,new)
backup=p.with_name(p.name+'.bak_'+str(time.time_ns()));backup.write_bytes(raw);assert backup.read_bytes()==raw
out=text.encode('utf-8');temp=p.with_name(p.name+'.tmp_adendo');temp.write_bytes(out);assert temp.read_bytes()==out;os.replace(temp,p)
seal=json.loads((V/'source/um_absoluto_selo.json').read_bytes());assert seal['um_version']=='v400'
d={'source':seal['um_version'],'source_sha256':seal['sha256']['um.py'],'scope':'Only source identifiers in video/still receipt metadata. Rendering, optics, timing, geometry and scene text unchanged.','file':str(p),'previous_sha256':hashlib.sha256(raw).hexdigest(),'sha256':hashlib.sha256(out).hexdigest(),'backup':str(backup)}
(W/'RENDER_METADATA_PATCH.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(d,ensure_ascii=False))
