"""Registered scalar matched-filter null calibration, streaming and bounded.

The Gaussian projection is exact for the declared synthetic covariance model.
The non-Gaussian control has elliptical Student t5 measurement noise with one
common scale per catalog PLUS independent Gaussian nuisance. The total vector
is not Student t5 when the Gaussian nuisance variance is nonzero.
"""
import numpy as np
from scipy.stats import beta

def projected_components(delta,sigma,design,nuisance_covariance):
    delta=np.asarray(delta,dtype=float);sigma=np.asarray(sigma,dtype=float)
    X=np.asarray(design,dtype=float);V=np.asarray(nuisance_covariance,dtype=float)
    if delta.ndim!=1 or sigma.shape!=delta.shape or X.shape!=(len(delta),2) or V.shape!=(2,2):raise ValueError('Null dimensions differ')
    if not all(np.isfinite(v).all() for v in [delta,sigma,X,V]) or np.any(sigma<=0):raise ValueError('Invalid synthetic null inputs')
    if not np.allclose(V,V.T,rtol=1e-10,atol=1e-14) or np.min(np.linalg.eigvalsh(V))<0:raise ValueError('Nuisance covariance is not PSD')
    # Woodbury avoids a dense N x N matrix at the prospective target N.
    W=1/(sigma*sigma)
    ev,Q=np.linalg.eigh(V);L=Q@np.diag(np.sqrt(np.maximum(ev,0)))
    U=X@L
    rhs=W*delta
    solved=rhs-W*(U@np.linalg.solve(np.eye(2)+U.T@(W[:,None]*U),U.T@rhs))
    information=float(delta@solved)
    if information<=0 or not np.isfinite(information):raise ValueError('Zero/invalid matched-filter information')
    w=solved/np.sqrt(information)
    noise=float(np.sum((w*sigma)**2));nuisance=float((X.T@w)@V@(X.T@w))
    if not np.isclose(noise+nuisance,1.,rtol=1e-7,atol=1e-10):raise ValueError('Projection variance failed')
    return {'noise_variance_fraction':noise,'nuisance_variance_fraction':nuisance,
            'signal_information_with_nuisance':information,'max_squared_signal_fraction':float(np.max((w*delta)**2)/np.sum((w*delta)**2))}

def binomial_result(k,n,alpha=.05):
    if type(k) is not int or type(n) is not int or n<=0 or not 0<=k<=n:raise ValueError('Invalid binomial counts')
    if not np.isfinite(alpha) or not 0<alpha<1:raise ValueError('Invalid binomial alpha')
    return {'false_positives':k,'draws':n,'empirical_p':k/n,
      'confidence_level':1-alpha,
      'one_sided_upper':float(beta.ppf(1-alpha,k+1,n-k)) if k<n else 1.,
      'central_interval':[float(beta.ppf(alpha/2,k,n-k+1)) if k else 0.,float(beta.ppf(1-alpha/2,k+1,n-k)) if k<n else 1.]}

def simulate_projection(components,draws,seed,model,time_guard,chunk=1000000):
    if model not in ('gaussian','elliptical_t5_measurement_plus_gaussian_nuisance'):raise ValueError('Unregistered synthetic posterior model')
    if type(draws) is not int or draws<2:raise ValueError('Invalid draw count')
    if type(chunk) is not int or chunk<1:raise ValueError('Invalid chunk size')
    if type(seed) is not int or seed<0:raise ValueError('Invalid seed')
    if not callable(time_guard):raise ValueError('Missing deadline guard')
    noise=components['noise_variance_fraction'];nuisance=components['nuisance_variance_fraction']
    if not np.isfinite([noise,nuisance]).all() or min(noise,nuisance)<0 or not np.isclose(noise+nuisance,1,rtol=1e-7,atol=1e-10):raise ValueError('Invalid projection variance')
    rng=np.random.default_rng(seed);k=0;used=0;sums=0.;squares=0.
    while used<draws:
        time_guard();n=min(chunk,draws-used)
        e=rng.standard_normal(n)
        if model=='elliptical_t5_measurement_plus_gaussian_nuisance':e*=np.sqrt(3/rng.chisquare(5,n))
        z=np.sqrt(noise)*e+np.sqrt(nuisance)*rng.standard_normal(n)
        if not np.isfinite(z).all():raise ValueError('Nonfinite null before counting')
        k+=int(np.sum(z>5));used+=n;sums+=float(z.sum());squares+=float(z@z)
    return dict(**binomial_result(k,used),seed=seed,model=model,
      mean=sums/used,variance_ddof1=(squares-sums*sums/used)/(used-1),
      threshold_one_sided=5.,components=components,
      scope='Synthetic posterior and fixed estimated covariance only; not waveform/selection/null calibration of the real experiment')
