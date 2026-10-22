"""Freeze installer preparation and capture private tests, without activation."""
from datetime import datetime, timezone
import os
from pathlib import Path
import subprocess
import sys
import time
from transaction import receipt, sha, write_new

ROOT = Path(__file__).resolve().parent
output = ROOT/'PREPARATION_R1.json'
if output.exists() or (ROOT/'TESTS_R1.log').exists():
    raise SystemExit('Existing evidence preserved')
start = datetime.now(timezone.utc).isoformat()
clock = time.perf_counter()
cmd = [sys.executable, '-B', '-X', 'utf8', '-m', 'unittest', 'test_transaction', 'test_controlled', '-v']
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
run = subprocess.run(cmd, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
write_new(ROOT/'TESTS_R1.log', run.stdout)
files = ['transaction.py','controlled.py','maintenance.py','legacy_app_checks.py',
         'queue_lock.py','test_transaction.py','test_controlled.py','freeze_preparation.py',
         'REUSED_PRIMITIVES.json','TESTS_R1.log']
receipt(output, {
    'unit':'F9.MEMORIA_ORGANISMO_20261016','requirement':'P','author':'codex-gerente-tgl',
    'status':'CANDIDATE_TESTED' if run.returncode == 0 else 'FAILED',
    'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),
    'seconds':time.perf_counter()-clock,'command':cmd,'cwd':str(ROOT),'exit':run.returncode,
    'files':[{'path':str(ROOT/p),'sha256':sha((ROOT/p).read_bytes())} for p in files],
    'tests':'21 private-copy checks; no production maintenance or installation',
    'corrected_test_fixture':'First maintenance-test run leaked SQLite fixture handles; explicit close fixed before freezing. Production paused_queue already closes in finally.',
    'protocol':[
        'Exact reviewed plan; source hashes and destination baselines validated twice.',
        'Existing queue drain lock + SQL write transaction prevent dispatch/admission during code replacement; running-uncertain ledger row refuses.',
        'Existing app supervisor is suspended; only the verified idle web child is terminated and restarted. Shared database/state preserved.',
        'Immediate byte backups, immutable intents/results, reverse rollback preserves a concurrent edit.',
        'Installation is not a multi-file atomic commit. Durable receipts identify partial failure. It does not reload old MCP processes.',
        'Final destination plan comes from A/N/Q manifests; joint review V must pin that plan and these scripts before D.',
        'Names are audit attribution, not authentication; reviewer and human authorization are checked by the invoking workflow.'
    ],'installed':False,'providers_called':0
})
print(output)
raise SystemExit(run.returncode)
