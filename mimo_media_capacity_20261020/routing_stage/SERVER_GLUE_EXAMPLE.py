"""Concrete host glue for both old inline and new typed audio/video clients.

Not installed. Caller supplies the REAL full-prefix engine body builder and
owner-bound resolver; this example does not assume another provider's schema.
"""
import iald_media_budget as budget

PROPOSALS = {
    'standard': {'fps':2.0,'media_resolution':'default'},
    'detail': {'fps':2.0,'media_resolution':'max'},
}


def build_options(*, full_body, resolved_facts, validate_upload, rates,
                  proposals=None, intent_limits=None):
    """full_body = {'messages':wire_full_prefix_and_history,'tools':full_tools,...}.

    resolved_facts is Cicero resolve_media_metadata(full_body['messages'],...)
    result; [] is correct when the old client only supplied inline audio/video.
    validate_upload is Cicero iald_mimo_multimodal.validate_upload, no network.
    """
    items=budget.adapt_resolved_metadata(resolved_facts)
    items+=budget.legacy_inline_metadata(full_body['messages'],validate_upload=validate_upload)
    plans=budget.options(full_body,items,PROPOSALS if proposals is None else proposals,
                         rates=rates,intent_limits=intent_limits)
    budget.routing_options(plans)  # Fail before JEV if no option can meet intent/context.
    return items,plans


def before_choose(*, client, build_full_engine_body, resolve_owner_bound_metadata,
                  request_media, validate_upload, rates, intent_limits=None):
    """All callbacks are host-owned, local and request-scoped; no remote calls.

    build_full_engine_body uses the exact wire_messages/prefix/ACOM/tools builder
    already used by MiMo, sets model and max_completion_tokens=131072 for preview.
    It must not crop any prefix/history. No other provider receives these refs.
    """
    full_body=build_full_engine_body(client)
    resolved=resolve_owner_bound_metadata(full_body['messages'])
    items,plans=build_options(full_body=full_body,resolved_facts=resolved,
        validate_upload=validate_upload,rates=rates,intent_limits=intent_limits)
    return request_media(client),items,plans


def after_choose(*, full_current_body, resolved_current_facts, validate_upload,
                 rates, receipt, maximum=131072, window=1048576, intent_limits=None):
    """Replan every current tool round with the selected policy; no new JEV call.

    Runtime can use this or exactly the same plan_request call. Do not add the
    temporary estimator on top. The planner is the sole source of context/cost.
    """
    items=budget.adapt_resolved_metadata(resolved_current_facts)
    items+=budget.legacy_inline_metadata(full_current_body['messages'],validate_upload=validate_upload)
    prepared={**full_current_body,'max_completion_tokens':maximum}
    return budget.plan_request(prepared,items,rates=rates,
        policy=receipt['media_budget']['policy'],intent_limits=intent_limits,
        maximum_output=maximum,context_limit=window)
