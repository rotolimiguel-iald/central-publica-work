"""Exact symbolic cross-checks, not a Lean proof. Writes new files only in this folder."""
from pathlib import Path
import datetime, hashlib, json, os
import sympy as sp

ROOT = Path(__file__).resolve().parent
assert ROOT.is_relative_to(Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve())
r, chi, theta, psi = x = sp.symbols("r chi theta psi", real=True)
c = sp.symbols("c", positive=True)
a = 2*sp.cos(r/2)
h = sp.diag(1, sp.sin(chi)**2, sp.sin(chi)**2*sp.sin(theta)**2)
g = sp.diag(1, *[-a*a*h[i,i] for i in range(3)])
gi = g.inv()
z = [sp.cos(chi), sp.sin(chi)*sp.cos(theta),
     sp.sin(chi)*sp.sin(theta)*sp.cos(psi), sp.sin(chi)*sp.sin(theta)*sp.sin(psi)]
half_r = sp.symbols("half_r", real=True)

def simp(expr):
    rewritten = expr.subs(r,2*half_r).replace(sp.tan,lambda y:sp.sin(y)/sp.cos(y))
    return sp.trigsimp(sp.simplify(sp.expand_trig(rewritten))).subs(half_r,r/2)

Gm = [[[simp(sum(gi[u,l]*(sp.diff(g[l,j], x[i])+sp.diff(g[l,i], x[j])-sp.diff(g[i,j], x[l]))
                        for l in range(4))/2) for j in range(4)] for i in range(4)] for u in range(4)]
Ric = sp.Matrix(4,4,lambda b,j: simp(sum(
    sp.diff(Gm[u][j][b],x[u])-sp.diff(Gm[u][u][b],x[j])+
    sum(Gm[u][u][v]*Gm[v][j][b]-Gm[u][j][v]*Gm[v][u][b] for v in range(4))
    for u in range(4))))
R = simp(sum(gi[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
Einstein = (Ric-R*g/2).applyfunc(simp)
W = sp.Matrix(4,4,lambda i,j: simp(sum(sp.diff(f,x[i])*sp.diff(f,x[j]) for f in z)))
Q = simp(sum(gi[i,j]*W[i,j] for i in range(4) for j in range(4)))
T = (c*(W-g*Q/2)).applyfunc(simp)
mu = a**3*sp.sin(chi)**2*sp.sin(theta)
box = [simp(sum(sp.diff(mu*gi[i,i]*sp.diff(f,x[i]),x[i]) for i in range(4))/mu) for f in z]
q = sp.sin(r/2)**2
P = [q]+[(1-q)*f*f for f in z]
F = sp.Matrix(4,4,lambda i,j: simp(sum(sp.diff(p,x[i])*sp.diff(p,x[j])/p for p in P)))
expected_fisher = sp.diag(1,*[a*a*h[i,i] for i in range(3)])
expected_ricci = sp.diag(sp.Rational(3,4),*[(4-3*a*a/4)*h[i,i] for i in range(3)])
eta = sp.pi*c/2
ell = sp.Matrix(sp.symbols("ell0:4", real=True))
s_coeff = -sp.pi*c*(ell.T*W*ell)[0]
area_coeff = -(ell.T*Ric*ell)[0]/2

checks = {}
def check(name, expressions):
    residuals = [simp(e) for e in expressions]
    checks[name] = {"passed": all(e == 0 for e in residuals),
                    "residuals": [str(e) for e in residuals]}

check("probability_normalization", [sum(P)-1])
check("categorical_fisher", list(F-expected_fisher))
check("selected_clock_dual_norm", [sp.diff(q,r)**2-q*(1-q)])
check("selected_reflected_metric", list(2*sp.diag(1,0,0,0)-F-g))
check("ricci_direct_from_connection", list(Ric-expected_ricci))
check("scalar_curvature", [R-(3-12/a**2)])
check("sigma_constraint", [sum(f*f for f in z)-1])
check("constraint_first_derivative", [sum(f*sp.diff(f,xi) for f in z) for xi in x])
check("sigma_kinetic_trace", [Q+3/a**2])
check("sigma_wave_equations", [box[j]+Q*z[j] for j in range(4)])
check("multiplier_euler_equations", [-c*box[j]+3*c/a**2*z[j] for j in range(4)])
check("aggregate_stress_divergence", [sum(box[j]*sp.diff(z[j],xi) for j in range(4)) for xi in x])
check("einstein_sigma_equation", list(Einstein+sp.Rational(3,4)*g-(4/c)*T))
check("area_entropy_residual_is_null_metric_multiple", [s_coeff-eta*area_coeff-sp.Rational(3,16)*sp.pi*c*(ell.T*g*ell)[0]])
assert all(item["passed"] for item in checks.values()), checks

result = {
    "status": "PASS_EXACT_SYMBOLIC_CHECKS__NOT_LEAN",
    "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "sympy_version": sp.__version__, "domain": "0<r<pi; 0<chi,theta,psi<pi/2; c>0",
    "curvature_convention": "R^rho_(sigma mu nu)=partial_mu Gamma^rho_(nu sigma)-partial_nu Gamma^rho_(mu sigma)+commutator; Ric_sigma,nu=sum_rho R^rho_(sigma rho nu)",
    "checks": checks, "number_of_checks": len(checks),
    "ricci": str(Ric), "scalar_curvature": str(R), "stress": str(T),
    "wave_operators": [str(value) for value in box],
    "um_py_executed_or_imported": False, "lean_run": False, "original_files_modified": False
}
data=(json.dumps(result, ensure_ascii=False, indent=2)+"\n").encode("utf-8")
target=ROOT/"VERIFICACAO_SIMBOLICA.json"
assert not target.exists()
temporary=target.with_name(target.name+".tmp")
with temporary.open("xb") as handle:
    handle.write(data); handle.flush(); os.fsync(handle.fileno())
assert temporary.read_bytes()==data
os.rename(temporary,target)
print(json.dumps({"status":result["status"],"checks":len(checks),"path":target.as_posix(),
                  "bytes":len(data),"sha256":hashlib.sha256(data).hexdigest()}))
