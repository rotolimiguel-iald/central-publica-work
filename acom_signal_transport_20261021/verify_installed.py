"""Verify exact release bytes and public authentication boundary, never call models."""
from pathlib import Path
import hashlib,json,http.client
from task import W,new,check

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

check('deployment')
plan=json.loads((W/'install_plan.json').read_bytes())
for row in plan['files']:
    assert sha(Path(row['destination']))==row['sha256']
science=json.loads((W/'SCIENCE_BASELINE.json').read_bytes())
for row in science['files']:assert sha(Path(row['path']))==row['sha256']
restart=json.loads((W/'restart.json').read_bytes());assert restart['status']=='PASS'
observed=[]
for host,port,tls in [('127.0.0.1',8082,False),('demo.iald.ia.br',443,True)]:
    for path in ['/app/iald_transport.mjs','/app/chat_wire_codec.mjs','/api/chat-jobs/session']:
        c=(http.client.HTTPSConnection if tls else http.client.HTTPConnection)(host,port,timeout=20)
        try:
            c.request('GET',path);r=c.getresponse();body=r.read(65536)
            assert r.status in (302,401), (path,r.status)
            if r.status==302:assert r.getheader('Location','').startswith('/login')
            assert b'export async function' not in body
            observed.append({'host':host,'path':path,'status':r.status,'source_not_exposed':True})
        finally:c.close()
new('INSTALLED_VERIFICATION.json',{'status':'PASS','files':len(plan['files']),'science_files':len(science['files']),'plan_sha256':sha(W/'install_plan.json'),'restart':restart,'anonymous_checks':observed,'scope':'Exact files, science and anonymous boundary; authenticated live validation separate'})
print(json.dumps({'status':'PASS','files':len(plan['files']),'science_files':len(science['files'])}))
