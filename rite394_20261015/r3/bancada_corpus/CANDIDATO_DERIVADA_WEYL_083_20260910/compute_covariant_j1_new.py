from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
from datetime import datetime, timezone
import hashlib, json, os

ROOT=Path(r"C:/IALD/Central de Patentes/Chatgpt")
OUT=ROOT/"CANDIDATO_DERIVADA_WEYL_083_20260910"
SOURCES=[
ROOT/"DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md",
ROOT/"SETOR_QUADRATICO_SEM_DERIVADAS_082_20260910_050315_8076779/IMAGEM_DO_DETECTOR_NO_SETOR_FINITO.md",
ROOT/"RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md",
]
def pin(path):
    b=path.read_bytes()
    return {"path":str(path),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
before=[pin(p) for p in SOURCES]
self_before=pin(Path(__file__).resolve())
Z={}
def const(a): return {} if not a else {(0,0,0,0,0):F(a)}
def mon(c=1,k=0,z=0,ell=0,f=0,p=0): return {} if not c else {(k,z,ell,f,p):F(c)}
def add(*args):
    out={}
    for a in args:
        for e,c in a.items(): out[e]=out.get(e,F(0))+c
    return {e:c for e,c in out.items() if c}
def scale(a,c): return {e:v*F(c) for e,v in a.items() if v*c}
def mul(a,b):
    out={}
    for ea,ca in a.items():
        for eb,cb in b.items():
            e=tuple(x+y for x,y in zip(ea,eb))
            out[e]=out.get(e,F(0))+ca*cb
    return {e:c for e,c in out.items() if c}
def diff(a,i):
    out={}
    for e,c in a.items():
        if e[i]:
            ee=list(e); ee[i]-=1
            out[tuple(ee)]=c*e[i]
    return out
def dz(a):
    return add(diff(a,1),mul(mon(p=1),diff(a,3)),
               mul(add(mon(2,z=-1,p=1),mon(-1,k=2,f=1)),diff(a,4)))
def data(a):
    out={}
    for (k,z,ell,f,p),c in a.items():
        if f: continue
        e=(k,z+ell,0,0,0)
        out[e]=out.get(e,F(0))+c
    return {e:c for e,c in out.items() if c}
def at_ratio(a,ratio):
    out={}
    for (k,z,ell,f,p),c in data(a).items():
        e=(0,z-k,0,0,0)
        out[e]=out.get(e,F(0))+c*F(ratio)**k
    return {e:c for e,c in out.items() if c}
def fmt(a):
    return [{"powers":dict(zip(["k","z","ell","f","p"],e)),
             "coefficient":str(c)} for e,c in sorted(a.items())]
def neg(a): return scale(a,-1)
def eq(a,b): return not add(a,neg(b))
eta=[1,-1,-1,-1]
pairs=list(combinations(range(4),2))
def eps(t):
    if len(set(t))<4:return 0
    return (-1)**sum(t[i]>t[j] for i in range(4) for j in range(i+1,4))
E=add(mon(F(1,2),k=2,f=1),mon(F(-1,2),z=-1,p=1))
B=mon(F(1,2),k=1,p=1)
W={}
def put(a,b,c,d,value):
    for i,j,s1 in [(a,b,1),(b,a,-1)]:
        for l,m,s2 in [(c,d,1),(d,c,-1)]:
            key=(i,j,l,m)
            val=scale(value,s1*s2)
            if key in W and not eq(W[key],val):raise RuntimeError("Conflicting Weyl entry")
            W[key]=val
for a,b,c,d,v in [
(0,1,0,1,E),(0,1,2,3,B),(0,2,0,2,neg(E)),(0,2,1,3,B),
(1,3,0,2,B),(1,3,1,3,E),(2,3,0,1,B),(2,3,2,3,neg(E))]:
    put(a,b,c,d,v)
def get(t):return W.get(tuple(t),Z)
def gamma(a,b,e):
    out=Z
    if a==b and e==3:out=add(out,mon(-1,z=-1))
    if a==e and b==3:out=add(out,mon(-1,z=-1))
    if b==e and a==3:out=add(out,mon(-eta[b],z=-1))
    return out
Arot={(1,2):mon(F(-1,2),k=1),(2,1):mon(F(1,2),k=1)}
def tau(t):
    out=Z
    for i in range(4):
        for u in range(4):
            a=Arot.get((t[i],u),Z)
            if a:
                ti=list(t);ti[i]=u
                out=add(out,mul(a,get(ti)))
    return out
indices=list(product(range(4),repeat=4))
N=[]
for e in range(4):
    ne={}
    for t in indices:
        value=dz(get(t)) if e==3 else tau(t) if e==0 else Z
        if e==3:value=add(value,mul(mon(-2,z=-1),get(t)))
        for i in range(4):
            for u in range(4):
                ti=list(t);ti[i]=u
                value=add(value,neg(mul(gamma(u,t[i],e),get(ti))))
        if value:ne[t]=value
    N.append(ne)
def trace_wedge(A,B):
    out=Z
    for a,b in product(range(4),repeat=2):
        for c,d in pairs:
            for e,f in pairs:
                sign=eps((c,d,e,f))
                if sign:
                    out=add(out,scale(mul(A.get((a,b,c,d),Z),B.get((b,a,e,f),Z)),
                                      eta[a]*eta[b]*sign))
    return out
J=mul(mon(z=4,ell=-4),trace_wedge(W,W))
J_expected=mul(mon(16,z=4,ell=-4),mul(E,B))
J1_direct=Z
for e in range(4):
    J1_direct=add(J1_direct,scale(trace_wedge(N[e],N[e]),eta[e]))
J1_direct=mul(mon(z=6,ell=-6),J1_direct)
boxJ=mul(mon(z=2,ell=-2),add(neg(dz(dz(J))),mul(mon(2,z=-1),dz(J))))
J1_wave=add(scale(boxJ,F(1,2)),mul(mon(-6,ell=-2),J))
profile=add(mul(mon(6,z=-1),dz(J1_direct)),mul(mon(-18,z=-2),J1_direct))
profile0=add(mul(mon(6,z=-1),dz(J)),mul(mon(-18,z=-2),J))
checks={}
checks["weyl_pair_symmetry"]=all(eq(get((a,b,c,d)),get((c,d,a,b))) for a,b,c,d in indices)
checks["weyl_bianchi"]=all(not add(get((a,b,c,d)),get((b,c,a,d)),get((c,a,b,d))) for a,b,c,d in indices)
checks["weyl_trace"]=all(not add(*(scale(get((a,b,a,d)),eta[a]) for a in range(4))) for b,d in product(range(4),repeat=2))
checks["pontryagin_normalization_16EB"]=eq(J,J_expected)
checks["J_data"]=eq(data(J),mon(-4,k=1,z=-1))
checks["Jprime_data"]=eq(data(dz(J)),add(mon(4,k=3),mon(-28,k=1,z=-2)))
checks["profile_081_reference"]=eq(data(profile0),add(mon(24,k=3,z=-1),mon(-96,k=1,z=-3)))
checks["direct_covariant_equals_wave_identity"]=eq(J1_direct,J1_wave)
checks["J1_odd_k"]=all(e[0]%2==1 for e in J1_direct)
checks["profile_odd_k"]=all(e[0]%2==1 for e in profile)
after=[pin(p) for p in SOURCES]
self_after=pin(Path(__file__).resolve())
if before!=after or self_before!=self_after:raise RuntimeError("Input or script changed")
result={
"created_utc":datetime.now(timezone.utc).isoformat(),
"method":"Exact Fraction Laurent polynomial; direct covariant derivatives with all four covariant Weyl slots and conformal weight; no source scripts imported/executed",
"notation":{"p":"f prime","dz":"ODE-reduced derivative with ell,k fixed","data":"f=0,p=1,ell=z only AFTER differentiation","J1":"g0^ef tr(nabla_e W wedge nabla_f W)/vol_g0"},
"checks":checks,"all_math_checks_pass":all(checks.values()),
"J":fmt(J),"box_J":fmt(boxJ),"J1_direct":fmt(J1_direct),
"J1_at_point":fmt(data(J1_direct)),"J1_prime_at_point":fmt(data(dz(J1_direct))),
"detector_without_coupling":fmt(data(profile)),
"detector_at_k_2_over_z":fmt(at_ratio(profile,2)),
"box_J_at_point":fmt(data(boxJ)),
"sources_before":before,"sources_after":after,
"script_before":self_before,"script_after":self_after,
"all_sources_unchanged":before==after,"script_unchanged":self_before==self_after,
"um_py_executed_or_imported":False,"lean_runs":0,
"not_verified_by_code":["Einstein EOM in a full neighborhood (written078)","helical symmetry of full TT family (written083)","wave identity for arbitrary Weyl jets (written083)","cohomological cancellation or all higher derivatives"]
}
OUT.mkdir(parents=True,exist_ok=True)
path=OUT/"CONTROLE_COVARIANTE_J1_083.json"
temp=path.with_name(path.name+".pending")
if path.exists():raise FileExistsError(path)
payload=(json.dumps(result,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
with temp.open("xb") as out:
    out.write(payload);out.flush();os.fsync(out.fileno())
if temp.read_bytes()!=payload:raise RuntimeError("Temp mismatch")
temp.rename(path)
if path.read_bytes()!=payload:raise RuntimeError("Final mismatch")
print(json.dumps({"receipt":pin(path),"math_checks":checks,
                 "J1_data":fmt(data(J1_direct)),"J1_prime":fmt(data(dz(J1_direct))),
                 "profile":fmt(data(profile)),"at_k2":fmt(at_ratio(profile,2))},ensure_ascii=False,indent=2))
if not all(checks.values()):raise SystemExit(1)

