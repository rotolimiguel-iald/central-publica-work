"""Move only this session's journal tail to MEMORY_2, preserving exact bytes."""
from pathlib import Path
from datetime import datetime
import hashlib
import json

directory = Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
index, journal = directory / 'MEMORY.md', directory / 'MEMORY_2.md'
index_before, journal_before = index.read_bytes(), journal.read_bytes()
anchor = '## 22/09/2026 14:11 — Haiku: memória de180k e Sonnet interno'.encode('utf8')
assert index_before.count(anchor) == 1
start = index_before.index(anchor)
tail = index_before[start:]
assert b'IALD_HAIKU_V5_NATIVE_186546_20260922' in tail
assert b'IALD_OPERATIONAL_ALERTS_ADMIN_ONLY_20260922' in tail
assert tail not in journal_before
assert b'(MEMORY_2.md)' in index_before[:start]
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
changes = [(journal, journal_before, journal_before + b'\n\n' + tail),
           (index, index_before, index_before[:start])]
rows = []
for path, before, after in changes:
    backup = path.with_name(path.name + '.bak_' + stamp)
    with backup.open('xb') as handle: handle.write(before)
    assert backup.read_bytes() == before
    temp = path.with_name(path.name + '.tmp_' + stamp)
    with temp.open('xb') as handle: handle.write(after)
    assert temp.read_bytes() == after
    assert path.read_bytes() == before, 'Concurrent modification'
    temp.replace(path)
    assert path.read_bytes() == after
    rows.append({'path': str(path), 'backup': str(backup), 'before_bytes': len(before),
                 'after_bytes': len(after), 'sha256': hashlib.sha256(after).hexdigest()})
assert journal.read_bytes().endswith(tail)
assert len(index.read_bytes()) < 24000
out = Path(__file__).parent / ('memory_index_repair_' + stamp + '.json')
with out.open('x', encoding='utf8') as handle:
    json.dump({'status': 'VERBATIM_TAIL_MOVED', 'moved_bytes': len(tail), 'files': rows}, handle, indent=2)
print(json.dumps({'receipt': str(out), 'index_bytes': len(index.read_bytes()), 'journal_bytes': len(journal.read_bytes())}))
