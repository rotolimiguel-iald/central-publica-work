"""Free token count of the authorized TGL candidate; no generation or secret output."""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
from dotenv import dotenv_values
import anthropic
from build_haiku_candidate import store

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
MODEL = 'claude-haiku-4-5-20251001'


def main():
    receipt = json.loads((WORK / 'haiku_candidate.json').read_bytes())
    raw = (WORK / 'haiku_candidate.md').read_bytes()
    if hashlib.sha256(raw).hexdigest() != receipt['sha256']:
        raise ValueError('Candidate changed since inventory')
    text = raw.decode('utf-8')
    if '<ATLAS_CANONICO' in text:
        raise ValueError('Private Atlas context forbidden')
    # Read the named key only; never print dotenv content or exception bodies.
    key = dotenv_values(ROOT / '.env').get('IALD_CLAUDE_API_KEY')
    if not key:
        raise ValueError('Anthropic credential absent')
    with anthropic.Anthropic(api_key=key, max_retries=0, timeout=120) as client:
        baseline = client.messages.count_tokens(model=MODEL, system='.', messages=[{'role':'user','content':'.'}])
        measured = client.messages.count_tokens(model=MODEL, system=text, messages=[{'role':'user','content':'.'}])
    result = {'time_utc': datetime.now(timezone.utc).isoformat(), 'model': MODEL,
              'endpoint': '/v1/messages/count_tokens', 'candidate_sha256': receipt['sha256'],
              'input_tokens': measured.input_tokens, 'baseline_tokens': baseline.input_tokens,
              'target_memory_tokens': 180000, 'generation_requests': 0,
              'status': 'MEASURED_DRAFT_NOT_DEPLOYED'}
    store(WORK / 'haiku_count.json', (json.dumps(result, indent=2) + '\n').encode())
    print(json.dumps(result))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status': 'FAILED', 'exception_type': type(exc).__name__}))
        raise SystemExit(1)
