# -*- coding: utf-8 -*-
"""E3b: rebuild from the journals of the randomly-killed root B; heads must equal the database; malformed lines visible."""
import json, shutil
from pathlib import Path
from common import RUNS, dump
from iald_memory import migrate, journal as J
root = RUNS / 'e3_crash' / 'B' / 'state'
out = RUNS / 'e3_crash' / 'B_rebuild'
if out.exists():
    shutil.rmtree(out)
rep = migrate.rebuild_from_journal(root / 'journal', out / 'state', snapshot_archive_dir=out / 'arquivo_D')
orig = migrate._summarize(migrate.verify_all(root, deep=True, snapshot_archive_dir=root.parent / 'arquivo_D'))
cmp = {c: (rep['contexts'][c]['head_event_hash'] == orig[c]['receipt']['event_hash'],
           rep['contexts'][c]['head_revision'] == orig[c]['receipt']['revision']) for c in orig}
mal = {p.name: J.verify_chain(p, [])['malformed_lines'] for p in (root / 'journal').glob('*.jsonl')}
a2 = RUNS / 'e3_crash' / 'A2' / 'state' / 'journal'
mal_a2 = {p.name: J.read_all(p)[1] for p in a2.glob('*.jsonl')}
from iald_memory import MemoryStore
from common import SCOPE
v = MemoryStore(a2.parent, snapshot_archive_dir=a2.parent.parent / 'arquivo_D').verify('ctx.a', SCOPE)
res = {'rebuild_ok': rep['ok'], 'heads_equal': cmp, 'malformed_B': mal, 'malformed_A2': mal_a2,
       'A2_verify_malformed_field': v['journal_malformed_lines'], 'A2_verify_ok': v['ok'],
       'summarize_has_malformed_key': 'journal_malformed_lines' in migrate._summarize({'x': v})['x']}
dump(RUNS / 'e3b_rebuild.json', res)
print(json.dumps(res))
