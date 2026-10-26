"""Check report source pins/excerpts and the three stated algebraic models only."""
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone
import sympy as s

base=Path(__file__).resolve().parent
report_path=base/"MASS_SOURCES.json"
raw=report_path.read_bytes()
report=json.loads(raw)
pins=[]
for source in report["sources"]:
    data=Path(source["path"]).read_bytes()
    pin=hashlib.sha256(data).hexdigest()
    lines=data.decode("utf-8-sig").splitlines()
    assert pin==source["sha256"], source["id"]
    for excerpt in source["excerpts"]:
        assert "\n".join(lines[excerpt["first_line"]-1:excerpt["last_line"]])==excerpt["text"]
    pins.append({"source_id":source["id"],"sha256":pin,"exact_excerpts":True})

x, mu2, lam, v2, y, g4, g6, t=s.symbols("x mu2 lam v2 y g4 g6 t", real=True)
V=lam*(x*x-v2)**2/4+mu2*x*x/2
assert s.expand(s.diff(V,x)-x*(lam*(x*x-v2)+mu2))==0
assert s.simplify(s.diff(V,x,2).subs(x*x,v2-mu2/lam)-2*(lam*v2-mu2))==0
v=s.symbols("v",real=True)
assert s.simplify(s.diff(V,x).subs({x:v,v2:v*v})-mu2*v)==0
S=mu2*x*x/2+g4*x**4/4+g6*x**6/6
assert s.expand(s.diff(S,x)-x*(mu2+g4*x*x+g6*x**4))==0
assert s.expand(s.diff(S,x,2).subs({x*x:y,mu2:-g4*y-g6*y*y})-2*y*(g4+2*g6*y))==0
assert s.expand(s.diff(t*V,x,2)-t*s.diff(V,x,2))==0

r,R,A,c,G=s.symbols("r R A c G",positive=True)
inside=A*(3-r*r/(R*R))
outside=2*A*R/r
lap=lambda u: s.simplify(s.diff(r*r*s.diff(u,r),r)/(r*r))
assert s.simplify(inside.subs(r,R)-outside.subs(r,R))==0
assert s.simplify(s.diff(inside,r).subs(r,R)-s.diff(outside,r).subs(r,R))==0
assert s.limit(outside,r,s.oo)==0
assert s.simplify(lap(inside)+6*A/(R*R))==0
assert lap(outside)==0
rho=-c*c*lap(inside)/(4*s.pi*G)
mass=s.integrate(4*s.pi*r*r*rho,(r,0,R))
assert s.simplify(mass-2*A*c*c*R/G)==0
flux_mass=-c*c/(4*s.pi*G)*4*s.pi*R*R*s.diff(inside,r).subs(r,R)
assert s.simplify(mass-flux_mass)==0
assert s.simplify(mass.subs(A,2*A)-2*mass)==0
for m,E,p in [(1,s.Rational(1),s.Rational(0)),(4,s.Rational(5,2),s.Rational(-3,2))]:
    assert E+p==1 and E*E-p*p==m and E>0

out={"status":"PASS_WITH_SCOPE","created_utc":datetime.now(timezone.utc).isoformat(),
     "report":{"path":str(report_path),"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw)},
     "source_pins":pins,"source_count":len(pins),
     "algebra_checks":{"quartic_stationary_radial":True,"omitted_constant_at_v":True,
       "sextic_stationary_radial":True,"potential_scaling_curvature":True,
       "clock_profile_C1_matching":True,"clock_profile_laplacians":True,
       "clock_profile_mass_gauss":True,"clock_amplitude_nonselection":True,
       "two_positive_mass_shells_same_tau":True},
     "scope":"Verificação local do autor por SymPy e hashes. Não é revisão independente, compilação Lean, seleção do kernel físico, teste empírico ou aceite. As famílias condicionais não são afirmadas como soluções de toda a teoria."}
dest=base/"MASS_VERIFICATION.json"
assert not dest.exists()
encoded=json.dumps(out,ensure_ascii=False,indent=2).encode("utf-8")
tmp=base/"MASS_VERIFICATION.json.tmp"
with tmp.open("xb") as f: f.write(encoded)
assert tmp.read_bytes()==encoded
os.replace(tmp,dest)
print(json.dumps({"status":out["status"],"path":str(dest),"sha256":hashlib.sha256(encoded).hexdigest(),"sources":len(pins)},ensure_ascii=False))
