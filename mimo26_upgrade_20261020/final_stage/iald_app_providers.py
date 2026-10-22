"""Account-scoped app transports. No scientific queue mutations.

Credentials remain in the existing Windows vault/client. Metrics contain no
prompts, answers, credentials or account identity. Nothing sends on import.
"""
import iald_router_media_view as router_media_view
import iald_app_memory as app_memory
import iald_routing_metrics as routing_metrics
from copy import copy
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import importlib
import codecs
import json
from pathlib import Path
import queue
import sqlite3
import sys
import threading
import time
import uuid
import iald_wallet_runtime as wallet_runtime
from iald_task_session import NAMES as TASK_TOOL_NAMES
from iald_task_bridge import encode_task_result

STACK = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
MODELS = {
    'deepseek': dict(model='deepseek-flash', label='DeepSeek V4.1 Flash', provider='DeepSeek',
        url='https://api.deepseek.com/chat/completions', output=393216,
        rates=(0.30, 0.006, 1.20), price_source='https://api-docs.deepseek.com/quick_start/pricing/'),
    'mimo': dict(model='mimo-v2.6-pro', label='MiMo V2.6 Pro', provider='Xiaomi MiMo',
        url='https://api.xiaomimimo.com/v1/chat/completions', output=131072,
        rates=(0.435, 0.0036, 0.87), price_source='https://mimo.mi.com/docs/en-US/price/pay-as-you-go'),
    'kimi': dict(model='kimi-code/k3', label='Kimi K3', provider='Moonshot AI',
        output=131072, rates=None, price_source='Kimi Code: assinatura, sem preço marginal verificado'),
}
WINDOW = 1048576
MAX_TOOLS = 4
MAX_PARSED_TOOLS = 32
MAX_ROUNDS = 4
TOOL_NAMES = frozenset(('iald_memory_read', 'search_tgl', 'fetch_tgl', 'search_web', 'fetch_url',
    'iald_kernel_search', 'iald_kernel_read', 'iald_kernel_verification',
    'iald_public_search', 'iald_public_read', 'get_current_datetime'))


FAMILY_ACCOUNTS = frozenset(('alanacaroline', 'liana'))


def allowed(record, username, provider=None):
    # Server-authenticated approved account only. Pending requests live elsewhere.
    if (not isinstance(username, str) or not username or not isinstance(record, dict)
            or not record or record.get('bloqueado') or record.get('acesso_bloqueado')):
        return False
    if provider is None:  # Legacy callers must never broaden a provider grant.
        return username == 'luiz' and record.get('plano') != 'gratuito'
    if provider not in MODELS:
        return False
    return True  # Approved accounts: shared executors under JEV, with individual consent.


def adapter(provider):
    if provider not in MODELS:
        raise ValueError('Provedor desconhecido.')
    if str(STACK) not in sys.path:
        sys.path.append(str(STACK))
    return importlib.import_module('iald_orchestrator.' + provider)


def availability(provider):
    try:
        module = adapter(provider)
        state = module.connection_status()
        return '' if state == 'ready' else 'Conexão do stack requer verificação: ' + str(state)
    except Exception:
        return 'Não foi possível verificar a conexão do stack.'


def options(record, username):
    rows = []
    for key, spec in MODELS.items():
        if not allowed(record, username, key):
            continue
        reason = availability(key)
        rows.append(dict(id=key, rotulo=spec['label'], modelo=spec['model'],
            provedor=spec['provider'], disponivel=not reason, motivo=reason,
            detalhe=spec['provider'] + ' · memória TGL' +
                (' · resposta completa após geração' if key == 'kimi' else '') +
                (' · ' + reason if reason else '')))
    return rows


def limits(provider, *, media_authorized=False):
    return dict(agente=provider != 'kimi', pensar=True, imagens=(provider == 'mimo'), audio=(provider == 'mimo' and media_authorized is True), video=(provider == 'mimo' and media_authorized is True),
        ferramentas=sorted(TOOL_NAMES) if provider != 'kimi' else [],
        max_saida=MODELS[provider]['output'], janela=WINDOW)


