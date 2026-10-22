from pathlib import Path
from datetime import datetime,timezone
from collections import Counter,defaultdict
import ast,copy,hashlib,json,re,os,sys
sys.stdout.reconfigure(encoding="utf-8")
HERE=Path(__file__).resolve().parent
TARGET=HERE.parent
BASE=Path("C:/IALD/Central de Patentes/Chatgpt").resolve()
assert HERE.is_relative_to(BASE)
checks=[]
def mark(name,condition,detail=None):
    checks.append({"check":name,"pass":bool(condition),"detail":detail})
def rec(p):
    raw=p.read_bytes()
    return {"path":p.as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
def new(p,data):
    assert p.resolve().is_relative_to(TARGET) and not p.exists(),p
    t=p.with_name(p.name+".tmp_new")
    with open(t,"xb") as f:f.write(data);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==data
    os.rename(t,p)
def norm(s):return s.replace("\r\n","\n").replace("\r","\n")
def table(raw):
    tree=ast.parse(raw.decode("utf-8"))
    candidates=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="_EMBEDDED_KERNEL_FILES" for t in n.targets)]
    assert len(candidates)==1
    node=candidates[0]
    assert isinstance(node.value,ast.Dict)
    keys=[ast.literal_eval(k) for k in node.value.keys]
    mark("unique_dictionary_keys",len(keys)==len(set(keys)),len(keys))
    values=[ast.literal_eval(v) for v in node.value.values]
    assert all(isinstance(k,str) for k in keys) and all(isinstance(v,str) for v in values)
    rows=raw.splitlines(keepends=True)
    start=sum(len(x) for x in rows[:node.value.lineno-1])+node.value.col_offset
    stop=sum(len(x) for x in rows[:node.value.end_lineno-1])+node.value.end_col_offset
    return tree,node,dict(zip(keys,values)),start,stop
def lean_clean(s):
    out=[];i=0;depth=0;string=False
    while i<len(s):
        c=s[i];pair=s[i:i+2]
        if depth:
            if pair=="/-":depth+=1;out.extend("  ");i+=2;continue
            if pair=="-/":depth-=1;out.extend("  ");i+=2;continue
            out.append("\n" if c=="\n" else " ");i+=1;continue
        if string:
            if c=="\\" and i+1<len(s):out.extend("  ");i+=2;continue
            if c=='"':string=False
            out.append("\n" if c=="\n" else " ");i+=1;continue
        if pair=="/-":depth=1;out.extend("  ");i+=2;continue
        if pair=="--":
            while i<len(s) and s[i]!="\n":out.append(" ");i+=1
            continue
        if c=='"':string=True;out.append(" ");i+=1;continue
        out.append(c);i+=1
    return "".join(out)
def declarations(text,path):
    stack=[];ns=[];out=[]
    cleaned=lean_clean(text)
    for no,line in enumerate(cleaned.splitlines(),1):
        l=line.strip()
        n=re.fullmatch(r"namespace\s+([\w.']+)",l)
        if n:stack.append(("namespace",list(ns)));ns+=n.group(1).split(".");continue
        if re.fullmatch(r"(?:noncomputable\s+)?section(?:\s+\S+)?",l) or l=="mutual":
            stack.append(("section",list(ns)));continue
        if re.fullmatch(r"end(?:\s+\S+)?",l):
            if stack:kind,previous=stack.pop();ns=previous
            continue
        d=re.match(r"(?:(?:private|protected|noncomputable)\s+)*(abbrev|def|structure|theorem|lemma|class|inductive|opaque|axiom)\s+([\w.']+)",l)
        if d:
            short=d.group(2)
            fullname=short[len("_root_."):] if short.startswith("_root_.") else ".".join(ns+[short])
            out.append({"kind":d.group(1),"name":fullname,"short":short.split(".")[-1],"line":no,"source":path})
    return out
