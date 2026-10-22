from pathlib import Path
import json,hashlib,sqlite3,psutil,datetime
W=Path(__file__).resolve().parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
files=['iald_nucleo_fixo.json','iald_jev_control.py','iald_auto_router.py','iald_app_memory.py','iald_activity_operations.py','iald_chat_jobs.py','IALD_Kernel_v5.txt']
out={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[],'jobs':[],'web':[]}
for name in files:
 p=R/name;raw=p.read_bytes();out['files'].append({'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
path=R/'.iald_runtime/chat_jobs/jobs.sqlite3'
with sqlite3.connect(path.as_uri()+'?mode=ro',uri=True) as c:
 for row in c.execute('select id,conversation_id,status,seq,error from jobs order by created desc limit 8'):
  out['jobs'].append(dict(zip(['id','conversation_id','status','seq','error'],row)))
for p in psutil.process_iter(['name']):
 if (p.info['name'] or '').lower()=='python.exe':
  try:
   if any(a.lower().endswith('iald_web_server.py') for a in p.cmdline()):out['web'].append({'pid':p.pid,'created':p.create_time(),'parent':p.ppid()})
  except psutil.NoSuchProcess:pass
with (W/'BASELINE_R1.json').open('x',encoding='utf-8') as f:json.dump(out,f,ensure_ascii=False,indent=2)
print(json.dumps({'files':len(out['files']),'web':out['web'],'latest_status':out['jobs'][0]['status']}))
