"""Record actual source-audit return and joint review without changing criteria."""
import copy
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, CLI, WHO, new, pin
import register_rule_tetelestai as reg

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0, str(OUT / 'mission_resume_20261016'))
import live_mission_r53 as live


def main():
    target = OUT / 'R53_SOURCE_REVIEW_START.json'
    if target.exists():
        raise RuntimeError('Recover the existing receipt; do not duplicate review')
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    current, project_receipt = live.project()
    for requirement in ['R4', 'R5']:
        task = next(x for x in current['projection']['active'] if x['id'] == requirement)
        live.call('mission_cli.py', dict(operation='check', reference=str(live.REFERENCE),
            actor=live.ACTOR, task_id=requirement, lease_id=task['lease']['id'],
            expected_revision=current['receipt']['revision'],
            projection_sha256=current['projection_sha256']), 'R53_REVIEW_PREFLIGHT_' + requirement)
    r5 = OUT / 'global_net_inventory/R53/DEVICE_CONTINUUM_SOURCE_AUDIT_R1.json'
    r5_pin = {k: v for k, v in pin(r5).items() if k in ['path', 'sha256']}
    state, _ = live.call('session_memory.py', dict(operation='get', reference=str(live.REFERENCE)), 'R53_REVIEW_GET')
    handles = copy.deepcopy(state['p']['handles'])
    handle = next(x for x in handles if x['id'] == 'r53-device-continuum-source')
    assert handle['status'] == 'running'
    handle.update(status='returned', receipt=r5_pin, requirement_satisfied=False)
    assert not any(x['id'] == 'r53-joint-source-review' for x in handles)
    handles.append(dict(id='r53-joint-source-review', kind='agent', task_ids=['R4', 'R5'],
        status='running', agent='/root/mission_memory_review', no_repeat=True,
        scope='Source audit only; original construction criteria remain open',
        started_by='collaboration.followup_task', registration_order='after_dispatch'))
    result, receipt = live.call('session_memory.py', dict(operation='transition',
        reference=str(live.REFERENCE), actor=live.ACTOR, expected_revision=state['revision'],
        event_id='r53-source-return-and-joint-review-start',
        changes=dict(flow=dict(handles=handles))), 'R53_REVIEW_FLOW')
    new(target, dict(claim=claim, reference=pin(live.REFERENCE), revision=result['revision'],
        initial_project=pin(project_receipt), r5_report=r5_pin, transition_receipt=pin(receipt),
        script=pin(Path(__file__)), no_science_acceptance=True, original_criteria_preserved=True))
    print(json.dumps(dict(receipt=pin(target), revision=result['revision']), ensure_ascii=False))


if __name__ == '__main__':
    main()
