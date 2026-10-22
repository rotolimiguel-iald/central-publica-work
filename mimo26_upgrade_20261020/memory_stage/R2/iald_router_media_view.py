"""Derived routing-only media view. No store creation, writes or network access.

Call routing_state(app_memory) at EVERY routing retrieval (including fit), then
prepare_body(body, app_memory.current()) before admission AND after final fit.
Executor app_memory.routing_state/project_messages remain unchanged.
"""
import base64
import binascii
import copy
import hashlib
import json
import re

SCHEMA = 'iald.router-media-view/v2'
URI = re.compile(r'data:((?:image|audio|video)/[A-Za-z0-9.+-]+);base64,([A-Za-z0-9+/=]+)', re.I)
MEDIA_START = re.compile(r'data:(?:image|audio|video)/', re.I)
FILE_BLOCK = re.compile(r'\[ARQUIVO:[^\n]*?\][\s\S]*?\[FIM\]')
PROV_START = '\n<IALD_ROUTER_MEDIA_VIEW_V1>\n'
PROV_END = '\n</IALD_ROUTER_MEDIA_VIEW_V1>'
ACOM_START = '<IALD_COMMON_MEMORY_V1>'
ACOM_END = '</IALD_COMMON_MEMORY_V1>'


class MediaViewError(ValueError):
    """Visible refusal without echoing source or payload bytes."""


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def _json_string(text):
    # Projections have a human preamble followed by a JSON object. Also handle
    # JSON strings containing JSON strings, without ever truncating required text.
    for offset in (0, text.find('\n{') + 1 if '\n{' in text else -1):
        if offset < 0:
            continue
        try:
            # raw_decode also preserves the closing operational-memory tag.
            obj, end = json.JSONDecoder().raw_decode(text, offset)
        except (ValueError, RecursionError):
            continue
        return text[:offset], obj, text[end:], text[offset:end]
    return None


def _walk(value, string_fn, path='$', media=None, depth=0):
    if depth > 48:
        raise MediaViewError('Media view nesting exceeds verified bound')
    if isinstance(value, dict):
        media = value.get('type', media)
        if media not in ('image', 'audio', 'video', 'image_url', 'input_audio', 'video_url'):
            media = None
        result = {}
        for key, item in value.items():
            new_key = string_fn(key, path + '.<key>', None)
            if new_key in result:
                raise MediaViewError('Media view key collision')
            hint = media if key in ('data', 'url', 'base64', 'image_url', 'input_audio', 'video_url') else None
            if key in ('image_url', 'input_audio', 'video_url'):
                hint = key
            result[new_key] = _walk(item, string_fn, path + '.' + key, hint, depth + 1)
        return result
    if isinstance(value, list):
        return [_walk(item, string_fn, path + '[' + str(i) + ']', media, depth + 1) for i, item in enumerate(value)]
    if isinstance(value, str):
        if media and re.fullmatch(r'[A-Za-z0-9+/]+={0,2}', value):
            # Even JSON-looking base64 (e.g. "1234" or "true") is an exact
            # payload in this typed transport field, not embedded JSON.
            return string_fn(value, path, media)
        parsed = _json_string(value)
        if parsed is not None:
            prefix, obj, suffix, original = parsed
            transformed = _walk(obj, string_fn, path + '::json', media, depth + 1)
            return (string_fn(prefix, path + '::prefix', None)
                    + (original if transformed == obj else encode(transformed))
                    + (_walk(suffix, string_fn, path + '::suffix', None, depth + 1) if suffix else ''))
        return string_fn(value, path, media)
    return value


