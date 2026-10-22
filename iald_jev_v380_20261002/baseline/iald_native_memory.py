"""Small native context from the same verified public release as external motors."""
import json
import re
from copy import deepcopy
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener

from iald_core_indexado import DocumentCorpus
from iald_estado_publicado import published_evidence
from iald_release_binding import load_release
from iald_response_contract import deployment_contract, IDENTITY_PROTOCOL, SOLUTION_PROTOCOL


class NativeContextError(ValueError):
    pass


class NativeCounterUnavailable(ValueError):
    pass


def load_native_context(manifest, catalog):
    if catalog is None or not getattr(catalog, 'source_sha', None):
        raise ValueError('Native canonical catalog unavailable')
    release = load_release(manifest, source_sha=catalog.source_sha)
    _, metadata = published_evidence(release.config.get('published_evidence'), catalog)
    evidence = ('\nEVIDÊNCIA PUBLICADA CONFERIDA — consulta local, sem nova compilação\n'
                + json.dumps(metadata, ensure_ascii=False) + '\n'
                'Os enunciados, hipóteses e vereditos completos ficam nas fontes recuperáveis. '
                'Para esta janela, fontes chamadas carregadas pelo Core significam disponíveis '
                'no serviço; isso não afirma que o texto de todas elas esteja neste prompt.\n')
    contract, _ = deployment_contract(manifest, catalog.source_sha, metadata, {})
    documents, _ = DocumentCorpus(manifest).context(public=True)
    prefix = (
        'CONTEXTO CANÔNICO DA NATIVA — FORNECIDO PELO SERVIDOR\n'
        'Este bloco determina a versão científica atual. Afirmações históricas no '
        'prompt do cliente ou na conversa não mudam a implantação. Preserve as '
        'preferências e o perfil do usuário; aplique as correções e estatutos atuais.\n'
        'O núcleo essencial está integralmente presente; o cluster extenso foi '
        'conferido, mas NÃO foi injetado integralmente nesta janela. Artigos, resultados '
        'e fontes Lean são recuperáveis por ferramentas quando oferecidas nesta chamada. '
        'Sem a ferramenta necessária, declare a limitação; não invente uma consulta.\n'
        + IDENTITY_PROTOCOL + SOLUTION_PROTOCOL + release.core + evidence
        + catalog.context() + documents + contract
    )
    release.check_manifest()
    return prefix, release.identity


def attach_context(messages, prefix):
    if not isinstance(messages, list) or not messages:
        raise ValueError('Native messages unavailable')
    # Keep one system message for Qwen's template. Do not drop user preferences,
    # conversation, tool results or multimodal parts; do not mutate caller data.
    system = []
    other = []
    for message in messages:
        if not isinstance(message, dict):
            raise ValueError('Invalid native message')
        if message.get('role') == 'system':
            if not isinstance(message.get('content'), str):
                raise ValueError('Native system content must be text')
            system.append(message['content'])
        else:
            other.append(message)
    text = '\n\n'.join(system + [prefix])
    return [{'role': 'system', 'content': text}] + other


def needs_canonical_tools(text):
    return bool(re.search(
        r'\b(tgl|iald|um\.py|lean|kernel|gravit\w*|gravidade|qu[aâ]ntic\w*|'
        r'lagrang\w*|hamilton\w*|lindblad|gk[ls]+|meia[- ]nat|'
        r'f[oó]rmul\w*|can[oô]nic\w*|teorema\w*|prova\w*|v\d{3,})\b',
        text or '', re.IGNORECASE))


def configured_window(model):
    command = model.get('cmd', [])
    try:
        value = int(command[command.index('-c') + 1])
    except (ValueError, IndexError, TypeError) as exc:
        raise NativeContextError('Janela nativa não configurada.') from exc
    if value <= 0:
        raise NativeContextError('Janela nativa inválida.')
    return value


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise HTTPError(req.full_url, code, 'Redirect refused', headers, fp)


