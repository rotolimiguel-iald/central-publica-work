"""Independent static audit of 77 integrated modules; no um.py is executed or imported."""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import ast,hashlib,json,os,re,sys
sys.stdout.reconfigure(encoding="utf-8")
BASE=Path(r"C:\IALD\Central de Patentes\Chatgpt")
OUT=Path(__file__).resolve().parent
FOLDER=BASE/"COPIA_INTEGRADA_20260909_174634_173402"
PREPARER=BASE/"INTEGRADOR_SELETOR_LOCALIDADE_20260909_174443_581582"
checks=[];inputs={}
def rec(p):
 p=Path(p);b=p.read_bytes()
 return {"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def remember(p):
 r=rec(p)
 if r["path"] in inputs:assert inputs[r["path"]]==r,"Input changed: "+r["path"]
 inputs[r["path"]]=r
 return r
def ck(name,ok,detail=None):checks.append({"check":name,"ok":bool(ok),"detail":detail})
def same(r):
 a=remember(r["path"])
 return a["bytes"]==r["bytes"] and a["sha256"]==r["sha256"]
def readj(p):
 remember(p)
 return json.loads(Path(p).read_bytes())
def save(name,value):
 p=OUT/name;assert not p.exists()
 b=value.encode("utf-8");tmp=p.with_name(p.name+".tmp")
 with tmp.open("xb") as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert tmp.read_bytes()==b
 os.replace(tmp,p);assert p.read_bytes()==b
 return rec(p)
def savej(name,value):return save(name,json.dumps(value,ensure_ascii=False,indent=2)+"\n")
def table(p):
 raw=Path(p).read_bytes();bom=3 if raw.startswith(b"\xef\xbb\xbf") else 0
 body=raw[bom:];tree=ast.parse(body.decode("utf-8"))
 found=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="_EMBEDDED_KERNEL_FILES" for t in n.targets)]
 assert len(found)==1 and isinstance(found[0].value,ast.Dict)
 node=found[0];keys=[ast.literal_eval(k) for k in node.value.keys]
 assert len(keys)==len(set(keys))
 value=ast.literal_eval(node.value)
 assert all(isinstance(k,str) and isinstance(v,str) for k,v in value.items())
 lines=body.splitlines(keepends=True)
 start=bom+sum(map(len,lines[:node.value.lineno-1]))+node.value.col_offset
 end=bom+sum(map(len,lines[:node.value.end_lineno-1]))+node.value.end_col_offset
 outside=raw[:start]+b"__REMOVED_TABLE__"+raw[end:]
 sent=[ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="_LEAN_SENTINELS" for t in n.targets)]
 assert len(sent)==1
 node.value=ast.Constant("__REMOVED_TABLE__")
 return value,ast.dump(tree,include_attributes=False),outside,sent[0]

def scrub(s):
 # Nested Lean block comments, line comments and quoted strings; preserve line numbers.
 r=[];i=0;depth=0;quoted=False
 while i<len(s):
  if depth:
   if s.startswith("/-",i):depth+=1;r+=[" "," "];i+=2;continue
   if s.startswith("-/",i):depth-=1;r+=[" "," "];i+=2;continue
   r.append("\n" if s[i]=="\n"else" ");i+=1;continue
  if quoted:
   if s[i]=="\\" and i+1<len(s):r+=[" "," "];i+=2;continue
   if s[i]=='"':quoted=False
   r.append("\n"if s[i]=="\n"else" ");i+=1;continue
  if s.startswith("/-",i):depth=1;r+=[" "," "];i+=2;continue
  if s.startswith("--",i):
   while i<len(s)and s[i]!="\n":r.append(" ");i+=1
   continue
  if s[i]=='"':quoted=True;r.append(" ");i+=1;continue
  r.append(s[i]);i+=1
 return "".join(r)

dp=re.compile(r"^(?P<mods>(?:(?:noncomputable|private|protected|local)\s+)*)(?P<kind>theorem|lemma|def|abbrev|structure|class|instance|opaque|axiom)\s+(?P<name>[\w'.]+)")

