from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parent
V=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def diff(a,b,path=''):
 if isinstance(a,dict) and isinstance(b,dict):
  return [d for k in a.keys() & b.keys() for d in diff(a[k],b[k],path+'/'+k)]
 if isinstance(a,list) and isinstance(b,list):
  if len(a)!=len(b):return [{'path':path,'kind':'length','a':len(a),'b':len(b)}]
  return [d for i,(x,y) in enumerate(zip(a,b)) for d in diff(x,y,path+'/'+str(i))]
 if type(a) in (int,float,bool) or type(b) in (int,float,bool):
  return [] if type(a)==type(b) and a==b else [{'path':path,'a':a,'b':b}]
 return []
rows=[]
for name in ['hud.json','frames.json','scene.json','PROVENANCE_PUBLIC.json','film1.json','film2.json']:
 before=W/'baseline_v399/data'/name;after=V/'data'/name
 differences=diff(json.loads(before.read_bytes()),json.loads(after.read_bytes()))
 allowed={'/sources/um.py/bytes','/sources/um_absoluto.json/bytes','/sources/um_absoluto_selo.json/bytes'} if name=='PROVENANCE_PUBLIC.json' else set()
 assert all(d['path'] in allowed for d in differences),differences
 rows.append({'path':'data/'+name,'baseline_sha256':sha(before),'current_sha256':sha(after),'differences':differences})
ready=json.loads((W/'DATA_READY.json').read_bytes())
for p in ready['data_pins']+ready['source_pins']+[ready['seal'],ready['numeric_comparison']]:
 assert sha(Path(p['path']))==p['sha256'],p['path']
prov=json.loads((V/'data/PROVENANCE_PUBLIC.json').read_bytes())
assert prov['anchors_all_ok'] and len(prov['anchors'])>=64
result={'source':ready['source'],'source_sha256':ready['source_sha256'],'status':'PASS_WITH_SCOPE','actor':'codex-video-v7','method':'Independent recursive exact typed comparison of every numeric/boolean leaf in common data fields; list lengths must match. Three source-file byte counts are the only allowed differences. Agent full-field comparison also inspected separately.','files':rows,'data_ready_sha256':sha(W/'DATA_READY.json'),'anchors':len(prov['anchors']),'anchors_all_ok':True,'limitations':['Read-only comparison, no new Lean compilation or physical test.','Does not assess visual rendering or auditory naturalness.']}
p=W/'PARENT_NUMERIC_REVIEW.json';assert not p.exists();p.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':result['status'],'files':len(rows),'anchors':result['anchors']}))
