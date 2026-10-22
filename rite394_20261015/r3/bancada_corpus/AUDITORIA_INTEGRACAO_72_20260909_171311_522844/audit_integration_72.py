"""Independent static audit of the 72-module successor; never execute or import any um.py."""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import ast,hashlib,json,os,re,sys
sys.stdout.reconfigure(encoding="utf-8")
BASE=Path(r"C:\IALD\Central de Patentes\Chatgpt")
OUT=Path(__file__).resolve().parent
FOLDER=BASE/"COPIA_INTEGRADA_20260909_170914_653192"
checks=[];inputs={}
def rec(p):
 p=Path(p);b=p.read_bytes();return {"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def remember(p):
 r=rec(p)
 if r["path"] in inputs:assert inputs[r["path"]]==r,"Input changed during review: "+r["path"]
 inputs[r["path"]]=r;return r
def ck(name,ok,detail=None):checks.append({"check":name,"ok":bool(ok),"detail":detail})
def same(r):
 a=remember(r["path"]);return a["bytes"]==r["bytes"]and a["sha256"]==r["sha256"]
def readj(p):remember(p);return json.loads(Path(p).read_text(encoding="utf-8"))
def save(name,text):
 p=OUT/name;assert not p.exists();b=text.encode("utf-8");t=p.with_name(p.name+".tmp")
 with t.open("xb")as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==b and b;t.rename(p);assert p.read_bytes()==b;return rec(p)
def savej(name,obj):return save(name,json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
# Only pure lexical declarations are loaded from the earlier reviewed scanner.
scanner=BASE/"AUDITORIA_COCICLO_COVARIANCIA_20260909_161309_333516"/"audit_continuation_v3.py"
remember(scanner);st=ast.parse(scanner.read_text(encoding="utf-8"));chosen=[]
for n in st.body:
 if isinstance(n,ast.FunctionDef)and n.name in {"scrub","decls"}:chosen.append(n)
 if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=="dp"for t in n.targets):chosen.append(n)
assert len(chosen)==3
scope={"re":re};exec(compile(ast.Module(body=chosen,type_ignores=[]),"<pure_lean_scanner>","exec"),scope)
decls=scope["decls"];scrub=scope["scrub"]
def table(p):
 raw=Path(p).read_bytes();tree=ast.parse(raw.decode("utf-8-sig"))
 found=[n for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=="_EMBEDDED_KERNEL_FILES"for t in n.targets)]
 assert len(found)==1 and isinstance(found[0].value,ast.Dict);node=found[0]
 keys=[ast.literal_eval(x)for x in node.value.keys];assert len(keys)==len(set(keys))
 embedded=ast.literal_eval(node.value);assert all(isinstance(k,str)and isinstance(v,str)for k,v in embedded.items())
 lines=raw.splitlines(keepends=True)
 start=sum(map(len,lines[:node.value.lineno-1]))+node.value.col_offset
 end=sum(map(len,lines[:node.value.end_lineno-1]))+node.value.end_col_offset
 outside=raw[:start]+b"__REMOVED_TABLE__"+raw[end:]
 sentinels=[ast.literal_eval(n.value)for n in tree.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=="_LEAN_SENTINELS"for t in n.targets)]
 assert len(sentinels)==1
 node.value=ast.Constant("__REMOVED_TABLE__")
 return embedded,ast.dump(tree,include_attributes=False),outside,sentinels[0]

irpath=FOLDER/"INTEGRATION_RESULT.json";ir=readj(irpath)
cfgpath=FOLDER/"CONFIG_APROVADA.json";cfg=readj(cfgpath)
predirpath=Path(ir["predecessor_integration_result"]["path"]);predir=readj(predirpath);predfolder=predirpath.parent
predbuildpath=Path(ir["predecessor_build_result"]["path"]);predbuild=readj(predbuildpath)
predplan=readj(predbuild["plan"]["path"])
ip=FOLDER/"um.py";sp=FOLDER/"um_ORIGINAL_SNAPSHOT.py";pp=Path(ir["source_um"]["path"])
op=Path(predir["source_um"]["path"]);osp=predfolder/"um_ORIGINAL_SNAPSHOT.py"
integrated=remember(ip);snapshot=remember(sp);predecessor=remember(pp);canonical=remember(op);original_snapshot=remember(osp)
for title,record in [
 ("new_integrated_pin",ir["integrated_copy"]),("new_snapshot_pin",ir["original_copy"]),("new_predecessor_pin",ir["source_um"]),
 ("predecessor_integration_pin",ir["predecessor_integration_result"]),("predecessor_build_pin",ir["predecessor_build_result"]),
 ("predecessor_integrated_pin",predir["integrated_copy"]),("predecessor_original_snapshot_pin",predir["original_copy"]),("predecessor_canonical_pin",predir["source_um"]),
 ("predecessor_build_plan_pin",predbuild["plan"]),("predecessor_build_integration_pin",predplan["integration_result"]),("predecessor_build_program_pin",predplan["integrated_copy"])]:
 ck(title,same(record))
