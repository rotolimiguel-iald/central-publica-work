"""Integrate approved Lean texts into a NEW um.py copy, without running/importing either program."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,os,re,sys,tokenize,io,copy
BASE=Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
def digest(raw):return hashlib.sha256(raw).hexdigest()
def record(p):
    b=p.read_bytes();return {"path":p.as_posix(),"bytes":len(b),"sha256":digest(b)}
def normalize(text):return text.replace("\r\n","\n").replace("\r","\n")
def new_file(p,b):
    assert p.resolve().is_relative_to(BASE) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_name(p.name+".tmp")
    with t.open("xb") as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b
    os.rename(t,p);assert p.read_bytes()==b
def find_table(tree):
    found=[n for n in tree.body if isinstance(n,ast.Assign) and
        any(isinstance(t,ast.Name) and t.id=="_EMBEDDED_KERNEL_FILES" for t in n.targets)]
    assert len(found)==1 and isinstance(found[0].value,ast.Dict)
    n=found[0];pairs=list(zip(n.value.keys,n.value.values))
    keys=[ast.literal_eval(k) for k,v in pairs]
    assert len(keys)==len(set(keys)) and all(isinstance(k,str) for k in keys)
    values={k:ast.literal_eval(v) for k,(_,v) in zip(keys,pairs)}
    assert all(isinstance(v,str) for v in values.values())
    return n,values,{k:v for k,(_,v) in zip(keys,pairs)}
def literal(text):
    for q in ["'"*3,chr(34)*3]:
        if q not in text and not text.endswith("\\"):
            return ("r"+q+text+q).encode("utf-8")
    return repr(text).encode("utf-8")
def offset(node,lines,end=False):
    line=node.end_lineno if end else node.lineno
    col=node.end_col_offset if end else node.col_offset
    return sum(map(len,lines[:line-1]))+col

def lean_declarations(text):
    """Read the reviewed one-namespace source convention, including named local instances."""
    pattern=re.compile(r"(?m)^(?:noncomputable[ \t]+)?"
        r"(abbrev|def|structure|theorem|local[ \t]+instance)[ \t]+"
        r"([^\W\d]\w*'*)(?=[ \t\r\n:({\[])")
    declarations=[(re.sub(r"[ \t]+"," ",m.group(1)),m.group(2))
                  for m in pattern.finditer(text)]
    names=[name for _,name in declarations]
    assert len(names)==len(set(names)), "Duplicate declaration names"
    # Reject anonymous/scoped/other instance syntax instead of silently omitting it.
    instance_headers=re.findall(r"(?m)^[ \t]*(?:(?:local|scoped|noncomputable|"
        r"private|protected)[ \t]+)*instance\b[^\r\n]*",text)
    local_instances=[name for kind,name in declarations if kind=="local instance"]
    assert len(instance_headers)==len(local_instances), (
        "Every instance must be a named top-level 'local instance NAME'; explicit review required")
    prints=re.findall(r"(?m)^#print axioms ([\w.']+)[ \t]*$",text)
    assert len(prints)==len(set(prints)) and set(prints)==set(names), (
        "Every declaration, including each local instance, requires exactly one #print axioms")
    return declarations

def main():
    assert len(sys.argv)==2, "Pass an approved frozen configuration JSON."
    cfgpath=Path(sys.argv[1]).resolve()
    cfg=json.loads(cfgpath.read_text(encoding="utf-8"))
    assert cfg["root_confirmed"] is True, "Module snapshot must be confirmed before generation."
    source=Path(cfg["source_um"]).resolve();raw=source.read_bytes()
    assert digest(raw)==cfg["source_um_sha256"], "um.py changed; freeze a new snapshot."
    text=raw.decode("utf-8");tree=ast.parse(text);node,embedded,value_nodes=find_table(tree)
    modules=[];all_names=set();newkeys=set();namespaces=set()
    for item in cfg["modules"]:
        p=Path(item["source"]).resolve();b=p.read_bytes()
        assert digest(b)==item["sha256"], "Approved module changed: "+str(p)
        br=Path(item["build_result"]).resolve()
        assert digest(br.read_bytes())==item["build_result_sha256"]
        proof=json.loads(br.read_text(encoding="utf-8"))
        assert proof["status"]=="PASS_COMPILED_SCOPE"
        assert any(x["sha256"]==digest(b) for x in proof["sources"])
        s=normalize(b.decode("utf-8"));module=p.stem
        assert re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*",module)
        key="TGLExt/"+module+".lean"
        assert key not in embedded and key not in newkeys,"Module key collision"
        newkeys.add(key)
        ns=re.findall(r"(?m)^namespace ([\w.]+)\s*$",s)
        assert len(ns)==1,"Namespace nesting needs explicit review"
        assert ns[0] not in namespaces,"Shared namespace needs explicit collision review"
        namespaces.add(ns[0])
        for oldcontent in embedded.values():
            assert not re.search(r"(?m)^namespace "+re.escape(ns[0])+r"\s*$",oldcontent),"Existing namespace collision"
        decls=lean_declarations(s)
        assert not re.search(r"\b(?:sorry|admit|native_decide|unsafe|axiom)\b",s)
        full=[{"kind":kind,"name":ns[0]+"."+name} for kind,name in decls]
        assert not ({d["name"] for d in full}&all_names)
        all_names.update(d["name"] for d in full)
        modules.append({"module":module,"key":key,"namespace":ns[0],"source":record(p),
                        "text":s,"declarations":full,"build_result":record(br)})
    all_declaration_names=[d["name"] for m in modules for d in m["declarations"]]
    local_instance_names=[d["name"] for m in modules for d in m["declarations"]
                          if d["kind"]=="local instance"]
    theorem_count=sum(d["kind"]=="theorem" for m in modules for d in m["declarations"])
    declaration_counts={"modules":len(modules),"theorems":theorem_count,
        "other_declarations":len(all_declaration_names)-theorem_count,
        "local_instances":len(local_instance_names),"total":len(all_declaration_names)}
    for key,value in cfg.get("measured_counts",{}).get("total",{}).items():
        assert key in declaration_counts and declaration_counts[key]==value, (
            "Configuration count mismatch: "+key)
    local_names={m["module"] for m in modules}
    existing_local_names={Path(key).stem for key in embedded
                          if key.startswith("TGLExt/") and key.endswith(".lean")}
    rewrite_names=local_names | existing_local_names
    replacements=[];dependencies={}
    for m in modules:
        original=m["text"];changes=[]
        def fix(match):
            name=match.group(1)
            if name in rewrite_names:
                changes.append({"from":name,"to":"TGLExt."+name})
                return "import TGLExt."+name
            return match.group(0)
        m["text"]=re.sub(r"(?m)^import ([\w.]+)$",fix,original)
        m["import_transpositions"]=changes
        dependencies[m["module"]]=[n.split(".")[-1] for n in re.findall(
            r"(?m)^import (TGLExt\.[\w.]+)$",m["text"]) if n.split(".")[-1] in local_names]
    ordered=[]
    while len(ordered)<len(modules):
        available=[m for m in modules if m["module"] not in ordered and
                   set(dependencies[m["module"]])<=set(ordered)]
        assert available,"Local import cycle"
        ordered.extend(m["module"] for m in available)
    modules=sorted(modules,key=lambda m:ordered.index(m["module"]))
    root=embedded["TGLExt.lean"]
    audit=embedded["TGL/Audit.lean"]
    root_add="\n-- New reviewed Chatgpt working-copy modules; no gate changes.\n"
    audit_add="\n-- New reviewed Chatgpt working-copy theorem audit; no new flags.\n"
    theorem_names=[]
    for m in modules:
        line="import TGLExt."+m["module"]
        assert not re.search(r"(?m)^"+re.escape(line)+r"\s*$",root)
        root_add+=line+"\n"
        for d in m["declarations"]:
            if d["kind"]=="theorem":
                name=d["name"];theorem_names.append(name)
                assert not re.search(r"(?m)^#print axioms "+re.escape(name)+r"\s*$",audit)
                audit_add+="#print axioms "+name+"\n"
    root_new=root+root_add;audit_new=audit+audit_add
    lines=raw.splitlines(keepends=True)
    for key,value in [("TGLExt.lean",root_new),("TGL/Audit.lean",audit_new)]:
        old_node=value_nodes[key]
        replacements.append((offset(old_node,lines),offset(old_node,lines,True),literal(value)))
    end=offset(node.value,lines,True);assert raw[end-1:end]==b"}"
    last=value_nodes[list(embedded)[-1]]
    tail=raw[offset(last,lines,True):end-1].decode("utf-8")
    stripped=re.sub(r"(?m)#.*$","",tail).strip()
    assert stripped in ("",",")
    addition=(b",\n" if stripped=="" else b"\n")
    for m in modules:
        addition+=("    "+repr(m["key"])+":\n").encode()+literal(m["text"])+b",\n"
    replacements.append((end-1,end-1,addition))
    output=raw
    for start,stop,data in sorted(replacements,reverse=True):
        assert offset(node.value,lines)<=start<=stop<=end
        output=output[:start]+data+output[stop:]
    newtree=ast.parse(output.decode("utf-8"));newnode,newembedded,_=find_table(newtree)
    assert [ast.dump(n,include_attributes=False) for n in tree.body if n is not node]==[
        ast.dump(n,include_attributes=False) for n in newtree.body if n is not newnode]
    assert output[:offset(node.value,lines)]==raw[:offset(node.value,lines)]
    assert output.endswith(raw[end:])
    assert set(newembedded)==set(embedded)|newkeys
    for key,value in embedded.items():
        expected=root_new if key=="TGLExt.lean" else audit_new if key=="TGL/Audit.lean" else value
        assert newembedded[key]==expected,"Changed old embedded source: "+key
    for m in modules:assert newembedded[m["key"]]==m["text"]
    folder=BASE/("COPIA_INTEGRADA_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    folder.mkdir(exist_ok=False)
    original_copy=folder/"um_ORIGINAL_SNAPSHOT.py"
    new_file(original_copy,raw);new_file(folder/"um.py",output)
    new_file(folder/"CONFIG_APROVADA.json",cfgpath.read_bytes())
    for m in modules:new_file(folder/"transposed_sources"/m["key"],m["text"].encode("utf-8"))
    summary={
        "status":"AST_AND_EMBEDDED_ROUND_TRIP_PASSED__NOT_EXECUTED",
        "created_utc":datetime.now(timezone.utc).isoformat(),"source_um":record(source),
        "original_copy":record(original_copy),"integrated_copy":record(folder/"um.py"),
        "source_um_executed":False,"integrated_copy_executed":False,"canonical_changes":False,
        "outside_embedded_table_ast_identical":True,"outside_embedded_table_bytes_unchanged":True,
        "existing_sources_unchanged_except_root_and_audit":True,
        "sentinels_flags_and_gate_code_unchanged":True,"new_individual_json_flags_added":False,
        "modules":[{k:v for k,v in m.items() if k!="text"} for m in modules],
        "integration_basis":"The frozen predecessor um.py copy; source_um is this explicit predecessor.",
        "predecessor_integration_result":cfg.get("predecessor_integration_result"),
        "predecessor_build_result":cfg.get("predecessor_build_result"),
        "existing_import_targets_recognized":sorted(existing_local_names),
        "theorem_names":theorem_names,"transposed_module_order":ordered,
        "all_declaration_names":all_declaration_names,
        "local_instance_names":local_instance_names,"declaration_counts":declaration_counts,
        "audit_policy":{"TGL/Audit.lean":"new theorems only",
            "leaf_prints":"all declarations, including named local instances",
            "NewModulesAudit.lean":"all declarations, including named local instances"},
        "new_embedded_file_count":len(modules),"old_embedded_file_count":len(embedded),
        "new_total_embedded_file_count":len(newembedded),
        "scope_note":"A static working copy only. No execution of um.py, no seal and no physical confirmation. New theorems have Audit entries but no individual JSON flags were added."}
    assert source.read_bytes()==raw
    for m in modules:assert record(Path(m["source"]["path"]))==m["source"]
    new_file(folder/"INTEGRATION_RESULT.json",(json.dumps(summary,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    print(json.dumps({"folder":folder.as_posix(),"status":summary["status"],
                      "modules":len(modules),"theorems":len(theorem_names),
                      "declarations":len(all_declaration_names),
                      "local_instances":len(local_instance_names)},ensure_ascii=False))
if __name__=="__main__":main()
