"""Builder dry-run harness: one scratch copy of the pipeline per EXPAND_OVERRIDE candidate; shim task (no mission calls); nothing written under the real v404 folder or the installed app."""
import re,sys,shutil,subprocess,json,time
from pathlib import Path
REAL=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029')
SP=Path(r'C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad')
PY=r'C:\Python314\python.exe'
cands={'D':(),'A':('_v402','_v403','_v404'),'B':('_v403','_v404'),'C':('_v404',)}
name=sys.argv[1];ov=cands[name]
root=SP/('cand'+name)/REAL.name
if root.exists():shutil.rmtree(root.parent)
(root/'app').mkdir(parents=True)
cfg=(REAL/'release_cfg.py').read_text(encoding='utf-8')
cfg2=re.sub(r'(?m)^EXPAND_OVERRIDE = .*$','EXPAND_OVERRIDE = '+repr(ov),cfg);assert cfg2!=cfg
(root/'release_cfg.py').write_text(cfg2,encoding='utf-8')
(root/'task.py').write_text("def check(task,actor=None):\n    return {'ready':True}\n",encoding='utf-8')
shutil.copy(REAL/'app/RELEASE.json',root/'app/RELEASE.json')
for f in ('prepare.py','finalize.py'):shutil.copy(REAL/'app'/f,root/'app'/f)
shutil.copytree(REAL/'app/build',root/'app/build')
env=None
for step in ('prepare.py','finalize.py'):
    t=time.time()
    p=subprocess.run([PY,'-B','-X','utf8',str(root/'app'/step)],capture_output=True,cwd=str(root))
    (root/('out_'+step+'.txt')).write_bytes(p.stdout);(root/('err_'+step+'.txt')).write_bytes(p.stderr)
    print(name,step,'rc',p.returncode,round(time.time()-t),'s',flush=True)
    if p.returncode:
        print(p.stdout.decode('utf8','replace')[-1500:]);print(p.stderr.decode('utf8','replace')[-1500:]);break
