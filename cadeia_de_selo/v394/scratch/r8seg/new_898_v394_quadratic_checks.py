def v394_quadratic_checks():
    """Check the compiled reading law, including false and impossible targets.

    A zero criterion in Lean is exact. Floating point uses the fixed squared
    tolerance below and never promotes numerical closeness to exact equality.
    The residual is constant along this flow, not a dissipative progress score.
    """
    import math
    import numpy as np
    g = _v394_geometry()
    target = g['I'] / 2
    tol = 2e-10
    rule_tol = 1e-10
    checks = []

    def close(name, left, right, tolerance=tol):
        error = float(np.linalg.norm(np.asarray(left)-np.asarray(right)))
        checks.append({'name': name, 'ok': math.isfinite(error) and error <= tolerance,
                       'error': error, 'tolerance': tolerance})

    def check(name, value):
        checks.append({'name': name, 'ok': bool(value)})

    close('concrete:accepted', _v394_quadratic_residual(g['rho0'], target), 0)
    close('concrete:rejected_half', _v394_quadratic_residual(g['rho0'], g['Pplus']), .5)
    check('concrete:distinct_raw_state', np.linalg.norm(g['rho0']-target) > .5)
    close('noninjective:same_reading', _v394_read(g['rho0']), _v394_read(target))
    close('polarization:is_not_reading_image', _v394_read(g['hplus']), np.zeros((2, 2)))
    close('impossible_target:lower_bound_at_projection',
          _v394_quadratic_residual(target, g['rho0']), .5)
    rng = np.random.default_rng(2026101501)
    states = [g['rho0'], target, g['Pplus'], g['Pminus']]
    states += [rng.normal(size=(2,2)) + 1j*rng.normal(size=(2,2)) for _ in range(8)]
    targets = [target, g['Pplus'], g['Pminus'], g['rho0']]
    for i, state in enumerate(states):
        for j, anchor in enumerate(targets):
            residual = _v394_quadratic_residual(state, anchor)
            check(f'positive:{i}:{j}', residual >= 0)
            close(f'frobenius:{i}:{j}', residual, np.linalg.norm(_v394_read(state)-anchor, 'fro')**2)
            for omega, gamma, time in ((.25,.01,0), (1,.03,2), (3,.7,20)):
                evolved = _v394_channel(state, time, omega, gamma)
                close(f'invariant:{i}:{j}:{omega}', _v394_quadratic_residual(evolved, anchor), residual)
            if i < 4 and j < 3:
                old = _v394_rule(state, anchor, rule_tol)
                close(f'prior_rule:{i}:{j}', old['residual']**2, residual)
                check(f'admission:{i}:{j}', old['admitted'] == (residual <= rule_tol**2))

    def refused(name, callback):
        try:
            callback()
        except (ValueError, TypeError, OverflowError):
            check(name, True)
        else:
            check(name, False)

    for value in (float('nan'), float('inf')):
        refused('refuse_nonfinite:'+repr(value), lambda value=value:
                _v394_quadratic_residual(np.full((2,2), value), target))
    refused('refuse_shape', lambda: _v394_quadratic_residual(np.zeros(2), target))
    refused('refuse_overflow', lambda: _v394_quadratic_residual(np.eye(2)*1e308, -np.eye(2)*1e308))
    return {'passed': all(x['ok'] for x in checks), 'check_count': len(checks),
            'checks': checks, 'failed': [x for x in checks if not x['ok']],
            'fixed_tolerance': tol, 'admission_squared_tolerance': rule_tol**2,
            'scope': 'Synthetic finite M2 reading; exact equivalence is the Lean theorem, not floating-point inference.'}