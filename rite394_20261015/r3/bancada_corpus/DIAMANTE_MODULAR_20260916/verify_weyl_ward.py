"""Controls for the scoped Weyl Ward obstruction; no observational claim."""
from pathlib import Path
import cmath
import hashlib
import json
import math
import os
import tempfile

ROOT = Path(__file__).resolve().parent


def mode(n, eta):
    p = math.sqrt((n + 1)**2 + 6)
    a = 2 / math.cosh(eta)
    f = (p - 1j * math.tanh(eta)) * cmath.exp(-1j*p*eta)
    return 2*f/(a*math.sqrt(2*p*(p*p+1)))


def derivative(n, eta):
    p = math.sqrt((n + 1)**2 + 6)
    return -1j*math.sqrt((p*p+1)/(2*p))*math.cosh(eta)*cmath.exp(-1j*p*eta)


def covariance(n, x, y):
    return derivative(n, x)*derivative(n, y).conjugate()


def main():
    # kappa=hbar=1 are positive units for these dimensionless identity checks.
    rows = []
    for n in (2, 4, 12):
        for eta in (0.2, 0.9, 1.7):
            exact = derivative(n, eta)
            errors = []
            for step in (0.0002, 0.0001):
                numeric = (mode(n, eta+step)-mode(n, eta-step))/(2*step)
                errors.append(abs(numeric-exact)/abs(exact))
            ratio = errors[0]/errors[1]
            assert errors[1] < 1e-6 and 3.8 < ratio < 4.2
            step = 1e-5
            vp, vm = (abs(derivative(n, eta+d))**2 for d in (step, -step))
            log_slope = (math.log(vp)-math.log(vm))/(2*step)
            assert abs(log_slope-2*math.tanh(eta)) < 1e-8
            assert abs(log_slope) > 0.1  # stationary false hypothesis rejected
            y = eta+0.13
            w = covariance(n, eta, y)
            simultaneous = (covariance(n, eta+step, y+step)-covariance(n, eta-step, y-step))/(2*step)
            predicted = (math.tanh(eta)+math.tanh(y))*w
            assert abs(simultaneous-predicted)/abs(w) < 1e-8
            def rescaled(s):
                return 4*covariance(n, eta+s, y+s)/(math.cosh(eta+s)*math.cosh(y+s))
            stationary_rescaled = abs(rescaled(0.11)-rescaled(0))/abs(rescaled(0))
            assert stationary_rescaled < 1e-12
            rows.append(dict(n=n, eta=eta, derivative_relative_errors=errors,
                             convergence_ratio=ratio, log_variance_slope=log_slope,
                             rescaled_stationarity_residual=stationary_rescaled))
    # n0,z are fixed unit R4 vectors; spherical gradient h is n0-(n0.z)z.
    z = [0.5]*4
    n0 = [1.0, 0.0, 0.0, 0.0]
    centers = []
    for radius in (0.3, 0.8, 1.9, math.pi/2):
        tau = 0.27
        def vector(sign):
            n = [sign*v for v in n0]
            h = sum(x*y for x, y in zip(n, z))
            time = (math.cos(tau)*h-math.cos(radius))/math.sin(radius)
            space = [math.sin(tau)/math.sin(radius)*(x-h*y) for x,y in zip(n,z)]
            return [time]+space
        pair = [x+y for x,y in zip(vector(1),vector(-1))]
        expected = [-2/math.tan(radius), 0, 0, 0, 0]
        residual = max(abs(x-y) for x,y in zip(pair, expected))
        assert residual < 1e-14
        exceptional = radius == math.pi/2
        assert exceptional or abs(expected[0]) > 0.1
        centers.append(dict(radius=radius, residual=residual,
                            status="NOT_COVERED_EXCEPTIONAL_RADIUS" if exceptional else "ANTIPODAL_IDENTITY_CHECKED"))
    files = [Path(__file__), ROOT/'TESTE_GEOMETRICO_WEYL_ESTADO_067.md',
             ROOT.parent/'MODOS_TENSORIAIS_EXATOS_20260909/ACAO_TT_E_MODOS_EXATOS.md']
    result = dict(status="PASS", scope="IDENTITY_CONTROLS_NOT_PROOF_OF_ANALYTIC_CONTINUATION_OR_PHYSICS",
                  units=dict(kappa=1, hbar=1), modes=rows, antipodal=centers,
                  negative_control="UNWEIGHTED_STATIONARITY_REJECTED",
                  alternative_weight_control="RESCALED_MODE_STATIONARITY_PRESERVED",
                  sources=[dict(path=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files])
    output = ROOT/'WEYL_WARD_CHECKS.json'
    data = (json.dumps(result, indent=2)+'\n').encode()
    fd, tmp = tempfile.mkstemp(dir=ROOT, suffix='.tmp')
    with os.fdopen(fd, 'wb') as f:
        f.write(data)
    assert Path(tmp).read_bytes() == data
    os.replace(tmp, output)
    print(json.dumps(dict(status=result['status'], modes=len(rows), antipodal=len(centers), output=str(output))))


if __name__ == '__main__':
    main()
