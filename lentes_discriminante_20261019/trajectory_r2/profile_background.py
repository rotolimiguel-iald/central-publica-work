"""Synthetic distance-only identifiability of the recovered homogeneous background."""
from pathlib import Path
import datetime, hashlib, json, math, re
import numpy as np
from scipy.optimize import least_squares
from numpy.polynomial.legendre import leggauss

ROOT=Path(__file__).resolve().parent
COST=Path(r'C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py')
UM=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')

def pin(p):
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def save(name,obj):
    with (ROOT/name).open('x',encoding='utf-8') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2)

def read_constant(text,name):
    vals=re.findall(r'^'+name+r'\s*=\s*([0-9.eE+-]+)\s*(?:#.*)?$',text,re.M)
    assert vals and len(set(float(x) for x in vals))==1, (name, vals)
    return float(vals[0])

def main():
    for name in ['BACKGROUND_PLAN_R2.json','BACKGROUND_RESULT_R2.json']:
        if (ROOT/name).exists(): raise FileExistsError(name)
    pairs=[(0.2,1.0),(0.3,1.5),(0.5,2.0),(0.7,2.5),(0.9,3.0)]
    save('BACKGROUND_PLAN_R2.json',{
        'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status':'INPUT_SYNTHETIC_ASIMOV_DISTANCE_ONLY_NOT_AN_OBSERVED_LENS_TEST',
        'pairs_zl_zs':pairs, 'fiducial_bare_H0':70.0,'fiducial_bare_Omega_m':0.3,
        'fiducial_source':'chosen synthetic controls, not fitted to observed data',
        'fixed_radiation':'T_CMB,N_eff from current Custo; physical omega_r held equal in both models',
        'signal':'literal background H_TGL^2=H0^2[(1+beta)Om(1+z)^3+(1+4beta/3)Or(1+z)^4+OL]',
        'GR_nuisance':'H0 in[40,100], Om in[.1,.5], jointly fit to five time-delay distances',
        'ideal_distance_sigma_fraction':0.01,'covariance':'independent, equal fractional errors; no lens mass uncertainties included',
        'quadrature_orders':[128,256], 'quadrature_fractional_difference_tolerance':1e-11,
        'purpose':'quantify restricted-family residual after background nuisance, before lens-model nuisance; not a power claim for data',
        'exact_control':'with transformed radiation coefficient also free, all distances coincide',
        'script':pin(Path(__file__)),'sources':[pin(COST),pin(UM)]})
    tc=COST.read_text(encoding='utf-8'); tu=UM.read_text(encoding='utf-8')
    beta=read_constant(tu,'ALPHA_FINE_CODATA_2018')*math.sqrt(math.e)
    T=read_constant(tc,'T_CMB_KELVIN'); Neff=read_constant(tc,'N_EFF_STANDARD')
    c=read_constant(tu,'C_LIGHT')/1000
    # These two constants reproduce the pinned source's compressed radiation function.
    omega_r=2.473e-5*(T/2.7255)**4*(1+(7/8)*Neff*(4/11)**(4/3))
    h0,Om=70.0,0.3; Or=omega_r/(h0/100)**2; OL=1-Om-Or
    coeff=np.array([(1+beta)*Om,(1+4*beta/3)*Or,OL])
    S=float(sum(coeff)); Hp=h0*math.sqrt(S); Op=coeff/S
    def distances(H,co,n):
        x,w=leggauss(n)
        def chi(z):
            zz=(x+1)*z/2
            E=np.sqrt(co[0]*(1+zz)**3+co[1]*(1+zz)**4+co[2])
            return float(c/H*z/2*np.dot(w,1/E))
        out=[]
        for zl,zs in pairs:
            cl,cs=chi(zl),chi(zs)
            out.append(cl*cs/(cs-cl)) # flat D_delta_t
        return np.array(out)
    truth=distances(h0,coeff,128)
    def gr(params,n=128):
        H,om=params;orr=omega_r/(H/100)**2
        return distances(H,np.array([om,orr,1-om-orr]),n)
    def residual(params):return (gr(params)/truth-1)/0.01
    fit=least_squares(residual,[Hp,Op[0]],bounds=([40,.1],[100,.5]),jac='3-point',
                      diff_step=1e-4,xtol=1e-14,ftol=1e-14,gtol=1e-14,x_scale='jac')
    assert fit.success,fit.message
    rr=gr(fit.x)/truth-1
    truth256=distances(h0,coeff,256);gr256=gr(fit.x,256)
    qdiff=max(float(np.max(abs(truth256/truth-1))),float(np.max(abs(gr256/gr(fit.x)-1))))
    assert qdiff<1e-11,qdiff
    exact=distances(Hp,Op,128)
    exact_error=float(np.max(abs(exact/truth-1)))
    assert exact_error<1e-13,exact_error
    sep=float(np.linalg.norm(rr)/0.01)
    save('BACKGROUND_RESULT_R2.json',{
        'status':'DERIVED_SYNTHETIC_DISTANCE_ONLY_NOT_PHYSICAL_5SIGMA',
        'beta_runtime':beta, 'fixed_T_CMB_K':T,'fixed_Neff':Neff,'fixed_omega_r':omega_r,
        'bare_parameters':{'H0':h0,'Om':Om,'Or':Or,'OL':OL},'H_at_zero':Hp,
        'free_radiation_equivalent_GR':{'H0':Hp,'Om':float(Op[0]),'Or':float(Op[1]),'OL':float(Op[2])},
        'exact_free_radiation_control_max_fractional_error':exact_error,
        'restricted_GR_best_fit':{'H0':float(fit.x[0]),'Om':float(fit.x[1]),'optimizer_success':bool(fit.success),'optimality':float(fit.optimality),'nfev':int(fit.nfev)},
        'rows':[{'zl':p[0],'zs':p[1],'TGL_Ddt_Mpc':float(t),'GR_profiled_Ddt_Mpc':float(v),'GR_minus_TGL_fraction':float(r)} for p,t,v,r in zip(pairs,truth,gr(fit.x),rr)],
        'max_abs_profiled_fractional_residual':float(np.max(abs(rr))),
        'rms_profiled_fractional_residual':float(np.sqrt(np.mean(rr**2))),
        'synthetic_Asimov_norm_at_1percent_each':sep,
        'ideal_common_fractional_sigma_for_norm5':float(np.linalg.norm(rr)/5),
        'statistical_scope':'Euclidean separation of five synthetic distances in declared Gaussian covariance; not an observed p-value or validated discovery power. Real mass/LOS/anisotropy freedom can further reduce distance-only information. External priors could change model comparison.',
        'quadrature_max_fractional_difference_128_vs_256':qdiff,
        'plan':pin(ROOT/'BACKGROUND_PLAN_R2.json'),'script':pin(Path(__file__))})
    print(json.dumps({'max_fraction':float(np.max(abs(rr))),'synthetic_norm_at_1percent':sep,'sigma_fraction_for_norm5':float(np.linalg.norm(rr)/5),'quadrature_error':qdiff}))

if __name__=='__main__':main()
