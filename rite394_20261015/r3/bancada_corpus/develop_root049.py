"""Compile one root049 source in an exclusive directory; no canonical writes."""
from pathlib import Path
from datetime import datetime, timezone
import os,sys,subprocess,hashlib,json
sys.stdout.reconfigure(encoding="utf-8")
ROOT=Path(__file__).resolve().parent
KERNEL=Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/tgl_kernel")
TOOL=Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0")
name=sys.argv[1] if len(sys.argv)>1 else "ClosedAntilinearStandardSubspace"
if not name.replace("_","").isalnum(): raise ValueError(name)
source=ROOT/(name+".lean")
build=ROOT/("DEV049_ROOT_"+datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
build.mkdir()
raw=source.read_bytes()
copy=build/source.name
with copy.open("xb") as f: f.write(raw)
ext=[p/".lake/build/lib/lean" for p in sorted((KERNEL/".lake/packages").iterdir()) if (p/".lake/build/lib/lean").is_dir()]
env=os.environ.copy(); env["LEAN_PATH"]=os.pathsep.join(map(str,[build,*ext,TOOL/"lib/lean"]))
cmd=[str(TOOL/"bin/lean.exe"),"-o",str(build/(name+".olean")),str(copy)]
print(json.dumps({"build":str(build),"cmd":cmd}),flush=True)
r=subprocess.run(cmd,cwd=build,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
with (build/"compile.log").open("xb") as f:f.write(r.stdout)
print(r.stdout.decode("utf-8",errors="replace"),flush=True)
assert raw==source.read_bytes() and raw==copy.read_bytes()
print(json.dumps({"exit_code":r.returncode,"build":str(build)}),flush=True)
sys.exit(r.returncode)
