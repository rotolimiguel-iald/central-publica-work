"""Recover only map/board/ACOM after duplicate-route refusal; no memory reappend."""
from setup_mission import ROOT,UNIT,ACTOR,REF,pin,save,shell,call
import json,sys
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def main():
    assert not (ROOT/'REGISTRATION_R2.json').exists()
    for row in read('MEMORY_APPLIED_R2.json'):
        assert pin(row['after']['path'])['sha256']==row['after']['sha256']
        assert pin(row['backup']['path'])['sha256']==row['before']['sha256']
    failed=read('MAP_REGISTER_R2.json');assert failed['exit']!=0
    assert not (ROOT/'BOARD_PROGRESS_R2.json').exists() and not (ROOT/'TRANSITION_R2.json').exists()
    entry=read('MAP_ENTRY_R2.json');assert entry['tipo']=='ROTA'
    entry['tipo']='RESULTADO'
    entry['nota']+=' Recuperação administrativa: rota já existe; esta camada é RESULTADO aditivo, não nova rota.'
    save('MAP_ENTRY_R2_RESULTADO.json',entry)
    mapped=shell('MAP_REGISTER_R2_RECOVERED.json',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R2_RESULTADO.json'),'--quem',ACTOR['id']])
    progress=read('PROGRESS_R2.json')
    boarded=shell('BOARD_PROGRESS_R2.json',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'PROGRESS_R2.json'),'--nota',progress['summary']])
    state=call('GET_REGISTER_R2_RECOVERED.json',{'operation':'get','reference':REF},False)
    handles=list(state['p']['handles'])
    for hid,rel,status in [('f9-full-prior-r1','r2_full_integration/COMMAND_RESULT_R1.json','failed'),('f9-full-prior-recovery-r2','r2_full_integration/recovery_r2/COMMAND_RESULT_R2.json','completed')]:
        assert all(h['id']!=hid for h in handles)
        assert (read(rel)['exit_code']==0)==(status=='completed')
        handles.append({'id':hid,'kind':'synthetic_physical_integration','task_id':'R2','status':status,
            'no_repeat':True,'receipt':pin(ROOT/rel),'interpretation':'Execution only; numerical qualification in PROGRESS_R2'})
    note=(ROOT/'MEMORY_APPEND_R2.txt').read_text(encoding='utf-8')
    trans=call('TRANSITION_R2.json',{'operation':'transition','reference':REF,'actor':ACTOR,
        'expected_revision':state['revision'],'event_id':'fase9-integration-components-r2',
        'changes':{'records':[{'id':'fase9-components-r2','kind':'fact','statute':'REAL','text':note,
         'sources':[{'kind':'artifact','ref':str(ROOT/'PROGRESS_R2.json'),'sha256':pin(ROOT/'PROGRESS_R2.json')['sha256']}]}],
        'flow':{'phase':'components_r2_scientific_inference_open','next_action':progress['next_action'],'handles':handles}}},False)
    after=call('PROJECT_AFTER_REGISTER_R2.json',{'operation':'project','reference':REF,'max_chars':50000})
    task=next(t for t in after['projection']['active'] if t['id']=='R1')
    call('HANDOFF_VALID_R2.json',{'operation':'handoff','reference':REF,'actor':ACTOR,
       'expected_revision':after['receipt']['revision'],'projection_sha256':after['projection_sha256'],
       'task_id':'R1','lease_id':task['lease']['id'],'max_chars':50000})
    save('REGISTRATION_R2.json',{'status':'PARTIAL_PROGRESS_REGISTERED','unit':UNIT,'progress':pin(ROOT/'PROGRESS_R2.json'),
        'memory':pin(ROOT/'MEMORY_APPLIED_R2.json'),'map':pin(ROOT/'MAP_REGISTER_R2_RECOVERED.json'),
        'board':pin(ROOT/'BOARD_PROGRESS_R2.json'),'acom':trans,'handoff':pin(ROOT/'HANDOFF_VALID_R2.json'),
        'administrative_correction':'Map rejected duplicate ROTA before mutation. Recovered as RESULTADO on existing route. Memory appends already succeeded and were not repeated.',
        'failed_map':pin(ROOT/'MAP_REGISTER_R2.json'),'scripts':[pin(ROOT/'register_progress_r2.py'),pin(ROOT/'recover_registration_r2.py')]})
    print(json.dumps({'status':'REGISTERED','map':mapped,'board':boarded,'revision':trans['revision']},ensure_ascii=False))
if __name__=='__main__':main()
