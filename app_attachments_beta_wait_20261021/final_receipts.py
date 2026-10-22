from task import *
def pin(p):
    p=Path(p);return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
def load(p):return json.loads(Path(p).read_bytes())
check('delivery')
plan=load(W/'release/install_plan.json'); r2=load(W/'repair/backend_R2/DELIVERY.json')
files=plan['files']+r2['files']
for f in files:assert pin(f['destination'])['sha256']==f['sha256']
for f in load(W/'release/SCIENCE_BASELINE.json')['files']:assert pin(f['path'])['sha256']==f['sha256']
text=(W/'LIVE_FINAL_SUCCESS.txt').read_text(encoding='utf-8')
assert 'vermelho | azul | ANEXO-73' in text
web=dict(status='PASS_AFTER_RECORDED_REFUSALS',response='vermelho | azul | ANEXO-73',attachments=['large_two_colors.png','fixture.pdf'],image_bytes=(W/'large_two_colors.png').stat().st_size,reload_during_generation=True,reload_after_completion=True,answer_preserved=True,waiting_count_after_completion=0,beta_animation='beta-wait-turn 3.6s',scope='Authenticated browser; no physical iPhone/Android inspection. Initial admission and budget refusals preserved; new validation after each repair, no replay of old request IDs.',evidence=[pin(W/n) for n in ['LIVE_FINAL_SUCCESS.txt','LIVE_FINAL_SUCCESS.jpg','LIVE_FINAL_RUNNING.jpg','LIVE_RUNNING.jpg','LIVE_BUDGET_REFUSAL.txt','LARGE_IMAGE_FAILURE.json']])
new('WEB_FINAL_VALIDATION.json',web)
ios=load(W/'release/IOS38_DISTRIBUTION.json');android=load(W/'release/ANDROID_AUTH_DOWNLOAD.json')
assert ios['status']=='AVAILABLE_BOTH_GROUPS' and android['status']=='PASS'
evidence=['release/install_plan.json','release/validation/review_final.json','release/deployment.json','release/restart.json','repair/backend_R2/REVIEW.json','repair/backend_R2/DEPLOYMENT.json','repair/backend_R2/RESTART.json','release/IOS38_DISTRIBUTION.json','release/mobile_stage/AUDIT.json','release/ANDROID_AUTH_DOWNLOAD.json','release/CHECK_APK_PUBLIC_R1.json','WEB_FINAL_VALIDATION.json']
new('delivery.json',dict(status='INSTALLED_LIVE_VALIDATED_MOBILE_AVAILABLE',unique_files=len(files),installed_files=[pin(f['destination']) for f in files],science='Five pinned sources unchanged, v394/kernel preserved; no scientific execution or gate change',offline_tests=63,web=web['status'],ios=ios,android=dict(version='4.1(33)',apk_available=True,authenticated_download_verified=True,google_play_published=False,physical_installation_verified=False),limits=['Image token budget is engineering estimate, not vendor tokenizer.','Physical phone tests not performed.','HEIC and audio/video remain unavailable.','Document limits and text extraction/context admission remain applicable.','Google Play channel remains unpublished.'],evidence=[pin(W/n) for n in evidence]))
print('Final receipts and all installed bytes verified')
