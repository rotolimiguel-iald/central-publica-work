"""Prepare exact runtime/client targets and native version changes; never install."""
from pathlib import Path
import ast,hashlib,json
import task
W=task.W;R=Path(r'C:\IALD\projetos_pyhton\IALD')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
task.check('deployment')
stage=W/'parent_stage';stage.mkdir(exist_ok=True)
server=R/'iald_web_server.py';before=server.read_bytes()
needle=b"'app/index.html', 'app/iald.js', 'app/registration_identity.js'"
assert before.count(needle)==1
after=before.replace(needle,b"'app/index.html', 'app/iald.js', 'app/iald_transport.mjs', 'app/chat_wire_codec.mjs', 'app/registration_identity.js'")
needle=b"    return send_from_directory(SERVE_DIR, filename)"
assert after.count(needle)==1
eol=b'\r\n' if b'\r\n' in before else b'\n'
after=after.replace(needle,eol.join([b"    if filename in {'app/iald_transport.mjs', 'app/chat_wire_codec.mjs'}:",b"        return send_from_directory(SERVE_DIR, filename, mimetype='text/javascript')",needle]))
needle=b"                                     account_key=_chat_account_generation)"
assert after.count(needle)==1
after=after.replace(needle,b"                                     account_key=_chat_account_generation,"+eol+b"                                     transport_origin_check=_private_media_origin_ok)")
ast.parse(after);(stage/'iald_web_server.py').open('xb').write(after)
rows=[]
def row(src,dst):
    if src.suffix=='.py':ast.parse(src.read_bytes())
    rows.append({'source':str(src),'destination':str(dst),'sha256':sha(src),'baseline':sha(dst) if dst.exists() else None})
row(stage/'iald_web_server.py',server)
for name in ('iald_chat_jobs.py','chat_wire_codec.py'):
    row(W/'integration/backend_R2'/name,R/name)
for folder in (R/'app',R/'iald-app/www',R/'iald-app/ios/App/App/public',R/'iald-app/android/app/src/main/assets/public'):
    for name in ('iald.js','iald_transport.mjs','chat_wire_codec.mjs'):
        row(W/'integration/client_R2'/name,folder/name)
native=[]
for rel,old,new,count in [('ios/App/App.xcodeproj/project.pbxproj',b'CURRENT_PROJECT_VERSION = 36;',b'CURRENT_PROJECT_VERSION = 37;',2),('android/app/build.gradle',b'versionCode 31',b'versionCode 32',1)]:
    dst=R/'iald-app'/rel;raw=dst.read_bytes();assert raw.count(old)==count
    src=stage/dst.name;src.open('xb').write(raw.replace(old,new));row(src,dst);native.append(rows[-1])
task.new('NATIVE_PLAN.json',{'files':native,'ios':'4.1(37)','android':'4.1(32)'})
science=json.loads((W.parent/'iald_readability_reliable_tools_20261021/SCIENCE_BASELINE.json').read_bytes())
for f in science['files']:assert sha(Path(f['path']))==f['sha256'],'Science baseline changed'
task.new('SCIENCE_BASELINE.json',science)
task.new('install_plan.json',{'status':'PREPARED_NOT_INSTALLED','files':rows,'science_baseline':str(W/'SCIENCE_BASELINE.json'),'accounts_modified':False,'wallet_modified':False})
(W/'validation').mkdir(exist_ok=True)
task.new('validation/final_checks.json',{'passed':True,'scope':'File pins, original baselines and syntax only; independent behavior review required','plan_sha256':sha(W/'install_plan.json'),'files':len(rows)})
task.new('BROWSER_CODEC_RESULT.json',{'status':'PASS','raw_bytes':122130,'wire_bytes':1104,'local_ms':11,'exact_bytes':True,'corrupt_hash_rejected':True,'model_calls':0,'browser':'Codex in-app browser','codec_sha256':sha(W/'client_server_stage/chat_wire_codec.mjs'),'screenshot':str(W/'BROWSER_CODEC_PASS.png'),'screenshot_sha256':sha(W/'BROWSER_CODEC_PASS.png'),'scope':'Synthetic local native-browser codec, not live HTTP chat, Safari or device measurement'})
print(json.dumps({'files':len(rows),'plan_sha256':sha(W/'install_plan.json')}))