result=json.loads((TARGET/"INTEGRATION_RESULT.json").read_text(encoding="utf-8"))
cfg=json.loads((TARGET/"CONFIG_APROVADA.json").read_text(encoding="utf-8"))
before_records=[rec(TARGET/"um.py"),rec(TARGET/"um_ORIGINAL_SNAPSHOT.py"),rec(TARGET/"CONFIG_APROVADA.json"),rec(TARGET/"INTEGRATION_RESULT.json")]
oldraw=(TARGET/"um_ORIGINAL_SNAPSHOT.py").read_bytes()
newraw=(TARGET/"um.py").read_bytes()
ot,on,old,oa,oz=table(oldraw)
nt,nn,newtable,na,nz=table(newraw)
mark("prefix_bytes_identical",oldraw[:oa]==newraw[:na])
mark("suffix_bytes_identical",oldraw[oz:]==newraw[nz:])
ot2=copy.deepcopy(ot);nt2=copy.deepcopy(nt)
for tree in [ot2,nt2]:
    for node in tree.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="_EMBEDDED_KERNEL_FILES" for t in node.targets):
            node.value=ast.Constant(value="<REMOVED_EMBEDDED_VALUE>")
mark("whole_ast_identical_except_table_value",ast.dump(ot2,include_attributes=False)==ast.dump(nt2,include_attributes=False))
mark("snapshot_hash_matches_approved_source",hashlib.sha256(oldraw).hexdigest()==cfg["source_um_sha256"])
mark("integrated_hash_matches_receipt",rec(TARGET/"um.py")==result["integrated_copy"])
mark("snapshot_hash_matches_receipt",rec(TARGET/"um_ORIGINAL_SNAPSHOT.py")==result["original_copy"])
live=Path(cfg["source_um"])
live_record=rec(live)
mark("live_original_matches_snapshot",live.read_bytes()==oldraw,live_record)
entries=cfg["modules"]
stems=[Path(e["source"]).stem for e in entries]
mark("unique_module_names",len(stems)==len(set(stems)))
keys={"TGLExt/"+stem+".lean" for stem in stems}
mark("exact_new_key_set",set(newtable)-set(old)==keys)
mark("no_old_key_removed",set(old)<=set(newtable))
changed=[k for k in old if k in newtable and old[k]!=newtable[k]]
mark("only_old_aggregators_changed",set(changed)=={"TGLExt.lean","TGL/Audit.lean"},changed)
for key in ["TGLExt.lean","TGL/Audit.lean"]:
    mark("append_only_"+key,newtable[key].startswith(old[key]))
all_new=[];module_rows=[]
for entry in entries:
    source=Path(entry["source"]);raw=source.read_bytes()
    text=norm(raw.decode("utf-8"));key="TGLExt/"+source.stem+".lean"
    mark("source_hash_"+source.stem,hashlib.sha256(raw).hexdigest()==entry["sha256"])
    receipt=Path(entry["build_result"]);proof=json.loads(receipt.read_text(encoding="utf-8"))
    mark("receipt_hash_"+source.stem,rec(receipt)["sha256"]==entry["build_result_sha256"])
    mark("prior_pass_"+source.stem,proof["status"]=="PASS_COMPILED_SCOPE" and any(x["sha256"]==hashlib.sha256(raw).hexdigest() for x in proof["sources"]))
    transposed=re.sub(r"(?m)^import ([\w.]+)$",lambda m:"import TGLExt."+m.group(1) if m.group(1) in set(stems) else m.group(0),text)
    mark("embedded_transposition_"+source.stem,newtable[key]==transposed)
    mark("disk_transposition_"+source.stem,(TARGET/"transposed_sources"/key).read_bytes()==transposed.encode("utf-8"))
    decl=declarations(text,source.as_posix());all_new+=decl
    shortprints=re.findall(r"(?m)^#print axioms ([\w.']+)\s*$",text)
    mark("source_axiom_prints_"+source.stem,Counter(shortprints)==Counter(d["short"] for d in decl))
    mark("root_import_"+source.stem,len(re.findall(r"(?m)^import TGLExt\."+re.escape(source.stem)+r"\s*$",newtable["TGLExt.lean"]))==1)
    summary=next(m for m in result["modules"] if m["module"]==source.stem)
    mark("receipt_declarations_"+source.stem,Counter((d["kind"],d["name"]) for d in decl)==Counter((d["kind"],d["name"]) for d in summary["declarations"]))
    module_rows.append({"module":source.stem,"source":rec(source),"theorems":sum(d["kind"]=="theorem" for d in decl),"others":sum(d["kind"]!="theorem" for d in decl),"declarations":decl,"import_transpositions":[m.group(1) for m in re.finditer(r"(?m)^import ([\w.]+)$",text) if m.group(1) in set(stems)]})
