"""Preregistered finite F1.ATRATOR synthetic experiment. No production imports or writes."""
from pathlib import Path
import ast, re, datetime, hashlib, json, math, platform, sys, time
import numpy as np
from scipy.linalg import expm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG = ROOT / 'PREREGISTRO_R1.json'

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write_new(path, obj):
    with Path(path).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')

def matrix(a):
    a = np.asarray(a)
    return np.stack([a.real, a.imag], axis=-1).tolist()

def norm(a):
    return float(np.linalg.norm(a, ord=2))

def verify_finite(obj):
    if isinstance(obj, dict):
        for value in obj.values(): verify_finite(value)
    elif isinstance(obj, (list, tuple)):
        for value in obj: verify_finite(value)
    elif isinstance(obj, (float, np.floating)) and not math.isfinite(obj):
        raise ValueError('Nonfinite number in result')

def check_preregistered_sources(p):
    for item in p['source_pins']:
        if digest(item['path']) != item['sha256']:
            raise ValueError('Source pin changed: ' + item['path'])


def run():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    start = time.perf_counter()
    manifest = json.loads((HERE / 'RUN_MANIFEST_R3.json').read_text(encoding='utf-8'))
    if digest(__file__) != manifest['script_sha256'] or digest(PREREG) != manifest['preregister_sha256']:
        raise ValueError('Run or preregister pin changed')
    p = json.loads(PREREG.read_text(encoding='utf-8'))
    check_preregistered_sources(p)
    nm = p['numerics']
    atol, rtol = nm['absolute_tolerance'], nm['relative_tolerance']
    threshold = nm['rank_threshold']
    band_lo, band_hi = nm['rank_ambiguity_band']
    def close_error(error, scale=1.): return bool(error <= atol + rtol * scale)
    um = next(x for x in p['source_pins'] if Path(x['path']).name == 'um.py')
    um_text = Path(um['path']).read_bytes().decode('utf-8-sig')
    tree = ast.parse(um_text)
    # The only physical line with this unindented assignment is inside a source literal.
    # Parse that assignment as code; never execute the wrapper or the embedded module.
    matches = list(re.finditer(r'^ALPHA_FINE_CODATA_2018[ \t]*=[ \t]*([^\r\n]+)\r?$', um_text, re.MULTILINE))
    if len(matches) != 1: raise ValueError('Alpha unindented source-line assignment is not unique')
    assignment = ast.parse(matches[0].group(0)).body[0]
    alpha = ast.literal_eval(assignment.value)
    sealed = [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'SEALED_CODATA_ALPHA' for t in n.targets)]
    if len(sealed) != 1 or ast.literal_eval(sealed[0].value) != alpha:
        raise ValueError('Embedded alpha differs from top-level sealed alpha')
    alpha_source_line = um_text[:matches[0].start()].count('\n') + 1
    if isinstance(alpha, bool) or not isinstance(alpha, (float, int)) or not math.isfinite(alpha):
        raise ValueError('Invalid alpha')
    beta = float(alpha * math.sqrt(math.e))
    if not 0. < beta < .5: raise ValueError('Primary strict-complement range failed')
    lam = 1. - 2. * beta
    c, s = math.sqrt(1. - beta), math.sqrt(beta)
    S = np.array([[c,s],[-s,c]], dtype=np.complex128)
    I2 = np.eye(2, dtype=np.complex128)
    X = np.array([[0,1],[1,0]], dtype=np.complex128)
    Y = np.array([[0,-1j],[1j,0]], dtype=np.complex128)
    Z = np.diag([1.,-1.]).astype(np.complex128)
    basis = [a / math.sqrt(2.) for a in [I2,X,Y,Z]]
    def to_vec(a): return np.array([np.trace(b.conj().T @ a) for b in basis])
    def from_vec(v): return sum((z*b for z,b in zip(v,basis)), np.zeros((2,2),complex))
    def dephase(a): return np.diag(np.diag(a))
    def full(a): return dephase(S @ dephase(a) @ S.conj().T)
    decay = math.exp(-1.)
    def rotated(a):
        b = S @ a @ S.conj().T
        b = decay*b+(1.-decay)*dephase(b)
        return S.conj().T @ b @ S
    def superoperator(fn):
        return np.column_stack([to_vec(fn(b)) for b in basis])
    Tpop = np.abs(S)**2
    Rpop = np.ones((2,2))/2.
    Cfull = superoperator(full)
    Rfull = np.diag([1.,0.,0.,0.])
    Crot = superoperator(rotated)
    def rotated_projection(a): return S.conj().T @ dephase(S @ a @ S.conj().T) @ S
    Rrot = superoperator(rotated_projection)
    rng = np.random.default_rng(nm['seed'])
    pops = rng.dirichlet([1.,1.], size=nm['random_population_states'])
    pops = np.vstack([pops,np.eye(2)])
    density = []
    for _ in range(nm['random_density_states']):
        a = rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
        rho = a @ a.conj().T
        density.append(rho / np.trace(rho))
    density += [np.diag([1.,0.]), np.diag([0.,1.])]
    density += [np.outer(v,v.conj()) for v in [np.array([1.,1.])/math.sqrt(2.),np.array([1.,1j])/math.sqrt(2.)]]
    dv = np.array([to_vec(r) for r in density])
    # Exact component formulas come from registered channels, not their numerical eigendecomposition.
    models = [
        ('primary_population',Tpop,Rpop,[(lam,np.eye(2)-Rpop)],pops,True),
        ('primary_density',Cfull,Rfull,[(lam,np.diag([0.,0.,0.,1.])),(0.,np.diag([0.,1.,1.,0.]))],dv,True),
        ('identity_population',np.eye(2),np.eye(2),[],pops,False),
        ('rotated_dephasing',Crot,Rrot,[(decay,np.eye(4)-Rrot)],dv,False),
    ]
    output = {}
    for name,T,R,components,states,unique_expected in models:
        T = np.asarray(T,dtype=np.complex128); R=np.asarray(R,dtype=np.complex128)
        dim=T.shape[0]; I=np.eye(dim)
        A=I-T
        u,sv,vh=np.linalg.svd(A)
        if any(band_lo <= v <= band_hi for v in sv): raise ValueError('Ambiguous rank ' + name)
        fix=vh.conj().T[:,sv<threshold]
        Rsvd=fix @ fix.conj().T
        eig,vec=np.linalg.eigh((T+T.conj().T)/2)
        if any(band_lo <= abs(v-1.) <= band_hi for v in eig): raise ValueError('Ambiguous spectral rank '+name)
        spec=vec[:,abs(eig-1.)<threshold]; Rspec=spec @ spec.conj().T
        e=np.ones(2)/math.sqrt(2.) if dim==2 else np.array([1.,0.,0.,0.])
        E=np.outer(e,e)
        complement_norm=norm(T @ (I-E))
        hypothesis=bool(norm(T@e-e)<=atol and complement_norm < 1.-threshold)
        residuals={'RT':norm(R@T-R),'TR':norm(T@R-R),'idempotence':norm(R@R-R),'selfadjoint':norm(R-R.conj().T),'spectral_projector':norm(R-Rspec),'svd_projector':norm(R-Rsvd),'lands_fixed':norm(A@R),'fixes_fixed':norm(R@fix-fix),'T_selfadjoint':norm(T-T.conj().T)}
        power_rows=[]
        for n in nm['powers']:
            actual=np.linalg.matrix_power(T,n)
            expected=R.copy()
            for value,Q in components: expected += (value**n)*Q
            bound=max([abs(value)**n for value,Q in components] or [0.])
            err=norm(actual-expected); dist=norm(actual-R)
            sample=max(float(np.linalg.norm(actual@x-R@x)) for x in states)
            power_rows.append({'n':n,'formula_residual':err,'distance_to_R':dist,'registered_bound':bound,'bound_ok':close_error(max(0.,dist-bound)),'sample_max_distance':sample,'formula_ok':close_error(err)})
        means=[]
        for N in nm['cesaro_lengths']:
            P=I.copy(); total=np.zeros_like(T)
            for _ in range(N): total+=P; P=T@P
            actual=total/N
            expected=R.copy()
            for value,Q in components: expected+=((1.-value**N)/(N*(1.-value)))*Q
            err=norm(actual-expected); dist=norm(actual-R)
            bound=max([1./(N*(1.-abs(value))) for value,Q in components] or [0.])
            means.append({'N':N,'formula_residual':err,'distance_to_R':dist,'registered_bound':bound,'formula_ok':close_error(err),'bound_ok':close_error(max(0.,dist-bound))})
        # q(z)=product(z-a) over distinct nonzero spectral values a of A, not of T.
        roots=sorted(set([1.-value for value,Q in components]))
        polynomial=I.copy(); q0=1.
        for root in roots: polynomial=polynomial@(A-root*I); q0*= -root
        letter=polynomial/q0
        residuals['normalized_letter']=norm(letter-R)
        residuals['A_q_A_annihilator']=norm(A@polynomial)
        flags={
            'A1':all(x['formula_ok'] and x['bound_ok'] for x in power_rows+means) and power_rows[-1]['distance_to_R']<=atol,
            'A2':residuals['RT']<=atol and residuals['TR']<=atol,
            'A3':all(v<=atol for k,v in residuals.items() if k not in ['RT','TR']),
            'A4':fix.shape[1]==1 and hypothesis,
        }
        expectedflags={'A1':True,'A2':True,'A3':True,'A4':unique_expected}
        output[name]={'matrix':matrix(T),'R':matrix(R),'R_svd':matrix(Rsvd),'R_spectral':matrix(Rspec),'eigenvalues':eig.tolist(),'I_minus_T_singular_values':sv.tolist(),'fixed_dimension':int(fix.shape[1]),'rank_I_minus_T':int(np.count_nonzero(sv>=threshold)),'spectral_gap_to_fixed':float(min([abs(v-1.) for v in eig if abs(v-1.)>=threshold],default=0.)),'nonzero_singular_condition':float(max([v for v in sv if v>=threshold],default=1.)/min([v for v in sv if v>=threshold],default=1.)),'strict_complement_hypothesis':hypothesis,'strict_complement_operator_norm':complement_norm,'fixed_vector':matrix(e),'residuals':residuals,'letter':{'A':'I-T','roots_q':roots,'q0':q0,'matrix':matrix(letter)},'powers':power_rows,'cesaro':means,'sample_count':len(states),'claims':{k:'PASSA' if v else ('FALHA_SEM_HIPOTESE' if k=='A4' and not hypothesis else 'FALHA') for k,v in flags.items()},'expected':expectedflags,'expected_outcomes_met':flags==expectedflags}
    # Independent physical channel checks from matrix units, positivity and trace.
    channels={}
    for name,fn,T in [('primary_density',full,Cfull),('rotated_dephasing',rotated,Crot)]:
        choi=np.zeros((4,4),complex)
        for i in range(2):
            for j in range(2):
                E=np.zeros((2,2),complex);E[i,j]=1.
                choi+=np.kron(E,fn(E))
        partial=np.einsum('iaja->ij',choi.reshape(2,2,2,2))
        min_eigen=float(np.linalg.eigvalsh((choi+choi.conj().T)/2).min())
        tp=norm(partial-I2)
        minstate=1.;trace=0.;hermitian=0.;nonlinear=0.
        for rho in density:
            for n in nm['powers']:
                out=from_vec(np.linalg.matrix_power(T,n)@to_vec(rho))
                minstate=min(minstate,float(np.linalg.eigvalsh((out+out.conj().T)/2).min()))
                trace=max(trace,float(abs(np.trace(out)-1.)))
                hermitian=max(hermitian,norm(out-out.conj().T))
            nonlinear=max(nonlinear,norm(fn(rho)-from_vec(T@to_vec(rho))))
        channels[name]={'choi':matrix(choi),'choi_min_eigenvalue':min_eigen,'trace_preservation_residual':tp,'sample_min_eigenvalue_over_powers':minstate,'max_trace_error_over_powers':trace,'max_hermitian_error':hermitian,'superoperator_reconstruction_error':nonlinear,'PASSA':bool(min_eigen>=-atol and minstate>=-atol and max(tp,trace,hermitian,nonlinear)<=atol)}
    a=-math.log(lam)/2.
    hyperbolic={'a':a,'normalized_exponential':matrix(expm(a*(X-I2))),'residual':norm(Tpop-expm(a*(X-I2))),'scope':'Population channel only; not full D Ad(S) D or canonical boost identification'}
    hyperbolic['PASSA']=hyperbolic['residual']<=atol
    optical={'S':matrix(S),'unitarity_residual':norm(S.conj().T@S-I2),'reflection_weight':float(abs(S[1,0])**2),'reflection_beta_residual':float(abs(abs(S[1,0])**2-beta)),'column_sums':Tpop.sum(axis=0).tolist(),'population_positivity_min':float(Tpop.min())}
    optical['PASSA']=bool(max(optical['unitarity_residual'],optical['reflection_beta_residual'])<=atol)
    affine={'scope':'OUTSIDE_LINEAR_CPTP_CLASS','equation':'x+1=x implies 1=0','x0':0,'trajectories':[{'n':n,'x_n':n} for n in nm['powers']],'cesaro':[{'N':N,'mean':(N-1)/2} for N in nm['cesaro_lengths']],'claims':{'A1_direct':'FALHA','A1_cesaro':'FALHA'},'reason':'Both sequences diverge to positive infinity, analytically; there is no fixed point.','expected_outcomes_met':True}
    fixed_examples={
        'identity_population':[matrix(np.array([1.,0.])),matrix(np.array([0.,1.]))],
        'rotated_dephasing':[matrix(S.conj().T@np.diag([1.,0.])@S),matrix(S.conj().T@np.diag([0.,1.])@S)],
        'primary_population_normalized':[.5,.5],
        'primary_density_normalized':matrix(I2/2.),
    }
    all_ok=all(x['expected_outcomes_met'] for x in output.values()) and all(x['PASSA'] for x in channels.values()) and optical['PASSA'] and hyperbolic['PASSA']
    result={'unit':'F1.ATRATOR','started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.perf_counter()-start,'environment':{'python':sys.version,'platform':platform.platform(),'numpy':np.__version__},'preregister_sha256':digest(PREREG),'script_sha256':digest(__file__),'um_sha256':digest(um['path']),'alpha':alpha,'alpha_assignment_line':alpha_source_line,'alpha_reader_scope':'Unique unindented source line in embedded module; cross-checked with wrapper SEALED_CODATA_ALPHA AST top level','beta_runtime':beta,'lambda':lam,'lambda_runtime':lam,'maximum_iteration':max(nm['powers']),'per_step_transient_contraction':lam,'transient_decay_rate_per_step':-math.log(lam),'probability_loss_per_step':0.0,'hypothesis_snapshot':p['hypotheses'],'normalization':p['claims']['A4']['normalization'],'theta':math.asin(math.sqrt(beta)),'tolerances':{k:nm[k] for k in ['absolute_tolerance','relative_tolerance','rank_threshold','rank_ambiguity_band','positivity_tolerance']},'models':output,'channel_checks':channels,'optical':optical,'normalized_hyperbolic_representation':hyperbolic,'no_fixed_affine':affine,'nonvacuity_and_fixed_examples':fixed_examples,'all_expected_outcomes_met':all_ok,'scope':'REAL numerical finite checks; DERIVED analytic bounds; no empirical sigma or physical creditation; ontology remains ONTO','observed_data':False,'gate_changed':False,'production_runs':False}
    verify_finite(result)
    check_preregistered_sources(p)
    write_new(HERE/'RESULTADOS_NUMERICOS_R3.json',result)
    print(json.dumps({'all_expected_outcomes_met':all_ok,'beta':beta,'lambda':lam,'models':{k:{'claims':v['claims'],'fixed_dimension':v['fixed_dimension'],'final_distance':v['powers'][-1]['distance_to_R'],'complement_norm':v['strict_complement_operator_norm']} for k,v in output.items()},'channels':{k:v['PASSA'] for k,v in channels.items()},'hyperbolic_residual':hyperbolic['residual'],'elapsed_seconds':result['elapsed_seconds']},ensure_ascii=False,indent=2,allow_nan=False))
    return 0 if all_ok else 1

if __name__=='__main__':
    raise SystemExit(run())
