"""Read Anthropic model metadata; no prompts or generation, no secret output."""
from pathlib import Path
import sys, json
from datetime import datetime, timezone
sys.path.insert(0, 'C:/Users/rotol/AppData/Roaming/Python/Python314/site-packages')
from dotenv import dotenv_values
import anthropic

root = Path(r'C:\IALD\projetos_pyhton\IALD')
out = Path(__file__).resolve().parent
try:
    key = dotenv_values(root / '.env').get('IALD_CLAUDE_API_KEY')
    assert key
    with anthropic.Anthropic(api_key=key, max_retries=0, timeout=30) as client:
        result = client.models.retrieve('claude-haiku-5-5').model_dump(mode='json')
    result = {'utc': datetime.now(timezone.utc).isoformat(), 'metadata': result,
              'generation_requests': 0}
    blob = json.dumps(result, ensure_ascii=False, indent=2).encode()
    dest = out / 'anthropic_model_metadata.json'
    assert not dest.exists()
    dest.write_bytes(blob)
    print(blob.decode())
except Exception as exc:
    print(json.dumps({'status': 'FAILED', 'type': type(exc).__name__,
                      'http_status': getattr(exc, 'status_code', None)}))
    sys.exit(1)
