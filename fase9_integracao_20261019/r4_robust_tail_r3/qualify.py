"""Pin a finite synthetic plan before exercising the conservative-tail candidate."""
from pathlib import Path
import datetime,hashlib,json,math
from robust_tail import upper_tail,RobustTailError
ROOT=Path(__file__).resolve().parent
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(name,obj):
    with (ROOT/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2,ensure_ascii=False)
def main():
    plan={'mode':'SYNTHETIC_ONLY','biases':[-2,0,.5],'variance_fractions':[0,.01,.2,1],
          'threshold_z':[1,2,5],'tolerance':1e-14,
          'checks':['Gaussian size bound over fixed grid','rank-one bound saturation',
                    'missing bias refusal','negative-threshold p=1','multiplicity',
                    'nonfinite/boolean refusal','underflow refusal'],
          'pins':[pin(ROOT/'robust_tail.py'),pin(ROOT/'PROOF.txt'),pin(Path(__file__)),
                  pin(ROOT.parent/'r1_envelope'/'covariance_envelope_r1.py')],
          'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    save('PLAN_R3.json',plan)
    kw=dict(weights=[1],local_sigmas=[1.2],background_sigma=.3,factor=1,
            null_bias_upper_bound=.5,bias_source='SYNTHETIC_ASSUMPTION',mode='SYNTHETIC_ONLY',tests_in_family=1)
    sf=lambda z:.5*math.erfc(z/math.sqrt(2))
    checks=[]
    for z in plan['threshold_z']:
        d=.5+1.5*z
        p=upper_tail(contrast=d,**kw)['p_upper_conservative']
        for mu in plan['biases']:
            for fraction in plan['variance_fractions']:
                actual=0 if fraction==0 else sf((d-mu)/(1.5*math.sqrt(fraction)))
                assert actual<=p+plan['tolerance']
                checks.append({'kind':'synthetic_size','z':z,'mean':mu,'variance_fraction':fraction,'pass':True})
        assert abs(p-sf(z))<plan['tolerance']
    assert upper_tail(contrast=.4,**kw)['p_upper_conservative']==1
    multi=upper_tail(contrast=3.5,**{**kw,'tests_in_family':4})
    assert multi['p_bonferroni']==min(1,4*multi['p_upper_conservative'])
    refusals=[]
    for change in [{'null_bias_upper_bound':None},{'contrast':float('nan')},{'contrast':True},
                   {'null_bias_upper_bound':-1},{'tests_in_family':True},{'mode':'OBSERVED'},
                   {'weights':[.9]},{'contrast':1e100}]:
        try:upper_tail(**{'contrast':3.5,**kw,**change})
        except RobustTailError as exc:refusals.append(str(exc))
        else:raise AssertionError(change)
    save('RESULT_R3.json',{'status':'PASS_SYNTHETIC_SCOPE','plan':pin(ROOT/'PLAN_R3.json'),
          'size_grid_checks':checks,'refusals':refusals,'saturation_z':[1,2,5],
          'physical_bias_bound_measured':False,'observed_verdict':None})
    print(json.dumps({'status':'PASS_SYNTHETIC_SCOPE','size_grid_cases':len(checks),'refusals':len(refusals)}))
if __name__=='__main__':main()
