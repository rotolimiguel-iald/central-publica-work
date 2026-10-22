"""Run only the fresh incremental plan; never run/import um.py."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,re,subprocess,sys
BASE=Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
TRIO={"propext","Classical.choice","Quot.sound"}

def rec(p):
    b=p.read_bytes();return {"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}

def new(p,b):
    assert p.resolve().is_relative_to(BASE) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+".tmp")
    with t.open("xb") as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b
    os.rename(t,p);assert p.read_bytes()==b

def run(planpath):
    plan=json.loads(planpath.read_text(encoding="utf-8"));build=Path(plan["build"]).resolve()
    assert build.is_relative_to(BASE) and plan["status"]=="PREPARED_NOT_EXECUTED"
    assert len(plan["cached_modules"])==45 and len(plan["runs"])==21
    assert plan["cached_boundary_unchanged"]
    assert [r["module"] for r in plan["runs"][-3:]]==[
        "FullTGLExtRoot","FullTGLAudit","NewModulesAudit"]
    cached_names={m["module"] for m in plan["cached_modules"]}
    assert len(cached_names)==45 and not (cached_names & {r["module"] for r in plan["runs"]})
    for item in plan["runs"]:
        for flag in ["-o","-i"]:
            target=Path(item["command"][item["command"].index(flag)+1]).resolve()
            assert target.is_relative_to(build)
    for record in plan["cached_boundary_records"]:
        assert rec(Path(record["path"]))==record, "Cached boundary changed before execution"
    assert not list(build.glob("*.log")) and not (build/"TRANSPOSED_RESULT.json").exists()
    for r in plan["sources"]+plan["source_files"]+plan["external_boundary"]+[x["copy"] for x in plan["dependency_overlay"]]+[plan["integration_result"],plan["integrated_copy"]]:
        assert rec(Path(r["path"]))==r,"Prepared input changed: "+r["path"]
    env=os.environ.copy();env.update(plan["environment_overrides"])
    pattern=re.compile(r"'([\w.']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
    results=[];valid=True
    for item in plan["runs"]:
        try:
            proc=subprocess.run(item["command"],cwd=build,env=env,stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,timeout=300)
            data=proc.stdout;returncode=proc.returncode
        except subprocess.TimeoutExpired as fail:
            data=fail.stdout or b"";returncode="TIMEOUT_300_SECONDS"
        new(build/(item["module"]+".log"),data)
        text=data.decode("utf-8",errors="replace")
        rows=[{"name":m.group(1),"axioms":[a.strip() for a in (m.group(2) or "").split(",") if a.strip()]}
              for m in pattern.finditer(text)]
        expected=set(item["expected_axiom_terms"])
        observed={r["name"] for r in rows}
        missing=sorted(expected-observed)
        if item.get("kind")=="full_audit":
            sentinels_ok=all(token in text for token in item["expected_sentinels"])
            good=returncode==0 and not missing and sentinels_ok
            good=good and "sorryAx" not in text and "Lean.trustCompiler" not in text
        else:
            sentinels_ok=None
            good=returncode==0 and len(rows)==len(expected) and observed==expected
            good=good and not pattern.sub("",text).strip()
        good=good and all(set(r["axioms"])<=TRIO for r in rows)
        results.append({"module":item["module"],"exit_code":returncode,"valid":good,
                        "missing_axiom_terms":missing,"sentinels_ok":sentinels_ok,
                        "warning_lines":sum("warning:" in line for line in text.splitlines()),
                        "axiom_rows":rows})
        print(json.dumps({"module":item["module"],"exit_code":returncode,"valid":good,"rows":len(rows)}),flush=True)
        valid=valid and good
        if not good:print(text,flush=True);break
    stable=all(rec(Path(r["path"]))==r for r in plan["external_boundary"]+plan["sources"]+
               plan["source_files"]+[x["copy"] for x in plan["dependency_overlay"]]+[plan["integration_result"],plan["integrated_copy"]])
    cached_stable=all(rec(Path(r["path"]))==r for r in plan["cached_boundary_records"])
    valid=valid and stable and cached_stable and len(results)==len(plan["runs"])
    outcome={"status":"PASS_TRANSPOSED_SCOPE" if valid else "FAIL_VISIBLE","created_utc":datetime.now(timezone.utc).isoformat(),
             "plan":rec(planpath),"runs":results,"input_boundary_unchanged":stable,
             "cached_modules":plan["cached_modules"],
             "cached_build_receipt":plan["cached_build_receipt"],
             "cached_build_plan":plan["cached_build_plan"],
             "cached_boundary_unchanged":cached_stable,
             "new_module_processes":18,"aggregate_processes":3,
             "um_py_executed":False,"canonical_changes":False,"transitive_dependencies_all_hashed":False,
             "scope_note":"Incremental scope: 18 new transposed modules plus the copied TGLExt root, full TGL/Audit and dedicated 1098-declaration audit are compiled in 21 processes. The 45 previous modules are reused from the recorded PASS 48-process build after exact source-byte and dependency-pin comparison; their artifact hashes were measured at reuse and preserved by copying. Cached modules and canonical transitive sources are not rebuilt. Current canonical dependency pins and all copied/cache input records are checked before and after execution. um.py is never executed or imported."}
    new(build/"TRANSPOSED_RESULT.json",(json.dumps(outcome,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    print(json.dumps({"status":outcome["status"],"result":str(build/"TRANSPOSED_RESULT.json")}))
    return 0 if valid else 1
if __name__=="__main__":
    assert len(sys.argv)==2, "Pass the prepared incremental BUILD_PLAN.json"
    sys.exit(run(Path(sys.argv[1]).resolve()))