new_theorems=[d["name"] for d in all_new if d["kind"]=="theorem"]
mark("unique_new_declarations",len(all_new)==len({d["name"] for d in all_new}))
mark("theorem_list_matches_sources",Counter(new_theorems)==Counter(result["theorem_names"]))
oldprints=re.findall(r"(?m)^#print axioms ([\w.']+)\s*$",old["TGL/Audit.lean"])
newprints=re.findall(r"(?m)^#print axioms ([\w.']+)\s*$",newtable["TGL/Audit.lean"])
mark("exact_audit_additions",Counter(newprints)-Counter(oldprints)==Counter(new_theorems) and not(Counter(oldprints)-Counter(newprints)))
mark("each_new_theorem_audited_once",all(newprints.count(t)==1 for t in new_theorems))
old_decls=[]
for key,text in old.items():
    if key.endswith(".lean"):old_decls+=declarations(text,key)
byfull=defaultdict(list);byshort=defaultdict(list)
for d in old_decls+all_new:
    byfull[d["name"]].append(d)
    byshort[d["short"]].append(d)
newfull={d["name"] for d in all_new};newshort={d["short"] for d in all_new}
full_collisions={n:rows for n,rows in byfull.items() if n in newfull and len(rows)>1}
short_collisions={n:rows for n,rows in byshort.items() if n in newshort and len({d["name"] for d in rows})>1}
mark("no_full_name_collisions",not full_collisions,full_collisions)
predecessors={}
for field in ["predecessor_six_module_copy","predecessor_seven_module_copy","predecessor_fourteen_module_copy"]:
    if field in cfg:
        p=Path(cfg[field]);r=rec(p)
        older_result=p.parent/"INTEGRATION_RESULT.json"
        if older_result.exists():
            oldresult=json.loads(older_result.read_text(encoding="utf-8"))
            mark("preserved_"+field,r==oldresult["integrated_copy"])
        predecessors[field]=r
