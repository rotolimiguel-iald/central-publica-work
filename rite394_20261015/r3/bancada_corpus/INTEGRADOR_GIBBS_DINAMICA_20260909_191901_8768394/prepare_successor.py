"""Prepare a new successor overlay with all predecessor modules cached; no Lean/um.py execution."""
from pathlib import Path
from datetime import datetime,timezone
import ast,copy,hashlib,json,os,re,sys
from integrate_approved_copy import find_table,lean_declarations
BASE=Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT=Path(__file__).resolve().parent
TRIO={"propext","Classical.choice","Quot.sound"}
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def rec(p):
    b=p.read_bytes();return {"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def new(p,b):
    assert p.resolve().is_relative_to(OUT) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+".tmp")
    with t.open("xb") as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b
    os.rename(t,p);assert p.read_bytes()==b
def copied(source,target,expected=None):
    before=rec(source)
    if expected is not None:assert before==expected
    b=source.read_bytes();new(target,b)
    assert rec(source)==before and target.read_bytes()==b
    return {"source":before,"copy":rec(target)}
def certified_result(path):
    r=read(path)
    assert r["status"]=="PASS_TRANSPOSED_SCOPE" and r["input_boundary_unchanged"]
    assert all(x["valid"] and x["exit_code"]==0 and x["warning_lines"]==0 for x in r["runs"])
    assert all(set(row["axioms"])<=TRIO for x in r["runs"] for row in x["axiom_rows"])
    assert rec(Path(r["plan"]["path"]))==r["plan"]
    return r
def certified_provenance(path,seen=None):
    """Resolve each cached module to a fresh PASS run through all recorded generations."""
    seen=set() if seen is None else set(seen)
    key=str(path.resolve()).casefold()
    assert key not in seen, "Cyclic cache receipt lineage"
    seen.add(key)
    result=certified_result(path)
    assert result.get("cached_boundary_unchanged",True)
    plan=read(Path(result["plan"]["path"]));build=Path(plan["build"]).resolve()
    pins=[rec(path),result["plan"]]
    resolved={run["module"]:run for run in result["runs"]}
    assert len(resolved)==len(result["runs"])
    cached={item["module"]:item for item in result.get("cached_modules",[])}
    assert len(cached)==len(result.get("cached_modules",[])) and not(set(cached)&set(resolved))
    if cached:
        parent_record=result["cached_build_receipt"]
        parent_path=Path(parent_record["path"])
        assert rec(parent_path)==parent_record
        inherited,parent_pins=certified_provenance(parent_path,seen)
        parent_plan=read(Path(read(parent_path)["plan"]["path"]))
        parent_build=Path(parent_plan["build"]).resolve()
        source_pins={str(Path(r["path"]).resolve()).casefold():r for r in plan["source_files"]}
        parent_sources={str(Path(r["path"]).resolve()).casefold():r for r in parent_plan["source_files"]}
        pins.extend(parent_pins)
        for name,item in cached.items():
            assert name in inherited and item["prior_run"]==inherited[name], (
                "Inherited run differs from the recursively certified module: "+name)
            assert item["source_bytes_identical"]
            source=parent_build/"TGLExt"/(name+".lean")
            current=build/"TGLExt"/(name+".lean")
            assert rec(source)==item["source"]==parent_sources[str(source.resolve()).casefold()]
            assert rec(current)==source_pins[str(current.resolve()).casefold()]
            assert current.read_bytes()==source.read_bytes()
            pins.extend([rec(source),rec(current)])
            if "new_plan_source" in item:
                recorded=item["new_plan_source"]
                assert rec(Path(recorded["path"]))==recorded
                assert Path(recorded["path"]).read_bytes()==current.read_bytes()
                pins.append(recorded)
            for artifact in item["artifacts"]:
                src,dst=Path(artifact["source"]["path"]),Path(artifact["copy"]["path"])
                assert src.resolve().parent==parent_build/"TGLExt" and dst.resolve().parent==build/"TGLExt"
                assert src.name==dst.name and src.name in {
                    name+s for s in [".olean",".ilean",".olean.server",".olean.private"]}
                assert rec(src)==artifact["source"] and rec(dst)==artifact["copy"]
                assert src.read_bytes()==dst.read_bytes()
                pins.extend([artifact["source"],artifact["copy"]])
            resolved[name]=inherited[name]
    return resolved,pins

