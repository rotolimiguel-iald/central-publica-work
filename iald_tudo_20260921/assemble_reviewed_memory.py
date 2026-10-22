"""Assemble explicitly reviewed capsules into a separate draft; fail on drift."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
# This allowlist records a human-readable independent review already inspected.
# Finding an arbitrary file or an approval-looking source string grants nothing.
REVIEWS = [('contour_theory', 'PARECER_CONTOUR_THEORY_V2.md',
            'contour_focal_v2_measurements.json'),
           ('interface_is_light', 'PARECER_INTERFACE_IS_LIGHT_V2.md',
            'interface_focal_v2_measurements.json')]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def verify_capsule(raw, source_raw, measurement, review_raw):
    if sha(raw) != measurement['capsule_sha256']:
        raise ValueError('Capsule changed after independent review')
    if sha(source_raw) != measurement['source_sha256']:
        raise ValueError('Source changed after independent review')
    review = review_raw.decode('utf-8')
    if 'APROVADA quanto à fidelidade' not in review or measurement['capsule_sha256'] not in review:
        raise ValueError('Expected focal approval absent')

def replace_topic(text, topic, capsule):
    pattern = re.compile(r'(?m)^### ' + re.escape(topic) +
                         r'\nFonte: resultado_publicado_integral /core/' + re.escape(topic) +
                         r'\n[^\n]+')
    hits = list(pattern.finditer(text))
    if len(hits) != 1:
        raise ValueError('Expected exactly one original topic')
    hit = hits[0]
    original = hit[0]
    replacement = capsule.rstrip('\r\n')
    assembled = text[:hit.start()] + replacement + text[hit.end():]
    if assembled[:hit.start()] != text[:hit.start()] or assembled[hit.start()+len(replacement):] != text[hit.end():]:
        raise ValueError('Unrelated content changed')
    return assembled, original

def write_new(path, raw):
    with path.open('xb') as stream:
        stream.write(raw)
    if path.read_bytes() != raw:
        raise ValueError('Output verification failed')

def main():
    base_raw = (WORK / 'haiku_candidate.md').read_bytes()
    base = json.loads((WORK / 'haiku_candidate.json').read_bytes())
    if sha(base_raw) != base['sha256']:
        raise ValueError('Base draft drift')
    manifest = json.loads((ROOT / 'iald_nucleo_fixo.json').read_bytes())
    entry = next(e for e in manifest['entries'] if e['id'] == 'resultado_publicado_integral')
    source_raw = Path(entry['path']).read_bytes()
    if sha(source_raw) != entry['public_sha256']:
        raise ValueError('Published source hash mismatch')
    text = base_raw.decode('utf-8')
    incorporated = []
    for topic, report_name, measurement_name in REVIEWS:
        review_path = WORK / 'adversarial_memory_review' / report_name
        measure_path = review_path.with_name(measurement_name)
        capsule_path = WORK / 'semantic_capsules' / (topic + '.md')
        capsule_raw = capsule_path.read_bytes()
        measure = json.loads(measure_path.read_bytes())
        review_raw = review_path.read_bytes()
        verify_capsule(capsule_raw, source_raw, measure, review_raw)
        text, old = replace_topic(text, topic, capsule_raw.decode('utf-8'))
        incorporated.append({'topic': topic, 'source_pointer': '/core/' + topic,
                             'source_sha256': sha(source_raw), 'capsule_sha256': sha(capsule_raw),
                             'review_path': str(review_path), 'review_sha256': sha(review_raw),
                             'original_block_sha256': sha(old.encode('utf-8'))})
    marker = '\n## Exposição canônica integral: fórmulas e derivações'
    if text.split(marker, 1)[1] != base_raw.decode('utf-8').split(marker, 1)[1]:
        raise ValueError('Exposition changed')
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    target = WORK / ('haiku_reviewed_' + stamp + '.md')
    output = text.encode('utf-8')
    result = {'status': 'PARTIALLY_REVIEWED_DRAFT_NOT_DEPLOYED', 'base_sha256': sha(base_raw),
              'sha256': sha(output), 'path': str(target), 'reviewed_topics': incorporated,
              'unchanged_other_topics': base['topic_count'] - len(incorporated),
              'kernel_core_exposition_unchanged': True, 'anthropic_tokens': None,
              'semantic_review_scope': 'Only the listed capsules; no global approval or retrieval test.'}
    write_new(target, output)
    write_new(target.with_suffix('.json'), (json.dumps(result, ensure_ascii=False, indent=2)+'\n').encode())
    if (WORK / 'haiku_candidate.md').read_bytes() != base_raw:
        raise ValueError('Original draft changed during assembly')
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
