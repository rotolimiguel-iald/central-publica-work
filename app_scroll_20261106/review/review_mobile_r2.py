from pathlib import Path
import json,hashlib,zipfile,re,subprocess,os,datetime
W=Path(r'C:\IALD\Central de Patentes\work\app_scroll_20261106');R=W/'review';D=W/'mobile/release';B=D/'build42';repo=Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
pins={};checks=[]
def pin(p):
 p=Path(p);v={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};pins[str(p)]=v;return v
def read(p):pin(p);return json.loads(Path(p).read_bytes())
def verify(v):assert pin(v['path'])['sha256']==v['sha256'],v['path']
def ok(name,v):assert v,name;checks.append(name)
audit=read(D/'AUDIT.json');pub=read(D/'APK_PUBLICATION.json');intent=read(D/'PUBLICATION_INTENT.json');anon=read(D/'ANONYMOUS_DOWNLOAD.json');push=read(D/'PUSH.json');commit=read(D/'COMMIT.json');pi=read(D/'PUSH_INTENT.json');archive=read(D/'IOS_ARCHIVE_FINAL.json');ios=read(D/'IOS47_DISTRIBUTION.json');plan=read(W/'mobile/PLAN.json')
for prior in ['REVIEW_R1.json','DEPLOY_REVIEW_R1.json','PUSH_BYTES_REVIEW.json']:
 review=read(R/prior)
 for p in review.get('pins',[]):verify(p)
 checks.append('prior_review_pins_'+prior)
for p in ios['evidence']:verify(p)
verify(pi['receipt']);verify(pi['review']);verify(intent['authorization']);verify(intent['source'])
for kind,prefix in [('apk','assets/public/'),('aab','base/assets/public/')]:
 p=Path(audit[kind]);ok(kind+'_artifact_hash',pin(p)['sha256']==audit[kind+'_sha256'])
 with zipfile.ZipFile(p) as z:
  ok(kind+'_zip_integrity',len(z.namelist())==len(set(z.namelist())) and z.testzip() is None)
  for name,h in audit['resources'].items():ok(kind+'_'+name+'_reviewed_bytes',hashlib.sha256(z.read(prefix+name)).hexdigest()==h==pin(W/'stage'/name)['sha256'])
for receipt in sorted(B.glob('*.receipt.json')):
 r=read(receipt);verify(r['log']);ok(receipt.name+'_success',r['exit_code']==0 and r['filtered_lines']==0)
logs={}
for name in ['apk_signature','baseline_signature','aab_certificate','aab_signature','badging']:
 p=B/(name+'.utf8.log');pin(p);logs[name]=p.read_text(encoding='utf-8')
cert=lambda s:re.findall(r'certificate SHA-256 digest:\s*([0-9a-fA-F]+)',s)
ok('recorded_signer_matches_previous',cert(logs['apk_signature'])==cert(logs['baseline_signature']) and len(cert(logs['apk_signature']))==1)
aabcert=re.findall(r'SHA256:\s*([0-9A-Fa-f:]+)',logs['aab_certificate'])
ok('recorded_aab_signer_matches_apk',len(aabcert)==1 and aabcert[0].replace(':','').lower()==cert(logs['apk_signature'])[0].lower())
ok('recorded_apk_version',"versionCode='42'" in logs['badging'] and "versionName='4.1'" in logs['badging'])
ok('recorded_aab_signature', 'jar verified.' in logs['aab_signature'].lower() and 'unsigned entries' not in logs['aab_signature'].lower() and 'jar is unsigned' not in logs['aab_signature'].lower())
verify(pub['artifact']);ok('published_apk_equals_audit',pub['artifact']['sha256']==audit['apk_sha256'] and Path(pub['artifact']['path']).stat().st_size==pub['bytes'])
for name,h in intent['older'].items():ok('older_apk_'+name,pin(Path(intent['target']).parent/name)['sha256']==h)
ok('26_older_apks',len(intent['older'])==pub['older_preserved']==26)
ok('anonymous_receipts_deny_apk',len(anon)==2 and all(a['status'] in (302,403) and a['apk_header'] is False for a in anon))
def git(*args):
 env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
 return subprocess.check_output(['git','-C',str(repo),*args],env=env,stderr=subprocess.DEVNULL)
