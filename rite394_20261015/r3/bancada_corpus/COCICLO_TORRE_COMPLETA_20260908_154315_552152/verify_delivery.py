"""Independent execution of package integrity checks, not independent scientific review."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,re,sys
sys.stdout.reconfigure(encoding="utf-8")
folder=Path(__file__).resolve().parent
assert folder.parent==Path(r"C:\IALD\Central de Patentes\Chatgpt")
build=folder/"BUILD_20260908_155436_565087"
b=json.loads((build/"BUILD_RESULT.json").read_text(encoding="utf-8"))
a=json.loads((folder/"AUDITORIA_MODELO_20260908_155734_006832.json").read_text(encoding="utf-8"))
report=folder/"DEMONSTRACAO_NO_MODELO_COMPLETO.md"
def record(p):
    raw=p.read_bytes()
    return {"path":p.as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
def matches(rec):
    got=record(Path(rec["path"]))
    return got["bytes"]==rec["bytes"] and got["sha256"]==rec["sha256"]
assert b["status"]=="PASS_COMPILED_SCOPE"
assert a["status"]=="PASS_READ_ONLY_LINK_AND_EXACT_EXAMPLES"
assert all(matches(rec) for rec in b["sources"]+b["external_boundary"]+a["canonical_sources"]+a["canonical_binaries"]+[a["um"]])
expected=set();rows=[];source_counts={"theorems":0,"definitions":0}
pattern=re.compile(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
artifacts=[report,Path(__file__),folder/"build_realization.py",folder/"audit_existing_model.py",
           build/"BUILD_RESULT.json",folder/"AUDITORIA_MODELO_20260908_155734_006832.json"]
for rec in b["sources"]:
    source=Path(rec["path"]);raw=source.read_bytes();txt=raw.decode("utf-8")
    assert (build/source.name).read_bytes()==raw
    assert not re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b",txt)
    decls=re.findall(r"(?m)^(?:noncomputable\s+)?(abbrev|def|theorem)\s+(\w+)",txt)
    prints=re.findall(r"(?m)^#print axioms (\w+)$",txt)
    assert len(prints)==len(set(prints)) and set(prints)=={n for _,n in decls}
    expected.update("ChatgptAudit.CocycleRealization."+n for n in prints)
    source_counts["theorems"]+=sum(k=="theorem" for k,_ in decls)
    source_counts["definitions"]+=sum(k!="theorem" for k,_ in decls)
    logpath=build/(source.stem+".log");log=logpath.read_text(encoding="utf-8")
    assert not pattern.sub("",log).strip()
    rows.extend({"name":m.group(1),"axioms":[s.strip() for s in (m.group(2) or "").split(",") if s.strip()]} for m in pattern.finditer(log))
    artifacts.extend([source,build/source.name,logpath])
    for ext in [".olean",".ilean",".olean.server",".olean.private"]:
        p=build/(source.stem+ext)
        if p.exists():
            assert p.stat().st_size>0
            artifacts.append(p)
        elif ext in [".olean",".ilean"]:
            raise RuntimeError("Missing compiler output: "+str(p))
assert len(rows)==len(expected) and {r["name"] for r in rows}==expected
assert all(set(r["axioms"])<={"propext","Classical.choice","Quot.sound"} for r in rows)
assert (build/"ImportsRealization.log").read_bytes()==b""
assert (build/"ImportsRealization.olean").stat().st_size>0
assert source_counts["theorems"]==b["theorems"] and source_counts["definitions"]==b["definitions"]
artifacts.extend([build/"ImportsRealization.lean",build/"ImportsRealization.olean",build/"ImportsRealization.log"])
rt=report.read_text(encoding="utf-8")
links=[]
for m in re.finditer(r"\]\(<([A-Za-z]:/[^>]+)>\)",rt):
    target=m.group(1);parts=re.match(r"^(.*?)(?::(\d+))?$",target)
    p=Path(parts.group(1));assert p.is_file(),target
    if parts.group(2):assert 1<=int(parts.group(2))<=len(p.read_text(encoding="utf-8").splitlines())
    links.append(target)
assert "[OPEN]" in rt and "[DERIVED" in rt and "[REAL" in rt
assert not re.search(r"@[A-Z_0-9]+@",rt)
history=[]
for p in sorted(folder.glob("BUILD_*/BUILD_RESULT.json")):
    v=json.loads(p.read_text(encoding="utf-8"))
    history.append({"path":p.as_posix(),"status":v["status"]})
result={"status":"PASS_DELIVERY_INTEGRITY","created_utc":datetime.now(timezone.utc).isoformat(),
"counts":source_counts,"axiom_reports":len(rows),"all_axioms_standard":True,"clean_compilation_logs":True,
"local_report_links_checked":len(links),"current_canonical_records_rechecked":len(b["external_boundary"]+a["canonical_sources"]+a["canonical_binaries"]+[a["um"]]),
"exact_finite_predicates":a["exact_checks"],"matched_embedded_modules":a["matched_modules"],
"accepted_build":build.as_posix(),"preserved_build_history":history,
"artifacts":[record(p) for p in dict.fromkeys(artifacts)],
"scope":{"independent_scientific_review":False,"full_canonical_rebuild":False,
"new_algebraic_reconstruction_fully_lean_formalized":False,"qg_proof":False,"canonical_writes":False}}
p=folder/("VERIFICACAO_ENTREGA_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f")+".json")
raw=(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
tmp=p.with_name(p.name+".tmp")
with tmp.open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==raw
os.rename(tmp,p)
assert p.read_bytes()==raw
print(json.dumps({"path":p.as_posix(),"status":result["status"],"counts":source_counts,
"axiom_reports":len(rows),"links_checked":len(links),"records_rechecked":result["current_canonical_records_rechecked"]},ensure_ascii=False))
