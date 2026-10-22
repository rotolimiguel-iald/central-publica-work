"""Build reviewable migration in staging, with fail-closed exact replacements."""
from pathlib import Path
import hashlib, json

W = Path(__file__).resolve().parent
R = Path(r'C:\IALD\projetos_pyhton\IALD')
S = W / 'stage'

def patch(name, replacements):
    path = S / name
    if not path.exists():
        raw = (R / name).read_bytes()
        (W / 'original' / name).write_bytes(raw)
        base = json.loads((W / 'baseline.json').read_bytes())
        base[name] = {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
        (W / 'baseline.json').write_bytes(json.dumps(base, indent=2).encode())
        path.write_bytes(raw)
    text = path.read_bytes().decode('utf-8').replace('\r\n', '\n')
    for old, new in replacements:
        assert text.count(old) == 1, (name, old[:130], text.count(old))
        text = text.replace(old, new)
    compile(text, name, 'exec')
    path.write_bytes(text.encode())

patch('claude_profiles.py', [
    ('    output_usd_per_million: float\n', '    output_usd_per_million: float\n    default_output: int = 4096\n'),
    ("HAIKU = Profile('claude-haiku-4-5-20251001', 200000, 64000, 180000, False, 1.0, 5.0)",
     "# Legacy certificate remains readable for other providers; never a 5.5 token count.\nLEGACY_HAIKU = Profile('claude-haiku-4-5-20251001', 200000, 64000, 180000, False, 1.0, 5.0)\n# Rates for >100k prompts: the deployed scientific memory is above that tier.\nHAIKU = Profile('claude-haiku-5-5', 1000000, 128000, 180000, False, 0.50, 2.50, 16384)"),
    ("    if model in (HAIKU.model, 'claude-haiku-4-5'):\n        return HAIKU", "    if model == HAIKU.model:\n        return HAIKU\n    if model in (LEGACY_HAIKU.model, 'claude-haiku-4-5'):\n        return LEGACY_HAIKU"),
    ('def reasoning_parameters(model, max_output, thinking_budget=0):\n    """Never send adaptive thinking/output_config.effort to Haiku."""',
     'def reasoning_parameters(model, max_output, thinking_budget=0, *, effort=None):\n    """Use the explicit model capability, not a family-name heuristic."""'),
    ("    if profile is SONNET:\n        return {'thinking': {'type': 'adaptive'}, 'output_config': {'effort': 'high'}}", "    if profile in (SONNET, HAIKU):\n        if thinking_budget:\n            raise ValueError('Manual thinking budget is unsupported by this model')\n        effort = effort or ('medium' if profile is HAIKU else 'high')\n        if effort not in ('low', 'medium', 'high'):\n            raise ValueError('Unreviewed effort')\n        return {'thinking': {'type': 'adaptive'}, 'output_config': {'effort': effort}}"),
])
patch('claude_memory_package.py', [
    ('from claude_profiles import HAIKU, context_budget', 'from claude_profiles import HAIKU, profile_for, context_budget'),
    ('def load_package(directory, *, canonical_manifest=None, source_sha=None):', 'def load_package(directory, *, canonical_manifest=None, source_sha=None, expected_model=None):'),
    ('    root=Path(directory).resolve()', '    profile = profile_for(expected_model or HAIKU.model)\n    root=Path(directory).resolve()'),
    ("manifest.get('model')!=HAIKU.model", "manifest.get('model')!=profile.model"),
    ("b.get('reserved_output_tokens')!=4096", "b.get('reserved_output_tokens')!=profile.default_output"),
    ('checked=context_budget(HAIKU.model,counted_model=HAIKU.model,', 'checked=context_budget(profile.model,counted_model=profile.model,'),
    ('MemoryMeasurement(HAIKU.model,digest', 'MemoryMeasurement(profile.model,digest'),
])
patch('claude_server_selection.py', [
    ('from claude_profiles import HAIKU,SONNET', 'from claude_profiles import HAIKU,SONNET,LEGACY_HAIKU'),
    ('    if not requested:\n', "    if requested in (LEGACY_HAIKU.model, 'claude-haiku-4-5'):\n        requested = HAIKU.model  # Explicit operator-authorized migration, no account rewrite.\n    if not requested:\n"),
    ("'Claude Haiku 4.5'", "'Claude Haiku 5.5'"),
    ('        result.max_saida=result.max_saida_pensar=4096\n        result.janela=200000', '        result.max_saida=result.max_saida_pensar=HAIKU.default_output\n        result.janela=HAIKU.window\n        result.esforco_claude="medium"'),
])
patch('claude_route_bridge.py', [
    ('HAIKU_PRICES_5M=(1.0,0.10,5.0,1.25)\nHAIKU_WRITE_1H=2.0', 'HAIKU_PRICES_5M=(0.50,0.05,2.50,0.625)\nHAIKU_WRITE_1H=1.0'),
    ('minimum=(200000*1.15*max(rates[0],rates[1],rates[3])+4096*rates[2])/1e6',
     "package=self.package()\n            reference=HAIKU.window-package.available_dynamic_tokens-package.reserved_output_tokens-1024\n            minimum=(reference*1.15*max(rates[0],rates[1],rates[3])+HAIKU.default_output*rates[2])/1e6"),
])
patch('claude_native_account.py', [
    ('import math\n', 'import math\nfrom claude_profiles import profile_for\n'),
    ('output > 4096', 'output > profile_for(self.model).default_output'),
])
patch('claude_guarded_transport.py', [('wire[\'max_tokens\']>4096', "wire['max_tokens']>HAIKU.default_output")])
patch('claude_profile_pipeline.py', [
    ('wire.update(reasoning_parameters(authorized, wire[\'max_tokens\'], thinking_budget))', "wire.update(reasoning_parameters(authorized, wire['max_tokens'], thinking_budget,\n                                         effort=getattr(selected_cfg, 'esforco_claude', 'medium')))"),
])
patch('claude_request_guard.py', [
    ("    if profile is HAIKU:\n        if wire.get('thinking', {}).get('type') == 'adaptive' or 'effort' in wire.get('output_config', {}):\n            raise ValueError('Sonnet-only reasoning parameters cannot be sent to Haiku')", "    if profile is HAIKU:\n        if (wire.get('thinking', {}).get('type') not in ('adaptive', 'disabled')\n                or wire.get('output_config', {}).get('effort') not in ('low', 'medium', 'high')\n                or any(k in wire for k in ('temperature', 'top_p', 'top_k'))):\n            raise ValueError('Unreviewed Haiku 5.5 parameters')\n        if not wire.get('messages') or wire['messages'][-1].get('role') != 'user':\n            raise ValueError('Assistant prefill unsupported')"),
])
patch('claude_context_snapshot.py', [
    ("MODEL = 'claude-haiku-4-5-20251001'\nWINDOW = 200000", 'from claude_profiles import HAIKU\nMODEL = HAIKU.model\nWINDOW = HAIKU.window'),
    ('or not 180000 <= permanent <= reference or output != 4096 or margin != 1024', 'or not HAIKU.memory_target <= permanent <= reference or output != HAIKU.default_output or margin != 1024'),
    ('data.update(max_saida=snapshot.output, pensar=False,', 'data.update(max_saida=snapshot.output, pensar=True,'),
    ('def verify_native_tools(wire, snapshot):', 'def verify_native_tools(wire, snapshot, *, trusted_tools=None):'),
    ("    actual = native_tools_sha256(wire.get('tools'))", "    offered = wire.get('tools')\n    if trusted_tools is not None:\n        if offered != trusted_tools:\n            raise HaikuUnavailable('scoped_native_tools_changed')\n        offered = offered[:len(PUBLIC_NAMES)]\n    actual = native_tools_sha256(offered)"),
    ('    _seven(definitions, native=False)\n    if not isinstance(payload, dict):', "    if not isinstance(definitions, list):\n        raise HaikuUnavailable('missing_server_definitions')\n    _seven(definitions[:len(PUBLIC_NAMES)], native=False)\n    # All definitions come from the server's authenticated task scope. A payload\n    # can never add/replace one; CheckedAdapter pins the entire native list.\n    names = [(t.get('function') or {}).get('name') for t in definitions if isinstance(t, dict)]\n    if len(names) != len(definitions) or any(not isinstance(n, str) or not n for n in names) or len(set(names)) != len(names):\n        raise HaikuUnavailable('invalid_scoped_definitions')\n    if not isinstance(payload, dict):"),
    ('    def __init__(self, adapter, snapshot):\n        self._adapter, self._snapshot = adapter, snapshot', "    def __init__(self, adapter, snapshot, *, trusted_openai_tools=None):\n        self._adapter, self._snapshot = adapter, snapshot\n        self._tools = None\n        if trusted_openai_tools is not None:\n            attach_openai_tools({}, trusted_openai_tools)\n            self._tools = deepcopy(adapter.converter_ferramentas(trusted_openai_tools))\n            verify_native_tools({'model': snapshot.model, 'tools': self._tools}, snapshot, trusted_tools=self._tools)\n        self._binding = None"),
    ('        verify_native_tools(wire, self._snapshot)\n        return wire', "        verify_native_tools(wire, self._snapshot, trusted_tools=self._tools)\n        # A thinking signature is valid only with the identical prefix. Pin\n        # model/system/tools for the lifetime of this one chat job/tool loop.\n        binding = deepcopy([wire.get(k) for k in ('model', 'system', 'tools')])\n        if self._binding is None:\n            self._binding = binding\n        elif self._binding != binding:\n            raise HaikuUnavailable('signed_context_changed_during_tool_loop')\n        return wire"),
])
patch('iald_task_bridge.py', [
    ('authorize=sandbox_authorize,cancel=control.cancel.is_set,window=200000,accounting=account)', 'authorize=sandbox_authorize,cancel=control.cancel.is_set,window=cfg.janela,accounting=account,\n            trusted_prefix_sha256=memory_sha)'),
])
patch('iald_task_sandbox.py', [
    ('effective_window = min(window, 200_000) if haiku else window', "effective_window = min(window, 1_000_000 if model == 'claude-haiku-5-5' else 200_000) if haiku else window"),
    ('        check_cancel()\n        phase = "count_tokens"', "        if model == 'claude-haiku-5-5':\n            request.update(thinking={'type': 'disabled'}, output_config={'effort': 'low'})\n        check_cancel()\n        phase = \"count_tokens\""),
])
patch('iald_motores.py', [
    ('    if modelo == "claude-sonnet-5-5":\n', '    if modelo == "claude-haiku-5-5":\n        return "Claude Haiku 5.5"\n    if modelo == "claude-sonnet-5-5":\n'),
])
patch('iald_web_server.py', [
    ('from claude_profiles import HAIKU as _HAIKU_PROFILE', 'from claude_profiles import HAIKU as _HAIKU_PROFILE, LEGACY_HAIKU as _LEGACY_HAIKU_PROFILE, reasoning_parameters as _haiku_reasoning'),
    ('return model == _HAIKU_PROFILE.model or (not model', 'return model in (_HAIKU_PROFILE.model, _LEGACY_HAIKU_PROFILE.model, "claude-haiku-4-5") or (not model'),
    ('def _load_haiku_package():', 'def _load_shared_science_package():\n    # Keep other providers on their audited compact v390 prefix. Its old count\n    # is provenance only; each connector still admits its own actual request.\n    return load_package(os.path.join(SERVE_DIR, ".iald_runtime", "haiku"),\n        canonical_manifest=os.path.join(SERVE_DIR, "iald_nucleo_fixo.json"),\n        source_sha=KERNEL_EXTERNO.source_sha, expected_model=_LEGACY_HAIKU_PROFILE.model)\n\n\ndef _load_haiku_package():'),
    ('os.path.join(SERVE_DIR, ".iald_runtime", "haiku"),\n        lambda directory', 'os.path.join(SERVE_DIR, ".iald_runtime", "haiku55"),\n        lambda directory'),
    ('    cfg.max_saida = 4096\n    payload = _haiku_attach_tools({"model": cfg.modelo, "max_completion_tokens": 4096,', '    cfg.max_saida = _HAIKU_PROFILE.default_output\n    payload = _haiku_attach_tools({"model": cfg.modelo, "max_completion_tokens": cfg.max_saida,'),
    ('package=CLAUDE_ROUTES.package,evaluation=APP_EVALUATION', 'package=_load_shared_science_package,evaluation=APP_EVALUATION'),
    ("task_scope=_new_app_task_scope(user,executor=chosen) if chosen not in ('kimi','claude-haiku','nativa') else None", "task_scope=_new_app_task_scope(user,executor=chosen) if chosen not in ('kimi','nativa') else None"),
    ('        package = CLAUDE_ROUTES.package()\n        prefix = package.prefix', '        package = _load_shared_science_package()\n        prefix = package.prefix'),
    ('haiku_adapter = _CheckedHaikuAdapter(iald_motor_claude, haiku_snapshot)', 'haiku_adapter = _CheckedHaikuAdapter(iald_motor_claude, haiku_snapshot, trusted_openai_tools=permitidas)'),
    ('            wire.pop("output_config", None)\n            wire["thinking"] = {"type": "disabled"}', '            wire.update(_haiku_reasoning(modelo, wire["max_tokens"], effort=cfg.esforco_claude))'),
])
print(json.dumps({'status': 'STAGED', 'files': len(list(S.glob('*.py')))}))
