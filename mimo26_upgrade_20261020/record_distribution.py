from pathlib import Path
import json,hashlib,datetime
import task
W=Path(__file__).resolve().parent
def pin(name):
 p=W/name
 return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
task.project();task.check('deploy')
d={'status':'IOS34_BOTH_GROUPS_IN_TESTING','observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reference':str(task.REF),'version':'4.1(34)','commit':'58b17734efa8f7c815942ba60e95c5cc3dc033d0','cloud':'Processed successfully; push-triggered; no manual duplicate build','groups':{'IALD Equipe':{'type':'internal','testers':1,'status':'Em testes','operator_membership_verified':True},'IALD Piloto':{'type':'external','testers':6,'status':'Em testes'}},'physical_installation_verified':False,'last_operator_installed_observed':'4.1(33), 2026-10-18','expiry_exact_utc':None,'expiry_display_observed':'90 days; exact expiration not inferred','evidence':[pin('mobile_stage/'+n) for n in ['IOS34_CLOUD_SUCCESS.jpg','IOS34_EQUIPE.txt','IOS34_EQUIPE.jpg','IOS34_PILOTO.txt','IOS34_PILOTO.jpg']]}
task.new('mobile_stage/IOS34_DISTRIBUTION.json',d)
task.new('LIVE_AUTHORIZATION_PENDING.json',{'status':'AWAITING_SPECIFIC_OPERATOR_APPROVAL','request_sent':False,'image_attached_only':True,'auto_review_rejection':'MiMo/Xiaomi scientific-context and synthetic-image transmission requires specific authorization and current consent. No bypass.','questions_pending':['MiMo v2 scientific public v394 + synthetic two-color image, tone audio and red video; up to USD1; no private Atlas','JEV v3 derived operational state and custody references for this synthetic test, no attachments or private Atlas'],'consents_accepted_this_delivery':False,'no_remote_uncertain_retry':True})
print(json.dumps({'status':d['status'],'live':'AWAITING_OPERATOR'},ensure_ascii=False))
