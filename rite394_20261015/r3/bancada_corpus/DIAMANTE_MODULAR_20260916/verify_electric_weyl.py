"""Electric Weyl checks, including a nonlinear Bianchi IX curvature control."""
import cmath
from datetime import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parent


def data(n, eta):
    lam = (n+1)**2-3
    p = math.sqrt(lam+9)
    c = 1/math.sqrt(2*p*(p*p+1))
    phase = cmath.exp(-1j*p*eta)
    t = c*(p*math.cosh(eta)-1j*math.sinh(eta))*phase
    tp = -1j*c*(p*p+1)*math.cosh(eta)*phase
    tpp = -c*(p*p+1)*(p*math.cosh(eta)+1j*math.sinh(eta))*phase
    electric = c/2*(-p*(lam+6)*math.cosh(eta)-4j*math.sinh(eta))*phase
    return lam,p,c,t,tp,tpp,electric


def nonlinear_electric(epsilon, t, tp, tpp):
    # Left-invariant unit S3 coframe, diagonal spatial metric d_i.
    # Shape (1,-1,0) is homogeneous TT with Laplace eigenvalue 6.
    shape = (1.,-1.,0.)
    d = [1+epsilon*s*t for s in shape]
    dp = [epsilon*s*tp for s in shape]
    dpp = [epsilon*s*tpp for s in shape]
    trace_rate = sum(dp[i]/d[i] for i in range(3))
    ric00 = -sum(dpp[i]/(2*d[i])-dp[i]**2/(4*d[i]**2) for i in range(3))
    ric = []
    for i in range(3):
        j,k = [v for v in range(3) if v != i]
        ric3 = 2*(d[i]**2-(d[j]-d[k])**2)/(d[j]*d[k])
        ric.append(ric3+dpp[i]/2+dp[i]*trace_rate/4-dp[i]**2/(2*d[i]))
    scalar = ric00-sum(ric[i]/d[i] for i in range(3))
    r0i0i = dpp[0]/2-dp[0]**2/(4*d[0])
    return r0i0i-(ric[0]-d[0]*ric00)/2-scalar*d[0]/6


def main():
    rows=[]
    for n in (2,5,10):
        for eta in (0.3,0.8,1.4):
            lam,p,c,t,tp,tpp,e = data(n,eta)
            assert abs(e-(tpp-(lam+2)*t)/4) < 1e-12
            step=1e-4
            ts=[data(n,eta+s)[3] for s in (step,0,-step)]
            second=(ts[0]-2*ts[1]+ts[2])/step**2
            electric_fd=(second-(lam+2)*t)/4
            fd_error=abs(electric_fd-e)/max(1,abs(e))
            assert fd_error < 2e-6
            a=2/math.cosh(eta)
            predicted=c*c*(p*p*(lam+6)**2+16*math.tanh(eta)**2)
            assert abs(abs(a*e)**2-predicted)/predicted < 1e-13
            def ratio(x):
                values=data(n,x)
                return abs(values[6])**2/abs(values[4])**2
            d_ratio=(ratio(eta+step)-ratio(eta-step))/(2*step)
            expected=8*math.tanh(eta)/(math.cosh(eta)**2*(p*p+1)**2)
            assert abs(d_ratio/expected-1) < 1e-5
            assert d_ratio > 0  # common scalar stationary hypothesis rejected
            curve_errors=[]
            if n==2:
                for eps in (0.002,0.001):
                    measured=(nonlinear_electric(eps,t.real,tp.real,tpp.real)-nonlinear_electric(-eps,t.real,tp.real,tpp.real))/(2*eps)
                    curve_errors.append(abs(measured-e.real))
                assert curve_errors[1] < 1e-5
                assert 3.8 < curve_errors[0]/curve_errors[1] < 4.2
            rows.append(dict(n=n,eta=eta,electric_second_difference_error=fd_error,
                             ratio_derivative=d_ratio,ratio_derivative_expected=expected,
                             nonlinear_curvature_errors=curve_errors))
    assert abs(nonlinear_electric(0,1,1,1)) < 1e-14
    result=dict(timestamp=datetime.now().astimezone().isoformat(),status='PASS',
                scope='SCOPED_LINEAR_STATE_NO_OBSERVATIONAL_DATA_NO_MODULAR_DIAGONALIZATION',
                units=dict(hbar=1,kappa=1),mode_checks=rows,
                stationary_common_weight_control='REJECTED_BY_NONCONSTANT_RATIO',
                curvature_control='NONLINEAR_BIANCHI_IX_LINEARIZATION_N2',
                sources=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                         for p in (Path(__file__),ROOT/'WEYL_ELETRICO_E_PESO_CONFORME.md',
                                   ROOT.parent/'MODOS_TENSORIAIS_EXATOS_20260909/ACAO_TT_E_MODOS_EXATOS.md')])
    output=ROOT/'ELECTRIC_WEYL_CHECKS.json'
    data_bytes=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    fd,tmp=tempfile.mkstemp(dir=ROOT,suffix='.tmp')
    with os.fdopen(fd,'wb') as stream:
        stream.write(data_bytes)
    assert Path(tmp).read_bytes()==data_bytes
    os.replace(tmp,output)
    print(json.dumps(dict(status='PASS',modes=len(rows),nonlinear_curvature_controls=3,output=str(output))))


if __name__=='__main__':
    main()
