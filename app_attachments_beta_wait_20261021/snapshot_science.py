from task import *
prior=W.parent/'acom_signal_transport_20261021'/'SCIENCE_BASELINE.json'
d=json.loads(prior.read_bytes())
for row in d['files']:
    b=Path(row['path']).read_bytes()
    assert hashlib.sha256(b).hexdigest()==row['sha256'], 'Science changed; reconcile before deployment'
new('SCIENCE_BASELINE.json',d)
print('Five science source hashes verified; no source changed')
