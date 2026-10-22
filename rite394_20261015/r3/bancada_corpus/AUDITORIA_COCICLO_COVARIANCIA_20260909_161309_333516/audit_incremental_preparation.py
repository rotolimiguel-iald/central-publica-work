"""Audit prepared incremental cache only. Never runs compiler, runner, adapter, or um.py."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import ast,hashlib,json,os,re,sys
sys.stdout.reconfigure(encoding="utf-8")
base=Path(r"C:\IALD\Central de Patentes\Chatgpt")
out=base/"AUDITORIA_COCICLO_COVARIANCIA_20260909_161309_333516"
adapter=base/"ADAPTADOR_INCREMENTAL_20260909_162620_395030"
rp=adapter/"RECIBO_PREPARACAO_INCREMENTAL.json"
pp=adapter/"BUILD_INCREMENTAL_20260909_162634_176093/BUILD_PLAN.json"
runner=adapter/"run_incremental.py"
checks=[];measured={}
def rec(p):
 p=Path(p);b=p.read_bytes();return {"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def measure(p):
 key=str(Path(p).resolve()).casefold()
 if key not in measured:measured[key]=rec(p)
 return measured[key]
def match(r):return measure(r["path"])==r
def ck(label,ok,detail=None):checks.append({"check":label,"ok":bool(ok),"detail":detail})
def read(p):measure(p);return json.loads(Path(p).read_text(encoding="utf-8"))
def key(p):return str(Path(p).resolve()).casefold()
r=read(rp);p=read(pp)
prior=read(p["cached_build_receipt"]["path"]);op=read(p["cached_build_plan"]["path"]);sp=read(p["source_build_plan"]["path"])
build=Path(p["build"]).resolve();oldbuild=Path(op["build"]).resolve();sourcebuild=Path(sp["build"]).resolve()
ck("prepared_receipt_status",r["status"]=="PASS_CACHE_COMPATIBILITY__PREPARED_21_NOT_EXECUTED")
ck("prepared_plan_pin",match(r["plan"])and Path(r["plan"]["path"]).resolve()==pp.resolve())
ck("prior_receipt_pin",match(p["cached_build_receipt"]))
ck("prior_plan_pin",match(p["cached_build_plan"])and prior["plan"]==measure(p["cached_build_plan"]["path"]))
ck("prior_PASS48",prior["status"]=="PASS_TRANSPOSED_SCOPE"and len(prior["runs"])==48 and prior["input_boundary_unchanged"])
ck("prior48_all_valid_zero",all(x["exit_code"]==0 and x["valid"]and x["warning_lines"]==0 for x in prior["runs"]))
ck("prior_axioms_standard",all(set(x["axioms"])<={"propext","Classical.choice","Quot.sound"}for run in prior["runs"]for x in run["axiom_rows"]))
ck("source_plan_pin",match(p["source_build_plan"])and r["source_plan"]==p["source_build_plan"])
ck("cached_receipt_plan_metadata_identical",p["cached_modules"]==r["cached_modules"])
ck("build_is_new_designated_directory",build==pp.parent.resolve()and build.parent==adapter.resolve()and build not in{oldbuild,sourcebuild})
oldboundary={key(x["path"]):x for x in op["external_boundary"]}
newboundary={key(x["path"]):x for x in sp["external_boundary"]}
ck("old_pin_set_in_new_pin_set",oldboundary.keys()<=newboundary.keys())
ck("1247_common_pins_identical",len(oldboundary)==1247 and all(newboundary.get(k)==v for k,v in oldboundary.items()))
ck("same_dependency_library_paths",op["environment_overrides"]["LEAN_PATH"].split(os.pathsep)[1:]==sp["environment_overrides"]["LEAN_PATH"].split(os.pathsep)[1:])
for collection in("sources","source_files","external_boundary","cached_boundary_records"):
 for x in p[collection]:ck(collection+":"+x["path"],match(x))
for name in("integration_result","integrated_copy"):ck("plan_pin:"+name,match(p[name]))
ck("66_sources_only_in_new_build",len(p["source_files"])==66 and all(Path(x["path"]).resolve().is_relative_to(build)for x in p["source_files"]))
sourcefiles={Path(x["path"]).resolve().relative_to(build).as_posix():x for x in p["source_files"]}
oldruns={x["module"]:x for x in prior["runs"]}
oldplanruns={x["module"]:x for x in op["runs"]}
sourceplanruns={x["module"]:x for x in sp["runs"]}
cached_names={x["module"]for x in p["cached_modules"]}
ck("45_unique_cache_modules",len(p["cached_modules"])==len(cached_names)==45)
cached_artifact_paths=set();cache_stats=[]
for cm in p["cached_modules"]:
 name=cm["module"];oldsrc=Path(cm["source"]["path"]);newsrc=Path(cm["new_plan_source"]["path"])
 ck(name+":source_records",match(cm["source"])and match(cm["new_plan_source"]))
 ck(name+":byte_equal_old_new_source",oldsrc.read_bytes()==newsrc.read_bytes())
 ck(name+":source_from_prior_PASS_build",oldsrc.resolve()==oldbuild/"TGLExt"/(name+".lean"))
 actual=(build/"TGLExt"/(name+".lean"))
 ck(name+":new_cache_source_byte_equal",actual.read_bytes()==oldsrc.read_bytes())
 ck(name+":prior_run_receipt_exact",cm["prior_run"]==oldruns[name]and cm["prior_run"]["valid"])
 ck(name+":expected_terms_same",oldplanruns[name]["expected_axiom_terms"]==sourceplanruns[name]["expected_axiom_terms"])
 ck(name+":required_binary_pair",{Path(a["source"]["path"]).suffix for a in cm["artifacts"]}>={".olean",".ilean"})
 for a in cm["artifacts"]:
  src=Path(a["source"]["path"]).resolve();copy=Path(a["copy"]["path"]).resolve()
  ck(name+":artifact_records:"+src.name,match(a["source"])and match(a["copy"]))
  ck(name+":artifact_bytes:"+src.name,src.read_bytes()==copy.read_bytes())
  ck(name+":artifact_provenance:"+src.name,src.parent==oldbuild/"TGLExt"and copy.parent==build/"TGLExt"and src.name==copy.name)
  cached_artifact_paths.add(key(copy))
 cache_stats.append({"module":name,"source":measure(oldsrc),"copied_source":measure(actual),"artifacts":cm["artifacts"]})
# The original new-plan overlay is predetermined canonical dependency material, not partial leaf outputs.
original_overlay_copy={key(x["copy"]["path"]):x for x in sp["dependency_overlay"]}
ck("588_predetermined_dependency_artifacts",len(original_overlay_copy)==588)
overlay_recorded=[]
for x in p["dependency_overlay"]:
 src=Path(x["source"]["path"]).resolve();dest=Path(x["copy"]["path"]).resolve()
 ck("overlay_dest_inside:"+dest.as_posix(),dest.is_relative_to(build))
 ck("overlay_pins:"+dest.as_posix(),match(x["source"])and match(x["copy"]))
 ck("overlay_bytes:"+dest.as_posix(),src.read_bytes()==dest.read_bytes())
 if x.get("kind")=="cached_reviewed_module":
  ck("overlay_prior_cache:"+dest.name,src.is_relative_to(oldbuild)and key(dest)in cached_artifact_paths)
 else:
  relative=dest.relative_to(build);intermediate=sourcebuild/relative
  ck("overlay_predetermined_source_plan:"+dest.name,key(intermediate)in original_overlay_copy)
  prior_item=original_overlay_copy.get(key(intermediate))
  if prior_item:ck("overlay_same_canonical_origin:"+dest.name,prior_item["source"]==x["source"]and prior_item["copy"]["sha256"]==x["copy"]["sha256"])
  ck("overlay_not_current_leaf_output:"+dest.name,not src.is_relative_to(sourcebuild)and not src.is_relative_to(build))
 overlay_recorded.append({"source":x["source"],"copy":x["copy"],"kind":x.get("kind","canonical_dependency")})
ck("90_cached_artifacts_678_overlay",len(cached_artifact_paths)==90 and len(p["dependency_overlay"])==678)
run_names=[x["module"]for x in p["runs"]]
ck("21_unique_new_runs",len(run_names)==len(set(run_names))==21)
ck("new_runs_exclude_cache",not cached_names.intersection(run_names))
ck("three_aggregate_runs_last",run_names[-3:]==["FullTGLExtRoot","FullTGLAudit","NewModulesAudit"])
inventory=read(base/"REEXAME_COCICLO_COVARIANCIA_20260909/INVENTARIO_FONTES.json")
expected18={Path(x["source"]).stem for x in inventory["modules"]if x["new_this_continuation"]}
ck("18_new_exact_inventory",set(run_names[:-3])==expected18)
commands=[]
for x in p["runs"]:
 cmd=x["command"];name=x["module"]
 ck("command_exact_lean_flags:"+name,len(cmd)==6 and cmd[1]=="-o"and cmd[3]=="-i"and Path(cmd[0]).name=="lean.exe")
 paths=[Path(cmd[2]).resolve(),Path(cmd[4]).resolve()]
 ck("command_outputs_only_newbuild:"+name,all(v.is_relative_to(build)for v in paths))
 rel=Path(cmd[-1]);source=(build/rel).resolve()
 ck("command_input_lean_inside:"+name,not rel.is_absolute()and source.is_relative_to(build)and source.suffix==".lean"and rel.as_posix()in sourcefiles)
 # Exact command of approved source-plan run, changing only its output root.
 priorcmd=sourceplanruns[name]["command"]
 remapped=[str(build/Path(a).resolve().relative_to(sourcebuild))if Path(a).is_absolute()and Path(a).resolve().is_relative_to(sourcebuild)else a for a in priorcmd]
 ck("command_exact_approved_remapping:"+name,cmd==remapped)
 ck("axiom_terms_exact_source_plan:"+name,x["expected_axiom_terms"]==sourceplanruns[name]["expected_axiom_terms"])
 commands.append({"module":name,"command":cmd,"expected_axiom_terms_count":len(x["expected_axiom_terms"])})
ded=p["runs"][-1];decl_names=p["declaration_names"]
ck("1098_dedicated_terms",len(decl_names)==len(set(decl_names))==1098 and Counter(ded["expected_axiom_terms"])==Counter(decl_names))
dt=(build/"NewModulesAudit.lean").read_text(encoding="utf-8")
ck("dedicated_source_prints1098",Counter(re.findall(r"(?m)^#print axioms ([\w.']+)$",dt))==Counter(decl_names))
ck("dedicated_has_all7instances",len(p["local_instance_names"])==7 and set(p["local_instance_names"])<=set(decl_names))
env=p["environment_overrides"]
ck("environment_first_library_newbuild",Path(env["LEAN_PATH"].split(os.pathsep)[0]).resolve()==build)
ck("environment_temp_src_only_newbuild",all(Path(env[k]).resolve()==build for k in["LEAN_SRC_PATH","TMP","TEMP"]))
ck("no_partial_current_build_in_library_paths",all(not Path(v).resolve().is_relative_to(sourcebuild)for v in env["LEAN_PATH"].split(os.pathsep)))
# Read-only control-flow inspection, not execution.
runner_record=measure(runner);rt=runner.read_text(encoding="utf-8");tree=ast.parse(rt)
ck("runner_AST_valid",isinstance(tree,ast.Module))
runfn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=="run")
calls=[n for n in ast.walk(runfn)if isinstance(n,ast.Call)]
ck("runner_only_subprocess_run",len([c for c in calls if isinstance(c.func,ast.Attribute)and isinstance(c.func.value,ast.Name)and c.func.value.id=="subprocess"and c.func.attr=="run"])==1)
ck("runner_verifies_cache_before_and_after",'for record in plan["cached_boundary_records"]:'in rt and 'cached_stable=all(rec(Path(r["path"]))==r for r in plan["cached_boundary_records"])'in rt)
ck("runner_checks_input_boundaries_before_and_after",'assert rec(Path(r["path"]))==r,"Prepared input changed: "+r["path"]'in rt and 'valid=valid and stable and cached_stable and len(results)==len(plan["runs"])'in rt)
ck("runner_no_um_import_execution",not any(isinstance(n,(ast.Import,ast.ImportFrom))and "um"in ast.unparse(n).split()for n in ast.walk(tree)))
ck("runner_subprocess_uses_plan_cwd",all(any(k.arg=="cwd"and isinstance(k.value,ast.Name)and k.value.id=="build"for k in c.keywords)for c in calls if isinstance(c.func,ast.Attribute)and isinstance(c.func.value,ast.Name)and c.func.value.id=="subprocess"))
ck("historical_binary_pin_limitation_explicit",p["scope"]["cache_binaries_historically_hashed_by_old_receipt"]is False and p["scope"]["cache_binary_hashes_measured_at_reuse"]is True)
for m in list(measured.values()):ck("stable_during_review:"+m["path"],rec(m["path"])==m)
result={"status":"PASS_STATIC_INCREMENTAL_PREPARATION_SCOPE"if all(x["ok"]for x in checks)else"FAIL_VISIBLE_INCREMENTAL_PREPARATION_AUDIT",
 "created_utc":datetime.now(timezone.utc).isoformat(),"phase":"Preparation and cache compatibility only; no claim about the currently running or future compilation outcome.",
 "counts":{"checks":len(checks),"passed_checks":sum(x["ok"]for x in checks),"cached_modules":len(cached_names),"cached_artifacts":len(cached_artifact_paths),"new_module_commands":len(run_names)-3,"aggregate_commands":3,"commands":len(run_names),"dedicated_terms":len(decl_names),"common_old_dependency_pins":len(oldboundary),"measured_files":len(measured)},
 "preparation_receipt":measure(rp),"plan":measure(pp),"runner":runner_record,"prior_PASS_receipt":measure(p["cached_build_receipt"]["path"]),
 "cache_modules":cache_stats,"commands":commands,"checks":checks,"failed_checks":[x for x in checks if not x["ok"]],
 "review":{"origin":"45 exact transposed sources and 90 byte-copied artifacts from the prior PASS48 build; no current partial leaf outputs are reused.",
 "pins":"Old/new canonical dependency pins agree. Inputs and cache are revalidated by the runner before and after execution.",
 "boundary":"All command outputs and logs are confined to the designated new incremental build. Existing frozen sources are read only.",
 "limitation":"The prior PASS48 receipt did not historically pin its generated binary hashes. Hashes are measured at reuse and preserved in the new plan; no claim of original compilation-time binary custody is made.",
 "independence":"Auditor did not execute prepare_incremental, run_incremental, Lean or any um.py."}}
path=out/"AUDITORIA_PREPARACAO_INCREMENTAL.json";tmp=path.with_name(path.name+".tmp");assert not path.exists()and not tmp.exists()
data=(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
with tmp.open("xb")as f:f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data;os.rename(tmp,path);assert path.read_bytes()==data
print(json.dumps({"status":result["status"],"counts":result["counts"],"failed_checks":result["failed_checks"],"output":rec(path)},ensure_ascii=False,indent=2))
