"""Candidate Gaussian contrast, fixed unknown H0; synthetic qualification only.

Exact rational linear algebra on supplied binary numbers verifies normalization
and SPD. Gaussian tail evaluation is float64, not an interval certificate.
"""
from fractions import Fraction as F
from statistics import NormalDist
import hashlib
import json
import math


class PivotError(ValueError):
    pass


def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise PivotError('finite nonboolean real number required')
    if isinstance(x, float) and not math.isfinite(x):
        raise PivotError('nonfinite number')
    return F(x)


def finite_float(x):
    try:
        value=float(x)
    except (ValueError, OverflowError) as ex:
        raise PivotError('numeric conversion failed') from ex
    if not math.isfinite(value):raise PivotError('numeric overflow')
    return value


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def sf(x):
    return .5*math.erfc(x/math.sqrt(2))


def tail_fields(p):
    if not math.isfinite(p) or not 0 < p <= 1:
        raise PivotError('unresolved/zero tail; no infinite sigma')
    return {'p':p,'z_equivalent_upper_tail':-NormalDist().inv_cdf(p) if p<1 else None,
            'z_limit_if_p_one':'-infinity' if p==1 else None,
            'numerics':'ANALYTIC_LAW_FLOAT64_TAIL_NOT_INTERVAL_CERTIFICATE'}


def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))


def matrix(raw,n):
    if not isinstance(raw,list) or len(raw)!=n or any(not isinstance(row,list) or len(row)!=n for row in raw):
        raise PivotError('covariance matrix shape')
    a=[[rational(x) for x in row] for row in raw]
    if any(a[i][j]!=a[j][i] for i in range(n) for j in range(n)):
        raise PivotError('exact covariance symmetry required')
    # Exact LDL Schur elimination: no tolerance repairs a negative/zero pivot.
    work=[row[:] for row in a]
    for k in range(n):
        pivot=work[k][k]
        if pivot<=0:raise PivotError('strict positive definite covariance required')
        for i in range(k+1,n):
            for j in range(k+1,n):
                work[i][j]-=work[i][k]*work[k][j]/pivot
    return a


def solve(a,b):
    n=len(b);m=[row[:]+[b[i]] for i,row in enumerate(a)]
    for k in range(n):
        v=m[k][k]
        if v==0:raise PivotError('singular solve')
        m[k]=[x/v for x in m[k]]
        for i in range(n):
            if i!=k:
                v=m[i][k];m[i]=[m[i][j]-v*m[k][j] for j in range(n+1)]
    return [row[-1] for row in m]


def _model(contract):
    required={'id','route_id','scenario_id','test_id','mode','distribution','factor',
              'weights_rule','C','background_variance','cross_covariance',
              'cross_covariance_source','fixed_before_centres','tail','matrix_sha256'}
    if not isinstance(contract,dict) or not required<=contract.keys():
        raise PivotError('complete contrast contract required; missing cross covariance is not zero')
    if contract['mode']!='SYNTHETIC_ONLY' or contract['distribution']!='JOINT_GAUSSIAN_FIXED_UNKNOWN_H0_KNOWN_ERRORS':
        raise PivotError('sampling model or mode not qualified')
    if contract['fixed_before_centres'] is not True:
        raise PivotError('parameters/weights must be fixed independently of centres')
    for key in ['id','route_id','scenario_id','test_id','cross_covariance_source']:
        if not isinstance(contract[key],str) or not contract[key].strip():raise PivotError('named source/identity required')
    if contract['tail'] not in ['upper','two_sided']:raise PivotError('explicit qualified tail required')
    C=contract['C']
    if not isinstance(C,list) or not 1<=len(C)<=32:raise PivotError('1..32 readers supported')
    n=len(C); c=matrix(C,n)
    rawd=contract['cross_covariance']
    if not isinstance(rawd,list) or len(rawd)!=n:raise PivotError('explicit cross vector required')
    d=[rational(x) for x in rawd];s2=rational(contract['background_variance'])
    rawjoint=[row[:]+[rawd[i]] for i,row in enumerate(C)]+[rawd[:]+[contract['background_variance']]]
    if digest(rawjoint)!=contract['matrix_sha256']:raise PivotError('joint matrix pin mismatch')
    joint=matrix(rawjoint,n+1)
    f=rational(contract['factor'])
    if f<=0:raise PivotError('positive factor required')
    if contract['weights_rule']=='FIXED_GLS_C':
        ww=solve(c,[F(1)]*n);normal=sum(ww);w=[x/normal for x in ww]
    elif contract['weights_rule']=='EXPLICIT_NORMALIZED_RATIONAL':
        raw=contract.get('weights')
        if not isinstance(raw,list) or len(raw)!=n:raise PivotError('weight vector required')
        w=[]
        for x in raw:
            if not isinstance(x,list) or len(x)!=2 or any(type(v) is not int for v in x) or x[1]<=0:
                raise PivotError('each weight is an integer numerator/positive denominator pair')
            w.append(F(*x))
    else:raise PivotError('unknown fixed weights rule')
    if sum(w)!=1:raise PivotError('weights must sum exactly to1; no silent tolerance or renormalization')
    l=w+[-f];variance=dot(l,[dot(row,l) for row in joint])
    if variance<=0:raise PivotError('positive contrast variance required')
    return n,w,f,joint,variance


