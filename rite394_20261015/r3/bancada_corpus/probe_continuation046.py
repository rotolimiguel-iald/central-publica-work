"""Development-only probes of continuation046 against the sealed045 boundary."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys
ROOT=Path(__file__).resolve().parent
DEPENDENCIES={
 "AperiodicPhaseAverage":[],
 "BoundedOmegaLimit":[],
 "AperiodicVectorAverage":["AperiodicPhaseAverage","BoundedOmegaLimit"],
 "AperiodicAveragePrefix":["AperiodicPhaseAverage"],
 "AperiodicCentralizerExpectation":["AperiodicVectorAverage","AperiodicAveragePrefix"],
 "AperiodicTowerLift":["AperiodicCentralizerExpectation"],
}
def new(p,b):
    assert p.resolve().is_relative_to(ROOT) and not p.exists()
    t=p.with_name(p.name+".tmp")
    with t.open("xb") as f: f.write(b); f.flush(); os.fsync(f.fileno())
    assert t.read_bytes()==b
    t.rename(p)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert len(sys.argv)>=2 and all(m in DEPENDENCIES for m in sys.argv[1:])
    assert not (ROOT/"CONTINUACAO046_MANIFESTO.json").exists()
    order=[]
    def visit(m):
        for d in DEPENDENCIES[m]: visit(d)
        if m not in order: order.append(m)
    for m in sys.argv[1:]: visit(m)
    seal=ROOT/"CONTINUACAO045_MANIFESTO.json"
    manifest=json.loads(seal.read_text(encoding="utf-8"))
    assert manifest["status"]=="PASS"
    marker=ROOT/"CONTINUACAO045_CLEAN_BUILD.json"
    pin=manifest["clean_build"]
    assert pin["sha256"]==sha(marker) and pin["bytes"]==marker.stat().st_size
    data=json.loads(marker.read_text(encoding="utf-8"))
    assert data["status"]=="PASS" and data["development_only"] is False
    base=Path(data["clean_directory"]).resolve()
    assert base.parent==ROOT and base.name.startswith("CONTINUACAO045_CLEAN_")
    folder=ROOT/("CONTINUACAO046_PROBE_"+datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    folder.mkdir(exist_ok=False)
    env=os.environ.copy()
    paths=[str(folder),*data["lean_path"]]
    assert ROOT not in [Path(p).resolve() for p in paths]
    env["LEAN_PATH"]=os.pathsep.join(paths)
    env.pop("LEAN_SRC_PATH",None); env.pop("LEAN_SYSROOT",None)
    compiler=data["toolchain"]["path"]
    assert sha(Path(compiler))==data["toolchain"]["sha256"]
    records=[]
    for module in order:
        origin=ROOT/(module+".lean"); raw=origin.read_bytes()
        src=folder/origin.name; new(src,raw)
        cmd=[compiler,"-o",str(folder/(module+".olean")),str(src)]
        print(json.dumps({"event":"probe_start","module":module,"folder":str(folder)}),flush=True)
        result=subprocess.run(cmd,cwd=folder,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        new(folder/(module+".log"),result.stdout)
        unchanged=origin.read_bytes()==raw and src.read_bytes()==raw
        row={"module":module,"exit_code":result.returncode,
             "source_sha256":hashlib.sha256(raw).hexdigest(),
             "source_unchanged":unchanged,"log":str(folder/(module+".log"))}
        records.append(row); print(json.dumps(row),flush=True)
        if result.returncode or not unchanged: break
    new(folder/"PROBE.json",(json.dumps({"development_only":True,"not_final_evidence":True,
      "base_manifest":str(seal),"base_manifest_sha256":sha(seal),
      "base_marker":str(marker),"base_marker_sha256":sha(marker),
      "lean_path":paths,"records":records},indent=2)+"\n").encode())
    sys.exit(records[-1]["exit_code"] or (0 if records[-1]["source_unchanged"] else 2))
if __name__=="__main__": main()
