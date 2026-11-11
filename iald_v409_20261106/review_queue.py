"""Independently replay the staged queue passages against their pinned originals."""
from bisect import bisect_right
import hashlib
import json
from pathlib import Path
import sqlite3

W = Path(__file__).resolve().parent
Q = W.parent / 'scientific_memory_sync_20261106_v409'

def read(path):
    return json.loads(path.read_bytes())

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    v = read(Q / 'VERIFY_STAGING.json')
    prep = read(Q / ('PREPARATION_' + v['epoch'] + '.json'))
    base = Path(prep['target'])
    m = read(base / 'manifest.json')
    assert v['status'] == 'PASS' and v['generation'] == m['generation']
    assert sha(base / 'manifest.json') == prep['manifest']['sha256']
    assert sha(base / 'index.sqlite3') == m['index_sha256']
    assert sha(Path(m['snapshot_root']) / 'SEALED_SNAPSHOT.json') == m['snapshot_manifest_sha256']
    originals = {Path(r['path']).name: r for r in prep['sources']}
    db = sqlite3.connect((base/'index.sqlite3').as_uri()+'?mode=ro&immutable=1', uri=True)
    count = 0
    try:
        assert db.execute('PRAGMA quick_check').fetchall() == [('ok',)]
        for row in m['documents']:
            p = Path(row['path'])
            assert p.is_relative_to(base) and p.name == row['name']
            raw = p.read_bytes()
            assert hashlib.sha256(raw).hexdigest() == row['sha256'] == sha(Path(originals[p.name]['path']))
            text = raw.decode('utf-8-sig')
            starts, position = [], 0
            for line in text.splitlines(keepends=True):
                starts.append(position)
                position += len(line)
            offset = 0
            for body, first, last in db.execute('SELECT body,first_line,last_line FROM passages WHERE document=? ORDER BY rowid', (p.name,)):
                end = offset + len(body)
                assert body and text[offset:end] == body
                assert int(first) == bisect_right(starts,offset) and int(last) == bisect_right(starts,end-1)
                offset = end
                count += 1
            assert offset == len(text)
        assert count == m['chunks'] == db.execute('SELECT count(*) FROM passages').fetchone()[0]
        hits = db.execute("SELECT COUNT(*) FROM passages WHERE passages MATCH ?", ('"p_igual_np_no_modo_selecao"',)).fetchone()[0]
        assert hits > 0
        assert len(set(originals)) == len(m['documents']) == 13
    finally:
        db.close()
    plan = read(Q / 'PROMOTION_PLAN.json')
    final = read(Q / 'MANIFEST_FINAL_CANDIDATE.json')
    destination = Path(plan['destination'])
    assert destination == Path(plan['active']['path']).parent / 'releases' / v['epoch']
    assert not destination.exists()
    assert sha(plan['active']['path']) == plan['active']['sha256']
    assert final['generation'] == m['generation'] and final['index_sha256'] == m['index_sha256']
    assert Path(final['snapshot_root']) == destination / 'snapshots' / v['epoch']
    for a,b in zip(final['documents'], m['documents']):
        assert dict(a, path=b['path']) == b
        assert Path(a['path']) == Path(final['snapshot_root']) / b['name']
    assert dict(final, snapshot_root=m['snapshot_root'], documents=m['documents']) == m
    assert len(plan['files']) == 16
    for row in plan['files']:
        assert sha(row['path']) == row['sha256']
        dest = Path(row['destination'])
        assert dest == destination / row['relative_path'] and dest.is_relative_to(destination)
        expected = sha(Q/'MANIFEST_FINAL_CANDIDATE.json') if dest.name=='manifest.json' else row['sha256']
        assert row['planned_sha256'] == expected
    report = {'status':'PASS' ,'scope':'Independent staged reconstruction, coordinates and retrieval; production promotion requires final paths and CAS.',
              'epoch':v['epoch'],'generation':v['generation'],'manifest_sha256':prep['manifest']['sha256'],
              'index_sha256':m['index_sha256'],'complete_documents':len(originals),
              'chunks_verified':count,'P_NP_identifier_passages':hits,'reviewer':'codex-app-01a094df','promotion_plan_sha256':sha(Q/'PROMOTION_PLAN.json'),'final_manifest_candidate_sha256':sha(Q/'MANIFEST_FINAL_CANDIDATE.json')}
    target = W/'review'/'QUEUE_RECONSTRUCTION.json'
    with target.open('x',encoding='utf-8') as stream:
        json.dump(report,stream,indent=2)
    print(json.dumps(report))

if __name__ == '__main__':
    main()
