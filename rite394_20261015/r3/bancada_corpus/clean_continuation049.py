"""Clean compilation of continuation049; exclusive outputs under Chatgpt only.
Mathlib/stdlib are a declared external trust boundary. No canonical module imports.
"""
from pathlib import Path
from datetime import datetime,timezone
import os,sys,json,re,hashlib,subprocess,traceback
ROOT=Path(__file__).resolve().parent
KERNEL=Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/tgl_kernel")
TOOLCHAIN=Path(r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0")
MODULES=["BoundedGraphOperator","ClosedAntilinearStandardSubspace",
         "ContinuousModularMultipliers","BoundedGraphStandardSubspace",
         "ContinuousModularDomain","ContinuousModularStandardSubspace"]
INTEGRATION="Imports049All"
NAMESPACE="ChatgptAudit.Continuous049"
ALLOWED_AXIOMS={"propext","Classical.choice","Quot.sound"}
MODULE_RE=re.compile(r"[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*")
INSTANCE_RE=re.compile(r"(?m)^[ \t]*(?:(?:local|scoped|noncomputable|unsafe)\s+)*instance\b")
def now():return datetime.now(timezone.utc).isoformat()
def stamp():return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def record(p):
    p=Path(p).resolve(strict=True)
    return {"path":str(p),"bytes":p.stat().st_size,"sha256":digest(p)}
def snapshot(paths):return [record(p) for p in sorted({Path(p).resolve() for p in paths},key=str)]
def new_bytes(p,raw,allow_empty=False):
    p=Path(p)
    if not p.resolve().is_relative_to(ROOT) or p.exists() or (not raw and not allow_empty):
        raise RuntimeError(f"Nonexclusive output refused: {p}")
    p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+".tmp")
    with tmp.open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.read_bytes()!=raw:raise RuntimeError("Temporary bytes differ")
    tmp.rename(p)
    if p.read_bytes()!=raw:raise RuntimeError("Final bytes differ")
