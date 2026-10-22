"""Server-side selection records for two models under one consent provider.

No account writes here. The route must load the account under its normal lock,
call these functions, then persist the returned fields atomically.
"""
from copy import copy
from claude_account_policy import authorize_model,available_models
from claude_profiles import HAIKU,SONNET,LEGACY_HAIKU

OPTIONS={'claude-haiku':HAIKU.model,'claude-sonnet':SONNET.model}

def policy_for(record,username,*,haiku_ready,sonnet_ready):
    # Existing user records are created only after the application's access
    # workflow. Pending requests live separately and must not be passed here.
    approved=isinstance(record,dict) and bool(record) and not bool(record.get('bloqueado'))
    return dict(username=username,account_approved=approved,haiku_ready=haiku_ready,sonnet_ready=sonnet_ready)

def selected_model(record,username,*,haiku_ready,sonnet_ready):
    policy=policy_for(record,username,haiku_ready=haiku_ready,sonnet_ready=sonnet_ready)
    requested=record.get('modelo_claude') if isinstance(record,dict) else None
    if requested in (LEGACY_HAIKU.model, 'claude-haiku-4-5'):
        requested = HAIKU.model  # Explicit operator-authorized migration, no account rewrite.
    if not requested:
        # Preserve the original operator's Sonnet selection. New public accounts
        # use Haiku; never silently upgrade them to the more expensive model.
        requested=SONNET.model if str(username).strip().lower()=='luiz' else HAIKU.model
    return authorize_model(requested,**policy)

def select_fields(option_id,record,username,*,haiku_ready,sonnet_ready):
    policy=policy_for(record,username,haiku_ready=haiku_ready,sonnet_ready=sonnet_ready)
    if option_id=='claude':
        chosen=selected_model(record,username,haiku_ready=haiku_ready,sonnet_ready=sonnet_ready)
    elif option_id in OPTIONS:
        chosen=authorize_model(OPTIONS[option_id],**policy)
    else:
        raise ValueError('Unknown Claude selection')
    return {'motor':'claude','modelo_claude':chosen}

def option_rows(record,username,*,haiku_ready,sonnet_ready):
    policy=policy_for(record,username,haiku_ready=haiku_ready,sonnet_ready=sonnet_ready)
    models=available_models(**policy)
    return [{'id':key,'provedor':'claude','modelo':model,
             'rotulo':'Claude Haiku 5.5' if model==HAIKU.model else 'Claude Sonnet 5.5',
             'detalhe':'Anthropic · '+model,'disponivel':True}
            for key,model in OPTIONS.items() if model in models]

def config_for_model(base,model):
    result=copy(base)
    if model not in OPTIONS.values():raise ValueError('Unknown model')
    if base.precos(model) is None:raise ValueError('Model price must be configured before activation')
    result.modelo=result.modelo_operador=model
    result.sucessor_automatico=False
    if model==HAIKU.model:
        result.max_saida=result.max_saida_pensar=HAIKU.default_output
        result.janela=HAIKU.window
        result.esforco_claude="medium"
    # Preserve quota exemptions, global caps, cache TTL and provider credential.
    # Native token counting, not cfg.janela*estimated factor, gates every call.
    return result