ck("new_source_is_predecessor_program",predecessor==predir["integrated_copy"]==predplan["integrated_copy"])
ck("new_snapshot_equals_predecessor_bytes",sp.read_bytes()==pp.read_bytes())
ck("canonical_snapshot_equals_current_bytes",osp.read_bytes()==op.read_bytes())
ck("config_confirmed",cfg["root_confirmed"]is True)
ck("config_hash_and_predecessor",cfg["source_um_sha256"]==predecessor["sha256"]and Path(cfg["source_um"]).resolve()==pp.resolve()
 and cfg["predecessor_integration_result"]==ir["predecessor_integration_result"]and cfg["predecessor_build_result"]==ir["predecessor_build_result"])
ck("predecessor_build_PASS",predbuild["status"]=="PASS_TRANSPOSED_SCOPE"and predbuild["input_boundary_unchanged"]and predbuild["cached_boundary_unchanged"]
 and all(r["exit_code"]==0 and r["valid"]and r["warning_lines"]==0 for r in predbuild["runs"]))
canon,cast,cbytes,csentinels=table(op)
old,oast,obytes,osentinels=table(pp)
new,nast,nbytes,nsentinels=table(ip)
_,sast,sbytes,ssentinels=table(sp)
ck("successor_AST_outside_table_identical",oast==nast==sast)
ck("successor_bytes_outside_table_identical",obytes==nbytes==sbytes)
ck("entire_chain_AST_outside_table_identical",cast==oast==nast)
ck("entire_chain_bytes_outside_table_identical",cbytes==obytes==nbytes)
ck("sentinels_exact_entire_chain",csentinels==osentinels==nsentinels==ssentinels)

newmeta=ir["modules"];oldmeta=predir["modules"]
newnames={m["module"]for m in newmeta};oldnames={m["module"]for m in oldmeta}
newkeys={m["key"]for m in newmeta};oldkeys={m["key"]for m in oldmeta}
ck("exact_nine_new_keys",set(new)-set(old)==newkeys and len(newkeys)==9)
ck("exact_72_cumulative_new_keys",set(new)-set(canon)==newkeys|oldkeys and len(newkeys|oldkeys)==72)
ck("no_deletions",set(canon)<=set(old)<=set(new))
ck("successor_old_modifications_only_aggregators",{k for k in old if old[k]!=new[k]}=={"TGLExt.lean","TGL/Audit.lean"})
ck("predecessor_old_modifications_only_aggregators",{k for k in canon if canon[k]!=old[k]}=={"TGLExt.lean","TGL/Audit.lean"})
ck("configuration_module_set",{Path(m["source"]).stem for m in cfg["modules"]}==newnames)
recognized={Path(k).stem for k in old if k.startswith("TGLExt/")and k.endswith(".lean")}
ck("rewriter_recognizes_predecessor_import_targets",set(ir["existing_import_targets_recognized"])==recognized)

