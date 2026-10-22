"""Remove JSON indentation only from the generated evidence block of a draft."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import sys
os.environ.setdefault('TIKTOKEN_CACHE_DIR', r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\tokenizer_cache')
import tiktoken

WORK = Path(__file__).resolve().parent
path = Path(sys.argv[1]).resolve()
assert path.parent == WORK and path.name.startswith('haiku_reviewed_') and path.suffix == '.md'
raw = path.read_bytes()
receipt = json.loads(path.with_suffix('.json').read_bytes())
digest = hashlib.sha256(raw).hexdigest()
assert digest == receipt['sha256']
text = raw.decode('utf-8')
marker = '\nESTADO DA PUBLICAÇÃO CONFERIDO NESTA REQUISIÇÃO — LEIA ANTES DE DIZER O QUE FALTA\n'
assert text.count(marker) == 1
start = text.index('\n{', text.index(marker)+len(marker)) + 1
value, length = json.JSONDecoder().raw_decode(text[start:])
assert value['scope'] == 'PUBLIC_RELEASE_RECORDS_HASH_MATCHED__COMPILER_NOT_RERUN'
assert 'sources' in value and 'current_gate' in value and 'constructed_hypotheses' in value
replacement = json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
assert json.loads(replacement) == value
output = text[:start] + replacement + text[start+length:]
assert output[:start] == text[:start] and output[start+len(replacement):] == text[start+length:]
enc = tiktoken.get_encoding('o200k_base')
size = lambda s:len(enc.encode(s, disallowed_special=()))
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
target = WORK / ('haiku_reviewed_compact_evidence_'+stamp+'.md')
new = output.encode('utf-8')
result = dict(receipt)
result.update({'path':str(target),'sha256':hashlib.sha256(new).hexdigest(),
               'previous_reviewed_draft_sha256':digest,'anthropic_tokens':None,
               'formatting_change':{'scope':'generated_publication_evidence_json_only',
                    'decoded_values_equal':True,'other_bytes_equal':True,
                    'old_o200k':size(text[start:start+length]),'new_o200k':size(replacement),
                    'saved_o200k':size(text)-size(output)},'o200k_tokens':size(output)})
with target.open('xb') as stream:
    stream.write(new)
assert target.read_bytes() == new and path.read_bytes() == raw
with target.with_suffix('.json').open('xb') as stream:
    stream.write((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({k:result[k] for k in ('path','sha256','formatting_change','o200k_tokens','anthropic_tokens')},ensure_ascii=False))
