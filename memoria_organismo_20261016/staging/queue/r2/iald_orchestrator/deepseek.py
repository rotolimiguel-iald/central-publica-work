"""Official DeepSeek V4.1 Flash: text-only, maximum reasoning, no retries."""
from decimal import Decimal
from pathlib import Path
import hashlib
import http.client
import json
import time
import urllib.error
import urllib.request
from .profiles import BASE
from .safe_files import save_json, utc_now
from .deepseek_secret_store import load_key, key_metadata

URL = 'https://api.deepseek.com/chat/completions'
MODEL = 'deepseek-flash'
DOCUMENTED_VERSION = 'DeepSeek-V4.1-Flash'
CONTEXT_WINDOW = 1048576
MAX_OUTPUT = 393216
MAX_INPUT_BYTES = CONTEXT_WINDOW - MAX_OUTPUT - 4096
MAX_RESPONSE_BYTES = 32_000_000
RECEIPT = BASE / 'validation/deepseek_connection.json'
AUTHORIZATION = BASE / 'state/deepseek_authorization.json'
PRICE_SOURCE = 'https://api-docs.deepseek.com/quick_start/pricing/'


def authorization():
    if not AUTHORIZATION.is_file():
        return {'enabled': False}
    data = json.loads(AUTHORIZATION.read_bytes())
    if (data.get('scope') != 'IALD_OPERATOR_AUTHORIZED_TASKS'
            or data.get('financial_cap_usd') is not None):
        return {'enabled': False}
    return data


