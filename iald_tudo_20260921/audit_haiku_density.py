"""Measure draft density without changing the candidate or its canonical sources."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import os
import re

WORK = Path(__file__).resolve().parent
os.environ.setdefault('TIKTOKEN_CACHE_DIR', str(WORK / 'tokenizer_cache'))
import tiktoken


def main():
    raw = (WORK / 'haiku_candidate.md').read_bytes()
    receipt = json.loads((WORK / 'haiku_candidate.json').read_bytes())
    digest = hashlib.sha256(raw).hexdigest()
    if digest != receipt['sha256']:
        raise ValueError('Candidate hash mismatch')
    text = raw.decode('utf-8')
    enc = tiktoken.get_encoding('o200k_base')
    size = lambda value: len(enc.encode(value, disallowed_special=()))
    markers = list(re.finditer(r'(?m)^#{1,3} .+$', text))
    sections = []
    for i, match in enumerate(markers):
        end = markers[i + 1].start() if i + 1 < len(markers) else len(text)
        body = text[match.start():end]
        sections.append({'heading': match.group(0), 'chars': len(body), 'o200k_tokens': size(body)})
    lines = text.splitlines()
    repeated = Counter(line for line in lines if len(line) >= 80)
    duplicates = []
    for line, count in repeated.items():
        if count > 1:
            duplicates.append({'sha256': hashlib.sha256(line.encode()).hexdigest(),
                               'occurrences': count, 'chars': len(line),
                               'gross_duplicate_o200k_tokens': (count - 1) * size(line),
                               'math_or_code_marker': any(c in line for c in ('$', '\\', '`', '{'))})
    result = {'status': 'DENSITY_AUDIT_ONLY_NO_CONTENT_REMOVED', 'candidate_sha256': digest,
              'tokenizer': 'o200k_base_NOT_ANTHROPIC',
              'total_o200k_tokens': size(text),
              'before_first_heading_o200k_tokens': size(text[:markers[0].start()]),
              'largest_sections': sorted(sections, key=lambda x: x['o200k_tokens'], reverse=True)[:30],
              'duplicate_line_count': len(duplicates),
              'gross_duplicate_o200k_tokens': sum(x['gross_duplicate_o200k_tokens'] for x in duplicates),
              'duplicates': sorted(duplicates, key=lambda x: x['gross_duplicate_o200k_tokens'], reverse=True)}
    target = WORK / ('haiku_density_' + digest[:12] + '.json')
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode()
    if target.exists() and target.read_bytes() != payload:
        raise ValueError('Existing audit differs; preserve it')
    if not target.exists():
        with target.open('xb') as stream:
            stream.write(payload)
    print(json.dumps({k: v for k, v in result.items() if k != 'duplicates'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
