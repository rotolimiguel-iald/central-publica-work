"""Summarize the auditor-guard logs of the final run: event kinds and the files read outside the folder."""
import collections, json, sys
from pathlib import Path
root = Path(sys.argv[1])
kinds, reads, blocks = collections.Counter(), collections.Counter(), []
for log in sorted((root / 'guard_log').glob('*.jsonl')):
    for line in log.read_text('utf-8').splitlines():
        try:
            d = json.loads(line)
        except Exception:
            continue
        kinds[d['kind']] += 1
        if d['kind'] == 'READ_OUTSIDE':
            reads[str(Path(d['path']).parent)[:100]] += 1
        if d['kind'].startswith('BLOCK_'):
            blocks.append({'kind': d['kind'], 'path': d.get('path')})
summary = {'logs': len(list((root / 'guard_log').glob('*.jsonl'))), 'kinds': dict(kinds),
           'reads_outside_by_dir': reads.most_common(20), 'blocks': blocks}
(root / 'evidencias' / 'guarda_resumo.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=1))
