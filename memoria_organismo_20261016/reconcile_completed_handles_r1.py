"""Reconcile observed terminal agents only; no requirement acceptance or release."""
import copy
import datetime as dt
import json
from mission_io import WORK, REFERENCE, ACTOR, call, pin, save

ARTIFACTS = {
    'org-app-inventory': [WORK/'inventory_app/APP_MISSION_INVENTORY_R2.json'],
    'org-native-inventory': [WORK/'inventory_native/NATIVE_HOLOGRAPHIC_INVENTORY_R1.json', WORK/'REVIEW_CONTRACT_R2.json'],
    'org-queue-inventory': [WORK/'inventory_queue/QUEUE_SESSIONS_BANCADA_INVENTORY_R1.json', WORK/'REVIEW_INVENTORY_I_R1.json', WORK/'I_ACCEPT_BLOCKED_R1.json'],
}
AGENTS = {
    'org-app-inventory': '/root/fock_r6_review',
    'org-native-inventory': '/root/maxwell_covariance_review',
    'org-queue-inventory': '/root/mission_memory_review',
}


def main():
    evidence_path = WORK/'AGENT_TERMINAL_OBSERVATION_R1.json'
    final_path = WORK/'TERMINAL_HANDLES_RECONCILED_R1.json'
    for path in (evidence_path, final_path):
        if path.exists():
            raise FileExistsError(path)
    before, before_receipt = call('session_memory.py', {'operation':'get', 'reference':str(REFERENCE)}, 'terminal_handles_before')
    if before['revision'] != 4:
        raise RuntimeError('Revision advanced; re-read agent and mission states')
    found = {h['id']: h for h in before['p']['handles']}
    if not all(k in found and found[k]['agent']==AGENTS[k] and found[k]['status']=='running' for k in AGENTS):
        raise RuntimeError('Unexpected handle identity or state')

    # This is a transcription of the live tool observation in this turn, not a
    # self-issued semantic review or a claim that artifact existence proves exit.
    observation = {
        'schema':'terminal-agent-observation/v1',
        'recorded_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'source_tool':'collaboration.list_agents',
        'observation_kind':'transcription_of_live_tool_result_in_current_turn',
        'agents':[{'handle_id':k, 'agent':a, 'tool_reported_status':'completed',
                   'artifacts':[pin(p) for p in ARTIFACTS[k]]} for k,a in AGENTS.items()],
        'scope':'Execution termination only. I remains review_pending. No accept, claim, extend, amend, or production changes.',
    }
    save(evidence_path, observation)
    handles = copy.deepcopy(before['p']['handles'])
    for h in handles:
        if h['id'] in AGENTS:
            h.update(status='completed', no_repeat=True,
                     terminal_observation=pin(evidence_path),
                     result_evidence=[pin(p) for p in ARTIFACTS[h['id']]],
                     completion_scope='execution_finished_not_requirement_accepted')
    request = {'operation':'transition', 'reference':str(REFERENCE),
               'actor':ACTOR, 'expected_revision':before['revision'],
               'event_id':'organism-terminal-inventory-handles-r1',
               'changes':{'flow':{'handles':handles}}}
    transitioned, transition_receipt = call('session_memory.py', request, 'terminal_handles_transition')
    after, after_receipt = call('session_memory.py', {'operation':'get', 'reference':str(REFERENCE)}, 'terminal_handles_after')
    if after['q'] != before['q']:
        raise RuntimeError('Unexpected requirement or material record change')
    if any(after['p'][key] != before['p'][key] for key in ('phase','next_action')):
        raise RuntimeError('Unexpected phase or next-action change')
    proj, project_receipt = call('mission_cli.py', {'operation':'project', 'reference':str(REFERENCE), 'max_chars':125000}, 'terminal_handles_project')
    task_i = next(x for x in proj['projection']['active'] if x['id']=='I')
    if task_i['status'] != 'review_pending' or proj['projection']['unresolved_handles'] or proj['projection']['next_ready']:
        raise RuntimeError('Projection does not preserve the pending acceptance boundary')
    verified, verify_receipt = call('session_memory.py', {'operation':'verify', 'reference':str(REFERENCE)}, 'terminal_handles_verify')
    save(final_path, {'schema':'terminal-handles-reconciliation/v1',
                     'revision_before':before['revision'], 'revision_after':after['revision'],
                     'requirement_I_status':task_i['status'], 'q_unchanged':True,
                     'phase_unchanged':True, 'next_action_unchanged':True,
                     'unresolved_handles':proj['projection']['unresolved_handles'],
                     'next_ready':proj['projection']['next_ready'],
                     'evidence':[pin(p) for p in (evidence_path,before_receipt,transition_receipt,after_receipt,project_receipt,verify_receipt)],
                     'production_source_changed':False, 'accept_performed':False})
    print(json.dumps({'receipt':pin(final_path), 'revision':after['revision'],
                      'requirement_I_status':task_i['status'], 'terminal_agents':3,
                      'unresolved_handles':0, 'next_ready':[]}, ensure_ascii=False))


if __name__=='__main__':
    main()
