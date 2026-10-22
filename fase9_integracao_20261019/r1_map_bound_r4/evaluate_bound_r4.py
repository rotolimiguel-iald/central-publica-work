"""One preregistered algebraic bound evaluation; no solver, fit or observations."""
from pathlib import Path
from decimal import Decimal, localcontext
import json,hashlib,datetime,time
B=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def write(name,value):
    with (B/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2,allow_nan=False)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
    for n in ('START_R4.json','RESULT_R4.json'):
        if (B/n).exists():raise FileExistsError(n)
    p=load(B/'PLAN_R4.json')
    for entry in p['pins']:
        if sha(Path(entry['path']))!=entry['sha256']:raise ValueError('PIN_CHANGED')
    start=utc();clock=time.perf_counter()
    write('START_R4.json',{'utc':start,'plan_sha256':sha(B/'PLAN_R4.json'),'single_execution':True})
    spec=load(Path(p['spec_path']))['spec'];cfg=load(Path(p['configuration_path']));budget=load(Path(p['budget_path']))
    with localcontext() as ctx:
        ctx.prec=70
        D=lambda x:Decimal(str(x))
        alpha=D(spec['beta']['alpha_read'])
        ALPHA_FINE_CODATA_2018=alpha
        beta=ALPHA_FINE_CODATA_2018*(D(1)/2).exp()
        exponent=4*beta/3;zstar=D(spec['lei']['z_star'])
        assert zstar==D(cfg['redshifts']['z_star_law'])
        law=spec['lei'];Om=D(law['Omega_m']);Or=D(law['Omega_r'])
        E2=Om*(1+zstar)**3+Or*(1+zstar)**4+1-Om-Or
        K=((E2.ln()/2)*(2*beta/3)).exp()
        Kmax=(exponent*(1+zstar).ln()).exp()
        hmax=D(cfg['prior']['bounds']['H0'][1]);hbg=D(spec['fundos']['BG1']['H0'])
        margin=D(budget['adversarial_mean_bias_budget_for_nominal_z5_if_background_independent'])
        assert margin>0 and abs(K-D(budget['K']))<D('1e-12')
        metadata=load(B/'SOURCES_R4.json')['selection_metadata']
        observed_optical_z=[D(v)/D('299792.458') for v in metadata['five_maser_optical_CMB_velocities_km_s']]
        points=p['redshift_domains']
        rows=[]
        for case in points:
            z=D(case['zmax'])
            assert 0<=z<=zstar
            logq=exponent*(1+z).ln();q=logq.exp();deficit=1-(-logq).exp()
            nominal=hbg*K*deficit;whole=hmax*Kmax*deficit
            rows.append({'id':case['id'],'zmax':str(z),'scope':case['scope'],
              'Q_upper':str(q),'distance_fraction_upper':str(q-1),'magnitude_shift_upper':str(5*logq/D(10).ln()),
              'H_intercept_fraction_deficit_upper':str(deficit),
              'nominal_BG1_intercept_bias_bound_km_s_Mpc':str(nominal),
              'conditional_whole_prior_intercept_bias_bound_km_s_Mpc':str(whole),
              'fraction_of_nominal_5sigma_margin':str(nominal/margin),
              'fixed_weight_l1_amplification_needed_to_exhaust_nominal_margin':str(margin/nominal) if nominal else None,
              'not_a_complete_reader_bias_bound':True})
        result={'status':'DERIVED_CONDITIONAL_DISTANCE_MAP_BOUND_ONLY','plan_sha256':sha(B/'PLAN_R4.json'),
          'started_utc':start,'ended_utc':utc(),'seconds':time.perf_counter()-clock,'exit_code':0,
          'beta_runtime':str(beta),'alpha_source':str(alpha),'K_nominal_runtime':str(K),'K_whole_conditional_box_upper':str(Kmax),
          'nominal_5sigma_margin_km_s_Mpc':str(margin),'theta_prior':cfg['prior'],
          'published_maser_optical_CMB_z_range':[str(min(observed_optical_z)),str(max(observed_optical_z))],
          'rows':rows,'numerics':'Decimal70 evaluation of analytic inequalities; not interval arithmetic',
          'fitted_local_centers':False,'solver_calls':0,'observed_significance':None,
          'complete_physical_map_admitted':False,'peculiar_velocity_full_prior_covered':False,
          'all_CAMB_parameter_box_energy_hypotheses_verified':False}
    write('RESULT_R4.json',result)
    print(json.dumps({'status':result['status'],'rows':len(rows),'result_sha256':sha(B/'RESULT_R4.json')}))
if __name__=='__main__':main()
