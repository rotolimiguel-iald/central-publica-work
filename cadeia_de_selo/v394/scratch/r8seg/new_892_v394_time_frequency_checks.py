def v394_time_frequency_checks(parameter_function, alpha, hbar):
    """Numerically cross-check matrix law against independently exponentiated GKLS.

    The caller supplies the independently typed physical-parameter constructor.
    Values are synthetic reference energies, never fitted to observed data.
    """
    import math
    import numpy as np
    from scipy.linalg import expm
    g = _v394_geometry()
    checks = []
    maxima = {}
    def check(name, condition, residual=None, tolerance=None):
        ok = bool(condition)
        if residual is not None:
            ok = ok and math.isfinite(float(residual))
        checks.append(dict(name=name, ok=ok, residual=residual, tolerance=tolerance))
    def close(name, a, b, tol=2e-10):
        r = float(np.linalg.norm(a-b))
        check(name, r <= tol, r, tol)
        maxima[name.split(':')[0]] = max(r, maxima.get(name.split(':')[0], 0.))
    close('matrix:C_X_Cstar',g['C']@g['X']@g['C'].conj().T,g['Y'])
    close('matrix:C_Px_Cstar',g['C']@((g['I']+g['X'])/2)@g['C'].conj().T,g['Pplus'])
    close('matrix:graviton_factor',g['hplus']@g['hminus']/4,g['Pplus'])
    close('matrix:tensor_square_is_not_matrix_square',g['hplus']@g['hplus'],np.zeros((2,2)))
    close('matrix:state_transport',g['rho0'],(g['I']-g['X'])/2)
    close('matrix:fixed_target',_v394_read(g['rho0']),g['I']/2)
    target = g['I']/2  # Pinned independently of outputs.
    rng=np.random.default_rng(20261015)
    states=[g['rho0'],g['Pplus'],g['Pminus'],target]
    for _ in range(8):
        z=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)); rho=z@z.conj().T
        states.append(rho/np.trace(rho))
    summaries=[]
    for omega_ref in (.25,1.,3.,10.):
        for offset in (1.,2.,100.):
            p=parameter_function(omega_ref*hbar,offset*omega_ref*hbar,hbar,alpha)
            omega=p['Omega_rad_s']; gamma=p['gamma_s_inv']; beta=p['beta']
            label=f'{omega_ref}:{offset}'
            check('physical:beta_runtime:'+label,abs(beta-alpha*math.sqrt(math.e))<1e-16)
            # Fixed reference time t=1/Omega, not a fitted energy/time datum.
            v0=omega_ref*hbar
            hg=1j*v0*g['K']
            close('hamiltonian:transport:'+label,g['C']@(-v0*g['X'])@g['C'].conj().T/hbar,hg/hbar)
            liouv=_v394_independent_liouvillian(p['energies_J'],v0,hbar,beta)
            check('physical:rate_bound:'+label,0<gamma/(2*omega)<=beta/2+1e-14)
            if offset==1: close('physical:ground_rate:'+label,gamma, beta*omega)
            tgrid=[0.,.2/omega,1/omega,2*math.pi/omega,10/omega,40/omega]
            max_ind=0.
            for j,t in enumerate(tgrid):
                for i,rho in enumerate(states):
                    y=_v394_channel(rho,t,omega,gamma)
                    independent=(expm(t*liouv)@rho.reshape(-1,order='F')).reshape((2,2),order='F')
                    max_ind=max(max_ind,float(np.linalg.norm(y-independent)))
                    close('gkls:'+label+f':{j}:{i}',y,independent)
                    close('reading:'+label+f':{j}:{i}',_v394_read(y),_v394_read(rho))
                    close('semigroup:'+label+f':{j}:{i}',_v394_channel(_v394_channel(rho,t*.37,omega,gamma),t*.63,omega,gamma),y)
                    close('trace:'+label+f':{j}:{i}',np.trace(y),1.)
                    check('positivity:'+label+f':{j}:{i}',float(np.linalg.eigvalsh(y).min())>=-1e-10)
                    close('energy:'+label+f':{j}:{i}',np.trace((hg/v0)@y),np.trace((hg/v0)@rho))
                c0=g['plus'].conj()@g['rho0']@g['minus']
                c1=g['plus'].conj()@_v394_channel(g['rho0'],t,omega,gamma)@g['minus']
                expected=np.exp((-gamma+2j*omega)*t)*c0
                close('coherence:'+label+f':{j}',c1,expected)
                close('clock_modulus:'+label+f':{j}',_v394_clock_modulus(c0,c1,gamma)*omega,t*omega,tol=1e-8)
                close('clock_phase:'+label+f':{j}',_v394_clock_phase(2*omega*t,omega)*omega,t*omega,tol=1e-11)
                check('rule:admit:'+label+f':{j}',_v394_rule(_v394_channel(g['rho0'],t,omega,gamma),target)['admitted'])
                check('rule:reject:'+label+f':{j}',not _v394_rule(_v394_channel(g['rho0'],t,omega,gamma),g['Pplus'])['admitted'])
            echo_dt=p['echo_dt_s'];eta=p['eta']
            close('echo:continuous_coherence_factor:'+label,math.exp(-gamma*echo_dt),eta,tol=1e-12)
            raw=np.array([[.2,.3+.4j],[-.7+.5j,1.2]],dtype=complex)
            for mode,sign in ((g['hplus'],1),(g['hminus'],-1)):
                got=(liouv@mode.reshape(-1,order='F')).reshape((2,2),order='F')
                close('generator:mode:'+label+':'+str(sign),got/omega,((-gamma+sign*2j*omega)*mode)/omega)
            t=1/omega
            choi=np.zeros((4,4),dtype=complex)
            for a in range(2):
                for b in range(2):
                    e=np.zeros((2,2),dtype=complex);e[a,b]=1
                    choi+=np.kron(e,_v394_channel(e,t,omega,gamma))
            check('choi:'+label,float(np.linalg.eigvalsh(choi).min())>=-1e-10)
            close('nonmultiplicative:correct_factor:'+label,
                  _v394_channel(g['hplus'],t,omega,gamma)@_v394_channel(g['hminus'],t,omega,gamma)/4,
                  math.exp(-2*gamma*t)*g['Pplus'])
            check('nonmultiplicative:counterexample:'+label,
                  np.linalg.norm(_v394_channel(g['hplus'],t,omega,gamma)@_v394_channel(g['hminus'],t,omega,gamma)/4-g['Pplus'])>1e-8)
            check('fixed_space:dimension2:'+label,int(np.count_nonzero(np.linalg.svd(liouv/omega,compute_uv=False)<1e-10))==2)
            long_t=12/gamma
            close('decay:asymptotic_norm:'+label,
                  np.linalg.norm(_v394_channel(g['rho0'],long_t,omega,gamma)-target),
                  math.exp(-12)*np.linalg.norm(g['rho0']-target),tol=1e-12)
            pp=parameter_function(2*v0,2*offset*v0,hbar,alpha)
            close('clock:rescaling:'+label,_v394_channel(raw,t,omega,gamma),
                  _v394_channel(raw,t/2,pp['Omega_rad_s'],pp['gamma_s_inv']))
            summaries.append(dict(omega_rad_s=omega,offset_ratio=offset,gamma_s_inv=gamma,
                                  echo_dt_s=echo_dt,gamma_over_relative_frequency=gamma/(2*omega),max_gkls_residual=max_ind))
    close('clock_phase:overflow_avoided',_v394_clock_phase(1e308,1e308),.5)
    # Controls test genuine failures, independent of the main verdict.
    def refused(name,fn):
        try: fn()
        except (ValueError,TypeError,OverflowError): check(name,True)
        else: check(name,False)
    for bad in (True,float('nan'),float('inf'),-1):
        refused('negative_input:time:'+repr(bad),lambda bad=bad:_v394_channel(g['rho0'],bad,1.,.1))
        refused('negative_input:rate:'+repr(bad),lambda bad=bad:_v394_channel(g['rho0'],1.,1.,bad))
    refused('clock_phase:unrepresentable',lambda:_v394_clock_phase(1.,5e-324))
    refused('clock_phase:underflow',lambda:_v394_clock_phase(5e-324,1e308))
    refused('negative_input:zero_coherence',lambda:_v394_clock_modulus(0j,.2j,.1))
    refused('negative_input:zero_rate_clock',lambda:_v394_clock_modulus(.3j,.2j,0))
    refused('negative_input:increasing_coherence',lambda:_v394_clock_modulus(.1j,.2j,.1))
    refused('negative_input:nonfixed_target',lambda:_v394_rule(g['rho0'],g['rho0']))
    close('zero_rate:no_convergence',np.linalg.norm(_v394_channel(g['rho0'],7.,1.,0.)-target),np.linalg.norm(g['rho0']-target))
    # Same samples, different intermediate phases: a negative uniqueness control.
    tstep=.7;omega=1.;alias=omega+math.pi/tstep
    close('alias:sample_agrees',_v394_channel(g['rho0'],tstep,omega,.1),_v394_channel(g['rho0'],tstep,alias,.1))
    check('alias:between_samples_differs',np.linalg.norm(_v394_channel(g['rho0'],tstep/2,omega,.1)-_v394_channel(g['rho0'],tstep/2,alias,.1))>.1)
    return {'passed':all(c['ok'] for c in checks),'checks':checks,'check_count':len(checks),
            'failed':[c for c in checks if not c['ok']],'maxima':maxima,'parameter_cases':summaries,
            'scope':'Synthetic M2 calculation with explicit positive energy reference. No observed data, no universal atomic identification.',
            'gate_changed':False}