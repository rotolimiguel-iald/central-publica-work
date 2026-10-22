"""Record provenance and size of a proposed semantic capsule, without installing it."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
os.environ.setdefault('TIKTOKEN_CACHE_DIR', str(ROOT / '.iald_runtime/tokenizer_cache'))
import tiktoken

manifest = json.loads((ROOT / 'iald_nucleo_fixo.json').read_bytes())
entry = next(e for e in manifest['entries'] if e['id'] == 'resultado_publicado_integral')
raw = Path(entry['path']).read_bytes()
assert hashlib.sha256(raw).hexdigest() == entry['public_sha256']
topic = json.loads(raw)['core']['contour_theory']
candidate_raw = (WORK / 'haiku_candidate.md').read_bytes()
receipt = json.loads((WORK / 'haiku_candidate.json').read_bytes())
assert hashlib.sha256(candidate_raw).hexdigest() == receipt['sha256']
candidate = candidate_raw.decode('utf-8')
original = '### contour_theory\n' + candidate.split('### contour_theory\n', 1)[1].split('\n### ', 1)[0]
capsule_raw = (HERE / 'contour_theory.md').read_bytes()
capsule = capsule_raw.decode('utf-8')
enc = tiktoken.get_encoding('o200k_base')
size = lambda value: len(enc.encode(value, disallowed_special=()))
result = {'status': 'PROPOSED_SEMANTIC_CAPSULE_NOT_INTEGRATED_NOT_APPROVED',
          'source_id': entry['id'], 'source_sha256': entry['public_sha256'],
          'source_pointer': '/core/contour_theory', 'source_fields': list(topic),
          'source_topic_sha256': hashlib.sha256(json.dumps(topic, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
          'candidate_sha256': receipt['sha256'], 'capsule_sha256': hashlib.sha256(capsule_raw).hexdigest(),
          'old_o200k_tokens': size(original), 'new_o200k_tokens': size(capsule),
          'saved_o200k_tokens': size(original) - size(capsule), 'anthropic_tokens': None,
          'reviewer_agent': '01a0c97e-fb7b-7510-8d5d-1ec2bbea845e',
          'scope': 'Size and provenance only; semantic approval is separate.'}
path = HERE / ('contour_provenance_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.json')
with path.open('xb') as stream:
    stream.write((json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode())
print(json.dumps({'receipt': str(path), 'old': result['old_o200k_tokens'], 'new': result['new_o200k_tokens'], 'saved': result['saved_o200k_tokens']}))