class _View:
    def __init__(self, binding):
        if binding is None:
            raise MediaViewError('Authenticated memory binding required')
        self.binding = binding
        snapshot = binding.snapshot()
        self.receipt = copy.deepcopy(snapshot['receipt'])
        if snapshot['context_id'] != binding.context_id or snapshot['scope'] != binding.scope:
            raise MediaViewError('Memory scope mismatch')
        self.pointer = dict(context_id=binding.context_id, scope=copy.deepcopy(binding.scope),
                            revision=self.receipt['revision'], event_hash=self.receipt['event_hash'],
                            state_sha256=self.receipt['state_sha256'],
                            objective_sha256=snapshot['objective_sha256'])
        self.inventory = {}
        self.tokens = {}  # explicit complete URIs and complete attachment blocks ONLY
        self.typed_payloads = {}  # (media kind, exact value), never substring matching

        def collect(text, path, media):
            for block in FILE_BLOCK.finditer(text):
                raw = block.group(0).encode('utf-8')
                digest = hashlib.sha256(raw).hexdigest()
                item = self.inventory.setdefault(digest, dict(sha256=digest, media_type='attachment/extracted-text',
                                                              bytes=len(raw), count=0, locations=[]))
                item['count'] += 1
                item['locations'].append(dict(json_path_sha256=sha(path)))
                self.tokens[block.group(0)] = '[IALD_ATTACHMENT_CUSTODY:' + digest + ']'
            if '[ARQUIVO:' in FILE_BLOCK.sub('', text):
                raise MediaViewError('Incomplete attachment block in custody')
            matches = list(URI.finditer(text))
            for match in matches:
                self.register(match.group(0), match.group(2), match.group(1), path)
            if media and not matches and text and re.fullmatch(r'[A-Za-z0-9+/]+={0,2}', text):
                self.register(text, text, {'input_audio': 'audio/unknown', 'image_url': 'image/unknown',
                                          'video_url': 'video/unknown'}.get(media, media + '/unknown'), path)
            if MEDIA_START.search(URI.sub('', text)):
                raise MediaViewError('Unsupported media encoding in custody')
            return text
        _walk(snapshot, collect)

    def register(self, whole, payload, mime, path):
        try:
            raw = base64.b64decode(payload, validate=True)
        except (ValueError, binascii.Error):
            raise MediaViewError('Invalid media encoding in custody') from None
        if not raw:
            raise MediaViewError('Empty media payload in custody')
        digest = hashlib.sha256(raw).hexdigest()
        marker = '[IALD_MEDIA_CUSTODY:' + digest + ']'
        self.inventory.setdefault(digest, dict(sha256=digest, media_type=mime.lower(), bytes=len(raw),
                                               count=0, locations=[]))
        item = self.inventory[digest]
        item['count'] += 1
        item['locations'].append(dict(json_path_sha256=sha(path)))
        if whole != payload:
            self.tokens[whole] = marker
        self.typed_payloads[(mime.split('/', 1)[0].lower(), payload)] = marker

    def transform(self, value):
        def replace(text, path, media):
            if media:
                kind = {'image_url': 'image', 'input_audio': 'audio', 'video_url': 'video'}.get(media, media)
                exact = self.typed_payloads.get((kind, text))
                if exact is not None:
                    return exact
            def explicit(match):
                marker = self.tokens.get(match.group(0))
                if marker is None:
                    raise MediaViewError('Explicit attachment lacks same-scope custody')
                return marker
            text = FILE_BLOCK.sub(explicit, text)
            text = URI.sub(explicit, text)
            if MEDIA_START.search(text):
                raise MediaViewError('Media payload lacks same-scope custody')
            if '[ARQUIVO:' in text:
                raise MediaViewError('Attachment lacks same-scope custody')
            if media and text and not re.fullmatch(r'\[IALD_MEDIA_CUSTODY:[0-9a-f]{64}\]', text):
                raise MediaViewError('Unbound media payload')
            return text
        result = _walk(value, replace)
        # Include all JSON-encoded strings and keys in the postcondition.
        wire = encode(result)
        slash_normalized = re.sub(r'\\+/', '/', wire)
        if (MEDIA_START.search(slash_normalized) or '[ARQUIVO:' in wire
                or any(token in slash_normalized for token in self.tokens)):
            raise MediaViewError('Media bytes remain in routing view')
        return result

    def checked(self):
        now = self.binding.snapshot()['receipt']
        if any(now.get(k) != self.receipt.get(k) for k in ('context_id', 'revision', 'event_hash', 'state_sha256')):
            raise MediaViewError('Memory revision changed during media projection')

    def provenance(self):
        return dict(schema=SCHEMA, statute='DERIVED', custody_pointer=self.pointer,
                    media=list(self.inventory.values()), recovery='Authenticated ACOM get at same revision; journal replay for older revisions',
                    count_semantics='ledger_occurrences_not_unique_attachments',
                    authority='routing_view_not_full_state_or_permission')