def decls(s):
 scopes=[];res=[]
 for ln,line in enumerate(scrub(s).splitlines(),1):
  n=re.match(r"^namespace\s+([\w'.]+)",line)
  if n:scopes.append(("namespace",n[1]));continue
  if re.match(r"^(?:noncomputable\s+)?section(?:\s|$)",line)or re.match(r"^mutual(?:\s|$)",line):scopes.append(("section",""));continue
  if re.match(r"^end(?:\s|$)",line):
   if scopes:scopes.pop()
   continue
  m=dp.match(line)
  if m:
   prefix=".".join(x[1]for x in scopes if x[0]=="namespace");name=m["name"]
   qual=name[7:]if name.startswith("_root_.")else prefix+"."+name if prefix else name
   res.append({"name":qual,"short":name,"kind":m["kind"],"local":"local"in m["mods"].split(),"line":ln})
 return res

scanner=BASE/"AUDITORIA_COCICLO_COVARIANCIA_20260909_161309_333516/audit_continuation_v3.py"
remember(scanner)
prior_auditor=BASE/"AUDITORIA_INTEGRACAO_72_20260909_171311_522844/audit_integration_72.py"
remember(prior_auditor)

# Follow the actual integration lineage; each successor records only its own delta.
stages=[];irpath=FOLDER/"INTEGRATION_RESULT.json";seen=set()
while True:
 assert irpath.as_posix() not in seen,"Integration lineage cycle"
 seen.add(irpath.as_posix());ir=readj(irpath)
 stages.append({"folder":irpath.parent,"path":irpath,"ir":ir})
 parent=ir.get("predecessor_integration_result")
 if not parent:break
 ck("lineage_pin:"+str(len(stages)),same(parent))
 irpath=Path(parent["path"])
