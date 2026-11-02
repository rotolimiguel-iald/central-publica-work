"""Reviewer r2: code diff of the r2 pipeline vs v402 and vs r1 (.bak = r1 state). Lists every .py/.ps1/.bat/.cmd/.sh/.js/.lean outside app/science, review/, superseded_r1/."""
import hashlib,difflib,re
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');V2=Path(r'C:\IALD\Central de Patentes\work\iald_v402_20261027')
sh=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
EXT={'.py','.ps1','.bat','.cmd','.sh','.js','.lean'}
def code(root):
    out={}
    for p in root.rglob('*'):
        if not p.is_file() or p.suffix not in EXT:continue
        rel=p.relative_to(root)
        if rel.parts[0] in('review','superseded_r1','validation') or rel.parts[:2]==('app','science') or rel.parts[:2]==('app','packages'):continue
        if '.bak_' in p.name:continue
        out[str(rel)]=p
    return out
a=code(W);b=code(V2)
print('files r2',len(a),'v402',len(b))
print('only r2:',sorted(set(a)-set(b)));print('only v402:',sorted(set(b)-set(a)))
same=[k for k in a if k in b and sh(a[k])==sh(b[k])];diff=[k for k in a if k in b and sh(a[k])!=sh(b[k])]
print('byte-identical to v402:',len(same));print('differ from v402:',diff)
# r1 state of the files that r2 touched: the .bak chain
r1_release_cfg=W/'release_cfg.py.bak_20261029_085633_r2_shared_p2';r1_prepare=W/'app/prepare.py.bak_20261029_085633_r2_shared_p2'
for name,cur,old in(('release_cfg.py',W/'release_cfg.py',r1_release_cfg),('app/prepare.py',W/'app/prepare.py',r1_prepare)):
    print('== r2 vs r1:',name)
    for l in difflib.unified_diff(old.read_text('utf-8').splitlines(),cur.read_text('utf-8').splitlines(),lineterm='',n=0):
        if l[:3] in('---','+++','@@ '):continue
        if l[:1] in '+-':print('  ',l[:300])
# r1 sanity: r1 prepare.py == v402 prepare.py ; r1 release_cfg == v402 + BUILDER + EXPAND_OVERRIDE only
print('r1 prepare.py == v402 prepare.py:',sh(r1_prepare)==sh(V2/'app/prepare.py'))
print('.bak chain sha16:',{p.name:sh(p)[:16] for p in sorted(W.glob('release_cfg.py.bak_*'))})
# any code file modified after r1 submit (08:28) other than the declared ones
import datetime
cut=(W/'receipts/v404-app-submit.json').stat().st_mtime
touched=[(k,datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime('%H:%M:%S')) for k,p in a.items() if p.stat().st_mtime>cut]
print('code files modified after the r1 submit:',touched)
