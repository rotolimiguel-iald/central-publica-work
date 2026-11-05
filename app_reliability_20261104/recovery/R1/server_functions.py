def agent_loop(messages, user="?", max_tokens=4096, temperature=0.7,
               ferramentas=None, operator_authorized=False, motor=None, max_voltas=None,
               max_chars_canonico=None, executar=None, responder_na_ultima=False, task_control=None,
               verificar_payload=None, task_tool_names=()):
    """
    Agent loop: sends messages to llama-server with public tools.
    If model responds with tool_call, executes and returns result.
    Repeats until final response (no tool_call) or MAX_AGENT_LOOPS.

    Yields SSE-formatted chunks for streaming to the client.
    The client (iald_chat.html / app iOS) sees normal streaming.

    `motor` (14/09/2026, aditivo): um iald_motores.AdaptadorAgente. Sem ele, o destino
    é o llama-server local, como sempre; com ele, a mesma volta fala com a OpenAI.

    `max_voltas` (14/09/2026 noite, aditivo): teto de voltas deste pedido. None = o
    MAX_AGENT_LOOPS de sempre. O plano gratuito usa menos: cada volta é uma chamada
    paga, com a janela inteira de entrada.

    14/09/2026 (noite, revisão de testes A2 — aditivos, sem eles tudo como antes):
      `max_chars_canonico`: teto dos resultados das consultas canônicas (iald_kernel_*,
          iald_atlas_*, iald_public_*), que antes nunca eram cortados (até 20.000 caracteres
          por leitura). O plano gratuito usa GRATUITO_MAX_CHARS_FERRAMENTA.
      `executar(nome, argumentos, user=, operator_authorized=)`: quem executa as ferramentas
          (padrão: execute_public_tool). O plano gratuito usa _executar_ferramenta_gratuito.
      `responder_na_ultima`: na última volta permitida o modelo externo recebe
          tool_choice "none" e responde com o que já leu, em vez de terminar em
          "Limite de iterações do agente atingido".

    β_TGL = α × √e — O Verbo é recursivo.
    """
    extra_task_names = frozenset(task_tool_names) - task_session.NAMES
    loop_count = 0
    if max_voltas is None:
        max_voltas = MAX_AGENT_LOOPS

    # Descarrega os cabeçalhos SSE IMEDIATAMENTE. Sem isto o primeiro byte só sai
    # depois que o modelo termina — e a Cloudflare derruba a conexão antes disso.
    yield ": iald-agent-inicio\n\n"

    # Primeiro sinal visível: a interface mostra que o agente assumiu, em vez de
    # deixar a tela parada enquanto o modelo decide se vai usar ferramenta.
    yield ("data: " + json.dumps({
        "iald_status": {"fase": "pensando", "rotulo": "analisando o pedido"}
    }, ensure_ascii=False) + "\n\n")

    # ── Messages pass through UNTOUCHED ──
    # The kernel (system prompt) is the ONLY authority.
    # The web server provides tools but does NOT inject instructions.
    # The model decides when to use tools based on the kernel's gradient.
    current_messages = list(messages)
    busca_falhou = False       # 15/09/2026: search_web devolveu MSG_BUSCA_INDISPONIVEL neste pedido

    while loop_count < max_voltas:
        current_messages = app_memory.project_messages(current_messages)
        if task_control is not None: task_control.check()
        loop_count += 1
        # 15/09/2026: na última volta permitida, ou depois que a busca na internet falhou, o modelo
        # responde com o que já leu em vez de pedir outra ferramenta. Antes a volta final terminava
        # em "Limite de iterações do agente atingido", sem resposta (reclamação do operador, 15/09).
        forcar_resposta = busca_falhou or loop_count == max_voltas

        # Non-streaming call WITH tools (needed to detect tool_calls)
        payload = {
            "model": "qwen3",
            "messages": current_messages,
            # None = chamador antigo, que continua recebendo tudo (aditivo).
            "tools": ferramentas if ferramentas is not None else PUBLIC_TOOLS,
            "tool_choice": "auto",
            "max_tokens": max_tokens,
            "temperature": temperature,
            # Ferramentas nunca pensam em silêncio: este caminho lê message.content
            # e reasoning_content ficaria invisível (o mesmo bug do chat mudo).
            "chat_template_kwargs": {"enable_thinking": False},
        }

        # ── STREAMING REAL (02/08/2026) ──
        # Antes: a chamada era NAO-streaming e o texto so aparecia quando o modelo
        # terminava; o "streaming" que o cliente via era falso, montado aqui
        # cortando a resposta pronta em pedacos de 30 caracteres.
        # Agora o texto sai token a token, como no caminho direto.
        payload["stream"] = True
        conteudo_parcial = []
        acumulador_tools = {}     # index -> {id, name, arguments}
        finish_reason = ""
        houve_texto = False
        erro_stream = None

        destino, cabecalhos = f"{LLAMA_URL}/v1/chat/completions", None
        if motor is not None:
            payload = motor.payload(payload)
            destino, cabecalhos = motor.url, motor.cabecalhos
            if forcar_resposta and payload.get("tools"):
                payload["tool_choice"] = "none"
        elif forcar_resposta:
            # llama-server: sem a lista de ferramentas o template não oferece nenhuma
            payload.pop("tools", None)
            payload.pop("tool_choice", None)

        if verificar_payload is not None:
            try:
                verificar_payload(payload)
            except (ValueError, OSError, KeyError, TypeError) as exc:
                message = (str(exc) if isinstance(exc, native_memory.NativeContextError)
                           else 'Memória canônica nativa indisponível ou divergente.')
                yield ': iald-sem-selo\n\n'
                yield 'data: ' + json.dumps({'error': message,
                    'choices': [{'delta': {'content': message}, 'finish_reason': 'stop'}]},
                    ensure_ascii=False) + '\n\n'
                yield 'data: [DONE]\n\n'
                return

        # 21/09/2026 (motor claude): o motor pode trazer o próprio envio (motor.enviar, que traduz o
        # payload OpenAI para a API do provedor e devolve linhas no formato OpenAI). Sem ele, o
        # req_lib.post de sempre (openai; os testes o trocam por um falso).
        enviar = getattr(motor, "enviar", None) if motor is not None else None
        externo_nao_openai = motor is not None and getattr(motor, "provedor", iald_motores.OPENAI) != iald_motores.OPENAI

        def model_lines():
            if task_control is not None: task_control.check()
            if motor is None:
                yield from _linhas_do_stream(lambda: app_memory.http_call('model.agent_loop', req_lib.post, 
                    destino, json=payload, headers=cabecalhos, stream=True, timeout=600))
            else:
                try:
                    if callable(enviar):
                        fazer = lambda: app_memory.http_call('model.adapter', enviar, payload, (10, motor.cfg.timeout))    # noqa: E731
                    else:
                        fazer = lambda: app_memory.http_call('model.agent_loop', req_lib.post,                                  # noqa: E731
                            destino, json=payload, headers=cabecalhos, stream=True,
                            timeout=(10, motor.cfg.timeout))
                    yield from iald_motores.linhas_com_espera(fazer, intervalo=AGENT_KEEPALIVE_SEC,
                        recovery=getattr(motor, 'recovery_attempt', None))
                except iald_motores.ErroProvedor as exc:
                    # 21/09/2026: no claude, recusa ANTES de gerar que certamente não foi cobrada (402
                    # sem crédito, 529 sobrecarga, 503 sem SDK ou sem conexão…) libera a reserva.
                    # ⚠ CORREÇÃO AO LADO (21/09/2026, revisão de custo/wire): era "todo status ≠ 502" —
                    # o 504 (tempo esgotado; a Anthropic pode ter processado o prefixo) saía como US$ 0
                    # e a falha de conexão (502) ficava cobrada pela estimativa cheia. A lista agora é
                    # a de iald_motor_claude.recusa_sem_cobranca; 500/502/504 ficam na reserva.
                    if externo_nao_openai:
                        sem_cobranca = iald_motor_claude.recusa_sem_cobranca(exc.status, exc.codigo)
                    else:
                        sem_cobranca = exc.status in (400, 401, 403, 404, 413, 422, 429)
                    if sem_cobranca:
                        motor.conta.descartar_ultima_chamada()
                    if not externo_nao_openai:
                        _marcar_sem_credito(exc)              # 15/09/2026: bandeira do saldo (só OpenAI)
                    else:
                        _marcar_sem_credito_claude(exc)       # 22/09/2026: a bandeira do crédito da Anthropic
                    yield ("erro", iald_motores.mensagem_ao_usuario(exc))
        for tipo, valor in model_lines():
            if tipo == "keepalive":
                yield ": keepalive\n\n"
                continue
            if tipo == "erro":
                erro_stream = valor
                break
            if tipo == "fim":
                break

            notices = getattr(motor, "context_notices", None) if motor is not None else None
            while notices:
                yield "data: " + json.dumps({"iald_status": notices.pop(0)}, ensure_ascii=False) + "\n\n"
            linha = valor
            if not linha:
                continue
            if isinstance(linha, bytes):
                linha = linha.decode("utf-8", "replace")
            linha = linha.strip()
            if not linha.startswith("data: "):
                continue
            corpo = linha[6:].strip()
            if corpo == "[DONE]":
                break
            try:
                d = json.loads(corpo)
            except json.JSONDecodeError:
                continue
            if externo_nao_openai and isinstance(d.get("error"), dict):
                # 21/09/2026: erro NO MEIO do stream (o envio do claude o devolve como linha
                # {"error": …} antes do [DONE]); a volta termina com o motivo, não com "(sem resposta)"
                # nem com ferramenta de argumentos cortados. O caminho da OpenAI fica como era.
                e = d["error"]
                erro_stream = iald_motores.mensagem_ao_usuario(iald_motores.ErroProvedor(
                    502, e.get("code"), e.get("type"), e.get("param"), e.get("message")))
                break
            if externo_nao_openai and isinstance(d.get("iald_aviso"), dict):
                # 21/09/2026 (revisão): o aviso que o envio do claude monta (a recusa do modelo, com
                # retirar_resposta) passa ao app como está; antes era descartado aqui
                yield "data: " + json.dumps({"iald_aviso": d["iald_aviso"]}, ensure_ascii=False) + "\n\n"
                continue
            if motor is not None and isinstance(d.get("usage"), dict):
                motor.uso(d["usage"])          # o custo exato, que a OpenAI manda no fim

            escolha = (d.get("choices") or [{}])[0]
            delta = escolha.get("delta") or {}
            if escolha.get("finish_reason"):
                finish_reason = escolha["finish_reason"]

            # Acumula tool_calls: o primeiro delta traz id/name, os seguintes vao
            # concatenando os fragmentos de `arguments` (medido: 8 deltas para uma
            # chamada de consultar_acervo).
            for tc in (delta.get("tool_calls") or []):
                i = tc.get("index", 0)
                alvo = acumulador_tools.setdefault(
                    i, {"id": "", "name": "", "arguments": ""})
                if tc.get("id"):
                    alvo["id"] = tc["id"]
                fn = tc.get("function") or {}
                if fn.get("name"):
                    alvo["name"] = fn["name"]
                if fn.get("arguments"):
                    alvo["arguments"] += fn["arguments"]

            pedaco = delta.get("content")
            if pedaco:
                if not houve_texto:
                    # primeiro token de texto: encerra o indicador de atividade
                    houve_texto = True
                    yield ("data: " + json.dumps(
                        {"iald_status": {"fase": "respondendo"}},
                        ensure_ascii=False) + "\n\n")
                conteudo_parcial.append(pedaco)
                if motor is not None and callable(getattr(motor, "texto", None)):
                    motor.texto(pedaco)        # saída vista (estimativa sem `usage`), 14/09 noite
                yield ("data: " + json.dumps(
                    {"choices": [{"delta": {"content": pedaco},
                                  "finish_reason": None}]},
                    ensure_ascii=False) + "\n\n")

        if erro_stream is not None:
            # 22/09/2026 — Selo IALD: falha não recebe selo (comentário SSE; o app ignora linha ":")
            yield ": iald-sem-selo\n\n"
            yield ("data: " + json.dumps(
                {"choices": [{"delta": {"content":
                    f"Erro de conexão com o modelo: {erro_stream}"}}]},
                ensure_ascii=False) + "\n\n")
            yield "data: [DONE]\n\n"
            return

        tool_calls = [
            {"id": v["id"] or f"call_{loop_count}_{k}", "type": "function",
             "function": {"name": v["name"], "arguments": v["arguments"]}}
            for k, v in sorted(acumulador_tools.items()) if v["name"]
        ]
        message = {"content": "".join(conteudo_parcial), "tool_calls": tool_calls}
        if tool_calls and not finish_reason:
            finish_reason = "tool_calls"

        if tool_calls and finish_reason == "tool_calls":
            # ── Model wants to call tool(s) ──
            # Add assistant message (with tool_calls) to conversation history
            assistant_msg = {
                "role": "assistant",
                "content": message.get("content", "") or "",
                "tool_calls": tool_calls,
            }
            current_messages.append(assistant_msg)

            # 21/09/2026 (revisão — wire): o motor pode dizer que a entrada de uma chamada NÃO é JSON
            # válido (claude: EstadoClaude.entrada_invalida). Essa ferramenta não roda com {} — o
            # bruto volta ao modelo como erro ({"INVALID_JSON": …}, is_error no envio do claude)
            # [KNOWN — skill claude-api, tool-use-concepts.md, eager input streaming]. Sem o gancho
            # (openai, llama), como antes.
            entrada_invalida = getattr(motor, "entrada_invalida", None) if motor is not None else None

            # Execute each tool call
            for tc in tool_calls:
                fn = tc.get("function", {})
                tool_name = fn.get("name", "?")
                tool_args_str = fn.get("arguments", "{}")
                tool_id = tc.get("id", f"call_{loop_count}")

                if callable(entrada_invalida) and entrada_invalida(tool_id):
                    auth_log("AGENT_TOOL_INVALIDA", user, f"loop={loop_count} tool={tool_name} (JSON inválido; não rodou)")
                    current_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "content": json.dumps({"INVALID_JSON": str(tool_args_str or "")[:4000]}, ensure_ascii=False),
                    })
                    continue

                try:
                    tool_args = json.loads(tool_args_str)
                except (json.JSONDecodeError, TypeError):
                    tool_args = {}

                # Log
                auth_log("AGENT_TOOL", user,
                         f"loop={loop_count} tool={tool_name} "
                         f"args={'[omitted]' if tool_name in extra_task_names else json.dumps(tool_args, ensure_ascii=False)[:200]}")
                log_request(user, f"/agent/{tool_name}", "TOOL",
                            status="agent_tool")

                # ── SINAL DE ATIVIDADE PARA A INTERFACE (02/08/2026) ──
                # Antes disto o usuário ficava CEGO durante o agent loop: até 6
                # chamadas encadeadas, algumas lentas (busca na web, prova viva),
                # sem um único sinal na tela. Não dava para distinguir "pensando"
                # de "travou".
                # Vai num campo PRÓPRIO (`iald_status`), nunca em delta.content —
                # se fosse no content, entraria no texto da resposta.
                yield ("data: " + json.dumps({
                    "iald_status": {
                        "fase": "ferramenta",
                        "tool": tool_name,
                        "rotulo": _ROTULO_FERRAMENTA.get(tool_name, tool_name),
                        "loop": loop_count,
                        "max_loops": max_voltas,
                    }
                }, ensure_ascii=False) + "\n\n")

                # Execute — busca na web / acervo / prova viva podem demorar;
                # o keepalive impede que o túnel derrube a conexão nesse meio-tempo.
                if busca_falhou and tool_name == "search_web":
                    # 15/09/2026: a busca já falhou neste pedido; não bate de novo nos provedores
                    result = MSG_BUSCA_INDISPONIVEL
                else:
                    result = yield from _com_keepalive(
                        lambda: app_memory.call('tool.' + tool_name, (executar or execute_public_tool), tool_name, tool_args, user=user,
                                                                  operator_authorized=operator_authorized)
                        if tool_name in {(t.get("function") or {}).get("name") for t in
                                         (ferramentas if ferramentas is not None else PUBLIC_TOOLS)}
                        else "Ferramenta não autorizada para esta sessão.",
                        **({'task_control':task_control} if task_control is not None else {})
                    )
                app_memory.tool_result(tool_name, tool_args, result)
                if task_control is not None: task_control.check()
                if tool_name == "search_web" and str(result or "").startswith(BUSCA_INDISPONIVEL_PREFIXO):
                    busca_falhou = True

                yield ("data: " + json.dumps({
                    "iald_status": {
                        "fase": "ferramenta_ok",
                        "tool": tool_name,
                        "rotulo": _ROTULO_FERRAMENTA.get(tool_name, tool_name),
                        "chars": len(result or ""),
                    }
                }, ensure_ascii=False) + "\n\n")

                # Truncate if too large (protect context window)
                if tool_name in task_session.NAMES | extra_task_names:
                    result = task_bridge.encode_task_result(result)
                elif (len(result) > AGENT_MAX_RESULT_CHARS
                        and tool_name not in ('search_tgl', 'fetch_tgl')
                        and not tool_name.startswith(("iald_kernel_", "iald_atlas_", "iald_public_"))):
                    result = (result[:AGENT_MAX_RESULT_CHARS]
                              + f"\n\n[...truncado, {len(result)} chars total]")
                elif (max_chars_canonico is not None and len(result) > max_chars_canonico
                        and tool_name.startswith(("iald_kernel_", "iald_atlas_", "iald_public_"))):
                    result = (result[:max_chars_canonico]
                              + f"\n\n[...truncado no uso gratuito, {len(result)} chars total; "
                                "peça um trecho menor]")

                # Add tool result to conversation
                current_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_id,
                    "content": result,
                })

            # Continue loop — model will process tool results
            continue

        else:
            # ── Resposta final: o texto JA FOI ENVIADO token a token acima ──
            # Nada de reenviar. Aqui so se fecha o stream — e se o modelo nao disse
            # absolutamente nada (nem texto, nem ferramenta), avisa em vez de deixar
            # o balao vazio.
            if not houve_texto:
                yield ": iald-sem-selo\n\n"      # 22/09/2026 — Selo IALD: "(sem resposta)" não é fala do modelo
                yield ("data: " + json.dumps(
                    {"iald_status": {"fase": "respondendo"}},
                    ensure_ascii=False) + "\n\n")
                yield ("data: " + json.dumps(
                    {"choices": [{"delta": {"content": "(sem resposta)"},
                                  "finish_reason": None}]},
                    ensure_ascii=False) + "\n\n")
            yield ("data: " + json.dumps(
                {"choices": [{"delta": {}, "finish_reason": "stop"}]}) + "\n\n")
            yield "data: [DONE]\n\n"
            return

    # Max loops exceeded
    warn = "\n\n⚠️ Limite de iterações do agente atingido."
    yield ": iald-sem-selo\n\n"          # 22/09/2026 — Selo IALD: sem resposta final, sem selo
    yield f"data: {json.dumps({'choices': [{'delta': {'content': warn}, 'finish_reason': 'stop'}]}, ensure_ascii=False)}\n\n"
    yield "data: [DONE]\n\n"


