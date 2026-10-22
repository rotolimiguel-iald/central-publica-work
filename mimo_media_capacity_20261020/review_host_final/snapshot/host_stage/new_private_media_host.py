"""Host glue only: no environment loading, remote calls or eager storage writes."""
import copy
from functools import wraps
import hashlib
import hmac
import math
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
import re
import threading

from private_media_store import (Scope, PrivateMediaStore, PrivateMediaRuntime,
    MediaError, MediaUnavailable, contains_refs, client_capabilities, MAX_RAW_BYTES)

CONVERSATION = re.compile(r'[A-Za-z0-9_-]{1,64}')
PUBLIC_BUDGET_REFUSAL = 'Anexo excede o contexto, bytes ou orçamento disponíveis; núcleo e histórico preservados. Para vídeo longo, escolha política compatível ou segmente explicitamente. Nada foi enviado.'
PUBLIC_REFERENCE_REFUSAL = 'Não foi possível validar o anexo nesta conta e conversa. Nada foi enviado.'


def has_private_or_typed_media(messages):
    return any(isinstance(m, dict) and isinstance(m.get('content'), list) and
               any(isinstance(p, dict) and p.get('type') in ('iald_media', 'input_audio', 'video_url')
                   for p in m['content']) for m in (messages or []))


def video_proposals(metadata):
    """Explicit full-duration policies; JEV selects, never a silent frame cap."""
    durations = [item['duration_seconds'] for item in metadata if item['kind'] == 'video']
    if not durations:
        return {'standard': {'fps': 2., 'media_resolution': 'default'},
                'detail': {'fps': 2., 'media_resolution': 'max'}}
    if any(type(value) not in (int, float) or not math.isfinite(value) or value <= 0 for value in durations):
        raise MediaError('Invalid measured video duration')
    duration = max(durations)
    if duration > 20480:
        raise MediaError('Video requires explicit segmentation beyond 20480 seconds')
    choices = {}
    candidates = [(str(fps), fps) for fps in (.1, .5, 1., 2., 5., 10.)]
    fitted = min(10., math.nextafter(2048. / duration, 0.))
    if fitted >= .1:
        candidates.append(('duration_fit', fitted))
    for name, fps in candidates:
        frames = int((Decimal(str(duration)) * Decimal(str(fps))).to_integral_value(rounding=ROUND_CEILING))
        if frames > 2048:
            continue
        choices['fps_' + name] = dict(fps=fps, media_resolution='default')
        choices['detail_fps_' + name] = dict(fps=fps, media_resolution='max')
    if not choices:
        raise MediaError('No full-duration video policy; explicit segmentation required')
    return choices


