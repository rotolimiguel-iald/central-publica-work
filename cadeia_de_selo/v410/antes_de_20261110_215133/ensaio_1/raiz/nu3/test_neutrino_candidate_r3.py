"""Independent synthetic review: loads candidate source only; canonical I/O is mocked."""
from pathlib import Path
import sys, importlib.util, types, json, hashlib, math, copy, datetime
import numpy as np
sys.dont_write_bytecode = True
candidate = Path(sys.argv[1]).resolve()
result_path = Path(sys.argv[2]).resolve()
if result_path.exists():
    raise FileExistsError(result_path)
raw = candidate.read_bytes()
canonical_path = candidate.with_name('canonical.py')
pkg = types.ModuleType('nu3_review_candidate'); pkg.__path__ = [str(candidate.parent)]
sys.modules[pkg.__name__] = pkg
for name, path in [('canonical', canonical_path), ('neutrino_contract', candidate)]:
    spec=importlib.util.spec_from_file_location(pkg.__name__+'.'+name,path)
    module=importlib.util.module_from_spec(spec); sys.modules[spec.name]=module; spec.loader.exec_module(module)
    if name=='neutrino_contract': target=module
alpha=7.2973525693e-3
beta=alpha*math.sqrt(math.e)
receipt={'alpha':alpha,'beta_tgl':beta,'canonical_manifest_sha256':'MOCK_CANONICAL_IDENTITY_ONLY'}
target.require_current=lambda operation: dict(receipt,operation=operation)
results=[]
def check(name, fn):
    try:
        detail=fn();results.append({'name':name,'status':'PASS','detail':detail})
    except Exception as exc:
        results.append({'name':name,'status':'FAIL','error':type(exc).__name__+': '+str(exc)})
def require(ok,message='assertion failed'):
    if not bool(ok):raise AssertionError(message)
def decode(out):
    z=np.array(out['result']['rho']);return z[...,0]+1j*z[...,1]
def call(payload):return target.simulate(payload)
def assert_close(a,b,tol=2e-12):
    residual=float(np.max(np.abs(np.asarray(a)-np.asarray(b))));require(residual<tol,str(residual));return residual
def invariant_result(payload):
    out=call(payload);rho=decode(out)
    require(out['synthetic'] is True and out['nature_sigma'] is None and out['data_opened'] is False and out['gate_effect']=='NONE')
    require(abs(np.trace(rho)-1)<2e-12)
    require(np.max(np.abs(rho-rho.conj().T))<2e-12)
    require(np.linalg.eigvalsh(rho).min()>-2e-12)
    return out,rho
def rk4(rho, duration, derivative, steps=1600):
    dt=duration/steps;rho=rho.copy()
    for _ in range(steps):
        a=derivative(rho);b=derivative(rho+dt*a/2);c=derivative(rho+dt*b/2);d=derivative(rho+dt*c)
        rho +=dt*(a+2*b+2*c+d)/6
    return rho
r4=np.zeros((4,4),complex);r4[0,0]=1
boundary={'channel':'boundary_parity_4state','s':0.73,'rho':target.encode(r4)}
def boundary_exact():
    out,rho=invariant_result(boundary)
    p=(1-math.exp(-1.46))/2
    expected=np.diag([1-p,0,p,0]);return assert_close(rho,expected)
check('boundary_analytic_occupation',boundary_exact)
def boundary_rk():
    state=np.array([1,1j,-2,0.4j]);state/=np.linalg.norm(state);rho=np.outer(state,state.conj())
    p=dict(boundary,rho=target.encode(rho));out,evolved=invariant_result(p)
    x=np.kron([[0,1],[1,0]],np.eye(2));expected=rk4(rho,p['s'],lambda r:x@r@x-r)
    q=np.diag([0,1,0,1]);require(abs(np.trace(q@rho)-np.trace(q@evolved))<2e-12)
    return assert_close(evolved,expected)
check('boundary_rk4_and_charge_conservation',boundary_rk)
def boundary_semigroup():
    first=call(dict(boundary,s=0.2));second=call(dict(boundary,s=0.53,rho=first['result']['rho']))
    return assert_close(decode(second),decode(call(boundary)))
check('boundary_semigroup',boundary_semigroup)
check('boundary_zero_time',lambda:assert_close(decode(call(dict(boundary,s=0))),r4))
def tiny_s():
    out=call(dict(boundary,s=1e-40));p=out['result']['flip_probability'];require(p>0);return assert_close(p/1e-40,1,1e-14)
