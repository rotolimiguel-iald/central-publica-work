from pathlib import Path
import json,hashlib,datetime
root=Path(__file__).resolve().parent
assert root.is_relative_to(Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve())
def pin(p):
    p=Path(p); b=p.read_bytes()
    return {"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
before=json.loads((root/"PINS_ANTES_ADENDO_SINAL_077.json").read_text(encoding="utf-8"))
after=[]
for p in before:
    m=pin(p["path"]);m["unchanged"]=all(m[k]==p[k] for k in ("path","bytes","sha256"));after.append(m)
assert all(x["unchanged"] for x in after)
note=root/"ADENDO_SINAL_KOSZUL_TATE_077.md"
obj={"created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"author":"/root/finish_gibbs_realization",
"status":"DERIVED_SIGN_CORRECTION_WITH_LINEAR_CHAIN_ISOMORPHISM",
"correction":"s0u*=+H0u for written S2 and right-derivative convention; s0c*=+R0adjoint u*",
"source_pins_after":after,"new_artifacts":[pin(note),pin(root/"PINS_ANTES_ADENDO_SINAL_077.json"),pin(Path(__file__))],
"primary":{"url":"https://arxiv.org/pdf/1803.10235v3","scope":"Equation140, checked directly"},
"scope":["Corrects equation3 convention in frozen077","Initial ghost3/4 counts use only fields and ghosts","No assertion of whole-note independent approval","No change to076"],
"um_executed_or_imported":False,"lean_or_cas_executed":False,"originals_written":False}
dest=root/"MANIFESTO_ADENDO_SINAL_077.json";tmp=root/(dest.name+".pending")
assert not dest.exists() and not tmp.exists()
b=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
with tmp.open("xb") as f:f.write(b)
assert tmp.read_bytes()==b and len(b)>0
tmp.rename(dest); assert dest.read_bytes()==b
print(json.dumps({"note":pin(note),"manifest":pin(dest),"sources_unchanged":len(after)},ensure_ascii=False))