def new_json(p,data):new_bytes(p,(json.dumps(data,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))

def mask_lean(text):
    """Mask nested comments and strings, preserving every character offset."""
    chars = list(text)
    i = 0
    depth = 0
    string = False
    while i < len(text):
        if depth:
            if text.startswith("/-", i):
                chars[i:i+2] = "  "
                depth += 1
                i += 2
            elif text.startswith("-/", i):
                chars[i:i+2] = "  "
                depth -= 1
                i += 2
            else:
                if text[i] not in "\r\n":
                    chars[i] = " "
                i += 1
        elif string:
            if text[i] == "\\":
                chars[i] = " "
                i += 1
                if i < len(text):
                    if text[i] not in "\r\n":
                        chars[i] = " "
                    i += 1
            else:
                if text[i] == '"':
                    string = False
                if text[i] not in "\r\n":
                    chars[i] = " "
                i += 1
        elif text.startswith("--", i):
            end = text.find("\n", i)
            if end < 0:
                end = len(text)
            for j in range(i, end):
                if text[j] != "\r":
                    chars[j] = " "
            i = end
        elif text.startswith("/-", i):
            chars[i:i+2] = "  "
            depth = 1
            i += 2
        elif text[i] == '"':
            chars[i] = " "
            string = True
            i += 1
        else:
            i += 1
    if depth or string:
        raise RuntimeError("Unterminated Lean comment or string")
    return "".join(chars)

def imports(text):
    result = []
    code = mask_lean(text)
    for match in re.finditer(r"(?m)^\ufeff?[ \t]*(?:(?:public|private)\s+)?import\s+([^\r\n]+)", code):
        tokens = match.group(1).split()
        if tokens[:1] == ["all"]:
            tokens = tokens[1:]
        if not tokens:
            raise RuntimeError("Empty import")
        for name in tokens:
            if not MODULE_RE.fullmatch(name):
                raise RuntimeError(f"Unsupported import syntax: {name}")
            if name not in result:
                result.append(name)
    return result

def instances(text):
    code = mask_lean(text)
    result = []
    for ordinal, match in enumerate(INSTANCE_RE.finditer(code), 1):
        tail = code[match.end():].lstrip()
        name = re.match(r"(?:[A-Za-z_][\w']*|\u00ab[^\u00bb]+\u00bb)", tail)
        anonymous = name is None or name.group(0) in {"where"}
        result.append({
            "ordinal": ordinal,
            "line": text.count("\n", 0, match.start()) + 1,
            "name": None if anonymous else name.group(0),
            "anonymous": anonymous,
            "insertion_offset": match.end(),
        })
    return result

def checked_source(text, module):
    code = mask_lean(text)
    if re.search(r"\b(?:sorry|admit|axiom|native_decide)\b", code):
        raise RuntimeError(f"Forbidden proof token in {module}")
    if re.search(r"set_option\s+linter\.[\w.]+\s+false", code):
        raise RuntimeError(f"Disabled linter in {module}")
    rows = instances(text)
    if any(row["anonymous"] for row in rows):
        raise RuntimeError(f"Anonymous instance in build batch: {module}")
    namespaces = re.findall(r"(?m)^namespace\s+([\w.]+)", code)
    if len(namespaces) != 1:
        raise RuntimeError(f"Expected one namespace in {module}")
    matches = list(re.finditer(r"(?m)^[ \t]*(?:noncomputable\s+)?(theorem|lemma|def|abbrev|structure)\s+([\w.']+)", code))
    declarations = [(m.group(1), m.group(2)) for m in matches]
    covered = {m.start(1) for m in matches}
    for m in INSTANCE_RE.finditer(code):
        covered.add(m.start() + re.search(r"\binstance\b", m.group(0)).start())
    keywords = {m.start() for m in re.finditer(
        r"(?<![\w.'])\b(?:theorem|lemma|def|abbrev|structure|instance|class|inductive|opaque)\b", code)}
    if covered != keywords:
        raise RuntimeError(f"Unsupported or uncounted declaration in {module}")
    printed = re.findall(r"(?m)^#print\s+axioms\s+([\w.]+)", code)
    theorems = [name for kind, name in declarations if kind in {"theorem", "lemma"}]
    # Current049 named instances are declarations to audit, but are not counted as definitions.
    instance_names = [row["name"] for row in rows]
    declared_names = [name for _, name in declarations] + instance_names
    if len(declared_names) != len(set(declared_names)):
        raise RuntimeError(f"Duplicate source declaration in {module}")
    if len(printed) != len(set(printed)) or set(declared_names) != set(printed):
        raise RuntimeError(f"Axiom print coverage mismatch in {module}")
    qualified = [name if name.startswith(namespaces[0] + ".") else namespaces[0] + "." + name
                 for name in printed]
    instance_axiom_rows = [qualified[i] for i, name in enumerate(printed) if name in instance_names]
    return {"namespace": namespaces[0], "expected_axiom_rows": qualified,
            "instance_axiom_rows": instance_axiom_rows, "axiom_prints": len(qualified),
            "theorems": len(theorems), "definitions": sum(k in {"def", "abbrev", "structure"} for k, _ in declarations),
            "instances": rows, "anonymous_instances": 0}

def parse_axioms(output):
    pattern = r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)"
    rows = []
    for match in re.finditer(pattern, output):
        names = [x.strip() for x in (match.group(2) or "").split(",") if x.strip()]
        rows.append({"declaration": match.group(1), "axioms": names})
    return rows

def companions(olean):
    result = [olean]
    for suffix in [".private", ".server"]:
        extra = Path(str(olean) + suffix)
        if extra.is_file():
            result.append(extra)
    return result

