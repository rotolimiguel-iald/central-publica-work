"""Prepare/run a fresh build of transposed modules; never run either um.py."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os,re,subprocess,sys
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

def lean_declarations(text):
    """Read the reviewed one-namespace source convention, including named local instances."""
    pattern=re.compile(r"(?m)^(?:noncomputable[ \t]+)?"
        r"(abbrev|def|structure|theorem|local[ \t]+instance)[ \t]+"
        r"([^\W\d]\w*'*)(?=[ \t\r\n:({\[])")
    declarations=[(re.sub(r"[ \t]+"," ",m.group(1)),m.group(2))
                  for m in pattern.finditer(text)]
    names=[name for _,name in declarations]
    assert len(names)==len(set(names)), "Duplicate declaration names"
    # Reject anonymous/scoped/other instance syntax instead of silently omitting it.
    instance_headers=re.findall(r"(?m)^[ \t]*(?:(?:local|scoped|noncomputable|"
        r"private|protected)[ \t]+)*instance\b[^\r\n]*",text)
    local_instances=[name for kind,name in declarations if kind=="local instance"]
    assert len(instance_headers)==len(local_instances), (
        "Every instance must be a named top-level 'local instance NAME'; explicit review required")
    prints=re.findall(r"(?m)^#print axioms ([\w.']+)[ \t]*$",text)
    assert len(prints)==len(set(prints)) and set(prints)==set(names), (
        "Every declaration, including each local instance, requires exactly one #print axioms")
    return declarations

def prepare(folder):
    folder=folder.resolve();assert folder.is_relative_to(BASE)
    result_path=folder/"INTEGRATION_RESULT.json"
    result=json.loads(result_path.read_text(encoding="utf-8"))
    assert result["status"]=="AST_AND_EMBEDDED_ROUND_TRIP_PASSED__NOT_EXECUTED"
    program=Path(result["integrated_copy"]["path"])
    assert rec(program)==result["integrated_copy"]
    tree=ast.parse(program.read_bytes().decode("utf-8"))
    tables=[n.value for n in tree.body if isinstance(n,ast.Assign) and
      any(isinstance(t,ast.Name) and t.id=="_EMBEDDED_KERNEL_FILES" for t in n.targets)]
    assert len(tables)==1
    embedded=ast.literal_eval(tables[0])
    kernel=Path(result["source_um"]["path"]).parent/"tgl_kernel"
    lean=Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe")
    build=folder/("BUILD_TRANSPOSED_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    build.mkdir(exist_ok=False)
    modules=result["modules"];names={m["module"] for m in modules};boundary=[lean,kernel/"lean-toolchain",kernel/"lake-manifest.json"]
    runs=[];source_records=[]
    for m in modules:
        source=folder/"transposed_sources"/m["key"]
        data=source.read_bytes();text=data.decode("utf-8")
        assert text==embedded[m["key"]]
        declarations=lean_declarations(text)
        expected_declarations=[{"kind":kind,"name":m["namespace"]+"."+name}
                               for kind,name in declarations]
        assert m["declarations"]==expected_declarations, (
            "Source declarations differ from frozen integration metadata: "+m["module"])
        assert not re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b",text)
        target=build/m["key"];new(target,data);source_records.append(rec(source))
        for module in re.findall(r"(?m)^import ([\w.]+)$",text):
            if module.startswith("TGLExt.") and module.split(".")[-1] in names:continue
            package=kernel if module.startswith(("TGLExt.","TGL.")) else kernel/".lake/packages/mathlib"
            binary=package/".lake/build/lib/lean"/(module.replace(".","/")+".olean")
            boundary.extend([package/(module.replace(".","/")+".lean"),binary])
            for suffix in [".server",".private"]:
                sibling=Path(str(binary)+suffix)
                if sibling.is_file():boundary.append(sibling)
        command=[str(lean),"-o",str(target.with_suffix(".olean")),"-i",str(target.with_suffix(".ilean")),m["key"]]
        runs.append({"module":m["module"],"command":command,
            "expected_axiom_terms":[d["name"] for d in m["declarations"]]})
    # Lean resolves a top-level namespace to its first matching library directory.
    # A new local TGLExt directory therefore needs an isolated binary overlay.
    # Copy bytes, never link canonical paths: only the reachable local import closure.
    queue=[]
    for m in modules:
        queue+=re.findall(r"(?m)^import ([\w.]+)$",(build/m["key"]).read_text(encoding="utf-8"))
    for key in ["TGLExt.lean","TGL/Audit.lean"]:
        new(build/key,embedded[key].encode("utf-8"))
        queue+=re.findall(r"(?m)^import ([\w.]+)$",embedded[key])
    local_full={"TGLExt."+m["module"] for m in modules}|{"TGLExt","TGL.Audit"}
    visited=set();overlay=[]
    while queue:
        module=queue.pop()
        if module in visited or module in local_full:continue
        if not (module.startswith(("TGLExt.","TGL.")) or module in ("TGLExt","TGL")):continue
        visited.add(module)
        source=kernel/(module.replace(".","/")+".lean")
        boundary.append(source)
        queue+=re.findall(r"(?m)^import ([\w.]+)$",source.read_text(encoding="utf-8"))
        binary=kernel/".lake/build/lib/lean"/(module.replace(".","/")+".olean")
        assert binary.is_file(),"Missing canonical compiled dependency "+module
        for original in [binary]+[Path(str(binary)+suffix) for suffix in [".server",".private"]
                                 if Path(str(binary)+suffix).is_file()]:
            boundary.append(original);snapshot=rec(original);data=original.read_bytes()
            target=build/original.relative_to(kernel/".lake/build/lib/lean")
            new(target,data)
            assert rec(original)==snapshot
            overlay.append({"module":module,"source":snapshot,"copy":rec(target)})
    sentinel_nodes=[n.value for n in tree.body if isinstance(n,ast.Assign) and
      any(isinstance(t,ast.Name) and t.id=="_LEAN_SENTINELS" for t in n.targets)]
    assert len(sentinel_nodes)==1
    runs.append({"module":"FullTGLExtRoot","command":[str(lean),"-o",str(build/"TGLExt.olean"),
                 "-i",str(build/"TGLExt.ilean"),"TGLExt.lean"],"expected_axiom_terms":[]})
    runs.append({"module":"FullTGLAudit","kind":"full_audit",
                 "command":[str(lean),"-o",str(build/"TGL/Audit.olean"),
                            "-i",str(build/"TGL/Audit.ilean"),"TGL/Audit.lean"],
                 "expected_axiom_terms":re.findall(r"(?m)^#print axioms ([\w.']+)\s*$",embedded["TGL/Audit.lean"]),
                 "expected_sentinels":ast.literal_eval(sentinel_nodes[0])})
    declaration_names=[d["name"] for m in modules for d in m["declarations"]]
    assert len(declaration_names)==len(set(declaration_names))
    if "all_declaration_names" in result:
        assert set(declaration_names)==set(result["all_declaration_names"])
        assert len(declaration_names)==len(result["all_declaration_names"])
    text="\n".join("import TGLExt."+m["module"] for m in modules)+"\n"
    text+="\n".join("#print axioms "+n for n in declaration_names)+"\n"
    new(build/"NewModulesAudit.lean",text.encode("utf-8"))
    runs.append({"module":"NewModulesAudit","command":[str(lean),"-o",str(build/"NewModulesAudit.olean"),
                 "-i",str(build/"NewModulesAudit.ilean"),"NewModulesAudit.lean"],
                 "expected_axiom_terms":declaration_names})
    packages=sorted(p for p in (kernel/".lake/packages").iterdir() if p.is_dir())
    libraries=[kernel/".lake/build/lib/lean"]+[p/".lake/build/lib/lean" for p in packages if (p/".lake/build/lib/lean").is_dir()]
    plan={"status":"PREPARED_NOT_EXECUTED","created_utc":datetime.now(timezone.utc).isoformat(),
          "integration_result":rec(result_path),"integrated_copy":rec(program),"build":build.as_posix(),
          "declaration_names":declaration_names,
          "local_instance_names":[d["name"] for m in modules for d in m["declarations"]
                                  if d["kind"]=="local instance"],
          "runs":runs,"sources":source_records,"dependency_overlay":overlay,"local_dependency_modules":len(visited),"external_boundary":[rec(p) for p in dict.fromkeys(boundary)],
          "environment_overrides":{"LEAN_PATH":os.pathsep.join([str(build)]+[str(p) for p in libraries]),
                                   "LEAN_SRC_PATH":str(build),"TMP":str(build),"TEMP":str(build),
                                   "PYTHONDONTWRITEBYTECODE":"1"},
          "source_files":[rec(p) for p in build.rglob("*.lean")],
          "scope":{"um_py_executed":False,"canonical_modules_rebuilt":False,"transitive_dependencies_all_hashed":False}}
    new(build/"BUILD_PLAN.json",(json.dumps(plan,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    print(json.dumps({"plan":str(build/"BUILD_PLAN.json"),"status":plan["status"]}))
def run(planpath):
    plan=json.loads(planpath.read_text(encoding="utf-8"));build=Path(plan["build"]).resolve()
    assert build.is_relative_to(BASE) and plan["status"]=="PREPARED_NOT_EXECUTED"
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
    valid=valid and stable and len(results)==len(plan["runs"])
    outcome={"status":"PASS_TRANSPOSED_SCOPE" if valid else "FAIL_VISIBLE","created_utc":datetime.now(timezone.utc).isoformat(),
             "plan":rec(planpath),"runs":results,"input_boundary_unchanged":stable,
             "um_py_executed":False,"canonical_changes":False,"transitive_dependencies_all_hashed":False,
             "scope_note":"The transposed modules, copied TGLExt root, copied full TGL/Audit and dedicated audit of all new declarations including named local instances are compiled against byte-copied canonical local dependencies and existing Mathlib binaries. Canonical module sources are not rebuilt; um.py is never run."}
    new(build/"TRANSPOSED_RESULT.json",(json.dumps(outcome,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    print(json.dumps({"status":outcome["status"],"result":str(build/"TRANSPOSED_RESULT.json")}))
    return 0 if valid else 1
if __name__=="__main__":
    assert len(sys.argv)==3 and sys.argv[1] in ("prepare","run")
    if sys.argv[1]=="prepare":prepare(Path(sys.argv[2]))
    else:sys.exit(run(Path(sys.argv[2]).resolve()))
