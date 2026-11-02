"""Reviewer poll (read-only): mission_step.py project every 60 s until verify is review_pending (max ~40 min)."""
import subprocess,json,time,sys
W=r'C:\IALD\Central de Patentes\work\iald_v404_20261029'
last=None
for i in range(40):
    try:
        d=json.loads(subprocess.check_output([r'C:\Python314\python.exe','-B','-X','utf8',W+r'\mission_step.py','project'],cwd=W))
        act={t['id']:(t['status'],bool(t.get('lease'))) for t in d['active']}
    except Exception as e:
        act={'error':str(e)[:100]}
    if act!=last:
        print(time.strftime('%H:%M:%S'),'rev',d.get('revision') if isinstance(d,dict) else None,act,flush=True);last=act
    if act.get('verify',(None,))[0]=='review_pending':
        print('VERIFY_REVIEW_PENDING',flush=True);sys.exit(0)
    time.sleep(60)
print('TIMEOUT',flush=True)
