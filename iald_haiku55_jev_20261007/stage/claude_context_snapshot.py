"""Prepared S3/S4 context and tool integrity boundary. Standard library only; no server/SDK import.

The trusted caller supplies the existing package loader and converter. No env,
network or writes. Hash the FINAL native wire tools, before count-only stripping.
"""
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
import hashlib
import json

from claude_profiles import HAIKU
MODEL = HAIKU.model
WINDOW = HAIKU.window
PUBLIC_NAMES = ('iald_kernel_verification', 'iald_kernel_search',
                'iald_kernel_read', 'iald_kernel_list', 'iald_public_read',
                'search_tgl', 'fetch_tgl')


class HaikuUnavailable(ValueError):
    """Visible preflight failure: caller must not count/send or silently fallback."""


@dataclass(frozen=True)
class MeasuredSnapshot:
    model: str
    prefix_sha256: str
    permanent: int
    reference_input: int
    output: int
    margin: int
    reference_remaining: int
    tools_sha256: str
    measurement_receipt: str


def _hash(value):
    return isinstance(value, str) and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def snapshot_from_manifest(manifest, package):
    """Cross-check metadata against an ALREADY validated load_package result.

    This does not authenticate the provider receipt or remeasure tokens.
    """
    try:
        b = manifest['budget']
        values = [b[k] for k in ('permanent_tokens', 'request_input_tokens',
                  'reserved_output_tokens', 'margin_tokens', 'remaining_tokens')]
        if any(type(v) is not int or v < 0 for v in values):
            raise HaikuUnavailable('invalid_measured_budget_types')
        permanent, reference, output, margin, remaining = values
        if (manifest['schema'] != 'iald.claude.memory.v1' or manifest['model'] != MODEL
                or b['model'] != MODEL or package.measurement.model != MODEL
                or not HAIKU.memory_target <= permanent <= reference or output != HAIKU.default_output or margin != 1024
                or remaining != WINDOW - reference - output - margin or remaining < 10000
                or b['ready'] is not True or b['fits'] is not True
                or b['memory_target_met'] is not True):
            raise HaikuUnavailable('invalid_measured_budget')
        if (package.measurement.permanent_tokens != permanent
                or package.reserved_output_tokens != output
                or package.available_dynamic_tokens != remaining
                or manifest['prefix_sha256'] != package.measurement.prefix_sha256
                or manifest['tools_sha256'] != package.tools_sha256
                or not _hash(manifest['prefix_sha256']) or not _hash(manifest['tools_sha256'])):
            raise HaikuUnavailable('package_metadata_mismatch')
        return MeasuredSnapshot(MODEL, manifest['prefix_sha256'], permanent, reference,
                                output, margin, remaining, manifest['tools_sha256'],
                                str(manifest.get('measurement_receipt', '')))
    except (KeyError, TypeError, AttributeError) as exc:
        raise HaikuUnavailable('invalid_package_metadata') from exc


def load_snapshot(directory, package_loader):
    """directory is server-controlled. Preserve loader's prefix/path validation."""
    path = Path(directory) / 'manifest.json'
    raw = path.read_bytes()
    manifest = json.loads(raw)
    package = package_loader(directory)
    result = snapshot_from_manifest(manifest, package)
    if path.read_bytes() != raw:
        raise HaikuUnavailable('manifest_changed_during_load')
    return package, result


def context_metadata(snapshot):
    """Measured reference budget, never remaining tokens of the current chat.

    margem=0.90 is retained ONLY for legacy JSON compatibility. Haiku clients
    must bypass CPT/history trimming and percent-used calculations: cpt=None
    and recorte_por_cpt_permitido=False explicitly declare that contract.
    margem_tokens is the measured native-token margin used by the guard.
    """
    return {
        'modelo': snapshot.model, 'disponivel': True,
        'n_ctx': WINDOW, 'janela': WINDOW, 'unidade_tokens': 'Anthropic',
        # Legacy frontend multiplier, NOT an Anthropic token reserve.
        'margem': 0.90, 'margem_tokens': snapshot.margin,
        'reserva_resposta': snapshot.output,
        'memoria_tokens_medidos': snapshot.permanent,
        'requisicao_referencia_tokens_medidos': snapshot.reference_input,
        'reserva_dinamica_medida': snapshot.reference_remaining,
        'saldo_conversa_atual_tokens': None,
        'contagem_nativa_por_pedido_obrigatoria': True,
        'base_reserva_dinamica': 'requisição de referência do recibo; não é saldo da conversa atual',
        'medicao_inclui_mensagem_minima': True,
        'nao_incluido_na_referencia': ['perfil/nota de serviço atuais', 'histórico atual', 'resultados de ferramentas'],
        'prefix_sha256': snapshot.prefix_sha256, 'tools_sha256': snapshot.tools_sha256,
        'origem_medicao': 'pacote validado pelo servidor',
        'teto_mensagens': 400,
        # No invented chars/token conversion from o200k to Anthropic.
        'cpt': None,
        'recorte_por_cpt_permitido': False,
    }


def status_response(load_checked_snapshot, jsonify, *, limits=False):
    """Haiku-only route adapter. Callback also checks current native tool schema.

    Return JSON503 on unavailable package/config/tools; exceptions do not leak
    filesystem paths. Route must authorize session/account BEFORE this callback.
    """
    try:
        snapshot = load_checked_snapshot()
        data = context_metadata(snapshot)
        if limits:
            data.update(max_saida=snapshot.output, pensar=True,
                        ferramentas=list(PUBLIC_NAMES), schemas_sempre_presentes=True)
        return jsonify(data), 200
    except (ValueError, OSError, KeyError, TypeError, AttributeError):
        return jsonify({'modelo': MODEL, 'disponivel': False,
                        'error': 'Memória, configuração ou ferramentas Haiku indisponíveis.',
                        'code': 'haiku_package_unavailable',
                        'saldo_conversa_atual_tokens': None}), 503


