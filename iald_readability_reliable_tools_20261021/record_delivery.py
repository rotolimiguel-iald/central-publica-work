from task import W,new,check
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
check('deploy');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cloud=(W/'IOS36_CLOUD_SUCCESS.txt').read_text(encoding='utf-8');commit=json.loads((W/'mobile_stage/PUSH.json').read_bytes())['commit']
assert 'Processada com sucesso' in cloud and commit in cloud
for name,group in [('IOS36_EQUIPE.txt','IALD Equipe'),('IOS36_PILOTO.txt','IALD Piloto')]:
    t=(W/name).read_text(encoding='utf-8');assert group in t and 'Em testes' in t.split('row Compilação 4.1 (36)')[1].split('row Compilação 4.1 (35)')[0]
operator=(W/'IOS36_OPERATOR.txt').read_text(encoding='utf-8');assert 'Luiz Antonio Rotoli Miguel' in operator and 'Instalado 4.1' in operator and '( 35 )' in operator
sources=[dict(path=str(W/n),sha256=sha(W/n)) for n in ['IOS36_CLOUD_SUCCESS.txt','IOS36_BOTH_GROUPS.txt','IOS36_OPERATOR.txt','IOS36_EQUIPE.txt','IOS36_PILOTO.txt']]
new('IOS_DISTRIBUTION.json',dict(status='BOTH_GROUPS_VERIFIED',build='4.1(36)',commit=commit,cloud_build_id='d9c9a4a7-904f-4cac-b8c0-c316ddb3b788',testflight_build_id='173f1191-5212-4eea-b04b-4a1bdb444344',observed_utc=datetime.now(timezone.utc).isoformat(),internal=dict(group='IALD Equipe',testers=1,status='Em testes',operator_participation_verified=True),external=dict(group='IALD Piloto',testers=6,status='Em testes'),operator_last_installed_observed='4.1(35)',physical_installation_verified=False,expiry_exact=None,sources=sources))
matrix=dict(web='ACTIVE_UI_VERIFIED',ios_internal='4.1(36) Em testes',ios_external='4.1(36) Em testes',android='4.1(31) APK_AUTH_DOWNLOAD_VERIFIED',google_play='NOT_PUBLISHED_THIS_DELIVERY',physical_installation_verified=False,existing_invites_unchanged=True)
new('AVAILABILITY_MATRIX.json',matrix)
new('delivery.json',dict(status='ENGINEERING_DELIVERED_PENDING_FINAL_REVIEW',commit=commit,**matrix,plan_sha256=sha(W/'install_plan.json'),installed_files=12,science_version='v394',science_preserved=True,prose_px=15.5,input_px=16,new_audio_video_disabled=True,history_preserved=True,document_limits=dict(per_message=6,pdf_bytes=25000000,text_bytes=2000000,images=3,image_bytes=8000000),provider_calls=0,deepseek='Alias preserved; documentary V4.1-Flash-1017, existing peak estimate maintained with off-peak metadata; no new provider features claimed.',compression='ACOM/transport proposal recorded, not implemented; no token or latency gain claimed.'))
print('Both iOS groups and coordinated availability recorded')
