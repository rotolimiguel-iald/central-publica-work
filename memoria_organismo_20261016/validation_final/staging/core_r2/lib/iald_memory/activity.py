"""Trusted-server activity lifecycle over the existing ACOM store/controller.

No authentication, providers, semantic acceptance or external retry lives here.
The embedding server authenticates scope, actor, commands and operation IDs.
Tickets are compared to durable server records; they are NOT bearer credentials.
All results remain candidates, including results rejected as stale.
"""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import uuid

from . import guard
from .store import ProjectionOverflow, RevisionConflict
from .mission import MissionController, is_mission_record, identifier, digest, encoded, evidence_pin

PROTOCOL = 'iald-activity/v1'
KEY = 'iald_activity_v1'


class ActivityError(ValueError):
    def __init__(self, code, **details):
        self.code, self.details = code, details
        super().__init__(code)


def _need(condition, code, **details):
    if not condition:
        raise ActivityError(code, **details)


class ActivityRuntime:
    """Bind only to a context already authenticated/created by its owner.

    actor is a trusted local agent representing that server, never model input.
    Artifacts are immutable JSON below store.root; callers cannot choose paths.
    A per-request requirement is bookkeeping, not a scientific decomposition.
    """

    def __init__(self, store, context_id, scope, actor):
        _need(isinstance(actor, dict) and set(actor) == {'id', 'kind'}
              and actor['kind'] == 'agent', 'trusted_server_actor_required')
        identifier(actor['id'])
        self.store, self.context_id = store, context_id
        self.scope, self.actor = deepcopy(scope), deepcopy(actor)
        self.controller = MissionController(store, context_id, self.scope)
        snapshot = self._get()  # Existing context; never adopt another/latest.
        self.anchor = snapshot['anchor_sha256']
        self.artifacts = Path(store.root) / 'activity_artifacts'

    def _get(self):
        return self.store.get(self.context_id, self.scope)

    def _artifact(self, value, *, persist=True):
        # The envelope isolates accounts even when their payload bytes coincide.
        raw = (encoded({'context_id': self.context_id, 'scope': self.scope,
                        'payload': value}) + '\n').encode('utf-8')
        guard.assert_clean_text(raw.decode('utf-8'), 'activity.artifact')
        sha = hashlib.sha256(raw).hexdigest()
        if persist:
            self.artifacts.mkdir(parents=True, exist_ok=True)
        path = self.artifacts / (sha + '.json')
        _need(persist or path.exists(), 'artifact_missing')
        if not path.exists():
            temp = path.with_name('.tmp_' + uuid.uuid4().hex)
            try:
                with temp.open('xb') as out:
                    out.write(raw)
                    out.flush()
                    os.fsync(out.fileno())
                # Windows rename refuses an existing destination. Unix hardlink
                # provides the same no-replace publication after fsync.
                try:
                    if os.name == 'nt':
                        os.rename(temp, path)
                    else:
                        os.link(temp, path)
                except FileExistsError:
                    pass
            finally:
                temp.unlink(missing_ok=True)
        _need(path.read_bytes() == raw, 'artifact_bytes_mismatch')
        return {'path': str(path.resolve()), 'sha256': sha}

    @staticmethod
    def _record(snapshot, record_id):
        return next((r for r in snapshot['q']['records'] if r['id'] == record_id), None)

    @staticmethod
    def _ids(request_id):
        identifier(request_id)
        key = digest(request_id)
        return {'task': 'req_' + key, 'request': 'activity_request_' + key,
                'steering': 'activity_command_' + key, 'handle': 'activity_' + key}

    @staticmethod
    def _operation(request_id, operation_id):
        identifier(operation_id)
        return 'activity_op_' + digest([request_id, operation_id])

    def _metadata_record(self, record_id, kind, data, *, candidate=False):
        artifact = self._artifact({'protocol': PROTOCOL, 'kind': kind, 'data': data})
        return {'id': record_id, 'kind': 'candidate' if candidate else 'fact',
                'statute': 'DECLARADO' if candidate else 'REAL',
                'text': encoded(data), 'sources': [dict(kind='artifact', ref=artifact['path'],
                                                       sha256=artifact['sha256'])],
                'meta': {KEY: {'kind': kind, 'data': data}}}

    def _data(self, record, expected_kind, *, check_admission=True):
        _need(record is not None, 'server_record_missing')
        meta = record.get('meta', {}).get(KEY, {})
        _need(meta.get('kind') == expected_kind, 'server_record_type_mismatch')
        expected = self._artifact({'protocol': PROTOCOL, 'kind': expected_kind,
                                  'data': meta['data']}, persist=False)
        _need(record['sources'] == [dict(kind='artifact', ref=expected['path'],
                                       sha256=expected['sha256'])]
              and record['text'] == encoded(meta['data']), 'server_record_mismatch')
        if expected_kind == 'request' and check_admission:
            evidence_pin(meta['data']['source'])
        return meta['data']

    @staticmethod
    def _steering(snapshot):
        # Sources/record kinds are accepted ONLY from authenticated server code.
        # Store forbids a model/executor-origin decision/erratum. A public tool
        # must never expose arbitrary records or this runtime as write authority.
        records = [r for r in snapshot['q']['records']
                   if ((r['kind'] in {'decision', 'erratum'} and r['statute'] == 'INPUT')
                       or (r['kind'] == 'pending' and r['statute'] in {'INPUT', 'OPEN'}))
                   and any(s['kind'] == 'operator' for s in r['sources'])]
        return digest({'anchor': snapshot['anchor_sha256'],
                       'constraints': snapshot['constraints'], 'steering': records})

    def _mission(self, snapshot):
        return self.controller.project_snapshot(snapshot, max_chars=2000000)

    def _action(self, operation, snapshot, event_id, **fields):
        request = dict(operation=operation, actor=self.actor, event_id=event_id,
                       expected_revision=snapshot['revision'], **fields)
        if operation != 'configure':
            request['projection_sha256'] = self._mission(snapshot)['projection_sha256']
        return self.controller.action(request)

    def _ticket(self, core, snapshot):
        return dict(core, revision=snapshot['revision'],
                    state_sha256=snapshot['receipt']['state_sha256'],
                    projection_sha256=self._mission(snapshot)['projection_sha256'])

    def _validate(self, ticket, snapshot, *, refresh=False):
        _need(isinstance(ticket, dict), 'invalid_ticket')
        ids = self._ids(ticket.get('request_id'))
        core = self._data(self._record(snapshot, ids['request']), 'request')
        _need(set(ticket) == set(core) | {'revision', 'state_sha256', 'projection_sha256'}
              and all(ticket.get(k) == v for k, v in core.items()), 'ticket_server_binding_mismatch')
        _need(core['actor'] == self.actor and core['scope'] == self.scope
              and core['context_id'] == self.context_id and core['anchor_sha256'] == self.anchor,
              'ticket_scope_or_actor_mismatch')
        _need(core['steering_sha256'] == self._steering(snapshot), 'steering_changed')
        mission = self._mission(snapshot)
        rows = mission['projection']['active'] + mission['projection']['settled']
        task = next(t for t in rows if t['id'] == core['task_id'])
        _need(task['epoch'] == core['epoch'], 'task_epoch_changed')
        if snapshot['revision'] != ticket['revision']:
            _need(refresh, 'revision_changed_explicit_refresh_required')
        else:
            _need(ticket['projection_sha256'] == mission['projection_sha256']
                  and ticket['state_sha256'] == snapshot['receipt']['state_sha256'],
                  'ticket_projection_mismatch')
        self.controller.check_snapshot(dict(actor=self.actor, task_id=core['task_id'],
            lease_id=core['lease_id'], expected_revision=snapshot['revision'],
            projection_sha256=mission['projection_sha256']), snapshot)
        return core

    def begin(self, request_id, command, criterion=None, *, origin, origin_ref=None,
              lease_seconds=43200):
        """Admit an authenticated command; identical retry only recovers its ticket.

        Caller supplies server-owned request_id. It MUST NOT use a client ticket
        as authorization. Partial local setup is safely resumable by same payload.
        """
        ids = self._ids(request_id)
        _need(origin in {'authenticated_operator', 'delegated', 'system'}, 'invalid_origin')
        _need(origin == 'authenticated_operator' or
              (isinstance(origin_ref, str) and bool(origin_ref)), 'delegation_reference_required')
        _need(isinstance(command, str) and bool(command), 'command_required')
        criterion = criterion or ('Processar o comando inscrito ' + request_id +
            ' sob o escopo vigente, preservando pendências; entregar candidato verificável para revisão.')
        _need(isinstance(criterion, str) and 0 < len(criterion) <= 6000, 'invalid_criterion')
        admission = {'request_id': request_id, 'command': command, 'criterion': criterion,
                     'origin': origin, 'origin_ref': origin_ref}
        payload_hash = digest(admission)
        source = self._artifact(admission)
        snapshot = self._get()
        existing = self._record(snapshot, ids['request'])
        if existing:
            core = self._data(existing, 'request')
            _need(core['payload_sha256'] == payload_hash, 'request_payload_conflict')
            _need(core['actor'] == self.actor, 'request_actor_conflict')
            # This is recovery, never permission to dispatch an existing intent.
            return dict(ticket=self._ticket(core, snapshot), replayed=True,
                        recovery=self.recover(request_id))
        steering = self._record(snapshot, ids['steering'])
        human = origin == 'authenticated_operator'
        expected = {'id': ids['steering'], 'kind': 'decision' if human else 'fact', 'statute': 'INPUT',
            'text': command, 'sources': [dict(kind='operator' if human else 'tool',
                                            ref=source['path'], sha256=source['sha256'])]}
        if steering:
            _need(steering == expected, 'request_payload_conflict')
        else:
            self.store.transition(self.context_id, self.scope, snapshot['revision'],
                ids['steering'], self.actor, {'records': [expected]})
        snapshot = self._get()
        _, state, _ = self.controller.load_snapshot(snapshot)
        requirement = {'id': ids['task'], 'criterion': criterion, 'depends_on': []}
        if state is None:
            self._action('configure', snapshot, 'activity_config_' + digest(request_id),
                         requirements=[requirement], sources=[source])
        elif ids['task'] not in state['tasks']:
            self._action('extend', snapshot, 'activity_extend_' + digest(request_id),
                         requirements=[requirement], sources=[source], reason='Authenticated command admission')
        else:
            _need(state['tasks'][ids['task']]['criterion'] == criterion, 'request_payload_conflict')
        snapshot = self._get()
        _, state, _ = self.controller.load_snapshot(snapshot)
        task = state['tasks'][ids['task']]
        if task['status'] == 'open':
            self._action('claim', snapshot, 'activity_claim_' + digest(request_id),
                         task_id=ids['task'], lease_seconds=lease_seconds)
        snapshot = self._get()
        _, state, _ = self.controller.load_snapshot(snapshot)
        task = state['tasks'][ids['task']]
        _need(task['status'] == 'working' and task['lease']['owner'] == self.actor['id'],
              'request_not_owned')
        if human:
            last_command = [r for r in snapshot['q']['records']
                            if r['kind'] in {'decision', 'erratum'} and r['statute'] == 'INPUT'
                            and any(s['kind'] == 'operator' for s in r['sources'])][-1]
            _need(last_command['id'] == ids['steering'], 'newer_command_requires_reconciliation')
        core = {'protocol': PROTOCOL, 'context_id': self.context_id, 'scope': self.scope,
            'anchor_sha256': snapshot['anchor_sha256'], 'actor': self.actor,
            'request_id': request_id, 'task_id': ids['task'], 'epoch': task['epoch'],
            'lease_id': task['lease']['id'], 'steering_sha256': self._steering(snapshot),
            'payload_sha256': payload_hash, 'source': source,
            'origin': origin, 'origin_ref': origin_ref}
        record = self._metadata_record(ids['request'], 'request', core)
        self.store.transition(self.context_id, self.scope, snapshot['revision'],
            ids['request'], self.actor, {'records': [record], 'flow': {'handles': [{
                'id': ids['handle'], 'kind': 'activity_request', 'request_id': request_id,
                'task_id': ids['task'], 'status': 'prepared', 'no_repeat': True}]}})
        return {'ticket': self._ticket(core, self._get()), 'replayed': False}

    def preflight(self, ticket, operation_id, *, refresh=False):
        """Validate, then durably claim an operation intent exactly once.

        A crash after this call makes external dispatch uncertain; recover, never
        repeat. Each routing/provider/tool action needs its own server-owned ID.
        """
        snapshot = self._get()
        core = self._validate(ticket, snapshot, refresh=refresh)
        op = self._operation(core['request_id'], operation_id)
        _need(self._record(snapshot, op) is None, 'operation_already_started', operation_id=operation_id)
        data = {'request_id': core['request_id'], 'operation_id': operation_id,
                'task_id': core['task_id'], 'epoch': core['epoch'],
                'steering_sha256': core['steering_sha256'], 'ticket_sha256': digest(core)}
        record = self._metadata_record(op, 'intent', data)
        receipt = self.store.transition(self.context_id, self.scope, snapshot['revision'], op,
            self.actor, {'records': [record], 'flow': {'handles': [{
                'id': op, 'kind': 'activity_operation', 'request_id': core['request_id'],
                'operation_id': operation_id, 'task_id': core['task_id'],
                'status': 'dispatching', 'no_repeat': True}]}})
        _need(not receipt.get('replayed'), 'operation_already_started', operation_id=operation_id)
        now = self._get()
        try:
            _need(now['revision'] == receipt['revision'] or refresh,
                  'revision_changed_explicit_refresh_required')
            current_ticket = self._ticket(core, now)
            self._validate(current_ticket, now)
        except Exception as exc:
            raise ActivityError('preflight_changed_after_intent', intent_record_id=op,
                                cause=getattr(exc, 'code', str(exc))) from exc
        return {'ticket': current_ticket, 'operation_id': operation_id,
                'intent_record_id': op, 'dispatch_allowed_once': True}

    def refresh(self, ticket):
        """Explicit mechanical revision refresh; steering/epoch/lease still checked."""
        snapshot = self._get()
        core = self._validate(ticket, snapshot, refresh=True)
        return self._ticket(core, snapshot)

    def _finish_request(self, core, snapshot):
        """Reconcile a crash after submit without reopening any external intent."""
        handle_id = self._ids(core['request_id'])['handle']
        own_ops = [h for h in snapshot['p']['handles']
                   if h.get('request_id') == core['request_id'] and h.get('kind') == 'activity_operation']
        _need(all(h.get('status') == 'completed' for h in own_ops), 'other_operations_unresolved')
        handle = next(h for h in snapshot['p']['handles'] if h['id'] == handle_id)
        if handle['status'] != 'completed':
            self.store.transition(self.context_id, self.scope, snapshot['revision'],
                'activity_finished_' + digest(core['request_id']), self.actor,
                {'flow': {'handles': [{'id': handle_id, 'status': 'completed', 'no_repeat': True}]}})
        return self._get()

    def complete(self, ticket, operation_id, result, *, terminal=True, refresh=False):
        """Persist a returned candidate before freshness checks; never auto-accept.

        terminal=False records an intermediate routing/tool/provider result only.
        A stale return raises ActivityError with candidate_record_id after durable
        inscription. Retrying this method is local reconciliation, never a resend.
        """
        _need(type(terminal) is bool, 'terminal_must_be_boolean')
        snapshot = self._get()
        ids = self._ids(ticket.get('request_id'))
        # Preserve an authenticated intent's return even if its admission source
        # has since broken. The later validator still refuses that broken pin.
        core = self._data(self._record(snapshot, ids['request']), 'request', check_admission=False)
        _need(core['actor'] == self.actor and all(ticket.get(k) == v for k, v in core.items()),
              'ticket_server_binding_mismatch')
        op = self._operation(core['request_id'], operation_id)
        intent = self._data(self._record(snapshot, op), 'intent')
        _need(intent['ticket_sha256'] == digest(core), 'operation_ticket_mismatch')
        # Full result remains a model candidate; its surrounding receipt is not
        # scientific verification. No model-controlled paths/actor are consumed.
        data = {'request_id': core['request_id'], 'operation_id': operation_id,
                'result': result, 'terminal': terminal}
        rid = 'activity_result_' + digest(data)
        record = self._metadata_record(rid, 'result', data, candidate=True)
        # Retry only local custody CAS, never a remote call or integration. Even
        # an exhausted CAS retains the immutable result file and reports its pin.
        for _ in range(8):
            existing = self._record(snapshot, rid)
            previous = [r for r in snapshot['q']['records']
                if r.get('meta', {}).get(KEY, {}).get('kind') == 'result'
                and r['meta'][KEY]['data']['request_id'] == core['request_id']
                and r['meta'][KEY]['data']['operation_id'] == operation_id]
            if existing:
                _need(self._data(existing, 'result') == data, 'server_record_mismatch')
                custody_revision = snapshot['revision']
                break
            changes = {'records': [record]}
            if not previous:
                changes['flow'] = {'handles': [{'id': op, 'status': 'completed',
                    'result_record_id': rid, 'no_repeat': True}]}
            try:
                receipt = self.store.transition(self.context_id, self.scope, snapshot['revision'],
                                                rid, self.actor, changes)
                custody_revision = receipt['revision']
                break
            except RevisionConflict:
                snapshot = self._get()
        else:
            raise ActivityError('candidate_custody_conflict', candidate_record_id=rid,
                                artifact=record['sources'][0], retry='LOCAL_CUSTODY_ONLY')
        _need(not previous or all(r['id'] == rid for r in previous),
              'result_identity_conflict', candidate_record_id=rid)
        # Validate against the revision BEFORE our own result append. The append
        # is mechanical and CAS protected; a later race is checked again below.
        try:
            self._validate(ticket, snapshot, refresh=refresh)
        except Exception as exc:
            # A successful submit replay is recovery of known integration.
            now = self._get()
            _, state, _ = self.controller.load_snapshot(now)
            task = state['tasks'][core['task_id']]
            result_pin = {'path': record['sources'][0]['ref'], 'sha256': record['sources'][0]['sha256']}
            if (existing and terminal and task['status'] in {'review_pending', 'satisfied'}
                    and task['evidence'] == [result_pin]
                    and task['epoch'] == core['epoch']
                    and core['steering_sha256'] == self._steering(now)):
                now = self._finish_request(core, now)
                return {'candidate_record_id': rid, 'replayed': True, 'integrated': True,
                        'accepted': False, 'receipt': now['receipt']}
            raise ActivityError('stale_result_preserved', candidate_record_id=rid,
                                cause=getattr(exc, 'code', str(exc))) from exc
        now = self._get()
        try:
            _need(now['revision'] == custody_revision or refresh,
                  'revision_changed_explicit_refresh_required')
            refreshed = self._ticket(core, now)
            self._validate(refreshed, now)
        except Exception as exc:
            raise ActivityError('stale_result_preserved', candidate_record_id=rid,
                                cause=getattr(exc, 'code', str(exc))) from exc
        if terminal:
            own_ops = [h for h in now['p']['handles'] if h.get('request_id') == core['request_id']
                       and h.get('kind') == 'activity_operation']
            _need(all(h.get('status') == 'completed' for h in own_ops),
                  'other_operations_unresolved', candidate_record_id=rid)
            # Submission is semantic review-pending, never satisfaction.
            result_pin = {'path': record['sources'][0]['ref'], 'sha256': record['sources'][0]['sha256']}
            self._action('submit', now, 'activity_submit_' + digest(core['request_id']),
                         task_id=core['task_id'], lease_id=core['lease_id'], evidence=[result_pin],
                         note='Candidate returned; semantic review remains required.')
            self._finish_request(core, self._get())
        now = self._get()
        return {'candidate_record_id': rid, 'replayed': bool(existing),
                'integrated': True, 'accepted': False, 'terminal': terminal,
                'ticket': self._ticket(core, now), 'receipt': now['receipt']}

    def mark_uncertain(self, ticket, operation_id, reason):
        """Record interruption without pretending that the external call failed."""
        snapshot = self._get()
        core = self._data(self._record(snapshot, self._ids(ticket['request_id'])['request']), 'request')
        _need(core['actor'] == self.actor and all(ticket.get(k) == v for k, v in core.items()),
              'ticket_server_binding_mismatch')
        op = self._operation(core['request_id'], operation_id)
        self._data(self._record(snapshot, op), 'intent')
        handle = next(h for h in snapshot['p']['handles'] if h['id'] == op)
        _need(handle['status'] in {'dispatching', 'uncertain'}, 'operation_already_returned')
        data = {'request_id': core['request_id'], 'operation_id': operation_id, 'reason': reason}
        rid = 'activity_uncertain_' + digest(data)
        if self._record(snapshot, rid):
            return snapshot['receipt']
        record = self._metadata_record(rid, 'uncertain', data)
        return self.store.transition(self.context_id, self.scope, snapshot['revision'], rid,
            self.actor, {'records': [record], 'flow': {'handles': [{'id': op, 'status': 'uncertain',
                'no_repeat': True}]}})

    def recover(self, request_id):
        """Return current server state. Never dispatch, refresh or integrate work."""
        ids = self._ids(request_id)
        snapshot = self._get()
        row = self._record(snapshot, ids['request'])
        core = self._data(row, 'request') if row else None
        records = [r for r in snapshot['q']['records']
                   if r.get('meta', {}).get(KEY, {}).get('data', {}).get('request_id') == request_id]
        return {'request_id': request_id, 'ticket': self._ticket(core, snapshot) if core else None,
                'records': deepcopy(records), 'handles': [deepcopy(h) for h in snapshot['p']['handles']
                    if h.get('request_id') == request_id], 'receipt': snapshot['receipt'],
                'automatic_retry': False, 'authority': 'SERVER_SCOPED_DATA_NOT_AUTHENTICATION'}

    def _terminal_projection_index(self, snapshot, mission):
        """Index exact completed execution receipts, never semantic satisfaction.

        Every artifact and link is checked against this snapshot. Unknown shapes,
        corrections, active/uncertain operations and conflicting handles stay in
        full. A broken recognized pin raises visibly. Returned model content is
        still an ordinary candidate; it is not converted to an approved fact.
        """
        records = snapshot['q']['records']
        by_id = {r['id']: r for r in records}
        protected = {r['supersedes'] for r in records if r.get('supersedes')}
        groups, handles = {}, {}
        for record in records:
            meta = record.get('meta', {}).get(KEY)
            if isinstance(meta, dict) and isinstance(meta.get('data'), dict):
                rid = meta['data'].get('request_id')
                if isinstance(rid, str):
                    groups.setdefault(rid, []).append(record)
        for handle in snapshot['p']['handles']:
            handles.setdefault(handle.get('request_id'), []).append(handle)
        tasks = {t['id']: t for t in mission['projection']['active'] + mission['projection']['settled']}
        indexed, handle_ids, task_ids, rows = set(), set(), set(), []

        def exact_record(record, kind):
            return (set(record) == {'id', 'kind', 'statute', 'text', 'sources', 'meta'}
                and record['id'] not in protected
                and set(record['meta']) == {KEY}
                and set(record['meta'][KEY]) == {'kind', 'data'}
                and record['meta'][KEY]['kind'] == kind
                and record['kind'] == ('candidate' if kind == 'result' else 'fact')
                and record['statute'] == ('DECLARADO' if kind == 'result' else 'REAL'))

        request_fields = {'protocol', 'context_id', 'scope', 'anchor_sha256', 'actor',
            'request_id', 'task_id', 'epoch', 'lease_id', 'steering_sha256',
            'payload_sha256', 'source', 'origin', 'origin_ref'}
        intent_fields = {'request_id', 'operation_id', 'task_id', 'epoch',
                         'steering_sha256', 'ticket_sha256'}
        handle_fields = {'id', 'kind', 'request_id', 'task_id', 'status', 'no_repeat'}
        for request_id, group in groups.items():
            ids = self._ids(request_id)
            request = by_id.get(ids['request'])
            if request is None or not exact_record(request, 'request'):
                continue
            core = self._data(request, 'request')
            if (set(core) != request_fields or core['protocol'] != PROTOCOL
                    or core['context_id'] != self.context_id or core['scope'] != self.scope
                    or core['anchor_sha256'] != snapshot['anchor_sha256']
                    or core['request_id'] != request_id or core['task_id'] != ids['task']):
                continue
            task = tasks.get(core['task_id'])
            if (not task or task['status'] not in {'review_pending', 'satisfied'}
                    or task['epoch'] != core['epoch'] or task['lease'] is not None
                    or task['submitted_by'] != core['actor'].get('id')):
                continue
            if task['status'] == 'satisfied' and (not task['reviewed_by']
                    or task['reviewed_by'] == task['submitted_by']):
                continue
            # _data checks the source pin. Reconstructing the admission envelope
            # also checks context/scope, payload and the literal command record.
            admission = json.loads(Path(core['source']['path']).read_bytes())['payload']
            if (set(admission) != {'request_id', 'command', 'criterion', 'origin', 'origin_ref'}
                    or digest(admission) != core['payload_sha256']
                    or admission['request_id'] != request_id
                    or admission['criterion'] != task['criterion']
                    or admission['origin'] != core['origin']
                    or admission['origin_ref'] != core['origin_ref']
                    or self._artifact(admission, persist=False) != core['source']):
                continue
            human = core['origin'] == 'authenticated_operator'
            steering = {'id': ids['steering'], 'kind': 'decision' if human else 'fact',
                'statute': 'INPUT', 'text': admission['command'], 'sources': [dict(
                    kind='operator' if human else 'tool', ref=core['source']['path'],
                    sha256=core['source']['sha256'])]}
            if by_id.get(ids['steering']) != steering:
                continue
            # App/queue adapters may also keep their own handles. They retain
            # the controller's normal full/indexed representation; this index
            # validates and replaces only this runtime's exact handle kinds.
            own_handles = [h for h in handles.get(request_id, [])
                           if h.get('kind') in {'activity_request', 'activity_operation'}]
            hmap = {h['id']: h for h in own_handles}
            if len(hmap) != len(own_handles) or ids['handle'] not in hmap:
                continue
            request_handle = hmap[ids['handle']]
            if (set(request_handle) != handle_fields
                    or request_handle != dict(id=ids['handle'], kind='activity_request',
                        request_id=request_id, task_id=ids['task'], status='completed', no_repeat=True)):
                continue
            mechanical, results, intents = [request], {}, {}
            safe = True
            for record in group:
                if record is request:
                    continue
                kind = record['meta'][KEY]['kind']
                if kind not in {'intent', 'result'} or not exact_record(record, kind):
                    safe = False
                    break
                data = self._data(record, kind)
                expected_fields = intent_fields if kind == 'intent' else {
                    'request_id', 'operation_id', 'result', 'terminal'}
                if set(data) != expected_fields or data['request_id'] != request_id:
                    safe = False
                    break
                operation_id = data['operation_id']
                identifier(operation_id)
                target = intents if kind == 'intent' else results
                if operation_id in target:
                    safe = False
                    break
                target[operation_id] = (record, data)
            if not safe or not intents or set(intents) != set(results):
                continue
            terminal = []
            for operation_id, (record, data) in intents.items():
                op = self._operation(request_id, operation_id)
                result, returned = results[operation_id]
                expected_intent = dict(request_id=request_id, operation_id=operation_id,
                    task_id=ids['task'], epoch=core['epoch'],
                    steering_sha256=core['steering_sha256'], ticket_sha256=digest(core))
                expected_handle = dict(id=op, kind='activity_operation', request_id=request_id,
                    operation_id=operation_id, task_id=ids['task'], status='completed',
                    result_record_id=result['id'], no_repeat=True)
                if (record['id'] != op or data != expected_intent
                        or type(returned['terminal']) is not bool
                        or result['id'] != 'activity_result_' + digest(returned)
                        or hmap.get(op) != expected_handle):
                    safe = False
                    break
                mechanical.append(record)
                if returned['terminal']:
                    terminal.append(result)
            if (not safe or len(terminal) != 1 or len(hmap) != len(intents) + 1
                    or task['evidence'] != [{'path': terminal[0]['sources'][0]['ref'],
                                             'sha256': terminal[0]['sources'][0]['sha256']}]):
                continue
            ordered = sorted(mechanical, key=lambda r: r['id'])
            indexed.update(r['id'] for r in ordered)
            handle_ids.update(hmap)
            task_ids.add(ids['task'])
            rows.append([request_id, sorted(intents), digest(ordered),
                         digest(sorted(own_handles, key=lambda h: h['id']))])
        return indexed, handle_ids, task_ids, {
            'columns': ['request_id', 'operation_ids', 'mechanical_records_sha256', 'handles_sha256'],
            'rows': sorted(rows, key=lambda r: r[0]),
            'record_kinds': ['request', 'intent'],
            'recovery': {'operation': 'recover', 'field': 'request_id',
                'context_id': self.context_id, 'revision': snapshot['revision'],
                'state_sha256': snapshot['receipt']['state_sha256'],
                'instruction': 'Current state only: compare revision/state hash. Filter records by indexed kinds, sort by id and verify digest; same for handles. Earlier state requires journal. Completed execution is not semantic acceptance.'}}

    def project(self, max_chars=24000, current_input=''):
        """One verified snapshot; compact mission overlay plus ACOM content API.

        text/required_chars/receipt/included/omitted fields remain compatible.
        projection_sha256 hashes this overlay; mission_projection_sha256 is the
        distinct full hash required by MissionController.check/action.
        """
        snapshot = self._get()
        mission = self._mission(snapshot)
        indexed, handle_ids, task_ids, execution_index = self._terminal_projection_index(snapshot, mission)
        overlay = deepcopy(mission['projection'])
        # Content records already appear in the generic projection. Only the
        # controller's validated machine lineage is replaced by its live index.
        overlay.pop('current_records', None)
        view = deepcopy(snapshot)
        view['q']['records'] = [r for r in view['q']['records']
                               if not is_mission_record(r) and r['id'] not in indexed]
        # The full p persists in the store; use controller's terminal handle index.
        view['p'] = deepcopy(mission['projection']['flow'])
        # Retain the structured API. Its wire representation references the
        # content's full objective/constraints/flow instead of serializing twice.
        wire = deepcopy(overlay)
        for key in ('objective', 'objective_sha256', 'constraints', 'flow', 'unresolved_handles'):
            wire.pop(key, None)
        wire['content_fields'] = {'objective': 'content.objective', 'constraints': 'content.constraints',
                                  'flow': 'content.flow', 'unresolved_handles': 'content.flow.handles'}
        wire['terminal_handles'] = [h for h in wire['terminal_handles'] if h['id'] not in handle_ids]
        wire['terminal_execution_index'] = execution_index
        wire['settled'] = [dict(id=t['id'], criterion=t['criterion'], depends_on=t['depends_on'],
            status=t['status'], epoch=t['epoch'], reviewed_by=t['reviewed_by'],
            note=t['note'], evidence=t['evidence'], review_evidence=t['review_evidence'],
            task_sha256=digest({k:v for k,v in t.items() if k != 'ready'}),
            recovery='mission.project current settled task; compare revision/state hash')
            if t['id'] in task_ids else t for t in wire['settled']]
        suffix = '\n<IALD_ACTIVITY_V1>\n' + encoded(wire) + '\n</IALD_ACTIVITY_V1>'
        _need(type(max_chars) is int and max_chars >= 256, 'invalid_projection_budget')
        budget = max_chars - len(suffix)
        try:
            content = self.store.project_snapshot(view, max_chars=max(256, budget), current_input=current_input)
        except ProjectionOverflow as exc:
            raise ProjectionOverflow(exc.required_chars + len(suffix), max_chars) from exc
        if content['required_chars'] + len(suffix) > max_chars:
            raise ProjectionOverflow(content['required_chars'] + len(suffix), max_chars)
        text = content['text'] + suffix
        guard.assert_clean_text(text, 'activity.project')
        return dict(content, text=text, required_chars=content['required_chars'] + len(suffix),
            actual_chars=len(text), projection_sha256=hashlib.sha256(text.encode('utf-8')).hexdigest(),
            mission_projection_sha256=mission['projection_sha256'], activity=overlay,
            terminal_execution_index=execution_index, indexed_record_ids=sorted(indexed),
            mission_record_ids=[r['id'] for r in snapshot['q']['records'] if is_mission_record(r)],
            receipt=deepcopy(snapshot['receipt']))
