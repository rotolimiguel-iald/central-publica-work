"""Recover the refused submission: mission pins require exactly path and sha256."""
import hashlib
import json
import sys
from pathlib import Path

OUT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
sys.path.insert(0, str(OUT / 'mission_resume_20261016'))
import live_mission_r39 as live

request_file = OUT / 'mission_resume_20261016/LIVE_R52_R7_SUBMIT_20261016T211017_944255Z_a72153ec_REQUEST.json'
failure_file = request_file.with_name(request_file.name.replace('_REQUEST', '_RECEIPT'))
failure = json.loads(failure_file.read_bytes())
assert failure == {'ok': False, 'error': 'MissionError', 'message': 'evidence_requires_path_and_sha256'}
request = json.loads(request_file.read_bytes())
for item in request['evidence']:
    assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest() == item['sha256']
request['evidence'] = [{k: item[k] for k in ('path', 'sha256')} for item in request['evidence']]
current, _ = live.project()
task = next(t for t in current['projection']['active'] if t['id'] == 'R7')
assert task['status'] == 'working' and task['lease']['owner'] == live.ACTOR['id']
request.update(expected_revision=current['receipt']['revision'], projection_sha256=current['projection_sha256'], lease_id=task['lease']['id'])
result, receipt = live.call('mission_cli.py', request, 'R52_R7_SUBMIT_RECOVERED')
print(json.dumps(dict(submitted=True, receipt=str(receipt))))
