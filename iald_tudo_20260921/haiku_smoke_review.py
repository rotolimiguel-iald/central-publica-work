"""Review-only smoke harness. CLI dry-run never imports ROOT or opens credentials.

--execute is deliberately blocked until an approved authenticated in-process
server entry exists. run_in_server reuses the LIVE ledger and SQLite guard;
it must never be called with a second server import in an external process.
"""
import argparse
from copy import copy
from decimal import Decimal
import hashlib
import importlib
import json
import math
from pathlib import Path
import re
import threading
import sys
from datetime import datetime, timezone

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent
QUESTIONS = ('Responda em uma frase: quem é o autor da TGL?',
             'Responda em uma frase: NOT_FALSIFIED equivale a confirmação?')
MODEL = 'claude-haiku-4-5-20251001'
PER_CALL = Decimal('0.325')
TOTAL = Decimal('0.65')
_RUN_LOCK = threading.Lock()


class SmokeBlocked(ValueError):
    """Messages are fixed safe codes, never raw provider/config exceptions."""


def _money(value):
    if isinstance(value, bool):
        raise SmokeBlocked('invalid_money')
    result = Decimal(str(value))
    if not result.is_finite() or result < 0:
        raise SmokeBlocked('invalid_money')
    return result


class SmokeGuard:
    """Additional limits over the SAME SpendingGuard, never replacement quotas.

    Gross successful caps consume the test allowance even after a free refusal.
    Attempts are also limited to two. The real guard can apply a safety factor:
    inspect the committed row before allowing send; reject/release any increase.
    Thus NativeAccount's hold receipt stays equal to the guard's actual cap.
    """
    def __init__(self, guard, read_cap=None):
        self.guard = guard
        self.read_cap = read_cap or self._read_cap
        self.attempts = 0
        self.gross = Decimal('0')
        self.keys = {}
        self.stopped = False
        self.lock = threading.RLock()

    def _read_cap(self, key):
        with self.guard._connect() as db:
            row = db.execute('SELECT cap FROM calls WHERE id=?', (key,)).fetchone()
        if row is None:
            raise SmokeBlocked('reservation_not_found')
        return row[0]

    def check(self, *args, **kwargs):
        if self.stopped:
            raise SmokeBlocked('test_stopped')
        return self.guard.check(*args, **kwargs)

    def reserve(self, user, model, cap, user_limit, global_limit, **kwargs):
        with self.lock:
            amount = _money(cap)
            if (self.stopped or user != 'luiz' or model != MODEL
                    or self.attempts >= 2 or amount > PER_CALL
                    or self.gross + amount > TOTAL or _money(global_limit) != Decimal('15')):
                raise SmokeBlocked('test_reservation_limit')
            self.attempts += 1
            key = self.guard.reserve(user, model, cap, user_limit, global_limit, **kwargs)
            try:
                actual = _money(self.read_cap(key))
                if actual != amount:
                    raise SmokeBlocked('guard_safety_factor_changed_cap')
            except Exception:
                self.stopped = True
                # No generation has happened: release only this new hold.
                self.guard.settle(key, 0)
                raise SmokeBlocked('reservation_preflight_failed') from None
            self.gross += amount
            self.keys[key] = amount
            return key

    def settle(self, key, amount=None, estimate=None):
        with self.lock:
            if key not in self.keys:
                raise SmokeBlocked('unknown_test_reservation')
            if estimate is not None:
                raise SmokeBlocked('partial_hold_forbidden')
            if amount is not None and _money(amount) > self.keys[key]:
                self.stopped = True
            # Preserve real overage recording/pauses; never suppress provider usage.
            return self.guard.settle(key, amount)


def _real(name):
    module = importlib.import_module(name)
    if Path(module.__file__).resolve().parent != ROOT.resolve():
        raise SmokeBlocked('module_not_from_installed_root')
    return module


def _store(path, value):
    raw = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False).encode('utf-8')
    tmp = path.with_suffix('.tmp')
    with tmp.open('xb') as stream:
        stream.write(raw)
    if tmp.read_bytes() != raw:
        raise SmokeBlocked('receipt_write_failed')
    tmp.replace(path)


def _short(text, cfg):
    # Response only, bounded; never persist request/system/wire or error objects.
    value = str(text)[:400]
    secret = getattr(cfg, 'chave', '')
    if secret:
        value = value.replace(secret, '[redacted]')
    return re.sub(r'sk-[A-Za-z0-9_-]+', '[redacted]', value)