class Host:
    def __init__(self, root, *, generation, users, allowed, app_memory, dispatch_guard,
                 budget_available, rates, validate_upload, store_factory=PrivateMediaStore):
        self.root = Path(root) / '.iald_runtime' / 'private_media'
        self.generation = generation
        self.users = users
        self.allowed = allowed
        self.memory = app_memory
        self.dispatch_guard = dispatch_guard
        self.budget_available = budget_available
        self.rates = dict(input=rates[0], cache_read=rates[1], output=rates[2])
        self.validate_upload = validate_upload
        self.factory = store_factory
        self._instance = None
        self._lock = threading.RLock()
        self.admitted_task = None  # injected host callback, captured before thread dispatch

    def _live_scope(self, scope):
        # Provider threads have no Flask context. Identity/generation validation
        # is explicit, not a captured cookie or inherited ContextVar.
        return (isinstance(scope, Scope) and isinstance(scope.conversation, str)
                and CONVERSATION.fullmatch(scope.conversation) is not None
                and self.allowed(self.users().get(scope.owner, {}), scope.owner)
                and scope.generation == self.generation(scope.owner))

    def scope(self, user, conversation):
        if not user or not self.allowed(self.users().get(user, {}), user):
            raise MediaUnavailable('Account unavailable')
        if not isinstance(conversation, str) or CONVERSATION.fullmatch(conversation) is None:
            raise MediaUnavailable('Conversation namespace required')
        return Scope(user, self.generation(user), conversation)

    @property
    def store(self):
        with self._lock:
            if self._instance is None:
                self._instance = self.factory(self.root, authorize_scope=self._live_scope,
                                              validate_media=self.validate_upload)
            return self._instance

    # Route adapter gets this lazy facade, not an eagerly opened database.
    def put(self, *args, **kwargs):
        return self.store.put(*args, **kwargs)

    def metadata(self, *args, **kwargs):
        return self.store.metadata(*args, **kwargs)

    def capabilities(self, user, conversation='capabilities'):
        return client_capabilities(self.scope(user, conversation))

    def runtime(self, user, messages, conversation, *, automatic):
        if not has_private_or_typed_media(messages):
            return None
        scope = self.scope(user, conversation)
        binding = self.memory.current()
        expected = 'app_' + hashlib.sha256((scope.generation + ':' + conversation).encode('utf-8')).hexdigest()
        if (binding is None or binding.scope != {'house': 'IALD_APP', 'principal': scope.generation}
                or binding.context_id != expected):
            raise MediaUnavailable('Authenticated activity binding mismatch')
        generation = scope.generation
        guard = self.dispatch_guard(user, 'mimo', automatic)
        task = self.admitted_task() if self.admitted_task is not None else None
        if task is not None and (task.owner != generation or task.user != user or task.closed or task.refs < 1):
            raise MediaUnavailable('Admitted task owner or lifecycle mismatch')

        def authorized():
            if self.generation(user) != generation:
                raise MediaUnavailable('Account generation changed')
            result = guard()
            if result is False:
                raise MediaUnavailable('Dispatch authorization denied')
            record = self.users().get(user, {})
            if task is not None:
                if task.closed or task.refs < 1:
                    raise MediaUnavailable('Admitted task is closed')
                # Existing ledger/spending guards still reserve each provider
                # call against global caps. Never re-admit user balance here.
            elif not self.budget_available(record, user, 'mimo'):
                raise MediaError('Existing spending admission unavailable')
            return True  # Existing dispatch callbacks may return None on success.

        return PrivateMediaRuntime(self.store, scope, authorize_dispatch=authorized, rates=self.rates)

    def revoke_conversation(self, user, conversation):
        return self.store.revoke_conversation(self.scope(user, conversation))

    def revoke_account(self, user):
        # The caller must already have passed the existing deletion entrypoint.
        scope = self.scope(user, 'account_delete')
        return self.store.revoke_account(scope, authorize_account_deletion=lambda owner, gen:
                                        owner == user and gen == self.generation(user))


def register(app, host, *, authenticated_user, binary_origin_ok, json_guard):
    """Register private upload and fail-before-delete hooks; never parse binary JSON."""
    from flask import request, jsonify
    from private_media_routes import register_private_media

    def auth():
        return bool(authenticated_user()) and binary_origin_ok() is True

    def route_scope(conversation):
        scope = host.scope(authenticated_user(), conversation)
        if request.method in ('POST', 'GET'):
            # This is captured client partition identity, NOT authentication.
            # Cookie/bearer authorization is already checked independently.
            expected = request.args.get('expected_media_scope', '')
            actual = client_capabilities(scope)['media_scope']
            if (not isinstance(expected, str) or re.fullmatch(r'[0-9a-f]{32}', expected) is None
                    or not hmac.compare_digest(expected, actual)):
                raise MediaUnavailable('Upload account partition changed')
        return scope

    result = register_private_media(app, host,
        host_scope=route_scope,
        authenticate_csrf=auth,
        upload_eligible=lambda scope: host.allowed(host.users().get(scope.owner, {}), scope.owner))

    def wrap_delete(endpoint, account=False):
        original = app.view_functions.get(endpoint)
        if original is None:
            raise RuntimeError('Required deletion route missing')

        @wraps(original)
        def deletion(*args, **kwargs):
            user = authenticated_user()
            if not user:
                return jsonify(error='Authentication required'), 401
            data, error = json_guard({'confirmar'} if account else set())
            if error is not None:
                return error
            if account:
                if data.get('confirmar') != 'EXCLUIR':
                    return jsonify(error='Confirmação ausente.'), 400
                record = host.users().get(user)
                if not record:
                    return jsonify(error='Conta não encontrada.'), 404
                if record.get('admin'):
                    return jsonify(error='Use o painel para conta de operador.'), 403
            try:
                if account:
                    host.revoke_account(user)
                else:
                    host.revoke_conversation(user, kwargs.get('conversation'))
            except (MediaError, PermissionError, ValueError, OSError, RuntimeError):
                return jsonify(error='Não foi possível excluir os anexos. Exclusão da conta/conversa não executada.'), 503
            return original(*args, **kwargs)
        app.view_functions[endpoint] = deletion

    wrap_delete('api_conta_excluir', account=True)
    wrap_delete('chat_jobs_delete_conversation')
    return result
