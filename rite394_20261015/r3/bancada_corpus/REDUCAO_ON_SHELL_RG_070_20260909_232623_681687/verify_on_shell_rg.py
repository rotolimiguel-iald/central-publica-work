from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os
import sympy as sp
ROOT = Path(__file__).resolve().parent
INPUT_PINS = [{'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\CALOR_COMPLETO_EINSTEIN_SIGMA_069_20260909_224252_371553\\COEFICIENTE_COMPLETO_UMA_VOLTA.md', 'bytes': 21867, 'sha256': 'ab4da8232fb0b55b33deed79b82fbe99f2a01ce895332d7e585f53925ac5b4e2'}, {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\RENORMALIZACAO_SIGMA_EFT_20260909\\FONTE_QUARTICA_E_HABITANTE_CORRIGIDO.md', 'bytes': 6747, 'sha256': '8b0eff1630bc2c7164900501e62acfd3233846898c2b5fa1f3e2e008345fa516'}, {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909\\TERMO_QUARTICO_NAO_ABSORVIDO.md', 'bytes': 6037, 'sha256': '8571a9d2882e46d3ad6889d46e308a2a76c76275db4a68049a52d2b6c0cd8b61'}]
def pin(path):
    path=Path(path); data=path.read_bytes()
    return {'path':str(path),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
for expected in INPUT_PINS:
    if pin(expected['path']) != expected:
        raise RuntimeError('Input pin changed: '+expected['path'])
checks=[]
def check(name, expression):
    residual=sp.factor(sp.expand(expression))
    checks.append({'name':name,'passed':residual==0,'residual':str(residual)})
s, lam, q, w2, ric2, rm2, r, rw, b2, boxq, boxr, tt = sp.symbols('s Lambda Q W2 Ric2 Riem2 R RicW B2 BoxQ BoxR uDtau')
eu, e, e2, ew, boxe, div_utau, tau2 = sp.symbols('Euler e E2 EW BoxE div_u_tau tau2')
x,K,ai,t,cutlog=sp.symbols('x K ai t cutoff_log')
R=sp.Rational
c42=R(43,72)*rm2-R(37,72)*ric2-R(31,144)*r**2+r*q/6+s*rw/6+(5*s+1)*q**2/6+(9*s**2-5*s+2)*w2/6+s*b2/6-boxr/6+(2-s)*boxq/12
c43=R(43,72)*rm2-R(37,72)*ric2-R(31,144)*r**2+r*q/6+(s+R(1,6))*q**2+(R(3,2)*s**2-s+R(1,3))*w2-boxr/6+boxq/6
bochner=boxq/2-rw+q**2-w2-tt
check('off_shell_bochner_difference',c42.subs(b2,bochner)-c43+s*tt/6)
geo=R(43,72)*eu+R(15,8)*ric2-R(13,16)*r**2+r*q/6+(s+R(1,6))*q**2+(R(3,2)*s**2-s+R(1,3))*w2-boxr/6+boxq/6
check('Euler_reduction',c43.subs(rm2,eu+4*ric2-r**2)-geo)
a0=-R(11,2)*lam**2
aq=lam*(R(2,3)-R(11,4)*s)
a1=-R(13,16)*s**2+R(7,6)*s+R(1,6)
a2=R(27,8)*s**2-s+R(1,3)
ae=R(43,72)
red=ae*eu+a0+aq*q+a1*q**2+a2*w2
on_shell={ric2:4*lam**2+2*lam*s*q+s**2*w2,r:4*lam+s*q,boxr:s*boxq}
check('general_on_shell_reduction',geo.subs(on_shell,simultaneous=True)-red-(1-s)*boxq/6)
ric_off=4*lam**2+2*lam*s*q+s**2*w2+2*s*ew-(2*lam+s*q)*e+e2
r_off=4*lam+s*q-e
metric_defect=R(15,4)*s*ew+(R(11,4)*lam-(s/4+R(1,6))*q)*e+R(15,8)*e2-R(13,16)*e**2
check('metric_EOM_certificate',geo.subs({ric2:ric_off,r:r_off,boxr:s*boxq-boxe},simultaneous=True)-red-(1-s)*boxq/6-boxe/6-metric_defect)
full=c42.subs(b2,bochner).subs(rm2,eu+4*ric2-r**2).subs({ric2:ric_off,r:r_off,boxr:s*boxq-boxe,tt:div_utau-tau2},simultaneous=True)
current=(1-s)*boxq/6+boxe/6-s*div_utau/6
check('full_EOM_plus_divergence_certificate',full-red-current-metric_defect-s*tau2/6)
ab=3*a1+a2
check('general_FRW_combination',ab-(R(15,16)*s**2+R(5,2)*s+R(5,6)))
check('physical_A1',a1.subs(s,4)+R(49,6))
check('physical_A2',a2.subs(s,4)-R(151,3))
check('physical_AB',ab.subs(s,4)-R(155,6))
background={s:4,lam:R(3,4),q:-3*x,w2:3*x**2,eu:R(3,2)-12*x,boxq:-R(3,2)*x}
physical_full=(red+(1-s)*boxq/6).subs(background,simultaneous=True)
check('FRW_recovers_original_C4',physical_full-(7440*x**2+1616*x-211)/96)
check('FRW_reduced_divergence',((1-s)*boxq/6).subs(background,simultaneous=True)-3*x/4)
check('FRW_quartic_coefficient',sp.expand(physical_full).coeff(x,2)-R(155,2))
gE=sp.Function('gE')(t)
gL=sp.Function('gL')(t)
bareE=gE+K*ai*(cutlog-2*t)
bareL=gL-K*ai*(cutlog-2*t)
check('Euclidean_bare_scale_independence',sp.diff(bareE,t).subs(sp.diff(gE,t),2*K*ai))
check('Lorentzian_bare_scale_independence',sp.diff(bareL,t).subs(sp.diff(gL,t),-2*K*ai))
check('FRW_Lorentzian_B_slope',(-2*K*ab).subs(s,4)+R(155,3)*K)
check('FRW_Lorentzian_local_density_slope',-3*x**2*(-2*K*ab).subs(s,4)-155*K*x**2)
for expected in INPUT_PINS:
    if pin(expected['path']) != expected:
        raise RuntimeError('Input changed during symbolic checks')
result={'status':'PASS_EXACT_ON_SHELL_RG_REDUCTION__NOT_LEAN' if all(c['passed'] for c in checks) else 'FAIL_EXACT_REDUCTION','created_utc':datetime.now(timezone.utc).isoformat(),'sympy_version':sp.__version__,'check_count':len(checks),'checks':checks,'coefficients':{'Euler':str(ae),'constant':str(a0),'Q':str(aq),'Q2':str(a1),'W2':str(a2),'B_3A1_plus_A2':str(sp.factor(ab)),'remaining_divergence':str((1-s)*boxq/6)},'input_pins':INPUT_PINS,'inputs_unchanged':True,'script':pin(__file__),'scope':'New exact algebraic controls of the reduction of the already derived C4 polynomial, EOM/divergence certificate, and RG convention. Input Einstein/Bochner identities are not newly tensor-compiled. No rerun of the 31 previous operator CAS checks.','execution':{'lean':False,'um_py_imported':False,'um_py_executed':False,'existing_files_modified':False}}
target=ROOT/'VERIFICACAO_REDUCAO_RG.json'
if target.exists():raise FileExistsError(target)
data=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
tmp=target.with_name(target.name+'.tmp')
with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
if tmp.read_bytes()!=data:raise RuntimeError('temporary receipt verification')
if target.exists():raise FileExistsError(target)
tmp.rename(target)
if target.read_bytes()!=data:raise RuntimeError('receipt verification')
print(json.dumps({'status':result['status'],'check_count':len(checks),'failed':[c for c in checks if not c['passed']],'receipt':pin(target)},ensure_ascii=True))
if not all(c['passed'] for c in checks):raise SystemExit(1)