def _source_packet(view, expected_sha, actual_chars):
    packet = view.binding.projection(max_chars=actual_chars)
    if (sha(packet['text']) != expected_sha or len(packet['text']) != actual_chars
            or any(packet['receipt'].get(k) != view.receipt.get(k)
                   for k in ('context_id', 'scope', 'revision', 'event_hash', 'state_sha256'))):
        raise MediaViewError('Projection source not recoverable at bound revision')
    return packet


def _common(common, view):
    if common is None:
        return None
    receipt = common['projection_receipt']
    if any(receipt.get(k) != view.receipt.get(k) for k in ('context_id', 'scope', 'revision', 'event_hash', 'state_sha256')):
        raise MediaViewError('Operational projection receipt mismatch')
    original = common['projection']
    coverage = common['coverage']
    if sha(original) != coverage['projection_sha256'] or len(original) != coverage['actual_chars']:
        raise MediaViewError('Original projection hash mismatch')
    _source_packet(view, sha(original), len(original))
    result = view.transform(common)
    text = result['projection']
    result['coverage'].update(actual_chars=len(text), required_chars=min(coverage['required_chars'], len(text)), projection_sha256=sha(text),
                              policy='DERIVED media custody references; no semantic text pruning')
    result['router_media_view'] = dict(view.provenance(), original_projection_sha256=sha(original),
                                      original_actual_chars=len(original), original_required_chars=coverage['required_chars'],
                                      original_coverage=copy.deepcopy(coverage))
    return result


def _check_derived(common, view):
    provenance = common.get('router_media_view', {})
    if provenance.get('custody_pointer') != view.pointer:
        raise MediaViewError('Derived memory pointer mismatch')
    source = _source_packet(view, provenance['original_projection_sha256'], provenance['original_actual_chars'])
    expected = view.transform(source['text'])
    if (common['projection'] != expected or common['coverage']['projection_sha256'] != sha(expected)
            or common['coverage']['actual_chars'] != len(expected)):
        raise MediaViewError('Derived projection hash mismatch')


def routing_state(app_memory, max_chars=None):
    original = app_memory.routing_state(max_chars=max_chars)
    if original is None:
        return None
    view = _View(app_memory.current())
    result = _common(original, view)
    view.checked()
    return result


def prepare_body(body, binding):
    """Return a copy: whole-body check, including prompt and escaped JSON history.

    Common memory must ALREADY be derived via routing_state. No user payload
    absent from authenticated custody can be hidden or sent by this function.
    """
    if binding is None:
        if body.get('state', {}).get('common_memory') is not None:
            raise MediaViewError('Operational memory lacks authenticated binding')
        _unbound_text_only(body)
        return copy.deepcopy(body)
    view = _View(binding)
    common = body.get('state', {}).get('common_memory')
    if common is not None:
        _check_derived(common, view)
    protected = body.get('state', {}).get('canonical_memory')
    # Scientific text has no media transport role. Refuse ambiguous embedded
    # payloads instead of changing any byte of the scientific package.
    _unbound_text_only(protected)
    result = view.transform(body)
    if result.get('state', {}).get('canonical_memory') != protected:
        raise MediaViewError('Scientific routing text changed during media projection')
    result['state']['router_media_view'] = view.provenance()
    view.checked()
    return result