def context_metadata(provider):
    return dict(n_ctx=WINDOW, margem=0.95, reserva_resposta=MODELS[provider]['output'],
        cpt=1.0, teto_mensagens=400, contagem='limite conservador por bytes UTF-8')


def configuration(base, provider):
    cfg = copy(base)
    cfg.modelo = cfg.modelo_operador = MODELS[provider]['model']
    cfg.provedor = provider
    cfg.janela = WINDOW
    cfg.max_saida = cfg.max_saida_pensar = MODELS[provider]['output']
    cfg.chave = ''  # Keys are loaded only by the transport, never by metadata APIs.
    cfg.reserva_nativa = False
    return cfg


def consent_text(provider):
    spec = MODELS[provider]
    return (f"Neste modo, a IALD envia à {spec['provider']} o texto das "
        "mensagens, o histórico recente, seu perfil informado no chat e a memória científica "
        "canônica da TGL. As consultas usam somente fontes públicas e o kernel autorizado; "
        "senhas, dados de login e o acervo privado da Central não são enviados. "
        + ("Os anexos de imagem, áudio e vídeo são enviados somente à Xiaomi MiMo. "
           "Os PDFs são enviados como texto extraído, sem o arquivo PDF original. "
           "Os bytes dos anexos não são enviados ao TypeSafe nem à OpenAI. "
           "A moderação textual continua usando a OpenAI. " if provider == 'mimo' else
           "A moderação das mensagens continua usando a OpenAI. ")
        + ("O Kimi usa o cliente oficial da sua assinatura, incluindo o armazenamento local de sessão "
           "e as preferências de dados dessa conta. " if provider == 'kimi' else
           "O serviço usa a API do provedor e suas regras de privacidade e faturamento. ")
        + "Você pode revogar este consentimento nas configurações. O aceite vale somente para este provedor.")


class ProtocolError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


"""Staging-only image boundary. No network, vault or scientific-memory edits."""
import base64
import binascii


def request_media(client):
    """Public router projection: latest prompt plus media kinds/counts, no URLs."""
    import re
    counts = {'image':0,'audio':0,'video':0}
    encoded_bytes = 0
    prompt = ''
    if not isinstance(client,list): raise ValueError('Invalid message list')
    for message in client:
        if not isinstance(message,dict): raise ValueError('Invalid message')
        if message.get('role') not in ('user','assistant'): continue
        content = message.get('content')
        texts=[]
        if isinstance(content,str): texts=[content]
        elif isinstance(content,list):
            for part in content:
                if not isinstance(part,dict): raise ValueError('Invalid part')
                kind=part.get('type')
                if kind=='text':
                    if not isinstance(part.get('text'),str): raise ValueError('Invalid text')
                    texts.append(part['text'])
                elif kind in ('image_url','input_audio','video_url'):
                    key={'image_url':'image','input_audio':'audio','video_url':'video'}[kind]
                    counts[key]+=1
                    field='data' if kind=='input_audio' else 'url'
                    obj=part.get(kind)
                    value=obj.get(field) if isinstance(obj,dict) else None
                    if not isinstance(value,str): raise ValueError('Invalid media')
                    encoded_bytes+=len(value.encode('utf-8'))
                else: raise ValueError('Unsupported part')
        else: raise ValueError('Invalid content')
        if message.get('role')=='user':
            prompt=re.sub(r'\[ARQUIVO:[^\n]*\][\s\S]*?\[FIM\]','', '\n'.join(texts)).strip()
    return dict(kinds=[key for key,value in counts.items() if value],prompt=prompt,counts=counts,encoded_bytes=encoded_bytes)




def transport_response_format(mode=None):
    """Opt-in JSON object only; not an assertion of JSON Schema enforcement."""
    if mode is None:
        return {}
    if mode != 'json_object':
        raise ValueError('Unsupported response format')
    return {'response_format': {'type': 'json_object'}}


