"""Stop only the verified, owned R10 Lean process after explicit handback."""
import datetime as dt
import json
import subprocess
import sys
import time
from pathlib import Path
from diary_r1 import ROOT, new, pin

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0,str(ROOT/'work/memoria_missao_20261016'))
import activate as a
a.ROOT=OUT/'mission_resume_20261016'
attempt=OUT/'gns_coefficient_tomita/attempts/20261016T105344_102192Z'
report=OUT/'mission_review_20261016/R7_CANCELLATION_AND_REPLACEMENT_RECOMMENDATION_R1.json'
candidate=OUT/'mission_review_20261016/CanonicalFockPolarRightCutoffOrderR11Candidate.lean'


def main():
    assert not (a.ROOT/'R7_R10_TERMINATION_RECEIPT.json').exists()
    v=a.call('mission_cli.py',dict(operation='project',reference=str(a.REF),max_chars=60000),'R7_ROOT_HANDOFF_PROJECT')
    task=next(t for t in v['projection']['active'] if t['id']=='R7')
    assert task['status']=='open' and task['lease'] is None, task
    a.call('mission_cli.py',dict(operation='claim',reference=str(a.REF),actor=a.ACTOR,task_id='R7',
        expected_revision=v['receipt']['revision'],projection_sha256=v['projection_sha256'],
        event_id='R7-root-after-diagnostic-claim',lease_seconds=14400),'R7_ROOT_CLAIM')
    v=a.call('mission_cli.py',dict(operation='project',reference=str(a.REF),max_chars=60000),'R7_ROOT_TERMINATE_PROJECT')
    task=next(t for t in v['projection']['active'] if t['id']=='R7')
    a.call('mission_cli.py',dict(operation='check',reference=str(a.REF),actor=a.ACTOR,task_id='R7',
        lease_id=task['lease']['id'],expected_revision=v['receipt']['revision'],
        projection_sha256=v['projection_sha256']),'R7_ROOT_TERMINATE_PREFLIGHT')
    assert not (attempt/'RECEIPT.json').exists(), 'Already terminal: reconcile without stopping anything.'
    start=json.loads((attempt/'START_RECEIPT.json').read_bytes())
    assert start['pid']==165856
    before=dict(at=dt.datetime.now(dt.timezone.utc).isoformat(),actor=a.ACTOR,
        reason='Recorded independent recommendation: over two hours without declaration diagnostics; preserve old attempt and execute corrected explicit-carrier candidate once.',
        recommendation=pin(report),candidate=pin(candidate),start=pin(attempt/'START_RECEIPT.json'),
        source=pin(attempt/'CanonicalFockPolarRightCutoffOrderR10.lean'))
    new(a.ROOT/'R7_R10_TERMINATION_INTENT.json',before)
    # The PowerShell code is fixed text. No source content is interpolated as shell code.
    ps=r'''
$ErrorActionPreference='Stop'
$p=Get-CimInstance Win32_Process -Filter 'ProcessId = 165856'
if ($null -eq $p) { throw 'Exact process no longer exists; do not target another process.' }
$expected='C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\gns_coefficient_tomita\attempts\20261016T105344_102192Z\CanonicalFockPolarRightCutoffOrderR10.lean'
if ($p.Name -ne 'lean.exe' -or -not $p.CommandLine.Contains($expected)) { throw 'PID identity mismatch.' }
$before=$p | Select-Object ProcessId,ParentProcessId,CreationDate,UserModeTime,KernelModeTime,CommandLine
$at=[DateTime]::UtcNow.ToString('o')
Stop-Process -Id 165856 -ErrorAction Stop
[pscustomobject]@{stop_utc=$at; process=$before; signal='Stop-Process exact verified PID'; process_absent=($null -eq (Get-Process -Id 165856 -ErrorAction SilentlyContinue))} | ConvertTo-Json -Depth 5 -Compress
'''
    p=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',ps],text=True,encoding='utf-8',capture_output=True)
    result=dict(returncode=p.returncode,stdout=p.stdout,stderr=p.stderr,at=dt.datetime.now(dt.timezone.utc).isoformat())
    new(a.ROOT/'R7_R10_TERMINATION_ACTION.json',result)
    assert p.returncode==0, result
    for _ in range(30):
        if (attempt/'RECEIPT.json').exists(): break
        time.sleep(1)
    assert (attempt/'RECEIPT.json').exists(),'Original builder receipt not yet available; do not start replacement.'
    terminal=json.loads((attempt/'RECEIPT.json').read_bytes())
    assert terminal['exit_code']!=0
    new(a.ROOT/'R7_R10_TERMINATION_RECEIPT.json',dict(intent=pin(a.ROOT/'R7_R10_TERMINATION_INTENT.json'),
        action=pin(a.ROOT/'R7_R10_TERMINATION_ACTION.json'),terminal=pin(attempt/'RECEIPT.json'),
        classification='CANCELLED_BY_COORDINATOR_FOR_DIAGNOSED_COST',exit_code=terminal['exit_code'],
        seconds=terminal['seconds'],new_attempt_started=False))
    v=a.call('mission_cli.py',dict(operation='project',reference=str(a.REF),max_chars=60000),'R7_CANCEL_CURRENT')
    handles=list(v['projection']['flow']['handles'])
    h=next(h for h in handles if h['id']=='build-20261016T105344_102192Z')
    h.update(status='cancelled',receipt=str(a.ROOT/'R7_R10_TERMINATION_RECEIPT.json'))
    result=a.call('session_memory.py',dict(operation='transition',reference=str(a.REF),actor=a.ACTOR,
        expected_revision=v['receipt']['revision'],event_id='R7-R10-cost-cancelled',
        changes=dict(records=[dict(id='R7-R10-cost-cancelled',kind='fact',statute='REAL',
            text='R10 original source/log preserved. Exact owned PID terminated after independent cost diagnosis and handback. Builder recorded nonzero exit; no duplicate active attempt. R11 candidate uncompiled, hypothesis of instance cost not yet confirmed.',
            sources=[a.source(a.ROOT/'R7_R10_TERMINATION_RECEIPT.json'),a.source(report)])],
            flow=dict(phase='R7_corrected_candidate_ready',next_action='One compact-cache R11 attempt with explicit stage markers; no change to scientific criterion.',handles=handles))),
        'R7_CANCEL_TRANSITION')
    print(json.dumps(dict(terminal=terminal['exit_code'],seconds=terminal['seconds'],revision=result.get('revision'))))


if __name__=='__main__':
    main()
