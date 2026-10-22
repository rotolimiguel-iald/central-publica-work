"""Verify source references and source preservation, not semantic completeness."""
import hashlib
import json
import re
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
manifest = json.loads((ROOT / 'iald_nucleo_fixo.json').read_bytes())
receipt = json.loads((WORK / 'haiku_candidate.json').read_bytes())
raw = (WORK / 'haiku_candidate.md').read_bytes()
assert hashlib.sha256(raw).hexdigest() == receipt['sha256']
entry = next(e for e in manifest['entries'] if e['id'] == 'resultado_publicado_integral')
source_raw = Path(entry['path']).read_bytes()
assert hashlib.sha256(source_raw).hexdigest() == entry['public_sha256']
source = json.loads(source_raw)
references = receipt['topics'] + receipt['omitted_numeric_series']
for reference in references:
    node = source
    for part in reference['pointer'].split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        node = node[int(part)] if isinstance(node, list) else node[part]
text = raw.decode('utf-8')
from build_haiku_candidate import capsule, compact_references
from iald_kernel import KernelCatalog
catalog = KernelCatalog(manifest['active_cluster']['kernel_bundle'])
assert len(receipt['fixed_hypothesis_sources']) == len(manifest['published_evidence']['hypothesis_sources'])
for evidence in receipt['fixed_hypothesis_sources']:
    lean = catalog._read_checked(evidence['path'])
    assert lean in text, 'Missing full nuclear Lean source'
    assert hashlib.sha256(lean.encode()).hexdigest() == evidence['sha256']
glossary_line = text.split('a referência preserva o valor, não acrescenta estatuto.\n', 1)[1].split('\n', 1)[0]
glossary = json.loads(glossary_line)
original_cluster = Path(manifest['active_cluster']['path']).read_text(encoding='utf-8')
exposition = original_cluster.split('## Exposição canônica integral: fórmulas e derivações', 1)[1]
selected_exposition = text.split('## Exposição canônica integral: fórmulas e derivações\n', 1)[1]
loaded_exposition = text.split('\n## Exposição canônica integral: fórmulas e derivações', 1)[1][:receipt['exposition_chars']]
assert hashlib.sha256(loaded_exposition.encode('utf-8')).hexdigest() == receipt['exposition_sha256']
audit_entry = next(e for e in manifest['entries'] if e['id'] == receipt['audit_ladder_source_id'])
audit_raw = Path(audit_entry['path']).read_bytes()
assert hashlib.sha256(audit_raw).hexdigest() == receipt['audit_ladder_source_sha256']
audit_text = audit_raw.decode('utf-8-sig')
allowed_removed_lines = set()
for row in receipt['audit_ladder_offsets']:
    selected = audit_text[row['offset']:row['offset'] + row['chars']]
    assert re.fullmatch(r'- `[^`\n]+` = `[^`\n]+`', selected)
    assert selected in exposition
    allowed_removed_lines.add(selected)
for row in receipt['deduplicated_verdicts']:
    assert source['core'][row['topic']]['verdict'] == row['value']
    allowed_removed_lines.add('**Estatutos [' + row['heading'] + ']** (veredito: `' + row['value'] + '`):')
preserved_lines = 0
for line in exposition.splitlines():
    if line.strip() and line not in allowed_removed_lines:
        assert line in selected_exposition, 'Unapproved exposition omission'
        preserved_lines += 1
# Every display-math block survives literally. This is preservation, not proof validation.
math_blocks = re.findall(r'\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]', exposition)
for block in math_blocks:
    assert block in selected_exposition
from iald_core_indexado import DocumentCorpus
corpus = DocumentCorpus(ROOT / 'iald_nucleo_fixo.json')
for row in (receipt['audit_ladder_offsets'][0], receipt['audit_ladder_offsets'][-1]):
    fetched = corpus.fetch(receipt['audit_ladder_source_id'], offset=row['offset'], max_chars=row['chars'])
    assert fetched['text'] == audit_text[row['offset']:row['offset']+row['chars']]
    assert not fetched['whole_document']
def compare(expected, actual):
    if isinstance(actual, dict) and set(actual) == {'@TGL_LITERAL'}:
        assert expected == glossary[actual['@TGL_LITERAL']]
        return
    if isinstance(actual, dict) and set(actual) == {'@EXPOSITION', 'starts_with', 'span'}:
        start, length = actual['span']
        assert type(start) is int and type(length) is int and start >= 0 and length > 0
        assert start + length <= len(loaded_exposition)
        assert loaded_exposition[start:start + length] == expected
        assert expected.startswith(actual['starts_with'])
        headings = re.findall(r'(?m)^#{1,6} .+$', loaded_exposition[:start])
        assert actual['@EXPOSITION'] == (headings[-1] if headings else '## Exposição canônica integral: fórmulas e derivações')
        return
    assert type(expected) is type(actual)
    if isinstance(expected, dict):
        assert expected.keys() == actual.keys()
        for key in expected:
            compare(expected[key], actual[key])
    elif isinstance(expected, list):
        assert len(expected) == len(actual)
        for left, right in zip(expected, actual):
            compare(left, right)
    else:
        assert expected == actual
for topic in receipt['topics']:
    heading = '\n### ' + topic['id'] + '\nFonte: resultado_publicado_integral ' + topic['pointer'] + '\n'
    assert text.count(heading) == 1
    actual = json.loads(text.split(heading, 1)[1].split('\n', 1)[0])
    expected = compact_references(capsule(source['core'][topic['id']], topic['pointer']), topic['pointer'])
    compare(expected, actual)
for name in ('mother_instruction', 'operational_core'):
    cfg = manifest[name]
    original = Path(cfg['path']).read_bytes()
    assert hashlib.sha256(original).hexdigest() == cfg['sha256']
    assert original.decode('utf-8-sig') in text
assert len(receipt['topics']) == manifest['active_cluster']['core_sections']
assert len({r['id'] for r in receipt['topics']}) == len(receipt['topics'])
print(json.dumps({'verified_references': len(references), 'topics': len(receipt['topics']),
                  'kernel_and_core_complete': True, 'semantic_coverage': 'NOT_YET_AUDITED',
                  'nuclear_lean_sources_full': len(receipt['fixed_hypothesis_sources']),
                  'compact_values_equivalent': True, 'display_math_blocks_preserved': len(math_blocks),
                  'exposition_lines_preserved_except_audit_metadata': preserved_lines,
                  'audit_offset_fetch_checked': True, 'deployed': False}))
