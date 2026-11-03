"""Exploratory (read-only, stat only, nothing opened): where do accounts / consents / wallet / activity live, and are they older than the window?"""
import os,re,datetime
from pathlib import Path
R=Path(r'C:\IALD\projetos_pyhton\IALD');W=Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
f=lambda t:datetime.datetime.fromtimestamp(t).strftime('%m-%d %H:%M:%S')
tm=(W/'maintenance.json').stat().st_mtime
PAT=re.compile(r'user|usuario|account|conta|consent|session|sess|auth|token|credential|secret|wallet|carteira|ledger|jobs|activity_|atividade|\.sqlite|\.db$|-wal$|-shm$',re.I)
SKIP=('iald-app','node_modules','__pycache__','canonical_releases','.git')
hits=[]
def walk(d,depth):
    try:
        with os.scandir(d) as it:
            for e in it:
                try:
                    if e.is_dir(follow_symlinks=False):
                        if e.name in SKIP or e.name.startswith('kernel-'):continue
                        if depth<4:walk(e.path,depth+1)
                    elif PAT.search(e.name) and not e.name.endswith(('.py','.pyc','.lean','.md','.tex','.bak')) and '.bak_' not in e.name:
                        st=e.stat(follow_symlinks=False);hits.append((e.path,st.st_size,st.st_mtime))
                except OSError:pass
    except OSError:pass
walk(str(R),0)
print('stores (stat only):',len(hits),'| window start',f(tm))
for p,s,m in sorted(hits,key=lambda x:x[0].lower()):print(' ',f(m),'%10d'%s,('AFTER' if m>=tm-120 else 'before'),p.replace(str(R),'R'))
for extra in (r'C:\IALD\bank\tglc_ledger.json',):
    try:
        st=os.stat(extra);print(' ',f(st.st_mtime),'%10d'%st.st_size,('AFTER' if st.st_mtime>=tm-120 else 'before'),extra,'(outside R, stat only)')
    except OSError as e:print(' ',extra,'stat failed',e)
