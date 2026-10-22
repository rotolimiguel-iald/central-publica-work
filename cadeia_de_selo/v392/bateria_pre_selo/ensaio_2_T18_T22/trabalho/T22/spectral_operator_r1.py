"""Conditional neutrino diagnostics; no observed likelihood or original imports.
Usage: python -X utf8 -B spectral_operator_r1.py --output NEW_JSON
"""
import argparse, math, cmath, json, re, hashlib, os, time
from pathlib import Path
from datetime import datetime, timezone

def finite(x, positive=False):
    if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or (positive and x<=0): raise ValueError('finite numeric input required')
    return x

def pin(p):
    b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def output(p,obj):
    if p.exists():raise FileExistsError(p)
    b=(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    temp=p.with_name(p.name+'.tmp_'+datetime.now(timezone.utc).strftime('%H%M%S_%f'))
    with temp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    if temp.read_bytes()!=b:raise RuntimeError('verification')
    os.rename(temp,p)

def pmns(s12sq,s13sq,s23sq):
    s12,s13,s23=map(math.sqrt,[s12sq,s13sq,s23sq])
    c12,c13,c23=map(math.sqrt,[1-s12sq,1-s13sq,1-s23sq])
    return [[c12*c13,s12*c13,s13],[-s12*c23-c12*s23*s13,c12*c23-s12*s23*s13,s23*c13],[s12*s23-c12*c23*s13,-c12*s23-s12*c23*s13,c23*c13]]

def evolve(rho,h,t,a):
    finite(t);finite(a)
    if t<0 or a<0:raise ValueError('positive semigroup required')
    return [[rho[i][j] if i==j else rho[i][j]*cmath.exp(complex(-a*(h[i]-h[j])**2*t,-(h[i]-h[j])*t)) for j in range(3)] for i in range(3)]
def probabilities(rho,U):return [sum(U[k][i]*rho[i][j]*U[k][j] for i in range(3) for j in range(3)).real for k in range(3)]
def det3(a):return sum((1 if (i,j,k) in [(0,1,2),(1,2,0),(2,0,1)] else -1)*a[0][i]*a[1][j]*a[2][k] for i in range(3) for j in range(3) for k in range(3) if len({i,j,k})==3)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out=Path(args.output)
    if out.exists():raise FileExistsError(out)
    start=datetime.now(timezone.utc);tick=time.perf_counter();base=Path(__file__).resolve().parent
    plan=json.loads((base/'PLANO_R1.json').read_text(encoding='utf-8'));q=plan['inputs_reference_not_fitted'];c=plan['constants']
    src=Path(plan['alpha_source']);raw=src.read_bytes();text=raw.decode('utf-8-sig')
    matches=re.findall(r'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)\s*(?:#.*)?$',text,re.M)
    if len(matches)!=1:raise RuntimeError('alpha assignment not unique')
    alpha=finite(float(matches[0]),True);beta=alpha*math.sqrt(math.e);beta_upper=math.sqrt(math.e)
    hbarJ=c['h_J_s']/(2*math.pi);hbar=hbarJ/c['eV_J'];tp=math.sqrt(hbarJ*c['G_SI']/c['c_m_s']**5)
    U=pmns(q['sin2theta12'],q['sin2theta13'],q['sin2theta23']);w=[x*x for x in U[0]]
    masses=[0.0,q['dm21_eV2'],q['dm31_eV2']]
    pairs=[(0,1),(0,2),(1,2)]
    gaps=[abs(masses[j]-masses[i]) for i,j in pairs]
    unitarity=max(abs(sum(U[i][k]*U[j][k] for k in range(3))-(i==j)) for i in range(3) for j in range(3))
    rho=[[complex(U[0][i]*U[0][j]) for j in range(3)] for i in range(3)]
    diag=[[complex(plan['synthetic_checks']['three_mass_populations'][i]) if i==j else 0j for j in range(3)] for i in range(3)]
    h=[0.,1.,3.];e0=sum(h[i]*rho[i][i].real for i in range(3));tests=[]
    for a in plan['synthetic_checks']['dimensionless_dephasing_strengths']:
        rr=evolve(rho,h,1.,a);dd=evolve(diag,h,1.,a);probs=probabilities(rr,U)
        minors=[rr[i][i].real for i in range(3)]+[(rr[i][i]*rr[j][j]-rr[i][j]*rr[j][i]).real for i,j in pairs]+[det3(rr).real]
        tests.append({'strength_INPUT':a,'trace':sum(rr[i][i].real for i in range(3)),'energy_error':sum(h[i]*rr[i][i].real for i in range(3))-e0,'probabilities':probs,'sum_probabilities':sum(probs),'min_principal_minor':min(minors),'diagonal_state_max_change':max(abs(dd[i][j]-diag[i][j]) for i in range(3) for j in range(3)),'diagonal_flavor_probabilities':probabilities(dd,U)})
        assert min(minors)>-1e-12 and abs(sum(probs)-1)<1e-12
        assert tests[-1]['diagonal_state_max_change']==0
    def channels(E_MeV,L_m,b):
        t=L_m/c['c_m_s']; rows=[]
        for (i,j),gap in zip(pairs,gaps):
            omega=gap/(2*E_MeV*1e6*hbar)
            gamma=.5*tp*b*omega**2
            rows.append({'pair':f'{j+1}{i+1}','omega_per_s':omega,'gamma_per_s':gamma,'gamma_t':gamma*t,'one_minus_damping':-math.expm1(-gamma*t)})
        return rows
    rows=[]
    for E in plan['inputs_reference_not_fitted']['energies_MeV']:
        for source,L in [('reactor',q['reactor_baseline_km']*1000),('supernova',q['supernova_baseline_kpc']*1000*q['parsec_m'])]:
            rows.append({'source':source,'E_MeV_INPUT':E,'L_m_INPUT':L,'channels':channels(E,L,beta),'upper_beta_channels_COUNTERFACTUAL':channels(E,L,beta_upper)})
    chi0=2*math.acosh(1/alpha);slopechecks=[]
    for slope in plan['synthetic_checks']['running_chi_log_slope']:
        r_slope=plan['synthetic_checks']['r_log_slope'];tau_slope=plan['synthetic_checks']['tau_log_slope']
        def lg(x):
            chi=chi0+slope*x;b=math.sqrt(math.e)/math.cosh(chi/2)
            return -2*x+tau_slope*x+math.log(b)+b*r_slope*x
        for x in [-math.log(2),0,math.log(2)]:
            chi=chi0+slope*x;b=math.sqrt(math.e)/math.cosh(chi/2);bp=-.5*b*math.tanh(chi/2)*slope
            analytic=-2+tau_slope+bp*(1/b+r_slope*x)+b*r_slope
            step=1e-5;numeric=(lg(x+step)-lg(x-step))/(2*step)
            slopechecks.append({'ln_E_E0':x,'chi_slope_INPUT':slope,'full_n_eff':analytic,'finite_difference':numeric,'difference':numeric-analytic,'meaning':'counterfactual identity, not current source prediction'})
            assert abs(numeric-analytic)<1e-8
    energies=[2+6*i/120 for i in range(121)];samples=[];L=q['reactor_baseline_km']*1000;t=L/c['c_m_s']
    for E in energies:
        ch=channels(E,L,beta)
        p0=1-sum(4*w[i]*w[j]*math.sin(ch[k]['omega_per_s']*t/2)**2 for k,(i,j) in enumerate(pairs))
        dp=sum(2*w[i]*w[j]*math.cos(ch[k]['omega_per_s']*t)*math.expm1(-ch[k]['gamma_t']) for k,(i,j) in enumerate(pairs))
        assert p0>0
        samples.append({'E_MeV':E,'P0':p0,'deltaP_stable':dp})
    mp=sum(x['P0'] for x in samples)/len(samples);md=sum(x['deltaP_stable'] for x in samples)/len(samples);coef=md/mp
    fixed=sum(x['deltaP_stable']**2/x['P0'] for x in samples)/len(samples)
    prof=sum((x['deltaP_stable']-coef*x['P0'])**2/x['P0'] for x in samples)/len(samples)
    power={'meaning':'ideal flat vacuum flux, known mixing, no detector smearing/background; local Gaussian expected separation only','per_unoscillated_exposure_fixed_norm':fixed,'per_unoscillated_exposure_profile_norm':prof,'N_unoscillated_for_nominal_5_fixed':25/fixed,'N_unoscillated_for_nominal_5_profile':25/prof,'N_detected_reference_for_nominal_5_profile':25/prof*mp,'max_abs_deltaP':max(abs(x['deltaP_stable']) for x in samples),'max_abs_relative_deltaP':max(abs(x['deltaP_stable']/x['P0']) for x in samples),'mean_P0':mp,'samples':samples,'physical_JUNO_power':None}
    invalid=0
    for x in [True,float('nan'),float('inf'),-1]:
        try:finite(x,True)
        except ValueError:invalid+=1
    assert invalid==4
    result={'unit':'F8.2.NU2','start_utc':start.isoformat(),'end_utc':datetime.now(timezone.utc).isoformat(),'elapsed_s':time.perf_counter()-tick,'status':'DERIVED_CONDITIONAL_NO_OBSERVED_SIGNIFICANCE','source_pins':[pin(src),pin(base/'PLANO_R1.json'),pin(base/'PLANO_RECONCILIACAO_R1.json'),pin(Path(__file__))],'beta0_runtime':beta,'alpha_source':alpha,'beta_upper_abstract':beta_upper,'max_beta_ratio_Kfac1_tau_fixed':beta_upper/beta,'max_ratio_orders':math.log10(beta_upper/beta),'tP_s_conditional':tp,'hbar_eV_s':hbar,'texture_gamma21_gamma31_gamma32_normalized21':[1,(gaps[1]/gaps[0])**2,(gaps[2]/gaps[0])**2],'unitarity_error':unitarity,'density_channel_checks':tests,'rate_examples':rows,'running_extension_checks':slopechecks,'ideal_reactor':power,'checks_invalid_rejected':invalid,'physical_chi_E':None,'physical_tau_star':None,'stellar_delta_capture_rate':None,'stellar_delta_Ye':None,'stellar_delta_L':None,'observed_significance':None,'limitations':['The current boundary dephasing source fixes beta0; beta(E) is only a counterfactual identity here','Planck tau and Kfac1 are conditional, not selected by theory','rho diagonal is stationary only for dephasing in that same basis; no source or matter feedback solved','No bound transfer from JUNO gamma21=gamma31 gamma32=0','Ideal exposure numbers are not a real experiment forecast']}
    output(out,result)
    print(json.dumps({'result':pin(out),'texture':result['texture_gamma21_gamma31_gamma32_normalized21'],'beta_ratio_max':result['max_beta_ratio_Kfac1_tau_fixed'],'diagonal_change':max(r['diagonal_state_max_change'] for r in tests),'max_deltaP_planck':power['max_abs_deltaP'],'N5_ideal_profile':power['N_unoscillated_for_nominal_5_profile']}))
if __name__=='__main__':main()
