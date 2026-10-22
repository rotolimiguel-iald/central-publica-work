"""Static first-order metric response to the written nonminimal F R coupling.

This solves metric constraints for a supplied deltaF, not the missing scalar boundary problem.
"""
from pathlib import Path
import sympy as s
import json,hashlib,datetime,time
ROOT=Path(__file__).resolve().parent
CUSTO=Path(r'C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py')
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(n,d):
    with (ROOT/n).open('x',encoding='utf-8') as f:json.dump(d,f,ensure_ascii=False,indent=2)
def main():
    for n in ['PLAN_R6_1.json','METRIC_RESULT_R6_1.json']:
        if (ROOT/n).exists():raise FileExistsError(n)
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();tic=time.perf_counter()
    save('PLAN_R6_1.json',{'status':'SYMBOLIC_PRECOMPUTATION','started_utc':start,
      'branch':'Static weak field, F=F0+f with constant positive F0. Homogeneous scalar background; scalar kinetic stress quadratic, V(background)=Vprime(background)=0. Negligible pressure and additional anisotropic/modular stress. Isolated perturbation boundary values remove homogeneous metric freedoms.',
      'source':'Written conformal FR part of Custo, NOT a claim that all TGL modular sources vanish in a lens. F=1/kappa²+2xi|Psi|² under FR/2 convention.',
      'input':'deltaF=f(x) supplied; scalar equation, modular source, boundary data and normalization NOT solved',
      'checks':['10 independent linearized Einstein components from h','metric constraints with density rho and supplied f','cancellation in U+V','nonrelativistic acceleration and null propagation'],
      'no_observed_data':True,'no_beta_inserted':True,'sources':[pin(CUSTO)],'script':pin(Path(__file__))})
    t,x,y,z=s.symbols('t x y z',real=True); coords=[t,x,y,z]; spatial=[x,y,z]
    U=s.Function('U')(x,y,z); V=s.Function('V')(x,y,z)
    eta=s.diag(-1,1,1,1); h=s.diag(-2*U,-2*V,-2*V,-2*V)
    mixed=eta*h; trace=s.trace(mixed)
    def box(q):return sum(eta[i,i]*s.diff(q,coords[i],2) for i in range(4))
    Ric=s.zeros(4)
    for a in range(4):
        for b in range(4):
            Ric[a,b]=s.expand((sum(s.diff(mixed[r,b],coords[r],coords[a])+s.diff(mixed[r,a],coords[r],coords[b]) for r in range(4))-box(h[a,b])-s.diff(trace,coords[a],coords[b]))/2)
    scalar=sum(eta[i,i]*Ric[i,i] for i in range(4))
    G=Ric-eta*scalar/2
    lap=lambda q:sum(s.diff(q,c,2) for c in spatial)
    assert s.simplify(G[0,0]-2*lap(V))==0
    F0=s.symbols('F0',positive=True); f=s.Function('f')(x,y,z); W=s.Function('W')(x,y,z)
    replacements={U:W-f/(2*F0),V:W+f/(2*F0)}
    # rho=2 F0 lap(W); this is the Poisson boundary problem of the matter source.
    T=s.zeros(4);T[0,0]=2*F0*lap(W)
    residuals=[]
    for a in range(4):
        for b in range(a,4):
            rhs=T[a,b]+s.diff(f,coords[a],coords[b])-eta[a,b]*box(f)
            residual=s.simplify(F0*G[a,b].subs(replacements).doit()-rhs)
            assert residual==0
            residuals.append({'a':a,'b':b,'residual':str(residual)})
    sumUV=s.simplify((U+V).subs(replacements));assert sumUV==2*W
    # null speed expansion, dimensionless U,V; t parameter restored by 1/c.
    e,uu,vv=s.symbols('e uu vv',real=True)
    null_time=s.series(s.sqrt((1-2*e*vv)/(1+2*e*uu)),e,0,2).removeO()
    assert s.simplify(null_time-(1-e*(uu+vv)))==0
    accel=[s.simplify(-s.diff(replacements[U],c)) for c in spatial]
    out={'status':'DERIVED_METRIC_SUBSYSTEM_CONDITIONAL','Einstein00':str(G[0,0]),'Einstein12':str(G[1,2]),
      'solution':{'U':'W-f/(2F0)','V':'W+f/(2F0)','Poisson':'lap W=rho/(2F0)','light_sum':'U+V=2W'},
      'checks':residuals,'null_dt_per_dl_times_c':str(null_time),'stellar_acceleration_c1':[str(v) for v in accel],
      'per_ray_gravitational_time':'-(1+z_l)/c * integral (U+V) dl = -2(1+z_l)/c * integral W dl, for dimensionless potentials and localized static lens',
      'two_path_gravitational_difference':'-2(1+z_l)/c * (integral_i W dl-integral_j W dl); geometric term and distance factors still required',
      'conclusion':'At fixed matter source and F0 the direct linear deltaF cancels from the light potential but shifts stellar dynamics. This does not cancel changes in F0, matter distribution, nonlinear scalar stress, modular sources, cosmological distances or boundary conditions.',
      'nonclosure':'f still must satisfy scalar equation with canonical potential, modular operator and boundary conditions; no phi-profile or lens amplitude derived. Measured G cannot be equated to 1/(8piF0) without its own calibration.',
      'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.perf_counter()-tic,'plan':pin(ROOT/'PLAN_R6_1.json'),'script':pin(Path(__file__))}
    save('METRIC_RESULT_R6_1.json',out)
    print(json.dumps({'status':out['status'],'components_verified':len(residuals),'solution':out['solution']}))
if __name__=='__main__':main()
