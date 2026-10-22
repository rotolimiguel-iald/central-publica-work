from pathlib import Path
import json, hashlib, datetime, re
root=Path(__file__).resolve().parent
assert root.is_relative_to(Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve())
def pin(p):
    p=Path(p); b=p.read_bytes()
    return {"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
snap=json.loads((root/"PINS_INICIAIS.json").read_text(encoding="utf-8"))
after=[]
for old in snap["pins"]:
    new=pin(old["path"]); new["unchanged"]=all(old[k]==new[k] for k in ("path","bytes","sha256")); after.append(new)
assert all(x["unchanged"] for x in after)
note=root/"S0_KILLING_E_PRIMEIRA_TRANSICAO.md"
links=[{"path":m.group(1),"exists":Path(m.group(1)).is_file()} for m in re.finditer(r"\[[^\]\n]*\]\(<([^>\n]+)>\)",note.read_text(encoding="utf-8"))]
assert all(x["exists"] for x in links)
obj={"created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"author":"/root/finish_gibbs_realization",
"status":"DERIVED_WRITTEN_CALCULATION_AWAITING_INDEPENDENT_REVIEW",
"source_pins":after,"own_artifacts":[pin(note),pin(root/"PINS_INICIAIS.json"),pin(Path(__file__))],
"links":links,"primary":[{"url":"https://arxiv.org/pdf/hep-th/9505173v2","scope":"Finite Lie algebra CE primitives for so(2r+1), section7.1 AppendixB; not full nonlinear BRST classification"}],
"calculated_scope":{"background":"Nonzero constant curvature, constant sigma, regular natural metric presentation",
"linear_ghost_quotient":10,"G_invariants_Lambda2_3_4":[0,4,3],"H3_C3_natural":4,"image_H3_C4_to_C3":1,"H4_C4_natural":0},
"limits":["No full CE lifting assertion","No nonzero lim1 assertion","No QME/anomaly verdict","No arbitrary background cohomology identification"],
"um_executed_or_imported":False,"lean_or_cas_executed":False,"originals_written":False}
dest=root/"MANIFESTO_PRIMEIROS_TRUNCAMENTOS_077.json"; tmp=root/(dest.name+".pending")
assert not dest.exists() and not tmp.exists()
b=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
with tmp.open("xb") as f:f.write(b)
assert tmp.read_bytes()==b and len(b)>0
tmp.rename(dest); assert dest.read_bytes()==b
print(json.dumps({"note":pin(note),"manifest":pin(dest),"sources":len(after)},ensure_ascii=False))