def transport_tool_options(provider, offered, round_no, rounds):
    """MiMo ignores tool_choice=none: omit tool definitions in final round."""
    if not offered or (provider == 'mimo' and round_no == rounds - 1):
        return {}
    return dict(tools=offered, tool_choice='none' if round_no == rounds - 1 else 'auto')


def image_parts(parts, *, images_authorized=False, media_authorized=False):
    """Server authorization must follow versioned MiMo image consent.

    Uses the existing Claude attachment signature detector, injected only when
    called. Never calls its permissive URL/marker conversion.
    """
    if images_authorized is not True:
        raise ValueError('MiMo image consent required')
    if not isinstance(parts, list) or not 1 <= len(parts) <= 16:
        raise ValueError('Invalid attachment parts')
    from iald_motor_claude import _tipo_pelos_bytes
    result, count, total = [], 0, 0
    for part in parts:
        if not isinstance(part, dict):
            raise ValueError('Invalid attachment part')
        if part.get('type') in ('input_audio','video_url'):
            from iald_mimo_multimodal import media_part
            if any(p.get('type') in ('input_audio','video_url') for p in result):
                raise ValueError('One audio/video attachment per message')
            result.append(media_part(part,media_authorized=media_authorized))
            continue
        if part.get('type') == 'text' and set(part) == {'type', 'text'}:
            if not isinstance(part['text'], str):
                raise ValueError('Invalid attachment text')
            result.append(dict(part))
            continue
        if set(part) != {'type', 'image_url'} or part.get('type') != 'image_url':
            raise ValueError('Unsupported media part')
        image = part['image_url']
        if not isinstance(image, dict) or set(image) != {'url'}:
            raise ValueError('Invalid image object')
        url = image['url']
        if not isinstance(url, str) or not url.startswith('data:image/') or ';base64,' not in url:
            raise ValueError('Only inline images accepted')
        header, data = url.split(';base64,', 1)
        if len(data) > 10_666_668:
            raise ValueError('Image exceeds local attachment limit')
        try:
            raw = base64.b64decode(data, validate=True)
        except (ValueError, binascii.Error):
            raise ValueError('Invalid image base64') from None
        mime = _tipo_pelos_bytes(data)
        if not raw or mime is None or header != 'data:' + mime:
            raise ValueError('Image type mismatch or unsupported format')
        count += 1
        total += len(raw)
        if count > 3 or len(raw) > 8_000_000 or total > 24_000_000:
            raise ValueError('Image attachment budget exceeded')
        result.append({'type': 'image_url', 'image_url': {'url': url}})
    return result


def wire_messages(messages, prefix, profile='', *, provider=None, images_authorized=False, media_authorized=False):
    if not isinstance(messages, list) or len(messages) > 400:
        raise ValueError('Histórico inválido ou muito extenso.')
    result = [{'role': 'system', 'content': prefix + ('\n\n' + profile if profile else '')}]
    for item in messages:
        if not isinstance(item, dict):
            raise ValueError('Mensagem inválida.')
        if item.get('role') in ('system', 'developer'):
            continue  # Client cannot replace server-owned memory/instructions.
        if isinstance(item.get('content'), list) and item.get('role') == 'user' and provider == 'mimo':
            parts = image_parts(item['content'], images_authorized=images_authorized, media_authorized=media_authorized)
            result.append({'role': 'user', 'content': parts})
            continue
        if item.get('role') not in ('user', 'assistant') or not isinstance(item.get('content'), str):
            raise ValueError('Este modelo aceita somente texto; remova imagens deste histórico.')
        result.append({'role': item['role'], 'content': item['content']})
    if len(result) < 2 or result[-1]['role'] != 'user':
        raise ValueError('Falta uma nova mensagem do usuário.')
    return router_media_view.project_system_messages(app_memory.project_messages(result))