def run_build():
    sys.stdout.reconfigure(encoding="utf-8")
    development=len(sys.argv)==3 and sys.argv[1]=="--module"
    if len(sys.argv)>1 and not development:raise RuntimeError("Only --module NAME is accepted")
    requested=[sys.argv[2]] if development else MODULES
    if any(m not in MODULES for m in requested):raise RuntimeError("Unknown module")
    tag=stamp()
    clean=ROOT/("CONTINUACAO049_"+("DEVELOPMENT_" if development else "CLEAN_")+tag)
    marker=ROOT/("CONTINUACAO049_DEVELOPMENT_"+tag+".json" if development else "CONTINUACAO049_CLEAN_BUILD.json")
    if clean.exists() or marker.exists():raise RuntimeError("Nonfresh build refused")
    clean.mkdir()
    try:
        original,graph,info={},{},{}
        visiting=set()
        order=[]
        def visit(module):
            if module in order:return
            if module in visiting:raise RuntimeError("Local import cycle")
            visiting.add(module)
            src=ROOT/(module+".lean")
            raw=src.read_bytes()
            text=raw.decode("utf-8-sig")
            data=checked_source(text,module)
            if data["namespace"]!=NAMESPACE:raise RuntimeError("Unexpected namespace")
            deps=imports(text)
            for dep in deps:
                if dep in MODULES:visit(dep)
                elif not dep.startswith("Mathlib."):raise RuntimeError(f"Undeclared dependency {dep}")
            original[module]=record(src);graph[module]=deps;info[module]=data
            new_bytes(clean/(module+".lean"),raw)
            order.append(module);visiting.remove(module)
        for module in requested:visit(module)
        new_bytes(clean/(INTEGRATION+".lean"),("".join("import "+m+"\n" for m in order)).encode("utf-8"))
        graph[INTEGRATION]=list(order)
        info[INTEGRATION]={"expected_axiom_rows":[],"axiom_prints":0,"theorems":0,
                           "definitions":0,"instances":[],"anonymous_instances":0}
        package_dirs=sorted([p for p in (KERNEL/".lake/packages").iterdir() if p.is_dir()])
        externals=[p/".lake/build/lib/lean" for p in package_dirs if (p/".lake/build/lib/lean").is_dir()]
        externals.append(TOOLCHAIN/"lib/lean")
        lean_path=[clean,*externals]
        if ROOT in lean_path or KERNEL/".lake/build/lib/lean" in lean_path:raise RuntimeError("Fallback path")
        lean=TOOLCHAIN/"bin/lean.exe"
        frozen={lean,Path(__file__),ROOT/"CONTINUACAO049_DERIVACAO_PREVIA.md",ROOT/"DERIVACAO049_INFRA.md"}
        frozen.update(ROOT.glob("DERIVACAO049_*.md"))
        for cfg in [KERNEL/"lean-toolchain",KERNEL/"lake-manifest.json",KERNEL/"lakefile.toml",KERNEL/"lakefile.lean"]:
            if cfg.is_file():frozen.add(cfg)
        for package in package_dirs:
            for cfg in [package/"lean-toolchain",package/"lake-manifest.json"]:
                if cfg.is_file():frozen.add(cfg)
        external={}
        for dep in sorted({d for ds in graph.values() for d in ds if d not in MODULES}):
            candidates=[p/Path(*dep.split(".")).with_suffix(".olean") for p in externals]
            found=[p for p in candidates if p.is_file()]
            if len(found)!=1:raise RuntimeError(f"External resolution not unique {dep}: {found}")
            files=companions(found[0])
            external[dep]={"resolved":str(found[0]),"files":snapshot(files)}
            frozen.update(files)
        for module in order:
            frozen.add(ROOT/(module+".lean"));frozen.add(clean/(module+".lean"))
        frozen.add(clean/(INTEGRATION+".lean"))
        before=snapshot(frozen)
        new_json(clean/"FROZEN_INPUTS.json",before)
        plan={"schema":"chatgpt.clean049.plan.v1","created_utc":now(),"build_order":order+[INTEGRATION],
              "graph":graph,"lean_path":[str(p) for p in lean_path],"original_sources":original,
              "source_info":info,"external_direct_imports":external,
              "external_boundary":"Direct imports and companions only; transitive package closure not measured."}
        new_json(clean/"BUILD_PLAN.json",plan)
        env=os.environ.copy();env["LEAN_PATH"]=os.pathsep.join(map(str,lean_path))
        steps=[]
        for index,module in enumerate(order+[INTEGRATION],1):
            if snapshot(frozen)!=before:raise RuntimeError("Frozen input changed before compilation")
            source=clean/(module+".lean");olean=clean/(module+".olean")
            if olean.exists():raise RuntimeError("Output exists before compilation")
            command=[str(lean),"-o",str(olean),str(source)]
            started=now()
            print(json.dumps({"event":"compile_start","module":module,"clean_directory":str(clean)}),flush=True)
            run=subprocess.run(command,cwd=clean,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            log=clean/f"{index:02d}_{module}.log";new_bytes(log,run.stdout,True)
            output=run.stdout.decode("utf-8",errors="replace")
            rows=parse_axioms(output)
            issues=[line for line in output.splitlines() if re.search(r"\b(?:error|warning)(?:\([^\n]*?\))?:",line)]
            stable=snapshot(frozen)==before
            exact=[r["declaration"] for r in rows]==info[module]["expected_axiom_rows"]
            permitted=all(set(r["axioms"])<=ALLOWED_AXIOMS for r in rows)
            passed=run.returncode==0 and stable and exact and permitted and not issues and olean.is_file() and "sorryAx" not in output
            meta=clean/f"{index:02d}_{module}.json"
            data={"module":module,"started_utc":started,"ended_utc":now(),"exit_code":run.returncode,
                  "passed":passed,"command":command,"cwd":str(clean),"lean_path":list(map(str,lean_path)),
                  "source":record(source),"log":record(log),"output_artifacts":snapshot(companions(olean)) if olean.is_file() else [],
                  "inputs_stable":stable,"axiom_coverage_exact":exact,"axiom_rows":rows,"issues":issues,
                  "source_info":info[module],"frozen_input_snapshot":record(clean/"FROZEN_INPUTS.json")}
            new_json(meta,data);steps.append(record(meta))
            print(json.dumps({"event":"compile_end","module":module,"passed":passed,"exit_code":run.returncode}),flush=True)
            if not passed:raise RuntimeError(f"Compilation rejected; see {meta}")
        after=snapshot(frozen);new_json(clean/"FROZEN_INPUTS_AFTER.json",after)
        if after!=before:raise RuntimeError("Frozen inputs changed over full build")
        build_files=snapshot(p for p in clean.rglob("*") if p.is_file())
        totals={k:sum(info[m][k] for m in order) for k in ["theorems","definitions","axiom_prints"]}
        totals["instances"]=sum(len(info[m]["instances"]) for m in order)
        result={"schema":"chatgpt.clean049.build.v1","status":"PASS","created_utc":now(),
                "development_only":development,"clean_directory":str(clean),"build_order":order+[INTEGRATION],
                "modules":order,"integration_module":INTEGRATION,"steps":steps,"totals":totals,
                "original_sources":original,"source_info":info,"graph":graph,
                "lean_path":list(map(str,lean_path)),"toolchain":record(lean),
                "frozen_before":before,"frozen_after":after,"build_files":build_files,
                "external_direct_imports":external,"external_boundary":plan["external_boundary"],
                "fresh_clean_build":True,"inputs_stable":True,"canonical_gate_changed":False,
                "H3":"OPEN","physical_reconstruction":"OPEN"}
        new_json(marker,result)
        print(json.dumps({"status":"PASS","marker":str(marker),"clean_directory":str(clean),"totals":totals}),flush=True)
    except BaseException as exc:
        new_json(clean/"FAILURE.json",{"created_utc":now(),"error":repr(exc),"traceback":traceback.format_exc()})
        raise
if __name__=="__main__":run_build()
