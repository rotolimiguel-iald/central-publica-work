"""Record the single R4 execution in p.handles; preserve all other handles."""
from setup_mission import ROOT,REF,ACTOR,call,pin
import json,sys
def main():
    stage=sys.argv[1]
    if stage not in ('started','terminal'):raise ValueError(stage)
    get=call('GET_HANDLE_R4_'+stage+'.json',{'operation':'get','reference':REF},False)
    handles=list(get['p']['handles']);hid='f9-full-prior-refinement-r4'
    old=next((h for h in handles if h['id']==hid),None)
    path=ROOT/'r2_refinement_r4'/('START_R4.json' if stage=='started' else 'COMMAND_RESULT_R4.json')
    data=json.loads(path.read_text(encoding='utf-8'))
    if stage=='started':
        if old is not None:raise ValueError('ALREADY_TRACKED')
        status='running'
    else:
        if old is None or old['status']!='running':raise ValueError('EXPECTED_RUNNING_HANDLE')
        status='completed' if data['exit_code']==0 else 'failed'
    handle={'id':hid,'kind':'synthetic_physical_integration','task_id':'R2','status':status,
            'no_repeat':True,'receipt':pin(path),'plan':pin(ROOT/'r2_refinement_r4/PLAN_R4.json'),
            'interpretation':'Execution only; no observed inference or numerical qualification asserted.'}
    if old:handle['start_receipt']=old['receipt']
    handles=[h for h in handles if h['id']!=hid]+[handle]
    result=call('HANDLE_R4_'+stage+'.json',{'operation':'transition','reference':REF,'actor':ACTOR,
       'expected_revision':get['revision'],'event_id':'fase9-refinement-r4-'+stage,
       'changes':{'flow':{**{k:v for k,v in get['p'].items() if k!='handles'},'handles':handles}}},False)
    print(json.dumps({'stage':stage,'revision':result['revision'],'status':status}))
if __name__=='__main__':main()
