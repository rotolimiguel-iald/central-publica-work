"""Local tokenizer measurement; no inference, remote network, private memory or server import."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import sys
from unittest.mock import patch

STAGE = Path(__file__).resolve().parent
PRODUCTION = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0] = [str(STAGE), str(PRODUCTION)]
import iald_native_memory as native
import iald_kernel
import iald_core_indexado


def measure(manifest):
    cfg = json.loads(manifest.read_bytes())
    cluster = cfg['active_cluster']
    catalog = iald_kernel.KernelCatalog(cluster['kernel_bundle'], cluster['kernel_verification'])
    prefix, identity = native.load_native_context(manifest, catalog)
    tree = ast.parse((STAGE / 'iald_web_server.py').read_bytes())
    constants = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in (
                        'PUBLIC_TOOLS', 'MODELS', 'ACTIVE_MODEL_ID', 'FERRAMENTAS_FORA_DA_LOJA'):
                    constants[target.id] = ast.literal_eval(node.value)
    sacred = next(ast.literal_eval(n.value) for n in ast.walk(tree) if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == 'sacred_msg' for t in n.targets))
    window = native.configured_window(constants['MODELS'][constants['ACTIVE_MODEL_ID']])
    receipt = {'scope': 'REAL_PUBLIC_ASSETS__LOCAL_TEMPLATE_AND_TOKENIZER_NO_GENERATION',
        'inference_calls': 0, 'remote_network_calls': 0, 'local_endpoints': ['/props', '/apply-template', '/tokenize'], 'manifest': str(manifest),
        'manifest_sha256': hashlib.sha256(manifest.read_bytes()).hexdigest(),
        'deployment': identity, 'prefix_bytes': len(prefix.encode('utf-8')),
        'catalog': catalog.status(), 'startup_log': native.startup_summary(manifest, catalog),
        'cases': [], 'unmeasured': ['operator private memory',
            'actual user profiles/history', 'image tokens and generation quality']}
    assets = [PRODUCTION / 'app/kernel_prompt.js', PRODUCTION / 'app/kernel_prompt_loja.js',
              PRODUCTION / 'iald_chat.html']
    for asset in assets:
        text = asset.read_text(encoding='utf-8')
        pattern = (r'export const SYSTEM_PROMPT(?:_LOJA)?\s*=\s*'
                   if asset.suffix == '.js' else r'var SYSTEM_PROMPT\s*=\s*')
        start = re.search(pattern, text).end()
        prompt, _ = json.JSONDecoder().raw_decode(text[start:])
        tools = [t for t in constants['PUBLIC_TOOLS'] if asset.name != 'kernel_prompt_loja.js'
                 or t['function']['name'] not in constants['FERRAMENTAS_FORA_DA_LOJA']]
        tools += iald_kernel.tool_definitions() + iald_core_indexado.tool_definitions()
        for output in (4096, 8192):
            messages = [{'role': 'system', 'content': prompt}, sacred,
                        {'role': 'user', 'content': 'Apresente as fórmulas essenciais da TGL v378.'}]
            payload = {'messages': native.attach_context(messages, prefix),
                       'tools': tools, 'max_tokens': output,
                       'chat_template_kwargs': {'enable_thinking': output == 8192}}
            decision = native.check_text_window(payload, window)
            used = decision['input_tokens'] + decision['output_reserve'] + decision['framing_allowance']
            legacy = {}
            for value in (32768, 16384):
                legacy[str(value)] = 'ACCEPTED' if used <= value else 'VISIBLE_CONTEXT_REFUSAL'
            receipt['cases'].append({'asset': str(asset),
                'asset_sha256': hashlib.sha256(asset.read_bytes()).hexdigest(),
                'client_prompt_bytes': len(prompt.encode('utf-8')), **decision,
                'measured_total_tokens': used, 'remaining_tokens': decision['effective_window'] - used,
                'legacy_windows': legacy, 'accepted': True})
    # Reproduce the exact 60,000-character history from NATIVE-001. Then append
    # an actual tool turn: its text must be counted anew and remain unchanged.
    from copy import deepcopy
    import math
    history = [{'role': 'user', 'content': 'a' * 30000},
               {'role': 'assistant', 'content': 'b' * 30000},
               {'role': 'user', 'content': 'Continue a resposta.'}]
    payload = {'messages': native.attach_context(
        [{'role': 'system', 'content': prompt}] + history, prefix),
        'tools': tools, 'max_tokens': 8192,
        'chat_template_kwargs': {'enable_thinking': False}}
    original = deepcopy(payload)
    regression = native.check_text_window(payload, window)
    assert payload == original
    receipt['p2_regression'] = {
        'frontend_history_tokens_estimated': sum(math.ceil(len(m['content']) / 2.91) for m in history),
        'full_payload_preserved': True, 'accepted': True, **regression}
    payload['messages'] += [
        {'role': 'assistant', 'content': None, 'tool_calls': [
            {'id': 'review1', 'type': 'function', 'function': {
                'name': 'fetch_tgl', 'arguments': '{"id":"um_forma_canonica_integral"}'}}]},
        {'role': 'tool', 'tool_call_id': 'review1', 'content': json.dumps(
            {'text': 'Public regression fixture. ' * 170, 'next_offset': 4500})}]
    original = deepcopy(payload)
    after_tool = native.check_text_window(payload, window)
    assert payload == original and after_tool['input_tokens'] > regression['input_tokens']
    receipt['after_tool_regression'] = {'full_payload_preserved': True, 'accepted': True, **after_tool}
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', type=Path, default=STAGE.parent / 'manifest_install.json')
    args = parser.parse_args()
    original_connect = socket.socket.connect
    def loopback_only(sock, address):
        if not isinstance(address, tuple) or address[:2] != ('127.0.0.1', 8081):
            raise AssertionError('Only local tokenizer access is authorized')
        return original_connect(sock, address)
    with patch.object(socket.socket, 'connect', loopback_only):
        result = measure(args.manifest)
    target = STAGE / 'native_token_measurement.json'
    raw = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if target.exists():
        raise SystemExit('Receipt exists; preserve it before rerunning with a changed release.')
    temporary = target.with_suffix('.json.tmp')
    temporary.write_bytes(raw)
    assert temporary.stat().st_size == len(raw)
    os.replace(temporary, target)
    print(json.dumps({'receipt': str(target), 'cases': len(result['cases']),
        'prefix_bytes': result['prefix_bytes'],
        'worst_total': max(c['measured_total_tokens'] for c in result['cases']),
        'smallest_remaining': min(c['remaining_tokens'] for c in result['cases']),
        'p2_regression_input_tokens': result['p2_regression']['input_tokens'],
        'tool_round_input_tokens': result['after_tool_regression']['input_tokens']}))
