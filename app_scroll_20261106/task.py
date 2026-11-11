"""Task-scoped ACOM client; running this file only reads the projection."""
import hashlib,json,subprocess,sys,uuid
from pathlib import Path
W=Path(__file__).resolve().parent
REF=W/'SESSION_REFERENCE.json'
OWNER='codex-app-scroll-01a094df'
UNIT='F9.APP_SCROLL_20261106'
PY=r'C:\Python314\python.exe'
def pin(p):
 p=Path(p);return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(name,obj):
 raw=obj if isinstance(obj,bytes) else json.dumps(obj,ensure_ascii=False,indent=2).encode()
 with (W/name).open('xb') as f:f.write(raw)
def call(payload,mission=True):
 p=subprocess.run([PY,'-B','-X','utf8',str(Path(r'C:\IALD\MEMORIA_IALD')/('mission_cli.py' if mission else 'session_memory.py'))],input=json.dumps(payload,ensure_ascii=False).encode(),capture_output=True)
 d=json.loads(p.stdout)
 if p.returncode or not d.get('ok'):raise RuntimeError(d)
 return d['result']
def project():return call({'operation':'project','reference':str(REF),'max_chars':100000})
def act(op,actor=OWNER,**kw):
 p=project();return call({'operation':op,'reference':str(REF),'actor':{'id':actor,'kind':'agent'},'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],**kw})
def check(name):
 p=project();t=next(t for t in p['projection']['active'] if t['id']==name)
 return call({'operation':'check','reference':str(REF),'task_id':name,'lease_id':t['lease']['id'],'actor':{'id':OWNER,'kind':'agent'},'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256']})
def init():
 if REF.exists():raise RuntimeError('Reference exists; project instead')
 source=pin(W/'ORIGINAL.txt')
 request_id=str(uuid.uuid5(uuid.NAMESPACE_URL,source['path']+'#'+source['sha256']))
 r=call({'operation':'init','objective_file':source['path'],'objective_sha256':source['sha256'],'request_id':request_id,'scope':{'house':'IALD','principal':'luiz'},'actor':{'id':OWNER,'kind':'agent'},'write_reference':str(REF),'constraints':{'unit':UNIT,'scope':'Client scroll repair and coordinated mobile release; no provider inference or science changes'}},False)
 save('INIT.json',r)
 p=call({'operation':'project','reference':str(REF)},False)
 r=call({'operation':'configure','reference':str(REF),'actor':{'id':OWNER,'kind':'agent'},'expected_revision':p['receipt']['revision'],'event_id':'app-scroll-configure','requirements':[
  {'id':'fix','criterion':'Reproduce unwanted scroll during and after streaming, fix user-controlled following in staged shared client, verify public/private chat with meaningful fixtures. Preserve existing features and science.','depends_on':[]},
  {'id':'deploy','criterion':'Independent review before byte-backed controlled static deployment to affected client surfaces; preserve runtime and scientific sources; verify installed bytes.','depends_on':['fix']},
  {'id':'mobile','criterion':'Synchronize affected iOS/Android assets and publish through existing authorized channels; report actual TestFlight both groups and Android availability, with blockers explicit. No physical installation claim.','depends_on':['deploy']}], 'sources':[source]})
 save('CONFIGURED.json',r)
 print(json.dumps({'reference':str(REF),'revision':r['receipt']['revision']}))
if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='init':init()
 else:
  p=project();print(json.dumps({'revision':p['receipt']['revision'],'active':p['projection']['active']},ensure_ascii=False))
