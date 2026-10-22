"""Independent static integration audit: AST and byte reads; never import or run um.py."""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import ast,copy,hashlib,json,os,re,sys
sys.stdout.reconfigure(encoding="utf-8")
base=Path(r"C:\IALD\Central de Patentes\Chatgpt")
out=base/"AUDITORIA_COCICLO_COVARIANCIA_20260909_161309_333516"
folder=base/"COPIA_INTEGRADA_20260909_161645_481582"
checks=[];inputs={};mods=[]
def rec(p):
 p=Path(p);raw=p.read_bytes()
 return {"path":p.as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
def remember(p):
 r=rec(p);inputs[r["path"]]=r;return r
def ck(name,ok,detail=None):checks.append({"check":name,"ok":bool(ok),"detail":detail})
def same(r):
 now=remember(r["path"]);return now["bytes"]==r["bytes"]and now["sha256"]==r["sha256"]
def write_new(name,obj):
 p=out/name;t=p.with_name(p.name+".tmp");assert not p.exists()and not t.exists()
 b=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
 with t.open("xb")as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==b;os.rename(t,p);assert p.read_bytes()==b
 return rec(p)
# Reuse only pure lexical scanner definitions, extracted by AST; the evidence-audit main is not executed.
scanner=out/"audit_continuation_v3.py";remember(scanner)
st=ast.parse(scanner.read_text(encoding="utf-8"))
chosen=[]
for n in st.body:
 if isinstance(n,ast.FunctionDef)and n.name in{"scrub","decls"}:chosen.append(n)
 if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=="dp"for t in n.targets):chosen.append(n)
assert len(chosen)==3
scope={"re":re};exec(compile(ast.Module(body=chosen,type_ignores=[]),"<pure_lean_scanner>","exec"),scope)
decls=scope["decls"];scrub=scope["scrub"]
def table(raw):
 text=raw.decode("utf-8-sig");tree=ast.parse(text)
 nodes=[n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=="_EMBEDDED_KERNEL_FILES"for t in n.targets)]
 assert len(nodes)==1
 n=nodes[0];assert isinstance(n.value,ast.Dict)
 keys=[ast.literal_eval(k)for k in n.value.keys];assert len(keys)==len(set(keys))
 t=ast.literal_eval(n.value);assert all(isinstance(k,str)and isinstance(v,str)for k,v in t.items())
 # Python AST columns count UTF-8 bytes, so compute byte offsets using the original bytes.
 lines=raw.splitlines(keepends=True)
 start=sum(map(len,lines[:n.value.lineno-1]))+n.value.col_offset
 end=sum(map(len,lines[:n.value.end_lineno-1]))+n.value.end_col_offset
 outside=raw[:start]+b"__AUDIT_REMOVED_EMBEDDED_VALUE__"+raw[end:]
 n.value=ast.Constant(value="__AUDIT_REMOVED_EMBEDDED_VALUE__")
 return t,ast.dump(tree,include_attributes=False),outside
