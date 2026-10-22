"""Synthetic convention checks for an explicit massless helicity pair; no data."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import sys
import time

OUT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REDE\continuum')
OUT.mkdir(exist_ok=True)

def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}

def new(name, obj):
    p=OUT/name
    if p.exists(): raise FileExistsError(p)
    b=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:
        f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b
    os.rename(t,p)
    return pin(p)

if sys.argv[1]=='freeze':
    print(new('PREREGISTRO_WIGNER_R1.json',{
        'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'script':pin(Path(__file__)), 'seed':20261013, 'samples':128,
        'absolute_tolerance':1e-9,'negative_control_min_gap':1e-4,
        'parameters':'rho=exp(uniform(-1,1)), r=uniform(-1,1), phi=uniform(-pi,pi); random spatial rotations and rapidities in [-0.7,0.7]. Reference momentum unit=1 INPUT.',
        'checks':['section','Lorentz','little_group','little_rotation_unitarity','cocycle','Poincare_product','boost_cocycle','halfturn_cocycle','J_square','J_translations','J_Lorentz','measure_jacobian'],
        'negative_control':'Conjugation plus helicity swap without q reflection must fail the jW translation law for generic transverse a.',
        'scope':'Finite synthetic numerical checks, not global proof, Lean proof, hardware or nature evidence. No beta adjustment: massless representation kinematics does not contain beta.',
        'falsifier':'Any listed residual above tolerance or negative control not detected.'}))
    sys.exit(0)

assert sys.argv[1]=='run'
import numpy as np
spec_path=OUT/'PREREGISTRO_WIGNER_R1.json'
spec=json.loads(spec_path.read_text(encoding='utf-8'))
assert spec['script']==pin(Path(__file__))
if (OUT/'RESULTADO_WIGNER_R1.json').exists():raise FileExistsError('result exists')
start=dt.datetime.now(dt.timezone.utc);clock=time.perf_counter()
rng=np.random.default_rng(spec['seed'])
eta=np.diag([1.,-1.,-1.,-1.]);k=np.array([1.,0.,0.,1.])
halfturn=np.diag([1.,1.,-1.,-1.]);jw=-halfturn
swap=np.array([[0.,1.],[1.,0.]])
res={x:0. for x in spec['checks']}

def measure(name,a,b):
    value=float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    if not np.isfinite(value):raise ValueError(name)
    res[name]=max(res[name],value)

def boost(s,direction):
    n=np.asarray(direction,dtype=float);n=n/np.linalg.norm(n)
    c=np.cosh(s);z=np.sinh(s);b=np.eye(4)
    b[0,0]=c;b[0,1:]=z*n;b[1:,0]=z*n
    b[1:,1:]+=(c-1)*np.outer(n,n)
    return b

def rotation(phi,n):
    n=np.asarray(n,dtype=float);n=n/np.linalg.norm(n)
    x,y,z=n
    cross=np.array([[0.,-z,y],[z,0.,-x],[-y,x,0.]])
    r=np.eye(4);r[1:,1:]=np.cos(phi)*np.eye(3)+(1-np.cos(phi))*np.outer(n,n)+np.sin(phi)*cross
    return r

def section(p):
    rho=np.linalg.norm(p[2:]);r=np.arcsinh(p[1]/rho)
    phi=np.arctan2(-p[2],p[3])
    return boost(r,[1,0,0])@rotation(phi,[1,0,0])@boost(np.log(rho),[0,0,1])

def cocycle(L,p):
    return np.linalg.solve(section(p),L@section(np.linalg.solve(L,p)))

def character(c):
    z=c[1,1]+1j*c[2,1]
    return np.diag([z,np.conj(z)])

def action(a,L,f,p):
    return np.exp(1j*(a@eta@p))*character(cocycle(L,p))@f(np.linalg.solve(L,p))

def field(p):
    return np.exp(-p[0])*np.array([p[1]+1j*p[2],p[3]+.2+.7j])

def J(f,p): return swap@np.conj(f(halfturn@p))
def Jold(f,p): return swap@np.conj(f(p))
negative_gap=0.
for _ in range(spec['samples']):
    rho=np.exp(rng.uniform(-1,1));r=rng.uniform(-1,1);phi=rng.uniform(-np.pi,np.pi)
    p=np.array([rho*np.cosh(r),rho*np.sinh(r),-rho*np.sin(phi),rho*np.cos(phi)])
    L1=boost(rng.uniform(-.7,.7),rng.normal(size=3))@rotation(rng.uniform(-np.pi,np.pi),rng.normal(size=3))
    L2=boost(rng.uniform(-.7,.7),rng.normal(size=3))@rotation(rng.uniform(-np.pi,np.pi),rng.normal(size=3))
    a=rng.normal(size=4);b=rng.normal(size=4)
    measure('section',section(p)@k,p)
    measure('Lorentz',L1.T@eta@L1,eta)
    c=cocycle(L1,p)
    measure('little_group',c@k,k)
    measure('little_rotation_unitarity',character(c).conj().T@character(c),np.eye(2))
    measure('cocycle',cocycle(L1@L2,p),c@cocycle(L2,np.linalg.solve(L1,p)))
    measure('Poincare_product',action(a,L1,lambda x:action(b,L2,field,x),p),action(a+L1@b,L1@L2,field,p))
    measure('boost_cocycle',cocycle(boost(rng.uniform(-.7,.7),[1,0,0]),p),np.eye(4))
    measure('halfturn_cocycle',cocycle(halfturn,p),np.eye(4))
    measure('J_square',J(lambda x:J(field,x),p),field(p))
    measure('J_translations',J(lambda x:action(a,np.eye(4),lambda y:J(field,y),x),p),action(jw@a,np.eye(4),field,p))
    measure('J_Lorentz',J(lambda x:action(np.zeros(4),L1,lambda y:J(field,y),x),p),action(np.zeros(4),halfturn@L1@halfturn,field,p))
    measure('measure_jacobian',rho*np.cosh(r)/p[0],1.)
    bad=Jold(lambda x:action(a,np.eye(4),lambda y:Jold(field,y),x),p)
    target=action(jw@a,np.eye(4),field,p)
    negative_gap=max(negative_gap,float(np.max(np.abs(bad-target))))
ok=all(x<=spec['absolute_tolerance'] for x in res.values()) and negative_gap>=spec['negative_control_min_gap']
result={'verdict':'PASS' if ok else 'FAIL','start_utc':start.isoformat(),'end_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'seconds':time.perf_counter()-clock,'preregistration':pin(spec_path),'script':pin(Path(__file__)),'python':sys.executable,'numpy':np.__version__,'samples':spec['samples'],'max_residuals':res,'negative_control_gap':negative_gap,'scope':spec['scope']}
print(json.dumps(new('RESULTADO_WIGNER_R1.json',result),ensure_ascii=False))
print(json.dumps(result,ensure_ascii=False))
sys.exit(0 if ok else 1)
