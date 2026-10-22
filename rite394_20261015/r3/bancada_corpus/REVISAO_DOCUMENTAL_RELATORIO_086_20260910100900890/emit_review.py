import sys,json,hashlib,pathlib,datetime,os,re
sys.stdout.reconfigure(encoding="utf-8")
out=pathlib.Path(__file__).resolve().parent
base=out.parent
assert base.name=="Chatgpt"
payload=out/"INPUT_DOCUMENTARY_REVIEW.json"
d=json.loads(payload.read_text(encoding="utf-8"))
def pin(p):
 p=pathlib.Path(p);assert base in p.resolve().parents,p
 b=p.read_bytes();return {"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
before=d["before"];after=[pin(p["path"]) for p in before]
actual={p["path"]:p for p in after}
checks=[{"kind":"review_window_unchanged","path":a["path"],"passed":a==b} for a,b in zip(before,after)]
def read(rel):return json.loads((base/rel).read_text(encoding="utf-8"))
def cp(kind,p):checks.append({"kind":kind,"path":p["path"],"passed":actual[p["path"]]==p})
e=read("REEXAME_SUFICIENCIA_086_20260910/REGISTRO_EMISSAO_NARRATIVOS_086.json")
rr=read("REVISOES_RAIZ_086_20260910/REGISTRO_REVISAO_RAIZ_086.json")
c=read("REEXAME_SUFICIENCIA_086_20260910/PINS_ANTES_NARRATIVOS_086.json")
for group in ["narratives","sources_before","sources_after"]:
 for p in e[group]:cp("emission_"+group,p)
for group in ["capture","helper"]:cp("emission_"+group,e[group])
for p in rr["sources"]:cp("root_review_source",p)
for group in ["review","helper"]:cp("root_review_"+group,rr[group])
for p in c["sources_before"]:cp("initial_capture_source",p)
cp("initial_capture_helper",c["helper"])
a=read("REEXAME_SUFICIENCIA_086_20260910/ESTADO_CANONICO_086.json")
s=read("INSPECAO_CANONICO_NAVEGACAO_086_20260910/ESTADO_CANONICO_INSPECAO_086.json")
for k in ["embedded_files","modules","present","absent","seal_um_hash_matches","seal_excerpt","all_read_sources_unchanged","um_executed_or_imported","originals_written"]:
 checks.append({"kind":"snapshots_equal_"+k,"passed":a[k]==s[k]})
na=lambda p:{k:p[k] for k in ["path","bytes","sha256"]}
pa={p["path"]:na(p) for p in a["pins"]};ps={p["path"]:na(p) for p in s["pins"]}
ca=[{k:p[k] for k in ["path","unchanged"]} for p in a["comparison_with_delivery085"]]
cs=[{k:p[k] for k in ["path","unchanged"]} for p in s["comparison_with_delivery085"]]
checks.append({"kind":"snapshot_comparison_flags","passed":ca==cs and all(p["unchanged"] for p in ca)})
canon=[]
for p in ca:
 checks.append({"kind":"snapshot_recorded_canonical_pin","path":p["path"],"passed":pa[p["path"]]==ps[p["path"]]})
 canon.append(pa[p["path"]])
checks.extend([{"kind":"snapshot_module_length","passed":len(s["modules"])==98},{"kind":"snapshot_present_count","passed":sum(x["present"] for x in s["modules"])==77},{"kind":"snapshot_absent_list","passed":[x["module"] for x in s["modules"] if not x["present"]]==s["absent"] and len(s["absent"])==21}])
links=set()
for p in e["narratives"]:
 text=pathlib.Path(p["path"]).read_text(encoding="utf-8")
 links.update(re.findall(r"\]\(<(C:/[^>]+)>\)",text))
for x in sorted(links):
 p=pathlib.Path(x);assert base in p.resolve().parents
 checks.append({"kind":"narrative_local_link","path":x,"passed":p.is_file()})
checks.append({"kind":"origin28_consistent","passed":len(e["checks"])==e["checks_total"]==e["checks_passed"]==28 and all(x["passed"] for x in e["checks"]) and not e["failed_checks"]})
checks.append({"kind":"origin_no_math_declared","passed":all(e[k]==0 for k in ["new_mathematical_executions","new_cas_runs","new_lean_runs"]) and not e["um_executed_or_imported"]})
assert all(x["passed"] for x in checks),json.dumps([x for x in checks if not x["passed"]],ensure_ascii=False)
def publish(p,b):
 assert not p.exists()
 t=p.with_name(p.name+".tmp_new")
 with t.open("xb") as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==b;os.replace(t,p);assert p.read_bytes()==b
 return pin(p)
report=publish(out/"PARECER_DOCUMENTAL_NARRATIVOS_086.md",d["note"].encode("utf-8"))
final=[pin(p["path"]) for p in before];assert final==after
record={"status":"PASS_DOCUMENTARY_SCOPE","created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"reviewer":"selected_geometry_design","report":report,"sources_before":before,"sources_after":final,"all_sources_unchanged":True,"checks":checks,"checks_passed":sum(x["passed"] for x in checks),"checks_total":len(checks),"failed_checks":[],"counts":{"narratives":3,"pinned_files":len(before),"unique_local_links":len(links),"compared_recorded_canonical_pins":4,"embedded_files":683,"plan_modules":98,"present_modules":77,"absent_modules":21},"canonical_pins_from_snapshots_only":canon,"snapshot_times":{"root":a["created_utc"],"singer":s["created_utc"]},"scope":"Documentary fidelity and pins; not independent approval of the author's own mathematical source.","independence_limits":["Own symbol086/form-normal084 not mathematically reapproved.","Previous W-nabla-W review distinct.","Future addendum/finalizer/tunnel/config/087 excluded."],"resolved_attempts":[{"type":"KeyError bytes","resolution":"Read actual snapshot schema and compare full pins; no writes before failure"},{"type":"Windows CreateProcess206","resolution":"Created a new helper/payload and used a short execution path; no process or writes occurred on failed launch"}],"new_mathematical_executions":0,"new_cas_runs":0,"new_lean_runs":0,"canonical_files_reopened":False,"um_executed_or_imported":False,"existing_files_modified":False,"final_delivery_manifest_audited":False,"own_emitter":pin(__file__),"own_payload":pin(payload)}
receipt=publish(out/"REGISTRO_REVISAO_DOCUMENTAL_086.json",(json.dumps(record,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"status":record["status"],"report":report,"receipt":receipt,"checks_passed":record["checks_passed"],"checks_total":len(checks),"counts":record["counts"]},ensure_ascii=False,indent=2))

