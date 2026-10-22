"""Static audit only. Never imports or executes um.py; outputs only new Chatgpt files."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter,defaultdict
import ast,hashlib,json,os,re,sys
sys.stdout.reconfigure(encoding="utf-8")
base=Path(r"C:\IALD\Central de Patentes\Chatgpt")
out=base/"PROGRESSO_ATLAS_PERTURBACOES_20260909_145303_940722"
assert out.is_dir() and out.parent==base
groups=["NATURALIDADE_ESCALAR_EINSTEIN_20260909_145442_429378"]
allowed_axioms={"propext","Classical.choice","Quot.sound"}
checks=[]; measured={}; modules=[]; all_names=[]; boundaries={}; cached_paths={}
def record(p):
 p=Path(p);raw=p.read_bytes()
 return {"path":p.as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
def check(label,ok,detail=None):
 checks.append({"label":label,"ok":bool(ok),"detail":detail})
def measure(p):
 p=Path(p);key=str(p.resolve()).lower()
 if key not in measured:measured[key]=record(p)
 return measured[key]
def recorded_matches(r):
 m=measure(r["path"])
 return m["bytes"]==r["bytes"] and m["sha256"]==r["sha256"]
def new(p,raw):
 assert p.parent==out and not p.exists()
 t=p.with_name(p.name+".tmp");assert not t.exists()
 with t.open("xb")as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==raw;os.rename(t,p);assert p.read_bytes()==raw
def strip_comments(s):
 s=re.sub(r"/-.*?-/",lambda m:"\n"*m.group(0).count("\n"),s,flags=re.S)
 return re.sub(r"(?m)--.*$","",s)
decl_pattern=re.compile(r"^(?:(?:noncomputable|private|protected)\s+)*(theorem|lemma|def|abbrev|structure|class|instance|opaque|axiom)\s+([\w'.]+)")
def declarations(s):
 # Names of explicit declarations only. Generated recursors/projections are outside this scan.
 scopes=[];res=[]
 for ln,line in enumerate(strip_comments(s).splitlines(),1):
  n=re.match(r"^namespace\s+([\w'.]+)",line)
  if n:scopes.append(("namespace",n.group(1)));continue
  if re.match(r"^(?:noncomputable\s+)?section(?:\s|$)",line):
   scopes.append(("section",""));continue
  if re.match(r"^mutual(?:\s|$)",line):scopes.append(("section",""));continue
  if re.match(r"^end(?:\s|$)",line):
   if scopes:scopes.pop()
   continue
  m=decl_pattern.match(line)
  if m:
   prefix=".".join(x[1]for x in scopes if x[0]=="namespace")
   name=m.group(2)
   qual=name[len("_root_."):]if name.startswith("_root_.")else prefix+"."+name if prefix else name
   res.append({"kind":m.group(1),"name":qual,"short":name,"line":ln})
 return res
log_pattern=re.compile(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
receipt_cache={}
def receipt(p):
 p=Path(p);key=str(p.resolve()).lower()
 if key not in receipt_cache:
  receipt_cache[key]={"record":measure(p),"data":json.loads(p.read_text(encoding="utf-8"))}
 return receipt_cache[key]["data"]
for group in groups:
 folder=base/group
 for source in sorted(folder.glob("*.lean")):
  raw=source.read_bytes();s=raw.decode("utf-8");sm=measure(source)
  ds=declarations(s);names=[d["name"]for d in ds];all_names+=names
  candidates=[]
  for rp in sorted(folder.glob("BUILD*/BUILD_RESULT.json")):
   r=receipt(rp)
   if r.get("status")=="PASS_COMPILED_SCOPE" and any(
      Path(q["path"]).stem==source.stem and q["sha256"]==sm["sha256"] for q in r.get("sources",[])):
    if any(x["module"]==source.stem and x["exit_code"]==0 for x in r["runs"]):candidates.append(rp)
  check(source.stem+":current_source_has_PASS",bool(candidates))
  if not candidates:continue
  rp=candidates[-1];r=receipt(rp);build=rp.parent
  check(source.stem+":source_equals_PASS_copy",raw==(build/source.name).read_bytes())
  source_entry=next(q for q in r["sources"]if Path(q["path"]).stem==source.stem)
  check(source.stem+":source_record_matches",recorded_matches(source_entry))
  log_path=build/(source.stem+".log");log=log_path.read_text(encoding="utf-8")
  log_rows=[{"name":m.group(1),"axioms":[x.strip()for x in (m.group(2)or"").split(",")if x.strip()]}for m in log_pattern.finditer(log)]
  check(source.stem+":log_only_axiom_output",not log_pattern.sub("",log).strip())
  check(source.stem+":all_declarations_audited",Counter(names)==Counter(x["name"]for x in log_rows))
  check(source.stem+":axioms_standard",all(set(x["axioms"])<=allowed_axioms for x in log_rows))
  subset=[x for x in r["axiom_rows"]if x["name"]in names]
  check(source.stem+":log_rows_equal_receipt",log_rows==subset)
  prints=re.findall(r"(?m)^#print axioms ([\w'.]+)\s*$",s)
  check(source.stem+":print_count",len(prints)==len(ds))
  check(source.stem+":no_proof_placeholder",not re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b",strip_comments(s)))
  check(source.stem+":all_receipt_runs_exit_zero",all(x["exit_code"]==0 for x in r["runs"]))
  check(source.stem+":recorded_boundary_unchanged",r.get("external_boundary_unchanged")==True)
  # Receipt totals concern every freshly compiled source in that receipt (some builds contain two).
  rd=[]
  for sr in r["sources"]:
   rd+=declarations((build/Path(sr["path"]).name).read_text(encoding="utf-8"))
  check(source.stem+":receipt_counts_from_sources",
    r["theorems"]==sum(x["kind"]in{"theorem","lemma"}for x in rd)
    and r["definitions"]==sum(x["kind"]not in{"theorem","lemma"}for x in rd))
  cache_results=[]
  for c in r.get("cached_local_modules",[]):
   cr=c["receipt"];ok_receipt=recorded_matches(cr)
   cr_data=receipt(cr["path"])
   ok_status=cr_data.get("status")=="PASS_COMPILED_SCOPE"
   check(source.stem+":cached_PASS:"+c["module"],ok_receipt and ok_status)
   artifact_results=[]
   for a in c["artifacts"]:
    ap=Path(a["path"]);am=measure(ap)
    matching=recorded_matches(a)
    mirror=build/ap.name
    mirror_match=mirror.is_file() and mirror.read_bytes()==ap.read_bytes()
    check(source.stem+":cached_artifact:"+c["module"]+ap.suffix,matching and mirror_match)
    cached_paths[str(ap.resolve()).lower()]=ap
    artifact_results.append({"recorded":a,"measured":am,"hash_matches":matching,"build_copy":measure(mirror)if mirror.exists()else None,"copy_equal":mirror_match})
   csrc=next(a for a in c["artifacts"]if a["path"].endswith(".lean"))
   check(source.stem+":cached_source_in_PASS:"+c["module"],
     any(q["sha256"]==csrc["sha256"] and Path(q["path"]).stem==c["module"]for q in cr_data["sources"]))
   cache_results.append({"module":c["module"],"receipt":measure(cr["path"]),"record_matches":ok_receipt,"status":cr_data["status"],"artifacts":artifact_results})
  for b in r.get("external_boundary",[]):
   key=str(Path(b["path"]).resolve()).lower()
   if key not in boundaries:boundaries[key]={"recorded":b,"measured":measure(b["path"]),"matches":recorded_matches(b)}
   check(source.stem+":external_record:"+str(b["path"]),recorded_matches(b))
  arts=[]
  for suffix in [".lean",".log",".olean",".ilean",".olean.server",".olean.private"]:
   q=build/(source.stem+suffix)
   if q.is_file():arts.append(measure(q))
  modules.append({"group":group,"module":source.stem,"source":sm,"receipt":measure(rp),"build":build.as_posix(),
    "theorems":sum(d["kind"]in{"theorem","lemma"}for d in ds),"others":sum(d["kind"]not in{"theorem","lemma"}for d in ds),
    "declarations":ds,"axiom_rows":log_rows,"artifacts_measured_now":arts,"cached_modules":cache_results,
    "receipt_scope":r.get("scope"),"receipt_scope_note":r.get("scope_note")})
duplicates={k:v for k,v in Counter(all_names).items()if v>1}
check("batch:no_full_name_collisions",not duplicates,duplicates)
# Canonical program: bytes/AST only. No eval, import, compilation or execution.
canonical=Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/um.py")
canonical_before=record(canonical);text=canonical.read_text(encoding="utf-8-sig")
tree=ast.parse(text,filename=str(canonical));table=None
for node in tree.body:
 targets=node.targets if isinstance(node,ast.Assign)else[node.target]if isinstance(node,ast.AnnAssign)else[]
 if any(isinstance(n,ast.Name)and n.id=="_EMBEDDED_KERNEL_FILES"for n in targets):
  table=ast.literal_eval(node.value);break
check("canonical:embedded_table_present",isinstance(table,dict))
baseline_path=base/"DELTA_V337_LIDO_20260909_141248_520198/DELTA_V337.json"
baseline=json.loads(baseline_path.read_text(encoding="utf-8"))
same_v337=canonical_before["sha256"]==baseline["live_source"]["sha256"] and canonical_before["bytes"]==baseline["live_source"]["bytes"]
check("canonical:unchanged_from_v337",same_v337)
canonical_names=defaultdict(list)
for name,src in (table or {}).items():
 if name.endswith(".lean") and isinstance(src,str):
  for d in declarations(src):canonical_names[d["name"]].append(name)
canonical_collisions={name:canonical_names[name]for name in set(all_names)if name in canonical_names}
check("batch:no_explicit_full_names_in_canonical",not canonical_collisions,canonical_collisions)
# Compare inherited local sources, excluding byte-identical copies of the current audited modules.
new_by_stem={m["module"]:m["source"]["sha256"]for m in modules}
inherited=defaultdict(list);seen_src=set()
for cp in cached_paths.values():
 if cp.suffix!=".lean":continue
 cm=measure(cp)
 if (cp.stem,cm["sha256"])in seen_src:continue
 seen_src.add((cp.stem,cm["sha256"]))
 if cp.stem in new_by_stem:
  check("cache:same_audited_source:"+cp.stem,cm["sha256"]==new_by_stem[cp.stem]);continue
 for d in declarations(cp.read_text(encoding="utf-8")):inherited[d["name"]].append(cp.as_posix())
inherited_collisions={name:inherited[name]for name in set(all_names)if name in inherited}
check("batch:no_full_names_in_inherited_local_cache",not inherited_collisions,inherited_collisions)
canonical_after=record(canonical)
check("canonical:stable_during_audit",canonical_before==canonical_after)
check("batch:one_module",len(modules)==1)
prior_path=out/"AUDITORIA_ESTATICA_CONTINUACAO.json"
prior=json.loads(prior_path.read_text(encoding="utf-8"))
prior_names={d["name"]for m in prior["modules"]for d in m["declarations"]}
previous_collisions=sorted(set(all_names)&prior_names)
check("addendum:no_full_name_collisions_with_prior_eleven",not previous_collisions,previous_collisions)
totals={"modules":len(modules),"theorems":sum(m["theorems"]for m in modules),"other_declarations":sum(m["others"]for m in modules),"audited_declarations":sum(len(m["axiom_rows"])for m in modules)}
group_totals=[]
for name in groups:
 ms=[m for m in modules if m["group"]==name]
 group_totals.append({"group":name,"modules":len(ms),"theorems":sum(m["theorems"]for m in ms),"others":sum(m["others"]for m in ms)})
result={"status":"PASS_STATIC_EVIDENCE_AUDIT"if all(c["ok"]for c in checks)else"FAIL_VISIBLE_STATIC_AUDIT",
 "created_utc":datetime.now(timezone.utc).isoformat(),"totals":totals,"groups":group_totals,
 "modules":modules,"checks":checks,"failed_checks":[c for c in checks if not c["ok"]],
 "full_name_collisions":{"within_batch":duplicates,"with_canonical_embedded":canonical_collisions,"with_inherited_local_cache":inherited_collisions,
 "scope":"Explicit top-level Lean declarations scanned statically; generated recursors/projections and the entire transitive Mathlib namespace are outside this name scan."},
 "canonical":{"before":canonical_before,"after":canonical_after,"v337_baseline_receipt":measure(baseline_path),"matches_v337":same_v337,"embedded_count":len(table or {}),"delta_examined_this_audit":False if same_v337 else None,"um_py_executed_or_imported":False},
 "external_boundary_records_remeasured":list(boundaries.values()),
 "artifact_counts":{"unique_paths_measured":len(measured),"unique_cached_artifact_paths":len(cached_paths),"unique_receipts_read":len(receipt_cache),"unique_direct_boundary_paths":len(boundaries)},
 "exclusions":["This is an incremental audit after the separate 11-module snapshot; the earlier audit is preserved unchanged.","No new compile in this audit; PASS receipts and logs inspected.","No full rebuild/hash of every transitive dependency.","New theorem counts exclude all inherited cached modules.","No original or existing file modified."],
 "auditor_role":"Independent static/evidence and full-source semantic review of the scalar/Einstein Lie module. Earlier 11-module audit preserved unchanged."}
result["previous_audit"]=measure(prior_path)
result["full_name_collisions"]["with_previous_eleven"]=previous_collisions
result["combined_totals"]={k:totals[k]+prior["totals"][k]for k in totals}
new(out/"ADENDO_EVIDENCIA_EINSTEIN_LIE.json",(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"status":result["status"],"totals":totals,"groups":group_totals,"failed_checks":result["failed_checks"],"checks":len(checks),"artifact_counts":result["artifact_counts"],"canonical":result["canonical"],"output":record(out/"ADENDO_EVIDENCIA_EINSTEIN_LIE.json")},ensure_ascii=False,indent=2))
