"""Read-only link audit plus exact finite illustrations of the existing tower."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal, localcontext
from datetime import datetime,timezone
from itertools import product
import ast,hashlib,json,os,re,sys
sys.stdout.reconfigure(encoding="utf-8")
out=Path(__file__).resolve().parent
assert out.parent==Path(r"C:\IALD\Central de Patentes\Chatgpt")
canon=Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
kernel=canon/"tgl_kernel"
modules=["SummableProfileCurve","SummableGravityControls","SiteLogLikelihood",
"SummableLikelihoodGenerator","LikelihoodCocycle","LikelihoodPreparedState",
"LikelihoodDensityLog","CentralizerDensity","DensityStateUniqueness",
"TowerDefinite","TowerAction","ExpectationPositive","TheFactorObject",
"TheOathOnTheTower","RightMult","ThermalLimitControls","PowersLadder"]
def digest(raw):return hashlib.sha256(raw).hexdigest()
def record(p):
    raw=p.read_bytes()
    return {"path":p.as_posix(),"bytes":len(raw),"sha256":digest(raw)}
def new(p,raw):
    assert p.parent==out and not p.exists()
    tmp=p.with_name(p.name+".tmp")
    with tmp.open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==raw
    os.rename(tmp,p)
    assert p.read_bytes()==raw
um=canon/"um.py"
umraw=um.read_bytes()
tree=ast.parse(umraw.decode("utf-8-sig"),filename=str(um))
assignments=[n for n in tree.body if isinstance(n,ast.Assign) and
    any(isinstance(t,ast.Name) and t.id=="_EMBEDDED_KERNEL_FILES" for t in n.targets)]
assert len(assignments)==1 and isinstance(assignments[0].value,ast.Dict)
embedded=ast.literal_eval(assignments[0].value)
assert isinstance(embedded,dict) and all(isinstance(k,str) and isinstance(v,str) for k,v in embedded.items())
norm=lambda s:s.replace("\r\n","\n").replace("\r","\n")
sources=[];boundaries=[];declarations={}
for name in modules:
    p=kernel/"TGLExt"/(name+".lean")
    raw=p.read_bytes();txt=raw.decode("utf-8-sig")
    key="TGLExt/"+name+".lean"
    match=key in embedded and norm(embedded[key])==norm(txt)
    if not match:raise RuntimeError("Visible embedded/source mismatch: "+key)
    rec=record(p);rec["embedded_key"]=key;rec["text_matches_after_line_ending_normalization"]=True
    sources.append(rec)
    declarations[name]=[{"name":m.group(1),"line":i} for i,line in enumerate(txt.splitlines(),1)
        if (m:=re.match(r"\s*(?:noncomputable\s+)?(?:def|theorem|lemma)\s+(\w+)",line))]
    binary=kernel/".lake/build/lib/lean/TGLExt"/(name+".olean")
    boundaries.append(record(binary))
    for suf in [".server",".private"]:
        extra=Path(str(binary)+suf)
        if extra.exists():boundaries.append(record(extra))
assert um.read_bytes()==umraw
for rec in sources+boundaries:
    assert record(Path(rec["path"]))["sha256"]==rec["sha256"]
checks=0
def check(value,label):
    global checks
    checks+=1
    if not value:raise AssertionError(label)
t=F(1);r=t*t/(1+t*t)
def x(n):return F(1,24)*F(1,2)**n*r
def contrast_ratio(n):return (1+F(3,2)*x(n))/(1-3*x(n))
for n in range(64):
    y=x(n)
    polynomial=(1+F(3,2)*y)*(1-F(3,2)*y)**2-(1+F(3,4)*y)**2*(1-3*y)
    check(polynomial==F(27,16)*y*y*(1+3*y),"polynomial identity")
    check(contrast_ratio(n)>contrast_ratio(n+1)**2,"strict dyadic separation")
cuts=[];example=[]
for length in range(1,11):
    weights=[];prepared=[];ratios=[]
    for bits in product([False,True],repeat=length):
        w=F(1);q=F(1);ratio=F(1)
        for n,bit in enumerate(bits):
            w*=F(1,3) if bit else F(2,3)
            q*=F(1,3)-x(n) if bit else F(2,3)+x(n)
            ratio*=1-3*x(n) if bit else 1+F(3,2)*x(n)
        check(q/w==ratio,"actual prepared/reference identity")
        weights.append(w);prepared.append(q);ratios.append(ratio)
        if length==3:
            with localcontext() as ctx:
                ctx.prec=50
                logratio=(Decimal(ratio.numerator)/Decimal(ratio.denominator)).ln()
                example.append({"bits_Pn": "".join("1" if b else "0" for b in bits),
                    "reference_weight":str(w),"prepared_weight":str(q),"relative_density":str(ratio),
                    "log_relative_density_approx":str(logratio)})
    check(sum(weights)==1,"reference normalization")
    check(sum(prepared)==1,"prepared normalization")
    check(sum(w*h for w,h in zip(weights,ratios))==1,"relative density normalization")
    check(len(set(ratios))==len(ratios),"simple relative spectrum")
    cuts.append({"sites":length,"configurations":len(ratios),"distinct_relative_eigenvalues":len(set(ratios))})
# Infinite-tail intervals for a fixed finite prefix use the proved analytical bound.
intervals=[]
with localcontext() as ctx:
    ctx.prec=70
    for n in [0,1,4,8,16,32]:
        def dlog(fr):return (Decimal(fr.numerator)/Decimal(fr.denominator)).ln()
        an=dlog(contrast_ratio(n));tail_upper=2*dlog(contrast_ratio(n+1))
        intervals.append({"site":n,"contrast_approx":str(an),
            "entire_tail_upper_bound_approx":str(tail_upper),
            "certified_gap_lower_bound_approx":str(an-tail_upper),
            "exact_gap_positive_check":contrast_ratio(n)>contrast_ratio(n+1)**2})
result={"status":"PASS_READ_ONLY_LINK_AND_EXACT_EXAMPLES",
"created_utc":datetime.now(timezone.utc).isoformat(),
"um":{"path":um.as_posix(),"bytes":len(umraw),"sha256":digest(umraw)},
"embedded_entries":len(embedded),"matched_modules":len(sources),
"canonical_sources":sources,"canonical_binaries":boundaries,
"declaration_locations":declarations,"canonical_rechecked_unchanged":True,
"exact_checks":checks,"parameter_t":str(t),"regular_parameter":str(r),
"cuts":cuts,"three_site_example":example,"infinite_tail_bound_illustrations":intervals,
"scope":{"um_executed":False,"um_imported":False,"canonical_writes":False,
"finite_examples_prove_infinite_theorem":False,"decimal_numbers_are_proofs":False,
"new_infinite_proof":"See fresh Lean compilation and analytical report",
"source_binary_rebuild_verified":False}}
p=out/("AUDITORIA_MODELO_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f")+".json")
new(p,(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
print(json.dumps({"path":p.as_posix(),"status":result["status"],"matched_modules":len(sources),
"exact_checks":checks,"examples":example,"bounds":intervals[:2]},ensure_ascii=False))