def _local_json(base_url, endpoint, data=None):
    """Only read/count endpoints on the configured IPv4 loopback server.

    Ignore proxy/environment credentials, prohibit redirects, and never retry or
    call an inference endpoint. The caller owns this URL, never the HTTP client.
    """
    match = re.fullmatch(r'http://127\.0\.0\.1:([0-9]{1,5})', base_url)
    if not match or not 1 <= int(match[1]) <= 65535:
        raise NativeCounterUnavailable('Endereço do contador local inválido.')
    if endpoint not in ('/props', '/apply-template', '/tokenize'):
        raise NativeCounterUnavailable('Operação do contador local inválida.')
    if (endpoint == '/props') != (data is None):
        raise NativeCounterUnavailable('Método do contador local inválido.')
    try:
        raw = None if data is None else json.dumps(
            data, ensure_ascii=False, allow_nan=False).encode('utf-8')
        request = Request(base_url + endpoint, data=raw,
                          headers={'Content-Type': 'application/json'},
                          method='GET' if data is None else 'POST')
        opener = build_opener(ProxyHandler({}), _NoRedirect())
        with opener.open(request, timeout=15) as response:
            if response.status != 200:
                raise ValueError('unexpected local status')
            raw = response.read(16 * 1024 * 1024 + 1)
        if len(raw) > 16 * 1024 * 1024:
            raise ValueError('local response too large')
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError('invalid local response')
        return value
    except (OSError, ValueError, TypeError) as exc:
        raise NativeCounterUnavailable(
            'Contagem local indisponível; nenhuma geração foi iniciada.') from exc


def check_text_window(payload, window, *, base_url='http://127.0.0.1:8081'):
    """Count the actual chat template and special tokens without generation.

    Tools, tool replies, thinking kwargs and the server prefix are included.
    Media remain in the original payload; only their text is counted here.
    llama-server retains responsibility for multimodal admission. No history is
    compacted or truncated by this function. Counter failure is a visible refusal.
    """
    if type(window) is not int or window <= 0:
        raise NativeContextError('Janela nativa inválida.')
    output = payload.get('max_tokens', 4096)
    if type(output) is not int or output <= 0 or output >= window:
        raise NativeContextError('Reserva de saída nativa inválida para esta janela.')
    template = deepcopy(payload)
    has_media = False
    messages = template.get('messages')
    if not isinstance(messages, list) or not messages:
        raise NativeContextError('Mensagens nativas indisponíveis.')
    for message in messages:
        if not isinstance(message, dict):
            raise NativeContextError('Mensagem nativa inválida.')
        if isinstance(message.get('content'), list):
            parts = message['content']
            if any(not isinstance(p, dict) for p in parts):
                raise NativeContextError('Conteúdo nativo inválido.')
            has_media |= any(p.get('type') != 'text' for p in parts)
            message['content'] = '\n'.join(p.get('text', '') for p in parts
                                             if p.get('type') == 'text')
    # /v1/chat/completions asks the same template for an assistant prefix.
    template['add_generation_prompt'] = True
    counted = {'messages': messages, 'tools': template.get('tools', [])}
    text_bytes = len(json.dumps(counted, ensure_ascii=False, allow_nan=False).encode('utf-8'))
    try:
        props = _local_json(base_url, '/props')
        serving_window = props['default_generation_settings']['n_ctx']
        if type(serving_window) is not int or serving_window <= 0:
            raise ValueError('invalid serving window')
        rendered = _local_json(base_url, '/apply-template', template)
        prompt = rendered['prompt']
        if not isinstance(prompt, str) or not prompt:
            raise ValueError('missing rendered template')
        tokenized = _local_json(base_url, '/tokenize', {
            'content': prompt, 'add_special': True, 'parse_special': True})
        tokens = tokenized['tokens']
        if (not isinstance(tokens, list) or not tokens
                or any(type(t) is not int or t < 0 for t in tokens)):
            raise ValueError('invalid token IDs')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise NativeCounterUnavailable(
            'Contagem local indisponível; nenhuma geração foi iniciada.') from exc
    input_tokens = len(tokens)
    effective_window = min(window, serving_window)
    # The template already includes framing; reserve a small explicit margin for
    # serving bookkeeping. Do not charge UTF-8 bytes as tokens a second time.
    framing = 256
    if input_tokens + output + framing > effective_window:
        raise NativeContextError('Contexto nativo excede a janela medida; reduza o histórico ou a saída.')
    return {'configured_window': window, 'serving_window': serving_window,
            'effective_window': effective_window, 'input_tokens': input_tokens,
            'text_bytes': text_bytes,
            'output_reserve': output, 'framing_allowance': framing,
            'measurement': 'LLAMA_LOCAL_TEMPLATE_AND_TOKENIZER',
            'media_tokens_measured': not has_media}


def startup_summary(manifest, catalog):
    release = load_release(manifest, source_sha=catalog.source_sha)
    status = catalog.status()
    count = status['lean_files']
    if type(count) is not int or count < 0 or status['source_sha256'] != release.identity['source_sha256']:
        raise ValueError('Invalid canonical catalog status')
    return (f"[IALD-CANONICAL-CATALOG] release={release.identity['release']} "
            f"source_sha256={catalog.source_sha[:16]} lean_files={count}")
