"""Independently undo declared draft transformations and compare all base bytes.

This verifies integration fidelity, not mathematical truth or semantic coverage.
No builder or assembler code is imported.
"""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re
import sys

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
def sha(raw):
    return hashlib.sha256(raw).hexdigest()
def require(ok, message):
    if not ok:
        raise ValueError(message)

def verify(path):
    path = Path(path).resolve()
    require(path.parent == WORK and path.name.startswith('haiku_reviewed_') and path.suffix == '.md', 'Invalid draft path')
    receipt = json.loads(path.with_suffix('.json').read_bytes())
    if receipt.get('topic_compaction_v6'):
        from verify_topic_v6_draft import verify_topics
        return verify_topics(path)
    if receipt.get('topic_compaction_v5'):
        from verify_topic_v5_draft import verify_topics
        return verify_topics(path)
    if receipt.get('runtime_synthesis_compaction'):
        from verify_runtime_draft import verify_runtime
        return verify_runtime(path)
    if receipt.get('topic_compaction_v4'):
        from verify_topic_v4_draft import verify_topics
        return verify_topics(path)
    if receipt.get('section_compaction'):
        from verify_section_draft import verify_section
        return verify_section(path)
    raw = path.read_bytes()
    require(sha(raw) == receipt['sha256'], 'Draft hash mismatch')
    base_raw = (WORK / 'haiku_candidate.md').read_bytes()
    require(sha(base_raw) == receipt['base_sha256'], 'Current base changed; verify against its original snapshot')
    base = base_raw.decode('utf-8')
    text = raw.decode('utf-8')
    manifest = json.loads((ROOT / 'iald_nucleo_fixo.json').read_bytes())
    entry = next(e for e in manifest['entries'] if e['id'] == 'resultado_publicado_integral')
    source_raw = Path(entry['path']).read_bytes()
    require(sha(source_raw) == entry['public_sha256'], 'Published source no longer matches manifest')
    seen = set()
    for row in receipt['reviewed_topics']:
        topic = row['topic']
        require(topic not in seen and re.fullmatch(r'[a-zA-Z0-9_]+', topic), 'Duplicate or invalid topic')
        seen.add(topic)
        require(row['source_sha256'] == sha(source_raw), 'Review source differs from current publication')
        capsule_raw = (WORK / 'semantic_capsules' / (topic + '.md')).read_bytes()
        require(sha(capsule_raw) == row['capsule_sha256'], 'Reviewed capsule drift')
        report_path = Path(row['review_path']).resolve()
        require(report_path.parent == WORK / 'adversarial_memory_review', 'Unexpected review location')
        report_raw = report_path.read_bytes()
        require(sha(report_raw) == row['review_sha256'], 'Review artifact drift')
        require('APROVADA quanto à fidelidade' in report_raw.decode('utf-8'), 'Expected focal approval absent')
        require(row['capsule_sha256'] in report_raw.decode('utf-8'), 'Approval does not name this capsule hash')
        pattern = (r'(?m)^### ' + re.escape(topic) + r'\nFonte: resultado_publicado_integral /core/'
                   + re.escape(topic) + r'\n[^\n]+')
        originals = list(re.finditer(pattern, base))
        require(len(originals) == 1, 'Missing or duplicate original topic')
        original = originals[0][0]
        require(sha(original.encode('utf-8')) == row['original_block_sha256'], 'Original topic differs from integration record')
        capsule = capsule_raw.decode('utf-8').rstrip('\r\n')
        require(text.count(capsule) == 1, 'Capsule missing, altered or duplicated in assembled text')
        text = text.replace(capsule, original, 1)
    if receipt.get('formatting_change'):
        marker = '\nESTADO DA PUBLICAÇÃO CONFERIDO NESTA REQUISIÇÃO — LEIA ANTES DE DIZER O QUE FALTA\n'
        require(text.count(marker) == base.count(marker) == 1, 'Evidence heading changed')
        source_start = base.index('\n{', base.index(marker) + len(marker)) + 1
        actual_start = text.index('\n{', text.index(marker) + len(marker)) + 1
        source_value, source_length = json.JSONDecoder().raw_decode(base[source_start:])
        actual_value, actual_length = json.JSONDecoder().raw_decode(text[actual_start:])
        require(actual_value == source_value, 'Evidence JSON changed beyond formatting')
        text = text[:actual_start] + base[source_start:source_start+source_length] + text[actual_start+actual_length:]
    require(text.encode('utf-8') == base_raw, 'Undeclared change outside approved transformations')
    require(path.read_bytes() == raw and (WORK/'haiku_candidate.md').read_bytes() == base_raw, 'Input changed during verification')
    return {'status':'DECLARED_TRANSFORMATIONS_VERIFIED_NOT_DEPLOYED','draft_sha256':sha(raw),
            'base_sha256':sha(base_raw),'reviewed_topics':sorted(seen),
            'all_other_base_bytes_preserved':True,'source_manifest_hash_matched':True,
            'scope':'Integration byte fidelity only; not global semantic approval, API fit or scientific proof.'}

if __name__ == '__main__':
    result = verify(sys.argv[1])
    target = WORK / ('reviewed_draft_verification_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json')
    with target.open('xb') as stream:
        stream.write((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
    print(json.dumps(result,ensure_ascii=False))
