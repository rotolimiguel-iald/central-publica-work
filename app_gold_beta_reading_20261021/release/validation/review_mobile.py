from pathlib import Path
import json,hashlib,re,zipfile,datetime,ast
w=Path('work/app_gold_beta_reading_20261021/release').resolve();a=w/'mobile_stage/AUDIT.json';build=w/'mobile_stage/build34';v=w/'validation';h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();load=lambda p:json.loads(Path(p).read_bytes());pin=lambda p:{'path':str(Path(p).resolve()),'sha256':h(p)}
audit=load(a);review=load(v/'review_final.json');checks=[];evidence=[pin(a),pin(w/'deployment.json'),pin(w/'INSTALLED_VERIFICATION.json'),pin(v/'review_final.json')]
def check(n,c,**d):
 if not c:raise AssertionError(n)
 checks.append(dict(name=n,passed=True,**d))
check('reviewed_publisher_and_mobile_pipeline_unchanged',h(w/'publish_apk34.py')==review['tool_pins']['publish_apk34.py'] and h(w/'mobile_release.py')==review['tool_pins']['mobile_release.py'])
check('audit_pass_android34',audit['status']=='PASS' and audit['versionCode']==34)
apk=Path(audit['apk']).resolve();aab=Path(audit['aab']).resolve();check('artifacts_belong_to_this_isolated_build',apk.is_relative_to(build) and aab.is_relative_to(build))
check('APK_final_bytes',h(apk)==audit['apk_sha256'],bytes=apk.stat().st_size);check('AAB_final_bytes',h(aab)==audit['aab_sha256'],bytes=aab.stat().st_size)
plan=load(w/'install_plan.json');deploy=load(w/'deployment.json');installed=load(w/'INSTALLED_VERIFICATION.json');check('static_deployment_matches_reviewed_plan_no_restart',deploy['plan_sha256']==review['plan_sha256']==h(w/'install_plan.json') and deploy['status']=='INSTALLED_STATIC_NO_RESTART' and deploy['restart'] is False and installed['status']=='PASS_WITH_SCOPE' and installed['files']==10)
for f in plan['files']:check('installed_receipt_covers_'+Path(f['destination']).name,deploy['files'][str(Path(f['destination']).resolve())]==f['sha256'])
expected={n:next(f['sha256'] for f in plan['files'] if Path(f['destination']).name==n) for n in ['iald.js','iald.css']};check('audit_resources_match_accepted_final_UI',audit['resources']==expected)
for archive,prefix in [(apk,'assets/public/'),(aab,'base/assets/public/')]:
 with zipfile.ZipFile(archive) as z:
  check('archive_resource_metadata_'+archive.suffix,len(z.namelist())==len(set(z.namelist())))
  for n,digest in expected.items():check('embedded_resource_'+archive.suffix+'_'+n,hashlib.sha256(z.read(prefix+n)).hexdigest()==digest)
logs={}
for label in ['gradle','apk_signature','baseline_signature','aab_signature','aab_certificate','badging']:
 receipt=build/(label+'.receipt.json');started=build/(label+'.started.json');rec=load(receipt);log=Path(rec['log']['path']);check('existing_receipt_and_log_'+label,rec['exit_code']==0 and rec['filtered_lines']==0 and log.resolve().is_relative_to(build) and h(log)==rec['log']['sha256']);evidence.extend([pin(receipt),pin(started),pin(log)]);logs[label]=log.read_text(encoding='utf-8')
