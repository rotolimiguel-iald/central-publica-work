"""Read-only static evidence audit. Writes only new reports, never executes any um.py."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter,defaultdict
import hashlib,json,os,re,sys
sys.stdout.reconfigure(encoding="utf-8")
base=Path(r"C:\IALD\Central de Patentes\Chatgpt")
out=base/"AUDITORIA_COCICLO_COVARIANCIA_20260909_161309_333516"
inventory_path=base/"REEXAME_COCICLO_COVARIANCIA_20260909/INVENTARIO_FONTES.json"
inventory=json.loads(inventory_path.read_text(encoding="utf-8"))
selected=[x for x in inventory["modules"] if x["new_this_continuation"]]
allowed={"propext","Classical.choice","Quot.sound"}
checks=[]; measured={}; receipts={}; audited_receipts={}; modules=[]; local_versions=defaultdict(dict)
def check(label,ok,detail=None):
 checks.append({"label":label,"ok":bool(ok),"detail":detail})
def record(p):
 p=Path(p);b=p.read_bytes()
 return {"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def measure(p):
 p=Path(p);key=str(p.resolve()).lower()
 if key not in measured:
  try:measured[key]=record(p)
  except Exception as e:
   measured[key]={"path":p.as_posix(),"error":type(e).__name__+": "+str(e)}
   check("read:"+p.as_posix(),False,measured[key]["error"])
 return measured[key]
def match(r):
 m=measure(r["path"])
 return all(m.get(k)==r.get(k) for k in ("bytes","sha256"))
def new(name,data):
 p=out/name;t=p.with_name(p.name+".tmp")
 assert not p.exists() and not t.exists() and p.parent==out
 b=data if isinstance(data,bytes)else data.encode("utf-8")
 with t.open("xb")as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==b;os.rename(t,p);assert p.read_bytes()==b
 return record(p)
def scrub(s):
 # Nested Lean block comments, line comments and quoted strings; preserve line numbers.
 r=[];i=0;depth=0;quoted=False
 while i<len(s):
  if depth:
   if s.startswith("/-",i):depth+=1;r+=[" "," "];i+=2;continue
   if s.startswith("-/",i):depth-=1;r+=[" "," "];i+=2;continue
   r.append("\n" if s[i]=="\n"else" ");i+=1;continue
  if quoted:
   if s[i]=="\\" and i+1<len(s):r+=[" "," "];i+=2;continue
   if s[i]=='"':quoted=False
   r.append("\n"if s[i]=="\n"else" ");i+=1;continue
  if s.startswith("/-",i):depth=1;r+=[" "," "];i+=2;continue
  if s.startswith("--",i):
   while i<len(s)and s[i]!="\n":r.append(" ");i+=1
   continue
  if s[i]=='"':quoted=True;r.append(" ");i+=1;continue
  r.append(s[i]);i+=1
 return "".join(r)
dp=re.compile(r"^(?P<mods>(?:(?:noncomputable|private|protected|local)\s+)*)(?P<kind>theorem|lemma|def|abbrev|structure|class|instance|opaque|axiom)\s+(?P<name>[\w'.]+)")
def decls(s):
 scopes=[];res=[]
 for ln,line in enumerate(scrub(s).splitlines(),1):
  n=re.match(r"^namespace\s+([\w'.]+)",line)
  if n:scopes.append(("namespace",n[1]));continue
  if re.match(r"^(?:noncomputable\s+)?section(?:\s|$)",line)or re.match(r"^mutual(?:\s|$)",line):scopes.append(("section",""));continue
  if re.match(r"^end(?:\s|$)",line):
   if scopes:scopes.pop()
   continue
  m=dp.match(line)
  if m:
   prefix=".".join(x[1]for x in scopes if x[0]=="namespace");name=m["name"]
   qual=name[7:]if name.startswith("_root_.")else prefix+"."+name if prefix else name
   res.append({"name":qual,"short":name,"kind":m["kind"],"local":"local"in m["mods"].split(),"line":ln})
 return res
lp=re.compile(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
def rows(log):
 return [{"name":m[1],"axioms":[x.strip()for x in(m[2]or"").split(",")if x.strip()]}for m in lp.finditer(log)]
def receipt(p):
 p=Path(p);key=str(p.resolve()).lower()
 if key not in receipts:receipts[key]={"record":measure(p),"data":json.loads(p.read_text(encoding="utf-8"))}
 return receipts[key]["data"]
def inspect_source(source,build,expected_rows=None):
 source=Path(source);s=source.read_text(encoding="utf-8");ds=decls(s);name=source.stem
 logp=build/(name+".log");log=logp.read_text(encoding="utf-8");lr=rows(log);names=[x["name"]for x in ds]
 label=build.name+":"+name
 check(label+":log_only_axiom_output",not lp.sub("",log).strip())
 check(label+":declarations_equal_log",Counter(names)==Counter(x["name"]for x in lr))
 check(label+":standard_axioms",all(set(x["axioms"])<=allowed for x in lr))
 check(label+":prints_complete",len(re.findall(r"(?m)^#print axioms [\w'.]+\s*$",s))==len(ds))
 check(label+":no_placeholders",not re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b",scrub(s)))
 # Every instance must have a name; no scanner omission is accepted.
 instance_lines=re.findall(r"(?m)^(?:(?:local|noncomputable|private|protected)\s+)*instance\b.*",scrub(s))
 check(label+":all_instances_named",len(instance_lines)==sum(d["kind"]=="instance"for d in ds)
  and all(re.match(r"^(?:(?:local|noncomputable|private|protected)\s+)*instance\s+[\w']+\s",line)for line in instance_lines))
 if expected_rows is not None:check(label+":log_rows_equal_receipt",lr==[x for x in expected_rows if x["name"]in names])
 artifacts=[]
 for suffix in(".lean",".log",".olean",".ilean",".olean.server",".olean.private"):
  p=build/(name+suffix)
  if p.exists():artifacts.append(measure(p))
 for suffix in(".olean",".ilean"):check(label+":compiled_artifact"+suffix,(build/(name+suffix)).is_file())
 return {"declarations":ds,"axiom_rows":lr,"artifacts":artifacts,"imports":re.findall(r"(?m)^import\s+([\w.]+)",scrub(s))}
def verify_receipt(p):
 p=Path(p);key=str(p.resolve()).lower()
 if key in audited_receipts:return audited_receipts[key]
 r=receipt(p);build=p.parent;label="receipt:"+build.as_posix()
 info={"receipt":measure(p),"sources":[],"cache_edges":[],"external_boundary":[],"imports":[],"runs":r.get("runs",[])}
 audited_receipts[key]=info
 check(label+":PASS",r.get("status")=="PASS_COMPILED_SCOPE")
 check(label+":runs_exit_zero",bool(r.get("runs"))and all(x["exit_code"]==0 for x in r["runs"]))
 check(label+":boundary_unchanged",r.get("external_boundary_unchanged") is True)
 fresh_names={Path(x["path"]).stem for x in r.get("sources",[])}
 cached={c["module"]:c for c in r.get("cached_local_modules",[])}
 ds_all=[]
 for sr in r.get("sources",[]):
  path=Path(sr["path"]);copy=build/path.name
  check(label+":source_record:"+path.stem,match(sr))
  check(label+":source_copy:"+path.stem,copy.is_file() and measure(copy).get("sha256")==sr["sha256"])
  sdata=inspect_source(copy,build,r.get("axiom_rows",[]))
  ds_all+=sdata["declarations"];info["sources"].append({"source_record":sr,"measured_current":measure(path),**sdata})
  local_versions[path.stem][sr["sha256"]]=copy.as_posix()
  for imp in sdata["imports"]:
   kind="external"if imp.startswith(("Mathlib.","TGL.","TGLExt.","Batteries.","Lean."))or imp in{"Mathlib","TGL","TGLExt","Init","Lean"}else"local"
   edge={"from":path.stem,"import":imp,"kind":kind}
   if kind=="local":
    ok=imp in fresh_names or imp in cached
    check(label+":import_closure:"+path.stem+"->"+imp,ok)
    edge["resolved"]=ok
   info["imports"].append(edge)
 check(label+":receipt_counts",r.get("theorems")==sum(x["kind"]in{"theorem","lemma"}for x in ds_all)
   and r.get("definitions")==sum(x["kind"]not in{"theorem","lemma"}for x in ds_all))
 check(label+":receipt_all_axiom_rows",Counter(x["name"]for x in r.get("axiom_rows",[]))==Counter(x["name"]for x in ds_all))
 for run in r.get("runs",[]):
  log=build/(run["module"]+".log")
  if log.exists():
   txt=log.read_text(encoding="utf-8")
   check(label+":run_log_no_warning_error:"+run["module"],not re.search(r"(?m)(?:^|: )(?:warning|error):",txt))
   if run["module"]not in fresh_names:check(label+":import_test_log_empty:"+run["module"],not txt.strip())
 for c in cached.values():
  check(label+":cache_receipt_hash:"+c["module"],match(c["receipt"]))
  parent=verify_receipt(c["receipt"]["path"])
  origin=receipt(c["receipt"]["path"])
  edge={"module":c["module"],"receipt":measure(c["receipt"]["path"]),"artifacts":[]}
  for a in c["artifacts"]:
   ap=Path(a["path"]);copy=build/ap.name
   check(label+":cache_artifact:"+ap.name,match(a))
   check(label+":cache_copy:"+ap.name,copy.is_file()and measure(copy).get("sha256")==a["sha256"])
   edge["artifacts"].append({"recorded":a,"measured":measure(ap),"build_copy":measure(copy)})
   if ap.suffix==".lean":
    check(label+":cache_in_origin:"+c["module"],any(Path(q["path"]).stem==c["module"]and q["sha256"]==a["sha256"]for q in origin.get("sources",[])))
  info["cache_edges"].append(edge)
 for b in r.get("external_boundary",[]):
  check(label+":boundary:"+b["path"],match(b))
  info["external_boundary"].append({"recorded":b,"measured":measure(b["path"])})
 return info
for item in selected:
 source=Path(item["source"]);rp=Path(item["build_result"]);sm=measure(source);rm=measure(rp)
 check(source.stem+":inventory_source_hash",sm.get("sha256")==item["sha256"])
 check(source.stem+":inventory_receipt_hash",rm.get("sha256")==item["build_result_sha256"])
 info=verify_receipt(rp)
 sd=next((x for x in info["sources"]if Path(x["source_record"]["path"]).stem==source.stem),None)
 check(source.stem+":in_selected_PASS",sd is not None)
 if sd is None:continue
 ds=sd["declarations"];th=sum(x["kind"]in{"theorem","lemma"}for x in ds);other=len(ds)-th
 check(source.stem+":inventory_counts",th==item["theorems"] and other==item["other_declarations"])
 modules.append({"module":source.stem,"group":source.parent.name,"source":sm,"receipt":rm,"theorems":th,"other_declarations":other,
  "local_instances":sum(x["kind"]=="instance"and x["local"]for x in ds),**{k:sd[k]for k in("declarations","axiom_rows","artifacts","imports")}})
all_names=[d["name"]for m in modules for d in m["declarations"]]
dup={k:v for k,v in Counter(all_names).items()if v>1}
check("batch:no_qualified_collisions",not dup,dup)
batch_hash={m["module"]:m["source"]["sha256"]for m in modules};inherited=defaultdict(list)
for name,versions in local_versions.items():
 check("closure:one_source_version:"+name,len(versions)==1,list(versions))
 if name in batch_hash:check("closure:current_batch_version:"+name,list(versions)==[batch_hash[name]]);continue
 for sha,path in versions.items():
  for d in decls(Path(path).read_text(encoding="utf-8")):inherited[d["name"]].append(path)
coll={k:inherited[k]for k in set(all_names)if k in inherited}
check("batch:no_collisions_with_inherited_local",not coll,coll)
counts={"modules":len(modules),"theorems":sum(x["theorems"]for x in modules),"other_declarations":sum(x["other_declarations"]for x in modules),
 "audited_declarations":sum(len(x["axiom_rows"])for x in modules),"local_instances":sum(x["local_instances"]for x in modules)}
check("batch:18_modules",len(modules)==18)
check("batch:counts_equal_inventory",all(counts[k]==v for k,v in inventory["counts"]["new_this_continuation"].items()))
# Re-read every measured path so changes during the audit are visible, without modifying any input.
for key,m in list(measured.items()):
 if "error"in m:continue
 try:after=record(m["path"]);check("stable:"+m["path"],after==m)
 except Exception as e:check("stable:"+m["path"],False,str(e))
result={"status":"PASS_STATIC_EVIDENCE_AUDIT"if all(x["ok"]for x in checks)else"FAIL_VISIBLE_STATIC_EVIDENCE_AUDIT",
 "created_utc":datetime.now(timezone.utc).isoformat(),"inventory":measure(inventory_path),"counts":counts,"modules":modules,
 "closure":{"receipts":list(audited_receipts.values()),"unique_receipts":len(audited_receipts),"unique_local_modules":len(local_versions),
 "local_module_versions":dict(local_versions),"import_scope":"Recursively verifies every recorded local cache receipt and direct local import of its freshly compiled sources. Canonical/Mathlib boundaries are rehashed as recorded; no full transitive Mathlib rebuild/hash."},
 "collisions":{"batch":dup,"inherited_local":coll,"scope":"Explicit qualified declarations; no claim to scan all generated names or all canonical/Mathlib declarations."},
 "checks":checks,"failed_checks":[x for x in checks if not x["ok"]],"unique_files_measured":len(measured),
 "limitations":["No new build executed; evidence is source/log/PASS receipt inspection.","No original or existing file modified.","No um.py read/import/execution in this audit.","Named local instances are included in other_declarations.",
 "Auditor authored finite Hamiltonian/exponential and two derivative sources; their semantic independent review was performed by root. Six coordinate sources were semantically reviewed by root; this audit adds independent static evidence."],
 "semantic_reviews":{"PauliPerturbedDynamics":"FAVORABLE: beta_t(A)=u_t alpha_t(A)u_t*, group from the concrete cocycle, inverse/factor/isometry. Temporal continuity requires a continuous canonical orbit, proved for V. No perturbed KMS state or normality asserted.",
 "PauliCocycleGenerator":"FAVORABLE: actual finite-cutoff generator convergence and linear cutoff error derive the limit derivative at zero; cocycle law propagates the right ODE. Single-bond nontriviality means not identically one, not nonidentity at every nonzero time."}}
r1=new("AUDITORIA_ESTATICA_18_FONTES.json",json.dumps(result,ensure_ascii=False,indent=2)+"\n")
compact={"status":result["status"],"audit":r1,"inventory":measure(inventory_path),"counts":counts,
 "modules":[{"module":m["module"],"source":m["source"],"receipt":m["receipt"],"theorems":m["theorems"],"other_declarations":m["other_declarations"],"local_instances":m["local_instances"]}for m in modules]}
r2=new("FONTES_E_RECIBOS_18.json",json.dumps(compact,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"status":result["status"],"counts":counts,"failed_checks":result["failed_checks"],"checks":len(checks),
 "unique_files_measured":len(measured),"receipts":len(audited_receipts),"local_modules":len(local_versions),"outputs":[r1,r2]},ensure_ascii=False,indent=2))