def output_budget(payload, maximum):
    """Reserve the largest safe output without reducing any input or memory.

    UTF-8 size is a conservative admission bound, not measured provider tokens.
    The 128-byte allowance covers the output field added after this calculation.
    Reject before loading credentials if a useful response cannot be reserved.
    """
    if type(maximum) is not int or maximum < 1:
        raise ValueError('Invalid output maximum')
    used = len(json.dumps(payload, ensure_ascii=False).encode('utf-8'))
    available = WINDOW - used - 4096 - 128
    reserve = min(maximum, available)
    if reserve < min(16384, maximum):
        raise ValueError('A memória e esta conversa não deixam espaço seguro para a resposta. '
                         'Nada foi enviado; o núcleo e o histórico foram preservados.')
    return reserve


def check_window(payload, reserve):
    # Tokenizers differ. UTF-8 bytes plus structural margin is a conservative
    # admission bound, never a claim of measured provider tokens.
    used = len(json.dumps(payload, ensure_ascii=False).encode('utf-8'))
    if used + reserve + 4096 > WINDOW:
        raise ValueError('A memória e esta conversa excedem a margem técnica do modelo. '
                         'Abra uma nova conversa; o núcleo não foi reduzido e nada foi reenviado.')
    return used


def usage_cost(provider, usage):
    if not isinstance(usage, dict):
        raise ValueError('Provedor não informou consumo verificável.')
    for name in ('prompt_tokens', 'completion_tokens', 'total_tokens'):
        if type(usage.get(name)) is not int or usage[name] < 0:
            raise ValueError('Contagem inválida do provedor.')
    pin, out = usage['prompt_tokens'], usage['completion_tokens']
    if pin + out != usage['total_tokens']:
        raise ValueError('Contagem inconsistente do provedor.')
    cached = (usage.get('prompt_cache_hit_tokens', 0) if provider == 'deepseek' else
              usage.get('cached_input_tokens', 0) if provider == 'kimi' else
              (usage.get('prompt_tokens_details') or {}).get('cached_tokens', 0))
    if type(cached) is not int or not 0 <= cached <= pin:
        raise ValueError('Contagem de cache inválida.')
    rates = MODELS[provider]['rates']
    cost = None if rates is None else ((pin-cached)*rates[0]+cached*rates[1]+out*rates[2])/1e6
    return dict(input_tokens=pin, output_tokens=out, cached_tokens=cached, cost_estimate_usd=cost)


def sse(value):
    return 'data: ' + (value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)) + '\n\n'


def scoped_task_names(tools, extra=(), authorize=None):
    """Server-created scope allowlist; a model/tool payload cannot extend it."""
    if not isinstance(extra,(tuple,list,set,frozenset)):
        raise ProtocolError('invalid_task_tool_scope')
    if any(not isinstance(name,str) or not 1 <= len(name) <= 64
           or not name.isascii() or not name.replace('_','').replace('-','').isalnum() for name in extra):
        raise ProtocolError('invalid_task_tool_scope')
    extra = frozenset(extra)
    offered = {(tool.get('function') or {}).get('name') for tool in tools}
    if not extra <= offered or extra & TOOL_NAMES:
        raise ProtocolError('invalid_task_tool_scope')
    if extra - TASK_TOOL_NAMES and not callable(authorize):
        raise ProtocolError('task_scope_authorization_required')
    return TASK_TOOL_NAMES | extra


