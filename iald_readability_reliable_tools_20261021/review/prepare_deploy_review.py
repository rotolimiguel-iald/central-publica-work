from pathlib import Path
import datetime, hashlib, json, re

W = Path(__file__).resolve().parents[1]
evidence = {}
checks = []

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def read(name):
    p = W / name
    raw = p.read_bytes()
    evidence[str(p)] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw)

def check(name, value):
    checks.append({'check': name, 'passed': bool(value)})

plan = read('install_plan.json')
review = read('validation/review_final.json')
installed = read('INSTALLED_VERIFICATION.json')
deployment = read('deployment.json')
restart = read('restart.json')
web = read('WEB_LIVE_VALIDATION.json')
mobile = read('validation/mobile_review.json')
audit = read('mobile_stage/AUDIT.json')
commit = read('mobile_stage/COMMIT.json')
push = read('mobile_stage/PUSH.json')
publication = read('APK_PUBLICATION.json')
auth = read('ANDROID_AUTH_DOWNLOAD.json')
anon = read('ANDROID_ANON_DOWNLOAD.json')
science = read('SCIENCE_BASELINE.json')
check('install_plan_review_receipts_same_pin', review['status'] == 'PASS' and
      digest(W/'install_plan.json') == review['plan_sha256'] == installed['plan_sha256'] == deployment['plan_sha256'])
for key, name in [('transaction_sha256','transaction.py'), ('maintenance_sha256','maintenance.py'), ('deploy_controlled_sha256','deploy_controlled.py')]:
    check(name+'_reviewed_pin', digest(W/name) == review[key])
check('twelve_destinations', len(plan['files']) == installed['files'] == len(deployment['files']) == len(deployment['backups']) == 12)
for f in plan['files']:
    check('installed:'+f['destination'], digest(f['destination']) == f['sha256'] == deployment['files'][f['destination']])
    check('backup:'+f['destination'], digest(deployment['backups'][f['destination']]) == f['baseline'])
for f in science['files']:
    check('science:'+f['role'], digest(f['path']) == f['sha256'])
check('restart_receipts', restart == installed['restart'] and restart['status'] == 'PASS' and restart['http_status'] == 200 and restart['old_web_pid'] != restart['new_web_pid'])
check('web_recorded_requirements', web['status'] == 'PASS_UI_NO_MODEL_CALLS' and web['prose_px'] == 15.5 and web['input_px'] >= 16 and not web['permanent_media_banner'] and web['multiple_text_attachments'] == 2 and web['audio_rejected_locally'] and web['historical_conversation_visible'] and web['provider_calls'] == 0)
for key,name in [('runner_sha256','mobile_release.py'),('publisher_sha256','publish_apk31.py'),('init_sha256','android31.init.gradle')]:
    check('mobile_review_pin:'+name, digest(W/name) == mobile[key])
check('mobile_distinct_review', mobile['status'] == 'PASS' and mobile['round'] == 'R3' and mobile['reviewer_actor'] == 'codex-client-stage-independent-mobile-reviewer')
check('android_audit', audit['status'] == 'PASS' and audit['versionCode'] == 31 and audit['signer_matches_previous'] and audit['build']['exit_code'] == 0 and audit['build']['filtered_lines'] == 0)
for key in ['apk','aab']:
    check('artifact_pin:'+key, digest(audit[key]) == audit[key+'_sha256'])
check('build_log_pin', digest(audit['build']['log']['path']) == audit['build']['log']['sha256'])
for name in ['apk_signature','baseline_signature','aab_signature','aab_certificate','badging']:
    receipt = read('mobile_stage/build31/'+name+'.receipt.json')
    log = W/'mobile_stage/build31'/ (name+'.utf8.log')
    evidence[str(log)] = digest(log)
    check('existing_signature_receipt:'+name, receipt['exit_code'] == 0 and receipt['filtered_lines'] == 0 and digest(log) == receipt['log']['sha256'])