check('boundary_expm1_tiny_positive',tiny_s)
check('boundary_large_time',lambda:assert_close(call(dict(boundary,s=1e300))['result']['flip_probability'],0.5))
state=np.array([1,1j,2],complex);state/=np.linalg.norm(state);rho=np.outer(state,state.conj())
physical={'channel':'physical_mass_gap_dephasing','mass_squared_eV2':[0,7.5e-5,2.5e-3],'energy_eV':4e6,'tau_star_s':1e-5,'Kfac':1.0,'time_s':2e-6,'rho':target.encode(rho)}
def physical_rk():
    out,got=invariant_result(physical);h=np.diag(np.array(physical['mass_squared_eV2'])/(2*physical['energy_eV']))
    hbar=6.582119569e-16
    lop=math.sqrt(beta*physical['tau_star_s']*physical['Kfac'])*h/hbar
    lsq=lop@lop
    def deriv(r):return -1j*(h@r-r@h)/hbar+lop@r@lop-(lsq@r+r@lsq)/2
    expected=rk4(rho,physical['time_s'],deriv)
    require(abs(np.trace(h@got)-np.trace(h@rho))<1e-24)
    return assert_close(got,expected,2e-12)
check('physical_direct_GKSL_RK4_and_energy',physical_rk)
def slope():
    g1=np.array(call(physical)['result']['gamma']);g2=np.array(call(dict(physical,energy_eV=8e6))['result']['gamma'])
    return assert_close(g1[0,1]/g2[0,1],4)
check('physical_E_inverse_square',slope)
def gamma_units():
    out=call(physical);g=np.array(out['result']['gamma']);delta=7.5e-5/(2*4e6)
    gamma_eV=0.5*beta*(1e-5/6.582119569e-16)*delta**2
    require(out['result']['gamma_units']=='s^-1')
    return assert_close(g[0,1]*6.582119569e-16/gamma_eV,1)
check('physical_natural_to_SI_units',gamma_units)
def texture():
    g=np.array(call(physical)['result']['gamma'])
    return assert_close([g[0,2]/g[0,1],g[1,2]/g[0,1]],[(2.5e-3/7.5e-5)**2,((2.5e-3-7.5e-5)/7.5e-5)**2],5e-12)
check('physical_linked_rate_texture',texture)
def tau_zero():
    out,got=invariant_result(dict(physical,tau_star_s=0));require(np.array(out['result']['gamma']).max()==0)
    return assert_close(np.trace(got@got),1)
check('physical_tau_zero_is_unitary',tau_zero)
def physical_diag():
    d=np.diag([0.2,0.3,0.5]);out,got=invariant_result(dict(physical,rho=target.encode(d)))
    return assert_close(got,d)
check('physical_diagonal_stationary',physical_diag)
def identity_shift():
    shifted=[v+0.01 for v in physical['mass_squared_eV2']]
    return assert_close(decode(call(dict(physical,mass_squared_eV2=shifted))),decode(call(physical)),3e-12)
check('physical_identity_shift_invariant',identity_shift)
def tiny_dephasing():
    out=call(dict(physical,tau_star_s=5.391247e-44));loss=np.array(out['result']['coherence_loss']);require(loss[0,1]>0)
    g=np.array(out['result']['gamma']);return assert_close(loss[0,1]/(g[0,1]*physical['time_s']),1,1e-14)
check('physical_expm1_planck_coherence_loss',tiny_dephasing)
modular={'channel':'modular_root_dephasing','modular_eigenvalues':[1,4,9],'s':0.6,'rho':target.encode(rho)}
def modular_root():
    out,got=invariant_result(modular);g=np.array(out['result']['gamma']);require(out['result']['gamma_units']=='per modular s')
    a=assert_close(g,beta/2*np.array([[0,1,4],[1,0,1],[4,1,0]]))
    lop=math.sqrt(beta)*np.diag([1,2,3]);lsq=lop@lop
    expect=rk4(rho,0.6,lambda r:lop@r@lop-(lsq@r+r@lsq)/2)
    return {'rates':a,'rk4':assert_close(got,expect)}
check('modular_root_rate_and_direct_GKSL',modular_root)
check('modular_zero_time',lambda:assert_close(decode(call(dict(modular,s=0))),rho))
for name,p in [('boundary',boundary),('physical',physical),('modular',modular)]:
    n=4 if name=='boundary' else 3
    check(name+'_maximally_mixed_stationary',lambda p=p,n=n:assert_close(decode(call(dict(p,rho=target.encode(np.eye(n)/n)))),np.eye(n)/n))
def scale():
    zero=call({'channel':'beta_scale','chi':0});require(zero['result']['beta_bulk']>1)
    require('no automatic substitution' in zero['result']['scope'])
    chi=2*math.acosh(1/alpha);cur=call({'channel':'beta_scale','chi':chi})
    assert_close(cur['result']['beta_bulk']/beta,1)
    vals=[call({'channel':'beta_scale','chi':x})['result']['beta_bulk'] for x in [0,1,5,10,100]]
    require(all(a>b for a,b in zip(vals,vals[1:])));return vals
