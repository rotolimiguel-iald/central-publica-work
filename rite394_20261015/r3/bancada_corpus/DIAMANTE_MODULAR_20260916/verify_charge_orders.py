"""Finite algebraic controls for stress variation and the fixed-slice charge."""
from datetime import datetime
import cmath
import hashlib
import json
import os
from pathlib import Path
import tempfile
import numpy as np

ROOT=Path(__file__).resolve().parent


def stress(g,w,c):
    return c*(w-np.trace(np.linalg.solve(g,w))*g/2)


def main():
    rng=np.random.default_rng(731)
    rows=[]
    for a,c in ((0.9,0.7),(1.3,2.),(1.8,1.1)):
        g=a*a*np.diag([1.,-1.,-1.,-1.])
        w=np.diag([0.,1.,1.,1.])
        h=rng.normal(size=(4,4)); h=(h+h.T)/2
        h[1:,1:]-=np.eye(3)*np.trace(h[1:,1:])/3
        step=1e-5
        measured=(stress(g+step*h,w,c)-stress(g-step*h,w,c))/(2*step)
        expected=3*c*h/(2*a*a)
        residual=float(np.linalg.norm(measured-expected)/np.linalg.norm(expected))
        assert residual<2e-8
        t=rng.normal(size=(3,3)); t=(t+t.T)/2
        t-=np.eye(3)*np.trace(t)/3
        t/=np.linalg.norm(t)
        def integrand(epsilon):
            spatial=np.eye(3)+epsilon*t
            return np.trace(np.linalg.inv(spatial))*np.sqrt(np.linalg.det(spatial))
        coefficient=np.trace(t@t)/4
        errors=[]
        for eps in (.01,.005):
            observed=(integrand(eps)+integrand(-eps)-6)/(2*eps**2)
            errors.append(float(abs(observed-coefficient)))
        assert errors[1]<2e-5 and 3.8<errors[0]/errors[1]<4.2
        wrong=np.trace(t@t)
        assert abs(observed-wrong)>.7  # omission of measure visibly rejected
        rows.append(dict(a=a,c=c,linear_stress_relative_residual=residual,
                         charge_coefficient=float(coefficient),expansion_errors=errors,
                         wrong_without_measure=float(wrong)))
    # Weyl product exact scalar phase bookkeeping; no false finite-dimensional CCR.
    v=np.array([.7,-.4]); f=np.array([.3,.8]); s=.23
    sigma=lambda x,y: float(x[0]*y[1]-x[1]*y[0])
    via_products=cmath.exp(-.5j*sigma(s*v,f)) * cmath.exp(-.5j*sigma(s*v+f,-s*v))
    expected=cmath.exp(-1j*s*sigma(v,f))
    assert abs(via_products-expected)<1e-14
    gaussian=np.exp(-float(f@f)/4)
    displacement=float(abs(expected*gaussian-gaussian))
    assert displacement>.05
    result=dict(timestamp=datetime.now().astimezone().isoformat(),status='PASS',
                scope='ALGEBRAIC_CONTROLS_NOT_RENORMALIZED_CHARGE',rows=rows,
                weyl_phase_residual=abs(via_products-expected),
                centered_state_change=displacement,
                false_state_invariance='REJECTED_FOR_NONZERO_SYMPLECTIC_PAIRING',
                sources=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                         for p in (Path(__file__),ROOT/'CARGA_RELACIONAL_E_ORDEM_DOS_CAMPOS.md')])
    data=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    fd,tmp=tempfile.mkstemp(dir=ROOT,suffix='.tmp')
    with os.fdopen(fd,'wb') as stream: stream.write(data)
    assert Path(tmp).read_bytes()==data
    output=ROOT/'CHARGE_ORDER_CHECKS.json'
    os.replace(tmp,output)
    print(json.dumps(dict(status='PASS',metric_profiles=len(rows),output=str(output))))


if __name__=='__main__':
    main()
