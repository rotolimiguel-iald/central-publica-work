"""Apply a reviewed, exact additive memory plan under requirement M; preserve byte backups."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
from mission_io import WORK, check, pin, save

OUT = WORK / 'memory_final'

def exclusive(path, raw):
    with path.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    if path.read_bytes() != raw:
        raise RuntimeError('Byte verification failed: ' + str(path))

def main():
    plan_path = OUT / 'PLAN_R1.json'
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    review = json.loads((OUT / 'REVIEW_R1.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS')
    assert review['plan'] == pin(plan_path)
    assert review['applier'] == pin(Path(__file__))
    assert review['reviewer'] != 'codex-gerente-tgl'
    _, check_receipt = check('M')
    assert not (OUT/'APPLIED_R1.json').exists()
    originals = []
    for row in plan['surfaces']:
        path = Path(row['path'])
        assert pin(path) == row['before']
        assert pin(row['append']['path']) == row['append']
        raw, extra = path.read_bytes(), Path(row['append']['path']).read_bytes()
        assert plan['marker'].encode() not in raw
        assert len(raw) == row['before_bytes']
        assert hashlib.sha256(raw+extra).hexdigest() == row['after_sha256']
        originals.append((row, path, raw, extra))
    doc = plan['new_document']
    assert pin(doc['source']['path']) == doc['source']
    assert not Path(doc['path']).exists()
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    save(OUT/'INTENT_R1.json', {'time_utc':stamp,'plan':pin(plan_path),'review':pin(OUT/'REVIEW_R1.json'),'preflight':pin(check_receipt)})
    receipts = []
    # Preserve all originals before the first replacement.
    backups = []
    for row,path,raw,extra in originals:
        backup = path.with_name(path.name+'.bak_'+stamp)
        exclusive(backup, raw)
        backups.append(backup)
    for i, ((row,path,raw,extra),backup) in enumerate(zip(originals,backups)):
        assert path.read_bytes() == raw, 'Concurrent modification: '+str(path)
        temp = path.with_name(path.name+'.tmp_'+stamp)
        exclusive(temp, raw+extra)
        assert path.read_bytes() == raw, 'Concurrent modification before replacement'
        os.replace(temp,path)
        assert path.read_bytes() == raw+extra
        result={'before':row['before'],'after':pin(path),'backup':pin(backup),
                'before_bytes':len(raw),'after_bytes':len(raw)+len(extra),'append_only':True}
        save(OUT/f'SURFACE_{i:02d}_R1.json',result)
        receipts.append(result)
    docpath = Path(doc['path'])
    doctemp = docpath.with_name(docpath.name+'.tmp_'+stamp)
    exclusive(doctemp,Path(doc['source']['path']).read_bytes())
    os.rename(doctemp,docpath)  # Windows rename refuses an existing destination.
    assert pin(docpath)['sha256'] == doc['source']['sha256']
    save(OUT/'APPLIED_R1.json', {'status':'APPLIED_VERIFIED','author':'codex-gerente-tgl',
         'time_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'plan':pin(plan_path),
         'surfaces':receipts,'new_document':pin(docpath),'preflight':pin(check_receipt)})
    print(json.dumps({'receipt':pin(OUT/'APPLIED_R1.json'),'surfaces':len(receipts)},ensure_ascii=False))

if __name__ == '__main__':
    main()
