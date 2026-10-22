from pathlib import Path
import os, hashlib, json, ast
ROOT=Path(r"C:/IALD/Central de Patentes/Chatgpt/REVISAO_REDUCAO_ISOTROPIA_084_20260910")
source=ROOT/"write_review_isotropy_new.py"
dest=ROOT/"write_review_isotropy_portable_new.py"
def pin(p):
    b=p.read_bytes();return {"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def emit(p,b):
    if p.exists():raise FileExistsError(p)
    t=p.with_name(p.name+".pending")
    with t.open("xb") as out:out.write(b);out.flush();os.fsync(out.fileno())
    if t.read_bytes()!=b:raise RuntimeError("Temp mismatch")
    t.rename(p)
    if p.read_bytes()!=b:raise RuntimeError("Final mismatch")
    return pin(p)
before=pin(source)
raw=source.read_bytes()
old=b'ref_checks=[{"pin":r,"matches":pin(Path(r["path"]))==r} for r in refs]'
new=b'ref_checks=[{"pin":r,"matches":(actual:=pin(Path(r["path"])))["bytes"]==r["bytes"] and actual["sha256"]==r["sha256"]} for r in refs]'
if raw.count(old)!=1:raise RuntimeError("Expected unique replacement")
clean=raw.replace(old,new)
ast.parse(clean.decode("utf-8"))
created=emit(dest,clean)
if pin(source)!=before:raise RuntimeError("Source changed")
record={"source_before":before,"source_after":pin(source),"new_script":created,
"change":"Compare measured byte length/hash at the registered path; avoid treating slash spelling as content mismatch.",
"old_script_executed":False,"old_script_modified":False,"stage":"Preflight documentary writer correction; no failed mathematical or review result",
"ast":"PASS","replacements":1}
emit(ROOT/"PROVENIENCIA_EMISSOR_PORTAVEL_084.json",(json.dumps(record,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps(created,ensure_ascii=False))

