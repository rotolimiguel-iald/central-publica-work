"""Offline base-payload measurement; no inference, network, private memory or server import."""
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
    receipt = {'scope': 'REAL_PUBLIC_ASSETS__OFFLINE_CONSERVATIVE_TEXT_ADMISSION',
        'inference_calls': 0, 'network_calls': 0, 'manifest': str(manifest),
        'manifest_sha256': hashlib.sha256(manifest.read_bytes()).hexdigest(),
        'deployment': identity, 'prefix_bytes': len(prefix.encode('utf-8')),
        'catalog': catalog.status(), 'startup_log': native.startup_summary(manifest, catalog),
        'cases': [], 'unmeasured': ['native tokenizer/chat-template token count',
            'live llama-server slot configuration', 'operator private memory',
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
                       'tools': tools, 'max_tokens': output}
            decision = native.check_text_window(payload, window)
            used = decision['text_bytes'] + decision['output_reserve'] + decision['framing_allowance']
            legacy = {}
            for value in (32768, 16384):
                try:
                    native.check_text_window(payload, value)
                    legacy[str(value)] = 'ACCEPTED'
                except native.NativeContextError:
                    legacy[str(value)] = 'VISIBLE_CONTEXT_REFUSAL'
            receipt['cases'].append({'asset': str(asset),
                'asset_sha256': hashlib.sha256(asset.read_bytes()).hexdigest(),
                'client_prompt_bytes': len(prompt.encode('utf-8')), **decision,
                'conservative_total': used, 'remaining_text_allowance_bytes': window - used,
                'legacy_windows': legacy, 'accepted': True})
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', type=Path, default=STAGE.parent / 'manifest_install.json')
    args = parser.parse_args()
    with patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden')):
        result = measure(args.manifest)
    target = STAGE / 'native_measurement.json'
    raw = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if target.exists():
        raise SystemExit('Receipt exists; preserve it before rerunning with a changed release.')
    temporary = target.with_suffix('.json.tmp')
    temporary.write_bytes(raw)
    assert temporary.stat().st_size == len(raw)
    os.replace(temporary, target)
    print(json.dumps({'receipt': str(target), 'cases': len(result['cases']),
        'prefix_bytes': result['prefix_bytes'],
        'worst_total': max(c['conservative_total'] for c in result['cases']),
        'smallest_remaining': min(c['remaining_text_allowance_bytes'] for c in result['cases'])}))
