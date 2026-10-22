"""Claim the unchanged physical residuals and issue bounded source-audit handoffs."""
import copy
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, CLI, WHO, new, pin
import register_rule_tetelestai as reg

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0,str(OUT/'mission_resume_20261016'))
import live_mission_r39 as live

def main():
    target=OUT/'R53_PHYSICAL_SOURCE_AUDIT_START.json'
    if target.exists():
        raise RuntimeError('Recover existing start; never dispatch twice')
    claim=reg.call([CLI,'ver','F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem']==WHO
    assert dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    for task_id in ['R4','R5']:
        p,_=live.project()
        t=next(x for x in p['projection']['active'] if x['id']==task_id)
        assert t['status']=='open' and t['lease'] is None
        live.call('mission_cli.py',dict(operation='claim',reference=str(live.REFERENCE),actor=live.ACTOR,
            task_id=task_id,expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'],
            event_id='r53-'+task_id.lower()+'-physical-source-claim',lease_seconds=7200),'R53_CLAIM_'+task_id)
    state,_=live.call('session_memory.py',dict(operation='get',reference=str(live.REFERENCE)),'R53_SOURCE_GET')
    handles=copy.deepcopy(state['p']['handles'])
    for ident,task,agent in [('r53-physical-clock-source','R4','/root/maxwell_covariance_review'),
                             ('r53-device-continuum-source','R5','/root/fock_r6_review')]:
        assert not any(h['id']==ident for h in handles)
        handles.append(dict(id=ident,kind='agent',task_id=task,status='running',agent=agent,no_repeat=True))
    live.call('session_memory.py',dict(operation='transition',reference=str(live.REFERENCE),actor=live.ACTOR,
        expected_revision=state['revision'],event_id='r53-physical-source-audits-start',
        changes=dict(flow=dict(handles=handles,phase='physical_device_identification_source_audit',
            next_action='Identificar nas fontes qual dispositivo realiza a rede e quais pontes de relogio/espectro ja existem. R7/R8 aceitos, nao reconstruir. Pergunta de identidade do dispositivo enviada ao operador; nao assumir a escolha. R3/R10 preservados.'))),'R53_SOURCE_FLOW')
    handoffs={}
    for task_id in ['R4','R5']:
        p,_=live.project()
        t=next(x for x in p['projection']['active'] if x['id']==task_id)
        common=dict(reference=str(live.REFERENCE),actor=live.ACTOR,task_id=task_id,lease_id=t['lease']['id'],
            expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'])
        live.call('mission_cli.py',dict(common,operation='check'),'R53_CHECK_'+task_id)
        _,r=live.call('mission_cli.py',dict(common,operation='handoff',max_chars=100000),'R53_HANDOFF_'+task_id)
        handoffs[task_id]=pin(r)
    new(target,dict(reference=pin(live.REFERENCE),claim=claim,handoffs=handoffs,
        source=pin(OUT.parent/'F1.REDE/CONTRATO_REDE_R1.md'),
        scope='Targeted source audit; device identity is pending user clarification; no substitute physical model selected.',
        original_criteria_preserved=True,providers_called=False,production_changes=False))
    print(json.dumps(dict(start=pin(target),handoffs=handoffs),ensure_ascii=False))

if __name__=='__main__':
    main()
