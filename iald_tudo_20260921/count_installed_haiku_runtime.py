"""One authorized free count of installed memory plus runtime tools/service note."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import anthropic
from dotenv import dotenv_values
import iald_core_indexado
import iald_fontes_publicas
import iald_kernel
import iald_motor_claude
import iald_motores
from claude_context_snapshot import load_snapshot, CheckedAdapter, attach_openai_tools
from claude_memory_package import load_package
from claude_haiku_messages import assemble
from claude_native_counter import count_native_request
from claude_profiles import HAIKU, context_budget, reasoning_parameters

def main():
    package, snapshot = load_snapshot(ROOT / '.iald_runtime/haiku', load_package)
    tools = (iald_kernel.tool_definitions() + iald_fontes_publicas.tool_definitions()
             + iald_core_indexado.tool_definitions())
    cfg = SimpleNamespace(modelo=HAIKU.model, max_saida=512, cache_ttl='5m', esforco_claude='high')
    conversation = [{'role': 'user', 'content': 'Responda em uma frase: quem é o autor da TGL?'}]
    messages, _ = assemble(iald_motores, conversation, package.prefix, HAIKU.model,
                           [tool['function']['name'] for tool in tools])
    payload = attach_openai_tools({'model': HAIKU.model, 'max_completion_tokens': 512,
                                  'messages': messages, 'tool_choice': 'none'}, tools)
    wire = CheckedAdapter(iald_motor_claude, snapshot).converter_pedido(cfg, payload, prefixo=package.prefix)
    wire.pop('output_config', None)
    wire.update(reasoning_parameters(HAIKU.model, 512))
    assert '<ATLAS_CANONICO' not in package.prefix
    key = dotenv_values(ROOT / '.env').get('IALD_CLAUDE_API_KEY')
    if not key:
        raise ValueError('Credential absent')
    with anthropic.Anthropic(api_key=key, max_retries=0, timeout=90) as client:
        count = count_native_request(client, wire)
    decision = context_budget(HAIKU.model, counted_model=HAIKU.model,
        permanent_tokens=package.measurement.permanent_tokens, request_input_tokens=count,
        reserved_output_tokens=4096, margin_tokens=1024)
    now = datetime.now(timezone.utc)
    result = {'checked_at': now.isoformat(), 'status': 'INSTALLED_RUNTIME_COUNTED_NOT_ACTIVATED',
        'model': HAIKU.model, 'prefix_sha256': snapshot.prefix_sha256,
        'tools_sha256': snapshot.tools_sha256, 'budget': decision,
        'wire_sha256': hashlib.sha256(json.dumps(wire, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
        'included': ['installed memory', 'seven tools', 'runtime service note', 'one real proposed test question'],
        'not_included': ['user profile', 'prior conversation', 'retrieval results'],
        'scope': 'native free count only; no model answer or app session exercised',
        'count_requests': 1, 'generation_requests': 0, 'memory_modified': False}
    path = WORK / ('installed_haiku_runtime_count_' + now.strftime('%Y%m%d_%H%M%S_%f') + '.json')
    raw = json.dumps(result, ensure_ascii=False, indent=2).encode('utf8')
    with path.open('xb') as stream:
        stream.write(raw)
    assert path.read_bytes() == raw
    print(json.dumps({'receipt': str(path), 'budget': decision, 'generation_requests': 0}))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status': 'FAILED', 'exception_type': type(exc).__name__}))
        raise SystemExit(1)