def run_in_server(server, *, approved_for_this_run=False, execution_id=''):
    """Future authenticated admin hook, NOT currently wired to any endpoint.

    approved_for_this_run must be server-owned approval, never HTTP input.
    Caller must verify this is the sole live writer process for RAZAO_CLAUDE.
    One approval/execution_id authorizes at most two sends; receipt is replay gate.
    """
    if approved_for_this_run is not True:
        raise SmokeBlocked('specific_user_approval_required')
    if not re.fullmatch(r'[a-zA-Z0-9_-]{8,80}', execution_id):
        raise SmokeBlocked('invalid_execution_id')
    if not _RUN_LOCK.acquire(blocking=False):
        raise SmokeBlocked('smoke_already_running')
    try:
        if Path(server.__file__).resolve().parent != ROOT.resolve():
            raise SmokeBlocked('requires_live_installed_server')
        if server.require_admin() is not None or server.session.get('username') != 'luiz':
            raise SmokeBlocked('authenticated_local_luiz_admin_required')
        # No env reading: use the existing in-memory server config only.
        motors = _real('iald_motores')
        budget = _real('iald_orcamento')
        native = _real('claude_native_account')
        context = _real('claude_context_snapshot')
        transport = _real('claude_guarded_transport')
        counter_module = _real('claude_native_counter')
        messages = _real('claude_haiku_messages')
        routing = _real('claude_route_bridge')
        policy_module = _real('claude_server_selection')
        adapter = _real('iald_motor_claude')
        package_module = _real('claude_memory_package')
        base = server.CLAUDE_CFG
        if base.cache_ttl != '5m' or _money(base.cota_global_usd) != Decimal('15'):
            raise SmokeBlocked('reviewed_cache_or_global_policy_changed')
        # Read actual user only on this future approved in-server path.
        with server._TRAVA_USUARIOS:
            record = copy(server.load_users_estrito().get('luiz') or {})
        if not record or record.get('bloqueado') or not motors.consentiu(record, motors.CLAUDE):
            raise SmokeBlocked('anthropic_consent_required')
        ledger = server.RAZAO_CLAUDE
        if (not isinstance(ledger, motors.RazaoDeUso)
                or Path(ledger.caminho).resolve() != (ROOT/'iald_uso_claude.json').resolve()):
            raise SmokeBlocked('live_ledger_identity_required')
        guard = server._guarda_do_motor(motors.CLAUDE)
        if (not isinstance(guard, budget.SpendingGuard)
                or Path(guard.path).resolve() != Path(ledger.caminho + '.reservas.sqlite3').resolve()):
            raise SmokeBlocked('live_spending_guard_required')
        package, snapshot = context.load_snapshot(ROOT/'.iald_runtime/haiku', package_module.load_package)
        bridge = routing.RouteBridge(motors=motors, base_config=base,
            package_loader=lambda: package, enabled=True,
            public_daily_usd=None, public_group_daily_usd=None)
        # Temporary record selects Haiku without writing the real account.
        selected = dict(record, modelo_claude=MODEL)
        cfg = bridge.configuration(selected, 'luiz')
        cfg.max_saida = cfg.max_saida_pensar = 512
        checked = context.CheckedAdapter(adapter, snapshot)
        definitions = server._haiku_tool_definitions()
        limiter = SmokeGuard(guard)
        state = adapter.EstadoClaude()
        cache = {}
        client = adapter.cliente_para(cfg).with_options(max_retries=0)
        if client.max_retries != 0:
            raise SmokeBlocked('no_retry_client_required')
        def count_wire(wire):
            context.verify_native_tools(wire, snapshot)
            identity = hashlib.sha256(json.dumps(wire, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
            if identity not in cache:
                cache[identity] = counter_module.count_native_request(client, wire)
            return cache[identity]
        def count_payload(payload):
            wire = checked.converter_pedido(cfg, payload, prefixo=package.prefix, estado=state)
            wire.pop('output_config', None)
            wire['thinking'] = {'type':'disabled'}
            return count_wire(wire)
        # Replay gate created BEFORE counts/reservations/provider sends.
        directory = WORK/'haiku_smoke_receipts'
        directory.mkdir(exist_ok=True)
        receipt_path = directory/(execution_id+'.json')
        with receipt_path.open('xb') as stream:
            stream.write(b'{"status":"STARTING"}')
        receipt = {'status':'RUNNING','execution_id':execution_id,'model':MODEL,
            'started_utc':datetime.now(timezone.utc).isoformat(),'calls':[],
            'prefix_sha256':snapshot.prefix_sha256,'tools_sha256':snapshot.tools_sha256,
            'limits':{'per_call_usd':.325,'total_usd':.65,'max_reservations':2,'max_output':512},
            'cache_ttl':'5m','max_retries':0,'scope':'authorized in-process smoke; no production feature activation'}
        _store(receipt_path, receipt)
        history = []
        for question in QUESTIONS:
            item = {'status':'PREPARING','input_tokens':None,'cache_write_tokens':None,
                    'cache_read_tokens':None,'output_tokens':None,'cost_usd':None,'response_short':''}
            receipt['calls'].append(item)
            account = None
            response = None
            text_parts = []
            complete = False
            try:
                # Consent/revocation remains live at EACH paid call.
                with server._TRAVA_USUARIOS:
                    current = server.load_users_estrito().get('luiz') or {}
                if current.get('bloqueado') or not motors.consentiu(current, motors.CLAUDE):
                    raise SmokeBlocked('anthropic_consent_required')
                history.append({'role':'user','content':question})
                assembled, _ = messages.assemble(motors, history, package.prefix, MODEL,
                                                [t['function']['name'] for t in definitions])
                payload = context.attach_openai_tools({'model':MODEL,'messages':assembled,
                    'max_completion_tokens':512,'tool_choice':'none'},definitions)
                account = native.NativeAccount(motors=motors,budget=budget,guard=limiter,
                    ledger=ledger,cfg=cfg,user='luiz',admin=bool(current.get('admin')),model=MODEL,
                    quota_key=server._chave_cota_de(current,'luiz'),plan=motors.plano_de(current),
                    prefix_tokens=package.measurement.permanent_tokens,count_request=count_payload)
                account.iniciar_chamada(payload)
                item['reserved_usd'] = account.pending['cap']
                item['input_count_before_send'] = account.pending['input']
                _store(receipt_path, receipt)
                policy = policy_module.policy_for(current,'luiz',**bridge.policy_flags('luiz'))
                response, decision = transport.post_guarded(checked,cfg,payload,
                    requested_model=MODEL,server_policy=policy,prefix=package.prefix,
                    memory=package.measurement,state=state,client=client,counter=count_wire,timeout=120)
                if response.status_code != 200:
                    error = response.json().get('error',{})
                    if adapter.recusa_sem_cobranca(response.status_code,error.get('code','')):
                        account.descartar_ultima_chamada()
                        item['status']='KNOWN_FREE_REFUSAL'
                        item['cost_usd']=0
                    else:
                        item['status']='UNCERTAIN_HOLD'
                    break
                got_done = False
                for line in response.iter_lines():
                    line = line.decode('utf-8') if isinstance(line,bytes) else line
                    if not line.startswith('data: '):continue
                    body=line[6:]
                    if body=='[DONE]':got_done=True;break
                    event=json.loads(body)
                    if event.get('error'):
                        raise SmokeBlocked('stream_interrupted')
                    if event.get('usage'):
                        if account.usos:raise SmokeBlocked('duplicate_usage')
                        usage=event['usage'];account.uso(usage)
                        details=usage.get('prompt_tokens_details') or {}
                        item.update(input_tokens=usage['prompt_tokens'],
                            cache_write_tokens=details.get('cache_write_tokens',0),
                            cache_read_tokens=details.get('cached_tokens',0),
                            output_tokens=usage['completion_tokens'],
                            cost_usd=native.usage_amount(usage,cfg.precos(MODEL))[3])
                    for choice in event.get('choices',[]):
                        delta=choice.get('delta') or {}
                        if delta.get('tool_calls'):raise SmokeBlocked('unexpected_tool_call')
                        if delta.get('content'):text_parts.append(str(delta['content']))
                if not got_done or not account.usos:
                    raise SmokeBlocked('missing_final_usage_or_done')
                complete=True;item['status']='MEASURED'
            except Exception:
                # No raw exceptions, wire, prefix, account record or credentials.
                item['status']='UNCERTAIN_HOLD' if account and account.pending else 'STOPPED'
            finally:
                try:
                    if response is not None:response.close()
                except Exception:
                    item['status']='STREAM_CLOSE_FAILED';complete=False
                try:
                    if account is not None:account.fechar()
                except Exception:
                    item['status']='LEDGER_RECONCILIATION_REQUIRED';complete=False
                item['response_short']=_short(''.join(text_parts),cfg)
                if item['status']=='UNCERTAIN_HOLD':
                    item['held_usd']=item.get('reserved_usd')
                    item['cost_usd']=None  # hold is not measured provider cost
                _store(receipt_path,receipt)
            if not complete or limiter.stopped:break
            history.append({'role':'assistant','content':''.join(text_parts)})
        receipt['status']='COMPLETED' if len(receipt['calls'])==2 and all(c['status']=='MEASURED' for c in receipt['calls']) else 'STOPPED_REVIEW_REQUIRED'
        receipt['reservation_attempts']=limiter.attempts
        receipt['gross_reserved_usd']=float(limiter.gross)
        _store(receipt_path,receipt)
        return receipt_path
    finally:
        _RUN_LOCK.release()


def prepare_wire():
    """Offline public requests only; no server, users, SDK, client or counter.

    Request 2 is a standalone preflight, NOT the unknown actual second turn.
    Wire artifacts contain public measured memory; metadata receipts do not.
    """
    import socket
    from unittest.mock import patch
    def deny_network(*args, **kwargs):
        raise SmokeBlocked('offline_network_forbidden')
    old_path = list(sys.path)
    old_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(ROOT))
    try:
        with patch.object(socket.socket, 'connect', deny_network), patch.object(socket.socket, 'connect_ex', deny_network), patch.object(socket, 'create_connection', deny_network), patch.object(socket, 'getaddrinfo', deny_network):
            motors = _real('iald_motores')
            adapter = _real('iald_motor_claude')
            context = _real('claude_context_snapshot')
            packages = _real('claude_memory_package')
            messages = _real('claude_haiku_messages')
            providers = [_real(n) for n in ('iald_kernel', 'iald_fontes_publicas', 'iald_core_indexado')]
            definitions = sum((p.tool_definitions() for p in providers), [])
            package, snapshot = context.load_snapshot(ROOT/'.iald_runtime/haiku', packages.load_package)
            cfg = motors.Config(modelo=MODEL, modelo_operador=MODEL, provedor=motors.CLAUDE,
                                max_saida=512, max_saida_pensar=512, cache_ttl='5m')
            checked = context.CheckedAdapter(adapter, snapshot)
            directory = WORK/('haiku_smoke_preflight_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'))
            directory.mkdir()
            result = {'status':'OFFLINE_WIRES_PREPARED', 'network_calls':0, 'generation_calls':0,
                      'real_account_reads':0, 'provider_token_count':None,
                      'second_request_scope':'standalone; real turn 2 requires real first answer and recount',
                      'config_scope':'real Config with explicit synthetic noncredential fields; not live server config',
                      'prefix_sha256':snapshot.prefix_sha256, 'tools_sha256':snapshot.tools_sha256,
                      'permanent_tokens_from_validated_receipt':snapshot.permanent,
                      'requests':[], 'source_sha256':{}}
            for index, question in enumerate(QUESTIONS, 1):
                assembled, _ = messages.assemble(motors, [{'role':'user','content':question}], package.prefix,
                                                MODEL, [t['function']['name'] for t in definitions])
                payload = context.attach_openai_tools({'model':MODEL, 'messages':assembled,
                    'max_completion_tokens':512, 'tool_choice':'none'}, definitions)
                wire = checked.converter_pedido(cfg, payload, prefixo=package.prefix, estado=adapter.EstadoClaude())
                wire.pop('output_config', None)
                wire['thinking'] = {'type':'disabled'}
                context.verify_native_tools(wire, snapshot)
                if wire['max_tokens'] != 512 or wire['tool_choice'] != {'type':'none'}:
                    raise SmokeBlocked('offline_wire_settings_mismatch')
                path = directory/f'wire_{index}_PUBLIC_MEMORY.json'
                _store(path, wire)
                result['requests'].append({'file':path.name,
                    'file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                    'production_count_cache_key':hashlib.sha256(json.dumps(wire, sort_keys=True, ensure_ascii=False).encode()).hexdigest()})
            for module in [motors, adapter, context, packages, messages]+providers:
                path = Path(module.__file__)
                result['source_sha256'][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
            _store(directory/'preflight.json', result)
            return {'status':result['status'], 'directory':str(directory), 'network_calls':0,
                    'generation_calls':0, 'real_account_reads':0, 'provider_token_count':None}
    finally:
        sys.path[:] = old_path
        sys.dont_write_bytecode = old_bytecode


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--prepare-wire',action='store_true',help='Build local public wires offline; never count or send')
    args=parser.parse_args()
    if args.prepare_wire and not args.execute:
        try:
            result = prepare_wire()
        except Exception:
            print(json.dumps({'status':'OFFLINE_PREPARATION_FAILED', 'generation_calls':0,
                              'error':'Local validation failed; no provider request or credential access requested.'}))
            return 3
        print(json.dumps(result, ensure_ascii=False))
        return 0
    print(json.dumps({'status':'BLOCKED_EXECUTION_BRIDGE_REQUIRED' if args.execute else 'DRY_RUN',
        'network_calls':0,'generation_calls':0,'real_account_reads':0,
        'questions':QUESTIONS,'model':MODEL,'tools':7,'tool_choice':'none',
        'max_output':512,'cache_ttl':'5m','max_retries':0,
        'per_call_usd':str(PER_CALL),'total_usd':str(TOTAL),'max_reservations':2,
        'blocker':'External execution unsafe with live ledger concurrency. No execution hook installed. Prefer reviewed free preflight then separately authorized UI; UI-specific smoke caps remain unverified.'},ensure_ascii=False))
    return 2 if args.execute else 0


if __name__=='__main__':
    raise SystemExit(main())
