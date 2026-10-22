from pathlib import Path
import ast,hashlib,json
W=Path(__file__).resolve().parents[2]
R=Path(r'C:\IALD\projetos_pyhton\IALD')
OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
plan=json.loads((W/'install_plan.json').read_bytes())
expected={R/'iald_web_server.py',R/'iald_chat_jobs.py',R/'chat_wire_codec.py',R/'iald-app/ios/App/App.xcodeproj/project.pbxproj',R/'iald-app/android/app/build.gradle'}
for surface in ['app','iald-app/www','iald-app/ios/App/App/public','iald-app/android/app/src/main/assets/public']:
    expected.update(R/surface/n for n in ['iald.js','iald_transport.mjs','chat_wire_codec.mjs'])
assert len(plan['files'])==17
assert {Path(f['destination']).resolve() for f in plan['files']}=={p.resolve() for p in expected}
checks=[]
for f in plan['files']:
    src,dst=Path(f['source']).resolve(),Path(f['destination']).resolve()
    assert src.is_relative_to(W.resolve()) and dst.is_relative_to(R.resolve())
    assert sha(src)==f['sha256'] and (sha(dst) if dst.exists() else None)==f['baseline']
    if src.suffix=='.py':ast.parse(src.read_bytes())
    checks.append({'source':str(src),'destination':str(dst),'sha256':sha(src),'baseline_checked':True})

# Reconstruct only authorized source edits; equality is on bytes, including EOL.
original=(R/'iald_web_server.py').read_bytes();after=original
needle=b"'app/index.html', 'app/iald.js', 'app/registration_identity.js'"
assert after.count(needle)==1
after=after.replace(needle,b"'app/index.html', 'app/iald.js', 'app/iald_transport.mjs', 'app/chat_wire_codec.mjs', 'app/registration_identity.js'")
eol=b'\r\n' if b'\r\n' in original else b'\n'
needle=b'    return send_from_directory(SERVE_DIR, filename)';assert after.count(needle)==1
after=after.replace(needle,eol.join([b"    if filename in {'app/iald_transport.mjs', 'app/chat_wire_codec.mjs'}:",b"        return send_from_directory(SERVE_DIR, filename, mimetype='text/javascript')",needle]))
needle=b'                                     account_key=_chat_account_generation)';assert after.count(needle)==1
after=after.replace(needle,b'                                     account_key=_chat_account_generation,'+eol+b'                                     transport_origin_check=_private_media_origin_ok)')
assert (W/'parent_stage/iald_web_server.py').read_bytes()==after
native=json.loads((W/'NATIVE_PLAN.json').read_bytes())
assert native['ios']=='4.1(37)' and native['android']=='4.1(32)' and len(native['files'])==2
for f in native['files']:
    assert f in plan['files'];src,dst=Path(f['source']),Path(f['destination'])
    if dst.suffix=='.pbxproj':a,b,count=b'CURRENT_PROJECT_VERSION = 36;',b'CURRENT_PROJECT_VERSION = 37;',2
    else:a,b,count=b'versionCode 31',b'versionCode 32',1
    raw=dst.read_bytes();assert raw.count(a)==count and src.read_bytes()==raw.replace(a,b)

science=json.loads((W/'SCIENCE_BASELINE.json').read_bytes())['files'];assert len(science)==5
for f in science:assert sha(Path(f['path']))==f['sha256']
mobile_science=json.loads((W/'mobile_prepare/SCIENCE_PINS.json').read_bytes())['files']
assert {str(Path(f['path']).resolve()):f['sha256'] for f in science}=={str(Path(f['path']).resolve()):f['sha256'] for f in mobile_science}
prior=json.loads((W/'review/DEPLOY_PRIMITIVES_REVIEW.json').read_bytes())
for f in prior['files']:assert sha(Path(f['path']))==f['sha256']
mobile=json.loads((W/'review/MOBILE_REVIEW_PREPARATION_R2.json').read_bytes())
for field,name in [('runner_sha256','mobile_release.py'),('publisher_sha256','publish_apk32.py'),('init_sha256','android32.init.gradle'),('logger_sha256','mobile_prepare/build_log.py'),('tool_plan_sha256','mobile_prepare/TOOL_PLAN.json'),('science_pins_sha256','mobile_prepare/SCIENCE_PINS.json')]:assert sha(W/name)==mobile[field]
tools=json.loads((W/'mobile_prepare/TOOL_PLAN.json').read_bytes())
for f in tools['tool_pins']+[tools['baseline_apk']]:assert sha(Path(f['path']))==f['sha256']
assert json.loads((W/'validation/final_checks.json').read_bytes())['plan_sha256']==sha(W/'install_plan.json')
rpc=json.loads((OUT/'joint/RPC_RECEIPT.json').read_bytes())
assert rpc['synthetic_producer_calls']==1 and any(x['envelope'] and 'transport=' in x['path'] for x in rpc['requests'])
for name in ['iald.js','iald_transport.mjs','chat_wire_codec.mjs']:
    assert (OUT/'joint/fixtures/client_control'/name).read_bytes()==(W/'integration/client_R2'/name).read_bytes()
report={'status':'PASS','plan_sha256':sha(W/'install_plan.json'),'files':checks,'science_pins':science,'server_exact_allowed_delta':True,'native_exact_version_delta':True,'mobile_scripts_unchanged_since_static_review':True,'tools_and_previous_apk_pins_current':True,'runtime_baselines_current':True,'joint_harness_client_R2_bytes_confirmed':True,'joint_requests':rpc['requests'],'execution':'Read-only hashes/AST; no runtime import, build, deployment or network.'}
(OUT/'PLAN_CHECK.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':'PASS','plan_sha256':report['plan_sha256'],'files':len(checks),'science':len(science),'joint_requests':rpc['requests']}))
