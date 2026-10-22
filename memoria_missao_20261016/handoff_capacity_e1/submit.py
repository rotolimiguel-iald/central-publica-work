"""Submit the installed correction as a candidate for independent acceptance."""
import json
from prepare import ROOT,OUT,REF,ACTOR,TASK,pin,source,new,project,base,call

def main():
    receipt=json.loads((ROOT/'VERIFICATION_INSTALLED.json').read_bytes())
    assert receipt['ok'] and receipt['mcp_handoff_equals_sync']
    p=project('BEFORE_SUBMIT')
    task=next(t for t in p['projection']['active'] if t['id']==TASK)
    call('mission_cli.py',{**base(p),'operation':'submit','task_id':TASK,'lease_id':task['lease']['id'],
        'event_id':'memory-e1-handoff-installed-submit',
        'evidence':[pin(ROOT/n) for n in ['mission_bridge_candidate.py','DEPLOYMENT_E1.json',
                    'VERIFICATION_CANDIDATE.json','SYNTHETIC_MCP.json','VERIFICATION_INSTALLED.json','REVIEW_E1.json']]},'SUBMIT')
    p=project('BEFORE_CUSTODY')
    flow=dict(p['projection']['flow'])
    terminal=OUT/'orbital_rotation/attempts/20261016T130457_992603Z/RECEIPT.json'
    build=json.loads(terminal.read_bytes())
    assert build['exit_code']==0
    for h in flow['handles']:
        if h['id']=='build-20261016T130457_992603Z':
            h.update(status='completed',receipt=str(terminal))
    flow.update(phase='memory_handoff_installed_review_pending',
        next_action='Independent acceptance of M1; then only existing science residues and exact R11 handle. Prefix probe completed; do not repeat it.')
    call('session_memory.py',{'operation':'transition','reference':str(REF),'actor':ACTOR,
        'expected_revision':p['receipt']['revision'],'event_id':'memory-e1-installed-custody',
        'changes':{'records':[{'id':'memory-e1-installed-custody','kind':'fact','statute':'REAL',
           'text':'MCP handoff now forwards explicit max_chars; real/synthetic large missions preserve sync projection. Installed new process verified. Existing prefix probe completed with exit 0; no restart or theorem acceptance. Memory correction awaits independent technical acceptance.',
           'sources':[source(ROOT/'VERIFICATION_INSTALLED.json'),source(terminal)]}],'flow':flow}},'CUSTODY')
    print(json.dumps({'submitted':TASK,'installed':True,'prefix_probe':'completed'}))

if __name__=='__main__':main()
