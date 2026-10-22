"""Read-only inventory of exact repeated source strings in topic JSON blocks."""
from collections import Counter
from pathlib import Path
import json
import re
import os
os.environ.setdefault('TIKTOKEN_CACHE_DIR', r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\tokenizer_cache')
import tiktoken

W = Path(__file__).resolve().parent
P = W / 'haiku_reviewed_section_20260922_130747_311801.md'
text = P.read_bytes().decode()
counter = Counter()
def walk(node):
    if isinstance(node, str):
        if len(node) >= 80:
            counter[node] += 1
    elif isinstance(node, list):
        for child in node:
            walk(child)
    elif isinstance(node, dict):
        if any(k in node for k in ('@TGL_LITERAL', '@EXPOSITION', '@SUMMARY')):
            return
        for k, child in node.items():
            if k != '@':
                walk(child)
for m in re.finditer(r'(?m)^### [^\n]+\nFonte: resultado_publicado_integral [^\n]+\n([^\n]+)', text):
    try:
        value = json.loads(m[1])
    except json.JSONDecodeError:
        continue
    walk(value)
enc = tiktoken.get_encoding('o200k_base')
rows = []
for s, n in counter.items():
    if n < 2:
        continue
    tokens = len(enc.encode(json.dumps(s, ensure_ascii=False)))
    saving = (n - 1) * tokens - 15 * n - 8
    if saving > 0:
        rows.append({'count': n, 'o200k_tokens': tokens, 'estimated_saving': saving,
                     'prefix': s[:150]})
rows.sort(key=lambda x: -x['estimated_saving'])
print(json.dumps({'candidate_strings': len(rows),
    'estimated_total_o200k_saving': sum(r['estimated_saving'] for r in rows),
    'top': rows[:20]}, ensure_ascii=False, indent=2))
