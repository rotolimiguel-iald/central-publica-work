# Read-only (mode=ro, immutable=1) metadata/rule-count probe of the production bank. Prints counts only, never text.
import sqlite3, sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'copia', 'MEMORIA_IALD', 'lib'))
from iald_memory import guard
db = r'C:\IALD\MEMORIA_IALD\state\memory.sqlite3'
uri = 'file:' + db.replace(chr(92), '/') + '?mode=ro&immutable=1'
c = sqlite3.connect(uri, uri=True)
ver = c.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()
ids = [r[0] for r in c.execute('SELECT context_id FROM contexts')]
folded = collections.Counter(i.casefold() for i in ids)
coll = [k for k, v in folded.items() if v > 1]
out = {'schema_version': ver[0] if ver else None, 'contexts': len(ids), 'case_colliding_groups': len(coll),
       'ids_with_uppercase': sum(1 for i in ids if i != i.lower()), 'events': c.execute('SELECT count(*) FROM events').fetchone()[0]}
blocked = collections.Counter(); per_house = collections.Counter(); houses = collections.Counter()
for cid, scope_json in c.execute('SELECT context_id, scope_json FROM contexts'):
    house = json.loads(scope_json).get('house'); houses[house] += 1
    row = c.execute('SELECT state_json FROM events WHERE context_id=? ORDER BY revision DESC LIMIT 1', (cid,)).fetchone()
    obj = c.execute('SELECT objective_blob FROM contexts WHERE context_id=?', (cid,)).fetchone()[0]
    import zlib
    text = (row[0] if row else '') + '\n' + zlib.decompress(obj).decode('utf-8', 'replace')
    rules = guard.scan_text(text)
    if rules:
        per_house[house] += 1
        for r in rules: blocked[r] += 1
out['houses'] = dict(houses); out['contexts_that_guard_would_refuse_by_house'] = dict(per_house); out['rule_hits'] = dict(blocked)
print(json.dumps(out, ensure_ascii=False, indent=1))
json.dump(out, open(os.path.join(HERE, 't4_prod_readonly_result.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
import zlib
for cid, scope_json, created in c.execute('SELECT context_id, scope_json, created_at FROM contexts'):
    row = c.execute('SELECT revision, state_json FROM events WHERE context_id=? ORDER BY revision DESC LIMIT 1', (cid,)).fetchone()
    obj = zlib.decompress(c.execute('SELECT objective_blob FROM contexts WHERE context_id=?', (cid,)).fetchone()[0]).decode('utf-8', 'replace')
    ro, rs = guard.scan_text(obj), guard.scan_text(row[1])
    print(cid, scope_json, created, 'rev', row[0], 'objective_rules', ro, 'state_rules', rs)
