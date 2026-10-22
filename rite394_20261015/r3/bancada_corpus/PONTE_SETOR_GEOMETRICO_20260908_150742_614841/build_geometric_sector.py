"""Compile only a copied new Lean source in an exclusive Chatgpt build.
Uses pre-existing Mathlib/toolchain binaries read-only. Does not run lake or um.py.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,re,subprocess,sys
sys.stdout.reconfigure(encoding="utf-8")
root=Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
folder=Path(__file__).resolve().parent
assert folder.parent==root and folder.name.startswith("PONTE_SETOR_GEOMETRICO_")
kernel=Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/tgl_kernel")
toolchain=Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0")
lean=toolchain/"bin"/"lean.exe"
source=folder/"GeometricSectorObstruction.lean"
data=source.read_bytes()
text=data.decode("utf-8")
if re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b",text):
    raise RuntimeError("Forbidden proof token in source")
decls=re.findall(r"(?m)^(?:noncomputable\s+)?(abbrev|def|theorem)\s+(\w+)",text)
prints=re.findall(r"(?m)^#print axioms (\w+)$",text)
assert len(prints)==len(set(prints)) and set(prints)=={n for _,n in decls}
build=folder/("BUILD_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
build.mkdir(exist_ok=False)
def new(path,raw):
    assert path.parent==build and not path.exists()
    temp=path.with_name(path.name+".tmp")
    with temp.open("xb") as f: f.write(raw); f.flush(); os.fsync(f.fileno())
    assert temp.read_bytes()==raw
    os.rename(temp,path)
    assert path.read_bytes()==raw
def record(path):
    raw=path.read_bytes()
    return {"path":path.as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
new(build/source.name,data)
new(build/"ImportsGeometricSector.lean",b"import GeometricSectorObstruction\n")
packages=sorted(p for p in (kernel/".lake/packages").iterdir() if p.is_dir())
libraries=[p/".lake/build/lib/lean" for p in packages if (p/".lake/build/lib/lean").is_dir()]
mathlib=kernel/".lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean"
boundary=[lean,kernel/"lean-toolchain",kernel/"lake-manifest.json"]
for module in re.findall(r"(?m)^import ([\w.]+)$",text):
    binary=kernel/".lake/packages/mathlib/.lake/build/lib/lean"/(module.replace(".","/")+".olean")
    source_dependency=kernel/".lake/packages/mathlib"/(module.replace(".","/")+".lean")
    boundary.extend([binary,source_dependency])
    for suffix in [".server",".private"]:
        candidate=Path(str(binary)+suffix)
        if candidate.is_file(): boundary.append(candidate)
before=[record(p) for p in boundary]
env=os.environ.copy()
env["LEAN_PATH"]=os.pathsep.join([str(build)]+[str(p) for p in libraries])
env["LEAN_SRC_PATH"]=str(build)
env["TMP"]=str(build); env["TEMP"]=str(build)
env["PYTHONDONTWRITEBYTECODE"]="1"
print("Compiling new source in "+str(build),flush=True)
runs=[]
for name in ["GeometricSectorObstruction","ImportsGeometricSector"]:
    command=[str(lean),"-o",str(build/(name+".olean")),"-i",str(build/(name+".ilean")),name+".lean"]
    started=datetime.now(timezone.utc).isoformat()
    try:
        proc=subprocess.run(command,cwd=build,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
    except subprocess.TimeoutExpired as failure:
        partial=failure.stdout or b""
        new(build/(name+".log"),partial)
        new(build/"TIMEOUT.json",(json.dumps({"status":"TIMEOUT","seconds":180,"module":name,"source":record(source)},indent=2)+"\n").encode("utf-8"))
        print(partial.decode("utf-8",errors="replace"),flush=True)
        print("TIMEOUT: "+str(build),flush=True)
        sys.exit(1)
    new(build/(name+".log"),proc.stdout)
    runs.append({"module":name,"command":command,"started_utc":started,"exit_code":proc.returncode})
    if proc.returncode:
        print(proc.stdout.decode("utf-8",errors="replace"),flush=True)
        break
log=(build/"GeometricSectorObstruction.log").read_text(encoding="utf-8")
pattern=re.compile(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
rows=[{"name":m.group(1),"axioms":[s.strip() for s in (m.group(2) or "").split(",") if s.strip()]} for m in pattern.finditer(log)]
expected={"ChatgptAudit.GeometricSector."+n for n in prints}
valid=(len(runs)==2 and all(r["exit_code"]==0 for r in runs)
       and len(rows)==len(expected) and {r["name"] for r in rows}==expected
       and all(set(r["axioms"])<={"propext","Classical.choice","Quot.sound"} for r in rows)
       and not pattern.sub("",log).strip()
       and (build/"ImportsGeometricSector.log").read_bytes()==b"")
after=[record(p) for p in boundary]
assert before==after
assert source.read_bytes()==data
result={"status":"PASS_COMPILED_SCOPE" if valid else "FAIL_VISIBLE",
"created_utc":datetime.now(timezone.utc).isoformat(),
"source":record(source),"build":build.as_posix(),
"theorems":sum(k=="theorem" for k,_ in decls),"definitions_and_abbreviations":sum(k!="theorem" for k,_ in decls),
"axiom_rows":rows,"runs":runs,
"external_boundary":before,"external_boundary_unchanged":True,
"library_search_paths":[p.as_posix() for p in libraries],
"scope":{"independent_review":False,"canonical_changes":False,"qg_proof":False,
"mathlib_transitive_dependencies_rebuilt":False,"mathlib_transitive_dependencies_all_hashed":False},
"scope_note":"Fresh compilation of this new source and an importing module; pre-existing Mathlib and toolchain are an explicit external trust boundary. No original program or canonical kernel module was compiled."}
new(build/"BUILD_RESULT.json",(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"status":result["status"],"build":build.as_posix(),"theorems":result["theorems"],
"definitions_and_abbreviations":result["definitions_and_abbreviations"],"axiom_rows":len(rows)},ensure_ascii=False),flush=True)
sys.exit(0 if valid else 1)
