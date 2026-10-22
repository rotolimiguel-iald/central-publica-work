"""Measure reversible in-context references; no API, deployment or source edits."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import re

WORK = Path(__file__).resolve().parent
os.environ.setdefault('TIKTOKEN_CACHE_DIR', r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\tokenizer_cache')
import tiktoken
enc = tiktoken.get_encoding('o200k_base')
def js(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))
def tokens(value):
    return len(enc.encode(value, disallowed_special=()))
def digest(raw):
    return hashlib.sha256(raw).hexdigest()

raw = (WORK / 'haiku_candidate.md').read_bytes()
receipt = json.loads((WORK / 'haiku_candidate.json').read_bytes())
assert digest(raw) == receipt['sha256']
text = raw.decode('utf-8')
marker = '\n## Exposição canônica integral: fórmulas e derivações'
exposition = text.split(marker, 1)[1][:receipt['exposition_chars']]
assert digest(exposition.encode()) == receipt['exposition_sha256']
changes = []
count = 0

def compact(node):
    global count
    if isinstance(node, str) and len(node) >= 60:
        start = exposition.find(node)
        if start >= 0:
            replacement = {'@LOADED_EXPOSITION': [start, len(node)]}
            if tokens(js(node)) > tokens(js(replacement)) + 12:
                count += 1
                return replacement
    if isinstance(node, dict):
        # Existing typed references are left intact, including their locators.
        if any(key.startswith('@') for key in node):
            return node
        return {key: compact(value) for key, value in node.items()}
    if isinstance(node, list):
        return [compact(value) for value in node]
    return node

def restore(node):
    if isinstance(node, dict):
        if set(node) == {'@LOADED_EXPOSITION'}:
            start, size = node['@LOADED_EXPOSITION']
            assert type(start) is int and type(size) is int
            assert start >= 0 and size > 0 and start + size <= len(exposition)
            return exposition[start:start+size]
        return {key: restore(value) for key, value in node.items()}
    if isinstance(node, list):
        return [restore(value) for value in node]
    return node

matches = list(re.finditer(r'(?m)^### ([^\n]+)\nFonte: resultado_publicado_integral ([^\n]+)\n([^\n]+)', text))
assert len(matches) == receipt['topic_count'] == 325
for match in matches:
    before = json.loads(match[3])
    after = compact(before)
    assert restore(after) == before
    changes.append((match.start(3), match.end(3), js(after)))

glossary_marker = 'a referência preserva o valor, não acrescenta estatuto.\n'
start = text.index(glossary_marker) + len(glossary_marker)
end = text.index('\n', start)
before = json.loads(text[start:end])
after = compact(before)
assert restore(after) == before
changes.append((start, end, js(after)))
variant = text
for start, end, replacement in sorted(changes, reverse=True):
    variant = variant[:start] + replacement + variant[end:]
assert variant.split(marker, 1)[1][:receipt['exposition_chars']] == exposition
note = ('REFERÊNCIA INTERNA ADICIONAL: @LOADED_EXPOSITION=[offset,comprimento] representa texto literal já carregado na exposição. '
        'Índices em caracteres Unicode a partir de imediatamente após seu título principal, incluindo a quebra de linha. '
        'Não é conteúdo removido nem busca externa. As fórmulas permanecem na exposição integral.\n')
variant = note + variant
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
target = WORK / ('haiku_lossless_' + stamp + '.md')
payload = variant.encode('utf-8')
with target.open('xb') as stream:
    stream.write(payload)
assert target.read_bytes() == payload
result = {'status': 'REVERSIBLE_DRAFT_NOT_DEPLOYED', 'base_sha256': receipt['sha256'],
          'variant_path': str(target), 'variant_sha256': digest(payload),
          'base_o200k': tokens(text), 'variant_o200k': tokens(variant),
          'saved_o200k': tokens(text)-tokens(variant), 'new_references': count,
          'topics_roundtrip_exact': len(matches), 'glossary_roundtrip_exact': True,
          'exposition_unchanged': True, 'anthropic_tokens': None,
          'scope': 'Exact JSON value recovery verified; model usability and Anthropic budget unverified.'}
record = target.with_suffix('.json')
with record.open('xb') as stream:
    stream.write((json.dumps(result, ensure_ascii=False, indent=2)+'\n').encode())
assert (WORK / 'haiku_candidate.md').read_bytes() == raw
print(json.dumps(result, ensure_ascii=False))