class Evaluation:
    def __init__(self, root):
        self.root = Path(root)
        self.lock = threading.Lock()
        self.active_accounts = set()

    def db(self):
        root = self.root / '.iald_runtime' / 'app_evaluation'
        root.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(root / 'metrics.sqlite3', timeout=5)
        db.execute('CREATE TABLE IF NOT EXISTS turns (id TEXT PRIMARY KEY, data TEXT NOT NULL)')
        return db

    def save(self, record):
        with closing(self.db()) as db, db:
            db.execute('INSERT OR REPLACE INTO turns VALUES (?, ?)',
                       (record['id'], json.dumps(record, ensure_ascii=False)))

    def report(self):
        with closing(self.db()) as db:
            records = [json.loads(row[0]) for row in db.execute('SELECT data FROM turns ORDER BY rowid DESC LIMIT 200')]
        return {'records': records, 'pricing_checked_at': '2026-09-30',
            'note': 'Custos estimados a partir do usage; Kimi é assinatura. Qualidade requer avaliação do operador.',
            'jev': 'Auxiliar de decisão estruturada; não ativado como chat nem como juiz de provas.'}

    def observe(self, flow, model, *, rates=None, memory_sha256=None, messages=None):
        """Read-only observer of existing transports; forwards their exact bytes.

        Some transports omit usage from public SSE. In that case the dashboard
        records unknown consumption instead of inventing tokens or a zero cost.
        """
        started = time.monotonic()
        record = dict(id=uuid.uuid4().hex, provider=model['motor'], model=model['id'],
            utc=datetime.now(timezone.utc).isoformat(), status='started', memory_sha256=memory_sha256,
            first_text_seconds=None, calls=[], streaming=True, metrics_source='existing_app_sse')
        routing_metrics.stamp(record, messages)
        decoder=codecs.getincrementaldecoder('utf-8')()
        buffer=''
        error=False
        try:
            self.save(record)
            for chunk in flow:
                buffer += decoder.decode(chunk) if isinstance(chunk,bytes) else chunk
                while '\n' in buffer:
                    line,buffer=buffer.split('\n',1)
                    if not line.startswith('data:'): continue
                    raw=line[5:].strip()
                    if raw=='[DONE]': record['status']='failed_or_uncertain' if error else 'completed';continue
                    try: item=json.loads(raw)
                    except ValueError: continue
                    if item.get('iald_aviso'): error=True
                    for choice in item.get('choices') or []:
                        if (choice.get('delta') or {}).get('content') and record['first_text_seconds'] is None:
                            record['first_text_seconds']=round(time.monotonic()-started,3)
                    usage=item.get('usage')
                    if isinstance(usage,dict):
                        pin,out=usage.get('prompt_tokens'),usage.get('completion_tokens')
                        cached=(usage.get('prompt_tokens_details') or {}).get('cached_tokens',0)
                        if all(type(n)is int and n>=0 for n in (pin,out,cached)) and cached<=pin:
                            cost=((pin-cached)*rates[0]+cached*rates[1]+out*rates[2])/1e6 if rates else None
                            if model['motor']=='claude':
                                writes=(usage.get('prompt_tokens_details') or {}).get('cache_write_tokens')
                                cost=(((pin-cached-writes)*rates[0]+cached*rates[1]+out*rates[2]+writes*rates[3])/1e6
                                    if rates and len(rates)==4 and type(writes)is int and 0<=writes<=pin-cached else None)
                            record['calls'].append(dict(status='completed',input_tokens=pin,output_tokens=out,
                                cached_tokens=cached,cost_estimate_usd=cost))
                yield chunk
        finally:
            if record['status']=='started':record['status']='interrupted'
            record['elapsed_seconds']=round(time.monotonic()-started,3)
            try:self.save(record)
            finally:
                close=getattr(flow,'close',None)
                if close:close()

    def stream(self, provider, messages, tools, execute_tool, *, memory_sha256, http_post=None, account_key='operator', spending=None, task_control=None, authorize=None, task_tool_names=()):
        """One active request per account. No fallback/retry after dispatch."""
        scoped_task_names(tools,task_tool_names,authorize)
        task_tool_names = frozenset(task_tool_names)
        with self.lock:
            busy = account_key in self.active_accounts
            if not busy:
                self.active_accounts.add(account_key)
        if busy:
            yield sse({'iald_aviso': {'tipo': 'em_andamento', 'texto': 'Uma resposta desta conta já está em andamento.'}})
            yield sse('[DONE]'); return
        events = queue.Queue(maxsize=256)
        cancel = task_control.cancel if task_control is not None else threading.Event()
        active_response = []
        started = time.monotonic()
        spec = MODELS[provider]
        record = dict(id=uuid.uuid4().hex, provider=provider, model=spec['model'],
            utc=datetime.now(timezone.utc).isoformat(), status='started', memory_sha256=memory_sha256,
            memory_scope='SHARED_VERIFIED_FIXED_CORE_AND_CLUSTER', context_count='UTF8_CONSERVATIVE_BOUND',
            price_source=spec['price_source'], pricing_checked_at='2026-09-30',
            streaming=provider != 'kimi', calls=[], first_text_seconds=None)
        routing_metrics.stamp(record, messages)

        def emit(value):
            while not cancel.is_set():
                try: events.put(value, timeout=.2); return
                except queue.Full: pass
            raise InterruptedError('Avaliação cancelada; pode haver consumo no provedor.')

        def run():
            subscription_event = None
            try:
                if cancel.is_set(): raise InterruptedError()
                self.save(record)  # Durable before dispatch; unknown usage is never zero.
                if provider == 'kimi':
                    # Public CLI API buffers the final answer; do not fake token streaming.
                    projected = router_media_view.project_system_messages(app_memory.project_messages(messages))
                    prompt = json.dumps({'instructions': projected[0]['content'], 'conversation': projected[1:]}, ensure_ascii=False)
                    check_window({'prompt': prompt}, spec['output'])
                    record['calls'].append({'status': 'dispatched', 'usage': None})
                    self.save(record)
                    if cancel.is_set(): raise InterruptedError()
                    if authorize is not None:authorize()
                    subscription_event = wallet_runtime.subscription_begin(spec['model'])
                    result = app_memory.call('model.kimi', adapter(provider).execute, prompt, cancel=cancel)
                    measured = usage_cost(provider, result['usage'])
                    record['calls'][-1] = dict(status='completed', **measured)
                    record['first_text_seconds'] = round(time.monotonic()-started, 3)
                    emit({'choices': [{'delta': {'content': result['text']}}]})
                else:
                    self._api(provider, messages, tools, execute_tool, emit, cancel,
                              active_response, record, started, http_post, spending, authorize, task_tool_names)
                record['status'] = 'completed'
            except Exception as exc:
                record['status'] = 'cancelled_or_uncertain' if cancel.is_set() else 'failed_or_uncertain'
                record['error_type'] = type(exc).__name__
                record['error_code'] = getattr(exc, 'code', 'transport_or_unclassified')
                if isinstance(exc, json.JSONDecodeError): record['error_code'] = 'invalid_provider_json'
                # Never render provider bodies, local paths or exception secrets.
                if not cancel.is_set():
                    from iald_orcamento import BudgetError
                    if isinstance(exc,BudgetError):
                        emit({'iald_aviso': {'tipo':'limite','texto':str(exc),'bloqueado_por':exc.bloqueado_por}})
                    else:
                        emit({'iald_aviso': {'tipo': 'falha_motor', 'texto':
                            'A resposta não concluiu. O registro foi preservado no painel; não houve repetição automática.'}})
            finally:
                wallet_runtime.subscription_end(subscription_event)
                if spending is not None:
                    try: spending.close()
                    except Exception:
                        record.update(status='failed_or_uncertain',error_code='spending_record_failed')
                        if not cancel.is_set():
                            try: emit({'iald_aviso':{'tipo':'limite','texto':'O registro de uso precisa de conferência. Não houve reenvio.','bloqueado_por':'razao'}})
                            except InterruptedError: pass
                record['elapsed_seconds'] = round(time.monotonic()-started, 3)
                try: self.save(record)
                finally:
                    with self.lock:
                        self.active_accounts.discard(account_key)
                    try:
                        if not cancel.is_set(): emit('[DONE]')
                    finally:
                        if task_control is not None: task_control.finish()

        worker_run, worker_failed = wallet_runtime.threaded(app_memory.thread_target(run))
        worker = threading.Thread(target=worker_run, daemon=True, name='iald-app-evaluation')
        tracked = False
        try:
            if task_control is not None:
                task_control.start(); tracked = True
            worker.start()
        except BaseException:
            worker_failed()
            with self.lock: self.active_accounts.discard(account_key)
            if tracked: task_control.finish()
            raise
        completed = False
        try:
            yield sse({'iald_modelo': {'id': spec['model'], 'rotulo': spec['label'], 'motor': provider}})
            yield sse({'iald_status': {'fase': 'pensando', 'rotulo':
                'Kimi está gerando; a resposta chegará completa.' if provider == 'kimi' else 'Preparando resposta com a memória TGL.'}})
            while True:
                if cancel.is_set(): raise InterruptedError()
                try: value = events.get(timeout=.2 if task_control is not None else 10)
                except queue.Empty:
                    if not worker.is_alive(): raise RuntimeError('Registro de avaliação indisponível.')
                    yield ': keepalive\n\n'; continue
                if value == '[DONE]': completed = True
                yield sse(value)
                if completed: break
        finally:
            # A normal child completion must not cancel its parent.
            if not completed: cancel.set()
            for response in list(active_response):
                try: response.close()
                except Exception: pass

    def _api(self, provider, messages, tools, execute_tool, emit, cancel, responses, record, started, http_post, spending=None, authorize=None, task_tool_names=()):
        import requests
        spec = MODELS[provider]
        module = adapter(provider)
        task_names = scoped_task_names(tools,task_tool_names,authorize)
        offered = [t for t in tools if (t.get('function') or {}).get('name') in (TOOL_NAMES | task_names)]
        names = {t['function']['name'] for t in offered}
        rounds = 8 if names & task_names else MAX_ROUNDS
        for round_no in range(rounds):
            if cancel.is_set(): raise InterruptedError()
            body = dict(model=spec['model'], messages=router_media_view.project_system_messages(app_memory.project_messages(messages)), stream=True,
                stream_options={'include_usage': True}, thinking={'type': 'enabled'})
            if provider == 'deepseek': body['reasoning_effort'] = 'max'
            body.update(transport_tool_options(provider, offered, round_no, rounds))
            reserve = output_budget(body, spec['output'])
            body['max_tokens' if provider == 'deepseek' else 'max_completion_tokens'] = reserve
            bound = check_window(body, reserve)
            key = module.load_key() if provider == 'deepseek' else module.load_mimo()
            headers = {'Content-Type': 'application/json',
                ('Authorization' if provider == 'deepseek' else 'api-key'): ('Bearer ' if provider == 'deepseek' else '') + key}
            del key
            try:
                if authorize is not None:authorize()
                if spending is not None: spending.before(provider, body, bound)
                record['calls'].append(dict(status='dispatched', usage=None, input_bytes_bound=bound, output_reserved_tokens=reserve))
                self.save(record)
                if cancel.is_set(): raise InterruptedError()
                if authorize is not None:
                    try:authorize()
                    except Exception:
                        record['calls'][-1]['status']='not_dispatched'
                        if spending is not None:spending.discard_undispatched()
                        raise
                response = app_memory.http_call('model.' + provider, (http_post or requests.post), spec['url'], json=body, headers=headers,
                    stream=True, allow_redirects=False, timeout=(15, 300))
            finally:
                headers.clear()
            responses.append(response)
            content, reasoning, calls, usage, finish, done = '', '', {}, None, None, False
            record['protocol'] = dict(round=round_no, chunks=0, tool_calls=0,
                finish_reason=None, http_status=response.status_code)
            try:
                # A disconnect can occur while requests.post waits for headers.
                # Register first, then check: cancellation either sees and closes
                # the registered response, or this branch closes it in finally.
                if cancel.is_set(): raise InterruptedError()
                if response.status_code != 200: raise RuntimeError('Provider HTTP ' + str(response.status_code))
                for raw in response.iter_lines(chunk_size=1):
                    if cancel.is_set(): raise InterruptedError()
                    if not raw: continue
                    line = raw.decode('utf-8') if isinstance(raw, bytes) else raw
                    if not line.startswith('data:'): continue
                    text = line[5:].strip()
                    if text == '[DONE]': done = True; break
                    chunk = json.loads(text)
                    record['protocol']['chunks'] += 1
                    if chunk.get('error') or chunk.get('model') != spec['model']:
                        raise ProtocolError('unexpected_provider_model')
                    if chunk.get('usage') is not None: usage = chunk['usage']
                    for choice in chunk.get('choices', []):
                        if choice.get('index', 0) != 0: raise ProtocolError('unexpected_choices')
                        delta = choice.get('delta') or {}
                        reasoning += delta.get('reasoning_content') or ''
                        value = delta.get('content') or ''
                        content += value
                        if len(content) + len(reasoning) > 4000000: raise ValueError('Resposta excessiva.')
                        if value:
                            if record['first_text_seconds'] is None: record['first_text_seconds'] = round(time.monotonic()-started, 3)
                            emit({'choices': [{'delta': {'content': value}}]})
                        for tool in delta.get('tool_calls') or []:
                            idx = tool.get('index')
                            if type(idx) is not int or not 0 <= idx < MAX_PARSED_TOOLS: raise ProtocolError('tool_batch_limit')
                            record['protocol']['tool_calls'] = max(record['protocol']['tool_calls'], idx+1)
                            item = calls.setdefault(idx, {'id': '', 'type': 'function', 'function': {'name': '', 'arguments': ''}})
                            if tool.get('id'): item['id'] = tool['id']
                            for field in ('name', 'arguments'):
                                item['function'][field] += (tool.get('function') or {}).get(field) or ''
                            if len(item['function']['arguments']) > 64000: raise ProtocolError('tool_arguments_limit')
                        if choice.get('finish_reason') is not None:
                            finish = choice['finish_reason']
                            record['protocol']['finish_reason'] = finish if finish in ('stop','tool_calls','length','content_filter','insufficient_system_resource') else 'unknown'
                if not done or finish not in ('stop', 'tool_calls'): raise ProtocolError('incomplete_stream')
                measured = usage_cost(provider, usage)
                record['calls'][-1] = dict(status='completed', input_bytes_bound=bound, output_reserved_tokens=reserve, **measured)
                self.save(record)
                if spending is not None: spending.settle(measured)
            finally:
                response.close(); responses.remove(response)
            if finish == 'stop':
                if calls or not content.strip(): raise ProtocolError('invalid_completion')
                return
            if not calls or round_no == rounds-1: raise ProtocolError('tool_round_limit')
            if cancel.is_set(): raise InterruptedError()
            batch = [calls[i] for i in sorted(calls)]
            messages.append(dict(role='assistant', content=content, reasoning_content=reasoning, tool_calls=batch))
            for position, item in enumerate(batch):
                if cancel.is_set(): raise InterruptedError()
                name = item['function']['name']
                args = json.loads(item['function']['arguments'])
                if name not in names or not item['id'] or not isinstance(args, dict): raise ProtocolError('tool_not_allowed')
                emit({'iald_status': {'fase': 'ferramenta', 'tool': name, 'rotulo': ('Executando etapa da tarefa' if name in task_names else 'Consultando fontes da TGL'),
                                     'loop': round_no+1, 'max_loops': rounds}})
                # Parse the entire bounded batch and preserve every call ID.
                # Do not abort a paid stream for a fifth valid read request.
                # Excess calls get an explicit tool result, never silent omission.
                if name in task_names and authorize is not None:authorize()
                result = (app_memory.call('tool.' + name, execute_tool, name, args) if position < MAX_TOOLS else
                    {'status':'TOOL_BUDGET_REACHED','notice':
                     'Esta chamada não foi executada. Use as fontes já obtidas e o núcleo carregado para concluir; peça só a passagem indispensável se faltar evidência.'})
                app_memory.tool_result(name, args, result)
                if name in task_names: result = encode_task_result(result)
                elif not isinstance(result, str): result = json.dumps(result, ensure_ascii=False)
                if name not in task_names and len(result) > 24000:
                    result = json.dumps({'status': 'PARTIAL', 'excerpt': result[:24000],
                        'notice': 'Resultado parcial. Consulte novamente com intervalo menor.'}, ensure_ascii=False)
                messages.append(dict(role='tool', tool_call_id=item['id'], content=result))
                emit({'iald_status': {'fase': 'ferramenta_ok', 'tool': name, 'rotulo': ('Etapa concluída' if name in task_names else 'Fonte consultada'), 'chars': len(result)}})
        raise ValueError('Avaliação não concluída.')