check('publication_download_chain', audit['apk_sha256'] == publication['sha256'] == auth['sha256'] == digest(publication['path']) == digest(auth['download_path']) and publication['bytes'] == auth['bytes'])
check('download_receipts', auth['status'] == anon['status'] == 'PASS' and anon['http_status'] == 302 and anon['location'] == '/login' and anon['apk_bytes_returned'] == 0)
check('commit_push_receipts', commit['commit'] == push['commit'] and push['status'] == 'PUSHED_VERIFIED' and push['ios_build'] == '4.1(36)')
expected = ['www/iald.js','www/iald.css','ios/App/App/public/iald.js','ios/App/App/public/iald.css','ios/App/App.xcodeproj/project.pbxproj','android/app/build.gradle']
root = Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
check('six_commit_files', set(commit['files']) == set(expected) and all(deployment['files'][str(root/n)] == h for n,h in commit['files'].items()))
check('android_resources_match_stage', all(digest(W/'client_stage/R2'/n) == h for n,h in audit['resources'].items()))
failed = [c for c in checks if not c['passed']]
report = {
    'status': 'BLOCK' if failed else 'PREPARED_PENDING_FINAL_EVIDENCE',
    'documentary_review': 'BLOCK' if failed else 'PASS_AVAILABLE_RECEIPTS',
    'reviewer': 'codex-readability-reviewer',
    'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'unit': 'F9.APP_READABILITY_RELIABLE_TOOLS_20261021',
    'scope': 'Revisão documental preparatória de deploy; comparação local de hashes e recibos existentes, sem novos testes, Git, build, rede ou provedores.',
    'plan_sha256': digest(W/'install_plan.json'),
    'checks': checks, 'findings': failed,
    'evidence': [{'path': p, 'sha256': h} for p,h in evidence.items()],
    'pending': [
        {'id': 'IOS_DISTRIBUTION', 'required': 'Recibo da build4.1(36) concluída, vinculada ao commit revisado, status real em IALD Equipe e IALD Piloto e identidade/participação do operador; limites de instalação física explícitos.'},
        {'id': 'MEMORY_FINAL', 'required': 'Recibo final de memória com fontes/hashes e matriz de disponibilidade web, iOS interno/externo e Android, incluindo canais/pendências.'}
    ],
    'interpretation': ['deployment.json, COMMIT.json e APK_PUBLICATION.json são retratos intermediários; restart.json, PUSH.json e ANDROID_*DOWNLOAD.json documentam as respectivas etapas posteriores.', 'A referência ACOM própria foi recuperada na revisão8, evento readability-web-installed.', 'O PASS mobile R3 de outro revisor é citado e vinculado por hash; validation/mobile_review.json não foi alterado.'],
    'limits': ['HTTP, interface, assinaturas e envio remoto são sustentados pelos recibos existentes; não foram reproduzidos nesta rodada.', 'APK/AAB e arquivos locais foram apenas lidos para integridade. Google Play e instalação física não são comprovados por publicação de APK.', 'Nenhum aceite final de deploy, mudança do quadro ou transição ACOM nesta preparação.'],
    'deployment_accepted': False, 'new_tests': 0, 'provider_calls': 0,
    'availability': {'web':'RECORDED_PASS','android_apk':'RECORDED_AUTHENTICATED_DOWNLOAD_PASS','android_aab':'LOCAL_AUDIT_PASS','ios':'PENDING_DISTRIBUTION_EVIDENCE','google_play':'NOT_PROVEN'}
}
out = W/'review/deploy_preparation.json'
if out.exists():
    backup = out.with_name(out.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    old = out.read_bytes(); backup.write_bytes(old); assert backup.read_bytes() == old
raw = json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8')
tmp = out.with_suffix('.json.tmp'); tmp.write_bytes(raw); assert tmp.read_bytes() == raw; tmp.replace(out)
print(json.dumps({'status':report['status'],'checks':len(checks),'failed':failed,'report':str(out),'sha256':digest(out)},ensure_ascii=False))