expected=commit['commit'];ok('same_commit_push_archive',expected==push['commit']==pi['commit']==archive['head_sha'])
ok('local_commit_parent',git('rev-parse',expected+'^').decode().strip()==commit['base']==plan['baseline']['base_commit'])
changed=set(git('diff','--name-only',commit['base'],expected).decode().splitlines());ok('six_commit_files',changed==set(plan['tracked_files'])==set(commit['pins']) and len(changed)==6)
for name,h in commit['pins'].items():ok('commit_blob_'+name,hashlib.sha256(git('show',expected+':'+name)).hexdigest()==h)
ok('archive_success',archive['status']=='completed' and archive['conclusion']=='success')
ok('ios_receipt_scoped',ios['status']=='BOTH_GROUPS_TESTING' and ios['build']=='4.1 (47)' and ios['physical_device_inspected'] is False and ios['submission_actions']==1 and 'no persisted Equipe screenshot' in ios['evidence_scope'])
ax=(D/'IOS47_PILOTO.txt').read_text(encoding='utf-8');row=ax.split('row Compilação 4.1 (47)',1)[1].split('row Compilação 4.1 (46)',1)[0]
ok('piloto_archived_AX', 'Grupo externo ∙ 6 testers' in ax and 'text Em testes' in row and ios['build_id'] in row)
installed=read(W/'INSTALLED.json');ip=read(W/'INSTALL_PLAN.json')
for r in installed['files']:ok('installed_'+str(len(checks)),pin(r['target'])['sha256']==r['new'])
for r in ip['preserve']:verify(r)
checks.append('1797_protected_pins_unchanged')
# Avoid copying the 1797-path preservation inventory into a second report; source plan remains pinned.
protected={r['path'] for r in ip['preserve']};pins={k:v for k,v in pins.items() if k not in protected}
report={'status':'PASS_WITH_SCOPE','reviewer':'codex-scroll-independent-reviewer','task_id':'mobile','mission_revision_observed':14,'mission_status_observed':'working','mission_acceptance_performed':False,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'check_count':len(checks),'pins':list(pins.values()),'commit':expected,'plan_sha256':pin(W/'mobile/PLAN.json')['sha256'],'assessment':'Integrity and non-overclaim review passes with the evidence scopes and outstanding items below; not a new code test, remote verification or mission acceptance.',
 'android':{'version':'4.1 (42)','apk_aab_hashes_and_embedded_assets':'verified locally','signatures':'existing successful verifier logs/receipts pinned and compared; cryptographic verification not reexecuted','published_bytes':pub['bytes'],'older_apks_verified':26,'anonymous':'recorded local302/public403 without APK header; no new HTTP call','authenticated_download':'PENDING','google_play':'NOT_PUBLISHED','physical_installation':'NOT_VERIFIED'},
 'ios':{'version':'4.1 (47)','archive':'success receipt from Xcode Cloud GitHub check matches exact pushed commit','piloto':'6 testers, Em testes: persisted screenshot visually inspected and AX/hash checked','equipe':'1 tester, Em testes and operator membership: direct parent tool observation reported in receipt/user handoff; no persisted Equipe screenshot/AX independently inspected','notes_groups_saved':'Parent reports Salvo and Grupos(2); not independently archived in reviewer evidence','last_installed':'4.1 (46), Nov 5, per parent observation; no physical inspection','expiry':'90-day relative UI label; exact date unknown','submission':'one action, Enviando then completion per parent; no repeated submission alleged'},
 'findings':[], 'pending':['Authenticated APK42 download verification remains pending','Admin47 preparation/application by Plato is separate and pending; not reviewed or credited here','Mobile requirement not submitted; no acceptance performed','Google Play not published; physical tests/installations not verified'],
 'scope':'Read-only local artifacts, hashes, ZIP structure, persisted UI evidence and local git blobs. No browser/API calls, builds, push, restart, runtime edit, or retesting unchanged code. Historic PUSH cloud/groups NOT_OBSERVED and APK anonymous PENDING are superseded only for those fields by later explicit receipts; authenticated-download PENDING remains.'}
with (R/'MOBILE_REVIEW_R2.json').open('xb') as f:f.write((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'status':report['status'],'checks':len(checks),'pins':len(pins),'report':str(R/'MOBILE_REVIEW_R2.json'),'accepted':False}))