def embedded(path):
    return find_table(ast.parse(path.read_bytes().decode("utf-8")))[1]
def main():
    assert len(sys.argv)==4, "Pass successor copy folder, frozen predecessor plan and predecessor result."
    copyfolder,baseplanpath,baseresultpath=[Path(x).resolve() for x in sys.argv[1:]]
    assert all(p.is_relative_to(BASE) for p in [copyfolder,baseplanpath,baseresultpath])
    bp=read(baseplanpath);br=certified_result(baseresultpath)
    assert br["plan"]==rec(baseplanpath) and br.get("cached_boundary_unchanged",True)
    basebuild=Path(bp["build"]).resolve()
    baseintegrationpath=Path(bp["integration_result"]["path"]);assert rec(baseintegrationpath)==bp["integration_result"]
    bi=read(baseintegrationpath)
    baseprogram=Path(bp["integrated_copy"]["path"]);assert rec(baseprogram)==bp["integrated_copy"]==bi["integrated_copy"]
    integrationpath=copyfolder/"INTEGRATION_RESULT.json";nr=read(integrationpath)
    assert nr["status"]=="AST_AND_EMBEDDED_ROUND_TRIP_PASSED__NOT_EXECUTED"
    assert nr["source_um"]==rec(baseprogram)
    assert nr["predecessor_integration_result"]==rec(baseintegrationpath)
    assert nr["predecessor_build_result"]==rec(baseresultpath)
    program=Path(nr["integrated_copy"]["path"]);assert rec(program)==nr["integrated_copy"]
    old_embedded,all_embedded=embedded(baseprogram),embedded(program)
    oldmods,newmods=bp["modules"],nr["modules"]
    assert len(oldmods)==bp["counts"]["total_modules"]
    assert len(newmods)==nr["declaration_counts"]["modules"]
    oldnames={m["module"] for m in oldmods};newnames={m["module"] for m in newmods}
    assert len(oldnames)==len(oldmods) and len(newnames)==len(newmods) and not(oldnames&newnames)
    for k,v in old_embedded.items():
        if k not in {"TGLExt.lean","TGL/Audit.lean"}:assert all_embedded[k]==v
    assert set(all_embedded)==set(old_embedded)|{m["key"] for m in newmods}
    cache_by_name={m["module"]:m for m in br.get("cached_modules",[])}
    prior_runs={x["module"]:x for x in br["runs"]}
    assert oldnames<=set(cache_by_name)|set(prior_runs)
    resolved_runs,ancestry=certified_provenance(baseresultpath)
    assert oldnames<=set(resolved_runs)
    source_records={str(Path(r["path"]).resolve().relative_to(basebuild)):r for r in bp["source_files"]}
    modules=oldmods+newmods
    declarations=[d["name"] for m in modules for d in m["declarations"]]
    assert len(declarations)==len(set(declarations))
    build=OUT/("BUILD_SUCCESSOR_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"));build.mkdir()
    sources=[]
    for m in modules:
        text=all_embedded[m["key"]]
        ds=lean_declarations(text)
        assert [{"kind":k,"name":m["namespace"]+"."+n} for k,n in ds]==m["declarations"]
        if m["module"] in oldnames:
            sr=source_records[str(Path(m["key"]))]
            origin=Path(sr["path"]);assert rec(origin)==sr
            assert origin.read_bytes()==text.encode("utf-8")
            expected={d["name"] for d in m["declarations"]}
            run=resolved_runs[m["module"]]
            assert run and run["valid"] and run["exit_code"]==0
            assert {r["name"] for r in run["axiom_rows"]}==expected
        else:
            origin=copyfolder/"transposed_sources"/m["key"]
            assert origin.read_bytes()==text.encode("utf-8")
        copied(origin,build/m["key"]);sources.append(rec(origin))
    for key in ["TGLExt.lean","TGL/Audit.lean"]:new(build/key,all_embedded[key].encode("utf-8"))
    audit="\n".join("import TGLExt."+m["module"] for m in modules)+"\n"
    audit+="\n".join("#print axioms "+d for d in declarations)+"\n"
    new(build/"NewModulesAudit.lean",audit.encode("utf-8"))
    overlays=[];canonical_names=set()
    for item in bp["dependency_overlay"]:
        if item["module"] in oldnames:continue
        origin=Path(item["copy"]["path"]);relative=origin.resolve().relative_to(basebuild)
        artifact=copied(origin,build/relative,item["copy"])
        overlays.append({"module":item["module"],**artifact,"kind":"prior_canonical_overlay"})
        canonical_names.add(item["module"])
    cache_boundary=[rec(baseplanpath),rec(baseresultpath),rec(baseintegrationpath),rec(baseprogram)]+ancestry
    cached=[]
    for m in oldmods:
        name=m["module"];source=basebuild/m["key"];cache_boundary.append(rec(source))
        entry={"module":name,"source":rec(source),"new_plan_source":rec(build/m["key"]),
            "source_bytes_identical":True,"prior_run":resolved_runs[name],
            "prior_origin":"previous fresh module" if name in prior_runs else "previous verified cache",
            "artifact_historical_pin_available":name in cache_by_name,"artifacts":[]}
        for suffix in [".olean",".ilean",".olean.server",".olean.private"]:
            origin=basebuild/"TGLExt"/(name+suffix)
            if suffix in [".olean",".ilean"]:assert origin.is_file()
            if not origin.is_file():continue
            artifact=copied(origin,build/"TGLExt"/origin.name)
            if name in cache_by_name:
                historical=[a["copy"] for a in cache_by_name[name]["artifacts"] if Path(a["copy"]["path"]).name==origin.name]
                assert historical==[artifact["source"]]
            entry["artifacts"].append(artifact);cache_boundary.append(artifact["source"])
            overlays.append({"module":name,**artifact,"kind":"cached_reviewed_module"})
        cached.append(entry)
    config_path=copyfolder/"CONFIG_APROVADA.json";cfg=read(config_path)
    kernel=Path(cfg["canonical_kernel"]).resolve()
    boundary=list(bp["external_boundary"])+cache_boundary+[rec(config_path)]
    for m in newmods:
        for module in re.findall(r"(?m)^import ([\w.]+)$",all_embedded[m["key"]]):
            if module in {"TGLExt."+name for name in oldnames|newnames}:continue
            if module.startswith(("TGLExt.","TGL.")):
                assert module in canonical_names, "New canonical dependency absent from preserved overlay: "+module
                package=kernel
            else:
                assert module.startswith("Mathlib."), "Unreviewed import path: "+module
                package=kernel/".lake/packages/mathlib"
            source=package/(module.replace(".","/")+".lean")
            binary=package/".lake/build/lib/lean"/(module.replace(".","/")+".olean")
            for origin in [source,binary]+[Path(str(binary)+suffix) for suffix in [".server",".private"] if Path(str(binary)+suffix).is_file()]:
                boundary.append(rec(origin))
    dedup={}
    for r in boundary:
        key=str(Path(r["path"]).resolve()).casefold()
        if key in dedup:assert dedup[key]==r
        dedup[key]=r
    boundary=list(dedup.values())
    lean=bp["runs"][0]["command"][0]
    runs=[]
    for m in newmods:
        target=build/m["key"]
        runs.append({"module":m["module"],"command":[lean,"-o",str(target.with_suffix(".olean")),"-i",str(target.with_suffix(".ilean")),m["key"]],
                     "expected_axiom_terms":[d["name"] for d in m["declarations"]]})
    runs.append({"module":"FullTGLExtRoot","command":[lean,"-o",str(build/"TGLExt.olean"),"-i",str(build/"TGLExt.ilean"),"TGLExt.lean"],"expected_axiom_terms":[]})
    tree=ast.parse(program.read_bytes().decode("utf-8"))
    nodes=[n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="_LEAN_SENTINELS" for t in n.targets)]
    assert len(nodes)==1
    runs.append({"module":"FullTGLAudit","kind":"full_audit","command":[lean,"-o",str(build/"TGL/Audit.olean"),"-i",str(build/"TGL/Audit.ilean"),"TGL/Audit.lean"],
        "expected_axiom_terms":re.findall(r"(?m)^#print axioms ([\w.']+)\s*$",all_embedded["TGL/Audit.lean"]),"expected_sentinels":ast.literal_eval(nodes[0])})
    runs.append({"module":"NewModulesAudit","command":[lean,"-o",str(build/"NewModulesAudit.olean"),"-i",str(build/"NewModulesAudit.ilean"),"NewModulesAudit.lean"],"expected_axiom_terms":declarations})
    env=copy.deepcopy(bp["environment_overrides"])
    for name in ["LEAN_PATH","LEAN_SRC_PATH","TMP","TEMP"]:env[name]=env[name].replace(str(basebuild),str(build))
    theorem_count=sum(d["kind"]=="theorem" for m in modules for d in m["declarations"])
    counts={"cached_modules":len(oldmods),"new_modules":len(newmods),"new_processes":len(runs),"total_modules":len(modules),"theorems":theorem_count,"other_declarations":len(declarations)-theorem_count,"all_declarations":len(declarations)}
    stable=all(rec(Path(r["path"]))==r for r in cache_boundary)
    assert stable and rec(program)==nr["integrated_copy"]
    plan={"status":"PREPARED_NOT_EXECUTED","created_utc":datetime.now(timezone.utc).isoformat(),"build":build.as_posix(),
        "integration_result":rec(integrationpath),"integrated_copy":rec(program),"modules":modules,
        "sources":sources,"source_files":[rec(p) for p in build.rglob("*.lean")],"runs":runs,
        "dependency_overlay":overlays,"external_boundary":boundary,"environment_overrides":env,
        "declaration_names":declarations,"cached_modules":cached,"cached_build_receipt":rec(baseresultpath),
        "cached_build_plan":rec(baseplanpath),"cached_boundary_records":cache_boundary,"cached_boundary_unchanged":stable,
        "counts":counts,"new_module_processes":len(newmods),"aggregate_processes":3,
        "cache_ancestry_records":ancestry,
        "scope_note":f"Incremental successor: {len(newmods)} new modules and three fresh root/audit processes; {len(oldmods)} modules reused with exact source equality and verified prior PASS provenance. All {len(declarations)} declarations are audited in the new dedicated audit. Cached/canonical transitive sources are not rebuilt. Artifact hashes are measured at reuse; historical cache pins are separately identified. No um.py execution or import.",
        "scope":{"um_py_executed":False,"canonical_changes":False,"transitive_dependencies_rebuilt":False,"transitive_dependencies_all_hashed":False}}
    path=build/"BUILD_PLAN.json";new(path,(json.dumps(plan,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    receipt={"status":"PREPARED_SUCCESSOR_CACHE_SCOPE_NOT_EXECUTED","created_utc":datetime.now(timezone.utc).isoformat(),
        "plan":rec(path),"counts":counts,"cached_build_receipt":rec(baseresultpath),"cached_boundary_unchanged":stable,
        "previous_fresh_modules":sum(m["prior_origin"]=="previous fresh module" for m in cached),
        "previous_cached_modules":sum(m["prior_origin"]=="previous verified cache" for m in cached),
        "um_py_executed_or_imported":False,"lean_executed":False}
    new(OUT/"RECIBO_PREPARACAO_SUCESSORA.json",(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    print(json.dumps({"status":receipt["status"],"plan":path.as_posix(),"counts":counts}),flush=True)
if __name__=="__main__":main()