def _seven(tools, native):
    if (not isinstance(tools, list) or len(tools) != 7
            or not all(isinstance(tool, dict) for tool in tools)):
        raise HaikuUnavailable('expected_seven_tool_schemas')
    try:
        if native:
            if any('function' in t or not isinstance(t.get('input_schema'), dict) for t in tools):
                raise HaikuUnavailable('expected_native_tool_schema')
            names = [t['name'] for t in tools]
        else:
            if any(t.get('type') != 'function' or not isinstance(t.get('function'), dict)
                   or not isinstance(t['function'].get('parameters'), dict) for t in tools):
                raise HaikuUnavailable('expected_openai_function_schema')
            names = [t['function']['name'] for t in tools]
        if len(set(names)) != 7 or set(names) != set(PUBLIC_NAMES):
            raise HaikuUnavailable('public_tool_set_changed')
    except (KeyError, TypeError, AttributeError) as exc:
        raise HaikuUnavailable('malformed_tool_schemas') from exc


def native_tools_sha256(tools):
    """EXACT receipt serializer; list order, spaces and transport flags retained.

    count_native_reviewed_draft.py hashes wire['tools'] BEFORE the count adapter
    removes eager_input_streaming. Never compact separators or sort the list.
    """
    _seven(tools, native=True)
    try:
        # Reject non-JSON/nonfinite data, without changing valid serialization.
        json.dumps(tools, allow_nan=False)
        raw = json.dumps(tools, sort_keys=True, ensure_ascii=False).encode('utf-8')
    except (TypeError, ValueError) as exc:
        raise HaikuUnavailable('invalid_native_tool_json') from exc
    return hashlib.sha256(raw).hexdigest()


def verify_native_tools(wire, snapshot, *, trusted_tools=None):
    """tool_choice='none' does NOT remove schemas and is deliberately accepted."""
    if not isinstance(wire, dict) or wire.get('model') != snapshot.model:
        raise HaikuUnavailable('wire_model_mismatch')
    offered = wire.get('tools')
    if trusted_tools is not None:
        if offered != trusted_tools:
            raise HaikuUnavailable('scoped_native_tools_changed')
        offered = offered[:len(PUBLIC_NAMES)]
    actual = native_tools_sha256(offered)
    if actual != snapshot.tools_sha256:
        raise HaikuUnavailable('native_tools_sha256_mismatch')
    return actual


def attach_openai_tools(payload, definitions):
    """Use on every Haiku payload, even the direct/non-agent branch.

    Installs the seven reviewed definitions only when absent. A conflicting
    existing schema is an error, never silently overwritten. Copies all data;
    tool_choice is preserved verbatim, including 'none'.
    """
    if not isinstance(definitions, list):
        raise HaikuUnavailable('missing_server_definitions')
    _seven(definitions[:len(PUBLIC_NAMES)], native=False)
    # All definitions come from the server's authenticated task scope. A payload
    # can never add/replace one; CheckedAdapter pins the entire native list.
    names = [(t.get('function') or {}).get('name') for t in definitions if isinstance(t, dict)]
    if len(names) != len(definitions) or any(not isinstance(n, str) or not n for n in names) or len(set(names)) != len(names):
        raise HaikuUnavailable('invalid_scoped_definitions')
    if not isinstance(payload, dict):
        raise HaikuUnavailable('expected_openai_payload')
    result = deepcopy(payload)
    if 'tools' in result and result['tools'] != definitions:
        raise HaikuUnavailable('openai_tools_changed')
    result['tools'] = deepcopy(definitions)
    return result


class CheckedAdapter:
    """Pass this proxy to post_guarded, so its FINAL converter is verified.

    It exposes the existing adapter unchanged except converter_pedido. This is
    intentionally not a standalone send function and never acquires a client.
    """
    def __init__(self, adapter, snapshot, *, trusted_openai_tools=None):
        self._adapter, self._snapshot = adapter, snapshot
        self._tools = None
        if trusted_openai_tools is not None:
            attach_openai_tools({}, trusted_openai_tools)
            self._tools = deepcopy(adapter.converter_ferramentas(trusted_openai_tools))
            verify_native_tools({'model': snapshot.model, 'tools': self._tools}, snapshot, trusted_tools=self._tools)
        self._binding = None

    def __getattr__(self, name):
        return getattr(self._adapter, name)

    def converter_pedido(self, *args, **kwargs):
        bind_context = kwargs.pop("bind_context", True)
        if type(bind_context) is not bool:
            raise HaikuUnavailable("invalid_context_binding_mode")
        wire = self._adapter.converter_pedido(*args, **kwargs)
        verify_native_tools(wire, self._snapshot, trusted_tools=self._tools)
        # A thinking signature is valid only with the identical prefix. Pin
        # model/system/tools for the lifetime of this one chat job/tool loop.
        binding = deepcopy([wire.get(k) for k in ('model', 'system', 'tools')])
        if self._binding is None:
            if bind_context:
                self._binding = binding
        elif self._binding != binding:
            raise HaikuUnavailable('signed_context_changed_during_tool_loop')
        return wire
