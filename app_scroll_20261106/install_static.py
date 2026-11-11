"""Plan or install the reviewed static client release. No services are restarted."""
import json,sys,os,hashlib,datetime
from pathlib import Path
from task import W, pin, save, check
R=Path(r'C:\IALD\projetos_pyhton\IALD')
def sha(p):return pin(p)['sha256']
def plan():
 mobile=json.loads((W/'mobile/PLAN.json').read_bytes())
 rows=list(mobile['rows'])
 for name in ('iald.js','owner_office.js'):
  rows.append({'source':str(W/'stage'/name),'target':str(R/'app'/name),'old':sha(W/'baseline'/name),'new':sha(W/'stage'/name)})
 previous=Path(r'C:\IALD\Central de Patentes\work\iald_v409_20261106')
 previous_plan=json.loads((previous/'install_plan.json').read_bytes())
 # Use the previously installed scientific plan only to enumerate targets; pin
 # their current bytes, never assume a remembered science version/hash.
 science_rows=previous_plan.get('files',previous_plan.get('rows',[]))
 protected=[]
 for row in science_rows:
  p=Path(row.get('target',row.get('destination','')))
  if p.is_file() and p.is_relative_to(R):protected.append(pin(p))
 for row in json.loads((previous/'PRESERVATION_BASELINE.json').read_bytes())['files']:
  p=Path(row['path'])
  if p.suffix=='.py':protected.append(pin(p))
 assert len(protected)>1000, len(protected)
 save('INSTALL_PLAN.json',{'rows':rows,'mobile_plan':pin(W/'mobile/PLAN.json'),'preserve':protected,'restart':False})
 print(json.dumps({'targets':len(rows),'protected':len(protected)}))
def install(review_name):
 check('deploy')
 p=W/'INSTALL_PLAN.json';plan=json.loads(p.read_bytes());review_path=W/review_name
 review=json.loads(review_path.read_bytes())
 assert review['status']=='PASS' and review['install_plan_sha256']==sha(p)
 assert review['reviewer']!='codex-app-scroll-01a094df'
 for r in plan['rows']:
  dest=Path(r['target']);src=Path(r['source'])
  assert dest.resolve()==dest and src.resolve()==src and dest.is_relative_to(R) and src.is_relative_to(W)
  assert sha(dest)==r['old'] and sha(src)==r['new']
 for r in plan['preserve']:assert sha(r['path'])==r['sha256'],r['path']
 save('INSTALL_INTENT.json',{'plan':pin(p),'review':pin(review_path)})
 stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');done=[]
 try:
  for r in plan['rows']:
   dest=Path(r['target']);backup=dest.with_name(dest.name+'.bak_'+stamp)
   with backup.open('xb') as f:f.write(dest.read_bytes());f.flush();os.fsync(f.fileno())
   assert sha(backup)==r['old']
   temporary=dest.with_name(dest.name+'.scroll_'+stamp+'.tmp')
   raw=Path(r['source']).read_bytes()
   with temporary.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
   assert sha(temporary)==r['new'] and len(raw)>0 and sha(dest)==r['old']
   os.replace(temporary,dest);done.append({**r,'backup':str(backup)})
   assert sha(dest)==r['new']
  for r in plan['preserve']:assert sha(r['path'])==r['sha256'],r['path']
 except BaseException:
  for r in reversed(done):
   dest=Path(r['target']);tmp=dest.with_name(dest.name+'.rollback_'+stamp)
   with tmp.open('xb') as f:f.write(Path(r['backup']).read_bytes());f.flush();os.fsync(f.fileno())
   assert sha(tmp)==r['old'];os.replace(tmp,dest)
  save('INSTALL_ROLLBACK.json',{'restored':done});raise
 save('INSTALLED.json',{'status':'PASS','files':done,'protected_count':len(plan['preserve']),'restart':False})
 print(json.dumps({'status':'PASS','files':len(done),'protected':len(plan['preserve'])}))
if __name__=='__main__':
 if sys.argv[1]=='plan':plan()
 elif sys.argv[1]=='install':install(sys.argv[2])
 else:raise ValueError('Unsupported action')
