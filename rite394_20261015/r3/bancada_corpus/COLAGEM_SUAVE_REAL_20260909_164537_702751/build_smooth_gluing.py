from pathlib import Path
import sys,os,json,re,hashlib,subprocess,datetime
sys.stdout.reconfigure(encoding="utf-8")
folder=Path(__file__).resolve().parent
chatgpt=Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
assert folder.is_relative_to(chatgpt)
config_path=Path(sys.argv[1]).resolve()
config=json.loads(config_path.read_bytes())
names=sys.argv[2:]
assert names and all(re.fullmatch(r"[A-Za-z_]\w*",n) for n in names)
library=Path(config["approved_library"]).resolve()
approved=library/"TRANSPOSED_RESULT.json"
receipt=json.loads(approved.read_bytes())
assert receipt["status"]=="PASS_TRANSPOSED_SCOPE"
assert len(receipt["runs"])==21 and all(r["exit_code"]==0 and r["valid"] for r in receipt["runs"])
assert len(receipt["cached_modules"])==45 and receipt["cached_boundary_unchanged"]
assert receipt["input_boundary_unchanged"] and not receipt["um_py_executed"]
assert all(z["source_bytes_identical"] and z["prior_run"]["valid"] for z in receipt["cached_modules"])
kernel=Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
lean=Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe")
build=folder/("BUILD_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"));build.mkdir()
def record(p):
 b=p.read_bytes();return {"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def new(p,b):
 assert p.resolve().is_relative_to(chatgpt) and not p.exists()
 p.parent.mkdir(parents=True,exist_ok=True)
 t=p.with_name(p.name+".tmp")
 with t.open("xb") as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==b
 os.replace(t,p);assert p.read_bytes()==b
boundary=[config_path,approved,library/"BUILD_PLAN.json",lean,kernel/"lean-toolchain",kernel/"lake-manifest.json"]
approved_plan=json.loads((library/"BUILD_PLAN.json").read_bytes())
assert record(library/"BUILD_PLAN.json")==receipt["plan"]
assert len(approved_plan["sources"])==63
integration={"modules":[{"source":z["path"]} for z in approved_plan["sources"]]}
for spec in integration["modules"]:
 mod=Path(spec["source"]).stem
 for suffix in [".lean",".olean",".ilean",".olean.server",".olean.private"]:
  p=library/"TGLExt"/(mod+suffix)
  if suffix in [".lean",".olean"]:assert p.is_file()
  if p.is_file():boundary.append(p)
cached=[]
for mod,spec in config.get("cached",{}).items():
 origin=Path(spec["source"]);prior=Path(spec["build"]);rp=prior/"BUILD_RESULT.json";r=json.loads(rp.read_bytes())
 assert r["status"]=="PASS_COMPILED_SCOPE"
 assert any(z["module"]==mod and z["exit_code"]==0 for z in r["runs"])
 assert any(z["sha256"]==record(origin)["sha256"] for z in r["sources"])
 assert (prior/(mod+".lean")).read_bytes()==origin.read_bytes()
 boundary.extend([origin,rp]);art=[]
 for suffix in [".lean",".olean",".ilean",".olean.server",".olean.private"]:
  p=prior/(mod+suffix)
  if suffix in [".lean",".olean"]:assert p.is_file()
  if p.is_file():new(build/p.name,p.read_bytes());boundary.append(p);art.append(record(p))
 cached.append({"module":mod,"receipt":record(rp),"artifacts":art})
sources={n:(folder/(n+".lean")).read_bytes() for n in names};declarations=[];expected=set()
for n,b in sources.items():
 s=b.decode("utf8")
 assert not re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b",s)
 ns=re.findall(r"(?m)^namespace ([\w.]+)$",s);assert len(ns)==1
 ds=re.findall(r"(?m)^(?:noncomputable\s+)?(abbrev|def|theorem|structure)\s+(\w+)",s)
 prints=re.findall(r"(?m)^#print axioms (\w+)$",s)
 assert len(prints)==len(set(prints)) and set(prints)=={name for _,name in ds}
 declarations.extend(ds);expected.update(ns[0]+"."+name for name in prints)
 new(build/(n+".lean"),b)
 for imp in re.findall(r"(?m)^import ([\w.]+)$",s):
  if imp in names or imp in config.get("cached",{}):continue
  relative=Path(imp.replace(".","/"))
  if imp.startswith("TGLExt.") and (library/(str(relative)+".olean")).is_file():
   root=library;sr=root/(str(relative)+".lean");binary=root/(str(relative)+".olean")
  else:
   root=kernel if imp.startswith("TGLExt.") else kernel/".lake/packages/mathlib"
   sr=root/(str(relative)+".lean");binary=root/".lake/build/lib/lean"/(str(relative)+".olean")
  boundary.extend([sr,binary])
  for ext in [".server",".private"]:
   p=Path(str(binary)+ext)
   if p.is_file():boundary.append(p)
boundary=list(dict.fromkeys(boundary));before=[record(p) for p in boundary]
new(build/"ImportFinite.lean",("\n".join("import "+n for n in names)+"\n").encode())
packages=sorted(p/".lake/build/lib/lean" for p in (kernel/".lake/packages").iterdir() if p.is_dir() and (p/".lake/build/lib/lean").is_dir())
libraries=[build,library,kernel/".lake/build/lib/lean"]+packages
env=os.environ.copy();env["LEAN_PATH"]=os.pathsep.join(map(str,libraries));env["LEAN_SRC_PATH"]=str(build)
env["TMP"]=env["TEMP"]=str(build);env["PYTHONDONTWRITEBYTECODE"]="1"
version=subprocess.run([str(lean),"--version"],capture_output=True,timeout=20,env=env,cwd=build);assert version.returncode==0
print("Compiling in "+str(build),flush=True)
pattern=re.compile(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
runs=[];rows=[];clean=True
for n in names+["ImportFinite"]:
 cmd=[str(lean),"-o",str(build/(n+".olean")),"-i",str(build/(n+".ilean")),n+".lean"]
 try:proc=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=build,env=env,timeout=240)
 except subprocess.TimeoutExpired as e:
  new(build/(n+".log"),e.stdout or b"");new(build/"TIMEOUT.json",json.dumps({"module":n,"status":"TIMEOUT","seconds":240}).encode());print("TIMEOUT "+n);sys.exit(1)
 new(build/(n+".log"),proc.stdout)
 log=proc.stdout.decode("utf8",errors="replace")
 rows.extend({"name":m.group(1),"axioms":[a.strip() for a in (m.group(2) or "").split(",") if a.strip()]} for m in pattern.finditer(log))
 clean=clean and not pattern.sub("",log).strip()
 runs.append({"module":n,"exit_code":proc.returncode,"command":cmd})
 if proc.returncode or not clean:print(log,flush=True)
 if proc.returncode:break
valid=len(runs)==len(names)+1 and all(r["exit_code"]==0 for r in runs) and clean and len(rows)==len(expected) and {r["name"] for r in rows}==expected and all(set(r["axioms"])<={"propext","Classical.choice","Quot.sound"} for r in rows)
assert before==[record(p) for p in boundary]
assert all((folder/(n+".lean")).read_bytes()==b for n,b in sources.items())
result={"status":"PASS_COMPILED_SCOPE" if valid else "FAIL_VISIBLE","created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
"build":build.as_posix(),"toolchain":version.stdout.decode().strip(),"sources":[record(folder/(n+".lean")) for n in names],
"theorems":sum(k=="theorem" for k,_ in declarations),"definitions":sum(k!="theorem" for k,_ in declarations),"axiom_rows":rows,
"runs":runs,"boundary":before,"boundary_unchanged":True,"approved_library":record(approved),"cached":cached,
"scope":{"um_py_executed":False,"original_changes":False,"full_transitive_rebuild":False,"full_transitive_hash":False,"independent_semantic_review":False},
"scope_note":"Fresh leaf and importer compiled against approved transposed63 library and optional byte-copied local PASS dependencies. Approved63 module sources/binaries and direct imports hashed before/after; canonical/Mathlib transitive dependencies not all rebuilt/hashed."}
new(build/"BUILD_RESULT.json",(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode())
print(json.dumps({"status":result["status"],"build":build.as_posix(),"theorems":result["theorems"],"definitions":result["definitions"],"audits":len(rows)}),flush=True)
sys.exit(0 if valid else 1)
