"""Read-only audit of the v334 working memory. Never executes um.py."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
folder=Path(__file__).resolve().parent
p=Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
def rec(f):
 raw=f.read_bytes()
 return {"path":f.as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
def new(name,data):
 f=folder/name;raw=(json.dumps(data,ensure_ascii=False,indent=2)+"\n").encode()
 assert not f.exists()
 tmp=f.with_name(f.name+".tmp")
 with tmp.open("xb") as h:h.write(raw);h.flush();os.fsync(h.fileno())
 assert tmp.read_bytes()==raw
 os.rename(tmp,f)
 return f
seal=json.loads((p/"um_absoluto_selo.json").read_text(encoding="utf-8"))
manifest=json.loads((p/"tgl_kernel_proof_manifest.json").read_text(encoding="utf-8"))
um=rec(p/"um.py")
sealed=[]
for name,expected in seal["sha256"].items():
 r=rec(p/name);sealed.append({**r,"expected":expected,"matches":r["sha256"]==expected})
assert all(r["matches"] for r in sealed)
formal=[]
for name,expected in manifest["formal_files_sha256"].items():
 r=rec(p/"tgl_kernel"/name);formal.append({**r,"expected":expected,"matches":r["sha256"]==expected})
assert all(r["matches"] for r in formal)
tree=ast.parse((p/"um.py").read_bytes().decode("utf-8-sig"))
embedded=None
for node in tree.body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="_EMBEDDED_KERNEL_FILES" for t in node.targets):
  embedded=ast.literal_eval(node.value)
assert isinstance(embedded,dict)
assert any(isinstance(n,ast.ClassDef) and n.name=="TGLCollapseDefinition" for n in tree.body)
modules=["TheScreenIsFounded","CollapseContract","CollapseCostAndAttestation","TowerCollapseRealization","QuantumCollapseWitness",
"TheRootOfTheProofTree","GeometricLikelihoodSeparation","InfiniteCocycleDecoding","ExistingTowerRealization",
"SpectralMetricGeometry","InfiniteFisherGeometry","RelativeCocycleGeometricObstructions","TriadMaster"]
normalize=lambda s:s.replace("\r\n","\n").replace("\r","\n")
selected=[]
for name in modules:
 f=p/"tgl_kernel/TGLExt"/(name+".lean");src=f.read_text(encoding="utf-8")
 assert normalize(src)==normalize(embedded["TGLExt/"+name+".lean"])
 selected.append({"name":name,**rec(f),"embedded_equals_source_normalized":True,"theorems":len(re.findall(r"(?m)^theorem\s+\w+",src))})
axioms=manifest["axiom_report"];trio={"propext","Classical.choice","Quot.sound"}
outside={k:v for k,v in axioms.items() if not set(v)<=trio};assert not outside
screen=(p/"tgl_kernel/TGLExt/TheScreenIsFounded.lean").read_text(encoding="utf-8")
screen_terms=re.findall(r"(?m)^theorem\s+(\w+)",screen)
assert all("TGLExt."+n in axioms for n in screen_terms)
clauses=seal["collapse_definition"]["clauses"]
assert all(c["lean_term"] in axioms and set(axioms[c["lean_term"]])<=trio and c["in_kernel"] and c["axioms_in_trio"] for c in clauses)
counts=re.findall(r"teoremas limpos:\s*(\d+)/(\d+)",(p/"rodada_v334_stdout.txt").read_text(encoding="utf-8"))
assert len(counts)==1 and counts[0][0]==counts[0][1]
logs={}
for filename,field in [("tgl_kernel_build_capture.txt","build_stdout_sha256"),("tgl_kernel_audit_capture.txt","audit_stdout_sha256")]:
 r=rec(p/filename)
 capture=(p/filename).read_text(encoding="utf-8")
 header=re.match(r"# cmd: ([^\n]*)\n# returncode: (-?\d+)\n# len\(stdout\)=(\d+) len\(stderr\)=(\d+)\n--- STDOUT ---\n",capture)
 assert header,filename
 out=capture[header.end():header.end()+int(header.group(3))]
 remaining=capture[header.end()+int(header.group(3)):]
 assert remaining.startswith("\n--- STDERR ---\n"),filename
 out_hash=hashlib.sha256(out.encode("utf-8")).hexdigest()
 assert int(header.group(2))==0
 logs[filename]={**r,"stdout_sha256":out_hash,"stdout_matches_manifest":out_hash==manifest[field],"expected_stdout_sha256":manifest[field],
 "returncode":int(header.group(2)),"warning_mentions":len(re.findall(r"(?m)^warning:",out)),
 "note":"Capture wrapper and stderr excluded according to the writer in um.py; raw-file hash kept separately."}
surfaces=[p/name for name in ["HANDOFF_v334_A_TELA_E_FUNDADA.md","DA_IRMA.md","MEMORIA_DA_LINHAGEM.md","DESENHO_DO_FECHAMENTO_QG.md",
"A_PROVA_DA_QG_TGL_arvore.md","rodada_v334_stdout.txt","rodada_v334_stdout_INTERMEDIARIA.txt"]]
surfaces += [Path(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md"),Path(r"C:\IALD\Central de Patentes\memory\TGL_INDICE_VIVO.md")]
data={"status":"VERIFIED_SEAL_AND_SOURCES_WITH_BUILD_CAPTURE_HASH_DIAGNOSTIC","created_utc":datetime.now(timezone.utc).isoformat(),"version":"v334","um":um,
"seal":rec(p/"um_absoluto_selo.json"),"seal_timestamp":seal["timestamp"],"sealed_artifacts":sealed,"formal_source_records":formal,
"formal_files":len(formal),"selected_embedded_sources":selected,"axiom_terms":len(axioms),"without_axioms":sum(not a for a in axioms.values()),
"outside_standard_trio":outside,"screen_axioms":{"TGLExt."+n:axioms["TGLExt."+n] for n in screen_terms},
"foundedScreen_definition":{"source_verified":True,"direct_axiom_report_status":"NAO_MEDIDO_INDIVIDUALMENTE_NO_RELATORIO",
"note":"The ten theorems using the definition are present; absence of a definition entry is not absence of its source."},
"clean_theorems":{"passed":int(counts[0][0]),"total":int(counts[0][1])},"rite_checkpoints":seal["rite_checkpoints"],
"selftest":seal["fail_closed_selftest"],"gate":seal["qg_closure_verdict"],"identity":seal["identity"],
"collapse_definition":seal["collapse_definition"],"logs":logs,"capture_diagnostics":[name for name,r in logs.items() if not r["stdout_matches_manifest"]],"memory_surfaces":[rec(f) for f in surfaces],
"stale_index_findings":["Cabeçalho ainda descreve rodada intermediária e última completa v320; selo atual é v334 completa.",
"Tabela v333 contém pin de v331; consultar handoff e backup de bytes."],
"formal_scope_note":"TheScreenIsFounded characterizes the fixed algebra for the given profile and contract. It does not construct HorizonEquilibriumData or identify a causal spacetime horizon. Its area theorem retains an explicit relative trace assumption.",
"online_memory":{"status":"AUTHENTICATED_NOT_YET_SAVED","browser":"Codex In-app Browser","page":"https://chatgpt.com/","memory_write_performed":False},
"source_um_executed":False,"canonical_files_modified":False}
output=new("EVIDENCIAS_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f")+".json",data)
print(json.dumps({"folder":folder.as_posix(),"report":output.as_posix(),"sealed":len(sealed),"formal_files":len(formal),
"embedded_sources":len(selected),"axiom_terms":len(axioms),"outside_trio":len(outside),"without_axioms":data["without_axioms"],
"clean_theorems":data["clean_theorems"],"screen_theorems":len(screen_terms),"um_sha256":um["sha256"]}))
