from pathlib import Path
from datetime import datetime, timezone
import sympy as sp
import json, os, hashlib

OUT = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
assert OUT.is_relative_to(ROOT)
checks=[]
def zero(name, expression):
    value=sp.trigsimp(sp.simplify(expression))
    checks.append({'name':name,'passed':value==0,'residual':str(value)})
    assert value==0, (name,value)

a,b1,b2,kappa=sp.symbols('a b1 b2 kappa',positive=True)
g=sp.diag(1,-a*a,-a*a,-a*a)
ginv=g.inv()
w=sp.diag(0,1,1,1)
q=sp.trace(ginv*w)
w2=sp.trace(ginv*w*ginv*w)
lag=b1*q*q+b2*w2
t4=4*b1*q*w+4*b2*w*ginv*w-g*lag
B=3*b1+b2
zero('quartic_trace',sp.trace(ginv*t4))
zero('quartic_density',t4[0,0]+3*B/a**4)
zero('quartic_spatial_pressure',t4[1,1]+B/a**2)
H=sp.symbols('H',real=True)
rho=-3*B/a**4
pressure=-B/a**4
zero('quartic_continuity',sp.diff(rho,a)*a*H+3*H*(rho+pressure))
r,d=sp.symbols('r d',real=True)
y=2+2*d*sp.cos(r)
kb=1-d*d
zero('corrected_first_friedmann',sp.diff(y,r)**2-(4*y-y*y-4*kb))
h=sp.diff(y,r)/(2*y)
zero('corrected_spatial_equation',sp.diff(h,r)+1/y-2*kb/y**2)
zero('uncorrected_limit',y.subs(d,1)-4*sp.cos(r/2)**2)
zero('static_endpoint_first_equation',(4*y-y*y-4*kb).subs(d,0))

raw=Path(__file__).read_bytes()
result={'status':'PASS_EXACT_QUARTIC_SOURCE_AND_BACKGROUND__NOT_LEAN','created_utc':datetime.now(timezone.utc).isoformat(),'sympy_version':sp.__version__,'checks':checks,'check_count':len(checks),'source':{'path':Path(__file__).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},'scope':'Exact algebraic contractions and FRW equations for chosen local quartic classical action. Not a complete quantum expectation/backreaction or ultraviolet result.','um_executed_or_imported':False,'originals_modified':False,'lean_executed':False}
p=OUT/'VERIFICACAO_FONTE_QUARTICA.json'
assert not p.exists()
tmp=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
data=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
with tmp.open('xb') as f:
    f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data
tmp.rename(p)
assert p.read_bytes()==data
print(json.dumps({'status':result['status'],'checks':len(checks),'receipt':p.as_posix()},ensure_ascii=True))
