from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations
import hashlib,json,os
import sympy as S
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt')
OUT=ROOT/'CONTROLE_WEYL_PONTUAL_078_20260910'
OUT.mkdir(exist_ok=False)
u,v=S.symbols('u v',real=True)
eps=[1,-1,-1,-1]
# D_abcd = partial_c partial_d gamma_ab at the proposed point.
D={}
def setd(a,b,c,d,value):
    for x,y in [(a,b),(b,a)]:
        for r,s in [(c,d),(d,c)]:D[x,y,r,s]=value
setd(1,1,3,3,u)
setd(2,2,3,3,-u)
setd(1,2,0,3,v)
def dd(a,b,c,d):return D.get((a,b,c,d),S.Integer(0))
def R(a,b,c,d):return S.Rational(1,2)*(dd(a,d,b,c)+dd(b,c,a,d)-dd(a,c,b,d)-dd(b,d,a,c))
Ric=S.Matrix(4,4,lambda b,d:sum(eps[a]*R(a,b,a,d) for a in range(4)))
scalar=sum(eps[a]*Ric[a,a] for a in range(4))
eta=S.diag(*eps)
P=(Ric-scalar*eta/6)/2
def g(a,b):return eps[a] if a==b else 0
def W(a,b,c,d):return S.expand(R(a,b,c,d)-g(a,c)*P[b,d]+g(a,d)*P[b,c]+g(b,c)*P[a,d]-g(b,d)*P[a,c])
checks=[]
def check(n,c):
    checks.append({'name':n,'passed':bool(c)});assert c,n
for b in range(4):
    for d in range(4):
        check('weyl_trace_'+str((b,d)),S.expand(sum(eps[a]*W(a,b,a,d) for a in range(4)))==0)
total=0
for a in range(4):
    for b in range(4):
        for c,d in combinations(range(4),2):
            for e,f in combinations(range(4),2):
                labels=(c,d,e,f)
                if len(set(labels))!=4:continue
                sign=(-1)**sum(labels[i]>labels[j] for i in range(4) for j in range(i+1,4))
                total+=sign*eps[a]*W(a,b,c,d)*eps[b]*W(b,a,e,f)
total=S.expand(total)
check('pontryagin_formula',total==-2*u*v)
record={'status':'PASS_EXACT_ALGEBRAIC_WEYL_POINT_CONTROL',
'created_utc':datetime.now(timezone.utc).isoformat(),
'metric':eps,'independent_second_derivatives':{'gamma11_zz':'u','gamma22_zz':'-u','gamma12_tau_z':'v'},
'curvature_convention':'R_abcd=1/2(gamma_ad,bc+gamma_bc,ad-gamma_ac,bd-gamma_bd,ac)',
'ricci':[[str(Ric[i,j]) for j in range(4)] for i in range(4)],'scalar':str(scalar),
'trace_weyl_wedge_weyl':str(total),'substitution':'u=2/z0, v=k gives -4*k/z0',
'checks':checks,'checks_total':len(checks),'new_lean_compilations':0,
'limits':'Pointwise algebraic curvature only. Does not prove linearized Einstein solution, complete jet evaluation map, BRST non-exactness or an obstruction to arbitrary higher lifts. Stage078, excluded from delivery077.',
'source':{'path':Path(__file__).as_posix(),'bytes':len(Path(__file__).read_bytes()),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
data=(json.dumps(record,ensure_ascii=False,indent=2)+'\n').encode()
target=OUT/'RESULTADO_WEYL_PONTUAL_078.json'
temp=target.with_suffix('.tmp')
with temp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
assert temp.read_bytes()==data;temp.rename(target);assert target.read_bytes()==data
print(json.dumps({'result':str(target),'pontryagin':str(total),'checks':len(checks),'sha256':hashlib.sha256(data).hexdigest()}))

