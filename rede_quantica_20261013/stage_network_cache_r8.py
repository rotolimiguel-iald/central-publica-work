"""Copy only verified old Lean objects into the isolated extension cache."""
import json
import os
from pathlib import Path
from diary_r1 import ROOT, new, pin

out = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
prior = out/'network_bundle_r7'
dest = out/'network_bundle_r8'
compiled_path = prior/'COMPILED_R1.json'
compiled = json.loads(compiled_path.read_bytes())
assert compiled['passed'] is True
plan = json.loads((dest/'PLAN.json').read_bytes())
assert plan['previous_compiled'] == pin(compiled_path)
receipt_path = dest/'CACHE_STAGE_RECEIPT_R1.json'
assert not receipt_path.exists()
old_stage = prior/'CACHE_STAGE_RECEIPT_R2.json'
objects = {x['copy']['path']: x['copy'] for x in json.loads(old_stage.read_bytes())['copies']}
for row in compiled['modules']:
    assert row['passed'] is True
    p = row['object']
    if p['path'] in objects:
        assert objects[p['path']] == p
    objects[p['path']] = p
copies = []
for source in sorted(objects.values(), key=lambda x: x['path']):
    path = Path(source['path'])
    assert pin(path) == source
    relative = path.resolve().relative_to((prior/'lib').resolve())
    target = dest/'lib'/relative
    assert target.resolve().is_relative_to((dest/'lib').resolve())
    assert not target.exists()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix+'.new')
    data = path.read_bytes()
    with temporary.open('xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    assert pin(temporary)['sha256'] == source['sha256']
    temporary.rename(target)
    copied = pin(target)
    assert copied['sha256'] == source['sha256']
    copies.append({'source': source, 'copy': copied})
new(receipt_path, dict(status='VERIFIED_OBJECT_COPIES_ONLY', compiled=pin(compiled_path),
    prior_cache_stage=pin(old_stage), plan=pin(dest/'PLAN.json'), copies=copies,
    script=pin(__file__), production_modified=False))
print(json.dumps(dict(receipt=pin(receipt_path), objects=len(copies))))
