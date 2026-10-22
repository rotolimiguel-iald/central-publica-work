"""Count an explicit reviewed draft at the authorized Anthropic endpoint."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys
from dotenv import dotenv_values
import anthropic

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
MODEL = 'claude-haiku-4-5-20251001'

def main():
    path = Path(sys.argv[1]).resolve()
    if path.parent != WORK or not path.name.startswith('haiku_reviewed_') or path.suffix != '.md':
        raise ValueError('Only an explicit local reviewed draft is accepted')
    receipt = json.loads(path.with_suffix('.json').read_bytes())
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != receipt['sha256'] or receipt['status'] != 'PARTIALLY_REVIEWED_DRAFT_NOT_DEPLOYED':
        raise ValueError('Draft hash or type mismatch')
    text = raw.decode('utf-8')
    if '<ATLAS_CANONICO' in text:
        raise ValueError('Private Atlas forbidden')
    key = dotenv_values(ROOT / '.env').get('IALD_CLAUDE_API_KEY')
    if not key:
        raise ValueError('Anthropic credential absent')
    with anthropic.Anthropic(api_key=key, max_retries=0, timeout=120) as client:
        base = client.messages.count_tokens(model=MODEL, system='.', messages=[{'role':'user','content':'.'}])
        measured = client.messages.count_tokens(model=MODEL, system=text, messages=[{'role':'user','content':'.'}])
    result = {'time_utc':datetime.now(timezone.utc).isoformat(), 'model':MODEL,
              'endpoint':'/v1/messages/count_tokens', 'candidate_sha256':digest,
              'candidate_path':str(path), 'input_tokens':measured.input_tokens,
              'baseline_tokens':base.input_tokens, 'generation_requests':0,
              'status':'MEASURED_REVIEWED_DRAFT_NOT_DEPLOYED',
              'scope':'Prefix plus minimal user message; no tools, history or output reserve included.'}
    target = WORK / ('haiku_reviewed_count_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.json')
    with target.open('xb') as stream:
        stream.write((json.dumps(result, ensure_ascii=False, indent=2)+'\n').encode())
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status':'FAILED', 'exception_type':type(exc).__name__}))
        raise SystemExit(1)
