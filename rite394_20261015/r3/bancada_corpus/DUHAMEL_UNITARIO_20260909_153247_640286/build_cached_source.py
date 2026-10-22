"""Compile new modules only, in fresh isolated builds; canonical dependencies read-only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,re,subprocess,sys
sys.stdout.reconfigure(encoding="utf-8")
folder=Path(__file__).resolve().parent
assert folder.parent==Path(r"C:\IALD\Central de Patentes\Chatgpt")
kernel=Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/tgl_kernel")
lean=Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe")
config_path=Path(sys.argv[1]).resolve()
config=json.loads(config_path.read_text(encoding="utf-8"))
names=sys.argv[2:]
assert names
cache_specs=config["cached"]
assert not(set(cache_specs)&set(names))
assert all(re.fullmatch(r"[A-Za-z0-9_]+",n) for n in names)

build=folder/("BUILD_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
build.mkdir(exist_ok=False)
def new(path,raw):
    assert path.parent==build and not path.exists()
    temp=path.with_name(path.name+".tmp")
    with temp.open("xb") as f:
        f.write(raw);f.flush();os.fsync(f.fileno())
    assert temp.read_bytes()==raw
    os.rename(temp,path)
    assert path.read_bytes()==raw
def record(p):
    raw=p.read_bytes()
    return {"path":p.as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
cache_boundary=[config_path]
cache_evidence=[]
for module,spec in cache_specs.items():
    origin=Path(spec["source"])
    prior=Path(spec["build"])
    receipt_path=prior/"BUILD_RESULT.json"
    receipt=json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["status"]=="PASS_COMPILED_SCOPE"
    assert any(r["module"]==module and r["exit_code"]==0 for r in receipt["runs"])
    source_data=origin.read_bytes()
    assert any(s["sha256"]==hashlib.sha256(source_data).hexdigest() and Path(s["path"]).stem==module for s in receipt["sources"])
    assert (prior/(module+".lean")).read_bytes()==source_data
    if (folder/(module+".lean")).exists():
        assert (folder/(module+".lean")).read_bytes()==source_data
    cache_boundary.extend([origin,receipt_path,prior/(module+".lean")])
    copied=[]
    for suffix in [".lean",".olean",".ilean",".olean.server",".olean.private"]:
        artifact=prior/(module+suffix)
        if suffix in [".lean",".olean"]:assert artifact.is_file()
        if artifact.is_file():
            new(build/artifact.name,artifact.read_bytes())
            cache_boundary.append(artifact)
            copied.append(record(artifact))
    cache_evidence.append({"module":module,"receipt":record(receipt_path),"artifacts":copied})
sources={n:(folder/(n+".lean")).read_bytes() for n in names}
all_decls=[];expected=set();boundary=[lean,kernel/"lean-toolchain",kernel/"lake-manifest.json"]+cache_boundary
for name,data in sources.items():
    text=data.decode("utf-8")
    if re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b",text):
        raise RuntimeError("Forbidden proof token")
    decls=re.findall(r"(?m)^(?:local\s+)?(?:noncomputable\s+)?(abbrev|def|theorem|structure|instance)\s+(\w+)",text)
    prints=re.findall(r"(?m)^#print axioms (\w+)$",text)
    assert len(prints)==len(set(prints)) and set(prints)=={n for _,n in decls}
    namespaces=re.findall(r"(?m)^namespace ([\w.]+)$",text)
    assert len(namespaces)==1
    namespace=namespaces[0]+"."
    all_decls.extend(decls);expected.update(namespace+n for n in prints)
    new(build/(name+".lean"),data)
    for module in re.findall(r"(?m)^import ([\w.]+)$",text):
        if module in names or module in cache_specs: continue
        local=kernel if module.startswith("TGLExt.") else kernel/".lake/packages/mathlib"
        binary=local/".lake/build/lib/lean"/(module.replace(".","/")+".olean")
        boundary.extend([binary,local/(module.replace(".","/")+".lean")])
        for suffix in [".server",".private"]:
            p=Path(str(binary)+suffix)
            if p.is_file():boundary.append(p)
boundary=list(dict.fromkeys(boundary))
before=[record(p) for p in boundary]
new(build/"ImportsRealization.lean",("\n".join("import "+n for n in names)+"\n").encode())
packages=sorted(p for p in (kernel/".lake/packages").iterdir() if p.is_dir())
libraries=[kernel/".lake/build/lib/lean"]+[p/".lake/build/lib/lean" for p in packages if (p/".lake/build/lib/lean").is_dir()]
env=os.environ.copy()
env["LEAN_PATH"]=os.pathsep.join([str(build)]+[str(p) for p in libraries])
env["LEAN_SRC_PATH"]=str(build);env["TMP"]=str(build);env["TEMP"]=str(build)
env["PYTHONDONTWRITEBYTECODE"]="1"
print("Compiling in "+str(build),flush=True)
version=subprocess.run([str(lean),"--version"],cwd=build,env=env,capture_output=True,timeout=20)
assert version.returncode==0
runs=[];rows=[];clean=True
pattern=re.compile(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
for name in names+["ImportsRealization"]:
    command=[str(lean),"-o",str(build/(name+".olean")),"-i",str(build/(name+".ilean")),name+".lean"]
    try:
        proc=subprocess.run(command,cwd=build,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
    except subprocess.TimeoutExpired as failure:
        new(build/(name+".log"),failure.stdout or b"")
        new(build/"TIMEOUT.json",(json.dumps({"status":"TIMEOUT","module":name,"seconds":240})+"\n").encode())
        print("TIMEOUT "+name,flush=True);sys.exit(1)
    new(build/(name+".log"),proc.stdout)
    runs.append({"module":name,"exit_code":proc.returncode,"command":command})
    log=proc.stdout.decode("utf-8",errors="replace")
    rows.extend({"name":m.group(1),"axioms":[s.strip() for s in (m.group(2) or "").split(",") if s.strip()]} for m in pattern.finditer(log))
    clean=clean and not pattern.sub("",log).strip()
    if proc.returncode or not clean: print(log,flush=True)
    if proc.returncode:break
valid=(len(runs)==len(names)+1 and all(r["exit_code"]==0 for r in runs) and clean
       and len(rows)==len(expected) and {r["name"] for r in rows}==expected
       and all(set(r["axioms"])<={"propext","Classical.choice","Quot.sound"} for r in rows))
assert before==[record(p) for p in boundary]
assert all((folder/(n+".lean")).read_bytes()==d for n,d in sources.items())
result={"status":"PASS_COMPILED_SCOPE" if valid else "FAIL_VISIBLE",
"created_utc":datetime.now(timezone.utc).isoformat(),"build":build.as_posix(),
"toolchain_version":version.stdout.decode().strip(),"sources":[record(folder/(n+".lean")) for n in names],
"theorems":sum(k=="theorem" for k,_ in all_decls),"definitions":sum(k!="theorem" for k,_ in all_decls),
"axiom_rows":rows,"runs":runs,"external_boundary":before,"external_boundary_unchanged":True,
"library_search_paths":[p.as_posix() for p in libraries],"cached_local_modules":cache_evidence,
"scope":{"independent_review":False,"canonical_changes":False,"qg_proof":False,"transitive_dependencies_rebuilt":False,"transitive_dependencies_all_hashed":False},
"scope_note":"Leaf modules freshly compiled against byte-copied local PASS artifacts and pre-existing canonical/Mathlib binaries. Cached sources verified against prior PASS receipts and artifacts; cache boundary and direct imports hashed before/after. Local dependencies not rebuilt in this leaf round. No original um.py executed."}
new(build/"BUILD_RESULT.json",(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"status":result["status"],"build":build.as_posix(),"theorems":result["theorems"],"definitions":result["definitions"],"axiom_rows":len(rows)}),flush=True)
sys.exit(0 if valid else 1)
