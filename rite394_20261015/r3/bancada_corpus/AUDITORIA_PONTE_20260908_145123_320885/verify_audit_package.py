from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os,re,sys
sys.stdout.reconfigure(encoding="utf-8")
folder=Path(__file__).resolve().parent
root=Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
if folder.parent!=root or not folder.name.startswith("AUDITORIA_PONTE_"):
    raise RuntimeError("Unauthorized output directory")
main=json.loads((folder/"RESULTADOS_EXATOS.json").read_text(encoding="utf-8"))
extra=json.loads((folder/"ADENDO_DEGENERESCENCIA.json").read_text(encoding="utf-8"))
sources={**main["sources"],**extra["sources"]}
reads={}
for key,entry in sources.items():
    data=Path(entry["path"]).read_bytes()
    if hashlib.sha256(data).hexdigest()!=entry["sha256"]:
        raise RuntimeError("Source changed: "+key)
    reads[entry["path"]]=data
module_matches=[v["text_equal_normalizing_line_endings"] for v in main["selected_embedded_comparisons"].values()]
module_matches += [v["embedded_text_equal"] for v in extra["sources"].values()]
exact_checks=list(main["centralizer_diagnostic"]["checks"].values())+list(main["metric_diagnostic"]["checks"].values())+list(extra["checks"].values())
assert len(sources)==31 and len(module_matches)==19 and all(module_matches)
assert len(exact_checks)==35 and all(exact_checks)
assert hashlib.sha256((folder/"audit_ponte_links.py").read_bytes()).hexdigest()==main["script_sha256"]
assert hashlib.sha256((folder/"RESULTADOS_EXATOS.json").read_bytes()).hexdigest()==extra["primary_results_sha256"]
report=(folder/"AUDITORIA_PONTE.md").read_text(encoding="utf-8")
links=[]
target=folder/"VERIFICACAO_FINAL.json"
for text in re.findall(r"\]\(<([A-Za-z]:/[^>]+)>\)",report):
    match=re.match(r"^(.*):(\d+)$",text)
    path=Path(match.group(1) if match else text)
    lineno=int(match.group(2)) if match else None
    if path==target:
        links.append({"path":str(path),"line":None,"status":"SELF_REFERENCE_CHECKED_AFTER_EXCLUSIVE_WRITE"})
        continue
    if not path.is_file(): raise RuntimeError("Missing link target: "+str(path))
    if lineno is not None:
        data=reads.get(path.as_posix())
        if data is None: data=path.read_bytes()
        if not (1<=lineno<=len(data.decode("utf-8-sig").splitlines())):
            raise RuntimeError("Invalid link line")
    links.append({"path":path.as_posix(),"line":lineno,"status":"EXISTS_AND_LINE_VALID_IF_SPECIFIED"})
assert len(links)>40
artifacts={}
for path in sorted(folder.iterdir()):
    if path.is_file():
        data=path.read_bytes()
        if path.suffix==".py": ast.parse(data.decode("utf-8-sig"),filename=str(path))
        artifacts[path.name]={"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}
assert not any(".tmp" in name for name in artifacts)
result={
"status":"PASS_PACKAGE_VALIDATION",
"created_utc":datetime.now(timezone.utc).isoformat(),
"original_source_count":len(sources),
"original_source_hashes_unchanged":True,
"selected_embedded_module_match_count":len(module_matches),
"exact_rational_check_count":len(exact_checks),
"local_link_count":len(links),
"local_links":links,
"artifact_hashes":artifacts,
"own_hash_omitted_to_avoid_self_reference":True,
"scope":{"new_lean_compilation":False,"independent_scientific_review":False,"original_program_execution":False,
"original_writes":False,"canonical_memory_or_gate_writes":False},
"addendum_script_note":"After its successful run, only its output-folder selection was made relocatable with a byte backup. Mathematical calculations were unchanged. The current scripts parse successfully; the relocation change was not a new Lean or scientific check."
}
data=(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
temp=folder/"VERIFICACAO_FINAL.json.tmp"
assert not target.exists()
with temp.open("xb") as f: f.write(data); f.flush(); os.fsync(f.fileno())
assert temp.read_bytes()==data
os.rename(temp,target)
assert target.read_bytes()==data
json.loads(target.read_text(encoding="utf-8"))
print(json.dumps({"status":result["status"],"source_count":len(sources),"module_matches":len(module_matches),
"exact_checks":len(exact_checks),"links":len(links),"artifacts_measured":len(artifacts),"verification":target.as_posix()},ensure_ascii=False))
