"""Assemble receipts only after terminal live tests and installed-data verification."""
from pathlib import Path
import hashlib,json,time,sqlite3
import task
W=task.W

def pin(name):
    p=W/name;raw=p.read_bytes()
    return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}

def main():
    task.project();task.check('verify')
    final=json.loads((W/'live_validation.json').read_bytes())
    installed=json.loads((W/'publication_fix/installed_verification.json').read_bytes())
    assert final['status']==installed['status']=='PASS'
    queue=json.loads((W/'queue_effective_generation.json').read_bytes());assert queue['status']=='PASS' and queue['release']=='v394'
    from_path=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\state\canonical_memory\ACTIVE.json')
    active=json.loads(from_path.read_bytes());assert active['generation']==queue['generation']
    old=json.loads((W/'deployment.json').read_bytes());patch=json.loads((W/'publication_fix/deployment.json').read_bytes())
    assert not old['client_files_changed'] and not patch['client_files_changed']
    evidence=[pin(n) for n in ('app/final/PUBLICATION_VERIFIED.json','queue_activation.json','queue_effective_generation.json','deployment.json','restart.json','publication_fix/deployment.json','publication_fix/restart.json','publication_fix/installed_verification.json','live_validation.json','LIVE_TEST_FIRST_JOB.json')]
    shared={'science_release':'v394','new_binary_required':False,'new_binary_built':False,'client_resources_changed':False,'physical_installation_verified':False,'store_distribution_reinspected':False}
    d={'status':'PASS','release':'v394','reference':str(task.REF),'identity':installed['identity'],'queue_generation':queue['generation'],
        'effective_files_verified':installed['files_verified'],'haiku_permanent_tokens':installed['haiku_permanent_tokens'],
        'matrix':{'web':{**shared,'authenticated_automatic_chat_verified':True,'Haja_Luz_continuation_verified':True},
        'ios_internal':{**shared,'availability':'Existing app uses the updated shared backend; no new TestFlight build in this delivery.'},
        'ios_external':{**shared,'availability':'Existing invited users use the same updated backend; no group membership changed.'},
        'android':{**shared,'availability':'Existing client uses the updated shared backend; no Google Play publication in this delivery.'},
        'scientific_queue':{'release':'v394','generation':queue['generation'],'three_modes_verified':True,'pinned_jobs_preserved':True},
        'bancada':{'release':'v394','read_only_state_verified':True,'restarted_by_this_delivery':False}},
        'science_executed':False,'scientific_gate_changed':False,'accounts_wallet_consents_changed':False,
        'limitations':['Backend effective use was tested through the authenticated web app, not physical iPhone/iPad/Android hardware.','All package admissions were checked; paid response generation was tested in automatic mode rather than every provider.','The first synthetic response took about181.5 seconds and exposed a stale publication label. Its receipt was preserved; exactly two operational labels and dependent bindings were corrected before final tests.','This delivery does not establish a scientific proof or physical confirmation.'],
        'evidence':evidence,'at_epoch':time.time()}
    task.new('delivery.json',d)
    print(json.dumps({'status':'PASS','release':'v394','effective_files':installed['files_verified'],'client_changes':False}))

if __name__=='__main__':main()
