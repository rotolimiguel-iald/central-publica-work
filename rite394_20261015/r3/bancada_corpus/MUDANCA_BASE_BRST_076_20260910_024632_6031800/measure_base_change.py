from pathlib import Path
import json, hashlib, datetime, re
ROOT=Path(__file__).resolve().parent
assert ROOT.is_relative_to(Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve())
def pin(p):
    p=Path(p); b=p.read_bytes()
    return {"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
before=json.loads((ROOT/"PINS_INICIAIS.json").read_text(encoding="utf-8"))
after=[]
for x in before["pins"]:
    y=pin(x["path"]); y["unchanged"]=all(y[k]==x[k] for k in ("path","bytes","sha256")); after.append(y)
assert all(x["unchanged"] for x in after)
note=ROOT/"MUDANCA_BASE_E_COMPLETACAO_H3_H4.md"
links=[]
content=note.read_text(encoding="utf-8")
for m in re.finditer(r"\[[^\]\n]*\]\(<([^>\n]+)>\)",content):
    path=m.group(1); target=Path(path)
    links.append({"target":path,"exists":target.is_file()})
assert all(x["exists"] for x in links)
obj={"created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
"author":"/root/finish_gibbs_realization","status":"DERIVED_WRITTEN_PROOFS_WITH_EXPLICIT_DOMAIN",
"source_pins_after":after,"own_artifacts":[pin(note),pin(ROOT/"PINS_INICIAIS.json"),pin(Path(__file__))],
"links":links,"primary_sources":[{"url":"https://arxiv.org/pdf/hep-th/9505173v2","verified_scope":"Appendix C, E.7 and surrounding finite-type hypotheses; coordinate Cartan identity and comparison proved in note"}],
"results":["Finite separated base change, no diagonal completion","Global oriented H3 target class nontrivial via on-shell SU2 orbit and killed by existing formal primitive","Inverse-limit exact sequence for natural valence truncations"],
"open":["Full Q2 completed mu iso g3/g4","Generation by K and relations","O4 joint invariants when required","Natural E2 and admissible anomaly removal","QME/current/UV"],
"um_executed_or_imported":False,"lean_or_cas_executed":False,"originals_written":False,"all_sources_unchanged":True}
dest=ROOT/"MANIFESTO_MUDANCA_BASE_076.json"; temp=ROOT/(dest.name+".pending")
assert not dest.exists() and not temp.exists()
b=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
with temp.open("xb") as f:f.write(b)
assert temp.read_bytes()==b and len(b)>0
temp.rename(dest)
assert dest.read_bytes()==b
print(json.dumps({"note":pin(note),"manifest":pin(dest),"sources":len(after),"links":len(links)},ensure_ascii=False))

