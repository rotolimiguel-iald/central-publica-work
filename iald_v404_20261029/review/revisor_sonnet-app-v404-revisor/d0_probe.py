"""Reviewer probe (read-only): processes, listeners and a stat-only sweep to calibrate the deploy review."""
import os,sys,json,time,datetime
from pathlib import Path
import psutil
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');R=Path(r'C:\IALD\projetos_pyhton\IALD')
rs=json.loads((W/'restart.json').read_bytes());mt=(W/'maintenance.json').stat().st_mtime
print('maintenance.json mtime',datetime.datetime.fromtimestamp(mt).isoformat(),'supervisor_created',datetime.datetime.fromtimestamp(rs['supervisor_created']).isoformat())
for p in psutil.process_iter(['pid','name','ppid','create_time','status']):
    try:
        n=(p.info['name'] or '').lower()
        if n in('python.exe','pythonw.exe','powershell.exe','pwsh.exe','llama-server.exe') or 'llama' in n:
            cl=' '.join(p.cmdline())[:170]
            if any(k in cl.lower() for k in('iald','llama','start_iald','bancada','web','supervis')):
                print(p.info['pid'],p.info['ppid'],n,datetime.datetime.fromtimestamp(p.info['create_time']).strftime('%m-%d %H:%M:%S'),p.info['status'],cl)
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
                        if max(st.st_mtime,st.st_ctime)>=mt-120:changed.append((e.path,st.st_size))
                except OSError:pass
    except OSError:pass
walk(str(R))
print('files seen',n,'sweep seconds',round(time.time()-t0,1),'changed since window-120s:',len(changed))
plan={r['destination'] for r in json.loads((W/'install_plan.json').read_bytes())['files']}
dep=json.loads((W/'deployment.json').read_bytes());baks=set(dep['backups'].values())
rest=[c for c in changed if c[0] not in plan and c[0] not in baks]
print('not plan/backup:',len(rest))
for p,s in sorted(rest):print('  ',p.replace(str(R),'R'),s)
