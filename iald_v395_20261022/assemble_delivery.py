"""Record installed scope separately from the authenticated test still pending."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import task
W=task.W
def pin(name):
    p=W/name;b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
    assert task.check('verify')['ready']
    i=json.loads((W/'INSTALLED_VERIFICATION.json').read_bytes())
    r=json.loads((W/'restart.json').read_bytes());assert i['status']==r['status']=='PASS'
    q=json.loads((W/'QUEUE_CURRENT.json').read_bytes());assert q['status']=='CURRENT'
    d=json.loads((W/'deployment.json').read_bytes());assert not d['client_files_changed']
    live='PENDENTE — login expirado; solicitado ao operador. Nenhuma resposta live desta versão foi testada.'
    shared={'science_release':'v395','shared_backend':True,'client_changed':False,'new_build_needed':False,'physical_installation_verified':False,'store_groups_reinspected':False}
    out={'status':'INSTALLED_VERIFIED_AUTHENTICATED_TEST_PENDING','release':'v395','installed_verified':True,
         'reference':str(task.REF),'identity':i['identity'],'at':datetime.now(timezone.utc).isoformat(),
         'files_verified':i['files_verified'],'authenticated_live_status':live,
         'matrix':{name:dict(shared) for name in ('web','ios_internal','ios_external','android')},
         'queue':q,'bancada':'B5-v395 read-only verified; not redeployed',
         'custody_site_repository_devices':'Existing custody receipt reused; no new publication',
         'scientific_execution':False,'gate_changed':False,'new_provider_generations':0,'public_token_count_requests':6,
         'evidence':[pin(n) for n in ('INSTALLED_VERIFICATION.json','deployment.json','restart.json','install_plan.json','validation/review_final.json','app/NATIVE_COUNTS_COMPLETE.json','QUEUE_CURRENT.json','BANCADA_CURRENT.json','CUSTODY_REUSED.json')]}
    task.new('DELIVERY.json',out)
    print(out['status'])
if __name__=='__main__':main()
