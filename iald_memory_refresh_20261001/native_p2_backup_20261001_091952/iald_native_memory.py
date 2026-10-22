"""Small native context from the same verified public release as external motors."""
import json
import re

from iald_core_indexado import DocumentCorpus
from iald_estado_publicado import published_evidence
from iald_release_binding import load_release
from iald_response_contract import deployment_contract, IDENTITY_PROTOCOL, SOLUTION_PROTOCOL


class NativeContextError(ValueError):
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


def check_text_window(payload, window):
    """Conservative text admission, NOT a Qwen tokenizer or a vision measurement.

    One token per UTF-8 byte plus framing/output reserve deliberately rejects
    some requests that might fit. Media are left to llama-server's existing
    multimodal admission; their token cost cannot be inferred from JSON bytes.
    """
    output = payload.get('max_tokens', 4096)
    if type(output) is not int or output <= 0 or output >= window:
        raise NativeContextError('Reserva de saída nativa inválida para esta janela.')
    messages = []
    has_media = False
    for message in payload.get('messages', []):
        copied = dict(message)
        if isinstance(copied.get('content'), list):
            has_media |= any(p.get('type') != 'text' for p in copied['content'] if isinstance(p, dict))
            copied['content'] = [p for p in copied['content'] if isinstance(p, dict) and p.get('type') == 'text']
        messages.append(copied)
    counted = {'messages': messages, 'tools': payload.get('tools', [])}
    text_bytes = len(json.dumps(counted, ensure_ascii=False, allow_nan=False).encode('utf-8'))
    # Template overhead is an explicit conservative allowance, not a native count.
    framing = 2048 + 32 * len(messages)
    if text_bytes + output + framing > window:
        raise NativeContextError('Contexto textual nativo excede a janela conservadora; reduza o histórico ou a saída.')
    return {'configured_window': window, 'text_bytes': text_bytes,
            'output_reserve': output, 'framing_allowance': framing,
            'measurement': 'CONSERVATIVE_UTF8_BYTES_NOT_NATIVE_TOKENS',
            'media_tokens_measured': not has_media}


def startup_summary(manifest, catalog):
    release = load_release(manifest, source_sha=catalog.source_sha)
    status = catalog.status()
    count = status['lean_files']
    if type(count) is not int or count < 0 or status['source_sha256'] != release.identity['source_sha256']:
        raise ValueError('Invalid canonical catalog status')
    return (f"[IALD-CANONICAL-CATALOG] release={release.identity['release']} "
            f"source_sha256={catalog.source_sha[:16]} lean_files={count}")
