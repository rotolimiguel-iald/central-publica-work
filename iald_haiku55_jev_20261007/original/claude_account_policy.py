"""Prepared server-side model policy; not wired to production routes yet.

Inputs must come from server authentication, approval and deployment checks, not
request JSON. Haiku availability never grants native-engine or Sonnet access.
Provider consent and spending/context guards remain mandatory downstream.
"""
from claude_profiles import HAIKU, SONNET, profile_for


def available_models(*, username, account_approved, haiku_ready=False,
                     sonnet_ready=False):
    if any(type(flag) is not bool for flag in
           (account_approved, haiku_ready, sonnet_ready)):
        raise ValueError('Server policy flags must be explicit booleans')
    if not isinstance(username, str) or not username.strip() or not account_approved:
        return ()
    allowed = []
    if haiku_ready:
        allowed.append(HAIKU.model)
    if username.strip().lower() == 'luiz' and sonnet_ready:
        allowed.append(SONNET.model)
    return tuple(allowed)


def authorize_model(requested_model, **server_policy):
    """Resolve only verified models, then enforce the account-specific allowlist.

    No fallback to another paid model: a stale or forged selection is rejected.
    """
    canonical = profile_for(requested_model).model
    if canonical not in available_models(**server_policy):
        raise PermissionError('Claude model unavailable for this account')
    return canonical
