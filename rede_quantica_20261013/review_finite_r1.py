"""Independent recompuation of the preregistered reduced device in a fresh copy."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import time
import datetime as dt

OUT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.REDE')
SRC = OUT / 'finite_device'
DST = OUT / 'review_device'
PY = r'C:\Users\rotol\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'

def save(path, data):
    if not isinstance(data, bytes):
        data = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False).encode('utf-8')
    with path.open('xb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    assert path.read_bytes() == data

def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

DST.mkdir(exist_ok=False)
copied=[]
for n in ['run_finite_device.py','PREREGISTRO_DEVICE_R1.json','FREEZE_DEVICE_R1.json']:
    save(DST/n,(SRC/n).read_bytes())
    copied.append({'source':pin(SRC/n),'copy':pin(DST/n)})
start=dt.datetime.now(dt.timezone.utc).isoformat(); t=time.perf_counter()
cmd=[PY,'-B','-X','utf8',str(DST/'run_finite_device.py')]
cp=subprocess.run(cmd,cwd=DST,capture_output=True)
end=dt.datetime.now(dt.timezone.utc).isoformat()
save(DST/'BUILD.log',json.dumps({'command':cmd,'start_utc':start,'end_utc':end,'seconds':time.perf_counter()-t,'exit':cp.returncode},indent=2).encode()+b'\n'+cp.stdout+b'\n'+cp.stderr)
if cp.returncode: raise RuntimeError(cp.stdout.decode('utf-8','replace')+cp.stderr.decode('utf-8','replace'))
result=json.loads((DST/'RESULTADO_DEVICE_R1.json').read_text(encoding='utf-8'))
checks=result['checks']
assert all(x['passed'] for x in checks)
save(DST/'REVIEW_DEVICE_R1.json',{
    'reviewer':'codex-gerente-tgl / root, independent of builder takesaki_local_lemmas',
    'status':'PASS_IN_STATED_REDUCED_SCOPE_NOT_C1_APPROVAL',
    'source':pin(SRC/'RESULTADO_DEVICE_R1.json'),'recomputed':pin(DST/'RESULTADO_DEVICE_R1.json'),
    'copies':copied,'exit_code':cp.returncode,'checks':len(checks),'all_pass':True,
    'review_findings':[
        'The 3-factor local-algebra embedding, product basis tests and disjoint supports implement the stated tensor-factor net.',
        'The Hamiltonian and holographic jump match the selected Supercondutor source with explicit bosonic 0/1 truncation.',
        'Column-major vectorization, Choi reshuffling and output partial trace are consistent; energy is tested as an open-system balance.',
        'The density and root-amplitude controls are checks of possible interpretations, not a claim that the documented classical codec is a CPTP channel.',
        'The 54 graph edges are INPUT; no simulation of 27 qubits, actual apparatus, infinite-mode convergence, rate calibration, 4D or empirical discrimination.'
    ],
    'material_findings':[], 'preregistration_preserved':True,
    'artifacts':[pin(DST/'BUILD.log'),pin(Path(__file__))]
})
print(json.dumps({'exit':cp.returncode,'checks':len(checks),'result':str(DST/'REVIEW_DEVICE_R1.json')},ensure_ascii=False))
