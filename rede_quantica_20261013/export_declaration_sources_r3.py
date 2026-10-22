"""Read defining modules from the completed candidate environment, once."""
from pathlib import Path
import datetime as dt
import hashlib, json, os, subprocess, time
from diary_r1 import ROOT, new, pin

out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015/full_rite'
run=ROOT/'work/rite394_20261015/r3'
kernel=run/'tgl_kernel'
lean=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
target=out/'declaration_sources_r3'
target.mkdir(exist_ok=False)
source=out/'DeclarationSourcesR2.lean'
new(target/source.name,source.read_bytes().decode('utf-8'))
deps=[pin(kernel/'.lake/build/lib/lean/TGL.olean'),pin(kernel/'.lake/build/lib/lean/TGLExt.olean'),pin(run/'tgl_kernel_proof_manifest.json'),pin(run/'um_absoluto.json')]
paths=[kernel/'.lake/build/lib/lean']+sorted((kernel/'.lake/packages').glob('*/.lake/build/lib/lean'))+[lean.parent.parent/'lib/lean']
env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,paths)))
cmd=[str(lean),'-o',str(target/'DeclarationSourcesR2.olean'),str(target/source.name)]
start=dt.datetime.now(dt.timezone.utc).isoformat();t=time.perf_counter()
r=subprocess.run(cmd,env=env,cwd=target,capture_output=True)
end=dt.datetime.now(dt.timezone.utc).isoformat();elapsed=time.perf_counter()-t
raw=r.stdout+r.stderr
new(target/'OUTPUT.txt',raw.decode('utf-8','replace'))
rows={}
for line in raw.decode('utf-8','replace').splitlines():
    if line.startswith('DECL_SOURCE\t'):
        _,name,module=line.split('\t')
        assert name not in rows
        rows[name]=module.replace('.','/')+'.lean'
new(target/'DECLARATION_SOURCES.json',rows)
receipt=dict(command=cmd,toolchain=subprocess.check_output([str(lean),'--version'],text=True).strip(),LEAN_PATH=env['LEAN_PATH'],start_utc=start,end_utc=end,seconds=elapsed,exit_code=r.returncode,count=len(rows),dependencies=deps,dependencies_unchanged=all(pin(p['path'])==p for p in deps),artifacts=[pin(p) for p in sorted(target.iterdir()) if p.is_file()],no_scientific_rerun=True,production_modified=False)
new(target/'RECEIPT.json',receipt)
print(json.dumps(dict(exit=r.returncode,count=len(rows),seconds=elapsed,receipt=pin(target/'RECEIPT.json'))))
if r.returncode:print(raw.decode('utf-8','replace'))
raise SystemExit(r.returncode)
