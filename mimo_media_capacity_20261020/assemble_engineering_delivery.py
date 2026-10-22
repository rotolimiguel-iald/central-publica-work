"""Assemble measured availability and explicit limits before memory closeout."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
W=Path(__file__).resolve().parent
def load(relative):return json.loads((W/relative).read_bytes())
def pin(relative):
    p=W/relative;raw=p.read_bytes()
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
runtime=load('FINAL_RUNTIME_PINS_R8.json')
for item in runtime['files']:
    assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256']
ios=load('mobile_stage/IOS35_DISTRIBUTION.json')
assert all(group['status']=='Em testes' for group in ios['groups'])
download=load('mobile_stage/ANDROID30_AUTHENTICATED_DOWNLOAD.json')
assert download['matches_signed_audited_apk'] is True
matrix=dict(web=dict(status='ACTIVE',url='https://demo.iald.ia.br/app/index.html'),
 ios_internal=dict(version='4.1(35)',group='IALD Equipe',status='Em testes',operator_participation_verified=True),
 ios_external=dict(version='4.1(35)',group='IALD Piloto',status='Em testes',testers=6),
 android=dict(version='4.1(30)',status='AUTHENTICATED_APK_PUBLISHED_AND_HASH_VERIFIED',
  url='https://demo.iald.ia.br/downloads/IALD-4.1-30.apk',bytes=download['bytes'],sha256=download['sha256']),
 google_play='NOT_PUBLISHED_IN_THIS_DELIVERY',physical_device_tests='NOT_VERIFIED',
 apple_reported_operator_installation='4.1(35),20Oct2026; provider report, not a physical test by this session')
sources=['FINAL_RUNTIME_PINS_R8.json','WEB_LIVE_SCOPE.json','SCIENCE_BASELINE.json',
 'host_stage/REAL_BYTE_BOUNDARY.json','live_stage/MANUAL_AUDIO_RESULT.json',
 'live_stage/MANUAL_VIDEO_RESULT.json','live_stage/MANUAL_VIDEO_TIMEOUT_DIAGNOSIS_R1.json',
 'live_stage/TEST_COST_ROLLUP_R1.json','mobile_stage/IOS35_DISTRIBUTION.json',
 'mobile_stage/ANDROID30_AUTHENTICATED_DOWNLOAD.json','mobile_stage/ANDROID30_ANONYMOUS_DOWNLOAD.json',
 'mobile_stage/apk30_publication/FINAL_R3/PUBLICATION_RESULT.json',
 'admin_deadlines35stage/DELIVERY_APPLIED_R1.json','extra_test_pending_unit.json']
value=dict(status='ENGINEERING_DEPLOYED_WITH_DOCUMENTED_PROVIDER_LIMITS',
 observed_at=datetime.now(timezone.utc).isoformat(),reference=str(W/'SESSION_REFERENCE.json'),
 scope='Increased private media admission, context/cost accounting and coordinated beta clients. Not full vendor perception validation.',
 max_raw_file_bytes=37499904,max_encoded_uri_bytes=50000000,
 fixed_audio_video_duration_caps_removed=True,duration_subject_to_context_and_transport=True,
 science_version='v394',science_preserved=True,weights_changed=False,
 availability=matrix,additional_paid_test='PENDING_EXPLICIT_USER_REPLY_UP_TO_USD0.50',
 limitations=['Audio120s completed but model declared inability to perceive it.',
  'Video30s failed with incomplete HTTP200 chunked stream; remote result and final usage uncertain. No retry.',
  'Video pessimistic debit is reserved cap, not measured provider cost or invoice.',
  'Job completed / wallet task cancelled discrepancy retained as an unresolved bookkeeping diagnostic.',
  'New automatic post-fix provider call not executed pending optional test-budget decision.'],
 memory_closeout='PENDING_REVIEWED_APPEND',final_mission_acceptance=False,
 sources=[pin(name) for name in sources])
for name,data in [('AVAILABILITY_MATRIX.json',matrix),('ENGINEERING_DELIVERY_PRE_MEMORY.json',value)]:
    with (W/name).open('xb') as f:f.write(json.dumps(data,ensure_ascii=False,indent=2).encode())
print('Availability matrix and engineering scope assembled with negative evidence')