def signature():
    return {'adapter_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'key': key_metadata(), 'model': MODEL, 'authorization': authorization()}


def connection_status():
    if not key_metadata()['stored']:
        return 'api_key_required'
    if authorization().get('enabled') is not True:
        return 'api_billing_not_enabled'
    if RECEIPT.is_file():
        data = json.loads(RECEIPT.read_bytes())
        if data.get('status') == 'validation_failed' and 'HTTP 402' in data.get('reason', ''):
            return 'api_balance_pending'
        if data.get('status') == 'ready' and data.get('signature') == signature():
            return 'ready'
    return 'installed_pending_auth_validation'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError('DeepSeek solicitou redirecionamento; credencial não encaminhada.')


def parse_response(data, max_output=MAX_OUTPUT):
    if not isinstance(data, dict) or data.get('model') != MODEL:
        raise RuntimeError('DeepSeek não confirmou o identificador do modelo solicitado.')
    choices = data.get('choices')
    if not isinstance(choices, list) or len(choices) != 1:
        raise RuntimeError('Resposta DeepSeek inválida.')
    choice = choices[0]
    message = choice.get('message', {})
    if (choice.get('finish_reason') != 'stop' or message.get('tool_calls')
            or message.get('function_call')):
        raise RuntimeError('DeepSeek não concluiu uma resposta textual; sem repetição automática.')
    content = message.get('content')
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError('DeepSeek devolveu resposta vazia.')
    usage = data.get('usage')
    if not isinstance(usage, dict):
        raise RuntimeError('DeepSeek não informou consumo; resultado não validado.')
    for key in ('prompt_tokens', 'completion_tokens', 'total_tokens',
                'prompt_cache_hit_tokens', 'prompt_cache_miss_tokens'):
        if type(usage.get(key)) is not int or usage[key] < 0:
            raise RuntimeError('Contagem DeepSeek ausente ou inválida.')
    if (usage['total_tokens'] != usage['prompt_tokens'] + usage['completion_tokens']
            or usage['prompt_cache_hit_tokens'] + usage['prompt_cache_miss_tokens'] != usage['prompt_tokens']
            or usage['completion_tokens'] > max_output or usage['total_tokens'] > CONTEXT_WINDOW):
        raise RuntimeError('Contagem DeepSeek inconsistente ou acima do contexto autorizado.')
    upper = (Decimal(usage['prompt_cache_miss_tokens']) * Decimal('0.3')
             + Decimal(usage['prompt_cache_hit_tokens']) * Decimal('0.006')
             + Decimal(usage['completion_tokens']) * Decimal('1.2')) / Decimal(1_000_000)
    # No internal reasoning or raw response retained. Billing may use off-peak rates.
    return {'text': content, 'usage': usage, 'model': MODEL,
            'documented_version': DOCUMENTED_VERSION, 'version_status': 'DOCUMENTED_ALIAS_NOT_IMMUTABLE_VERSION',
            'thinking_effort_requested': 'max', 'cost_estimate_usd': str(upper),
            'cost_estimate_range_usd': [str(upper / 2), str(upper)],
            'cost_status': 'PEAK_RATE_UPPER_ESTIMATE_NOT_INVOICE',
            'pricing_source': PRICE_SOURCE, 'pricing_checked_at': '2026-09-24',
            'verification': 'PROVIDER_COMPLETED_NOT_FACT_CHECKED'}


def execute(prompt, *, cancel=None, process_callback=None, max_output=MAX_OUTPUT):
    if authorization().get('enabled') is not True:
        raise RuntimeError('Uso pago DeepSeek ainda não autorizado.')
    if not isinstance(prompt, str) or not prompt.strip() or len(prompt.encode('utf-8')) > MAX_INPUT_BYTES:
        raise ValueError('Pedido DeepSeek vazio ou acima do orçamento técnico de entrada.')
    if type(max_output) is not int or not 1 <= max_output <= MAX_OUTPUT:
        raise ValueError('Limite de saída DeepSeek inválido.')
    if cancel and cancel.is_set():
        raise RuntimeError('Tarefa cancelada antes do envio.')
    payload = {'model': MODEL, 'messages': [{'role': 'user', 'content': prompt}],
               'max_tokens': max_output, 'stream': False,
               'thinking': {'type': 'enabled'}, 'reasoning_effort': 'max'}
    key = load_key()
    request = urllib.request.Request(URL, json.dumps(payload).encode('utf-8'),
        {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
    del key
    started = time.monotonic()
    try:
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=7200) as response:
            body = response.read(MAX_RESPONSE_BYTES + 1)
            if len(body) > MAX_RESPONSE_BYTES:
                raise RuntimeError('Resposta DeepSeek excedeu o limite técnico de armazenamento.')
    except urllib.error.HTTPError as exc:
        if exc.code in (402, 429):
            from .providers import ProviderLimitError
            raise ProviderLimitError(f'DeepSeek informou limite ou saldo indisponível (HTTP {exc.code}); sem repetição automática.') from None
        raise RuntimeError(f'DeepSeek recusou a chamada (HTTP {exc.code}); confira acesso no provedor.') from None
    except (urllib.error.URLError, TimeoutError, http.client.IncompleteRead):
        raise RuntimeError('Conexão DeepSeek interrompida; consumo pode ter ocorrido, sem repetição automática.') from None
    finally:
        request.remove_header('Authorization')
    if cancel and cancel.is_set():
        raise RuntimeError('Tarefa cancelada após envio; crédito pode ter sido consumido.')
    try:
        data = json.loads(body)
    except ValueError:
        raise RuntimeError('DeepSeek devolveu JSON inválido; sem repetição automática.') from None
    return dict(parse_response(data, max_output), elapsed_seconds=round(time.monotonic()-started, 3))


def validate_connection():
    # Persist dispatch before the request: an interrupted validation is not retried.
    if RECEIPT.is_file():
        previous = json.loads(RECEIPT.read_bytes())
        if previous.get('status') in ('validating', 'validation_failed'):
            raise RuntimeError('Validação DeepSeek já iniciada/falhou; conferir evidência antes de nova autorização.')
        if connection_status() == 'ready':
            return previous
    if not authorization().get('enabled') or not key_metadata()['stored']:
        raise RuntimeError('Cadastre a chave e autorize o uso antes de validar.')
    save_json(RECEIPT, {'status': 'validating', 'started_at': utc_now(), 'signature': signature()})
    try:
        result = execute('Responda somente o número: 6 × 7.', max_output=2048)
        if result['text'].strip().strip('.') != '42':
            raise RuntimeError('Teste DeepSeek não retornou 42.')
        record = {'status': 'ready', 'result': result}
    except Exception as exc:
        record = {'status': 'validation_failed', 'reason': str(exc)}
    record.update(checked_at=utc_now(), signature=signature())
    save_json(RECEIPT, record)
    return record
