def _v394_independent_liouvillian(energies_j, v0_j, hbar_js, beta):
    import numpy as np
    lo, hi = energies_j
    g = _v394_geometry()
    h = lo*g['Pplus'] + hi*g['Pminus']
    jump = (beta/hbar_js)**.5 * (lo**.5*g['Pplus'] + hi**.5*g['Pminus'])
    gram = jump.conj().T @ jump
    eye = g['I']
    return (-1j/hbar_js*(np.kron(eye, h)-np.kron(h.T, eye))
            + np.kron(jump.conj(), jump)
            - .5*np.kron(eye, gram)-.5*np.kron(gram.T, eye))