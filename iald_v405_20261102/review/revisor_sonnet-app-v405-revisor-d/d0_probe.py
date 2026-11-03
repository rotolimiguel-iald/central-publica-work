"""Reviewer probe (read-only) for the v405 DEPLOY: processes, listeners and a stat-only sweep (no file opened).
Actor label: sonnet-app-v405-revisor-d. Adapted from the v404 reviewer probe; paths and reporting extended
(per-file mtimes of everything that is neither plan destination nor backup)."""
import os,sys,json,time,datetime
from pathlib import Path
import psutil
W=Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102');R=Path(r'C:\IALD\projetos_pyhton\IALD')
f=lambda t:datetime.datetime.fromtimestamp(t).strftime('%m-%d %H:%M:%S')
rs=json.loads((W/'restart.json').read_bytes());mt=(W/'maintenance.json').stat().st_mtime;mr=(W/'restart.json').stat().st_mtime
print('now',datetime.datetime.now().isoformat(timespec='seconds'))
print('maintenance.json mtime',datetime.datetime.fromtimestamp(mt).isoformat(),'| restart.json mtime',datetime.datetime.fromtimestamp(mr).isoformat(),'| supervisor_created',datetime.datetime.fromtimestamp(rs['supervisor_created']).isoformat())
print('processes (python/powershell/llama with iald|llama|start_iald|bancada|web|supervis in cmdline):')
for p in psutil.process_iter(['pid','name','ppid','create_time','status']):
    try:
        n=(p.info['name'] or '').lower()
        if n in('python.exe','pythonw.exe','powershell.exe','pwsh.exe','llama-server.exe') or 'llama' in n:
            cl=' '.join(p.cmdline())[:170]
            if any(k in cl.lower() for k in('iald','llama','start_iald','bancada','web','supervis')):
                print(' ',p.info['pid'],p.info['ppid'],n,f(p.info['create_time']),p.info['status'],cl)
    except Exception as e:pass
print('listeners:')
for c in psutil.net_connections(kind='tcp'):
    if c.status==psutil.CONN_LISTEN and c.laddr.port in(8081,8082,18765,18766,18777):print(' ',c.laddr.port,c.pid)
t0=time.time();changed=[];n=0
def walk(d):
    global n
    try:
        with os.scandir(d) as it:
            for e in it:
                try:
                    if e.is_dir(follow_symlinks=False):walk(e.path)
                    else:
                        n+=1;st=e.stat(follow_symlinks=False)
                        if max(st.st_mtime,st.st_ctime)>=mt-120:changed.append((e.path,st.st_size,st.st_mtime,st.st_ctime))
                except OSError:pass
    except OSError:pass
walk(str(R))
print('files seen',n,'sweep seconds',round(time.time()-t0,1),'changed (mtime|ctime) since window-120s:',len(changed))
plan={r['destination'] for r in json.loads((W/'install_plan.json').read_bytes())['files']}
dep=json.loads((W/'deployment.json').read_bytes());baks=set(dep['backups'].values())
rest=[c for c in changed if c[0] not in plan and c[0] not in baks]
print('in plan:',sum(1 for c in changed if c[0] in plan),'| backups:',sum(1 for c in changed if c[0] in baks),'| not plan/backup:',len(rest))
for p,s,m,c in sorted(rest):print('  mtime',f(m),'ctime',f(c),s,p.replace(str(R),'R'))
