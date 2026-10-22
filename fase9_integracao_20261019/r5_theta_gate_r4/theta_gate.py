"""Read pinned outer-theta results and independently recompute refinement refusal.

Numerical agreement is an engineering diagnostic, never a scientific acceptance
or an operator act. Scalar-V2 and joint-ROOT contexts remain separate.
"""
import hashlib,json,math
from pathlib import Path

class ThetaGateError(ValueError):pass
MODELS={'H1_TGL','H2_LCDM','H3_beta_free','H4_Cepheid','H5_rd_free'}
def number(x):
    if type(x) not in (int,float) or not math.isfinite(x):raise ThetaGateError('FINITE_NONBOOLEAN_NUMBER_REQUIRED')
    return x
def pinned(path,expected):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected:raise ThetaGateError('PIN_MISMATCH')
    return json.loads(raw)
def consume(result_path,result_sha256,recipe_path,recipe_sha256):
    try:
        doc=pinned(result_path,result_sha256);recipe=pinned(recipe_path,recipe_sha256)
        if doc['schema']!='F9_THETA_RELATIVE_INTEGRATION_RESULT_V1' or doc['status']!='ENGINEERING_ONLY':
            raise ThetaGateError('UNQUALIFIED_RESULT_SCHEMA_OR_SCOPE')
        if doc['algorithm']!='POSITIVE_NESTED_COMPOSITE_SIMPSON' or recipe['dataset_kind']!='SYNTHETIC':
            raise ThetaGateError('SYNTHETIC_NESTED_RULE_ONLY')
        first,last=recipe['first_level'],recipe['last_level']
        if type(first) is not int or type(last) is not int or first<1 or last<=first:
            raise ThetaGateError('INVALID_LEVEL_POLICY')
        target=number(recipe['absolute_log_refinement_target'])
        if target<=0:raise ThetaGateError('INVALID_TARGET')
        levels=doc['levels']
        if not isinstance(levels,list) or [x['level'] for x in levels]!=list(range(first,last+1)):
            raise ThetaGateError('LEVEL_SET_MISMATCH')
        for level in levels:
            if type(level['level']) is not int or type(level['intervals_per_axis']) is not int or type(level['nodes_in_rule']) is not int:
                raise ThetaGateError('INTEGER_LEVEL_METADATA_REQUIRED')
            if level['intervals_per_axis']!=2**level['level'] or level['nodes_in_rule']!=(2**level['level']+1)**3:
                raise ThetaGateError('NESTED_NODE_COUNT_MISMATCH')
            if set(level['models'])!=MODELS:raise ThetaGateError('MODEL_SET_MISMATCH')
            for model in level['models'].values():
                number(model['log_relative_integral_without_log_kappa'])
                for key in ['summation_underflowed_terms','support_zero_nodes']:
                    if type(model[key]) is not int or model[key]<0:raise ThetaGateError('INVALID_NODE_DIAGNOSTIC')
        field='log_relative_integral_without_log_kappa'
        gaps={m:abs(levels[-1]['models'][m][field]-levels[-2]['models'][m][field]) for m in MODELS}
        ref=doc['refinement']
        if number(ref['requested_target'])!=target:raise ThetaGateError('TARGET_MISMATCH')
        if set(ref['last_absolute_log_difference'])!=MODELS:raise ThetaGateError('GAP_MODEL_SET_MISMATCH')
        for m,gap in gaps.items():
            if number(ref['last_absolute_log_difference'][m])!=gap:raise ThetaGateError('REPORTED_GAP_MISMATCH')
        computed=all(v<=target for v in gaps.values())
        if type(ref['indicator_satisfied']) is not bool or ref['indicator_satisfied']!=computed:
            raise ThetaGateError('REPORTED_CONVERGENCE_MISMATCH')
        if ref['all_declared_levels_completed'] is not True or ref['early_stopping'] is not False:
            raise ThetaGateError('INCOMPLETE_DECLARED_CAMPAIGN')
        counts=doc['callback_counts'];expected=(2**last+1)**3
        for key in ['attempted','completed','required_unique_nodes']:
            if type(counts[key]) is not int or counts[key]!=expected:raise ThetaGateError('CALLBACK_COUNT_MISMATCH')
        quality=doc['conditional_precision_summary']
        failures=[]
        for key in ['conditional_underflowed_nodes','service_not_converged','service_unassessed']:
            if type(quality[key]) is not int or quality[key]<0:raise ThetaGateError('INVALID_CONDITIONAL_DIAGNOSTIC')
            if quality[key]:failures.append(key)
        failures+=['REFINEMENT_NOT_CONVERGED:'+m for m,gap in sorted(gaps.items()) if gap>target]
        if any(model['summation_underflowed_terms'] for level in levels for model in level['models'].values()):
            failures.append('OUTER_SUMMATION_UNDERFLOW')
        return {'status':'REFUSE_NUMERICAL' if failures else 'REFINEMENT_DIAGNOSTIC_PASS',
            'reasons':failures,'recomputed_gaps':gaps,'target':target,
            'input_sha256':result_sha256,'recipe_sha256':recipe_sha256,
            'witness':'joint_ROOT283','may_freeze':False,'may_open_observed_data':False,
            'qualified_observed_verdict':False,'rigorous_integral_error_bound':None,
            'scope':'Pinned synthetic theta refinement only; not scalar V2, admissions, or global error certification.'}
    except ThetaGateError:raise
    except (KeyError,TypeError,ValueError,OSError,OverflowError) as exc:
        raise ThetaGateError('MALFORMED_OR_UNREADABLE_RESULT: '+str(exc)) from exc
