"""Freeze the two stable operator-field modules and audit their exact ten targets."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
REVIEW=Path(__file__).resolve().parent
ROOT=REVIEW.parent
PREVIOUS=Path((REVIEW/"constant_fibre_identification_latest_run.txt").read_text(encoding="utf-8"))
RUN=REVIEW/("operator_field_independent_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
NAMES=["StrongOperatorField","OperatorFieldFaithfulness"]
ALLOWED={"propext","Classical.choice","Quot.sound"}
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def write(path,raw):
    assert path.resolve().is_relative_to(REVIEW)
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        old=path.read_bytes()
        if old==raw:return
        bak=path.with_name(path.name+".bak_"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        with bak.open("xb") as f:f.write(old)
        assert bak.read_bytes()==old
    tmp=path.with_name(path.name+".tmp")
    with tmp.open("xb") as f:f.write(raw)
    assert tmp.read_bytes()==raw
    tmp.replace(path)
def save(path,obj):write(path,json.dumps(obj,ensure_ascii=False,indent=2).encode("utf-8"))
def imports(raw):return re.findall(r"^import\s+([\w.]+)",raw.decode("utf-8"),re.M)
prior=json.loads((PREVIOUS/"manifest.json").read_bytes())
prior_comp=json.loads((PREVIOUS/"compilation.json").read_bytes())
assert prior_comp["all_exit_zero"] and prior_comp["all_axioms_allowed"]
catalog={n:{"binary":r["frozen_binary"],"source":r["frozen_source"],"sha256":r["sha256"],"source_sha256":r["source_sha256"]} for n,r in prior["dependencies"].items()}
for rel,r in prior["sources"].items():
    c=next(x for x in prior_comp["records"] if x["module"]==rel)
    catalog[rel[:-5].replace("/",".")]={"binary":str(PREVIOUS/"build"/Path(rel).with_suffix(".olean")),"source":r["snapshot"],"sha256":c["output_sha256"],"source_sha256":r["sha256"]}
newnames={"TGLV350."+n for n in NAMES}
sources={}; declarations=[]; all_declarations=[]
for name in NAMES:
    rel="TGLV350/"+name+".lean"; path=ROOT/"kernel"/rel; raw=path.read_bytes()
    snap=RUN/"sources"/rel;write(snap,raw)
    candidates=[]
    for p in sorted((ROOT/"logs").glob(name+"_*.json"),reverse=True):
        data=json.loads(p.read_bytes())
        if data.get("sha256")==sha(raw) and data.get("returncode")==0 and data.get("source_unchanged_during_compile"):
            candidates.append((p,data))
    assert candidates,name
    log,author=candidates[0]
    assert sha((ROOT/"build"/Path(rel).with_suffix(".olean")).read_bytes())==author["output_sha256"]
    for p in [log,Path(author["stdout"]),Path(author["stderr"])]:write(RUN/"author_logs"/p.name,p.read_bytes())
    txt=raw.decode("utf-8"); namespaces=re.findall(r"^namespace\s+([\w.]+)$",txt,re.M)
    assert len(namespaces)==1; ns=namespaces[0]
    printed=[ns+"."+n for n in re.findall(r"^#print axioms ([\w.]+)$",txt,re.M)]
    local=[ns+"."+n for n in re.findall(r"^(?:noncomputable\s+)?(?:def|theorem|abbrev|structure)\s+([\w.]+)",txt,re.M)]
    assert set(printed)<=set(local)
    declarations+=printed;all_declarations+=local
    sources[rel]={"path":str(path),"snapshot":str(snap),"sha256":sha(raw),"lines":len(txt.splitlines()),"imports":imports(raw),"namespace":ns,"declarations":printed,"all_named_declarations":local,"author_log":str(log),"author_binary_sha256":author["output_sha256"]}
assert len(declarations)==10 and len(set(declarations))==10
aux=set(all_declarations)-set(declarations)
assert len(all_declarations)==13 and len(aux)==3
needed=set(); package_imports=set()
def visit(name):
    if name in newnames:
        for n in sources[name.replace(".","/")+".lean"]["imports"]:visit(n)
        return
    if not (name.split(".")[0] in {"TGL","TGLExt","TGLV350"}):
        package_imports.add(name);return
    if name in needed:return
    assert name in catalog,"missing frozen dependency: "+name
    needed.add(name)
    row=catalog[name];raw=Path(row["source"]).read_bytes()
    assert sha(raw)==row["source_sha256"]
    for imp in imports(raw):visit(imp)
for name in newnames:visit(name)
deps={}
for name in sorted(needed):
    row=catalog[name].copy();rel=Path(*name.split("."));raw=Path(row["source"]).read_bytes();binary=Path(row["binary"]).read_bytes()
    assert sha(raw)==row["source_sha256"] and sha(binary)==row["sha256"]
    assert sha((ROOT/"kernel"/rel.with_suffix(".lean")).read_bytes())==row["source_sha256"],name
    source=RUN/"dependency_sources"/rel.with_suffix(".lean");target=RUN/"build"/rel.with_suffix(".olean")
    write(source,raw);write(target,binary)
    for p in Path(row["binary"]).parent.glob(Path(row["binary"]).name+".*"):
        if p.is_file():write(target.with_name(p.name),p.read_bytes())
    row.update(frozen_source=str(source),frozen_binary=str(target),imports=imports(raw),live_source_matches_frozen=True)
    deps[name]=row
environment=json.loads((ROOT/"environment.json").read_bytes());env=os.environ.copy()
env["LEAN_PATH"]=os.pathsep.join([str(RUN/"build")]+environment["lean_path"][2:])
(RUN/"tmp").mkdir();env["TMP"]=env["TEMP"]=str(RUN/"tmp")
version=subprocess.run([environment["lean"],"--version"],env=env,cwd=RUN,capture_output=True)
assert version.returncode==0
manifest={"run":str(RUN),"previous_run":str(PREVIOUS),"mode":"INDEPENDENT_BUILD_TWO_STABLE_OPERATOR_FIELD_MODULES","sources":sources,"dependencies":deps,"declarations":declarations,"all_named_declarations":all_declarations,"auxiliary_checked_transitively":sorted(aux),"external_package_imports":sorted(package_imports),"lean_path":env["LEAN_PATH"],"lean_version":version.stdout.decode("utf-8").strip(),"compiler_sha256":sha(Path(environment["lean"]).read_bytes()),"previous_reviews":{str(p):sha(p.read_bytes()) for p in REVIEW.glob("REVIEW_*.md")},"initial_um_sha256":sha((ROOT/"um.py").read_bytes())}
save(RUN/"manifest.json",manifest);write(REVIEW/"operator_field_latest_run.txt",str(RUN).encode("utf-8"))
write(RUN/"environment.json",(ROOT/"environment.json").read_bytes())
audit="\n".join("import TGLV350."+n for n in NAMES)+"\n"
for n in all_declarations:
    audit+="set_option pp.universes true in\n#check "+n+"\n"
    if n in declarations:audit+="#print axioms "+n+"\n"
write(RUN/"sources/OperatorFieldFullAudit.lean",audit.encode("utf-8"))
print(json.dumps({"run":str(RUN),"project_dependencies":len(deps),"source_count":len(sources),"printed_targets":len(declarations),"named_types_checked":len(all_declarations)}),flush=True)
records=[]
for rel in list(sources)+["OperatorFieldFullAudit.lean"]:
    src=RUN/"sources"/rel;out=RUN/"build"/Path(rel).with_suffix(".olean");out.parent.mkdir(parents=True,exist_ok=True)
    assert not out.exists()
    command=[environment["lean"],"-o",str(out),str(src)];t=time.monotonic()
    proc=subprocess.run(command,env=env,cwd=RUN/"sources",capture_output=True)
    txt=proc.stdout.decode("utf-8",errors="replace")
    ax={n:[a.strip() for a in body.split(",") if a.strip()] for n,body in re.findall(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]",txt,re.S)}
    for n in re.findall(r"'([\w.']+)' does not depend on any axioms",txt):ax.setdefault(n,[])
    stdout=RUN/"logs"/(Path(rel).stem+".stdout.txt");stderr=RUN/"logs"/(Path(rel).stem+".stderr.txt")
    write(stdout,proc.stdout);write(stderr,proc.stderr)
    record={"module":rel,"command":command,"returncode":proc.returncode,"seconds":round(time.monotonic()-t,3),"source_sha256":sha(src.read_bytes()),"output_sha256":sha(out.read_bytes()) if out.exists() else None,"axioms":ax,"axioms_allowed":bool(ax) and all(set(a)<=ALLOWED for a in ax.values()),"stdout":str(stdout),"stderr":str(stderr)}
    records.append(record);save(RUN/"compilation.json",{"complete":False,"records":records})
    print(json.dumps({k:record[k] for k in ["module","returncode","seconds","axioms_allowed"]}),flush=True)
    if proc.returncode:print(txt,flush=True);break
summary={"records":records,"complete":len(records)==3,"all_exit_zero":len(records)==3 and all(x["returncode"]==0 for x in records),"full_audit_names_exact":len(records)==3 and set(records[-1]["axioms"])==set(declarations),"all_axioms_allowed":all(x["axioms_allowed"] for x in records),"sources_unchanged":all(sha(Path(x["path"]).read_bytes())==x["sha256"] for x in sources.values()),"dependencies_unchanged":all(sha(Path(x["frozen_source"]).read_bytes())==x["source_sha256"] and sha(Path(x["frozen_binary"]).read_bytes())==x["sha256"] for x in deps.values()),"previous_reviews_preserved":all(sha(Path(p).read_bytes())==h for p,h in manifest["previous_reviews"].items())}
save(RUN/"compilation.json",summary);print(json.dumps({k:v for k,v in summary.items() if k!="records"}),flush=True)
