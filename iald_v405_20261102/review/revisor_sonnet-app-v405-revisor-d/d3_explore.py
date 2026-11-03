"""Exploratory (read-only, stat only): what changed in R since the RUNTIME_BASELINE was taken (07:53), outside plan/backups;
and which stores that look like accounts/wallet/consents/activity exist, with their mtimes (names only, nothing opened)."""
import os,json,datetime,re,collections
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102');R=Path(r'C:\IALD\projetos_pyhton\IALD')
f=lambda t:datetime.datetime.fromtimestamp(t).strftime('%m-%d %H:%M:%S')
cut=(W/'app/RUNTIME_BASELINE.json').stat().st_mtime-600   # 10 min before the baseline file
tm=(W/'maintenance.json').stat().st_mtime;tr=(W/'restart.json').stat().st_mtime
plan={r['destination'] for r in json.loads((W/'install_plan.json').read_bytes())['files']}
baks=set(json.loads((W/'deployment.json').read_bytes())['backups'].values())
changed=[];stores=[];n=0
PAT=re.compile(r'wallet|carteira|consent|account|conta|activity|atividade|users|usuario|jobs|histor|ledger|reserva|session|memoria|memory|fatos|verbal|access|contract|psinet|\.sqlite|\.db$|-wal$|-shm$',re.I)
def walk(d):
    global n
    try:
        with os.scandir(d) as it:
            for e in it:
                try:
                    if e.is_dir(follow_symlinks=False):walk(e.path)
                    else:
                        n+=1;st=e.stat(follow_symlinks=False)
                        if PAT.search(e.name) and not e.path.startswith(str(R/'canonical_releases')):stores.append((e.path,st.st_size,st.st_mtime,st.st_ctime))
                        if max(st.st_mtime,st.st_ctime)>=cut and e.path not in plan and e.path not in baks:changed.append((e.path,st.st_size,st.st_mtime,st.st_ctime))
                except OSError:pass
    except OSError:pass
walk(str(R))
print('files seen',n,'| cut',f(cut),'| window',f(tm),'->',f(tr))
print('changed since cut, not plan/backup:',len(changed))
for p,s,m,c in sorted(changed,key=lambda x:x[2]):print(' ',f(m),'ctime',f(c),'%9d'%s,p.replace(str(R),'R'))
print('\nstores by name pattern (stat only):',len(stores))
for p,s,m,c in sorted(stores):
    flag='IN-WINDOW' if tm-5<=m<=tr+5 else ('after-window' if m>tr+5 else '')
    print(' ',f(m),'%10d'%s,p.replace(str(R),'R'),flag)
