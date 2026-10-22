"""Patch only a prepared copy: native context, measured tools and final reservation."""
import ast


def patch_server(source):
    def change(old, new):
        nonlocal source
        assert source.count(old) == 1, (old[:90], source.count(old))
        source = source.replace(old, new, 1)

    def function(name, code):
        nonlocal source
        nodes = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name]
        assert len(nodes) == 1, name
        node = nodes[0]
        lines = source.splitlines(keepends=True)
        source = ''.join(lines[:node.lineno - 1]) + code.strip() + '\n' + ''.join(lines[node.end_lineno:])

    change('from claude_native_account import NativeAccount as _HaikuNativeAccount', '''from claude_native_account import NativeAccount as _HaikuNativeAccount, DeferredStartAccount as _DeferredHaikuAccount
from claude_context_snapshot import (load_snapshot as _load_haiku_snapshot,
    MeasuredSnapshot as _HaikuSnapshot, context_metadata as _haiku_metadata,
    CheckedAdapter as _CheckedHaikuAdapter, attach_openai_tools as _haiku_attach_tools,
    verify_native_tools as _verify_haiku_tools)

def _haiku_tool_definitions():
    return (iald_kernel.tool_definitions() + iald_fontes_publicas.tool_definitions()
            + iald_core_indexado.tool_definitions())

def _haiku_client_ready():
    # Compatibility marker only: it never grants account/model authorization.
    return request.headers.get("X-IALD-Context") == "anthropic-native-v1"

def _haiku_snapshot(package):
    # All package fields were cross-checked against the manifest by the loader.
    return _HaikuSnapshot(_HAIKU_PROFILE.model, package.measurement.prefix_sha256,
        package.measurement.permanent_tokens,
        _HAIKU_PROFILE.window - package.available_dynamic_tokens - package.reserved_output_tokens - 1024,
        package.reserved_output_tokens, 1024, package.available_dynamic_tokens,
        package.tools_sha256, "")

def _haiku_selected(record, username):
    record = record or {}
    if record.get("motor") != iald_motores.CLAUDE:
        return False
    model = record.get("modelo_claude")
    return model == _HAIKU_PROFILE.model or (not model and str(username).strip().lower() != "luiz")''')
    function('_load_haiku_package', '''
def _load_haiku_package():
    from copy import copy
    package, snapshot = _load_haiku_snapshot(
        os.path.join(SERVE_DIR, ".iald_runtime", "haiku"), load_package)
    cfg = copy(CLAUDE_CFG)
    cfg.modelo = cfg.modelo_operador = _HAIKU_PROFILE.model
    cfg.max_saida = 4096
    payload = _haiku_attach_tools({"model": cfg.modelo, "max_completion_tokens": 4096,
        "messages": [{"role": "system", "content": package.prefix}, {"role": "user", "content": "."}],
        "tool_choice": "none"}, _haiku_tool_definitions())
    wire = iald_motor_claude.converter_pedido(cfg, payload, prefixo=package.prefix)
    _verify_haiku_tools(wire, snapshot)
    return package
''')
    change('''    except (ValueError, PermissionError, OSError):
        return "claude"
''', '''    except (ValueError, PermissionError, OSError):
        return "claude-haiku" if _haiku_selected(registro, username) else "claude-sonnet"
''')
    change('resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"',
           'resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-IALD-Context"')
    change('''    opcoes.extend(CLAUDE_ROUTES.options(registro, usuario))''',
           '''    opcoes.extend(row for row in CLAUDE_ROUTES.options(registro, usuario)
                  if row["id"] != "claude-haiku" or _haiku_client_ready())''')
    change('''                # Validate the selected profile, including its configured price.
                CLAUDE_ROUTES.configuration(dict(conta, **fields), username)''',
           '''                # Validate the selected profile, including its configured price.
                CLAUDE_ROUTES.configuration(dict(conta, **fields), username)
                if fields.get("modelo_claude") == _HAIKU_PROFILE.model and not _haiku_client_ready():
                    return jsonify({"error": "Atualize o aplicativo para usar o Haiku com memória integral."}), 426''')
    change('''    haiku = claude and cfg.modelo == _HAIKU_PROFILE.model
    if claude:''', '''    haiku = claude and cfg.modelo == _HAIKU_PROFILE.model
    if haiku and not _haiku_client_ready():
        return _sse_aviso("Atualize o aplicativo para usar o Haiku com memória integral.", "recurso_indisponivel")
    if claude:''')
    # The exact public schemas stay present in every turn, including the final no-tool turn.
    change('''        permitidas = ((iald_kernel.tool_definitions() + iald_fontes_publicas.tool_definitions()
                       + iald_core_indexado.tool_definitions()) if haiku''',
           '''        permitidas = (_haiku_tool_definitions() if haiku''')
    change('''        usar_agente = bool(permitidas) and (cfg.memoria_modo != "prompt" or
                         (not tem_imagem and _precisa_ferramentas(ultima)))''',
           '''        usar_agente = bool(permitidas) and (haiku or cfg.memoria_modo != "prompt" or
                         (not tem_imagem and _precisa_ferramentas(ultima)))''')
    change('if gratuito and usar_agente and saldo_inicial is not None:',
           'if gratuito and not haiku and usar_agente and saldo_inicial is not None:')
    change('''                haiku_package = CLAUDE_ROUTES.package()
                prompt_externo''', '''                haiku_package = CLAUDE_ROUTES.package()
                haiku_snapshot = _haiku_snapshot(haiku_package)
                haiku_adapter = _CheckedHaikuAdapter(iald_motor_claude, haiku_snapshot)
                prompt_externo''')
    change('''            wire = iald_motor_claude.converter_pedido(cfg, payload, prefixo=prompt_externo, estado=estado_claude)''',
           '''            payload = _haiku_attach_tools(payload, permitidas)
            wire = haiku_adapter.converter_pedido(cfg, payload, prefixo=prompt_externo, estado=estado_claude)''')
    change('''                if haiku:
                    response, decision = post_guarded(iald_motor_claude, cfg, payload,''',
           '''                if haiku:
                    payload = _haiku_attach_tools(payload, permitidas)
                    # The agent has now set its final tool_choice. Count/reserve
                    # this exact payload before the sole provider send.
                    conta.iniciar_chamada(payload)
                    response, decision = post_guarded(haiku_adapter, cfg, payload,''')
    change('''            adaptador = iald_motores.AdaptadorAgente(cfg, base, url, cabecalhos, conta,''',
           '''            adaptador = iald_motores.AdaptadorAgente(cfg, base, url, cabecalhos,
                                                   _DeferredHaikuAccount(conta) if haiku else conta,''')
    change('''                            conta.iniciar_chamada(payload)
                            if enviar is not None:''',
           '''                            if not haiku:
                                conta.iniciar_chamada(payload)
                            if enviar is not None:''')
    # Internal provider billing notices must never be injected into app conversations.
    function('_alerta_saldo_operador', '''
def _alerta_saldo_operador(registro, mensagens, usuario, saldos=None):
    """Operational credit alerts belong only to the protected admin panel."""
    return None
''')
    change('''    if motor_ctx in iald_motores.EXTERNOS:
        # 21/09/2026: a janela''', '''    if _haiku_selected(registro_ctx, session.get("username", "")):
        if not _haiku_client_ready():
            return jsonify({"error": "Atualize o aplicativo para usar o Haiku com memória integral.",
                            "code": "client_context_update_required"}), 426
        try:
            CLAUDE_ROUTES.configuration(registro_ctx, session.get("username", ""))
            data = _haiku_metadata(_haiku_snapshot(CLAUDE_ROUTES.package()))
            return jsonify(data), 200
        except (ValueError, OSError, KeyError, TypeError, AttributeError):
            return jsonify({"modelo": _HAIKU_PROFILE.model, "disponivel": False,
                "contagem_nativa_por_pedido_obrigatoria": True,
                "error": "Memória ou ferramentas do Haiku indisponíveis.",
                "code": "haiku_package_unavailable"}), 503
    if motor_ctx in iald_motores.EXTERNOS:
        # 21/09/2026: a janela''')
    change('''    superficie = "app" if session.get("app_surface") else "web"
    if motor == iald_motores.CLAUDE:''', '''    if motor == iald_motores.CLAUDE and cfg.modelo == _HAIKU_PROFILE.model:
        try:
            data = _haiku_metadata(_haiku_snapshot(CLAUDE_ROUTES.package()))
            data.update(agente=True, pensar=False, max_saida=cfg.max_saida, imagens=imagens,
                        ferramentas=[t["function"]["name"] for t in _haiku_tool_definitions()])
            return data
        except (ValueError, OSError, KeyError, TypeError, AttributeError):
            return {"agente": False, "pensar": False, "ferramentas": [], "max_saida": 0,
                    "janela": 0, "imagens": imagens, "erro": "Memória ou ferramentas Haiku indisponíveis."}
    superficie = "app" if session.get("app_surface") else "web"
    if motor == iald_motores.CLAUDE:''')
    # A malformed manifest must remain an explicit unavailable state, not HTTP500.
    source = source.replace('except (ValueError, PermissionError, OSError):',
                            'except (ValueError, PermissionError, OSError, KeyError):')
    source = source.replace('except (PermissionError, ValueError, OSError):',
                            'except (PermissionError, ValueError, OSError, KeyError):')
    change('''                        "consentimentos": _consentimentos_registrados(registro)})
    modelo = iald_motores.modelo_para(registro, cfg)''',
           '''                        "consentimentos": _consentimentos_registrados(registro)}), (503 if _haiku_selected(registro, username) else 200)
    modelo = iald_motores.modelo_para(registro, cfg)''')
    # The normal Haiku branch can only be reached after loader/schema validation.
    ast.parse(source)
    return source


