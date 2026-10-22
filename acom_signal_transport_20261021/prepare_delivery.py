"""Aggregate measured receipts and operator-facing UI observations; no deployment."""
import json,hashlib,sqlite3
from pathlib import Path
from task import W,new,check
check('deployment')
def load(p):return json.loads((W/p).read_bytes())
def pin(p):
    f=W/p
    return {'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
post=load('LIVE_POST_EXECUTION.json');assert post['job']['status']=='completed'
intent=load('LIVE_POST_INTENT.json')
dbpath=Path(r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\chat_jobs\jobs.sqlite3')
with sqlite3.connect(dbpath.as_uri()+'?mode=ro',uri=True) as db:
    ids=[x[0] for x in db.execute('SELECT id FROM jobs WHERE created>=?',(intent['started'],))]
assert ids==[post['job']['id']], 'Do not guess unrelated job identity'
new('live_validation.json',{'status':'PASS_WITH_PRESERVED_INITIAL_ADMISSION_FAILURE','expected':'TRANSPORTE_INTEGRO_73','observed_in_browser':'TRANSPORTE_INTEGRO_73','recovered_after_reload':True,'new_jobs_after_reload':0,'duration_seconds':post['duration_seconds'],'model':post['model'],'evidence':[pin(p) for p in ['LIVE_POST_EXECUTION.json','LIVE_POST_JOB_RESULT.json','LIVE_POST_SUCCESS.png','LIVE_POST_RECOVERED.png','LIVE_DIAGNOSIS.json','LIVE_INITIAL_FAILURE.png','FINAL_RUNTIME_PINS.json']], 'limits':['Synthetic text attachment only; no general model-quality or latency-gain claim','No physical iPhone/iPad/Android runtime inspection','Live wire byte counts were not captured; codec and actual HTTP contract were tested separately','First job refused locally before MiMo; new post-fix job, no uncertain retry']})
for name,group,count in [('EQUIPE','IALD Equipe',1),('PILOTO','IALD Piloto',6)]:
    text=(W/f'mobile_stage/IOS37_{name}.txt').read_text(encoding='utf-8')
    assert group in text and 'Compilação 4.1 (37)' in text
    first=text.index('row Compilação 4.1 (37)')
    assert 'Em testes' in text[first:first+1300]
push=load('mobile_stage/PUSH.json');assert push['status']=='PUSHED_VERIFIED'
new('mobile_stage/IOS37_DISTRIBUTION.json',{'status':'AVAILABLE_BOTH_GROUPS','version':'4.1(37)','commit':push['commit'],'cloud':'Processada com sucesso','groups':[{'name':'IALD Equipe','type':'internal','testers':1,'status':'Em testes','operator_member_verified':True},{'name':'IALD Piloto','type':'external','testers':6,'status':'Em testes'}],'operator_last_installed_observed':'4.1(36)','physical_installation_verified':False,'expiry_display':'Expira em 90 dias','expires_at':None,'exact_expiry_unknown':True,'notes_saved':True,'testers_automatically_notified_setting':True,'evidence':[pin('mobile_stage/'+n) for n in ['IOS37_CLOUD.png','IOS37_GROUPS.png','IOS37_EQUIPE.png','IOS37_EQUIPE.txt','IOS37_PILOTO.png','IOS37_PILOTO.txt']]})
apk=load('ANDROID32_DOWNLOAD.json');assert apk['status']=='PASS'
new('availability.json',{'status':'WEB_IOS_BOTH_GROUPS_ANDROID_APK_AVAILABLE','availability':{'web':'Backend e cliente instalados; anexo sintético respondido e recuperado após recarga','ios_internal':'4.1(37) Em testes; IALD Equipe, 1 tester; participação do operador conferida','ios_external':'4.1(37) Em testes; IALD Piloto, 6 testers','android':'4.1(32) APK/AAB assinados; APK publicado, download autenticado e hash conferidos','google_play':'Não publicado nesta entrega; cadastro do canal permanece pendente','physical_installation_verified':False},'pending':['Teste físico no iPhone/iPad/Android não realizado','Google Play não publicado'],'limitations':['Compactação sem perdas reduz bytes quando vantajosa; não reduz tokens após descompactar nem comprova menor latência do modelo','Controle luminídico permanece experimental e não foi instalado no transporte','Expiração TestFlight exata não informada: Apple mostra prazo relativo de 90 dias'],'evidence':[pin('mobile_stage/IOS37_DISTRIBUTION.json'),pin('ANDROID32_DOWNLOAD.json'),pin('APK_PUBLICATION.json'),pin('live_validation.json')]})
new('delivery.json',{'status':'INSTALLED_VERIFIED_LIVE_PASSED_MOBILE_AVAILABLE','runtime_files':18,'science_files_preserved':5,'transport':'Negotiated stateless zlib DEFLATE/base64 exact UTF8 envelope; identity if no gain/unavailable; page-wise replies; no uncertain POST retry','budget_fix':'Final provider JSON measured after output field insertion; MiMo/DeepSeek, limits/policies preserved','luminidic_control':'Experimental isolated fixture only, not deployed','evidence':[pin(p) for p in ['FINAL_RUNTIME_PINS.json','deployment.json','restart.json','budget_fix/deployment.json','budget_fix/restart.json','validation/review_final.json','budget_fix/validation/review_final.json','live_validation.json','availability.json']],'final_independent_acceptance':'Pending separate receipt; do not infer from this aggregation'})
print('Final deployment/live/mobile receipts prepared')
