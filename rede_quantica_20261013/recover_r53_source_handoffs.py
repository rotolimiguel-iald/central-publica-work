"""Recover completed R53 claims after a visible projection-capacity refusal."""
import json
import sys
from pathlib import Path
from diary_r1 import ROOT,new,pin

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0,str(OUT/'mission_resume_20261016'))
import live_mission_r53 as live

def main():
    target=OUT/'R53_PHYSICAL_SOURCE_AUDIT_START.json'
    if target.exists():
        raise RuntimeError('Existing immutable start; recover its handoffs')
    refusal=OUT/'mission_resume_20261016/LIVE_PROJECT_20261016T212752_525625Z_7c7e3690_RECEIPT.json'
    assert json.loads(refusal.read_bytes())['message']=='projection_overflow_required_100030'
    handoffs={}
    for task_id in ['R4','R5']:
        p,_=live.project()
        t=next(x for x in p['projection']['active'] if x['id']==task_id)
        assert t['status']=='working' and t['lease']['owner']==live.ACTOR['id']
        common=dict(reference=str(live.REFERENCE),actor=live.ACTOR,task_id=task_id,
            lease_id=t['lease']['id'],expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'])
        live.call('mission_cli.py',dict(common,operation='check'),'R53_RECOVER_CHECK_'+task_id)
        _,r=live.call('mission_cli.py',dict(common,operation='handoff',max_chars=live.MAX_CHARS),'R53_RECOVER_HANDOFF_'+task_id)
        handoffs[task_id]=pin(r)
    new(target,dict(reference=pin(live.REFERENCE),handoffs=handoffs,capacity=live.MAX_CHARS,
        refusal=pin(refusal),helper=pin(OUT/'mission_resume_20261016/live_mission_r53.py'),
        source=pin(OUT.parent/'F1.REDE/CONTRATO_REDE_R1.md'),
        scope='Recover existing claims and handles only; no repeat or truncation. Device identity remains pending human clarification.',
        original_criteria_preserved=True,providers_called=False,production_changes=False))
    print(json.dumps(dict(start=pin(target),handoffs=handoffs),ensure_ascii=False))

if __name__=='__main__':
    main()
