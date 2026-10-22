"""Reject unstable evidence integrations. Agreement is diagnostic, not a proof.

Policies and thresholds must be pinned before observations. A finite set of
quadratures cannot certify the absence of a narrow missed peak. Consequently
this checker never authorizes a physical verdict from refinement alone.
"""
import math

class NumericalQualificationError(ValueError): pass

def finite(value):
    if type(value) not in (float,int) or not math.isfinite(value):
        raise NumericalQualificationError('NONFINITE_OR_BOOLEAN')
    return float(value)

def assess_evidence(level_results,policy):
    try:
        levels=policy['levels'];tol=finite(policy['max_abs_delta_log_evidence'])
        if (not isinstance(levels,list) or len(levels)<3 or any(type(n)!=int or n<100 for n in levels)
            or levels!=sorted(set(levels)) or tol<=0):
            raise NumericalQualificationError('INVALID_PINNED_POLICY')
        if not isinstance(level_results,dict) or not level_results:
            raise NumericalQualificationError('NO_MODELS')
        checks={}
        for model,estimates in level_results.items():
            if set(estimates)!=set(map(str,levels)):
                raise NumericalQualificationError('LEVEL_SET_MISMATCH')
            values=[finite(estimates[str(n)]) for n in levels]
            gaps=[abs(b-a) for a,b in zip(values,values[1:])]
            if any(gap>tol for gap in gaps[-2:]):
                raise NumericalQualificationError('REFINEMENT_NOT_CONVERGED: '+model)
            checks[model]={'log_evidence':values[-1],'last_two_gaps':gaps[-2:]}
        return {'status':'REFINEMENT_DIAGNOSTIC_PASS','models':checks,
                'max_pairwise_log_bayes_drift_bound_from_tolerance':2*tol,
                'rigorous_integral_error_bound':None,'qualified_observed_verdict':False,
                'scope':'Finite refinement agreement; not a certified integral or tail bound'}
    except NumericalQualificationError:raise
    except (KeyError,TypeError,ValueError) as exc:
        raise NumericalQualificationError('MALFORMED_NUMERICAL_EVIDENCE: '+str(exc)) from exc

def threshold_stable(value,certified_abs_error,threshold):
    """Decision only when an independently justified error interval clears it.

    This arithmetic cannot establish that a supplied bound is rigorous; its
    evidence/authority must be verified upstream. Refinement gaps aren't bounds.
    """
    value=finite(value);threshold=finite(threshold)
    if certified_abs_error is None:raise NumericalQualificationError('CERTIFIED_BOUND_MISSING')
    error=finite(certified_abs_error)
    if error<0:raise NumericalQualificationError('NEGATIVE_ERROR')
    if value-error>threshold:return 'ABOVE'
    if value+error<threshold:return 'BELOW'
    raise NumericalQualificationError('THRESHOLD_WITHIN_ERROR_INTERVAL')