def _sse_aviso(texto, tipo, extra=None):
    """Resposta de chat que só avisa. HTTP 200 de propósito: o app trata 401/403 como sessão
    vencida e qualquer outro erro como servidor fora — e a pessoa não leria o motivo."""
    aviso = {"tipo": tipo, "texto": texto}
    aviso.update(extra or {})

    def gerar():
        yield "data: " + json.dumps({"iald_aviso": aviso}, ensure_ascii=False) + "\n\n"
        yield "data: " + json.dumps({"choices": [{"delta": {"content": texto}, "finish_reason": None}]},
                                    ensure_ascii=False) + "\n\n"
        yield "data: " + json.dumps({"choices": [{"delta": {}, "finish_reason": "stop"}]}) + "\n\n"
        yield "data: [DONE]\n\n"
    return Response(gerar(), status=200, content_type="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


def _chat_openai(req_json, user, registro, is_stream, tokens_in, *, task_scope=None, dispatch_check=None, routing_instruction=None, recovery_attempt=None):
    """Atende um /v1/chat/completions pela OpenAI. None = devolver ao caminho nativo.

    14/09/2026 (noite): o plano da conta manda — cota em tokens por dia e por mês, teto em
    dólar, saída máxima, agente e modo pensar (iald_motores.limites_do_plano). O plano
    gratuito NUNCA devolve None: a reserva nativa não vale para ele, porque a porta aberta
    jamais pode cair na máquina (e na memória) do operador.

    14/09/2026 (noite, tarefa S2 — revisões de testes A1/A2, segurança ALTO 1/MÉDIO 1), no plano
    gratuito: uma resposta em andamento por chave de cota; saldo de tokens conferido antes de
    montar, histórico mais antigo descartado até caber no saldo e conferência de novo antes de
    CADA chamada (SaldoDoPedido); no máximo 2 voltas e resultado canônico cortado em qualquer
    modo de memória; Atlas fora por padrão; conversa acima de TETO_TOTAL_TEXTO_GRATUITO recusada;
    resposta moderada no fim. Para todos: todo o texto do cliente que vai ao modelo é moderado
    (histórico, perfil e última mensagem, em blocos, sem descartar excedente); aviso "limite"
    sempre com bloqueado_por e cota.

    21/09/2026: o corpo virou _chat_externo(…, motor) — o MESMO caminho serve o claude. Este nome
    continua (api_post e os testes o chamam) e responde exatamente como antes.
    """
    return _chat_externo(req_json, user, registro, is_stream, tokens_in, iald_motores.OPENAI, task_scope=task_scope, dispatch_check=dispatch_check, routing_instruction=routing_instruction, recovery_attempt=recovery_attempt)


def _chat_automatico(req_json,user,registro,is_stream,tokens_in):
    lease = app_router.acquire(user)
    if lease is None:
        return _sse_aviso('Uma resposta desta conta já está em andamento.','em_andamento')
    transferred = False
    task_control = None
    def finish_task():
        if task_control is not None: task_control.close(lease.release)
        else: lease.release()
    try:
        if not app_router.available():
            return _sse_aviso('O modo automático aguarda a validação da conexão JEV.','motor_indisponivel')
        response = _chat_automatico_autorizado(req_json,user,registro,is_stream,tokens_in)
        task_control = getattr(response,'iald_task_control',None)
        if isinstance(response,Response) and response.is_streamed:
            original = response.response
            def stream_with_lease():
                try:
                    yield from original
                finally:
                    try:
                        close = getattr(original,'close',None)
                        if close: close()
                    finally:
                        finish_task()
            response.response = stream_with_lease()
            response.call_on_close(finish_task)
            transferred = True
        return response
    finally:
        if not transferred: finish_task()


def _chat_automatico_autorizado(req_json,user,registro,is_stream,tokens_in,*,_recovery=None):
    from copy import deepcopy
    from flask import stream_with_context
    recovery = _recovery or app_recovery.Recovery(req_json, MOTORES_CFG)
    if _recovery is None:
        recovery.wallet = wallet_runtime.current()
        recovery.memory = app_memory.current()
    elif (wallet_runtime.current() is not recovery.wallet
            or app_memory.current() is not recovery.memory
            or _motor_do_usuario(user)[0] != app_router.AUTO):
        return _sse_aviso('O estado ou a autorização da tarefa mudou.', 'motor_indisponivel')
    if not app_router.allowed(registro,user):
        return _sse_aviso('Modo automático não liberado para esta conta.','motor_indisponivel')
    consent=_consentimento_automatico(registro,user)
    if not consent['dado']:
        return _sse_aviso('Leia e aceite o aviso do modo automático.','consentimento_ia',
            dict(versao=consent['versao'],provedor=consent['provedor'],detalhe=consent['texto']))
    if not is_stream or not isinstance(req_json,dict):
        return jsonify({'error':'Envie chat com stream: true.'}),400
    try:
        client=req_json.get('messages')
        private_media = _private_runtime_for(req_json,user,automatic=True)
        if private_media is not None:
            client=private_media.canonicalize(client,provider='mimo')
            req_json=dict(req_json,messages=client)
        media = app_providers.request_media(client)
        has_media = bool(media['kinds'])
        if has_media:
            if not app_providers.allowed(registro,user,'mimo'):
                return _sse_aviso('MiMo não autorizado para estes anexos. Nada foi enviado.','recurso_indisponivel')
            media_consent = _consentimento_do_motor(registro,'mimo')
            if not media_consent['dado']:
                return _sse_aviso('Leia e aceite o aviso do MiMo para enviar estes anexos.','consentimento_ia',
                    dict(versao=media_consent['versao'],provedor=media_consent['provedor'],detalhe=media_consent['texto']))
        app_providers.wire_messages(client,'routing_validation',provider='mimo' if has_media else None,
            images_authorized=has_media,media_authorized=has_media,private_media=private_media)
        candidates=[]
        candidate_models={}
        for row in _opcoes_de_motor(registro,user):
            key=row['id']
            if key not in app_router.DESCRIPTIONS or not row.get('disponivel'):continue
            if key=='nativa' and MODERACAO_LIGADA and not iald_motores.consentiu(registro,'openai'):continue
            consent_provider='claude' if key.startswith('claude-') else key
            if key == 'nativa' or iald_motores.consentiu(registro,consent_provider):
                candidates.append(key)
                if isinstance(row.get('modelo'),str) and row['modelo']:candidate_models[key]=row['modelo']
        if not candidates:raise ValueError('No consented executor')
        candidates=[key for key in candidates if key not in recovery.excluded
            and _automatic_budget_available(registro,user,key)]
        if not candidates:
            return _sse_aviso('Nenhum modelo autorizado tem orçamento disponível e verificável agora. Nada foi enviado ao JEV.', 'limite')
        operator_context = (operator_bench.routing_context(registro,user)
                            if operator_bench.is_operator(registro,user) else None)
        routing_prompt = media['prompt'] or ('Analise o anexo enviado.' if has_media else '')
        media_budget_options=None
        if private_media is not None:
            private_media.authorize_dispatch()
            preview=_private_preview_body(client,user,registro,private_media)
            policies=private_media_host.video_proposals(private_media.budget_metadata(client))
            media_budget_options=private_media.routing_options(preview,proposals=policies)
        chosen,receipt=app_router.choose(routing_prompt,candidates,operator_context=operator_context,
            model_ids={key:candidate_models[key] for key in candidates if key in candidate_models},
            multimodal=has_media,media=media,media_integrated=has_media,media_budget_options=media_budget_options)
        if chosen not in candidates:raise PermissionError('Executor outside admitted candidates')
        recovery.check_science(receipt)
        if private_media is not None:
            if chosen!='mimo':raise MediaUnavailable('Incompatible private media destination')
            selected_media_plan=private_media.select_routing_policy(receipt['media_policy_id'])
            if selected_media_plan!=receipt['media_budget']:raise MediaError('Changed policy receipt')
        # Recheck permissions/consent after the router returns, before generation.
        current=load_users_estrito().get(user,{})
        if not app_router.allowed(current,user) or not iald_motores.consentiu(current,app_router.AUTO):
            raise PermissionError('Access revoked')
        if chosen not in {r['id'] for r in _opcoes_de_motor(current,user) if r.get('disponivel')}:
            raise PermissionError('Executor revoked')
        consent_provider='claude' if chosen.startswith('claude-') else chosen
        if chosen != 'nativa' and not iald_motores.consentiu(current,consent_provider):
            raise PermissionError('Executor consent revoked')
        if operator_context is not None and not operator_bench.is_operator(current,user):
            raise PermissionError('Operator access revoked')
        if not _automatic_budget_available(current,user,chosen):raise PermissionError('Executor budget changed')
        routing_instruction=app_router.route_instruction(receipt)
        task_scope=recovery.scope
        if task_scope is None and chosen not in ('kimi','nativa'):
            task_scope=_new_app_task_scope(user,executor=chosen)
        if task_scope is not None:
            task_scope.executor=chosen
            recovery.bind_scope(task_scope,receipt,app_router)
        selected=dict(current,motor=chosen)
        if chosen.startswith('claude-'):
            selected.update(CLAUDE_ROUTES.select(chosen,current,user))
            response=_chat_claude(req_json,user,selected,is_stream,tokens_in,task_scope=task_scope,dispatch_check=_dispatch_guard(user,chosen,True),routing_instruction=routing_instruction)
        elif chosen in app_providers.MODELS:
            response=_chat_avaliacao(req_json,user,selected,is_stream,chosen,task_scope=task_scope,dispatch_check=_dispatch_guard(user,chosen,True),routing_instruction=routing_instruction,private_media=private_media,media_admission=receipt.get('media_budget'))
        elif chosen=='openai':
            response=_chat_openai(req_json,user,selected,is_stream,tokens_in,task_scope=task_scope,dispatch_check=_dispatch_guard(user,chosen,True),routing_instruction=routing_instruction,
                recovery_attempt=(recovery.attempt if not recovery.reselected and private_media is None and not has_media else None))
        elif chosen=='nativa':
            response=_chat_nativa_automatica(req_json,user,current,routing_instruction=routing_instruction)
        else:raise ValueError('No compatible executor')
        if response is None:raise ValueError('No compatible executor')
        if task_scope:response.iald_task_control=task_scope.control
        if _recovery is None and isinstance(response,Response) and response.mimetype=='text/event-stream':
            response=recovery.wrap(response,lambda: _chat_automatico_autorizado(
                deepcopy(recovery.request),user,load_users_estrito().get(user,{}),is_stream,tokens_in,_recovery=recovery))
            response.response=stream_with_context(response.response)
        return response
    except MediaUnavailable:
        return _sse_aviso(private_media_host.PUBLIC_REFERENCE_REFUSAL,'anexo_indisponivel')
    except MediaBudgetError as exc:
        # Whitelisted local diagnosis only; never echo arbitrary exception data.
        if str(exc)=='Uncertain media policy; no automatic quality substitution':
            return _sse_aviso('O seletor não atingiu a confiança mínima para a política de mídia. Núcleo, histórico e anexo foram preservados. O seletor pode ter sido consultado; o anexo não foi enviado ao modelo executor. Nenhum reenvio automático.', 'politica_midia_incerta')
        return _sse_aviso('Anexo excede o contexto, bytes ou orçamento disponíveis; núcleo e histórico preservados. O seletor pode ter sido consultado; nada foi enviado ao modelo executor.', 'anexo_excede_contexto')
    except MediaError:
        return _sse_aviso('Não foi possível validar o anexo ou sua admissão; núcleo e histórico preservados. O seletor pode ter sido consultado; nada foi enviado ao modelo executor.', 'anexo_validacao_recusada')
    except app_router.RoutingContextOverflow:
        return _sse_aviso('A memória obrigatória desta conversa excede o espaço do seletor automático. Nada foi enviado aos provedores. Abra uma nova conversa para continuar; a conversa anterior permanece salva.','roteamento_contexto_excedido')
    except (ValueError,PermissionError,OSError,KeyError,TypeError,RuntimeError):
        return _sse_aviso('Não foi possível concluir a escolha automática. Tente novamente em alguns instantes; não houve reenvio para outro executor.','motor_indisponivel')


def _chat_externo(req_json, user, registro, is_stream, tokens_in, motor=iald_motores.OPENAI, *, task_scope=None, dispatch_check=None, routing_instruction=None, recovery_attempt=None):
    """O caminho externo inteiro, para o provedor do `motor` (21/09/2026; antes era _chat_openai).

    Com motor openai, byte a byte o de antes. Com motor claude, o MESMO pipeline — reservas, razão,
    rótulo, voltas do agente, ferramentas, medição TGLC — e o MESMO prefixo TGL (_contexto_externo), com:
    configuração, razão, reservas e pedidos por minuto do claude; consentimento da Anthropic;
    max_completion_tokens = CLAUDE_CFG.max_saida (o pensamento adaptativo gasta a mesma saída); entrada
    estimada e prefixo descontado da cota × fator_tokens; envio por iald_motor_claude.post_como_openai
    (um EstadoClaude por pedido, para o pensamento assinado voltar nas voltas com ferramenta); Atlas
    sem §V/§VI/§X (_executar_ferramenta_claude); moderação na chave da OpenAI; nunca a bandeira de
    crédito da OpenAI; nunca None."""
    dispatch_check = dispatch_check or _dispatch_guard(user,motor,False)
    claude = motor == iald_motores.CLAUDE
    if claude: recovery_attempt = None
    razao = RAZAO_CLAUDE if claude else RAZAO_OPENAI
    limitador = LIMITE_CLAUDE if claude else LIMITE_OPENAI
    try:
        cfg = (CLAUDE_ROUTES.configuration(registro, user) if claude
               else iald_motores.config_da_conta(MOTORES_CFG, registro))
    except (ValueError, PermissionError, OSError, KeyError):
        return _sse_aviso("Modelo Claude indisponível para esta conta.", "motor_indisponivel")
    haiku = claude and cfg.modelo == _HAIKU_PROFILE.model
    if haiku and not _haiku_client_ready():
        return _sse_aviso("Atualize o aplicativo para usar o Haiku com memória integral.", "recurso_indisponivel")
    if claude:
        # o prefixo e as consultas canônicas são os da casa: o modo de memória é o da configuração da OpenAI
        cfg.memoria_modo = MOTORES_CFG.memoria_modo
    if not isinstance(req_json, dict):
        req_json = {}
    admin = bool(registro.get("admin"))
    plano = iald_motores.plano_de(registro)
    gratuito = plano == iald_motores.GRATUITO
    chave_cota = _chave_cota_de(registro, user)
    modelo = iald_motores.modelo_para(registro, cfg)
    if claude and not CLAUDE_ROUTES.options(registro, user):
        # a outra trava: api_post só chega aqui com escolher_motor == claude; conferido de novo, e
        # recusa visível — nunca desvio para outro motor
        print(f"[claude] {user}: conta fora da lista do claude (ou gratuita); nada enviado", flush=True)
        return _sse_aviso(MSG_CLAUDE_NAO_LIBERADO, "motor_indisponivel")
    if claude and _memoria_modo_integral(MOTORES_CFG):
        # 21/09/2026 (revisão de segurança, ALTO): em atlas_integral o prefixo leva o Atlas INTEIRO,
        # com §V (patentes), §VI (caminhos) e §X (estado operacional) — o que o operador mandou deixar
        # FORA da Anthropic ("O mesmo pacote do ChatGPT", sem §V/§VI/§X). Antes só o gratuito era
        # recusado neste modo, e a conta do claude nunca é gratuita.
        print(f"[claude] {user}: IALD_MEMORIA_MODO=atlas_integral; nada enviado à Anthropic", flush=True)
        return _sse_aviso(MSG_CLAUDE_ATLAS_INTEGRAL, "motor_indisponivel")
    if gratuito and _memoria_modo_integral(cfg):
        # 14/09/2026 (noite, tarefa SV): o prompt levaria o Atlas inteiro, com §V, §VI e §X
        print(f"[motores] {user}: plano gratuito recusado em IALD_MEMORIA_MODO=atlas_integral", flush=True)
        return _sse_aviso(MSG_GRATUITO_ATLAS_INTEGRAL, "motor_indisponivel")
    motivo = _motor_externo_indisponivel(modelo, cfg) if claude else _motor_externo_indisponivel(modelo)
    if motivo:
        print(f"[motores] {user}: {motivo}", flush=True)
        if cfg.reserva_nativa and not gratuito and not claude:
            return None
        return _sse_aviso(motivo, "motor_indisponivel")
    if not is_stream:
        return jsonify({"error": "O motor externo só atende com stream: true."}), 400
    if gratuito:
        # 14/09/2026 (noite, tarefa SV — revisão COTAS, regressão 1): imagem no gratuito é recusada
        # ANTES de qualquer conta de saldo, sem chamar o modelo (ver MSG_IMAGEM_GRATUITO)
        mensagens_cliente = req_json.get("messages") if isinstance(req_json.get("messages"), list) else []
        ultima_do_usuario = next((m for m in reversed(mensagens_cliente)
                                  if isinstance(m, dict) and m.get("role") == "user"), None)
        if ultima_do_usuario is not None and _tem_imagem(ultima_do_usuario.get("content")):
            print(f"[motores] {user}: imagem recusada no plano gratuito", flush=True)
            return _sse_aviso(MSG_IMAGEM_GRATUITO, "recurso_indisponivel", {"recurso": "imagens"})
        if any(isinstance(m, dict) and _tem_imagem(m.get("content")) for m in mensagens_cliente):
            req_json = dict(req_json, messages=[_sem_imagens(m) for m in mensagens_cliente])
    if claude and not iald_motores.consentiu(registro, iald_motores.CLAUDE):
        # 21/09/2026: o consentimento da ANTHROPIC — o da OpenAI não o substitui
        return _sse_aviso(
            "Esta conta está no Claude, da Anthropic, e isso precisa do seu consentimento. Abra o "
            "aviso para ler o que é enviado e decidir.",
            "consentimento_ia",
            {"versao": iald_motores.VERSAO_CONSENTIMENTO_ANTHROPIC, "provedor": "Anthropic", "modelo": modelo,
             "detalhe": iald_motores.TEXTO_CONSENTIMENTO_ANTHROPIC})
    if not claude and not iald_motores.consentiu(registro):
        return _sse_aviso(
            "Esta conta responde pelo serviço de IA da OpenAI e isso precisa do seu "
            "consentimento. Abra o aviso para ler o que é enviado e decidir.",
            "consentimento_ia",
            {"versao": iald_motores.VERSAO_CONSENTIMENTO, "provedor": "OpenAI", "modelo": modelo,
             "detalhe": iald_motores.TEXTO_CONSENTIMENTO})
    try:dispatch_check()
    except PermissionError:return _sse_aviso('Acesso ou consentimento revogado.','motor_indisponivel')
    soltar = []           # o que devolver no fim: a marca de andamento e a vaga do semáforo
    entregue = False
    if gratuito:
        marca = _MarcaAndamento.tomar(chave_cota)
        if marca is None:
            print(f"[motores] {user}: já há uma resposta em andamento nesta cota gratuita", flush=True)
            return _sse_aviso(MSG_EM_ANDAMENTO, "em_andamento")
        soltar.append(marca.soltar)
    try:
        permitido, motivo, bloqueado_por = wallet_runtime.permit(
            cfg, razao, limitador, user, admin, plano=plano, chave_cota=chave_cota, detalhado=True)
        if not permitido:
            return _aviso_limite(motivo, bloqueado_por, user, registro, motor)
        limites = iald_motores.limites_do_plano(cfg, plano)
        cfg.cota_usuario_usd = cfg.cota_operador_usd = limites["usd_dia"]
        cfg.janela = iald_motores.janela_do_plano(cfg, plano)
        saldo_inicial = None
        if gratuito and not wallet_runtime.enabled():
            try:
                saldo_inicial, campo_saldo = iald_motores.saldo_de_tokens(
                    limites, razao.leitura_de_cota(user, chave_cota, plano))
            except Exception as exc:          # noqa: BLE001 — fail-closed
                print(f"[motores] controle de uso ilegível ({exc}); gasto bloqueado", flush=True)
                return _aviso_limite(iald_motores.MSG_RAZAO_ILEGIVEL, "razao", user, registro, motor)
            if saldo_inicial < iald_motores.SALDO_MINIMO_TOKENS:
                return _aviso_limite(iald_motores.MSG_SALDO_MES if campo_saldo == "tokens_mes"
                                     else iald_motores.MSG_SALDO_DIA, campo_saldo, user, registro, motor)

        superficie = "app" if session.get("app_surface") else str(req_json.get("iald_surface") or "web").strip().lower()
        modo = "think" if (req_json.get("iald_mode") == "think" and limites["pensar"]) else "fast"
        mensagens = req_json.get("messages") or []
        tem_imagem, texto_ultima = False, ""
        for m in reversed(mensagens):
            if isinstance(m, dict) and m.get("role") == "user":
                c = m.get("content", "")
                if isinstance(c, list):
                    tem_imagem = any(isinstance(p, dict) and p.get("type") == "image_url" for p in c)
                texto_ultima = iald_motores.texto_de(c)
                break
        ultima = texto_ultima.lower()
        instrucao = "" if registro.get("sacred_language") else INSTRUCAO_LINGUAGEM_TECNICA
        if routing_instruction and task_scope is None: instrucao += '\n'+routing_instruction
        # 15/09/2026: a própria IALD avisa o OPERADOR quando o crédito da OpenAI está crítico
        # (21/09/2026: só no motor openai — o aviso é do crédito da OpenAI e fica fora do claude)
        # ⚠ AO LADO (22/09/2026): agora são os dois créditos, cada um nomeado no texto do aviso
        # (ordem do operador: "saber o que tenho de crédito em cada operadora") — vale nos dois motores
        alerta_saldo = _alerta_saldo_operador(registro, mensagens, user)
        if alerta_saldo:
            instrucao = (instrucao + "\n\n" if instrucao else "") + alerta_saldo

        permitidas = (_haiku_tool_definitions() if haiku
                      else _ferramentas_externas(cfg, limites, superficie, gratuito) + app_memory.tool_definitions())
        if haiku:
            permitidas += [t for t in _ferramentas_para('app') if t['function']['name'] in ('search_web','fetch_url','get_current_datetime','iald_public_search')]
        if task_scope:
            permitidas += task_scope.tools
            instrucao += "\n"+task_policy.INSTRUCTIONS+'\n'+getattr(task_scope,'instructions','')
        usar_agente = bool(permitidas) and (task_scope is not None or haiku or cfg.memoria_modo != "prompt" or
                         (not tem_imagem and _precisa_ferramentas(ultima)))
        # 14/09/2026 23:02 (Claude, reverificação final, item 5): com ferramentas, a 2ª volta também
        # precisa caber no saldo — senão a 1ª é cobrada e a pessoa fica sem resposta (medido: 4.681
        # tokens levaram o dia a 63% sem nada). Estimativa conservadora pela CPT do texto do cliente
        # (a janela e o saldo cortam depois, então ela só sobra): se duas voltas não cabem, responde
        # direto, sem ferramentas.
        if gratuito and not haiku and usar_agente and saldo_inicial is not None:
            texto_cliente = sum(len(iald_motores.texto_de(m.get("content"))) for m in mensagens
                                if isinstance(m, dict) and m.get("role") in ("user", "assistant"))
            entrada_aprox = int(texto_cliente / iald_motores.CPT) + 1500      # + ferramentas e nota
            duas_voltas = (2 * entrada_aprox + int(GRATUITO_MAX_CHARS_FERRAMENTA / iald_motores.CPT)
                           + 2 * iald_motores.SALDO_MINIMO_TOKENS)
            if duas_voltas > saldo_inicial:
                usar_agente = False
                print(f"[motores] {user}: saldo gratuito não cobre duas voltas; resposta sem ferramentas",
                      flush=True)
        nomes = [t["function"]["name"] for t in permitidas] if usar_agente else []
        # A saída máxima do plano vale no modo rápido. No pensar ela cresce na MESMA proporção
        # que IALD_OPENAI_MAX_SAIDA_PENSAR guarda sobre IALD_OPENAI_MAX_SAIDA (padrão 2×): o
        # raciocínio come a saída, e o assinante não pode perder o teto de pensar que já tinha.
        if modo == "think":
            proporcao = max(cfg.max_saida_pensar / max(cfg.max_saida, 1), 1.0)
            teto_saida = min(cfg.max_saida_pensar, int(limites["max_saida"] * proporcao))
        else:
            teto_saida = min(cfg.max_saida, limites["max_saida"])
        if claude:
            # 21/09/2026: no claude o pensamento adaptativo gasta o MESMO max_tokens da resposta; com o
            # teto do plano (4.096–8.192) a resposta pararia em "length". Vale IALD_CLAUDE_MAX_SAIDA.
            teto_saida = cfg.max_saida
        try:
            if haiku:
                haiku_package = CLAUDE_ROUTES.package()
                haiku_snapshot = _haiku_snapshot(haiku_package)
                haiku_adapter = _CheckedHaikuAdapter(iald_motor_claude, haiku_snapshot, trusted_openai_tools=permitidas)
                prompt_externo = haiku_package.prefix
                memoria_info = {"context_sha256": haiku_package.measurement.prefix_sha256, "scope": "HAIKU_MEASURED_PUBLIC"}
                cfg.janela = _HAIKU_PROFILE.window
            else:
                prompt_externo, memoria_info = _contexto_externo(public=gratuito)
            if gratuito and memoria_info.get('scope') == 'PUBLIC_FIXED_SOURCES':
                # The shared fixed knowledge must not consume the 32k conversation window.
                # Spending, user quotas, moderation, tools and native-access rules still apply.
                prefix_tokens = max(iald_motores.estimar_tokens(prompt_externo),
                    iald_memoria_canonica.payload_tokens({'messages': [
                        {'role': 'developer', 'content': prompt_externo}]}))
                cfg.janela = min(MOTORES_CFG.janela, prefix_tokens + iald_motores.JANELA_GRATUITO)
            # 21/09/2026: o claude recebe as MESMAS mensagens (o prefixo abre a mensagem developer, intacto);
            # a nota de serviço — parte variável, fora do cache — diz que quem responde é o Claude
            if haiku:
                para_openai, info = _assemble_haiku_messages(
                    iald_motores, mensagens, prompt_externo, modelo, nomes, instrucao)
            else:
                para_openai, info = iald_motores.montar_mensagens(
                    mensagens, prompt_externo, modelo, nomes, cfg.janela, teto_saida, instrucao,
                    provedor=iald_motores.PROVEDORES[motor])
        except ValueError as exc:
            return _sse_aviso(f"Pedido inválido para o motor externo: {exc}.", "pedido_invalido")
        if claude and iald_motor_claude.MARCA_ATLAS_INTEGRAL in prompt_externo:
            # 21/09/2026 (revisão de segurança): defesa em profundidade — qualquer que seja o modo, o
            # prefixo com o Atlas integral não sai para a Anthropic (o envio também confere)
            print(f"[claude] {user}: o prefixo leva o Atlas integral; nada enviado à Anthropic", flush=True)
            return _sse_aviso(MSG_CLAUDE_ATLAS_INTEGRAL, "motor_indisponivel")
        para_openai = app_memory.project_messages(para_openai)
        try:
            pedido_saida = int(req_json.get("max_tokens") or 0) or teto_saida
        except (TypeError, ValueError):
            pedido_saida = teto_saida

        base = iald_motores.montar_payload(
            cfg, modelo, para_openai, modo, min(pedido_saida, teto_saida),
            identificador=iald_motores.identificador_seguro(
                user, app.secret_key, "iald-anthropic-v1:" if claude else "iald-openai-v1:"),
            chave_cache="iald-" + memoria_info["context_sha256"][:16])
        if claude:
            base["max_completion_tokens"] = cfg.max_saida       # antes da reserva (ver teto_saida acima)

        native_count_cache = {}
        estado_claude = iald_motor_claude.EstadoClaude() if claude else None
        def count_haiku_wire(wire):
            identity = hashlib.sha256(json.dumps(wire, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
            if identity not in native_count_cache:
                try:
                    client = iald_motor_claude.cliente_para(cfg).with_options(max_retries=0)
                    native_count_cache[identity] = _count_haiku_native_request(client, wire)
                except Exception as exc:
                    raise iald_memoria_canonica.MemoryUnavailable("Contagem de contexto Haiku indisponível; nenhuma geração iniciada.") from exc
            return native_count_cache[identity]

        def tokens_para_saldo(payload):
            if not haiku:
                return _tokens_do_payload_para_saldo(payload)
            payload = _haiku_attach_tools(payload, permitidas)
            wire = haiku_adapter.converter_pedido(cfg, payload, prefixo=prompt_externo, estado=estado_claude, bind_context=False)
            wire.update(_haiku_reasoning(modelo, wire["max_tokens"], effort=cfg.esforco_claude))
            return count_haiku_wire(wire)

        def prefixo_da_cota(msgs):
            """O prefixo fixo que a cota da pessoa não paga, em tokens do PROVEDOR (× fator_tokens no
            claude: o `usage` dele vem em tokens Claude). Na OpenAI, a estimativa de sempre."""
            if haiku:
                # Same measured minimal-request baseline used by the package;
                # extra profile/history/tools are counted in the full request.
                return haiku_package.measurement.permanent_tokens
            estimado = iald_motores.prefixo_tokens_estimado(msgs)
            return math.ceil(estimado * max(float(cfg.fator_tokens or 1.0), 1.0)) if claude else estimado
        prefixo = prefixo_da_cota(para_openai)

        descartadas_saldo = 0
        if gratuito and not wallet_runtime.enabled():
            # O histórico mais antigo sai até a entrada estimada caber no saldo (a janela já fez
            # o mesmo corte pelo tamanho). Sobrou só a última mensagem e ainda não cabe → limite.
            def entrada_estimada():
                amostra = dict(base, messages=para_openai)
                if usar_agente:
                    amostra["tools"] = permitidas
                return max(0, tokens_para_saldo(amostra) - prefixo)
            try:
                entrada = entrada_estimada()
                while not haiku and entrada + iald_motores.SALDO_MINIMO_TOKENS > saldo_inicial and len(para_openai) > 2:
                    para_openai.pop(1)
                    descartadas_saldo += 1
                    while len(para_openai) > 2 and para_openai[1].get("role") != "user":
                        para_openai.pop(1)          # a conversa não começa pela resposta da IALD
                        descartadas_saldo += 1
                    entrada = entrada_estimada()
            except iald_memoria_canonica.MemoryUnavailable as exc:
                return _sse_aviso(f"Pedido inválido para o motor externo: {exc}.", "pedido_invalido")
            if entrada + iald_motores.SALDO_MINIMO_TOKENS > saldo_inicial:
                return _aviso_limite(iald_motores.MSG_SALDO_MES if campo_saldo == "tokens_mes"
                                     else iald_motores.MSG_SALDO_DIA, campo_saldo, user, registro, motor)
            base["messages"] = para_openai
            base["max_completion_tokens"] = max(iald_motores.SALDO_MINIMO_TOKENS,
                                                min(base["max_completion_tokens"], saldo_inicial - entrada))

        # MODERAÇÃO de todo o texto do cliente que vai nesta chamada (MÉDIO 1): o perfil e cada
        # mensagem mantida (usuário e assistente — o histórico vem do cliente e pode ser forjado).
        contexto_usuario, _lupa = iald_motores.extrair_do_cliente(mensagens)
        textos_cliente = ([contexto_usuario] if contexto_usuario else []) + [
            iald_motores.texto_de(m.get("content")) for m in para_openai[1:]]
        if gratuito and sum(len(t) for t in textos_cliente) > iald_motores.TETO_TOTAL_TEXTO_GRATUITO:
            return _sse_aviso(MSG_TEXTO_LONGO, "pedido_invalido", {"motivo": "texto_longo"})
        # 21/09/2026: a moderação é SEMPRE na chave da OpenAI (a Anthropic não tem endpoint de moderação)
        cfg_moderacao = MOTORES_CFG if claude else cfg
        if MODERACAO_LIGADA:
            moderacao = iald_motores.moderar_textos(textos_cliente, req_lib.post, cfg_moderacao.url_base,
                                                    cfg_moderacao.chave, cache=_CACHE_MODERACAO)
            categorias = ",".join(moderacao.get("categorias") or []) or "-"
            if moderacao.get("bloquear"):
                # (acolher vence bloquear DENTRO do mesmo bloco — ver iald_motores.moderar_textos)
                auth_log("MODERACAO_BLOQUEIO", user, f"categorias={categorias}")
                return _sse_aviso(iald_motores.MENSAGEM_MODERACAO_BLOQUEIO, "moderacao")
            if not moderacao.get("ok"):
                print(f"[moderacao] {user}: {moderacao.get('erro') or 'falhou'}; "
                      f"{'pedido recusado' if MODERACAO_FALHA == 'bloquear' else 'seguindo sem moderação'}",
                      flush=True)
                if MODERACAO_FALHA == "bloquear":
                    return _sse_aviso(MSG_MODERACAO_INDISPONIVEL, "moderacao_indisponivel")
            if moderacao.get("acolher"):
                # quem fala de se ferir recebe o CVV, não uma recusa seca
                auth_log("MODERACAO_ACOLHIMENTO", user, f"categorias={categorias}")
                para_openai[0] = dict(para_openai[0], content=para_openai[0]["content"] + "\n\n"
                                      + iald_motores.INSTRUCAO_ACOLHIMENTO)
                base["messages"] = para_openai
                prefixo = prefixo_da_cota(para_openai)

        if gratuito:
            if not _SEMAFORO_GRATUITO.acquire(blocking=False):
                print(f"[motores] {user}: sem vaga no uso gratuito ({GRATUITO_STREAMS_SIMULTANEOS} streams)", flush=True)
                return _sse_aviso(MSG_OCUPADO, "ocupado")
            soltar.append(_Vaga(_SEMAFORO_GRATUITO).soltar)

        try:
            if haiku:
                conta = legado = _HaikuNativeAccount(motors=iald_motores, budget=iald_orcamento,
                    guard=_guarda_do_motor(motor), ledger=razao, cfg=cfg, user=user, admin=admin,
                    model=modelo, quota_key=chave_cota, plan=plano, prefix_tokens=prefixo,
                    count_request=tokens_para_saldo)
            else:
                legado = iald_motores.ContaDoPedido(
                    razao, user, modelo, cfg.precos(modelo), chave_cota=chave_cota, plano=plano,
                    prefixo_tokens=prefixo,
                    # 21/09/2026 (revisão de custo): chamada sem usage no razão do claude × fator_tokens,
                    # como o guarda de reservas a liquida (1.0 na OpenAI: como antes)
                    fator_tokens=cfg.fator_tokens if claude else 1.0)
                conta = iald_orcamento.ReservedAccount(
                    _guarda_do_motor(motor), legado, cfg, user, admin, modelo, quota_key=chave_cota,
                    group=plano, group_limit=cfg.cota_global_gratuito_usd if gratuito else None)
        except Exception:
            return _aviso_limite(MSG_RESERVA_INDISPONIVEL, "razao", user, registro, motor)
        if gratuito and not wallet_runtime.enabled():
            conta = iald_motores.ContaComSaldo(conta, iald_motores.SaldoDoPedido(
                cfg, razao, user, plano, chave_cota, legado, prefixo,
                tokens_para_saldo))
        haiku_context_notices = []
        enviar = None
        if claude:
            # 21/09/2026: quem fala com a API é o SDK da Anthropic, por iald_motor_claude — a chave vai
            # por ele, NUNCA num cabeçalho montado aqui. `prefixo` = o texto EXATO que abre a mensagem
            # developer (o mesmo que a OpenAI recebe): vira o bloco de sistema com cache_control.
            # Um EstadoClaude por pedido: o pensamento assinado de cada volta com ferramenta volta intacto.
            url, cabecalhos = "https://api.anthropic.com/v1/messages", {}
            def enviar(payload, timeout=None):
                if haiku:
                    payload = _haiku_attach_tools(payload, permitidas)
                    # The agent has now set its final tool_choice. Count/reserve
                    # this exact payload before the sole provider send.
                    from claude_tool_budget import fit_latest_tool_results, ToolResultsDoNotFit
                    try:
                        before_fit = payload
                        payload = fit_latest_tool_results(payload, tokens_para_saldo, cfg.janela)
                        if payload["messages"] != before_fit["messages"]:
                            haiku_context_notices.append({"fase": "respondendo", "rotulo":
                                "Resultados em excertos parciais; respondendo com as evidências que cabem."})
                    except ToolResultsDoNotFit as exc:
                        raise iald_orcamento.WindowError(str(exc)) from exc
                    conta.iniciar_chamada(payload)
                    _check_reserved_dispatch(dispatch_check,conta)
                    response, decision = post_guarded(haiku_adapter, cfg, payload,
                        requested_model=modelo, server_policy=_claude_policy(registro, user),
                        prefix=prompt_externo, memory=haiku_package.measurement,
                        state=estado_claude, timeout=timeout, counter=count_haiku_wire)
                    return response
                return app_memory.http_call('model.claude', iald_motor_claude.post_como_openai, cfg, payload, prefixo=prompt_externo,
                                                          estado=estado_claude, timeout=timeout)
        else:
            url = cfg.url_base + "/chat/completions"
            cabecalhos = {"Authorization": f"Bearer {cfg.chave}", "Content-Type": "application/json"}
        log_request(user, "/v1/chat/completions", "POST", tokens_in=info["tokens_estimados"],
                    status=f"{motor}_agente" if usar_agente else f"{motor}_stream")
        if info["descartadas"]:
            print(f"[motores] {user}: {info['descartadas']} mensagem(ns) antiga(s) fora da janela de "
                  f"{cfg.janela} tokens", flush=True)
        if descartadas_saldo:
            print(f"[motores] {user}: {descartadas_saldo} mensagem(ns) antiga(s) fora do saldo de tokens "
                  f"do uso gratuito", flush=True)

        if usar_agente:
            exigir_consulta = cfg.memoria_modo != "prompt" and bool(re.search(
                r"\b(localiz\w*|procur\w*|busqu\w*|pesquis\w*|consult\w*|verifi\w*|confira|conferir|leia|ler)\b", ultima))
            adaptador = iald_motores.AdaptadorAgente(cfg, base, url, cabecalhos,
                                                   _DeferredHaikuAccount(conta) if haiku else conta,
                                                   exigir_consulta=exigir_consulta, enviar=enviar,
                                                   provedor=motor,
                                                   # 21/09/2026 (revisão): JSON inválido não roda
                                                   entrada_invalida=estado_claude.entrada_invalida if claude else None)
            adaptador.recovery_attempt = recovery_attempt
            if haiku:
                adaptador.context_notices = haiku_context_notices
            if claude:
                executor = _executar_ferramenta_claude
            elif gratuito:
                executor = _executar_ferramenta_gratuito
            else:
                executor = None

            if task_scope:
                original_executor=executor or execute_public_tool
                def task_executor(name,args,**kwargs):
                    if name in _task_scope_names(task_scope):return json.dumps(_execute_scope_tool(task_scope,name,args,user),ensure_ascii=False)
                    return original_executor(name,args,**kwargs)
                executor=task_executor

            def gerar():
                try:
                    yield from agent_loop(para_openai, user=user, max_tokens=base["max_completion_tokens"],
                                          ferramentas=permitidas, operator_authorized=False, motor=adaptador,
                                          max_voltas=GRATUITO_MAX_VOLTAS_AGENTE if gratuito else None,
                                          max_chars_canonico=GRATUITO_MAX_CHARS_FERRAMENTA if gratuito else None,
                                          executar=executor,
                                          responder_na_ultima=gratuito,
                                          verificar_payload=lambda _:_check_reserved_dispatch(dispatch_check,conta), task_control=task_scope.control if task_scope else None,
                                          task_tool_names=_task_scope_names(task_scope))
                except app_recovery.DefinitiveRefusal as exc:
                    conta.descartar_ultima_chamada()
                    exc.settled = True
                    raise
                except (iald_motores.CotaEsgotada, iald_orcamento.BudgetError) as exc:
                    yield from _linhas_da_recusa(exc, user, registro, motor)
                except iald_memoria_canonica.MemoryUnavailable as exc:
                    yield from _sse_aviso(str(exc), "motor_indisponivel").response
                except Exception as exc:
                    print("[motores] falha do agente: " + iald_motores.mascarar(exc), flush=True)
                    yield from _sse_aviso("Falha no serviço externo; o registro de uso foi preservado.", "falha_motor").response
                finally:
                    conta.fechar()
        else:
            def gerar():
                try:
                    yield ": iald-motor-externo\n\n"
                    payload = base
                    for tentativa in (1, 2):
                        enviou = False
                        try:
                            if not haiku:
                                conta.iniciar_chamada(payload)
                            if enviar is not None:
                                fazer = lambda: enviar(payload, (10, cfg.timeout))          # noqa: E731
                            else:
                                fazer = lambda: app_memory.http_call('model._chat_externo', req_lib.post, url, json=payload, headers=cabecalhos,  # noqa: E731
                                                             stream=True, timeout=(10, cfg.timeout))
                            enviar_verificado = fazer
                            def fazer():
                                _check_reserved_dispatch(dispatch_check,conta)
                                return enviar_verificado()
                            for pedaco in iald_motores.transmitir(
                                    fazer,
                                    ao_uso=conta.uso, ao_texto=conta.texto, intervalo=AGENT_KEEPALIVE_SEC,
                                    avisos=claude, recovery=recovery_attempt):     # 21/09/2026 (revisão): o aviso da recusa passa
                                if pedaco.startswith("data: {"):
                                    enviou = True
                                yield pedaco
                            return
                        except app_recovery.DefinitiveRefusal as exc:
                            conta.descartar_ultima_chamada()
                            exc.settled = True
                            raise
                        except iald_motores.ErroProvedor as exc:
                            # 21/09/2026: no claude, recusa ANTES de gerar que certamente não foi cobrada
                            # libera a reserva. ⚠ CORREÇÃO AO LADO (revisão de custo/wire): era "status ≠
                            # 502" — agora a lista de iald_motor_claude.recusa_sem_cobranca (504 e a
                            # conexão caída depois de enviar ficam na reserva; a conexão que nem abriu, 503
                            # claude_conexao, sai). O erro no meio do stream chega como 502 e fica.
                            if claude:
                                sem_cobranca = iald_motor_claude.recusa_sem_cobranca(exc.status, exc.codigo)
                            else:
                                sem_cobranca = exc.status in (400, 401, 403, 404, 413, 422, 429)
                            if not enviou and sem_cobranca:
                                conta.descartar_ultima_chamada()
                            if (tentativa == 1 and not enviou and exc.recusou_esforco()
                                    and "reasoning_effort" in payload):
                                # o modelo não aceita esse nível: tira o parâmetro e tenta uma vez
                                cfg.marcar_esforco_recusado(modelo)
                                payload = {k: v for k, v in payload.items() if k != "reasoning_effort"}
                                print(f"[motores] {modelo} recusou reasoning_effort; seguindo sem ele", flush=True)
                                continue
                            print(f"[motores] {user}: {exc}", flush=True)
                            if not claude:
                                _marcar_sem_credito(exc)      # 15/09/2026: bandeira do saldo (só OpenAI)
                            else:
                                _marcar_sem_credito_claude(exc)   # 22/09/2026: crédito da Anthropic
                            texto = iald_motores.mensagem_ao_usuario(exc)
                        except (iald_motores.CotaEsgotada, iald_orcamento.BudgetError) as exc:
                            # 14/09/2026 (noite): recusa do controle de gasto é "limite" com a cota
                            # (antes saía como falha_motor, sem bloqueado_por)
                            yield from _linhas_da_recusa(exc, user, registro, motor)
                            return
                        except iald_memoria_canonica.MemoryUnavailable as exc:
                            texto = str(exc)
                        except Exception as exc:          # noqa: BLE001 — rede, timeout
                            print(f"[motores] {user}: falha de rede: {iald_motores.mascarar(exc)}", flush=True)
                            texto = iald_motores.mensagem_ao_usuario(exc)
                        yield "data: " + json.dumps({"iald_aviso": {"tipo": "falha_motor", "texto": texto}},
                                                    ensure_ascii=False) + "\n\n"
                        yield "data: " + json.dumps({"choices": [{"delta": {"content": texto},
                                                                  "finish_reason": "stop"}]},
                                                    ensure_ascii=False) + "\n\n"
                        yield "data: [DONE]\n\n"
                        return
                finally:
                    conta.fechar()

        def com_soltura(fluxo):
            try:
                yield from fluxo
            finally:
                for fn in soltar:
                    fn()

        fluxo = gerar()
        if gratuito and MODERACAO_LIGADA:
            fluxo = _moderar_resposta_sse(fluxo, user, cfg_moderacao, authorize=dispatch_check)
        fluxo = com_soltura(fluxo)
        if not gratuito:
            # 14/09/2026 (noite): conta gratuita não gera crédito de uso TGL — a medição criaria a
            # conta no razão com o crédito inicial de 1.000 (ensure_account) na primeira resposta,
            # desfazendo "sem crédito TGL no gratuito" [INPUT: a ratificar]
            # 21/09/2026: a origem da medição é o motor ("openai" | "claude")
            fluxo = _medir_saida_sse(fluxo, user, motor)
        resposta = Response(fluxo, status=200, content_type="text/event-stream",
                            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
        if user == 'luiz':
            resposta.response = APP_EVALUATION.observe(resposta.response,
                {'motor': motor, 'id': modelo}, rates=cfg.precos(modelo),
                memory_sha256=memoria_info.get('context_sha256'),messages=req_json.get('messages'))
            resposta._iald_evaluation_observed = True
        resposta = _identificar_resposta(resposta, {"motor": motor, "id": modelo,
                                    "rotulo": iald_motores.rotulo_do_modelo(modelo)})
        for fn in soltar:
            resposta.call_on_close(fn)
        entregue = True
        return resposta
    finally:
        if not entregue:
            for fn in soltar:
                fn()


def _check_reserved_dispatch(check,account):
    try:check()
    except Exception:
        # This check is strictly before the transport. Never use it to erase
        # a hold after a request has started or an upstream result is uncertain.
        account.descartar_ultima_chamada()
        raise


def _dispatch_guard(user,executor,automatic):
    def check():
        current=load_users_estrito().get(user,{})
        if not app_router.allowed(current,user):raise PermissionError('Account access revoked')
        if automatic and not iald_motores.consentiu(current,app_router.AUTO):
            raise PermissionError('Automatic consent revoked')
        provider='claude' if executor.startswith('claude-') else executor
        if provider=='nativa':
            if MODERACAO_LIGADA and not iald_motores.consentiu(current,'openai'):
                raise PermissionError('Moderation consent missing')
        elif not iald_motores.consentiu(current,provider):raise PermissionError('Executor consent revoked')
        if provider in app_providers.MODELS and not app_providers.allowed(current,user,provider):
            raise PermissionError('Executor access revoked')
        if executor=='claude-sonnet' and user!='luiz':raise PermissionError('Operator only')
        return current
    return check


def _identificar_resposta(resposta, modelo):
    """Attach server provenance; forward the original SSE bytes and close it on cancel."""
    if resposta.status_code != 200:
        return resposta
    if resposta.mimetype == "text/event-stream":
        if session.get('username') == 'luiz' and not getattr(resposta, '_iald_evaluation_observed', False):
            resposta.response = APP_EVALUATION.observe(resposta.response, modelo, messages=(request.get_json(silent=True) or {}).get('messages'))
        original = resposta.response
        def identified():
            try:
                first = True
                for chunk in original:
                    if first:
                        first = False
                        prefix = "data: " + json.dumps({"iald_modelo": modelo}, ensure_ascii=False) + "\n\n"
                        # Add provenance to the first existing chunk, never advance the
                        # response lifecycle with an extra yield before upstream starts.
                        yield prefix.encode("utf-8") + chunk if isinstance(chunk, bytes) else prefix + chunk
                    else:
                        yield chunk
            finally:
                close = getattr(original, "close", None)
                if close:
                    close()
        resposta.response = identified()
    elif resposta.is_json:
        data = resposta.get_json()
        if isinstance(data, dict) and data.get("choices"):
            data["iald_modelo"] = modelo
            resposta.set_data(json.dumps(data, ensure_ascii=False))
    return resposta


def _medir_saida_sse(fluxo, user, origem):
    """
    Observador PASSIVO de um fluxo SSE.

    Regra inegociável: o pedaço é repassado INTACTO e ANTES de qualquer conta.
    A medição vive dentro de try/except mudo — um erro de contagem não pode
    engolir um token da resposta nem derrubar o stream. O `finally` garante a
    contabilização mesmo quando o cliente desliga no meio (GeneratorExit).
    """
    # Sem dono não há o que creditar: sai do caminho e vira um repasse puro.
    # (A guarda também existe em _contabilizar_uso; aqui ela evita contar à toa
    # e torna o contrato do observador explícito em vez de herdado.)
    if not user or user == "?":
        yield from fluxo
        return

    chars = 0
    usage_real = {}
    bufer = ""
    try:
        for pedaco in fluxo:
            yield pedaco                      # ← primeiro entrega, depois mede
            try:
                if isinstance(pedaco, (bytes, bytearray)):
                    texto = pedaco.decode("utf-8", "replace")
                else:
                    texto = str(pedaco)
                bufer += texto
                linhas = bufer.split("\n")
                bufer = linhas.pop()
                for ln in linhas:
                    ln = ln.strip()
                    if not ln.startswith("data: "):
                        continue              # ":" = keepalive
                    corpo = ln[6:].strip()
                    if not corpo or corpo == "[DONE]":
                        continue
                    ck = json.loads(corpo)
                    u = ck.get("usage")
                    if isinstance(u, dict) and u.get("completion_tokens"):
                        usage_real = u
                    escolhas = ck.get("choices") or []
                    if escolhas:
                        delta = escolhas[0].get("delta") or {}
                        chars += len(delta.get("content") or "")
                        chars += len(delta.get("reasoning_content") or "")
            except Exception:
                pass                          # medir jamais interrompe o stream
    finally:
        try:
            if usage_real.get("completion_tokens"):
                tokens = int(usage_real["completion_tokens"])      # exato
            elif chars:
                tokens = int(chars / HolographicMemory.CPT)        # estimado
            else:
                tokens = 0
            if tokens > 0:
                _contabilizar_uso(user, tokens, origem)
        except Exception:
            pass
