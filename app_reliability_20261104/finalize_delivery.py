"""Custody of observed validation; no provider calls or runtime mutations."""
from pathlib import Path
import hashlib, json
from datetime import datetime, timezone
from task import W, REF, new, check, act, project

def pin(name):
    p=W/name
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

check('delivery')
observed=(W/'CHAT_AFTER_RELOAD.txt').read_text(encoding='utf-8')
if not all(x in observed for x in ['ChatGPT 5.6 Luna','MiMo V2.6 Pro','Luiz Antonio Rotoli Miguel','v407']):
    raise RuntimeError('Observed transcript does not support the validation')
live={
    'status':'PASS_WITH_SCOPE','at':datetime.now(timezone.utc).isoformat(),
    'method':'Authenticated browser observation by parent; evidence text and screenshot preserved',
    'turns':[
        {'selection':'manual','executor':'ChatGPT 5.6 Luna','result':'Correct author and deployed v407; no requested search or program execution'},
        {'selection':'automatico','executor':'MiMo V2.6 Pro','result':'Confirmed same author and v407 from conversation context'}],
    'reload':'Both answers visible after page reload',
    'composer':'Send enabled when parent typed an unsent synthetic text, then composer cleared',
    'left_selected':'automatico',
    'credential_probe':'Separate minimal official API probe HTTP200, 14 total tokens; not the full chat cost',
    'scope':['No induced production credential failure or live failover test; rejection recovery verified offline',
             'No private case consulted, no physical phone inspection',
             'These two turns do not certify general TGL accuracy or full context recall',
             'Chat costs and token counts not measured in this receipt',
             'Private Apple revalidation notice visible; public chat validation does not renew private access'],
    'evidence':[pin(x) for x in ['OPENAI_CHAT_RESULT.txt','OPENAI_CHAT_RESULT.jpg','AUTO_CHAT_RESULT.txt','CHAT_AFTER_RELOAD.txt','CHAT_AFTER_RELOAD.jpg','NEW_CREDENTIAL_PROBE.json']]
}
new('LIVE_VALIDATION.json',live)
prior=json.loads((W/'DELIVERY_PROGRESS.json').read_text())
final={
    'status':'INSTALLED_AUTHENTICATED_CHAT_VERIFIED','at':datetime.now(timezone.utc).isoformat(),
    'reference':str(REF),'complements':pin('DELIVERY_PROGRESS.json'),
    'installed_files':5,'scientific_files_unchanged':1782,'science_version':'v407',
    'v408':'Final sealed/published release not observed in inspected sources; no speculative activation',
    'recovery_scope':prior['recovery_scope'],
    'recovery_exclusions':['Manual selection','Other initial providers','Attachments','Private chat','Timeout, unknown execution or partial output'],
    'tests':prior['tests'],
    'credentials':{'old_failure':'HTTP401 expired_secret_key','new_provider_state':'Active / Nunca',
                   'permissions':'Restricted: Chat completions request','storage':'Dedicated protected server file; existing environment configuration unchanged',
                   'acl':'Current Windows user and SYSTEM only; inheritance disabled','api_probe':'HTTP200 / OK / 14 tokens',
                   'reload':'Only web child under same supervisor; HTTP200',
                   'ui_observation_limit':'A hidden credential input appeared in an AX tool snapshot after closing the modal. No credential value is reproduced in these receipts; absence of all exposure is not claimed.'},
    'administration':{'validity_registry':'Updated with explicit expires_never and observed provenance; visible only to internal administration',
                      'verification':'Local snapshot function and source renderer; administrative browser view not authenticated and not claimed'},
    'availability':{
        'web':'Backend active; manual OpenAI and AUTO/MiMo chat and reload verified',
        'ios_internal':'Shared backend active; no client change or new TestFlight binary required; store/device not reinspected',
        'ios_external':'Same shared backend; no new distribution or tester change',
        'android':'Same shared backend; no new client binary; no device test',
        'google_play':'No publication in this delivery; historic registration pendency not resolved here'},
    'remaining_product_work':[],
    'limits':['Recovery rejection branch tested offline, not induced in live production',
              'No guarantee against future provider revocation, credit exhaustion or downtime',
              'No program/Lean execution, scientific gate change, TGL retraining or private-data transfer',
              'v408 activation depends on matching final seal, custody/publication and updater delivery'],
    'sources':[pin(x) for x in ['DEPLOYMENT.json','INSTALLED_VERIFICATION.json','RESTART.json','CREDENTIAL_RELOAD.json','CREDENTIAL_DELIVERY.json','LIVE_VALIDATION.json','review/RELEASE_REVIEW.json','review/RECOVERY_ACCEPT_RECEIPT.json','review/credential/CREDENTIAL_ACCEPT_RECEIPT.json','science/ACCEPT_RECEIPT.json','credential/VALIDITY_UPDATED.json']]
}
new('FINAL_DELIVERY.json',final)
p=project();lease=next(x for x in p['projection']['active'] if x['id']=='delivery')['lease']['id']
result=act('submit',task_id='delivery',lease_id=lease,event_id='app-reliability-final-delivery-submitted',evidence=[pin('FINAL_DELIVERY.json'),pin('LIVE_VALIDATION.json')])
new('FINAL_SUBMITTED.json',result)
print(json.dumps({'final':pin('FINAL_DELIVERY.json'),'revision':result['receipt']['revision']}))
