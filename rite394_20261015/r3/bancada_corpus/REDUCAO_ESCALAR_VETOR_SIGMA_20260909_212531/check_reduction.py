"""Exact algebra checks for the written Einstein-sigma scalar/vector reduction."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sympy as s

ROOT = Path(__file__).resolve().parent
lam, D, a, H, x, xd, y, z = s.symbols("lam D a H x xd y z", real=True, nonzero=True)
kappa = s.symbols("kappa", positive=True)
checks = []


def check(name, expression):
    value = s.simplify(s.expand(expression))
    checks.append({"name": name, "residual": str(value), "pass": value == 0})
    if value != 0:
        raise AssertionError((name, value))


# Integrated unit-normalized harmonic Lagrangians, common a^3/(2*kappa) omitted.
LS = -6*H**2*z**2 + 4*H*s.sqrt(lam)*z*y - 2*y**2 + 4*(xd-y)**2 - 4*(lam-4)*x**2/a**2 + 8*s.sqrt(lam)*z*x/a**2
yS = 6*xd/(lam+3) - 2*lam*x/(H*a**2*(lam+3))
zS = 2*s.sqrt(lam)*xd/(H*(lam+3)) + 2*s.sqrt(lam)*x/(H**2*a**2*(lam+3))
check("scalar_shift_constraint", s.diff(LS, y).subs({y:yS, z:zS}))
check("scalar_lapse_constraint", s.diff(LS, z).subs({y:yS, z:zS}))
KS = 4*(lam-3)/(lam+3)
BS = 16*lam/(H*a**2*(lam+3))
CS = 8*lam/(H**2*a**4*(lam+3)) - 4*(lam-4)/a**2
LS_sub = s.simplify(LS.subs({y:yS, z:zS}))
check("scalar_constraint_substitution", LS_sub - (KS*xd**2 + BS*x*xd + CS*x**2))
# Background identities adot=aH and Hdot=-1/a^2.
weighted_B = a**3*BS
B_derivative = s.diff(weighted_B, a)*a*H + s.diff(weighted_B, H)*(-1/a**2)
check("scalar_total_derivative_and_potential", CS - B_derivative/(2*a**3) + KS*(lam+4)/a**2)
check("scalar_symplectic_momentum", 4*(xd-yS) - (KS*xd + BS*x/2))
check("scalar_l1_shift_residual_gauge", yS.subs(lam,3) - (xd-x/(H*a**2)))
check("scalar_l1_lapse_residual_gauge", zS.subs(lam,3) - (xd/(s.sqrt(3)*H)+x/(s.sqrt(3)*H**2*a**2)))
check("scalar_l1_zero_kinetic", KS.subs(lam,3))

LV = D*y**2/2 + 4*(xd-y)**2 - 4*D*x**2/a**2
yV = 8*xd/(D+8)
KV = 4*D/(D+8)
check("vector_shift_constraint", s.diff(LV,y).subs(y,yV))
check("vector_reduced_action", LV.subs(y,yV) - KV*(xd**2-(D+8)*x**2/a**2))
check("vector_symplectic_momentum", 4*(xd-yV)-KV*xd)
check("vector_killing_zero_action", LV.subs({D:0,y:xd}))

eta = s.symbols("eta", real=True)
p = s.symbols("p", real=True, positive=True)
asech = 2/s.cosh(eta)
check("conformal_scale_second_derivative", s.diff(asech,eta,2)/asech - (1-2/s.cosh(eta)**2))
f = (p-s.I*s.tanh(eta))*s.exp(-s.I*p*eta)/s.sqrt(2*p*(p**2+1))
mode_residual = s.diff(f,eta,2)+(p**2+2/s.cosh(eta)**2)*f
check("exact_positive_frequency_mode", s.trigsimp(mode_residual))
check("mode_wronskian", s.trigsimp(f*s.diff(s.conjugate(f),eta)-s.diff(f,eta)*s.conjugate(f)-s.I))
ell = s.symbols("ell", integer=True, positive=True)
check("scalar_frequency", (lam+4-1).subs(lam,ell*(ell+2))-((ell+1)**2+2))
check("vector_frequency", (D+8-1).subs(D,ell*(ell+2)-3)-((ell+1)**2+3))

report = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "PASS_EXACT_CAS_NOT_LEAN",
    "sympy_version": s.__version__,
    "check_count": len(checks),
    "checks": checks,
    "scope": "Verifies algebra of the displayed mode Lagrangians and background identities; the ADM/SVT reduction is proved in the accompanying written note, not certified by these checks alone.",
    "um_executed_or_imported": False,
    "originals_modified": False,
}
target = ROOT / "VERIFICACAO_REDUCAO.json"
if target.exists():
    raise FileExistsError(target)
payload = (json.dumps(report, ensure_ascii=False, indent=2)+"\n").encode("utf-8")
temporary = target.with_name(target.name+".new")
with temporary.open("xb") as stream:
    stream.write(payload)
    stream.flush()
    os.fsync(stream.fileno())
assert temporary.read_bytes() == payload
os.rename(temporary,target)
assert target.read_bytes() == payload
print(json.dumps({"status":report["status"],"checks":len(checks),"path":str(target),"bytes":len(payload),"sha256":hashlib.sha256(payload).hexdigest()},ensure_ascii=False,indent=2))
