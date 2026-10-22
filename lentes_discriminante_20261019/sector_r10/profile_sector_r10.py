"""Compose the existing covariant sector closure with lens mass profiling, not a data fit."""
from pathlib import Path
import ast, hashlib, json, math, re, sys
import sympy as s
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
PROGRAM=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
FECHO=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')

def pin(p):
    p=Path(p);raw=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
def save(name,obj):
    with (BASE/name).open('x',encoding='utf-8',newline='\n') as f:json.dump(obj,f,ensure_ascii=False,indent=2)

if __name__=='__main__':
    phase=sys.argv[1]
    if phase=='plan':
        sources=[FECHO/'weighted_action_r86/source/COVARIANT_SECTOR_SOURCE_R86.md',
                 FECHO/'weighted_action_r86/REVIEW_R86_FINAL.json',
                 FECHO/'stationary_selection_r89/source/ACTION_EOM_RESIDUAL_R89.md',
                 ROOT/'trajectory_r2/DELIVERY_IDENTIFIABILITY_R2.json',
                 ROOT/'calibration_r4/REVIEW_R4.json', PROGRAM]
        for p in sources:
            if not p.is_file():raise FileNotFoundError(p)
        save('PLAN_R10.json',{'status':'CONDITIONAL_COVARIANT_SECTOR_COMPOSITION',
             'scope':'Nonrelativistic matter normalization at fixed/shared distances and constant effective gravitational coupling; no additional scalar, spin, modular anisotropic or nonmetric photon effect.',
             'checks':['constant-w action closure','dust multiplier','same Fermat functional after mass map','same acceleration after mass map','profiled Fisher zero','varying-w pressure derivative retained'],
             'sources':[pin(p) for p in sources], 'script':pin(__file__),
             'operator_authorization':'Original lens goal and candidate_r9/OPERADOR_VERBATIM.txt',
             'observed_data_composed':False,'new_parameter_choice':False})
        print('PLAN_WRITTEN');raise SystemExit(0)
    if phase!='run':raise ValueError(phase)
    if (BASE/'RESULT_R10.json').exists():raise FileExistsError('RESULT_R10.json')
    plan=json.loads((BASE/'PLAN_R10.json').read_text(encoding='utf-8'))
    for item in plan['sources']+[plan['script']]:assert pin(item['path'])==item,item['path']
    matches=[]
    for i,line in enumerate(PROGRAM.read_text(encoding='utf-8').splitlines(),1):
        m=re.fullmatch(r'ALPHA_FINE_CODATA_2018\s*=\s*(.+)',line)
        if m:matches.append((i,ast.literal_eval(m.group(1))))
    assert len(matches)==1
    line,alpha=matches[0];beta_runtime=alpha*math.sqrt(math.e)
    n,C=s.symbols('n C',positive=True)
    w,beta=s.symbols('w beta',real=True)
    rho=C*n**(1+w);p=n*s.diff(rho,n)-rho;A=1+beta*(1+w)
    checks={'constant_w_pressure':s.simplify(n*s.diff(A*rho,n)-A*rho-A*p),
            'dust_multiplier':s.simplify(A.subs(w,0)-(1+beta))}
    M,D,q,y,j=s.symbols('M D theta source j',real=True)
    f=s.Function('potential_shape')(q)
    A0=1+beta
    fermat_T=D*((q-y)**2/2-A0*M*f)
    Mg=s.symbols('M_GR',real=True)
    fermat_GR=D*((q-y)**2/2-Mg*f)
    checks['fermat_identical']=s.simplify(fermat_T-fermat_GR.subs(Mg,A0*M))
    checks['lens_stationarity_identical']=s.simplify(s.diff(fermat_T,q)-s.diff(fermat_GR.subs(Mg,A0*M),q))
    checks['stellar_acceleration_identical']=s.simplify(A0*M*j-(Mg*j).subs(Mg,A0*M))
    # Whitened derivative wrt beta is the log-mass column divided by (1+beta).
    norm2=s.symbols('positive_nuisance_column_norm_squared',positive=True)
    checks['profiled_fisher']=s.simplify(norm2/A0**2-(norm2/A0)**2/norm2)
    rhof=s.Function('rho')(n);pf=n*s.diff(rhof,n)-rhof
    r_eff=rhof+beta*n*s.diff(rhof,n)
    p_eff=n*s.diff(r_eff,n)-r_eff
    checks['varying_w_pressure']=s.simplify(p_eff-pf-beta*n*s.diff(pf,n))
    assert all(v==0 for v in checks.values()),checks
    save('RESULT_R10.json',{'status':'PASS_EXACT_DEGENERACY_WITH_NAMED_SCOPE',
        'checks':{k:str(v) for k,v in checks.items()},'runtime_alpha_source_line':line,
        'alpha_source':pin(PROGRAM),'beta_runtime':beta_runtime,'dust_mass_ratio_GR_to_TGL':1+beta_runtime,
        'log_mass_shift':math.log1p(beta_runtime),
        'ideal_independent_log_mass_sigma_for_median_5':math.log1p(beta_runtime)/5,
        'profiled_local_signal':'EXACTLY_ZERO_WITH_FREE_MASS_NORMALIZATION',
        'limits':['This is the named covariant material closure, not a uniquely selected local TGL completion.',
                  'No prediction for the extra source, scalar branch, distance law or laboratory G follows.',
                  'The mass-precision number assumes all other errors zero, no calibration shift and independent external mass; necessary optimistic benchmark, not detection power.',
                  'No observed data or centers used.'],
        'plan':pin(BASE/'PLAN_R10.json'),'script':pin(__file__),'sympy':s.__version__})
    print(json.dumps({'status':'PASS','checks':len(checks),'result':pin(BASE/'RESULT_R10.json')},ensure_ascii=False))
