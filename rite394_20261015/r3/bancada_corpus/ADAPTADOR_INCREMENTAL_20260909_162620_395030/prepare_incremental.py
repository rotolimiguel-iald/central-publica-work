"""Prepare only a fresh incremental build from frozen plans and PASS cache; no Lean/um.py execution."""
from pathlib import Path
from datetime import datetime,timezone
import copy,hashlib,json,os,sys
BASE=Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT=Path(__file__).resolve().parent
TRIO={"propext","Classical.choice","Quot.sound"}
def rec(p):
    b=p.read_bytes();return {"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def new(p,b):
    assert p.resolve().is_relative_to(OUT) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+".tmp")
    with t.open("xb") as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b
    os.rename(t,p);assert p.read_bytes()==b
def mapped(record,oldroot,newroot):
    p=Path(record["path"]).resolve();rel=p.relative_to(oldroot)
    assert rec(p)==record
    b=p.read_bytes();target=newroot/rel
    new(target,b);assert rec(p)==record and target.read_bytes()==b
    return rec(target)
def key(record):return str(Path(record["path"]).resolve()).casefold()
def main():
    assert len(sys.argv)==3
    sourceplan_path,cacheplan_path=[Path(x).resolve() for x in sys.argv[1:]]
    assert all(p.is_relative_to(BASE) for p in [sourceplan_path,cacheplan_path])
    sourceplan,cacheplan=read(sourceplan_path),read(cacheplan_path)
    cache_result_path=cacheplan_path.parent/"TRANSPOSED_RESULT.json"
    cache_result=read(cache_result_path)
    assert sourceplan["status"]==cacheplan["status"]=="PREPARED_NOT_EXECUTED"
    assert cache_result["status"]=="PASS_TRANSPOSED_SCOPE"
    assert cache_result["plan"]==rec(cacheplan_path)
    assert cache_result["input_boundary_unchanged"]
    assert len(cache_result["runs"])==len(cacheplan["runs"])
    assert all(r["exit_code"]==0 and r["valid"] and r["warning_lines"]==0 for r in cache_result["runs"])
    assert all(set(row["axioms"])<=TRIO for r in cache_result["runs"] for row in r["axiom_rows"])
    sourcebuild,cachebuild=[Path(p["build"]).resolve() for p in [sourceplan,cacheplan]]
    assert sourceplan_path.parent==sourcebuild and cacheplan_path.parent==cachebuild
    aggregate={"FullTGLExtRoot","FullTGLAudit","NewModulesAudit"}
    cache_runs={r["module"]:r for r in cacheplan["runs"] if r["module"] not in aggregate}
    fresh_runs={r["module"]:r for r in sourceplan["runs"] if r["module"] not in aggregate}
    assert len(cache_runs)==45 and len(fresh_runs)==63 and set(cache_runs)<=set(fresh_runs)
    oldboundary={key(r):r for r in cacheplan["external_boundary"]}
    newboundary={key(r):r for r in sourceplan["external_boundary"]}
    assert set(oldboundary)<=set(newboundary), "An old dependency pin is absent from the new plan"
    assert all(oldboundary[k]==newboundary[k] for k in oldboundary), "Cached/new dependency pins differ"
    assert sourceplan["environment_overrides"]["LEAN_PATH"].split(os.pathsep)[1:]==cacheplan["environment_overrides"]["LEAN_PATH"].split(os.pathsep)[1:]
    old_sources={str(Path(r["path"]).resolve().relative_to(cachebuild)):r for r in cacheplan["source_files"]}
    new_sources={str(Path(r["path"]).resolve().relative_to(sourcebuild)):r for r in sourceplan["source_files"]}
    verified=[]
    for module,prior_run in cache_runs.items():
        assert prior_run["expected_axiom_terms"]==fresh_runs[module]["expected_axiom_terms"]
        rel=str(Path("TGLExt")/(module+".lean"))
        oldrecord,newrecord=old_sources[rel],new_sources[rel]
        assert rec(Path(oldrecord["path"]))==oldrecord and rec(Path(newrecord["path"]))==newrecord
        assert Path(oldrecord["path"]).read_bytes()==Path(newrecord["path"]).read_bytes()
        verified.append({"module":module,"source":oldrecord,"new_plan_source":newrecord,
                         "source_bytes_identical":True,"prior_run":next(r for r in cache_result["runs"] if r["module"]==module)})
    build=OUT/("BUILD_INCREMENTAL_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"));build.mkdir()
    plan=copy.deepcopy(sourceplan)
    plan["created_utc"]=datetime.now(timezone.utc).isoformat()
    plan["build"]=build.as_posix()
    plan["source_files"]=[mapped(r,sourcebuild,build) for r in sourceplan["source_files"]]
    plan["dependency_overlay"]=[]
    for item in sourceplan["dependency_overlay"]:
        entry=copy.deepcopy(item)
        entry["copy"]=mapped(item["copy"],sourcebuild,build)
        plan["dependency_overlay"].append(entry)
    cache_boundary=[rec(sourceplan_path),rec(cacheplan_path),rec(cache_result_path),rec(Path(__file__).resolve())]
    for entry in verified:
        module=entry["module"];entry["artifacts"]=[]
        cache_boundary.append(entry["source"])
        for suffix in [".olean",".ilean",".olean.server",".olean.private"]:
            source=cachebuild/"TGLExt"/(module+suffix)
            if suffix in [".olean",".ilean"]:assert source.is_file(), "Missing required cache artifact"
            if not source.is_file():continue
            before=rec(source);target=build/"TGLExt"/source.name
            new(target,source.read_bytes());assert rec(source)==before
            copied=rec(target);assert copied["sha256"]==before["sha256"] and copied["bytes"]==before["bytes"]
            artifact={"source":before,"copy":copied};entry["artifacts"].append(artifact)
            cache_boundary.append(before)
            plan["dependency_overlay"].append({"module":module,"source":before,"copy":copied,"kind":"cached_reviewed_module"})
    plan["cached_modules"]=verified
    plan["cached_build_receipt"]=rec(cache_result_path)
    plan["cached_build_plan"]=rec(cacheplan_path)
    plan["source_build_plan"]=rec(sourceplan_path)
    plan["cached_boundary_records"]=cache_boundary
    plan["cached_boundary_unchanged"]=all(rec(Path(r["path"]))==r for r in cache_boundary)
    assert plan["cached_boundary_unchanged"]
    plan["external_boundary"]+=cache_boundary
    plan["runs"]=[]
    for item in sourceplan["runs"]:
        if item["module"] in cache_runs:continue
        entry=copy.deepcopy(item);command=[]
        for arg in entry["command"]:
            p=Path(arg)
            command.append(str(build/p.resolve().relative_to(sourcebuild)) if p.is_absolute() and p.resolve().is_relative_to(sourcebuild) else arg)
        entry["command"]=command;plan["runs"].append(entry)
    assert len(plan["runs"])==21 and {r["module"] for r in plan["runs"]}&aggregate==aggregate
    assert [r["module"] for r in plan["runs"][-3:]]==["FullTGLExtRoot","FullTGLAudit","NewModulesAudit"]
    env=plan["environment_overrides"]
    for name in ["LEAN_PATH","LEAN_SRC_PATH","TMP","TEMP"]:
        env[name]=env[name].replace(str(sourcebuild),str(build))
        assert str(sourcebuild) not in env[name]
    plan["scope"].update({"cached_modules":45,"new_module_processes":18,"aggregate_processes":3,
        "old_and_new_dependency_record_pins_identical":True,"old_external_dependency_pins_compared":len(oldboundary),
        "canonical_files_read_by_adapter":False,"canonical_pins_revalidated_by_runner_before_and_after":True,
        "cache_binary_hashes_measured_at_reuse":True,"cache_binaries_historically_hashed_by_old_receipt":False,
        "canonical_modules_rebuilt":False,"transitive_dependencies_all_hashed":False,"um_py_executed":False})
    for r in sourceplan["sources"]+[sourceplan["integration_result"],sourceplan["integrated_copy"]]:
        assert rec(Path(r["path"]))==r
    assert rec(sourceplan_path)==plan["source_build_plan"] and rec(cacheplan_path)==plan["cached_build_plan"]
    plan_path=build/"BUILD_PLAN.json"
    new(plan_path,(json.dumps(plan,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    receipt={"status":"PASS_CACHE_COMPATIBILITY__PREPARED_21_NOT_EXECUTED",
        "created_utc":datetime.now(timezone.utc).isoformat(),"plan":rec(plan_path),
        "source_plan":rec(sourceplan_path),"cached_build_receipt":rec(cache_result_path),
        "cached_modules":verified,"cached_boundary_unchanged":plan["cached_boundary_unchanged"],
        "counts":{"cached_modules":45,"new_modules":18,"new_processes":21,
            "source_files_copied":len(plan["source_files"]),"dependency_artifacts_copied":len(sourceplan["dependency_overlay"]),
            "cached_artifacts_copied":sum(len(v["artifacts"]) for v in verified),
            "old_dependency_pins_compared":len(oldboundary)},
        "scope":plan["scope"],
        "note":"Exact bytes of all 45 transposed Lean sources match the previous PASS build. Cache artifact hashes are measured now and byte-preserved; the previous receipt certifies runs/sources but did not pin generated binaries. All 63 modules remain loaded by the new root and both new audits. No current build outputs were read; only frozen source files and predetermined dependency-overlay entries from the current plan were copied."}
    new(OUT/"RECIBO_PREPARACAO_INCREMENTAL.json",(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    print(json.dumps({"status":receipt["status"],"plan":plan_path.as_posix(),"counts":receipt["counts"]}),flush=True)
if __name__=="__main__":main()
