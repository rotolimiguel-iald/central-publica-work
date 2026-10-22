from pathlib import Path
import json,hashlib
import task
W=Path(__file__).resolve().parent
def read(name): return json.loads((W/name).read_bytes())
def pin(name):
 p=W/name;return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
task.project();task.check('deploy')
original=read('install_plan.json');followup=read('audio_followup/install_plan.json')
expected={x['destination']:x['sha256'] for x in original['files']}
expected.update({x['destination']:x['sha256'] for x in followup['files']})
for path,sha in expected.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha,path
task.new('FINAL_INSTALLED_PINS.json',{'status':'PASS','files':len(expected),'pins':expected,'science_release':'v394','supplementary_patch':'Host typed-media guidance only'})
names=['deployment.json','restart.json','INSTALLED_VERIFICATION.json','FINAL_INSTALLED_PINS.json','audio_followup/deployment.json','audio_followup/restart.json','audio_followup/validation/review_final.json','mobile_stage/IOS34_DISTRIBUTION.json','mobile_stage/ANDROID29_AUTHENTICATED_DOWNLOAD.json','mobile_stage/apk29_publication/DELIVERY_PUBLISHED_R1.json','LIVE_OPERATOR_APPROVAL.json','live_stage/FOUR_CALLS_COST.json','live_stage/IMAGE_RESULT.json','live_stage/AUDIO_RESULT.json','live_stage/VIDEO_RESULT.json','live_stage/AUDIO_POST_RESULT.json']
cost=read('live_stage/FOUR_CALLS_COST.json');assert float(cost['known_cost_estimate_usd'])<1
task.new('delivery.json',{'status':'TECHNICALLY_DELIVERED_PENDING_FINAL_REVIEW','reference':str(task.REF),'science_release':'v394','science_and_kernel_changed':False,'original_files':21,'supplementary_files':1,'unique_files':len(expected),'matrix':{'web':'Installed; image, video and post-guidance audio answered correctly via automatic MiMo; reload persisted responses','ios_internal':'4.1(34) Em testes; operator membership verified','ios_external':'4.1(34) Em testes; six existing testers','android':'4.1(29) signed audited APK/AAB; authenticated APK download hash verified; Google Play not published'},'physical_installation_verified':False,'known_cost_estimate_usd':cost['known_cost_estimate_usd'],'invoice_verified':False,'limits':['First audio answer failed; preserved. One successful post-guidance trial does not isolate causality or guarantee perception.','Synthetic fixtures only; audio 0.5 seconds and video 1 second. No speech/noise/long-media benchmark.','Local audio/video limits 512000 bytes and 30/10 seconds subject to context admission.','No native MiMo media generation or Python execution promised.','No scientific execution, scientific gate change or private Atlas egress.'],'evidence':[pin(n) for n in names]})
print(json.dumps({'status':'READY_FOR_FINAL_REVIEW','files':len(expected),'cost_estimate_usd':cost['known_cost_estimate_usd']}))
