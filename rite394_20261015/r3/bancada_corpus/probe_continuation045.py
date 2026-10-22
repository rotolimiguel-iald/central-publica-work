"""Development-only Lean probes; final evidence must use clean_continuation045."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys
ROOT = Path(__file__).resolve().parent
ALLOWED = ["FiniteSitePermutations", "FiniteSiteHorizons"]
def new(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
def main():
    assert len(sys.argv) == 2 and sys.argv[1] in ALLOWED
    assert not (ROOT / "CONTINUACAO045_MANIFESTO.json").exists()
    order = ALLOWED[:ALLOWED.index(sys.argv[1])+1]
    marker = ROOT / "CONTINUACAO045_DEVELOPMENT_20260906_232105_077981.json"
    data = json.loads(marker.read_text(encoding="utf-8"))
    assert data["status"] == "PASS" and data["development_only"] is True
    base = Path(data["clean_directory"]).resolve()
    assert base.parent == ROOT and base.name.startswith("CONTINUACAO045_CLEAN_")
    folder = ROOT / ("CONTINUACAO045_PROBE_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
    folder.mkdir(exist_ok=False)
    legacy_pins = {}
    for ordinal in [6, 7]:
        legacy = json.loads((ROOT / f"ORDEM{ordinal:03d}_MANIFESTO.json").read_text(encoding="utf-8"))
        legacy_pins.update({str(Path(row["path"]).resolve()).lower():row for row in legacy["files"]})
    for filename in ["ChainSiteFlow.lean", "ChainSiteFlow.olean", "ChainSiteFlow.olean.private", "ChainSiteFlow.olean.server"]:
        old_dependency = ROOT / filename
        if not old_dependency.is_file():
            assert filename.endswith((".private", ".server"))
            continue
        dep_raw = old_dependency.read_bytes()
        pin = legacy_pins[str(old_dependency.resolve()).lower()]
        assert len(dep_raw) == pin["bytes"] and hashlib.sha256(dep_raw).hexdigest() == pin["sha256"]
        new(folder / filename, dep_raw)
    env = os.environ.copy()
    marker040 = ROOT / "CONTINUACAO040_CLEAN_BUILD.json"
    pins040 = json.loads((ROOT / "CONTINUACAO040_MANIFESTO.json").read_text(encoding="utf-8"))
    expected040 = next(row for row in pins040["files"] if Path(row["path"]).resolve() == marker040.resolve())
    assert hashlib.sha256(marker040.read_bytes()).hexdigest() == expected040["sha256"]
    data040 = json.loads(marker040.read_text(encoding="utf-8"))
    assert data040["status"] == "PASS" and data040["development_only"] is False
    paths = list(dict.fromkeys([str(folder), *data["lean_path"], *data040["lean_path"]]))
    assert ROOT not in [Path(p).resolve() for p in paths]
    env["LEAN_PATH"] = os.pathsep.join(paths)
    env.pop("LEAN_SRC_PATH", None); env.pop("LEAN_SYSROOT", None)
    compiler = data["toolchain"]["path"]
    assert hashlib.sha256(Path(compiler).read_bytes()).hexdigest() == data["toolchain"]["sha256"]
    records=[]
    for module in order:
        origin = ROOT / (module + ".lean")
        raw = origin.read_bytes()
        src = folder / origin.name
        new(src,raw)
        cmd = [compiler, "-o", str(folder/(module+".olean")), str(src)]
        print(json.dumps({"event":"probe_start","module":module,"folder":str(folder)}),flush=True)
        result = subprocess.run(cmd,cwd=folder,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        new(folder/(module+".log"), result.stdout)
        assert origin.read_bytes() == raw and src.read_bytes() == raw
        row={"module":module,"exit_code":result.returncode,"source_sha256":hashlib.sha256(raw).hexdigest(),
             "log":str(folder/(module+".log"))}
        records.append(row)
        print(json.dumps(row),flush=True)
        if result.returncode != 0:
            break
    new(folder/"PROBE.json",(json.dumps({"development_only":True,"not_final_evidence":True,
       "base_marker":str(marker),"base_marker_sha256":hashlib.sha256(marker.read_bytes()).hexdigest(),
       "lean_path":env["LEAN_PATH"],"records":records},indent=2)+"\n").encode())
    sys.exit(records[-1]["exit_code"])
if __name__ == "__main__":
    main()
