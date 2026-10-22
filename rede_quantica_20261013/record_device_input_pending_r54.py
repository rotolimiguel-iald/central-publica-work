"""Represent the verified missing device identity without reopening accepted work."""
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, new, pin

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0, str(OUT / 'mission_resume_20261016'))
import live_mission_r53 as live


def main():
    target = OUT / 'R54_DEVICE_IDENTITY_PENDING.json'
    if target.exists():
        raise RuntimeError('Recover the existing receipt instead of repeating transitions')
    source = OUT / 'PROGRESS_R53.json'
    source_pin = {k: v for k, v in pin(source).items() if k in ['path', 'sha256']}
    transitions = []
    for task_id in ['R4', 'R5']:
        current, _ = live.project()
        task = next(t for t in current['projection']['active'] if t['id'] == task_id)
        assert task['status'] == 'working'
        assert task['lease']['owner'] == live.ACTOR['id']
        result, receipt = live.call('mission_cli.py', dict(operation='block',
            reference=str(live.REFERENCE), actor=live.ACTOR, task_id=task_id,
            expected_revision=current['receipt']['revision'],
            projection_sha256=current['projection_sha256'],
            event_id='r54-device-identity-pending-' + task_id.lower(),
            reason='Source audits and independent review are terminal. The intended mechanical device/sector has not been identified by the operator: MQC, Supercondutor or Psi-NET. Preserve original criterion and all accepted suppliers; no physical model is selected by inference. Resume only after the identifying input and reconcile dependencies explicitly.',
            sources=[source_pin]), 'R54_PENDING_' + task_id)
        transitions.append(pin(receipt))
    current, receipt = live.project()
    assert not current['projection']['unresolved_handles']
    assert not current['projection']['next_ready']
    assert not current['projection']['tetelestai']
    new(target, dict(reference=pin(live.REFERENCE), revision=current['receipt']['revision'],
        project_receipt=pin(receipt), transitions=transitions, source=source_pin,
        pending_input='Identify the intended mechanical device/sector: MQC, Supercondutor or Psi-NET.',
        active=[{k: t.get(k) for k in ['id', 'status', 'criterion', 'depends_on', 'note']}
                for t in current['projection']['active']],
        live_execution_handles=[], full_goal_complete=False, requirements_changed=False,
        accepted_work_reopened=False, providers_called=False, production_changed=False))
    verified, vr = live.call('session_memory.py', dict(operation='verify',
        reference=str(live.REFERENCE)), 'R54_PENDING_VERIFY')
    print(json.dumps(dict(receipt=pin(target), revision=current['receipt']['revision'],
        verify_ok=verified.get('ok'), verify_receipt=str(vr)), ensure_ascii=False))


if __name__ == '__main__':
    main()
