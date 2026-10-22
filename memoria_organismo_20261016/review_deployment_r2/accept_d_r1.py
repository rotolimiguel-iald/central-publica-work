"""Authorized mechanical acceptance of D by its actual independent reviewer."""
import json
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORK))
import mission_io as io

reference = WORK/'SESSION_REFERENCE.json'
review = WORK/'review_deployment_r2/D_FINAL_REVIEW_R1.json'
report = json.loads(review.read_bytes())
assert report['status'] == 'PASS_WITH_SCOPE'
assert report['author'] == 'codex-organism-deployment-review'
assert report['requirement_satisfied'] is True
assert io.pin(report['delivery']['path']) == report['delivery']
projection, before = io.project()
task = next(t for t in projection['projection']['active'] if t['id'] == 'D')
assert task['status'] == 'review_pending'
assert task['evidence'] == [report['delivery']]
assert task['submitted_by'] != report['author']
payload = {'operation':'accept','reference':str(reference),
           'actor':{'kind':'agent','id':report['author']},'task_id':'D',
           'expected_revision':projection['receipt']['revision'],
           'projection_sha256':projection['projection_sha256'],
           'event_id':'organism-D-independent-deployment-accept-r1',
           'review_evidence':[io.pin(review)],
           'note':'Revisão independente PASS_WITH_SCOPE: 31 arquivos/20 backups/93 recibos; processo efetivo e teste JEV real conferidos. Login, TestFlight, Bancada e clientes MCP antigos permanecem explícitos na matriz. APK/AAB locais. Variação documental do push privado e normalização Git registradas ao lado; nenhuma alegação de distribuição física.'}
result, accepted = io.call('mission_cli.py', payload, 'D_independent_accept')
after, final = io.project()
settled = next(t for t in after['projection']['settled'] if t['id'] == 'D')
assert settled['status'] == 'satisfied' and settled['reviewed_by'] == report['author']
receipt = {'reference':str(reference),'review':io.pin(review),'accept_invocation':payload,
           'accept_receipt':io.pin(accepted),'before':io.pin(before),'after':io.pin(final),
           'revision':after['receipt']['revision'],'status':settled['status'],
           'production_actions_by_reviewer':False}
io.save(WORK/'review_deployment_r2/D_ACCEPTED_R1.json',receipt)
print(json.dumps({'receipt':io.pin(WORK/'review_deployment_r2/D_ACCEPTED_R1.json'),
                  'review':io.pin(review),'revision':after['receipt']['revision'],
                  'status':settled['status']},ensure_ascii=False))
