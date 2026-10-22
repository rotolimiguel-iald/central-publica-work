"""Run/pin this backend front; no runtime installation or reviewer impersonation."""
import ast
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

W=Path(__file__).resolve().parent;P=W.parent;R=Path('C:/IALD/projetos_pyhton/IALD')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
dependency=P/'routing_stage/iald_media_budget.py'
dependency_pin=sha(dependency)
tests=[('test_private_media.py','TEST_RESULTS.json'),('test_provider_boundary.py','PROVIDER_TEST_RESULTS.json'),
       ('test_private_routes.py','ROUTE_TEST_RESULTS.json'),('test_upload_lifecycle_R2.py','LIFECYCLE_R2_TEST_RESULTS.json')]
results=[]
for script,receipt in tests:
    completed=subprocess.run([sys.executable,'-B','-X','utf8',str(W/script)],capture_output=True,timeout=60)
    report=json.loads((W/receipt).read_bytes())
    if completed.returncode or not report['passed']:raise RuntimeError({'script':script,'stderr':completed.stderr.decode(errors='replace')})
    results.append({'script':script,'receipt':receipt,'sha256':sha(W/receipt),'tests':report['tests'],'passed':True})
assert sha(dependency)==dependency_pin,'Goodall dependency changed while testing; rerun against new pin'
source=json.loads((W/'PROVIDER_SOURCE.json').read_bytes())
assert sha(R/'iald_app_providers.py')==source['runtime_sha256']
for name in ('private_media_store.py','private_media_routes.py','iald_mimo_multimodal.py','iald_app_providers.py'):
    ast.parse((W/name).read_bytes())
symbols={}
tree=ast.parse((W/'private_media_store.py').read_text(encoding='utf-8'))
for node in tree.body:
    if isinstance(node,ast.ClassDef) and node.name=='PrivateMediaRuntime':
        symbols[node.name]={fn.name:ast.unparse(fn.args) for fn in node.body if isinstance(fn,ast.FunctionDef) and not fn.name.startswith('_')}
    if isinstance(node,ast.FunctionDef) and node.name in ('resolve_media_metadata','client_capabilities','reject_worker_media','contains_media'):
        symbols[node.name]=ast.unparse(node.args)
files=['private_media_store.py','private_media_routes.py','iald_mimo_multimodal.py','iald_app_providers.py',
       'providers.patch','CONTRACT.json','METADATA_INTERFACE.json','HOST_INTEGRATION.md',
       'test_private_media.py','test_provider_boundary.py','test_private_routes.py','test_upload_lifecycle_R2.py']
report={'status':'BACKEND_R2_CANDIDATE_TESTED_READY_FOR_DISTINCT_REVIEW_NOT_INSTALLED',
    'generated_utc':datetime.now(timezone.utc).isoformat(),
    'reference':str(P/'SESSION_REFERENCE.json'),'context_id':'bcf544f7-1878-5d27-b532-f1e1aad466aa',
    'unit':'F9.MIMO_MEDIA_CAPACITY_20261020','tests':sum(r['tests'] for r in results),'test_results':results,
    'files':{name:sha(W/name) for name in files},
    'dependency':{'path':str(dependency),'sha256':dependency_pin,'single_budget_engine':True,
        'usage':'adapt_resolved_metadata + legacy_inline_metadata + options/plan_request + reserve_existing + spending_bound + exact wire policy/byte checks'},
    'runtime_provider_baseline':source['runtime_sha256'],'runtime_unchanged':True,
    'public_interfaces':symbols,
    'review_findings':{
        'MEDIA_R1_M1_UPLOAD_REVOKE_RACE':{'candidate_fix':'Exclusive publication transaction rechecks auth/status/lease before any temp file creation; write verified, renamed and active status committed under same DB lock; revoked tombstone cannot resurrect.','regressions':'conversation and account delete during validation both fail visibly with no orphan/blob/quota success.','distinct_reviewer_status':'RETEST_PENDING'},
        'MEDIA_R1_M2_STALE_RESERVATIONS_GLOBAL_LOCKOUT':{'candidate_fix':'Durable PID+birth+300s unpublished upload lease; startup/admission reconciles proven abandoned intents/files only; active retained media never reaped.','regressions':'Four actual child os._exit interruptions, other-owner successful upload, live unexpired upload preserved, orphan temp cleaned, active blob preserved.','distinct_reviewer_status':'RETEST_PENDING'}},
    'retention':'No expiry of active files; explicit conversation/account delete only;technical upload leases do not cap audio/video duration.',
    'capacity':{'full_data_uri_decimal_bytes':50000000,'raw_bytes':37499904,'header_margin_bytes':128,'provider_json_bytes':64000000,'no_fixed_audio_video_duration_cap':True},
    'integration_handoff':{
        'owner':'PARENT/Averroes host_stage; no edits of main server or app_spend by this front',
        'required':'Use HOST_INTEGRATION.md. Pass host configured rates and selected video_policy explicitly. runtime.admit RETURNS RAW GOODALL PLAN with input_tokens_bound/output_reserved_tokens (not wrapper); provider here consumes those names. expand REQUIRES plan= for current round; no blind use of old expand(body,provider) example.',
        'budget':'Parent merges Goodall SPENDING_INTEGRATION.diff; reserve_existing calls spending.before(...,media_plan=plan) once. Missing integrated guard refuses, never bypasses.',
        'routing':'Before choose, runtime.routing_options full body -> give budget.routing_options(plans) to JEV media_budget_options; select_routing_policy(choice); carry receipt.media_budget on host context. Legacy inline measured without blob re-ingestion.',
        'http':'Actual _RequisicaoIALD property branch returning MAX_RAW_BYTES belongs to parent; route adapter only verifies no setter/global override.',
        'worker':'Call reject_worker_media before any worker/nonMiMo credential, routing or request for BOTH inline audio/video and refs.',
        'new_conversation':'First upload establishes owner-generation-CID namespace; no prior model job required. Bootstrap media_scope partitions IndexedDB and drafts; not a bearer.',
        'probe':'Runtime vendor/ffmpeg pin path reused; staging real video test uses that verified runtime dependency without installation.'},
    'limitations':['Actual host session/CSRF/generation glue and client IndexedDB behavior require parent integration review.',
        'No maximum-size remote-provider benchmark; modality admission remains an explicit estimate and actual usage settles wallet.',
        'No calls to MiMo/JEV, no production writes, no public media URLs or remote fetching.',
        'The300s lease bounds publication/quota recovery, not interruption of a blocked OS/socket read; host transport timeout remains required.',
        'Existing lease-less private-media schema fails visibly and needs explicit migration; this new feature has not been installed.',
        'Failed Windows temporary-directory test artifact in earlier builder attempt and all reviewer snapshots/receipts retained; final tests use bounded staging temp roots.'],
    'scientific_package_changed':False,'consent_versions':'MiMo2/Auto3 preserved, no autogrant',
    'provider_calls':0,'installed':False}
target=W/'BACKEND_R2_HANDOFF.json'
with target.open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
manifest={'schema':'iald.backend-staging-freeze/v1','revision':'R2','files':report['files'],
    'handoff_sha256':sha(target),'dependency':report['dependency'],'tests':report['tests'],'installed':False}
with (W/'MANIFEST_R2.json').open('x',encoding='utf-8') as f:json.dump(manifest,f,indent=2)
print(json.dumps({'handoff':str(target),'manifest':str(W/'MANIFEST_R2.json'),'tests':report['tests'],'passed':True,'distinct_review':'PENDING','installed':False}))
