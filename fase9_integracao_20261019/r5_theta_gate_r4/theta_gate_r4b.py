"""Additive final-value consistency checks; preserve the first pinned consumer."""
from theta_gate import consume as _consume,pinned,number,MODELS,ThetaGateError

def consume(result_path,result_sha256,recipe_path,recipe_sha256):
    answer=_consume(result_path,result_sha256,recipe_path,recipe_sha256)
    # A second verified read must have the identical digest; a changed file is
    # refused rather than combining snapshots. No unverified value is consumed.
    try:
        doc=pinned(result_path,result_sha256)
        if set(doc['models'])!=MODELS or set(doc['lnB_against_H2_same_context'])!=MODELS:
            raise ThetaGateError('FINAL_MODEL_SET_MISMATCH')
        last=doc['levels'][-1]['models'];field='log_relative_integral_without_log_kappa'
        bg=number(last['H2_LCDM'][field])
        for m in MODELS:
            val=number(doc['models'][m]['log_relative_evidence_without_common_log_kappa'])
            if val!=last[m][field]:raise ThetaGateError('FINAL_INTEGRAL_MISMATCH')
            if number(doc['lnB_against_H2_same_context'][m])!=val-bg:
                raise ThetaGateError('FINAL_BAYES_RATIO_MISMATCH')
        counts=doc['callback_counts'];background=counts['background_calls']
        new=background['new_calls_declared'];reused=background['durable_cache_hits_declared']
        if type(new) is not int or type(reused) is not int or min(new,reused)<0 or new+reused!=counts['completed']:
            raise ThetaGateError('DECLARED_PHYSICAL_CALL_COUNT_MISMATCH')
        answer['final_integrals_and_ratios_match_levels']=True
        answer['declared_call_counts_consistent_not_solver_reaudited']=True
        return answer
    except ThetaGateError:raise
    except (KeyError,TypeError,ValueError,OverflowError) as exc:
        raise ThetaGateError('MALFORMED_FINAL_VALUES: '+str(exc)) from exc