check('build_exit0_and_isolated_version_markers',audit['build']['exit_code']==0 and audit['build']['log']['sha256']==h(build/'gradle.utf8.log') and 'IALD_MOBILE_OUTPUTS_ISOLATED' in logs['gradle'] and 'IALD_MOBILE_VERSION 4.1(34)' in logs['gradle'])
check('badging_identity_and_version',"package: name='br.ia.IALD' versionCode='34' versionName='4.1'" in logs['badging'])
check('signature_commands_bound_to_reviewed_artifacts',load(build/'apk_signature.started.json')['command'][-1]==str(apk) and load(build/'aab_signature.started.json')['command'][-1]==str(aab))
cert=lambda t:re.findall(r'certificate SHA-256 digest:\s*([0-9a-fA-F]+)',t)
apkcert=cert(logs['apk_signature']);priorcert=cert(logs['baseline_signature']);aabcert=re.findall(r'SHA256:\s*([0-9A-Fa-f:]+)',logs['aab_certificate'])
check('APK_existing_signature_log_verifies_v2','Verifies' in logs['apk_signature'] and 'Verified using v2 scheme (APK Signature Scheme v2): true' in logs['apk_signature'] and 'Number of signers: 1' in logs['apk_signature'])
check('same_cert_APK_baseline_AAB',len(apkcert)==1 and apkcert==priorcert and len(aabcert)==1 and aabcert[0].replace(':','').lower()==apkcert[0].lower() and audit['signer_matches_previous'] is True)
check('AAB_signed_entries_verified_not_unsigned','jar verified.' in logs['aab_signature'].lower() and 'unsigned entries' not in logs['aab_signature'].lower() and 'jar is unsigned' not in logs['aab_signature'].lower() and bool(re.search(r'^\s*s[mki? ]*\s+\d+\s+',logs['aab_signature'],re.M)))
# Exact reviewed destination, extracted from publisher AST rather than guessed.
publisher=w/'publish_apk34.py';tree=ast.parse(publisher.read_bytes());destnode=next(x.value for x in ast.walk(tree) if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='dest' for t in x.targets));dest=Path(ast.literal_eval(destnode.args[0])).resolve();expected_dest=Path('C:/IALD/projetos_pyhton/IALD/downloads/IALD-4.1-34.apk').resolve()
check('publisher_destination_exact_and_absent',dest==expected_dest and not dest.exists() and not (w/'APK_PUBLICATION.json').exists() and not (w/'APK_PUBLICATION_INTENT.json').exists())
check('publisher_no_repeat_and_additive_rules_present',all(t in publisher.read_text() for t in ["temp.open('xb')","assert not dest.exists()","older_apks_preserved","before={p.name:sha(p)","audit_sha256","publisher_sha256"]))
result={'status':'PASS','reviewer':'codex-gold-reviewer','reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'audit_sha256':h(a),'publisher_sha256':h(publisher),'plan_sha256':h(w/'install_plan.json'),'apk':pin(apk),'aab':pin(aab),'resources':expected,'signer_certificate_sha256':apkcert[0].lower(),'publication':{'destination':str(dest),'url':'https://demo.iald.ia.br/downloads/IALD-4.1-34.apk','status':'APPROVED_ADDITIVE_COPY_NOT_EXECUTED_BY_REVIEWER','authenticated_download':'PENDING_LOGIN_AND_VERIFICATION','anonymous_access':'NOT_TESTED_THIS_REVIEW'},'checks':checks,'evidence':evidence,'warnings_preserved':['AAB jarsigner reports self-signed signer/PKIX trust-chain warning, no timestamp (certificate expiry2054-01-29), and POSIX/symlink metadata not protected by signature. Signed archive validation succeeded; certificate matches existing APK. This does not assert CA trust or Google Play acceptance.'],'limits':['Existing build/signature receipts inspected and pinned; no rebuild, signature tool rerun, full archive test rerun, model or network calls.','Only selected embedded JS/CSS bytes re-read for correspondence with final accepted UI.','No publication, authenticated download, Google Play publication, iOS39 availability or physical installation claimed.','Eight memory surfaces not reviewed/applied: final dated addendum is not ready.'],'findings':[]}
p=v/'mobile_review.json';assert not p.exists();raw=json.dumps(result,ensure_ascii=False,indent=2).encode();tmp=p.with_suffix('.json.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p);print(json.dumps({'status':'PASS','checks':len(checks),'path':str(p),'sha256':h(p),'apk_bytes':apk.stat().st_size,'aab_bytes':aab.stat().st_size,'publication_executed':False}))
