"""Conditional feasibility checks for F8.2.SN1; never an observed SN test.
Only standard library. No imports of um.py. No fabricated stellar matching.
Usage: python -B calculate_r1.py --output NEW_PATH
Existing output is refused before source reads or computation.
"""
import argparse
from decimal import Decimal, ROUND_CEILING
import hashlib
import json
import math
import os
from pathlib import Path
import re
from statistics import NormalDist
import time
from datetime import datetime, timezone
import uuid

def pin(path):
    data=path.read_bytes()
    return {"path":str(path),"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data)}

def matmul(a,b):
    n=len(a)
    return [[sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def sub(a,b):return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def comm(a,b):return sub(matmul(a,b),matmul(b,a))
def trace(a):return sum(a[i][i] for i in range(len(a)))

def finite_number(x):
    if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x):raise ValueError('finite non-boolean number required')
    return x

def sample_size(signal,sigma,z=5.0,power=None,systematic=0.0):
    for x in [signal,sigma,z,systematic]:finite_number(x)
    if signal<=0 or sigma<=0 or z<=0 or systematic<0:raise ValueError('invalid domain')
    target=z+(NormalDist().inv_cdf(power) if power is not None else 0.0)
    denom=(Decimal(str(signal))/Decimal(str(target)))**2-Decimal(str(systematic))**2
    if denom<=0:return None
    return int((Decimal(str(sigma))**2/denom).to_integral_value(rounding=ROUND_CEILING))

def run(out):
    if out.exists():raise FileExistsError(out)
    start=datetime.now(timezone.utc).isoformat(); tick=time.perf_counter()
    root=Path(__file__).resolve().parent
    plans=[root/'PLANO_CALCULO_R1.json',root/'PLANO_COMPLEMENTO_R2.json']
    p1=json.loads(plans[0].read_text(encoding='utf-8'));p2=json.loads(plans[1].read_text(encoding='utf-8'))
    source=Path(p1['fonte_alpha']['path']);raw=source.read_bytes()
    matches=list(re.finditer(rb'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)\s*$',raw,re.M))
    if len(matches)!=1:raise ValueError('expected one literal top-level alpha')
    alpha=float(matches[0].group(1)); beta0=alpha*math.sqrt(math.e); chi0=2*math.acosh(1/alpha)
    alpha_pin={'path':str(source),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'line':raw[:matches[0].start()].count(b'\n')+1,'identifier':'ALPHA_FINE_CODATA_2018','value':alpha}
    assert math.isclose(1/math.cosh(chi0/2),alpha,rel_tol=2e-15)
    legacy=[]
    for f in p1['entradas_sinteticas']['alpha_multipliers']:
        a=alpha*f;b=a*math.sqrt(math.e)
        legacy.append({'alpha_multiplier_INPUT':f,'chi':2*math.acosh(1/a),'beta':b,'retired_mass_ratio':(1-b)**1.5,'retired_mass_shift_percent':100*math.expm1(1.5*math.log1p(-b))})
    cm=p2['Coulomb']['CM'];coulomb=[]
    for z in p2['Coulomb']['Z']:
        cz=(4*cm/3)*(4/(9*math.pi))**(1/3)*z**(2/3)
        q=cz*alpha;baseline=(1+q)**1.5
        rows=[]
        for f in p2['Coulomb']['alpha_multipliers']:
            ratio=((1+q*f)/(1+q))**1.5
            rows.append({'alpha_multiplier_INPUT':f,'mass_ratio_to_same_Coulomb_baseline':ratio,'shift_percent':100*(ratio-1)})
        sensitivity=1.5*q/(1+q)
        h=1e-5
        numeric=(math.log(((1+q*math.exp(h))/(1+q))**1.5)-math.log(((1+q*math.exp(-h))/(1+q))**1.5))/(2*h)
        assert math.isclose(sensitivity,numeric,rel_tol=2e-8,abs_tol=1e-10)
        coulomb.append({'Z':z,'q_Z':q,'mass_ratio_to_ideal':baseline,'dlnM_dlnAlpha':sensitivity,'independent_finite_difference':numeric,'rows':rows})
    H=[[float(i) if i==j else 0.0 for j in range(3)] for i in range(3)]
    rho=[[1/3 for j in range(3)] for i in range(3)]
    double=comm(H,comm(H,rho)); dephasing=[]
    for a in p1['entradas_sinteticas']['integrated_diffusion']:
        evolved=[[rho[i][j]*math.exp(-a*(i-j)**2) for j in range(3)] for i in range(3)]
        dephasing.append({'integrated_diffusion_INPUT':a,'energy':trace(matmul(H,evolved)),'trace':trace(evolved),'populations':[evolved[i][i] for i in range(3)],'rho01':evolved[0][1],'purity':trace(matmul(evolved,evolved))})
    assert trace(matmul(H,double))==0.0
    assert all(row['energy']==1.0 and row['trace']==1.0 for row in dephasing)
    h=p2['curvature']['constants']['h'];G=p2['curvature']['constants']['G'];c=p2['curvature']['constants']['c'];lp2=(h/(2*math.pi))*G/c**3
    curvature=[]
    for density in p2['curvature']['density_g_cm3_hypothetical']:
        rho_si=density*1000;ricci_proxy=8*math.pi*G*rho_si/c**2
        eps=beta0*lp2*ricci_proxy
        curvature.append({'density_g_cm3_INPUT':density,'curvature_proxy_m_minus2':ricci_proxy,'epsilon_beta0':eps,'log10_abs_epsilon':math.log10(abs(eps)),'epsilon_abstract_beta_upper_sqrt_e':math.sqrt(math.e)*lp2*ricci_proxy})
    power=[]
    for signal in p1['entradas_sinteticas']['signals_mag_hypothetical']:
        sig=p1['entradas_sinteticas']['sigma_mag_hypothetical']
        power.append({'signal_mag_INPUT':signal,'sigma_mag_INPUT':sig,'n_median_separation_5sigma':sample_size(signal,sig),'n_90pct_power_one_sided_5sigma':sample_size(signal,sig,power=.9),'maximum_common_systematic_for_median_5sigma':signal/5})
    n=10;amplitude=.01;sigma=.1
    constant=[amplitude]*n;shape=[amplitude if i%2==0 else -amplitude for i in range(n)]
    projection=lambda v:sum((x-sum(v)/len(v))**2/sigma**2 for x in v)
    assert projection(constant)<1e-25
    invalid=0
    for x in [float('nan'),float('inf'),-float('inf'),True]:
        try:sample_size(x,.1)
        except ValueError:invalid+=1
    assert invalid==4
    assert sample_size(.01,.1)==2500
    assert sample_size(.001,.1)==250000
    result={'unit':'F8.2.SN1','revision':'R2: Decimal sample-size ceiling avoids binary rounding at exact integers; R1 preserved','status':'DERIVED_CONDITIONAL_NO_OBSERVED_DATA','start_utc':start,'end_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.perf_counter()-tick,'pins':[pin(Path(__file__)),*[pin(p) for p in plans]],'alpha_source':alpha_pin,'beta0':beta0,'chi0_defined_by_inverting_alpha':chi0,'v388_alpha_identity_error':1/math.cosh(chi0/2)-alpha,'legacy_formula_RETIRED_NOT_PREDICTION':legacy,'legacy_cancellation_NOT_PREDICTION':{'K_factor_required':1/(1-beta0),'Ye_factor_required':(1-beta0)**(-.75)},'known_Coulomb_sensitivity_NOT_TGL_PREDICTION':coulomb,'dephasing_FIXED_H_COMMUTING_JUMPS':{'energy_derivative_double_commutator':trace(matmul(H,double)),'rows':dephasing},'curvature_operator_SIZE_ONLY':{'planck_length_squared_m2':lp2,'rows':curvature,'warning':'Ricci-flat fixed background sets this operator density and its Maxwell correction to zero; metric variation/backreaction is not concluded zero. No luminosity inferred.'},'power_HYPOTHETICAL_ONLY':power,'nuisance_projection':{'n':n,'amplitude_mag_INPUT':amplitude,'sigma_mag_INPUT':sigma,'constant_signal_projected_Z2':projection(constant),'balanced_shape_projected_Z2':projection(shape)},'checks':{'scale_inverse':True,'Coulomb_derivative_by_finite_difference':True,'dephasing_energy_and_trace':True,'nuisance_constant_absorbed':True,'nonfinite_boolean_rejections':invalid},'physical_TGL_deltaP':None,'physical_TGL_deltaYe':None,'physical_TGL_deltaL':None,'physical_TGL_sigma':None,'reason':'No stellar matching equation obtained from scale identity alone. Nulls mean not calculated, not physical zero.'}
    data=(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    tmp=out.with_name(out.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f:f.write(data)
    if tmp.stat().st_size!=len(data):raise IOError('size mismatch')
    os.rename(tmp,out)
    print(json.dumps({'path':str(out),'sha256':hashlib.sha256(data).hexdigest(),'beta0':beta0,'Coulomb':coulomb,'curvature':curvature,'power':power},ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.output)
