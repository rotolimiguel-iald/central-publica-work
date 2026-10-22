"""Synthetic diagnostic, standard library only; no observational significance."""
from pathlib import Path
from datetime import datetime, timezone
import cmath, hashlib, json, math, random, statistics, time
B=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def mul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def comm(a,t):
    c,s=math.cos(t), math.sin(t)
    z=[[c*c-s*s,-2*c*s],[-2*c*s,s*s-c*c]]
    x,y=mul(a,z),mul(z,a)
    return max(abs(x[i][j]-y[i][j]) for i in range(2) for j in range(2))
def projector(phi):
    c,s=math.cos(phi), math.sin(phi)
    return [[c*c,c*s],[c*s,s*s]]
def main():
    out=B/'RESULT_SYNTHETIC_R1.json'
    if out.exists(): raise RuntimeError('Refuse overwriting prior result')
    start=datetime.now(timezone.utc); tick=time.perf_counter()
    pre=json.loads((B/'PREREG_SYNTHETIC_R1.json').read_text(encoding='utf8'))
    cust=json.loads((B/'CUSTODY_R1.json').read_text(encoding='utf8'))
    assert sha(Path(cust['um']['path']))==cust['um']['sha256']
    for s in cust['sources']:
        assert sha(Path(s['original']))==s['sha256']==sha(Path(s['copy']))
    beta=cust['alpha_source']['value']*math.sqrt(math.e)
    theta=math.asin(math.sqrt(beta)); c=pre['c_m_s']; logq=math.log1p(-beta)
    checks=[]
    def check(name,v): checks.append(dict(name=name,pass_=bool(v)))
    table=[]
    for length in pre['lengths_km']:
        t0=length*1000/c
        qs={str(q):math.ceil(math.log1p(-q)/logq) for q in pre['quantiles']}
        for q,n in qs.items():
            check(f'quantile bracket {length}km {q}', -math.expm1((n-1)*logq)<float(q)<=-math.expm1(n*logq))
        table.append(dict(length_km=length,free_crossing_ms=1000*t0,
            total_mean_ms=1000*t0/beta,excess_mean_ms=1000*t0*(1-beta)/beta,
            sd_ms=1000*t0*math.sqrt(1-beta)/beta,
            total_quantiles_ms={q:n*t0*1000 for q,n in qs.items()},
            alternative_success_transmission_mean_ms=1000*t0/(1-beta)))
    rng=random.Random(pre['seed'])
    samples=[math.floor(math.log1p(-rng.random())/logq)+1 for _ in range(pre['mc_samples'])]
    mu=statistics.mean(samples); sd=statistics.pstdev(samples)
    exact_mu=1/beta; exact_sd=math.sqrt(1-beta)/beta
    check('MC mean',abs(mu/exact_mu-1)<pre['tolerances']['mc_mean_relative'])
    check('MC SD',abs(sd/exact_sd-1)<pre['tolerances']['mc_sd_relative'])
    check('excess identity',abs((exact_mu-1)-(1-beta)/beta)<1e-12)
    angles=[]
    for deg in [6.2973,20,40]:
        phi=math.radians(deg); residue=comm(projector(phi),-phi)
        angles.append(dict(projector_deg=deg,selector_deg=-deg,residue=residue))
        check(f'arbitrary angle {deg}',residue<1e-12)
    check('identity has no unique angle',all(comm([[1,0],[0,1]],t)<1e-12 for t in [0,theta,0.4,1.2]))
    # Dimensionless E and hbar=1, S(E)=exp(i E d) O(theta).
    # Q=-i S^dagger dS/dE = d I analytically despite fixed mixing.
    delay=0.7; energy=1.3; phase=cmath.exp(1j*energy*delay)
    q=-1j*phase.conjugate()*(1j*delay*phase)
    check('constant angle nonzero Wigner delay counterexample',abs(q-delay)<1e-12)
    t=table[1]['total_mean_ms']
    check('equal GW/nu mean delay cancels',t-t==0)
    check('mean l/beta degeneracy',abs((20/beta)-(40/(2*beta)))<1e-12)
    min_wait=[dict(simultaneous_independent_packets=m,mean_min_attempts=1/(-math.expm1(m*logq))) for m in [1,10,100]]
    check('first arrival mean differs',min_wait[1]['mean_min_attempts']<exact_mu)
    result=dict(start_utc=start.isoformat(),end_utc=datetime.now(timezone.utc).isoformat(),seconds=time.perf_counter()-tick,
      beta_runtime=beta,theta_degrees=math.degrees(theta),coefficient_variation=math.sqrt(1-beta),
      table=table,mc=dict(n=len(samples),seed=pre['seed'],mean_attempts=mu,sd_attempts=sd,exact_mean=exact_mu,exact_sd=exact_sd),
      arbitrary_angles=angles,minimum_wait=min_wait,checks=checks,all_checks_pass=all(x['pass_'] for x in checks),
      status='SYNTHETIC_DIAGNOSTIC_ONLY',observed_sigma=None,
      prereg_sha256=sha(B/'PREREG_SYNTHETIC_R1.json'),script_sha256=sha(Path(__file__)),
      um_unchanged=sha(Path(cust['um']['path']))==cust['um']['sha256'],
      source_files_unchanged=all(sha(Path(x['original']))==x['sha256'] for x in cust['sources']))
    with out.open('x',encoding='utf8') as f:json.dump(result,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps(dict(beta=beta,theta=result['theta_degrees'],table=table,checks=len(checks),passed=result['all_checks_pass'],observed_sigma=None),indent=2))
    if not result['all_checks_pass']:raise SystemExit(1)
if __name__=='__main__':main()
