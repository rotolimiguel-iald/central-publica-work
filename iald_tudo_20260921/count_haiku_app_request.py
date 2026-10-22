"""Free Haiku count using the existing seven public app tool definitions."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from dotenv import dotenv_values
import anthropic

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from build_haiku_candidate import store
from claude_profiles import context_budget, HAIKU
import iald_kernel
import iald_fontes_publicas
import iald_core_indexado
from iald_motor_claude import converter_ferramentas


def main():
    record = json.loads((WORK / 'haiku_candidate.json').read_bytes())
    measured = json.loads((WORK / 'haiku_count.json').read_bytes())
    raw = (WORK / 'haiku_candidate.md').read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != record['sha256'] or digest != measured['candidate_sha256']:
        raise ValueError('Candidate changed since provider count')
    text = raw.decode('utf-8')
    if '<ATLAS_CANONICO' in text:
        raise ValueError('Private Atlas context forbidden')
    # Same public non-agent branch as _ferramentas_externas, without importing server.
    definitions = (iald_kernel.tool_definitions() + iald_fontes_publicas.tool_definitions()
                   + iald_core_indexado.tool_definitions())
    names = [t['function']['name'] for t in definitions]
    if set(names) != {'iald_kernel_verification','iald_kernel_search','iald_kernel_read',
                      'iald_kernel_list','iald_public_read','search_tgl','fetch_tgl'}:
        raise ValueError('Public tool set changed; review required')
    tools = converter_ferramentas(definitions)
    key = dotenv_values(ROOT / '.env').get('IALD_CLAUDE_API_KEY')
    if not key:
        raise ValueError('Missing Anthropic key')
    question = 'Quem é o autor da TGL? Explique a relação entre Hamiltoniano, Lindblad e dephasing no escopo documentado.'
    with anthropic.Anthropic(api_key=key, max_retries=0, timeout=120) as client:
        count = client.messages.count_tokens(model=HAIKU.model, system=text, tools=tools,
                    messages=[{'role': 'user', 'content': question}])
    budget = context_budget(HAIKU.model, counted_model=HAIKU.model,
                            permanent_tokens=measured['input_tokens'],
                            request_input_tokens=count.input_tokens, reserved_output_tokens=4096)
    result = {'time_utc': datetime.now(timezone.utc).isoformat(), 'candidate_sha256': digest,
              'status': 'MEASURED_PUBLIC_TOOL_REQUEST_NOT_DEPLOYED', 'tools': names,
              'tools_sha256': hashlib.sha256(json.dumps(tools, sort_keys=True, ensure_ascii=False).encode()).hexdigest(),
              'budget': budget, 'provider_count_input_tokens': count.input_tokens,
              'permanent_measurement_includes_minimal_message': True,
              'not_included': ['runtime service note/profile', 'actual conversation history', 'tool result turns'],
              'generation_requests': 0}
    store(WORK / 'haiku_app_request_count.json', (json.dumps(result, indent=2) + '\n').encode())
    print(json.dumps(result))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status': 'FAILED', 'exception_type': type(exc).__name__}))
        raise SystemExit(1)
