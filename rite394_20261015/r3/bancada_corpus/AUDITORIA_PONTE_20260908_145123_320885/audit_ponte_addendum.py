from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import ast,json,hashlib,os,sys
sys.stdout.reconfigure(encoding="utf-8")
folder=Path(__file__).resolve().parent
if folder.parent != Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve() or not folder.name.startswith("AUDITORIA_PONTE_"):
    raise RuntimeError("Output folder outside authorized audit scope")
base=json.loads((folder/"RESULTADOS_EXATOS.json").read_text(encoding="utf-8"))
um=Path(base["sources"]["um"]["path"]).read_bytes()
if hashlib.sha256(um).hexdigest()!=base["sources"]["um"]["sha256"]:
    raise RuntimeError("um.py changed since primary audit")
tree=ast.parse(um.decode("utf-8-sig"))
assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="_EMBEDDED_KERNEL_FILES" for t in n.targets))
embedded=ast.literal_eval(assignment.value)
extra={}
for name in ["TowerDefinite","TowerAction"]:
    path=Path(base["sources"]["TheOathOnTheTower"]["path"]).parent/(name+".lean")
    data=path.read_bytes()
    text=data.decode("utf-8-sig").replace("\r\n","\n").replace("\r","\n")
    entry={"path":path.as_posix(),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),
        "lines":len(text.splitlines()),"embedded_text_equal":text==embedded["TGLExt/"+name+".lean"].replace("\r\n","\n").replace("\r","\n")}
    if not entry["embedded_text_equal"]: raise RuntimeError("Additional source mismatch")
    extra[name]=entry
    ranges=[(48,86)] if name=="TowerDefinite" else [(357,376)]
    for lo,hi in ranges:
        for i,line in enumerate(text.splitlines(),1):
            if lo<=i<=hi: print(name,str(i)+":",line)
def z(): return [[F(0) for j in range(4)] for i in range(4)]
def mul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
def tr(a): return [list(row) for row in zip(*a)]
def dg(a): return [[a[i][j] if i==j else F(0) for j in range(4)] for i in range(4)]
identity=z()
for i in range(4): identity[i][i]=F(1)
v=[row[:] for row in identity]
v[1][1]=v[2][2]=F(3,5)
v[1][2]=F(-4,5); v[2][1]=F(4,5)
rho=z()
for i,w in enumerate([F(1,9),F(2,9),F(2,9),F(4,9)]): rho[i][i]=w
projection=z(); projection[1][1]=F(1)
rotated=mul(mul(v,projection),tr(v))
checks={
    "rotation_unitary":mul(tr(v),v)==identity,
    "rotation_preserves_same_nontracial_rho":mul(mul(v,rho),tr(v))==rho,
    "rotated_off_diagonal_exact":rotated[1][2]==F(12,25),
    "diagonal_expectation_not_covariant":dg(rotated)!=mul(mul(v,dg(projection)),tr(v)),
}
assert all(checks.values())
for entry in extra.values():
    assert hashlib.sha256(Path(entry["path"]).read_bytes()).hexdigest()==entry["sha256"]
result={"created_utc":datetime.now(timezone.utc).isoformat(),
    "status":"PASS_ADDITIONAL_SOURCE_MATCH_AND_EXACT_ROTATION",
    "sources":extra,"rotation":v,"rotated_projection":rotated,"checks":checks,
    "scope":"Same nontracial finite prefix; no new Lean compilation, original writes, or independent review.",
    "primary_results_sha256":hashlib.sha256((folder/"RESULTADOS_EXATOS.json").read_bytes()).hexdigest()}
data=(json.dumps(result,ensure_ascii=False,indent=2,default=str)+"\n").encode("utf-8")
target=folder/"ADENDO_DEGENERESCENCIA.json"
temp=folder/"ADENDO_DEGENERESCENCIA.json.tmp"
if target.exists(): raise RuntimeError("Exclusive creation required")
with temp.open("xb") as f: f.write(data); f.flush(); os.fsync(f.fileno())
assert temp.read_bytes()==data
os.rename(temp,target)
assert target.read_bytes()==data
print(json.dumps({"status":result["status"],"output":target.as_posix(),"checks":checks},ensure_ascii=False))