def assert_public_body(body, binding):
    """Final fail-closed egress check; no mutation, dispatch or automatic retry."""
    expected = prepare_body(body, binding)
    if encode(expected) != encode(body):
        raise MediaViewError('Routing body requires media projection before admission')
    return True


def _unbound_text_only(value):
    def refuse(text, path, media):
        if (MEDIA_START.search(re.sub(r'\\+/', '/', text)) or '[ARQUIVO:' in text or media
                or 'IALD_MEDIA_CUSTODY:' in text or 'IALD_ATTACHMENT_CUSTODY:' in text):
            raise MediaViewError('Media or custody reference lacks authenticated binding')
        return text
    _walk(value, refuse)


def project_system_messages(messages, common=None, *, binding=None):
    """Only SYSTEM/DEVELOPER media copies; user/assistant typed parts unchanged.

    Invoke AFTER the last app_memory.project_messages and BEFORE admission.
    `common`, when supplied, is an original or derived routing projection, never
    a replacement binding. Source media must exist in this authenticated ledger.
    """
    if binding is None:
        import iald_app_memory
        binding = iald_app_memory.current()
    if binding is None:
        # No operational memory to project; refuse any inline system media.
        if common is not None:
            raise MediaViewError('Operational memory lacks authenticated binding')
        for message in messages:
            if message.get('role') in ('system', 'developer'):
                _unbound_text_only(message)
        return copy.deepcopy(messages)
    view = _View(binding)
    if common is not None:
        if 'router_media_view' in common:
            _check_derived(common, view)
        else:
            _common(common, view)
    clean_messages = copy.deepcopy(messages)
    for message in clean_messages:
        if message.get('role') not in ('system', 'developer'):
            continue
        content = message.get('content')
        if isinstance(content, str) and PROV_START in content:
            if content.count(PROV_START) != 1 or content.count(PROV_END) != 1:
                raise MediaViewError('Ambiguous media provenance block')
            prefix, remainder = content.split(PROV_START, 1)
            old, suffix = remainder.split(PROV_END, 1)
            try:
                old = json.loads(old)
            except ValueError:
                raise MediaViewError('Invalid existing media provenance') from None
            if old.get('schema') != SCHEMA or old.get('custody_pointer') != view.pointer:
                raise MediaViewError('Stale existing media provenance')
            message['content'] = prefix + suffix
    result = []
    for message in clean_messages:
        if message.get('role') in ('system', 'developer'):
            content = message.get('content')
            if not isinstance(content, str):
                raise MediaViewError('Host operational envelope must be textual')
            if ACOM_START in content:
                if content.count(ACOM_START) != 1 or content.count(ACOM_END) != 1:
                    raise MediaViewError('Ambiguous operational memory envelope')
                prefix, remainder = content.split(ACOM_START, 1)
                operational, suffix = remainder.split(ACOM_END, 1)
                _unbound_text_only(prefix)
                _unbound_text_only(suffix)
                message['content'] = prefix + ACOM_START + view.transform(operational) + ACOM_END + suffix
            else:
                # Preserve science, instructions and protocol text outside the
                # host ACOM region byte-for-byte; no bare payload scan there.
                _unbound_text_only(content)
        result.append(message)
    # References inside system strings resolve through the unchanged memory
    # envelope and this scoped pointer, not a fabricated full-state artifact.
    if view.inventory:
        system = next((message for message in result if message.get('role') == 'system'), None)
        if system is None:
            system = dict(role='system', content='')
            result.insert(0, system)
        if not isinstance(system.get('content'), str):
            raise MediaViewError('System provenance requires textual host envelope')
        system['content'] += PROV_START + encode(view.provenance()) + PROV_END
    view.checked()
    return result