newdecls=[];olddecls=[];newtheorems=[];oldtheorems=[];module_rows=[];deps={};instances=[]
TRIO={"propext","Classical.choice","Quot.sound"}
def audit_module(m,stage):
 name=m["module"];rawpath=Path(m["source"]["path"]);actual=remember(rawpath)
 ck(stage+":"+name+":source_pin",same(m["source"]))
 ck(stage+":"+name+":receipt_pin",same(m["build_result"]))
 leaf=readj(m["build_result"]["path"])
 ck(stage+":"+name+":source_in_PASS",leaf["status"]=="PASS_COMPILED_SCOPE"and any(Path(p["path"]).stem==name and p["sha256"]==actual["sha256"]and p["bytes"]==actual["bytes"]for p in leaf["sources"]))
 s=rawpath.read_text(encoding="utf-8").replace("\r\n","\n").replace("\r","\n")
 rewrite=(newnames|recognized)if stage=="new"else oldnames
 changes=[]
 def fix(mt):
  if mt[1]in rewrite:changes.append({"from":mt[1],"to":"TGLExt."+mt[1]});return "import TGLExt."+mt[1]
  return mt[0]
 transposed=re.sub(r"(?m)^import ([\w.]+)$",fix,s)
 ck(stage+":"+name+":exact_import_transposition",new[m["key"]]==transposed)
 ck(stage+":"+name+":transposition_record",m["import_transpositions"]==changes)
 tp=(FOLDER if stage=="new"else predfolder)/"transposed_sources"/m["key"]
 remember(tp);ck(stage+":"+name+":transposed_file",tp.read_bytes()==transposed.encode("utf-8"))
 ds=decls(s);expected=[{"kind":"local instance"if d["kind"]=="instance"and d["local"]else d["kind"],"name":d["name"]}for d in ds]
 ck(stage+":"+name+":declaration_scan",m["declarations"]==expected)
 ds_names={d["name"]for d in ds};rows=[r for r in leaf["axiom_rows"]if r["name"]in ds_names]
 ck(stage+":"+name+":explicit_declarations_audited",Counter(r["name"]for r in rows)==Counter(d["name"]for d in ds))
 ck(stage+":"+name+":axioms_standard",all(set(r["axioms"])<=TRIO for r in rows))
 th=[d["name"]for d in ds if d["kind"]in {"theorem","lemma"}]
 inst=[d["name"]for d in ds if d["kind"]=="instance"and d["local"]]
 instances.extend(inst)
 imports=re.findall(r"(?m)^import ([\w.]+)$",scrub(transposed))
 ck(stage+":"+name+":no_bare_local_import",all(i not in rewrite for i in imports))
 for imp in imports:
  if imp.startswith(("TGLExt.","TGL.")):
   ck(stage+":"+name+":embedded_import:"+imp,imp.replace(".","/")+".lean"in new)
 if stage=="new":deps[name]=[i[7:]for i in imports if i.startswith("TGLExt.")and i[7:]in newnames]
 module_rows.append({"stage":stage,"module":name,"source":actual,"receipt":remember(m["build_result"]["path"]),"transposed":remember(tp),"theorems":len(th),"others":len(expected)-len(th),"local_instances":inst})
 return expected,th
for m in oldmeta:
 ds,th=audit_module(m,"old");olddecls+=ds;oldtheorems+=th
for m in newmeta:
 ds,th=audit_module(m,"new");newdecls+=ds;newtheorems+=th
alldecls=olddecls+newdecls;alltheorems=oldtheorems+newtheorems
ck("new_declaration_name_metadata",Counter(d["name"]for d in newdecls)==Counter(ir["all_declaration_names"]))
ck("new_theorem_name_metadata",newtheorems==ir["theorem_names"])
ck("predecessor_theorem_name_metadata",oldtheorems==predir["theorem_names"])
ck("named_instances_preserved",len(instances)==7 and len(set(instances))==7 and not ir["local_instance_names"]and Counter(instances)==Counter(predir["local_instance_names"]))
dups={n:c for n,c in Counter(d["name"]for d in alldecls).items()if c>1}
ck("no_duplicate_full_names_among_72",not dups,dups)
canonicalnames=defaultdict(list);phase=[]
for k,s in canon.items():
 if not k.endswith(".lean"):continue
 for d in decls(s):canonicalnames[d["name"]].append(k)
collisions={d["name"]:canonicalnames[d["name"]]for d in alldecls if d["name"]in canonicalnames}
ck("no_new_full_names_collide_with_canonical",not collisions,collisions)
for k,s in new.items():
 if k.endswith(".lean"):
  phase.extend({"key":k,"qualified_name":d["name"],"line":d["line"]}for d in decls(s)if d["short"]=="phaseReading")
ck("phaseReading_short_ambiguity_preserved",len(phase)==2)

for label,left,right,names,th in [
 ("successor",old,new,newnames,newtheorems),
 ("predecessor",canon,old,oldnames,oldtheorems),
 ("cumulative",canon,new,newnames|oldnames,alltheorems)]:
 ck(label+":root_additive",right["TGLExt.lean"].startswith(left["TGLExt.lean"]))
 ck(label+":audit_additive",right["TGL/Audit.lean"].startswith(left["TGL/Audit.lean"]))
 rd=right["TGLExt.lean"][len(left["TGLExt.lean"]):];ad=right["TGL/Audit.lean"][len(left["TGL/Audit.lean"]):]
 imports=re.findall(r"(?m)^import ([\w.]+)$",scrub(rd))
 prints=re.findall(r"(?m)^#print axioms ([\w'.]+)$",scrub(ad))
 ck(label+":root_imports_exact",Counter(imports)==Counter("TGLExt."+n for n in names))
 ck(label+":audit_theorems_exact",prints==th)
 ck(label+":root_no_extra_Lean",not re.sub(r"(?m)^import [\w.]+\s*$","",scrub(rd)).strip())
 ck(label+":audit_no_extra_Lean",not re.sub(r"(?m)^#print axioms [\w'.]+\s*$","",scrub(ad)).strip())
