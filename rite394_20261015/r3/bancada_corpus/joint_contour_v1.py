"""Draft Gaussian common-constant test. No access to canonical files or network."""
import hashlib
import json
import math
from fractions import Fraction

ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
ALLOWED = ('JOINT_CONTOUR_NOT_FALSIFIED','JOINT_CONTOUR_FALSIFIED','JOINT_CONTOUR_INCONCLUSIVE')

def beta_runtime():
    return ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)

def protocol_hash(protocol):
    return hashlib.sha256(json.dumps(protocol,sort_keys=True,separators=(',',':'),
                                    ensure_ascii=False,allow_nan=False).encode()).hexdigest()

def chi2_survival(q,n):
    if q < 0 or not math.isfinite(q) or not 1 <= n <= 32:
        raise ValueError('Invalid chi-square arguments')
    x = q/2
    if n % 2:
        value = math.erfc(math.sqrt(x))
        a = 0.5
    else:
        value = math.exp(-x)
        a = 1.0
    while a < n/2:
        value += 0.0 if x == 0 else math.exp(a*math.log(x)-x-math.lgamma(a+1))
        a += 1
    return min(1.0,max(0.0,value))

def critical_value(n,alpha):
    low,high = 0.0,1.0
    while chi2_survival(high,n) > alpha:
        high *= 2
    for _ in range(100):
        middle = (low+high)/2
        if chi2_survival(middle,n) > alpha:
            low = middle
        else:
            high = middle
    return high

def as_fraction(value):
    if isinstance(value,bool):
        raise ValueError('Nonfinite or Boolean number')
    number = Fraction(str(value))
    if not math.isfinite(float(number)):
        raise ValueError('Nonfinite number')
    return number

def inverse_spd(matrix):
    n = len(matrix)
    if not 1 <= n <= 32 or any(len(row)!=n for row in matrix):
        raise ValueError('Invalid covariance shape')
    a = [[as_fraction(v) for v in row] for row in matrix]
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)):
        raise ValueError('Asymmetric covariance')
    # Exact LDL pivots certify positive definiteness before inversion.
    work = [row[:] for row in a]
    for k in range(n):
        if work[k][k] <= 0:
            raise ValueError('Covariance not positive definite')
        for i in range(k+1,n):
            for j in range(k+1,n):
                work[i][j] -= work[i][k]*work[k][j]/work[k][k]
    inverse = [[Fraction(i==j) for j in range(n)] for i in range(n)]
    for k in range(n):
        pivot = a[k][k]
        a[k] = [v/pivot for v in a[k]]
        inverse[k] = [v/pivot for v in inverse[k]]
        for i in range(n):
            if i != k:
                factor = a[i][k]
                a[i] = [a[i][j]-factor*a[k][j] for j in range(n)]
                inverse[i] = [inverse[i][j]-factor*inverse[k][j] for j in range(n)]
    return inverse

def bilinear(x,w,y):
    return sum((x[i]*w[i][j]*y[j] for i in range(len(x)) for j in range(len(y))),Fraction(0))

def gaussian_scores(values,covariance,beta):
    x = [as_fraction(v) for v in values]
    w = inverse_spd(covariance)
    if len(x) != len(w):
        raise ValueError('Dimension mismatch')
    u = [Fraction(1)]*len(x)
    b = as_fraction(beta)
    information = bilinear(u,w,u)
    estimate = bilinear(u,w,x)/information
    ra = [v-b for v in x]
    rb = [v-estimate for v in x]
    qa,qb = bilinear(ra,w,ra),bilinear(rb,w,rb)
    gain = information*(estimate-b)**2
    assert qa-qb == gain
    return {'estimate':estimate,'information':information,'qa':qa,'qb':qb,'gain':gain,
            'delta_aic':Fraction(2)-gain,'inverse':w}

def inconclusive(reason,**details):
    return {'verdict':ALLOWED[2],'veto_requested':False,'reason':reason,**details}

def evaluate(payload,protocol,expected_hash):
    try:
        if protocol_hash(protocol) != expected_hash:
            return inconclusive('PROTOCOL_HASH_MISMATCH')
        mode = payload.get('data_kind')
        if mode not in ('synthetic','prospective'):
            return inconclusive('INVALID_DATA_KIND')
        if mode == 'prospective' and not (protocol.get('ratified') is True and
                                         payload.get('prospective_lock_verified') is True):
            return inconclusive('NOT_RATIFIED_OR_NOT_PROSPECTIVE')
        rows = payload['domains']
        roster = protocol['roster']
        if len(set(roster)) != len(roster) or len(rows) != len(roster):
            return inconclusive('ROSTER_MISMATCH')
        if [r['id'] for r in rows] != roster:
            return inconclusive('ROSTER_MISMATCH')
        if any(r.get('eligible') is not True for r in rows):
            return inconclusive('DOMAIN_INELIGIBLE')
        for guard in ('provenance_valid','systematics_valid','covariance_valid','gaussian_model_valid'):
            if payload.get(guard) is not True:
                return inconclusive('INVALID_'+guard.upper())
        scores = gaussian_scores([r['estimate'] for r in rows],payload['covariance'],beta_runtime())
        n = len(rows)
        alpha = math.erfc(5/math.sqrt(2))
        critical = critical_value(n,alpha)
        qa = float(scores['qa'])
        p = chi2_survival(qa,n)
        shift = as_fraction(beta_runtime())/2
        alternatives = [[shift]*n]+[[shift if i==j else Fraction(0) for i in range(n)] for j in range(n)]
        powers = []
        for d in alternatives:
            noncentral = float(bilinear(d,scores['inverse'],d))
            root = math.sqrt(noncentral)
            z = math.sqrt(critical)
            powers.append(0.5*math.erfc((z-root)/math.sqrt(2))+
                          0.5*math.erfc((z+root)/math.sqrt(2)))
        details = {k:str(scores[k]) for k in ('estimate','information','qa','qb','gain','delta_aic')}
        details.update({'p_value':p,'alpha':alpha,'critical':critical,'minimum_power_bound':min(powers),
                        'aic_preference':'A' if scores['delta_aic']>0 else 'B' if scores['delta_aic']<0 else 'TIE',
                        'data_kind':mode,'protocol_hash':expected_hash})
        if p <= alpha:
            return {'verdict':ALLOWED[1],'veto_requested':True,'reason':'VALID_BILATERAL_REJECTION',**details}
        if min(powers) < 0.90:
            return inconclusive('INSUFFICIENT_POWER',**details)
        return {'verdict':ALLOWED[0],'veto_requested':False,'reason':'NO_REJECTION_WITH_POWER',**details}
    except (ValueError,TypeError,KeyError,OverflowError,ZeroDivisionError) as error:
        return inconclusive('INVALID_INPUT',error=str(error))