stages.reverse()
ck("three_stages_63_9_5",[len(s["ir"]["modules"]) for s in stages]==[63,9,5])
canonicalpath=Path(stages[0]["ir"]["source_um"]["path"])
canonical=remember(canonicalpath)
canon,cast,cbytes,csentinels=table(canonicalpath)
previous=canon;previous_ast=cast;previous_bytes=cbytes;previous_sent=csentinels
allmeta=[];alldecls=[];alltheorems=[];module_rows=[];stage_rows=[]
TRIO={"propext","Classical.choice","Quot.sound"}
for number,stage in enumerate(stages):
 folder=stage["folder"];ir=stage["ir"];label=f"stage{number+1}"
 cfg=readj(folder/"CONFIG_APROVADA.json")
 sp=folder/"um_ORIGINAL_SNAPSHOT.py";ip=folder/"um.py";source=Path(ir["source_um"]["path"])
 ck(label+":source_pin",same(ir["source_um"]))
 ck(label+":snapshot_pin",same(ir["original_copy"]))
 ck(label+":integrated_pin",same(ir["integrated_copy"]))
 remember(sp);remember(ip)
 ck(label+":snapshot_bytes_exact",sp.read_bytes()==source.read_bytes())
 ck(label+":configured_root_confirmation",cfg["root_confirmed"] is True)
 ck(label+":configured_source",cfg["source_um_sha256"]==rec(source)["sha256"] and Path(cfg["source_um"]).resolve()==source.resolve())
 ck(label+":configuration_module_set",{Path(x["source"]).stem for x in cfg["modules"]}=={m["module"] for m in ir["modules"]})
 if number:
  pred=stages[number-1]
  ck(label+":immediate_predecessor",ir["source_um"]==pred["ir"]["integrated_copy"])
  ck(label+":predecessor_integration_pin",same(ir["predecessor_integration_result"]))
  ck(label+":configured_predecessor",cfg["predecessor_integration_result"]==ir["predecessor_integration_result"] and cfg["predecessor_build_result"]==ir["predecessor_build_result"])
  br=readj(ir["predecessor_build_result"]["path"])
  ck(label+":predecessor_build_pin",same(ir["predecessor_build_result"]))
  ck(label+":predecessor_PASS",br["status"]=="PASS_TRANSPOSED_SCOPE" and br["input_boundary_unchanged"] and br["cached_boundary_unchanged"] and all(r["exit_code"]==0 and r["valid"] and r["warning_lines"]==0 for r in br["runs"]))
  ck(label+":predecessor_plan_pin",same(br["plan"]))
  bp=readj(br["plan"]["path"])
  ck(label+":predecessor_plan_integration_pin",same(bp["integration_result"]) and bp["integration_result"]==ir["predecessor_integration_result"])
  ck(label+":predecessor_plan_program_pin",same(bp["integrated_copy"]) and bp["integrated_copy"]==ir["source_um"])
  ck(label+":cached_old_sources_preserved",all(x.get("source_bytes_identical") and x["prior_run"]["valid"] for x in br["cached_modules"]))
 new,nast,nbytes,nsentinels=table(ip)
 _,sast,sbytes,ssentinels=table(sp)
 ck(label+":outside_table_AST_exact",previous_ast==nast==sast==cast)
 ck(label+":outside_table_bytes_exact",previous_bytes==nbytes==sbytes==cbytes)
 ck(label+":sentinels_exact",previous_sent==nsentinels==ssentinels==csentinels)
 ck(label+":no_execution_or_flags_reported",not ir["source_um_executed"] and not ir["integrated_copy_executed"] and not ir["canonical_changes"] and not ir["new_individual_json_flags_added"])
 names={m["module"] for m in ir["modules"]};keys={m["key"] for m in ir["modules"]}
 ck(label+":exact_added_keys",set(new)-set(previous)==keys and len(keys)==len(names)==len(ir["modules"]))
 ck(label+":no_deletions",set(previous)<=set(new))
 ck(label+":only_old_aggregators_changed",{k for k in previous if previous[k]!=new[k]}=={"TGLExt.lean","TGL/Audit.lean"})
 recognized={Path(k).stem for k in previous if k.startswith("TGLExt/") and k.endswith(".lean")}
 if number:ck(label+":recognized_import_targets",set(ir["existing_import_targets_recognized"])==recognized)
 rewrite=names|recognized if number else names
 ds_stage=[];th_stage=[];local_stage=[];deps={}
 for m in ir["modules"]:
  name=m["module"];prefix=label+":"+name
  rawpath=Path(m["source"]["path"]);actual=remember(rawpath)
  ck(prefix+":source_pin",same(m["source"]))
  ck(prefix+":leaf_receipt_pin",same(m["build_result"]))
  leaf=readj(m["build_result"]["path"])
  ck(prefix+":source_in_PASS_receipt",leaf["status"]=="PASS_COMPILED_SCOPE" and any(Path(p["path"]).stem==name and p["sha256"]==actual["sha256"] and p["bytes"]==actual["bytes"] for p in leaf["sources"]))
  ck(prefix+":leaf_module_exit_zero",any(r["module"]==name and r["exit_code"]==0 for r in leaf["runs"]))
  s=rawpath.read_text(encoding="utf-8").replace("\r\n","\n").replace("\r","\n")
  changes=[]
  def fix(mt):
   if mt[1] in rewrite:
    changes.append({"from":mt[1],"to":"TGLExt."+mt[1]})
    return "import TGLExt."+mt[1]
   return mt[0]
  transposed=re.sub(r"(?m)^import ([\w.]+)$",fix,s)
  ck(prefix+":exact_import_only_transposition",new[m["key"]]==transposed)
  ck(prefix+":metadata_transpositions_exact",m["import_transpositions"]==changes)
  tp=folder/"transposed_sources"/m["key"];remember(tp)
  ck(prefix+":transposed_file_exact",tp.read_bytes()==transposed.encode("utf-8"))
  ds=decls(s)
  expected=[{"kind":"local instance" if d["kind"]=="instance" and d["local"] else d["kind"],"name":d["name"]} for d in ds]
  ck(prefix+":independent_declaration_scan",m["declarations"]==expected)
  ds_names={d["name"] for d in ds};rows=[r for r in leaf["axiom_rows"] if r["name"] in ds_names]
  ck(prefix+":all_explicit_terms_audited",Counter(r["name"] for r in rows)==Counter(d["name"] for d in ds))
  ck(prefix+":standard_axioms",all(set(r["axioms"])<=TRIO for r in rows))
  ck(prefix+":no_escape_tokens",not re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b",scrub(s)))
  th=[d["name"] for d in ds if d["kind"] in {"theorem","lemma"}]
  loc=[d["name"] for d in ds if d["kind"]=="instance" and d["local"]]
  imports=re.findall(r"(?m)^import ([\w.]+)$",scrub(transposed))
  ck(prefix+":no_bare_local_imports",all(x not in rewrite for x in imports))
  for imp in imports:
   if imp.startswith(("TGLExt.","TGL.")):ck(prefix+":embedded_import:"+imp,imp.replace(".","/")+".lean" in new)
  deps[name]=[x[7:] for x in imports if x.startswith("TGLExt.") and x[7:] in names]
  module_rows.append({"stage":number+1,"module":name,"source":actual,"receipt":remember(m["build_result"]["path"]),"transposed":remember(tp),"key":m["key"],"theorems":len(th),"others":len(ds)-len(th),"local_instances":loc})
  ds_stage+=ds;th_stage+=th;local_stage+=loc
  allmeta.append(m)
 ck(label+":declaration_metadata",Counter(d["name"] for d in ds_stage)==Counter(ir["all_declaration_names"]))
 ck(label+":theorem_metadata",th_stage==ir["theorem_names"])
 ck(label+":local_instances_metadata",Counter(local_stage)==Counter(ir["local_instance_names"]))
 dc={"modules":len(names),"theorems":len(th_stage),"other_declarations":len(ds_stage)-len(th_stage),"local_instances":len(local_stage),"total":len(ds_stage)}
 ck(label+":counts_metadata",dc==ir["declaration_counts"])
 for key in ["TGLExt.lean","TGL/Audit.lean"]:
  ck(label+":additive:"+key,new[key].startswith(previous[key]))
 rootdelta=new["TGLExt.lean"][len(previous["TGLExt.lean"]):]
 auditdelta=new["TGL/Audit.lean"][len(previous["TGL/Audit.lean"]):]
 rootimports=re.findall(r"(?m)^import ([\w.]+)$",scrub(rootdelta))
 auditprints=re.findall(r"(?m)^#print axioms ([\w'.]+)$",scrub(auditdelta))
 ck(label+":exact_aggregator_imports",Counter(rootimports)==Counter("TGLExt."+n for n in names))
 ck(label+":exact_aggregator_theorems",auditprints==th_stage)
 ck(label+":no_extra_root_code",not re.sub(r"(?m)^import [\w.]+\s*$","",scrub(rootdelta)).strip())
 ck(label+":no_extra_audit_code",not re.sub(r"(?m)^#print axioms [\w'.]+\s*$","",scrub(auditdelta)).strip())
 order=ir["transposed_module_order"];positions={n:i for i,n in enumerate(order)}
 ck(label+":topological_order",len(order)==len(names) and set(order)==names and all(positions[d]<positions[n] for n,dd in deps.items() for d in dd))
 ck(label+":embedded_count_metadata",len(previous)==ir["old_embedded_file_count"] and len(new)==ir["new_total_embedded_file_count"] and len(names)==ir["new_embedded_file_count"])
 stage_rows.append({"integration":remember(stage["path"]),"configuration":remember(folder/"CONFIG_APROVADA.json"),"source":remember(source),"snapshot":remember(sp),"integrated":remember(ip),"counts":dc,"old_embedded":len(previous),"new_embedded":len(new),"new_lean":sum(k.endswith(".lean") for k in new)})
 alldecls+=ds_stage;alltheorems+=th_stage
 previous,previous_ast,previous_bytes,previous_sent=new,nast,nbytes,nsentinels
final=previous
ck("all_77_sources_preserved_in_final",all(final[m["key"]]==(Path(module_rows[i]["transposed"]["path"]).read_text(encoding="utf-8")) for i,m in enumerate(allmeta)))
totals={"modules":len(module_rows),"theorems":len(alltheorems),"other_declarations":len(alldecls)-len(alltheorems),"local_instances":sum(d["kind"]=="instance" and d["local"] for d in alldecls),"total":len(alldecls)}
ck("measured_77_1065_293_1358",totals=={"modules":77,"theorems":1065,"other_declarations":293,"local_instances":7,"total":1358})
ck("delta5_93_29_122",stage_rows[-1]["counts"]=={"modules":5,"theorems":93,"other_declarations":29,"local_instances":0,"total":122})
ck("embedded_counts_606_669_678_683",[len(canon)]+[r["new_embedded"] for r in stage_rows]==[606,669,678,683])
ck("lean_counts_602_665_674_679",[sum(k.endswith(".lean") for k in canon)]+[r["new_lean"] for r in stage_rows]==[602,665,674,679])
dups={n:c for n,c in Counter(d["name"] for d in alldecls).items() if c>1}
ck("no_duplicate_full_names_among77",not dups,dups)
canonicalnames=defaultdict(list)
for k,s in canon.items():
 if k.endswith(".lean"):
  for d in decls(s):canonicalnames[d["name"]].append(k)
collisions={d["name"]:canonicalnames[d["name"]] for d in alldecls if d["name"] in canonicalnames}
ck("no_new_full_names_collide_with_canonical",not collisions,collisions)
phase=[]
for k,s in final.items():
 if k.endswith(".lean"):
  phase += [{"key":k,"qualified_name":d["name"],"line":d["line"]} for d in decls(s) if d["short"]=="phaseReading"]
ck("short_phaseReading_ambiguity_preserved",len(phase)==2)
rd=final["TGLExt.lean"][len(canon["TGLExt.lean"]):]
ad=final["TGL/Audit.lean"][len(canon["TGL/Audit.lean"]):]
ck("cumulative_77_imports",Counter(re.findall(r"(?m)^import ([\w.]+)$",scrub(rd)))==Counter("TGLExt."+m["module"] for m in allmeta))
ck("cumulative_1065_theorem_audits",re.findall(r"(?m)^#print axioms ([\w'.]+)$",scrub(ad))==alltheorems)

procedures=[]
for name in ["integrate_approved_copy.py","prepare_successor.py","run_successor.py"]:
 p=PREPARER/name;remember(p);ast.parse(p.read_bytes().decode("utf-8"))
 procedures.append(rec(p))
prepared=None;combined=None
prep_path=PREPARER/"RECIBO_PREPARACAO_SUCESSORA.json"
if prep_path.exists():
 prep=readj(prep_path);ck("prepared_plan_pin",same(prep["plan"]));plan=readj(prep["plan"]["path"])
 build=Path(plan["build"]);auditpath=build/"NewModulesAudit.lean";remember(auditpath)
 declarations=re.findall(r"(?m)^#print axioms ([\w'.]+)$",scrub(auditpath.read_text(encoding="utf-8")))
 ck("dedicated_audit_all1358",Counter(declarations)==Counter(d["name"] for d in alldecls) and len(declarations)==1358)
 ck("plan_all77_module_metadata",{m["module"]:m for m in plan["modules"]}=={m["module"]:m for m in allmeta})
 ck("plan_all1358_names",Counter(plan["declaration_names"])==Counter(d["name"] for d in alldecls))
 ck("plan_program_and_integration_pins",same(plan["integrated_copy"]) and same(plan["integration_result"]) and plan["integrated_copy"]==stages[-1]["ir"]["integrated_copy"])
 for item in plan["source_files"]:ck("prepared_source_pin:"+item["path"],same(item))
 expected_full=re.findall(r"(?m)^#print axioms ([\w'.]+)$",scrub(final["TGL/Audit.lean"]))
 fullrun=[r for r in plan["runs"] if r["module"]=="FullTGLAudit"]
 ck("plan_FullTGLAudit5557_exact",len(fullrun)==1 and len(expected_full)==5557 and fullrun[0]["expected_axiom_terms"]==expected_full)

 ck("dedicated_audit_seven_instances",all(d["name"] in declarations for d in alldecls if d["kind"]=="instance" and d["local"]))
 ck("prepared_72_cache_5_new_3_aggregates",len(plan["cached_modules"])==72 and len(plan["runs"])==8 and [r["module"] for r in plan["runs"][:5]]==stages[-1]["ir"]["transposed_module_order"])
 ck("prepared_sources_match_all77",all((build/"TGLExt"/(m["module"]+".lean")).read_bytes()==final[m["key"]].encode("utf-8") for m in allmeta))
 prepared={"receipt":remember(prep_path),"plan":remember(prep["plan"]["path"]),"dedicated_audit":remember(auditpath),"counts":plan["counts"],"executed_by_this_audit":False}
 combined_path=build/"TRANSPOSED_RESULT.json"
 if combined_path.exists():
  cr=readj(combined_path)
  ck("combined_plan_pin",same(cr["plan"]) and cr["plan"]==rec(Path(prep["plan"]["path"])))
  ck("combined_PASS_8_clean_exits",cr["status"]=="PASS_TRANSPOSED_SCOPE" and len(cr["runs"])==8 and all(r["exit_code"]==0 and r["valid"] and r["warning_lines"]==0 for r in cr["runs"]))
  ck("combined_boundaries_preserved",cr["input_boundary_unchanged"] and cr["cached_boundary_unchanged"] and not cr["um_py_executed"])
  expected_runs={r["module"]:r for r in plan["runs"]}
  for run in cr["runs"]:
   ck("combined_terms:"+run["module"],Counter(x["name"] for x in run["axiom_rows"])==Counter(expected_runs[run["module"]]["expected_axiom_terms"]) and all(set(x["axioms"])<=TRIO for x in run["axiom_rows"]))
  for m in allmeta:
   binary=build/"TGLExt"/(m["module"]+".olean")
   ck("all77_compiled_artifacts:"+m["module"],binary.is_file())
   if binary.is_file():remember(binary)
  combined={"receipt":remember(combined_path),"status":cr["status"],"runs":len(cr["runs"]),"FullTGLAudit":5557,"NewModulesAudit":1358,"executed_by_this_audit":False}

for p,r in list(inputs.items()):ck("stable:"+p,rec(p)==r)
status="PASS_STATIC_INTEGRATION_SCOPE" if all(c["ok"] for c in checks) else "FAIL_VISIBLE_STATIC_INTEGRATION_SCOPE"
result={"status":status,"created_utc":datetime.now(timezone.utc).isoformat(),"counts":{"checks":len(checks),"passed_checks":sum(c["ok"] for c in checks),**totals},"delta_counts":stage_rows[-1]["counts"],"stages":stage_rows,"modules":module_rows,"canonical":canonical,"canonical_snapshot":stage_rows[0]["snapshot"],"current_canonical":canonical,"integrated":remember(FOLDER/"um.py"),"final_integrated":remember(FOLDER/"um.py"),"checks_passed":sum(c["ok"] for c in checks),"checks_total":len(checks),"approved_configuration":remember(FOLDER/"CONFIG_APROVADA.json"),"checks":checks,"failed_checks":[c for c in checks if not c["ok"]],"name_collisions":{"among77":dups,"with_canonical":collisions},"phaseReading_diagnostic":{"status":"AMBIGUOUS_SHORT_NAME_PRESERVED","matches":phase},"prepared_successor":prepared,"combined_build_read":combined,"procedures_parsed_not_executed":procedures,"scope":{"um_py_executed_or_imported":False,"integrator_executed_by_auditor":False,"build_executed_by_auditor":False,"outside_table_AST_and_bytes_preserved":cast==previous_ast and cbytes==previous_bytes,"new_individual_flags":False},"limits":["Static integration audit; no runtime execution, seal or physical verdict.","Explicit declaration scan includes named local instances, but excludes generated declarations and a whole-Mathlib name scan.","Leaf PASS precedes exact import transposition; combined compilation is separate.","The predecessor build has scoped cache provenance, not a full fresh rebuild or hash of every external transitive dependency."],"inputs":[r for r in inputs.values()]}
out=savej("AUDITORIA_INTEGRACAO_77.json",result)
note=f"""# Auditoria estática independente da sucessora77

{status}

[REAL — medido] {totals['modules']} módulos: {totals['theorems']} teoremas e {totals['other_declarations']} outras declarações, total {totals['total']}, incluindo sete instâncias locais nomeadas. Delta da predecessora72: cinco módulos, 93 teoremas e 29 outras declarações, 122 termos.

A genealogia inteira foi percorrida: canônico → lote63 → delta9 (72) → delta5 (77). O recibo da camada72 contém apenas seu delta9; ele não foi confundido com o inventário cumulativo. Foram verificadas todas as 77 fontes, seus hashes/recibos, transposições exatas dos imports e preservação das fontes em cada sucessora.

AST e bytes fora de _EMBEDDED_KERNEL_FILES permanecem idênticos em toda a cadeia. As sentinelas são exatas. Dentro da tabela, somente as novas entradas e acréscimos aditivos nos agregadores TGLExt.lean e TGL/Audit.lean mudaram. Código externo, flags e gate não foram alterados.

Arquivos embutidos: 606 → 669 → 678 → 683. Arquivos Lean: 602 → 665 → 674 → 679. Os 93 novos teoremas foram acrescentados à auditoria agregada; o total cumulativo acrescentado é de 1065. Não houve colisão de nomes completos entre as declarações explícitas novas nem com as canônicas. A ambiguidade curta phaseReading permanece em dois namespaces distintos.

"""
note+=("O plano preparado já foi lido: 72 módulos em cache, cinco folhas novas e três agregadores. NewModulesAudit contém exatamente os 1358 termos, incluindo as sete instâncias, e as 77 fontes preparadas coincidem com a tabela final.\n\n" if prepared else "A preparação da compilação ainda não tinha recibo durante esta leitura; a auditoria dedicada de 1358 termos e o resultado da compilação serão verificados separadamente.\n\n")
if combined:note+="O recibo da compilação conjunta foi lido: PASS_TRANSPOSED_SCOPE, oito processos com exit 0, sem avisos; FullTGLAudit5557 e NewModulesAudit1358 conferidos contra o plano. O auditor não executou a compilação.\n\n"
note+=f"Verificações: {result['counts']['passed_checks']}/{result['counts']['checks']}. [Recibo completo](<{(OUT/'AUDITORIA_INTEGRACAO_77.json').as_posix()}>).\n\n"
note+="Nenhum um.py foi executado/importado. O auditor não executou integrador, preparador ou compilação. Nenhum original ou fonte congelada foi alterado. A auditoria estática não substitui o recibo de compilação conjunta, execução de runtime ou veredito físico.\n"
report=save("RELATORIO_INTEGRACAO_77.md",note)
manifest=savej("MANIFESTO_AUDITORIA_77.json",{"status":status,"artifacts":[out,report],"script":rec(Path(__file__))})
print(json.dumps({"status":status,"counts":result["counts"],"delta":result["delta_counts"],"failed_checks":result["failed_checks"],"prepared":prepared,"final":result["final_integrated"],"outputs":[out,report,manifest]},ensure_ascii=False,indent=2))
