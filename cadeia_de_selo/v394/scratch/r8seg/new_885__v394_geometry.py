def _v394_geometry():
    import numpy as np
    i = np.eye(2, dtype=complex)
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    k = np.array([[0, 1], [-1, 0]], dtype=complex)
    ep = np.array([1, 1j], dtype=complex)
    em = np.conj(ep)
    pp, pm = np.outer(ep, ep.conj())/2, np.outer(em, em.conj())/2
    hp, hm = np.outer(ep, ep), np.outer(em, em)
    c = np.diag([1, 1j])
    original = np.array([1, 1j])/np.sqrt(2)
    state = c @ original
    return dict(I=i, X=x, Y=y, K=k, C=c, Pplus=pp, Pminus=pm,
                hplus=hp, hminus=hm, plus=ep/np.sqrt(2), minus=em/np.sqrt(2),
                rho0=np.outer(state, state.conj()))