irp=folder/"INTEGRATION_RESULT.json";remember(irp);ir=json.loads(irp.read_text(encoding="utf-8"))
cp=folder/"CONFIG_APROVADA.json";remember(cp);cfg=json.loads(cp.read_text(encoding="utf-8"))
ip=folder/"um.py";sp=folder/"um_ORIGINAL_SNAPSHOT.py";np=Path(ir["source_um"]["path"])
integrated=remember(ip);snapshot=remember(sp);canonical=remember(np)
ck("integration_record_integrated",same(ir["integrated_copy"]))
ck("integration_record_snapshot",same(ir["original_copy"]))
ck("integration_record_current_canonical",same(ir["source_um"]))
ck("snapshot_byte_equal_current",sp.read_bytes()==np.read_bytes())
ck("configuration_current_source_hash",canonical["sha256"]==cfg["source_um_sha256"])
ck("configuration_explicitly_approved",cfg["root_confirmed"]is True)
a,aa,ab=table(sp.read_bytes());b,ba,bb=table(ip.read_bytes())
ck("AST_outside_table_identical",aa==ba)
ck("bytes_outside_table_identical",ab==bb)
newkeys=set(b)-set(a);removed=set(a)-set(b)
changed={k for k in set(a)&set(b)if a[k]!=b[k]}
expectedkeys={m["key"]for m in ir["modules"]};names={m["module"]for m in ir["modules"]}
ck("new_63_keys_exact",newkeys==expectedkeys and len(newkeys)==63,sorted(newkeys))
ck("no_old_keys_removed",not removed,sorted(removed))
ck("only_root_and_audit_modified",changed=={"TGLExt.lean","TGL/Audit.lean"},sorted(changed))
ck("configuration_same_module_set",{Path(x["source"]).stem for x in cfg["modules"]}==names)
module_meta={m["module"]:m for m in ir["modules"]};all_decs=[];all_theorems=[];local_instances=[];dependency_map={}
for name,m in module_meta.items():
 src=Path(m["source"]["path"]);r=remember(src);s=src.read_bytes().decode("utf-8").replace("\r\n","\n").replace("\r","\n")
 ck(name+":frozen_source_hash",same(m["source"]))
 ck(name+":frozen_PASS_receipt_hash",same(m["build_result"]))
 pr=json.loads(Path(m["build_result"]["path"]).read_text(encoding="utf-8"))
 ck(name+":PASS_source_match",pr.get("status")=="PASS_COMPILED_SCOPE"and any(Path(v["path"]).stem==name and v["sha256"]==r["sha256"]for v in pr["sources"]))
 transpositions=[]
 def fix(mt):
  imp=mt[1]
  if imp in names:
   transpositions.append({"from":imp,"to":"TGLExt."+imp});return "import TGLExt."+imp
  return mt[0]
 expected=re.sub(r"(?m)^import ([\w.]+)$",fix,s)
 ck(name+":only_import_transposition",b[m["key"]]==expected)
 tp=folder/"transposed_sources"/m["key"]
 ck(name+":transposed_file_equals_embedded",tp.read_bytes()==expected.encode("utf-8"));remember(tp)
 ck(name+":import_transposition_metadata",m["import_transpositions"]==transpositions)
 ds=decls(s)
 expected_ds=[{"kind":"local instance"if d["kind"]=="instance"and d["local"]else d["kind"],"name":d["name"]}for d in ds]
 ck(name+":declarations_include_instances",m["declarations"]==expected_ds)
 # This is an explicit-declaration scan, independently matched to the compiled leaf's audit rows.
 actual_rows=[x["name"]for x in pr["axiom_rows"]if x["name"]in{d["name"]for d in ds}]
 ck(name+":declarations_match_leaf_axiom_rows",Counter(actual_rows)==Counter(d["name"]for d in ds))
 all_decs+=expected_ds;all_theorems += [d["name"]for d in ds if d["kind"]in{"theorem","lemma"}]
 local_instances += [d["name"]for d in ds if d["kind"]=="instance"and d["local"]]
 imports=re.findall(r"(?m)^import ([\w.]+)$",scrub(expected))
 dep=[x[7:]for x in imports if x.startswith("TGLExt.")and x[7:]in names];dependency_map[name]=dep
 ck(name+":local_imports_transposed",all(imp not in names for imp in imports))
 mods.append({"module":name,"source":r,"receipt":remember(m["build_result"]["path"]),"transposed":remember(tp),
  "theorems":sum(d["kind"]in{"theorem","lemma"}for d in ds),"others":sum(d["kind"]not in{"theorem","lemma"}for d in ds),
  "local_instances":[d["name"]for d in ds if d["kind"]=="instance"and d["local"]],"direct_new_dependencies":dep})
ck("all_declarations_metadata",Counter(d["name"]for d in all_decs)==Counter(ir["all_declaration_names"]))
ck("theorem_names_metadata",all_theorems==ir["theorem_names"])
ck("local_instance_metadata",Counter(local_instances)==Counter(ir["local_instance_names"]))
ck("seven_local_instances_named",len(local_instances)==7 and len(set(local_instances))==7)
dups={k:v for k,v in Counter(d["name"]for d in all_decs).items()if v>1}
ck("no_new_full_name_collisions",not dups,dups)
oldnames=defaultdict(list);phase=[]
for key,text in a.items():
 if not key.endswith(".lean"):continue
 for d in decls(text):
  oldnames[d["name"]].append(key)
  if d["short"]=="phaseReading":phase.append({"key":key,"qualified_name":d["name"],"line":d["line"]})
