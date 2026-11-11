"""Verify all materialized production bytes before allowing pointer activation."""
from copy import deepcopy
from pathlib import Path
import json
from review_queue import Q, W, read, sha

def main():
    stage = read(W/'review/QUEUE_RECONSTRUCTION.json')
    promotion = Q/'promotion'
    plan = read(promotion/'PLAN.json')
    verified = read(promotion/'VERIFY_FINAL_PATHS.json')
    target = Path(plan['destination'])
    expected = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\state\canonical_memory\releases') / stage['epoch']
    assert target.resolve(strict=True) == expected
    assert verified['status'] == 'PASS' and verified['generation'] == stage['generation']
    assert verified['chunks'] == stage['chunks_verified']
    old_manifest = read(Q/'staging/releases'/stage['epoch']/'manifest.json')
    relocated = deepcopy(old_manifest)
    relocated['snapshot_root'] = str(target/'snapshots'/stage['epoch'])
    for entry in relocated['documents']:
        entry['path'] = str(Path(relocated['snapshot_root'])/entry['name'])
        assert sha(Path(entry['path'])) == entry['sha256']
    assert read(target/'manifest.json') == relocated
    assert sha(target/'index.sqlite3') == stage['index_sha256']
    assert sha(Path(relocated['snapshot_root'])/'SEALED_SNAPSHOT.json') == relocated['snapshot_manifest_sha256']
    assert sha(target/'manifest.json') == plan['manifest']['sha256']
    pointer = Path(plan['baseline']['path'])
    assert sha(pointer) == plan['baseline']['sha256'] and read(pointer)['release'] == 'v408'
    receipt = {'status':'PASS','generation':stage['generation'],'reviewer':stage['reviewer'],
               'manifest_sha256':sha(target/'manifest.json'),'verification_sha256':sha(promotion/'VERIFY_FINAL_PATHS.json'),
               'expected_active_sha256':sha(pointer),'docs':len(relocated['documents']),
               'chunks':stage['chunks_verified'],'index_byte_identical_to_independent_replay':True}
    with (W/'review/QUEUE_FINAL_PATHS.json').open('x',encoding='utf-8') as f:
        json.dump(receipt,f,indent=2)
    print(receipt['status'],receipt['generation'])

if __name__ == '__main__':
    main()