generic=cfg.get("predecessor_copy_sha256")
errata={"status":"HISTORICAL_METADATA_ERRATUM_NO_CODE_CHANGE","created_utc":datetime.now(timezone.utc).isoformat(),"configuration":rec(TARGET/"CONFIG_APROVADA.json"),"inherited_generic_hash":generic,"measured_predecessors":predecessors,"generic_hash_matches":[k for k,v in predecessors.items() if v["sha256"]==generic],"effective_predecessor_field":"predecessor_fourteen_module_copy","explanation_pt":"O hash genérico herdado corresponde à cópia7, não à cópia6 cujo caminho também foi herdado. O predecessor efetivo deste lote é a cópia14, com campo próprio. Esses campos de linhagem não são lidos pelo integrador; source_um tem validação independente por hash. Nenhum arquivo congelado foi corrigido retroativamente."}
mark("inputs_unchanged_during_independent_audit",before_records==[rec(TARGET/"um.py"),rec(TARGET/"um_ORIGINAL_SNAPSHOT.py"),rec(TARGET/"CONFIG_APROVADA.json"),rec(TARGET/"INTEGRATION_RESULT.json")])
report={"status":"PASS_INDEPENDENT_STATIC_AUDIT" if all(c["pass"] for c in checks) else "FAIL_INDEPENDENT_STATIC_AUDIT","created_utc":datetime.now(timezone.utc).isoformat(),"target":TARGET.as_posix(),"scope":{"um_py_executed_or_imported":False,"lean_recompiled":False,"runtime_verified":False,"build_in_progress_files_changed":False,"ast_and_literal_read_only":True},"checks":checks,"counts":{"modules":len(entries),"theorems":len(new_theorems),"others":len(all_new)-len(new_theorems),"declarations":len(all_new),"old_embedded":len(old),"new_embedded":len(newtable),"new_axiom_prints":len(newprints)-len(oldprints)},"snapshot":rec(TARGET/"um_ORIGINAL_SNAPSHOT.py"),"integrated_copy":rec(TARGET/"um.py"),"live_original":live_record,"module_rows":module_rows,"full_name_collisions":full_collisions,"short_name_collisions":short_collisions,"lineage_erratum":errata}
new(HERE/"AUDITORIA_INDEPENDENTE.json",(json.dumps(report,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
new(TARGET/"ERRATA_DE_LINHAGEM.json",(json.dumps(errata,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
counts=report["counts"]
lines=["# Auditoria independente da integração — 09/09/2026","",
"[REAL] "+report["status"]+". Leitura AST/literal e comparação independente; nenhum um.py executado/importado, nenhuma recompilação Lean paralela.","",
f"[REAL] {counts['modules']} módulos, {counts['theorems']} teoremas + {counts['others']} outras declarações = {counts['declarations']} termos. Tabela embutida: {counts['old_embedded']} → {counts['new_embedded']} arquivos.","",
"[REAL] Prefixo e sufixo de bytes em torno do valor da tabela preservados. AST completo idêntico após substituir somente o valor da tabela. Isso inclui alvos da atribuição, núcleo Python, flags, gate e sentinelas. As entradas antigas mudaram apenas em TGLExt.lean e TGL/Audit.lean, por adição.","",
"[REAL] Fontes e recibos foram relidos, seus hashes conferidos e cada string embutida comparada com a transposição mecânica independente dos imports. O Audit acrescenta exatamente um print para cada novo teorema, sem retirar prints antigos.","",
f"[REAL] Colisões por nome completo envolvendo declarações novas: {len(full_collisions)}. Colisões de nome curto: {len(short_collisions)}; os nomes completos distinguem seus referentes. Elas afetam consultas por nome curto e não são automaticamente conflitos Lean.",""]
for name,rows in sorted(short_collisions.items()):
    lines.append("- "+name+": "+"; ".join(sorted({d["name"] for d in rows})))
lines+=["","[REAL — errata histórica] ERRATA_DE_LINHAGEM.json registra os bytes/hash lidos das cópias6,7,14. O campo genérico herdado associa o hash da cópia7 ao conjunto de metadados que também inclui o caminho da cópia6. O predecessor efetivo deste lote é a cópia14. Os campos herdados não são usados no mecanismo de geração. CONFIG_APROVADA.json, INTEGRATION_RESULT.json e arquivos do build em curso permaneceram intactos.","","[OPEN — escopo] Esta auditoria não atesta execução do programa, confirmação física nem recompilação canônica integral. A compilação transposta fica registrada separadamente pela tarefa principal.","","SHA-256 da cópia, lido: "+report["integrated_copy"]["sha256"]]
failed=[c for c in checks if not c["pass"]]
if failed:lines+=["","[FAIL] Verificações que falharam:",json.dumps(failed,ensure_ascii=False,indent=2)]
new(HERE/"RELATORIO_INDEPENDENTE.md",("\n".join(lines)+"\n").encode("utf-8"))
print(json.dumps({"status":report["status"],"counts":counts,"failed_checks":failed,"full_collisions":len(full_collisions),"short_collisions":{k:sorted({d["name"] for d in v}) for k,v in short_collisions.items()},"audit_folder":HERE.as_posix(),"integrated_hash":report["integrated_copy"]["sha256"],"lineage_hash_matches":errata["generic_hash_matches"]},ensure_ascii=False))