collision={d["name"]:oldnames[d["name"]]for d in all_decs if d["name"]in oldnames}
ck("no_new_names_collide_with_original_explicit_names",not collision,collision)
phase += [{"key":m["key"],"qualified_name":d["name"],"line":d["line"]}for m in ir["modules"]for d in decls(b[m["key"]])if d["short"]=="phaseReading"]
root=b["TGLExt.lean"];audit=b["TGL/Audit.lean"]
ck("root_additive_prefix",root.startswith(a["TGLExt.lean"]))
ck("audit_additive_prefix",audit.startswith(a["TGL/Audit.lean"]))
rootdelta=root[len(a["TGLExt.lean"]):];auditdelta=audit[len(a["TGL/Audit.lean"]):]
rootimports=re.findall(r"(?m)^import ([\w.]+)$",scrub(rootdelta))
auditprints=re.findall(r"(?m)^#print axioms ([\w'.]+)$",scrub(auditdelta))
ck("root_exact_63_new_imports",Counter(rootimports)==Counter("TGLExt."+n for n in names))
ck("audit_exact_856_new_theorems",auditprints==all_theorems and len(auditprints)==856)
ck("root_no_extra_executable_lean",not re.sub(r"(?m)^import [\w.]+\s*$","",scrub(rootdelta)).strip())
ck("audit_no_extra_executable_lean",not re.sub(r"(?m)^#print axioms [\w'.]+\s*$","",scrub(auditdelta)).strip())
order=ir["transposed_module_order"];pos={n:i for i,n in enumerate(order)}
ck("topological_order_complete",len(order)==63 and set(order)==names)
ck("topological_order_correct",all(pos[d]<pos[n]for n,deps in dependency_map.items()for d in deps))
decl_counts={"modules":len(mods),"theorems":len(all_theorems),"other_declarations":len(all_decs)-len(all_theorems),"local_instances":len(local_instances),"total":len(all_decs)}
ck("declaration_counts_match_measured",decl_counts==ir["declaration_counts"])
ck("old_files_606_new_669",len(a)==606 and len(b)==669)
ck("old_lean_602_new_665",sum(k.endswith(".lean")for k in a)==602 and sum(k.endswith(".lean")for k in b)==665)
ck("sentinels_flags_gate_preserved_by_AST_and_bytes",aa==ba and ab==bb)
ck("no_individual_json_flags_added",aa==ba and all(k.endswith(".lean")for k in newkeys))
for path,r in list(inputs.items()):ck("stable:"+path,rec(path)==r)
canonical_after=rec(np)
result={"status":"PASS_STATIC_INTEGRATION_SCOPE"if all(x["ok"]for x in checks)else"FAIL_VISIBLE_STATIC_INTEGRATION_SCOPE",
 "created_utc":datetime.now(timezone.utc).isoformat(),"counts":{"checks":len(checks),"passed_checks":sum(x["ok"]for x in checks),**decl_counts},
 "integrated":integrated,"snapshot":snapshot,"current_canonical":canonical_after,"current_canonical_before":canonical,
 "integration_result":rec(irp),"approved_configuration":rec(cp),"modules":mods,"checks":checks,"failed_checks":[x for x in checks if not x["ok"]],
 "embedded_counts":{"before":len(a),"after":len(b),"lean_before":sum(k.endswith(".lean")for k in a),"lean_after":sum(k.endswith(".lean")for k in b)},
 "collisions":{"within_new":dups,"with_original":collision},"phaseReading_diagnostic":{"status":"AMBIGUOUS_SHORT_NAME_PRESERVED","matches":phase},
 "scope":{"um_py_executed_or_imported":False,"new_compile_executed":False,"existing_files_written":False,"outside_table_AST_and_bytes_unchanged":aa==ba and ab==bb,
 "TGL_Audit":"856 new theorems only","leaf_and_dedicated_policy":"1098 declarations, including 7 named local instances. Dedicated compilation is performed separately by root."},
 "limits":["Static integration correctness only; no runtime seal or new per-theorem JSON flags.",
 "Explicit declaration name scan excludes generated names; no whole-Mathlib namespace scan.",
 "Build receipts match the frozen pre-transposition sources. Joint transposed compilation is separate and not assumed by this static result."]}
r=write_new("AUDITORIA_INTEGRACAO_63.json",result)
print(json.dumps({"status":result["status"],"counts":result["counts"],"failed_checks":result["failed_checks"],"phaseReading":phase,"output":r},ensure_ascii=False,indent=2))
