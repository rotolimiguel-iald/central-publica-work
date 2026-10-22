"""Verify artifact integrity and proof-report coverage; no canonical writes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,re,sys
sys.stdout.reconfigure(encoding="utf-8")
folder=Path(__file__).resolve().parent
assert folder.parent==Path(r"C:\IALD\Central de Patentes\Chatgpt")
build=folder/"BUILD_20260908_162345_889479"
b=json.loads((build/"BUILD_RESULT.json").read_text(encoding="utf-8"))
d=json.loads((folder/"DIAGNOSTICOS_20260908_162543_810408.json").read_text(encoding="utf-8"))
integration=json.loads((folder/"INTEGRACAO056.json").read_text(encoding="utf-8"))
def rec(p):
    raw=p.read_bytes()
    return {"path":p.as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
for r in b["sources"]+b["external_boundary"]+d["canonical_sources"]+[d["canonical_um"]]:
    assert rec(Path(r["path"]))=={k:r[k] for k in ["path","bytes","sha256"]},r["path"]
assert b["status"]=="PASS_COMPILED_SCOPE"
expected=set();rows=[];counts={};files=[]
pattern=re.compile(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
for item in b["sources"]:
    p=Path(item["path"]);raw=p.read_bytes();s=raw.decode("utf-8")
    assert (build/p.name).read_bytes()==raw
    ns=re.findall(r"(?m)^namespace ([\w.]+)$",s);assert len(ns)==1
    decls=re.findall(r"(?m)^(?:noncomputable\s+)?(def|theorem|abbrev)\s+(\w+)",s)
    prints=re.findall(r"(?m)^#print axioms (\w+)$",s)
    assert set(prints)=={n for _,n in decls} and len(prints)==len(set(prints))
    assert not re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b",s)
    expected.update(ns[0]+"."+n for n in prints)
    counts[p.stem]={"theorems":sum(k=="theorem" for k,_ in decls),
                   "definitions":sum(k!="theorem" for k,_ in decls)}
    logpath=build/(p.stem+".log");log=logpath.read_text(encoding="utf-8")
    assert not pattern.sub("",log).strip()
    rows.extend({"name":m.group(1),"axioms":[x.strip() for x in (m.group(2) or "").split(",") if x.strip()]} for m in pattern.finditer(log))
    files.extend([p,build/p.name,logpath])
    for suffix in [".olean",".ilean",".olean.server",".olean.private"]:
        out=build/(p.stem+suffix)
        if out.exists():
            assert out.stat().st_size>0;files.append(out)
        else:assert suffix not in [".olean",".ilean"]
assert len(rows)==len(expected) and {r["name"] for r in rows}==expected
assert all(set(r["axioms"])<={"propext","Classical.choice","Quot.sound"} for r in rows)
assert (build/"ImportsRealization.log").read_bytes()==b""
assert (build/"ImportsRealization.olean").stat().st_size>0
assert sum(x["theorems"] for x in counts.values())==92
assert sum(x["definitions"] for x in counts.values())==20
for row in integration["new_modules"]:assert rec(Path(row["artifact"]["path"]))==row["artifact"]
links=0
for p in folder.glob("*.md"):
    s=p.read_text(encoding="utf-8")
    assert not re.search(r"@[A-Z_0-9]+@",s)
    for m in re.finditer(r"\]\(<([A-Za-z]:/[^>]+)>\)",s):
        target=m.group(1);m2=re.match(r"^(.*?)(?::(\d+))?$",target)
        dest=Path(m2.group(1));assert dest.is_file(),target
        if m2.group(2):assert int(m2.group(2))<=len(dest.read_text(encoding="utf-8").splitlines())
        links+=1
for p in folder.iterdir():
    if p.is_file() and p.suffix in [".md",".py",".json"] and not p.name.startswith(("MANIFESTO","VERIFICACAO")):
        files.append(p)
files += [build/"BUILD_RESULT.json",build/"ImportsRealization.lean",build/"ImportsRealization.log",build/"ImportsRealization.olean"]
history=[]
for p in sorted(folder.glob("BUILD_*/BUILD_RESULT.json")):
    r=json.loads(p.read_text(encoding="utf-8"))
    history.append({"path":p.as_posix(),"status":r["status"]})
result={"status":"PASS_DELIVERY_INTEGRITY","created_utc":datetime.now(timezone.utc).isoformat(),
"counts":counts,"new_theorems":51,"new_definitions":11,"antecedent_theorems_recompiled":41,
"combined_theorems":92,"combined_definitions":20,"axiom_reports":len(rows),"axiom_rows":rows,
"clean_logs":True,"local_links_checked":links,"exact_rational_checks":d["exact_checks"],
"canonical_records_unchanged_on_recheck":True,"preserved_build_history":history,
"artifacts":[rec(p) for p in dict.fromkeys(files)],
"scope":{"independent_scientific_review":False,"canonical_writes":False,"full_canonical_rebuild":False,
"general_gravitational_reconstruction_completed":False}}
p=folder/("VERIFICACAO_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f")+".json")
raw=(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
tmp=p.with_name(p.name+".tmp")
with tmp.open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==raw;os.rename(tmp,p);assert p.read_bytes()==raw
print(json.dumps({"path":p.as_posix(),"status":result["status"],"counts":counts,
"axiom_reports":len(rows),"links_checked":links,"artifacts":len(result["artifacts"])},ensure_ascii=False))