order=ir["transposed_module_order"];position={n:i for i,n in enumerate(order)}
ck("new_topological_order",len(order)==9 and set(order)==newnames and all(position[d]<position[n]for n,dd in deps.items()for d in dd))
newcounts={"modules":len(newmeta),"theorems":len(newtheorems),"other_declarations":len(newdecls)-len(newtheorems),"local_instances":0,"total":len(newdecls)}
totals={"modules":len(module_rows),"theorems":len(alltheorems),"other_declarations":len(alldecls)-len(alltheorems),"local_instances":len(instances),"total":len(alldecls)}
ck("new_counts_metadata",newcounts==ir["declaration_counts"])
ck("measured_72_972_264_1236",totals=={"modules":72,"theorems":972,"other_declarations":264,"local_instances":7,"total":1236})
ck("embedded_file_counts",len(canon)==606 and len(old)==669 and len(new)==678)
ck("embedded_lean_counts",sum(k.endswith(".lean")for k in canon)==602 and sum(k.endswith(".lean")for k in old)==665 and sum(k.endswith(".lean")for k in new)==674)
ck("flags_gate_sentinels_code_preserved",cast==oast==nast and cbytes==obytes==nbytes)
ck("new_keys_only_Lean",all(k.endswith(".lean")for k in newkeys))
preparer_folder=BASE/"INTEGRADOR_LOCAL_GERAL_20260909_170426_647362"
for f in ["integrate_approved_copy.py","integrator_changes.diff","prepare_successor.py"]:
 remember(preparer_folder/f)
 if f.endswith(".py"):ast.parse((preparer_folder/f).read_text(encoding="utf-8"))
# Check the prepared dedicated audit only if its preparation receipt already exists.
prep_path=preparer_folder/"RECIBO_PREPARACAO_SUCESSORA.json";prepared=None
if prep_path.exists():
 prep=readj(prep_path);ck("preparation_plan_pin",same(prep["plan"]));plan=readj(prep["plan"]["path"]);build=Path(plan["build"])
 auditpath=build/"NewModulesAudit.lean";audittext=auditpath.read_text(encoding="utf-8");remember(auditpath)
 declared=re.findall(r"(?m)^#print axioms ([\w'.]+)$",scrub(audittext))
 ck("dedicated_audit_all_1236",Counter(declared)==Counter(d["name"]for d in alldecls)and len(declared)==1236)
 ck("dedicated_audit_includes_seven_instances",all(n in declared for n in instances))
 ck("prepared_9_new_plus_3_aggregates",len(plan["runs"])==12 and [r["module"]for r in plan["runs"][:9]]==order)
 ck("prepared_cached_63",len(plan["cached_modules"])==63)
 prepared={"receipt":remember(prep_path),"plan":remember(prep["plan"]["path"]),"counts":plan["counts"],"dedicated_audit":remember(auditpath),"status":prep["status"],"executed_by_this_audit":False}
