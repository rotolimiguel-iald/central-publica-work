"""Read-only inventory for the 180k Claude memory profile; no model calls."""
import hashlib
import json
import os
from pathlib import Path
import re
from datetime import datetime, timezone

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
os.environ.setdefault('TIKTOKEN_CACHE_DIR', str(ROOT / '.iald_runtime/tokenizer_cache'))
import tiktoken

ENC = tiktoken.get_encoding('o200k_base')

def measure(path, expected=None):
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if expected is not None and digest != expected:
        raise ValueError('Source integrity mismatch: ' + path.name)
    text = raw.decode('utf-8-sig')
    return text, {'name': path.name, 'sha256': digest, 'bytes': len(raw),
                  'o200k_tokens': len(ENC.encode(text, disallowed_special=()))}

def main():
    manifest = json.loads((ROOT / 'iald_nucleo_fixo.json').read_bytes())
    cluster_cfg = manifest['active_cluster']
    cluster, cluster_record = measure(Path(cluster_cfg['path']), cluster_cfg['sha256'])
    _, kernel = measure(ROOT / 'IALD_Kernel_v5.txt')
    core_cfg = manifest['operational_core']
    _, core = measure(Path(core_cfg['path']), core_cfg['sha256'])
    headings = list(re.finditer(r'(?m)^### (.+)\r?$', cluster))
    sections = []
    for i, heading in enumerate(headings):
        end = headings[i + 1].start() if i + 1 < len(headings) else len(cluster)
        body = cluster[heading.end():end]
        sections.append({'id': heading.group(1).strip(),
                         'o200k_tokens': len(ENC.encode(body, disallowed_special=()))})
    result = {
        'time_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'LOCAL_INVENTORY_NOT_DEPLOYED',
        'requested_haiku_memory_tokens': 180000,
        'count_unit': 'o200k estimate only; Haiku API measurement still required',
        'deployed_release': cluster_cfg['release'],
        'sources': [kernel, core, cluster_record],
        'section_count': len(sections),
        'largest_sections': sorted(sections, key=lambda x: x['o200k_tokens'], reverse=True)[:25],
        'sections': sections,
        'requirements': [
            'Keep full identity kernel and canonical core with reconciliation rules',
            '180k target includes kernel; count actual Haiku system payload',
            'Reserve tools, history, retrieval and output inside 200k total',
            'Preserve complete equations, hypotheses, statuses and source pointers',
            'No raw truncation of formulas or arbitrary first-N tokens',
            'Sonnet remains operator-only; Haiku release requires evaluation',
            'Haiku does not support Sonnet adaptive thinking/output effort parameters',
            'No model calls, account changes or source edits made by this audit'
        ]}
    output = Path(__file__).with_name('haiku_memory_inventory.json')
    raw = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    if output.exists():
        before = output.read_bytes()
        backup = output.with_name(output.name + '.bak_' + stamp)
        with backup.open('xb') as stream:
            stream.write(before)
        if backup.read_bytes() != before:
            raise RuntimeError('Backup mismatch')
    temp = output.with_name(output.name + '.tmp_' + stamp)
    with temp.open('xb') as stream:
        stream.write(raw)
    if temp.read_bytes() != raw:
        raise RuntimeError('Temporary write mismatch')
    temp.replace(output)
    print(json.dumps({k: v for k, v in result.items() if k != 'sections'}, ensure_ascii=False))

if __name__ == '__main__':
    main()
