"""Measure unused generated glossary entries without changing any draft."""
from pathlib import Path
import json
import hashlib
import re
import os
os.environ.setdefault('TIKTOKEN_CACHE_DIR', r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\tokenizer_cache')
import tiktoken

work = Path(__file__).resolve().parent
raw = (work / 'haiku_candidate.md').read_bytes()
receipt = json.loads((work / 'haiku_candidate.json').read_bytes())
assert hashlib.sha256(raw).hexdigest() == receipt['sha256']
text = raw.decode()
marker = 'a referência preserva o valor, não acrescenta estatuto.\n'
start = text.index(marker) + len(marker)
end = text.index('\n', start)
glossary = json.loads(text[start:end])
used = set()
def walk(node):
    if isinstance(node, dict):
        if '@TGL_LITERAL' in node:
            assert set(node) == {'@TGL_LITERAL'}
            assert node['@TGL_LITERAL'] in glossary
            used.add(node['@TGL_LITERAL'])
        for value in node.values():
            walk(value)
    elif isinstance(node,list):
        for value in node:
            walk(value)
matches = list(re.finditer(r'(?m)^### ([^\n]+)\nFonte: resultado_publicado_integral ([^\n]+)\n([^\n]+)', text))
assert len(matches) == 325
for match in matches:
    walk(json.loads(match[3]))
exposition_marker = '\n## Exposição canônica integral: fórmulas e derivações'
exposition = text.split(exposition_marker, 1)[1][:receipt['exposition_chars']]
unused = set(glossary) - used
enc = tiktoken.get_encoding('o200k_base')
size = lambda s: len(enc.encode(s, disallowed_special=()))
result = {'candidate_sha256':receipt['sha256'], 'glossary_entries':len(glossary),
          'used_entries':len(used), 'unused_entries':len(unused),
          'unused_literal_present_in_exposition':sum(glossary[k] in exposition for k in unused),
          'unused_not_in_exposition':[k for k in sorted(unused) if glossary[k] not in exposition],
          'glossary_o200k':size(text[start:end]),
          'used_glossary_o200k':size(json.dumps({k:v for k,v in glossary.items() if k in used},ensure_ascii=False,separators=(',',':'))),
          'unused_ids':sorted(unused), 'status':'MEASUREMENT_ONLY'}
print(json.dumps(result,ensure_ascii=False))
