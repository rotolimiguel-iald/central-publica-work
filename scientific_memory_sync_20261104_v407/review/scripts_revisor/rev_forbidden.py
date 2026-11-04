import sys, json, sqlite3, re
sys.dont_write_bytecode = True
from pathlib import Path
from contextlib import closing
BASE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
sys.path.insert(0, str(BASE))
from iald_orchestrator import canonical_memory as cm
from iald_orchestrator.policy import FORBIDDEN
res = {}
for ep in ('v404_302dc102683e9fb1', 'v407_4323b401f15cc971'):
    uri = (cm.RELEASES / ep / 'index.sqlite3').resolve().as_uri() + '?mode=ro'
    per = {}
    with closing(sqlite3.connect(uri, uri=True)) as db:
        for rid, doc, body, a, b in db.execute('SELECT rowid, document, body, first_line, last_line FROM passages'):
            if FORBIDDEN.search(body):
                per.setdefault(doc, []).append((int(a), int(b)))
    res[ep] = {d: len(v) for d, v in per.items()}
    res[ep + '_first_hits'] = {d: v[:3] for d, v in per.items()}
print(json.dumps(res, ensure_ascii=False, indent=1))
Path(r'C:\IALD\Central de Patentes\work\scientific_memory_sync_20261104_v407\review\REV_FORBIDDEN_SCAN.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
