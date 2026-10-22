"""Independent spectral/resolvent checks. Finite regulators, not QFT evidence."""
from pathlib import Path
import datetime, hashlib, json, os
import numpy as np

ROOT=Path(__file__).resolve().parent
rows=[]

def check(name, residual, limit=2e-10):
    value=float(residual)
    assert np.isfinite(value) and value<=limit,(name,value,limit)
    rows.append(dict(name=name,value=value,limit=limit,passed=True))

def hermitian_function(matrix, function):
    vals,vectors=np.linalg.eigh(matrix)
    return (vectors*function(vals))@vectors.conj().T

def log_density(matrix):
    vals=np.linalg.eigvalsh(matrix)
    if not np.all(vals>0):raise ValueError('Density must be faithful')
    if not np.allclose(matrix,matrix.conj().T,atol=1e-13):
        raise ValueError('Density must be Hermitian')
    if not np.isclose(np.trace(matrix),1,atol=1e-13):
        raise ValueError('Density must be normalized')
    return hermitian_function(matrix,np.log)

def faithful_density(rng,n):
    a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    a=a@a.conj().T+np.eye(n)
    return a/np.trace(a)

def resolvent_integral(rho,sigma,order=192):
    nodes,weights=np.polynomial.legendre.leggauss(order)
    result=np.zeros_like(rho)
    for node,weight in zip(nodes,weights):
        x=(node+1)/2
        u=x/(1-x)
        identity=np.eye(len(rho))
        left=np.linalg.inv(rho+u*identity)
        right=np.linalg.inv(sigma+u*identity)
        # Stable resolvent identity: A^-1 - B^-1 = A^-1(B-A)B^-1.
        result+=weight/(2*(1-x)**2)*(left@(sigma-rho)@right)
    return result

def derivative_integral(rho,direction,order=192):
    nodes,weights=np.polynomial.legendre.leggauss(order)
    result=np.zeros_like(rho)
    for node,weight in zip(nodes,weights):
        x=(node+1)/2
        u=x/(1-x)
        inverse=np.linalg.inv(rho+u*np.eye(len(rho)))
        result-=weight/(2*(1-x)**2)*(inverse@direction@inverse)
    return result

rng=np.random.default_rng(20260916)
for n in [2,3,5]:
    rho=faithful_density(rng,n)
    sigma=faithful_density(rng,n)
    probe=faithful_density(rng,n)
    lr,ls=log_density(rho),log_density(sigma)
    remainder=ls-lr
    check(f'{n}:decomposition',np.linalg.norm(-lr-(-ls+remainder)))
    check(f'{n}:resolvent',np.linalg.norm(resolvent_integral(rho,sigma)-remainder))
    check(f'{n}:selfadjoint',np.linalg.norm(remainder-remainder.conj().T))
    assert np.linalg.norm(rho@sigma-sigma@rho)>1e-4
    for s,t in [(0.23,-0.41),(0.8,0.3)]:
        power=lambda log,time:hermitian_function(log,lambda x:np.exp(1j*time*x))
        cocycle=lambda time:power(lr,time)@power(ls,-time)
        alpha=lambda time,a:power(ls,time)@a@power(ls,-time)
        u=cocycle(s)
        check(f'{n}:cocycle:{s}',np.linalg.norm(cocycle(s+t)-u@alpha(s,cocycle(t))))
        check(f'{n}:intertwining:{s}',np.linalg.norm(u@alpha(s,probe)@u.conj().T-
              power(lr,s)@probe@power(lr,-s)))
    eps=1e-5
    direction=probe-rho
    difference=(-log_density(rho+eps*direction)+log_density(rho-eps*direction))/(2*eps)
    check(f'{n}:first_variation',np.linalg.norm(difference-derivative_integral(rho,direction)),2e-7)
    entropy=lambda state:-np.trace(state@log_density(state))
    relative=np.trace(probe@(log_density(probe)-lr))
    expected=relative+entropy(probe)-entropy(rho)-np.trace((probe-rho)@(-ls))
    check(f'{n}:entropy_remainder',abs(np.trace((probe-rho)@remainder)-expected))
    eigs=np.linalg.eigvalsh(remainder)
    assert eigs[0]<0<eigs[-1],eigs
    rows.append(dict(name=f'{n}:mixed_sign_residual',eigenvalues=eigs.tolist(),passed=True))

# Exact leakage control: zero compressed generator, nontrivial full evolution.
p=np.diag([1.,0.]).astype(complex)
r=np.array([[0,1],[1,0]],complex)
u=hermitian_function(r,lambda x:np.exp(-1j*np.pi*x/2))
check('zero_compressed_generator',np.linalg.norm(p@r@p))
check('leakage_at_pi_over_two',np.linalg.norm(u@p@u.conj().T-(np.eye(2)-p)))
assert np.linalg.norm(u@p@u.conj().T-p)>1

# A real rank-two invariant corner, not a scalar-only rank-one corner.
p=np.diag([1,1,0]).astype(complex)
u=np.diag(np.exp(1j*np.array([0.37,0.37,-0.8])))
x=np.array([[2,1+2j,0],[1-2j,4,0],[0,0,0]],complex)
check('rank_two_scalar_phase_corner',np.linalg.norm(u@x@u.conj().T-x))
bad=np.diag(np.exp(1j*np.array([0.37,0.8,-0.8])))
assert np.linalg.norm(bad@x@bad.conj().T-x)>0.1

# The equality being tested changes when the cocycle is merely internal.
rho=np.diag([0.75,0.25]).astype(complex)
sigma=np.eye(2,dtype=complex)/2
lr,ls=log_density(rho),log_density(sigma)
u=hermitian_function(lr,lambda x:np.exp(0.4j*x))@hermitian_function(ls,lambda x:np.exp(-0.4j*x))
assert np.linalg.norm(u@r@u.conj().T-r)>0.1

# Negative controls on the proposed identities.
rho=faithful_density(rng,3);sigma=faithful_density(rng,3)
good=log_density(sigma)-log_density(rho)
assert np.linalg.norm(resolvent_integral(rho,sigma)+good)>0.1
for invalid in [np.diag([1.,0.]),np.eye(2),np.diag([1.1,-0.1])]:
    try:log_density(invalid.astype(complex))
    except ValueError:continue
    raise AssertionError('Invalid density accepted')

result={'scope':'Finite regulator checks; no physical diamond state supplied',
        'timestamp':datetime.datetime.now().astimezone().isoformat(),
        'numpy':np.__version__,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'checks':rows,'negative_controls':'wrong resolvent sign, noncentral internal action, leakage, invalid densities refused',
        'physical_modular_geometricity_proved':False}
out=ROOT/'NUMERICAL_CHECKS.json'
assert not out.exists()
tmp=out.with_suffix('.json.tmp');data=json.dumps(result,indent=2).encode('utf8')
tmp.write_bytes(data);assert tmp.read_bytes()==data;os.replace(tmp,out)
print(json.dumps({'checks':len(rows),'all_passed':True,'output':str(out)}))
