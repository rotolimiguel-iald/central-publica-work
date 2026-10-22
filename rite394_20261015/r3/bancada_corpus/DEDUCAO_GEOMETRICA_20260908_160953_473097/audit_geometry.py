"""Read-only source audit; exact finite Fisher checks; bounded decimal illustrations."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
from itertools import product
from datetime import datetime,timezone
import ast,hashlib,json,os,re,sys
sys.stdout.reconfigure(encoding="utf-8")
folder=Path(__file__).resolve().parent
assert folder.parent==Path(r"C:\IALD\Central de Patentes\Chatgpt")
canon=Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
kernel=canon/"tgl_kernel"
modules=["SummableGravityControls","SummableProfileCurve","SummableRelativeQuartic",
"SummableStateThermodynamics","MicroscopicEinsteinBridge","SummableGravityBridge",
"TriadMaster","CentralizerPhaseOrbit","LikelihoodDensityLog","DensityStateUniqueness",
"SiteLogLikelihood","TheOathOnTheTower"]
def record(p):
    raw=p.read_bytes()
    return {"path":p.as_posix(),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
umrec=record(canon/"um.py")
tree=ast.parse((canon/"um.py").read_text(encoding="utf-8-sig"))
assignments=[n for n in tree.body if isinstance(n,ast.Assign) and
    any(isinstance(t,ast.Name) and t.id=="_EMBEDDED_KERNEL_FILES" for t in n.targets)]
assert len(assignments)==1 and isinstance(assignments[0].value,ast.Dict)
embedded=ast.literal_eval(assignments[0].value)
assert isinstance(embedded,dict)
norm=lambda s:s.replace("\r\n","\n").replace("\r","\n")
sources=[];declarations={}
for name in modules:
    p=kernel/"TGLExt"/(name+".lean");txt=p.read_text(encoding="utf-8-sig")
    assert norm(embedded["TGLExt/"+name+".lean"])==norm(txt)
    sources.append(record(p))
    declarations[name]=[{"name":m.group(1),"line":i} for i,line in enumerate(txt.splitlines(),1)
        if (m:=re.match(r"\s*(?:noncomputable\s+)?(?:def|theorem|structure)\s+(\w+)",line))]
collisions=[]
for p in folder.glob("*.lean"):
    source=p.read_text(encoding="utf-8")
    namespaces=re.findall(r"(?m)^namespace ([\w.]+)$",source)
    assert len(namespaces)==1
    namespace=namespaces[0]
    # Match exact names inside the same namespace in the literal canonical sources.
    names=set(re.findall(r"(?m)^(?:noncomputable\s+)?(?:def|theorem|abbrev)\s+(\w+)",source))
    for key,val in embedded.items():
        if not key.endswith(".lean"):continue
        if re.search(r"(?m)^namespace "+re.escape(namespace)+r"\s*$",val):
            overlap=names&set(re.findall(r"(?m)^(?:noncomputable\s+)?(?:def|theorem|abbrev)\s+(\w+)",val))
            collisions += [{"module":p.name,"canonical":key,"name":n} for n in overlap]
assert not collisions
checks=0
def check(ok,label):
    global checks
    checks+=1
    if not ok:raise AssertionError(label)
def b(n):return F(1,24)*F(1,2)**n
def q(r,n):return F(1,3)-b(n)*r
def site_fisher(r,n):return b(n)**2/(q(r,n)*(1-q(r,n)))
def fisher_tail_bound(count):return F(4,357)*F(1,4)**count
finite=[]
for r in [F(0),F(1,2),F(1)]:
    for count in range(1,9):
        mean=F(0);variance=F(0);mass=F(0)
        for bits in product([False,True],repeat=count):
            weight=F(1);score=F(0)
            for n,bit in enumerate(bits):
                qn=q(r,n)
                weight *= qn if bit else 1-qn
                score += -b(n)/qn if bit else b(n)/(1-qn)
            mass+=weight;mean+=weight*score;variance+=weight*score**2
        expected=sum((site_fisher(r,n) for n in range(count)),F(0))
        check(mass==1,"product normalization")
        check(mean==0,"joint score centered")
        check(variance==expected,"joint Fisher equals sum of site Fisher")
        prefix_square=sum((b(n)**2 for n in range(count)),F(0))
        check(F(9,2)*prefix_square<=variance<=F(576,119)*prefix_square,"prefix Fisher bounds")
        finite.append({"r":str(r),"sites":count,"joint_fisher":str(variance),
                      "entire_missing_tail_upper_bound":str(fisher_tail_bound(count))})
for r in [F(0),F(1,2),F(1)]:
    for n in range(32):
        qn=q(r,n)
        check(F(7,24)<=qn<=F(1,3),"weight range")
        check(F(119,576)<=qn*(1-qn)<=F(2,9),"variance range")
        check(F(9,2)*b(n)**2<=site_fisher(r,n)<=F(576,119)*b(n)**2,"site Fisher bounds")
    partial=sum((site_fisher(r,n) for n in range(40)),F(0))
    check(partial+fisher_tail_bound(40)>=F(1,96),"global lower bound enclosure")
    check(partial<=F(4,357),"global upper bound")
# The phase at pi is diag(-1,1) on site zero and acts nontrivially on E01.
reflection=[[F(-1),F(0)],[F(0),F(1)]]
e01=[[F(0),F(1)],[F(0),F(0)]]
def mul(x,y):
    return [[sum((x[i][k]*y[k][j] for k in range(2)),F(0)) for j in range(2)] for i in range(2)]
for r in [F(0),F(1,2),F(1)]:
    rho=[[F(1,3),F(0)],[F(0),F(2,3)]]
    sigma=[[q(r,0),F(0)],[F(0),1-q(r,0)]]
    relative=[[q(r,0)/F(1,3),F(0)],[F(0),(1-q(r,0))/F(2,3)]]
    check(mul(mul(reflection,rho),reflection)==rho,"reference fixed")
    check(mul(mul(reflection,sigma),reflection)==sigma,"preparation fixed")
    check(mul(mul(reflection,relative),reflection)==relative,"relative density fixed")
check(mul(mul(reflection,e01),reflection)==[[F(0),F(-1)],[F(0),F(0)]],"quantum observable changed")
examples=[];fisher_enclosures=[]
with localcontext() as ctx:
    ctx.prec=85
    def dec(x):return Decimal(x.numerator)/Decimal(x.denominator)
    count=48
    for t in [F(1),F(1,2),F(1,10),F(1,100),F(1,1000)]:
        r=t*t/(1+t*t)
        entropy=Decimal(0)
        for n in range(count):
            qn=q(r,n)
            entropy+=dec(qn)*(dec(qn/F(1,3))).ln()+dec(1-qn)*(dec((1-qn)/F(2,3))).ln()
        ratio=entropy/dec(t**4)
        examples.append({"t":str(t),"relative_entropy_over_t4_approx":str(ratio),
            "infinite_tail_bound_on_ratio":str(F(1,96)*F(1,4)**count),
            "limit":str(F(1,192)),"decimal_rounding_not_certified":True})
    for r in [F(0),F(1,2),F(1)]:
        partial=sum((site_fisher(r,n) for n in range(count)),F(0))
        fisher_enclosures.append({"r":str(r),"lower_approx":str(dec(partial)),
            "upper_approx":str(dec(partial+fisher_tail_bound(count))),
            "exact_lower":str(partial),"exact_upper":str(partial+fisher_tail_bound(count))})
assert record(canon/"um.py")==umrec
assert all(record(Path(r["path"]))==r for r in sources)
result={"status":"PASS_EXACT_DIAGNOSTICS_AND_READ_ONLY_SOURCE_LINK",
"created_utc":datetime.now(timezone.utc).isoformat(),"exact_checks":checks,
"matched_canonical_modules":len(sources),"canonical_um":umrec,"canonical_sources":sources,
"declarations":declarations,"namespace_collision_check":"NO_LITERAL_MATCH_IN_SAME_NAMESPACE",
"finite_fisher_checks":finite,"fisher_global_enclosures":fisher_enclosures,
"entropy_limit_illustrations":examples,
"scope":{"canonical_changes":False,"um_executed_or_imported":False,
"finite_tests_are_infinite_proof":False,"decimal_roundoff_is_certified":False,
"physical_area_deduced":False,"qg_proof":False}}
p=folder/("DIAGNOSTICOS_"+datetime.now().strftime("%Y%m%d_%H%M%S_%f")+".json")
raw=(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
tmp=p.with_name(p.name+".tmp")
with tmp.open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==raw;os.rename(tmp,p);assert p.read_bytes()==raw
print(json.dumps({"path":p.as_posix(),"exact_checks":checks,"matched_modules":len(sources),
"fisher":[{"r":r["r"],"value":r["lower_approx"]} for r in fisher_enclosures],
"entropy":[{"t":r["t"],"value":r["relative_entropy_over_t4_approx"]} for r in examples]},ensure_ascii=False))
