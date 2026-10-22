"""Conditional accumulated optical geometry, NOT an established TGL lens law."""
from pathlib import Path
import json,hashlib,math,re,datetime
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import minimize_scalar

ROOT=Path(__file__).resolve().parent
UM=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(n,d):
    with (ROOT/n).open('x',encoding='utf-8') as f:json.dump(d,f,ensure_ascii=False,indent=2)

def main():
    for n in ['OPTICAL_PLAN_R3.json','OPTICAL_RESULT_R3.json']:
        if (ROOT/n).exists():raise FileExistsError(n)
    pairs=[(.2,1),(.3,1.5),(.5,2),(.7,2.5),(.9,3)]
    save('OPTICAL_PLAN_R3.json',{
        'status':'INPUT_CONDITIONAL_OPTICAL_EXTENSION_NOT_CANONICAL_PREDICTION',
        'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'hypothesis':'Promote accumulated luminosity radial integral to flat optical geometry for every pair of endpoints; not established by current TGL lens consumer.',
        'H_scale':70,'Omega_m':.3,'Omega_r':0,'pairs':pairs,
        'scope':'Synthetic low-redshift matter+Lambda control matching ORDEM018 illustrative background; not full physical CMB cosmology.',
        'K_star':'absorbed exactly in free overall H_scale; no redshift_star or value invented',
        'GR_fits':['scale only','scale and Omega_m in[.1,.5]'],
        'scale_fit':'analytic least squares of fractional distances at each Omega_m',
        'Omega_grid':401,'quadrature':[128,256],'sigma_fraction_each_independent':.01,
        'validation':'beta0 exact control; quadrature relative difference <1e-11; minimum from declared grid bracket plus endpoints',
        'no_observed_data':True,'sources':[pin(UM)],'script':pin(Path(__file__))})
    t=UM.read_text(encoding='utf-8')
    alpha=float(re.search(r'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)',t,re.M).group(1))
    c=float(re.search(r'^C_LIGHT\s*=\s*([0-9.eE+-]+)',t,re.M).group(1))/1000
    beta=alpha*math.sqrt(math.e)
    def vec(om,nu,n):
        x,w=leggauss(n)
        def chi(z):
            u=(x+1)*z/2; E=np.sqrt(om*(1+u)**3+1-om)
            return c/70*z/2*np.dot(w,E**(nu-1))
        return np.array([chi(l)*chi(s)/(chi(s)-chi(l)) for l,s in pairs])
    truth=vec(.3,2*beta/3,128)
    def profile(om):
        ratio=vec(om,0,128)/truth
        scale=float(sum(ratio)/sum(ratio**2))
        r=scale*ratio-1
        return float(r@r),scale,r
    grid=np.linspace(.1,.5,401); vals=np.array([profile(om)[0] for om in grid]);i=int(vals.argmin())
    bracket=(float(grid[max(0,i-1)]),float(grid[min(400,i+1)]))
    fit=minimize_scalar(lambda om:profile(om)[0],bounds=bracket,method='bounded',options={'xatol':1e-14})
    assert fit.success
    candidates=[(.1,profile(.1)),(.5,profile(.5)),(float(fit.x),profile(fit.x))]
    ombest,out=min(candidates,key=lambda x:x[1][0]);cost,scale,r=out
    only=profile(.3)
    truth256=vec(.3,2*beta/3,256)
    result256=vec(ombest,0,256)*scale
    qerr=max(float(np.max(abs(truth256/truth-1))),float(np.max(abs(result256/(vec(ombest,0,128)*scale)-1))))
    assert qerr<1e-11
    zero=vec(.3,0,128);zero_scale=float(sum(zero/zero)/sum((zero/zero)**2))
    assert zero_scale==1.0
    save('OPTICAL_RESULT_R3.json',{
        'status':'DERIVED_CONDITIONAL_SYNTHETIC_NOT_OBSERVED_SIGNIFICANCE',
        'beta_runtime':beta,'nu':2*beta/3,
        'H_scale_definition':'H_nu*K_star for optical extension; only synthetic normalization, not an inferred physical H0',
        'scale_only':{'H_scale_GR':70/only[1],'max_fraction':float(np.max(abs(only[2]))),'norm_at_1percent':math.sqrt(only[0])/.01},
        'scale_and_Om':{'H_scale_GR':70/scale,'Om':ombest,'grid_bracket':bracket,
            'max_fraction':float(np.max(abs(r))),'norm_at_1percent':math.sqrt(cost)/.01,
            'equal_independent_sigma_fraction_for_norm5':math.sqrt(cost)/5,
            'conditional_K_scale_survival':'zero with free scale; only residual shape considered'},
        'rows':[{'zl':l,'zs':s,'optical_Ddt_Mpc':float(tt),'GR_profiled_Ddt_Mpc':float((1+rr)*tt),'fraction':float(rr)} for (l,s),tt,rr in zip(pairs,truth,r)],
        'quadrature_difference':qerr,'beta_zero_scale_control':zero_scale,
        'scope':'Distance-only Asimov norm; additional lens mass/line-of-sight freedoms not included. External priors may restrict background freedom. Hypothesis that D_L reading is optical metric remains unproven.',
        'plan':pin(ROOT/'OPTICAL_PLAN_R3.json'),'script':pin(Path(__file__))})
    print(json.dumps({'max_fraction':float(np.max(abs(r))),'norm_at_1percent':math.sqrt(cost)/.01,'sigma_fraction_for_norm5':math.sqrt(cost)/5,'quadrature_difference':qerr}))

if __name__=='__main__':main()
