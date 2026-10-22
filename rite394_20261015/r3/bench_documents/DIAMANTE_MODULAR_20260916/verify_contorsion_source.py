"""Exact rational controls for a connection difference; not a physical fit."""
from fractions import Fraction as F
from itertools import product
import random
import json
from finalize_weyl_bridge import ROOT, atomic

I = range(4)
keys3 = list(product(I, repeat=3))
keys4 = list(product(I, repeat=4))


def ricci(connection, derivative):
    # Gamma[r,mu,s]; derivative[a,r,mu,s] = partial_a Gamma[r,mu,s].
    return {(s,n): sum(derivative[r,r,n,s] - derivative[n,r,r,s]
                      + sum(connection[r,r,l]*connection[l,n,s]
                            - connection[r,n,l]*connection[l,r,s] for l in I)
                      for r in I) for s,n in product(I, repeat=2)}


def source_parts(base, c, dc):
    nabla = {(a,r,m,s): dc[a,r,m,s] + sum(
        base[r,a,l]*c[l,m,s] - base[l,a,m]*c[r,l,s]
        - base[l,a,s]*c[r,m,l] for l in I) for a,r,m,s in keys4}
    linear = {(s,n): sum(nabla[r,r,n,s]-nabla[n,r,r,s] for r in I)
              for s,n in product(I, repeat=2)}
    quadratic = {(s,n): sum(c[r,r,l]*c[l,n,s]-c[r,n,l]*c[l,r,s]
                           for r,l in product(I, repeat=2))
                 for s,n in product(I, repeat=2)}
    return linear, quadratic


def einstein_symmetric(r):
    metric = [1,-1,-1,-1]
    trace = sum(metric[a]*r[a,a] for a in I)
    return {(a,b): (r[a,b]+r[b,a])/2
            - (F(metric[a],2)*trace if a == b else 0)
            for a,b in product(I, repeat=2)}


def main():
    checks = []
    rng = random.Random(17092026)
    for case in range(8):
        base = {k:F(rng.randrange(-3,4)) for k in keys3}
        base = {(r,m,s):(base[r,m,s]+base[r,s,m])/2 for r,m,s in keys3}
        dbase = {k:F(rng.randrange(-3,4)) for k in keys4}
        c = {k:F(rng.randrange(-3,4)) for k in keys3}
        dc = {k:F(rng.randrange(-3,4)) for k in keys4}
        linear, quadratic = source_parts(base,c,dc)
        initial = ricci(base,dbase)
        for eps in (F(-2),F(-1,2),F(0),F(1),F(2)):
            actual = ricci({k:base[k]+eps*c[k] for k in keys3},
                           {k:dbase[k]+eps*dc[k] for k in keys4})
            delta = {k:actual[k]-initial[k] for k in initial}
            expected = {k:eps*linear[k]+eps**2*quadratic[k] for k in initial}
            checks.append({'name':f'connection_expansion_{case}_{eps}', 'passed':delta == expected})
            bdelta = einstein_symmetric(delta)
            bl,bq = einstein_symmetric(linear),einstein_symmetric(quadratic)
            checks.append({'name':f'symmetric_source_{case}_{eps}',
                           'passed':bdelta == {k:eps*bl[k]+eps**2*bq[k] for k in bl}})
    # Metric-compatible pure-vector contorsion in Minkowski space.
    metric = [1,-1,-1,-1]
    vector = [F(1),F(2),F(0),F(-1)]
    c = {(r,m,s):(vector[s] if r == m else 0)
         - (metric[m]*metric[r]*vector[r] if m == s else 0) for r,m,s in keys3}
    zero3,zero4 = {k:F(0) for k in keys3},{k:F(0) for k in keys4}
    linear,quadratic = source_parts(zero3,c,zero4)
    checks.extend([
        {'name':'metric_compatibility_vector_example', 'passed':all(
            metric[r]*c[r,m,s]+metric[s]*c[s,m,r] == 0 for r,m,s in keys3)},
        {'name':'constant_contorsion_zero_linear_nonzero_quadratic',
         'passed':all(v == 0 for v in linear.values()) and any(v != 0 for v in quadratic.values())},
        {'name':'negative_control_wrong_linear_scaling_rejected',
         'passed':any(4*v != 2*v for v in quadratic.values())},
    ])
    assert all(item['passed'] for item in checks)
    result = {'scope':'EXACT_RATIONAL_CONNECTION_IDENTITY_CONTROLS_NOT_TGL_FIELD_EQUATIONS',
              'checks':checks,'count':len(checks),'passed':sum(x['passed'] for x in checks),
              'physical_K_beta_supplied':False,'modular_state_computed':False}
    atomic(ROOT/'CONTORSION_SOURCE_CHECKS.json',json.dumps(result,indent=2))
    print(json.dumps({'status':'PASS','checks':len(checks),'arithmetic':'fractions_exact'}))


if __name__ == '__main__':
    main()