for path,r in list(inputs.items()):ck("stable:"+path,rec(path)==r)
result={
 "status":"PASS_STATIC_INTEGRATION_SCOPE"if all(c["ok"]for c in checks)else"FAIL_VISIBLE_STATIC_INTEGRATION_SCOPE",
 "created_utc":datetime.now(timezone.utc).isoformat(),
 "counts":{"checks":len(checks),"passed_checks":sum(c["ok"]for c in checks),**totals},
 "delta_counts":newcounts,"integrated":integrated,"snapshot":snapshot,"predecessor":predecessor,"canonical_snapshot":original_snapshot,"current_canonical":rec(op),
 "integration_result":remember(irpath),"predecessor_integration_result":remember(predirpath),"predecessor_build_result":remember(predbuildpath),"approved_configuration":remember(cfgpath),
 "modules":module_rows,"checks":checks,"failed_checks":[c for c in checks if not c["ok"]],
 "embedded_counts":{"canonical":len(canon),"predecessor":len(old),"successor":len(new),"canonical_lean":sum(k.endswith(".lean")for k in canon),"predecessor_lean":sum(k.endswith(".lean")for k in old),"successor_lean":sum(k.endswith(".lean")for k in new)},
 "name_collisions":{"among_72":dups,"with_canonical":collisions},"phaseReading_diagnostic":{"status":"AMBIGUOUS_SHORT_NAME_PRESERVED","matches":phase},
 "prepared_successor":prepared,
 "scope":{"um_py_executed_or_imported":False,"integrator_executed_by_auditor":False,"build_executed_by_auditor":False,"new_individual_flags":False,"outside_table_AST_and_bytes_preserved":cast==oast==nast and cbytes==obytes==nbytes,
 "TGL_Audit_delta":"116 new theorem prints; cumulative new theorem prints 972","dedicated_audit_policy":"1236 cumulative declarations, including seven named local instances; build result separate"},
 "limits":["Static integration scope, not runtime seal or physics conclusion.","Explicit Lean declaration scan includes named local instances, but excludes generated declarations and a whole-Mathlib name scan.","Leaf PASS receipts refer to frozen sources before exact import transposition; successor combined compilation is a separate obligation.","The predecessor build has scoped cache provenance and does not claim all external transitive dependencies were rehashed or rebuilt."],
 "inputs":[r for r in inputs.values()]}
output=savej("AUDITORIA_INTEGRACAO_72.json",result)
note="# Auditoria estática independente da sucessora72\n\n"+result["status"]+"\n\n"
note+=f'Medidos {totals["modules"]} módulos, {totals["theorems"]} teoremas e {totals["other_declarations"]} outras declarações, total {totals["total"]}, incluindo sete instâncias locais nomeadas. Delta da predecessora: nove módulos, 116 teoremas e 22 outras declarações.\n\n'
note+='A cadeia canônico → predecessora63 → sucessora72 foi conferida por AST e bytes. Só a tabela embutida mudou: nove entradas novas e acréscimos nos imports de TGLExt.lean e nas auditorias de TGL/Audit.lean. Nenhum código, bandeira, sentinela ou gate fora da tabela foi alterado. O snapshot da sucessora é cópia byte a byte da predecessora; o snapshot da predecessora coincide com o canônico atual.\n\n'
note+='Foram conferidos pins e fontes dos 72 módulos, recibos individuais, transposição exata dos imports, nomes completos e instâncias. Nenhuma colisão de nome completo foi encontrada no escopo de declarações explícitas. A ambiguidade curta phaseReading permanece, em namespaces diferentes. Contagem de arquivos embutidos: 606 → 669 → 678; arquivos Lean: 602 → 665 → 674.\n\n'
note+='O integrador sucessor e prepare_successor.py foram lidos sem execução pelo auditor. A reescrita de imports reconhece os alvos da predecessora; a preparação amarra os 63 módulos ao PASS anterior e seu ancestral por pins, copia arquivos somente para pasta nova e separa os hashes históricos dos medidos no reuso. A compilação incremental da sucessora é responsabilidade da raiz e seu resultado não é presumido por esta auditoria.\n\n'
note+=("O plano de preparação já existente foi lido: 63 módulos em cache, nove folhas novas e três agregadores; NewModulesAudit contém exatamente as 1236 declarações, incluindo as sete instâncias.\n\n"if prepared else"O plano de preparação ainda não existia durante esta leitura; a política de auditoria dedicada de 1236 declarações permanece obrigação da compilação separada.\n\n")
note+=f'Verificações: {result["counts"]["passed_checks"]}/{result["counts"]["checks"]}. Detalhes e hashes lidos: [recibo]({OUT.as_posix()}/AUDITORIA_INTEGRACAO_72.json).\n\n'
note+='Nenhum um.py foi executado/importado. Nenhum original ou fonte congelada foi alterado. Não é selo de runtime, afirmação de física, nem compilação nova feita pelo auditor.\n'
nr=save("RELATORIO_INTEGRACAO_72.md",note)
mr=savej("MANIFESTO_AUDITORIA_72.json",{"status":result["status"],"artifacts":[output,nr],"script":rec(Path(__file__))})
print(json.dumps({"status":result["status"],"counts":result["counts"],"delta":newcounts,"failed_checks":result["failed_checks"],"prepared":prepared,"outputs":[output,nr,mr]},ensure_ascii=False,indent=2))
