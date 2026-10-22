"""Prepared native streaming bridge; preserves the existing SSE/usage adapter.

Caller must enforce authentication, provider consent and spending reservation
before entry. This layer enforces account/model authorization and exact context.
It never falls back to another model and never retries a paid request.
"""
from copy import copy
from claude_account_policy import authorize_model
from claude_native_counter import count_native_request
from claude_profile_pipeline import profile_call
from claude_request_guard import ContextRejected
from claude_profiles import HAIKU,profile_for,context_budget

def post_guarded(adapter, cfg, payload, *, requested_model, server_policy,
                 prefix, memory, state=None, timeout=None, client=None,
                 counter=None):
    # Policy is checked before constructing a client or counting tokens.
    try:
        authorized=authorize_model(requested_model,**server_policy)
        incoming=payload.get('model')
        if incoming is not None and profile_for(incoming).model!=authorized:
            raise PermissionError('Payload model differs from authorization')
    except (ValueError,PermissionError):
        return adapter.erro_openai(403,'claude_model_forbidden','Modelo não liberado para esta conta.'),None
    if adapter._leva_atlas_integral(payload,prefix):
        return adapter.erro_openai(400,'claude_atlas_integral','Este contexto não está autorizado para a Anthropic.'),None
    selected=copy(cfg)
    selected.modelo=authorized
    try:
        native_client=client if client is not None else adapter.cliente_para(selected)
        native_client=adapter._com_prazo(native_client,timeout)
        native_client=native_client.with_options(max_retries=0)
        if native_client.max_retries!=0:
            raise ValueError('No-retry client required')
    except Exception as exc:
        return adapter._resposta_de_excecao(exc),None

    def convert(current_cfg,current_payload,**kwargs):
        wire=adapter.converter_pedido(current_cfg,current_payload,**kwargs)
        if authorized==HAIKU.model and wire['max_tokens']>4096:
            raise ValueError('Haiku output exceeds the measured profile reserve')
        return wire

    generation_attempted=False
    measured_decision=None

    def counted(wire):
        nonlocal measured_decision
        n=(counter(wire) if counter is not None else count_native_request(native_client,wire))
        measured_decision=context_budget(authorized,counted_model=memory.model,
            permanent_tokens=memory.permanent_tokens,request_input_tokens=n,
            reserved_output_tokens=wire.get('max_tokens'),margin_tokens=1024)
        return n

    def ambiguous_response():
        # A stream may already have incurred cost. Never classify local failure
        # after attempting generation as a known free refusal.
        return adapter.erro_openai(502,'claude_generation_uncertain',
            'O envio ao Claude foi interrompido. O uso será conciliado pelo controle de gasto.'),measured_decision

    def send(wire):
        # The guarded native request must not pass through post_como_openai:
        # reconversion there would restore the old Sonnet-only parameters.
        nonlocal generation_attempted
        generation_attempted=True
        manager=native_client.messages.stream(**wire)
        stream=manager.__enter__()
        try:
            headers=adapter._cabecalhos(getattr(getattr(stream,'response',None),'headers',None))
            headers.setdefault('content-type','text/event-stream')
            flow=adapter._Fluxo(manager,stream,state,authorized)
            return adapter.RespostaClaude(200,headers,linhas=flow.linhas(),fechar=flow.cancelar)
        except BaseException:
            manager.__exit__(*__import__('sys').exc_info())
            raise

    try:
        return profile_call(requested_model=authorized,server_policy=server_policy,cfg=selected,
            payload=payload,prefix=prefix,memory=memory,converter=convert,
            count_request=counted,
            send_request=send,state=state)
    except ContextRejected as exc:
        return adapter.erro_openai(400,'claude_context_limit',
            'A conversa excede o espaço disponível. Inicie uma nova conversa; a memória TGL será mantida.'),exc.decision
    except ValueError as exc:
        if generation_attempted:
            return ambiguous_response()
        return adapter.erro_openai(400,'claude_context_invalid',
            'Não foi possível validar a memória e os limites deste pedido. Nada foi enviado para geração.'),None
    except Exception as exc:
        if generation_attempted:
            return ambiguous_response()
        return adapter._resposta_de_excecao(exc),None
