from pathlib import Path
import ast, hashlib, json, os, time, sys

W=Path(__file__).resolve().parent
V=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
sys.path.insert(0,str(W.parent))
import mission
project=mission.project()
task=next(t for t in project['projection']['active']+project['projection']['settled'] if t['id']=='ADENDO_A')
check=mission.call({'operation':'check',**mission.current('codex-video-v7'),'task_id':'ADENDO_A','lease_id':task['lease']['id'],'max_chars':100000})
assert check['ready'],check
seal=json.loads((V.parent.parent/'Nós/um_absoluto_selo.json').read_bytes())
assert seal['um_version']=='v400'
p=V/'make_v7.py'
raw=p.read_bytes()
text=raw.decode('utf-8')
changes=[
 ("{'version': version,", "{'source': version, 'source_sha256': pins['um.py'], 'version': version,"),
 ("{'version': seal['um_version'], 'elapsed_seconds'", "{'source': seal['um_version'], 'source_sha256': seal['sha256']['um.py'], 'version': seal['um_version'], 'elapsed_seconds'"),
 ("{'schema':'tgl.render.v7','version':h['seal_version'],", "{'schema':'tgl.render.v7','source':h['seal_version'],'version':h['seal_version'],"),
 ("{'schema':'tgl.public-delivery.v7','version':h['seal_version'],", "{'schema':'tgl.public-delivery.v7','source':h['seal_version'],'version':h['seal_version'],"),
 ("{'schema':'tgl.delivery-pointer.v7','delivery':'delivery_v7/PUBLIC_DELIVERY_V7.json',", "{'schema':'tgl.delivery-pointer.v7','source':h['seal_version'],'source_sha256':h['seal_pin'],'delivery':'delivery_v7/PUBLIC_DELIVERY_V7.json',"),
]
for old,new in changes:
    assert text.count(old)==1, old
    text=text.replace(old,new)
ast.parse(text)
new=text.encode('utf-8')
backup=p.with_name(p.name+'.bak_'+str(time.time_ns()));backup.write_bytes(raw)
assert backup.read_bytes()==raw
temp=p.with_name(p.name+'.tmp_adendo_a');temp.write_bytes(new)
assert len(new)>0 and temp.read_bytes()==new
os.replace(temp,p)
receipt={'source':seal['um_version'],'source_sha256':seal['sha256']['um.py'],
 'scope':'Add explicit source version/hash to current build receipts and delivery pointer; no rendering, scene, numeric or narration change.',
 'file':str(p),'previous_sha256':hashlib.sha256(raw).hexdigest(),'sha256':hashlib.sha256(new).hexdigest(),'backup':str(backup),'syntax':'PASS'}
(W/'BUILDER_METADATA_PATCH.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