def qualify(contract,y,b):
    n,w,f,joint,var=_model(contract)
    if not isinstance(y,list) or len(y)!=n:raise PivotError('observation dimension')
    yy=[rational(x) for x in y];bb=rational(b)
    contrast=dot(w,yy)-f*bb
    variance=finite_float(var);numerator=finite_float(contrast)
    if variance<=0:raise PivotError('variance underflow')
    z=numerator/math.sqrt(variance)
    if not math.isfinite(z):raise PivotError('z overflow')
    p=sf(z) if contract['tail']=='upper' else 2*sf(abs(z))
    return {'calibration':'ANALYTIC_GAUSSIAN_NUISANCE_FREE_PIVOT','contract_sha256':digest(contract),
            'route_id':contract['route_id'],'scenario_id':contract['scenario_id'],'test_id':contract['test_id'],
            'contrast':numerator,'variance':variance,'z_pivot':z,'tail':contract['tail'],**tail_fields(p),
            'weights_exact':[[v.numerator,v.denominator] for v in w],
            'nuisance_H0_cancelled_exactly':True,'scope':'UNIFORM_IN_FIXED_H0_WITHIN_DECLARED_JOINT_GAUSSIAN_MODEL',
            'observed_F9_verdict':None,'gate_moved':False}


def design_power(contract,alternative_factor,H_true,threshold_z,alternative_covariance):
    """Power at a named alternative; H_true is design input, never estimated here.

    alternative_covariance must explicitly be SAME_AS_NULL or a complete SPD
    joint matrix. No assumption that alternative and null variances coincide.
    """
    n,w,f,joint,v0=_model(contract)
    alt=rational(alternative_factor);h=rational(H_true);threshold=finite_float(rational(threshold_z))
    if alt<=0 or threshold<=0:raise PivotError('positive factor/threshold required')
    if isinstance(alternative_covariance,str) and alternative_covariance=='SAME_AS_NULL':v1=v0
    else:
        cov=matrix(alternative_covariance,n+1);l=w+[-f];v1=dot(l,[dot(row,l) for row in cov])
    v0f=finite_float(v0);v1f=finite_float(v1)
    if v0f<=0 or v1f<=0:raise PivotError('unresolved design variance')
    # Separate square roots avoid overflowing v1/v0 for finite input variances.
    # Every standardized intermediate must remain representable; otherwise refuse.
    root0=math.sqrt(v0f);root1=math.sqrt(v1f)
    mean=finite_float(finite_float((alt-f)*h)/root0)
    sd=finite_float(root1/root0)
    if sd<=0:raise PivotError('design standard deviation underflow')
    upper=finite_float(finite_float(threshold-mean)/sd)
    power=sf(upper)
    if contract['tail']=='two_sided':
        lower=finite_float(finite_float(threshold+mean)/sd)
        power+=sf(lower)
    if not math.isfinite(power) or not 0<=power<=1:raise PivotError('invalid power')
    return {'power':power,'alternative_mean_z':mean,'alternative_sd_z':sd,'threshold_z':threshold,
            'tail':contract['tail'],'H_true_design_input':finite_float(h),'observed_power':False}


def family_adjust(contract,records):
    required={'id','route_id','method','test_ids','scenario_ids','scope'}
    if not isinstance(contract,dict) or not required<=contract.keys():raise PivotError('multiplicity contract missing')
    if contract['scope']!='SYNTHETIC_CANDIDATE_NOT_ADOPTED_F9':raise PivotError('no observed adoption authorized')
    if contract['method'] not in ['bonferroni','none_single_test']:raise PivotError('Sidak independence not qualified')
    tests=contract['test_ids'];scenarios=contract['scenario_ids']
    for values in [tests,scenarios]:
        if not isinstance(values,list) or not values or any(not isinstance(v,str) or not v for v in values) or len(set(values))!=len(values):
            raise PivotError('complete named finite family required')
    if contract['method']=='none_single_test' and len(tests)!=1:raise PivotError('multiple tests require correction')
    expected={(t,s) for t in tests for s in scenarios};seen={}
    if not isinstance(records,list) or any(not isinstance(r,dict) for r in records):
        raise PivotError('calibrated records list required')
    for r in records:
        key=(r.get('test_id'),r.get('scenario_id'))
        if key not in expected or key in seen or r.get('route_id')!=contract['route_id']:
            raise PivotError('missing/duplicate/cross-route record')
        if r.get('calibration')!='ANALYTIC_GAUSSIAN_NUISANCE_FREE_PIVOT':raise PivotError('unqualified pivot')
        p=finite_float(rational(r.get('p')))
        if not 0<p<=1:raise PivotError('invalid tail')
        seen[key]=p
    if set(seen)!=expected:raise PivotError('incomplete scenario/test coverage')
    m=len(tests);result={}
    for t in tests:
        p=max(seen[t,s] for s in scenarios)
        result[t]={'p_robust':p,**tail_fields(min(1,m*p) if contract['method']=='bonferroni' else p)}
    return {'method':contract['method'],'m':m,'results':result,'contract_sha256':digest(contract),
            'scope':'FINITE_UNION_AND_NAMED_FAMILY_ONLY; NO_SIDAK; NO_F9_ADOPTION','observed_F9_verdict':None}
