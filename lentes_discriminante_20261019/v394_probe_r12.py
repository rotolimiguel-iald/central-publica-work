"""Bounded lens-relevance test of exact extracted v394 finite-model functions."""
from pathlib import Path
import ast,datetime,hashlib,json,math,sys
P=Path(__file__).resolve().parent/'v394_r12'
def save(name,obj):
    with (P/name).open('x',encoding='utf-8',newline='\n') as f:json.dump(obj,f,ensure_ascii=False,indent=2)
def pin(p):
    p=Path(p);b=p.read_bytes();return {'path':str(p.resolve()),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def main():
    source=P/'v394_source.py.snapshot';txt=source.read_text(encoding='utf-8-sig');tree=ast.parse(txt)
    names=['V394PhysicalContractError','_v394_finite_real','v394_physical_parameters','v394_kms_clock','v394_gibbs_root_parameters']
    nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
    assert len(nodes)==len(names)
    selected='\n\n'.join(''.join(txt.splitlines(keepends=True)[n.lineno-1:n.end_lineno]) for n in nodes)
    with (P/'physical_functions_extracted.py').open('x',encoding='utf-8') as f:f.write(selected)
    alpha_node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ALPHA_FINE_CODATA_2018' for t in n.targets))
    alpha=ast.literal_eval(alpha_node.value)
    plan={'source':pin(source),'functions':pin(P/'physical_functions_extracted.py'),'alpha_source_line':alpha_node.lineno,'alpha':alpha,'beta':'alpha*sqrt(e) at runtime','tolerance':1e-12,'cases_Omega_kappa':[[1.,1.],[2.,10.],[10.,20.]],'scale_control':3.,'claims':['Conditional finite Gibbs instance fixes Eref from V0,kappa.','Coherence factor exp((-gamma+2iOmega)t): at fixed spectrum beta changes magnitude but not unwrapped phase.','Simultaneously scaling V0 and kappa by s and time by 1/s preserves this factor; no absolute clock obtained.'],'not_claimed':['Astrophysical propagation law','full release execution','observed statistical power','Gibbs state or kappa fixed by galaxy data','all TGL delays vanish'],'preregistered_before_probe':True}
    save('PLAN_R12.json',plan)
    ns={};exec(compile(selected,str(P/'physical_functions_extracted.py'),'exec'),ns)
    hb=6.62607015e-34/(2*math.pi); beta=alpha*math.sqrt(math.e);cases=[]
    for om,kap in plan['cases_Omega_kappa']:
        x=ns['v394_gibbs_root_parameters'](om*hb,kap,hb,alpha)
        y=ns['v394_gibbs_root_parameters'](3*om*hb,3*kap,hb,alpha)
        z=ns['v394_gibbs_root_parameters'](om*hb,kap,hb,alpha/2)
        t=.37/om; rawrate=beta/(2*hb)*(math.sqrt(x['energies_J'][1])-math.sqrt(x['energies_J'][0]))**2
        residuals={'root_rate':abs(rawrate/x['gamma_s_inv']-1),'scale_gamma':abs(y['gamma_s_inv']/(3*x['gamma_s_inv'])-1),'scale_Eref':abs(y['Eref_J']/(3*x['Eref_J'])-1),'scale_phase':abs(2*y['Omega_rad_s']*t/3-2*x['Omega_rad_s']*t),'scale_exposure':abs(y['gamma_s_inv']*t/3-x['gamma_s_inv']*t),'counterfactual_half_alpha_phase':abs(z['Omega_rad_s']-x['Omega_rad_s']),'counterfactual_half_alpha_rate':abs(z['gamma_s_inv']/(x['gamma_s_inv']/2)-1)}
        assert all(math.isfinite(v) and v<plan['tolerance'] for v in residuals.values())
        cases.append({'Omega':om,'kappa':kap,'Eref_over_V0':x['Eref_J']/x['V0_J'],'gamma_over_Omega':x['gamma_s_inv']/om,'residuals':residuals})
    import sympy as s
    b, rate, omega,t=s.symbols('beta rate omega t',real=True)
    logc=(-b*rate+2*s.I*omega)*t
    checks={'d_phase_d_beta':s.simplify(s.diff(s.im(logc),b))==0,'d_log_modulus_d_beta':s.simplify(s.diff(s.re(logc),b)+rate*t)==0}
    assert all(checks.values())
    report={'status':'PASS_WITH_FINITE_MODEL_SCOPE','source':pin(source),'plan':pin(P/'PLAN_R12.json'),'script':pin(__file__),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'beta':beta,'cases':cases,'symbolic_checks':checks,'max_residual':max(v for x in cases for v in x['residuals'].values()),'interpretation':'The provided finite-model clock reads time after specifying spectrum/rate. It does not supply a lens refractive potential or beta-dependent phase delay. The beta effect tested is damping. Galaxy-to-spectrum, kappa, state, coupling and metric response remain needed. No assertion about all TGL lens branches.','observed_data':False,'canonical_program_executed':False}
    save('PROBE_RESULT_R12.json',report)
    print(json.dumps({'status':report['status'],'cases':len(cases),'max_residual':report['max_residual'],'symbolic_checks':checks}))
if __name__=='__main__':main()
