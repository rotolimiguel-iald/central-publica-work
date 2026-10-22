"""Development-only047 probes against the union of sealed045/046 local binaries."""
from pathlib import Path
from datetime import datetime,timezone
import os,json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parent
DEPENDENCIES={
 "ExpectationAlgebra":[],
 "OperatorBlockRepresentation":[],
 "GeneralExpectationCP":["ExpectationBlockPositive","OperatorBlockRepresentation"],
 "GeneralExpectationPositive":["ExpectationAlgebra"],
 "ExpectationBlockPositive":["GeneralExpectationPositive"],
 "ExpectationContinuity":["ExpectationAlgebra"],
 "MonotoneOperatorLimit":[],
 "ExpectationNormality":["ExpectationContinuity","GeneralExpectationPositive","MonotoneOperatorLimit"],
}
def new(p,b):
 assert p.resolve().is_relative_to(ROOT) and not p.exists()
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+".tmp")
 with t.open("xb") as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==b;t.rename(p)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 assert len(sys.argv)>1 and all(m in DEPENDENCIES for m in sys.argv[1:])
 assert not (ROOT/"CONTINUACAO047_MANIFESTO.json").exists()
 marker=ROOT/"CONTINUACAO047_DEV_BOUNDARY.json"
 d=json.loads(marker.read_text(encoding="utf-8"))
 assert d["development_only"] is True
 base=Path(d["directory"]);assert base.parent==ROOT
 for row in d["files"]:
  p=Path(row["path"]);assert sha(p)==row["sha256"] and p.stat().st_size==row["bytes"]
 folder=ROOT/("CONTINUACAO047_PROBE_"+datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
 folder.mkdir(exist_ok=False)
 env=os.environ.copy();paths=[str(folder),str(base),*d["external_roots"]]
 assert ROOT not in [Path(p).resolve() for p in paths]
 env["LEAN_PATH"]=os.pathsep.join(paths);env.pop("LEAN_SRC_PATH",None);env.pop("LEAN_SYSROOT",None)
 compiler=d["toolchain"]["path"];assert sha(Path(compiler))==d["toolchain"]["sha256"]
 order=[]
 def visit(m):
  for x in DEPENDENCIES[m]:visit(x)
  if m not in order:order.append(m)
 for m in sys.argv[1:]:visit(m)
 records=[]
 for m in order:
  origin=ROOT/(m+".lean");raw=origin.read_bytes();src=folder/origin.name;new(src,raw)
  print(json.dumps({"event":"probe_start","module":m,"folder":str(folder)}),flush=True)
  cmd=[compiler,"-o",str(folder/(m+".olean")),str(src)]
  r=subprocess.run(cmd,cwd=folder,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  new(folder/(m+".log"),r.stdout)
  row={"module":m,"exit_code":r.returncode,"source_sha256":hashlib.sha256(raw).hexdigest(),
       "source_unchanged":origin.read_bytes()==raw and src.read_bytes()==raw,"log":str(folder/(m+".log"))}
  records.append(row);print(json.dumps(row),flush=True)
  if r.returncode or not row["source_unchanged"]:break
 new(folder/"PROBE.json",(json.dumps({"development_only":True,"not_final_evidence":True,
    "base_marker":str(marker),"base_marker_sha256":sha(marker),"lean_path":paths,"records":records},indent=2)+"\n").encode())
 sys.exit(records[-1]["exit_code"] or (0 if records[-1]["source_unchanged"] else 2))
if __name__=="__main__":main()