def patch_client(source):
    def change(old, new):
        nonlocal source
        assert source.count(old) == 1, (old[:90], source.count(old))
        source = source.replace(old, new, 1)

    change('''  o.headers = Object.assign({}, o.headers || {});
  const t = tokenApp();''', '''  o.headers = Object.assign({}, o.headers || {});
  o.headers['X-IALD-Context'] = 'anthropic-native-v1';
  const t = tokenApp();''')
    start = source.index('async function carregarContexto() {')
    end = source.index('\nfunction estimarTokens(', start)
    source = source[:start] + '''let contextoRequest = 0;
let motorRequest = 0;
function contextoNativo() {
  if (S.ctx.contagem_nativa_por_pedido_obrigatoria === true) return true;
  if (S.motor) return S.motor.motor_selecao === 'claude-haiku'
    || S.motor.modelo === 'claude-haiku-4-5-20251001';
  return S.ctx.contagem_nativa_por_pedido_obrigatoria === true;
}

async function carregarContexto() {
  const ticket = ++contextoRequest;
  try {
    const r = await fetchIALD('/api/contexto');
    if (ticket !== contextoRequest) return;
    if (!r.ok) throw new Error('context unavailable');
    const d = await r.json();
    if (ticket !== contextoRequest) return;
    S.ctx = { n_ctx: 32768, margem: 0.92, reserva_resposta: 8192,
      cpt: 2.91, teto_mensagens: 400, ...d, carregado: true };
  } catch (e) {
    if (ticket !== contextoRequest) return;
    S.ctx = { ...S.ctx, carregado: false };
  }
  atualizarDica();
}
''' + source[end:]
    change('''function estimarTokens(c) {
  if (c == null)''', '''function estimarTokens(c) {
  if (contextoNativo()) return null;
  if (c == null)''')
    change('''function orcamento(sys) {
  const util''', '''function orcamento(sys) {
  if (contextoNativo()) return null;
  const util''')
    change('''  if (!msgs || !msgs.length) return [];
  const orc = orcamento(sys);''', '''  if (!msgs || !msgs.length) return [];
  // The server counts the actual Haiku request and rejects overflow visibly.
  if (contextoNativo()) return msgs.slice();
  const orc = orcamento(sys);''')
    change('''function atualizarDica() {
  const c = conversaAtiva();''', '''function atualizarDica() {
  if (contextoNativo()) {
    const label = $('#dica-janela');
    const meter = $('#medidor');
    const measured = S.ctx.carregado && S.ctx.contagem_nativa_por_pedido_obrigatoria === true
      && Number.isFinite(S.ctx.memoria_tokens_medidos) && S.ctx.n_ctx === 200000;
    label.textContent = measured
      ? `${num(S.ctx.memoria_tokens_medidos)} tokens · memória TGL`
      : 'Memória TGL · verificando disponibilidade';
    label.title = measured
      ? 'Memória fixa na janela de 200.000 tokens. A conversa completa é validada ao enviar.'
      : 'A disponibilidade do contexto será conferida no servidor antes da resposta.';
    meter.querySelector('i').style.width = measured
      ? Math.min(100, 100 * S.ctx.memoria_tokens_medidos / S.ctx.n_ctx) + '%' : '0%';
    meter.dataset.nivel = measured ? 'alto' : 'baixo';
    return;
  }
  const c = conversaAtiva();''')
    change('''async function lerMotor(opcoes) {
  try {''', '''async function lerMotor(opcoes) {
  const ticket = ++motorRequest;
  try {''')
    change('''    S.motor = await r.json();
  } catch (e) { return; }
  pintarMotor();''', '''    const next = await r.json();
    if (ticket !== motorRequest) return;
    const previous = S.motor && (S.motor.motor_selecao || S.motor.modelo || S.motor.motor);
    S.motor = next;
    const current = S.motor.motor_selecao || S.motor.modelo || S.motor.motor;
    if (previous !== current) {
      S.ctx = { n_ctx: 32768, margem: 0.92, reserva_resposta: 8192,
        cpt: 2.91, teto_mensagens: 400, carregado: false };
      await carregarContexto();
    }
  } catch (e) { return; }
  if (ticket !== motorRequest) return;
  pintarMotor();''')
    # HTTP503 retains options/consent for recovery, instead of preserving a stale selection.
    change('''    const r = await fetchIALD('/api/motor', { signal: AbortSignal.timeout(6000) });
    if (!r.ok) return;''', '''    const r = await fetchIALD('/api/motor', { signal: AbortSignal.timeout(6000) });
    if (ticket !== motorRequest || (!r.ok && r.status !== 503)) return;''')
    return source