check('beta_scale_separate_and_monotone',scale)
def reject(p):
    try:call(p)
    except Exception as exc:return type(exc).__name__
    raise AssertionError('invalid input accepted')
for field in ['energy_eV','tau_star_s','Kfac','time_s']:
    for label,value in [('nan',float('nan')),('infinity',float('inf')),('boolean',True),('text','1.0'),('negative',-1)]:
        check(f'reject_physical_{field}_{label}',lambda f=field,v=value:reject(dict(physical,**{f:v})))
check('reject_zero_energy',lambda:reject(dict(physical,energy_eV=0)))
for label,value in [('nan',float('nan')),('inf',float('inf')),('bool',True),('negative',-0.1)]:
    check('reject_boundary_s_'+label,lambda v=value:reject(dict(boundary,s=v)))
    check('reject_scale_chi_'+label,lambda v=value:reject({'channel':'beta_scale','chi':v}))
for label,bad in [('not_hermitian',np.array([[1,1j,0],[0,0,0],[0,0,0]])),('negative_eigenvalue',np.diag([1.1,-0.1,0])),('bad_trace',np.eye(3))]:
    check('reject_density_'+label,lambda bad=bad:reject(dict(physical,rho=target.encode(bad))))
for label,value in [('nan',float('nan')),('bool',False),('text','0')]:
    bad=copy.deepcopy(physical);bad['rho'][0][0][0]=value
    check('reject_density_cell_'+label,lambda p=bad:reject(p))
check('reject_density_shape',lambda:reject(dict(physical,rho=[])))
check('reject_mass_negative',lambda:reject(dict(physical,mass_squared_eV2=[-1,0,1])))
check('reject_mass_bool',lambda:reject(dict(physical,mass_squared_eV2=[False,1,2])))
check('reject_numerical_overflow',lambda:reject(dict(physical,energy_eV=1e-300)))
check('reject_unknown_channel',lambda:reject(dict(physical,channel='production_absolute')))
def manifest_change():
    calls=[]
    def changing(op):
        calls.append(op);return dict(receipt,canonical_manifest_sha256='A' if len(calls)==1 else 'B')
    target.require_current=changing
    try:return reject(boundary)
    finally:target.require_current=lambda operation:dict(receipt,operation=operation)
check('reject_changed_canonical_identity',manifest_change)
def kfac_zero():
    out,got=invariant_result(dict(physical,Kfac=0))
    require(np.array(out['result']['gamma']).max()==0)
    return assert_close(got,decode(call(dict(physical,tau_star_s=0))))
check('physical_zero_Kfac_is_unitary',kfac_zero)
check('reject_beta_underflow_1500',lambda:reject({'channel':'beta_scale','chi':1500}))
check('reject_beta_underflow_1e300',lambda:reject({'channel':'beta_scale','chi':1e300}))

def exact_fields_refusal(payload):
    try:call(payload)
    except ValueError as exc:
        require(str(exc).startswith('EXACT_CHANNEL_FIELDS_REQUIRED'),str(exc));return str(exc)
    raise AssertionError('field mismatch did not produce explicit refusal')
for label,p,missing in [('boundary',boundary,'s'),('physical',physical,'energy_eV'),('modular',modular,'modular_eigenvalues'),('scale',{'channel':'beta_scale','chi':2},'chi')]:
    def extras(p=p):
        denied={}
        for key in ['beta','alpha','tau']:
            denied[key]=exact_fields_refusal(dict(p,**{key:0.125}))
        return denied
    check('reject_extra_beta_alpha_tau_'+label,extras)
    incomplete={k:v for k,v in p.items() if k!=missing}
    check('reject_missing_field_'+label,lambda p=incomplete:exact_fields_refusal(p))

report={'unit':'F8.2.NU3','reviewed_candidate':str(candidate),'candidate_sha256':hashlib.sha256(raw).hexdigest(),'canonical_source_sha256':hashlib.sha256(canonical_path.read_bytes()).hexdigest(),'test_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'numpy':np.__version__,'mocked':'require_current only; finite_number imported from candidate canonical.py; no runtime identity certification','no_observed_data':True,'no_bench_writes':True,'tests':results,'pass':sum(r['status']=='PASS' for r in results),'fail':sum(r['status']=='FAIL' for r in results)}
with result_path.open('x',encoding='utf-8',newline='\n') as f:json.dump(report,f,ensure_ascii=False,indent=2)
print(json.dumps({'pass':report['pass'],'fail':report['fail'],'candidate_sha256':report['candidate_sha256'],'result':str(result_path),'failures':[r for r in results if r['status']=='FAIL']}))
