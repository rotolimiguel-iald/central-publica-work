"""Compile new modules only, in fresh isolated builds; canonical dependencies read-only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,re,subprocess,sys
sys.stdout.reconfigure(encoding="utf-8")
folder=Path(__file__).resolve().parent
assert folder.parent==Path(r"C:\IALD\Central de Patentes\Chatgpt")
kernel=Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/tgl_kernel")
lean=Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe")
names=sys.argv[1:] or ["CollapseContract"]
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
sources={n:(folder/(n+".lean")).read_bytes() for n in names}
all_decls=[];expected=set();boundary=[lean,kernel/"lean-toolchain",kernel/"lake-manifest.json"]
for name,data in sources.items():
    text=data.decode("utf-8")
    if re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b",text):
        raise RuntimeError("Forbidden proof token")
    decls=re.findall(r"(?m)^(?:(?:noncomputable|local)\s+)?(abbrev|def|theorem|structure|instance)\s+(\w+)",text)
    prints=re.findall(r"(?m)^#print axioms (\w+)$",text)
    assert len(prints)==len(set(prints)) and set(prints)=={n for _,n in decls}
    namespaces=re.findall(r"(?m)^namespace ([\w.]+)$",text)
    assert len(namespaces)==1
    namespace=namespaces[0]+"."
    all_decls.extend(decls);expected.update(namespace+n for n in prints)
    new(build/(name+".lean"),data)
    for module in re.findall(r"(?m)^import ([\w.]+)$",text):
        if module in names: continue
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
"library_search_paths":[p.as_posix() for p in libraries],
"scope":{"independent_review":False,"canonical_changes":False,"qg_proof":False,"transitive_dependencies_rebuilt":False,"transitive_dependencies_all_hashed":False},
"scope_note":"New modules freshly compiled against pre-existing canonical TGLExt and Mathlib binaries. Direct imported sources and binaries hashed before/after; no canonical module rebuilt and no original um.py executed."}
new(build/"BUILD_RESULT.json",(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"status":result["status"],"build":build.as_posix(),"theorems":result["theorems"],"definitions":result["definitions"],"axiom_rows":len(rows)}),flush=True)
sys.exit(0 if valid else 1)
