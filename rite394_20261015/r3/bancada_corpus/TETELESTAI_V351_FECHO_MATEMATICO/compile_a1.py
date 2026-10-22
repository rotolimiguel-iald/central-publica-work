"""Pinned Lean, inherited read-only dependency objects, isolated output and attempts."""
from pathlib import Path
import subprocess, os, json, hashlib, datetime, sys
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel'
LEAN=Path(r'C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe')
source=ROOT/Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'kernel/TGLExt/V351RegularCoreTraceContract.lean'
assert source.is_relative_to(ROOT)
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
out=ROOT/'attempts'/stamp; out.mkdir(parents=True)
(out/source.name).write_bytes(source.read_bytes())
paths=[ROOT/'build',OLD/'.lake/build/lib/lean']
paths += sorted(p/'.lake/build/lib/lean' for p in (OLD/'.lake/packages').iterdir() if p.is_dir())
env=os.environ.copy();env['LEAN_PATH']=';'.join(map(str,paths))
(ROOT/'build/TGLExt').mkdir(parents=True,exist_ok=True)
module_root=ROOT/'kernel' if source.is_relative_to(ROOT/'kernel') else ROOT/'probes'
command=[str(LEAN),'--root='+str(module_root),'-o',str(ROOT/'build/TGLExt'/source.with_suffix('.olean').name),str(source)]
run=subprocess.run(command,cwd=ROOT/'kernel',env=env,capture_output=True)
(out/'stdout.txt').write_bytes(run.stdout);(out/'stderr.txt').write_bytes(run.stderr)
record=dict(command=command,cwd=str(ROOT/'kernel'),lean_path=list(map(str,paths)),returncode=run.returncode,
 source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),lean_version=subprocess.check_output([str(LEAN),'--version']).decode().strip())
(out/'run.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(str(out));print(run.stdout.decode('utf-8',errors='replace'));print(run.stderr.decode('utf-8',errors='replace'))
sys.exit(run.returncode)
