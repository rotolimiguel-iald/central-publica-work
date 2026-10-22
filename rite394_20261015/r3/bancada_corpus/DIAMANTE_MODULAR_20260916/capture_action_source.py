from pathlib import Path
import datetime, hashlib, json, os

ROOT = Path(__file__).resolve().parent
paths = [Path(r'C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py'),
         Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\tgl_paper_unified.py')]
entries = []
for path in paths:
    raw = path.read_bytes()
    lines = raw.decode('utf-8-sig').splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith('def _latex_part_I_lagrangian_en(')]
    assert len(starts) == 1
    start = starts[0]
    end = next(i for i in range(start+1, len(lines)) if lines[i].startswith('def '))
    entries.append({'path': str(path), 'bytes': len(raw),
                    'sha256': hashlib.sha256(raw).hexdigest(),
                    'start_line': start+1, 'end_line': end,
                    'excerpt': '\n'.join(lines[start:end])})
dest = ROOT / 'TGL_ACTION_SOURCE_EXCERPTS.json'
assert not dest.exists()
raw = json.dumps({'timestamp': datetime.datetime.now().astimezone().isoformat(),
                  'status': 'SOURCE_READ_NOT_EXECUTED', 'entries': entries},
                 ensure_ascii=False, indent=2).encode('utf8')
tmp = dest.with_suffix('.json.tmp')
tmp.write_bytes(raw); assert tmp.read_bytes() == raw
os.replace(tmp, dest)
print(json.dumps({'sources': len(entries), 'output': str(dest)}))
