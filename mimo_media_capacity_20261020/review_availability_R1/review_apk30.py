import ast,hashlib,json,re,sys,zipfile
from pathlib import Path
W=Path(__file__).resolve().parent.parent;H=W/'mobile_stage/apk30_publication/FINAL_R2'
sys.path.insert(0,str(W));import task
current=task.project()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),sha256=sha(p))
P=H/'APK30_ADDITIVE_PUBLICATION_PLAN_FINAL_R2.json';plan=json.loads(P.read_bytes());relay=json.loads((H/'PLANCK_4CHECKS_RELAY.json').read_bytes())
assert sha(P)==relay['plan']['sha256']
for e in [plan['source'],plan['result'],plan['archive_audit'],plan['reuse_primitive'],*plan['source_pins'],*plan['preserve_existing_apks']]:
    assert sha(e['path'])==e['sha256']
    if 'bytes' in e:assert Path(e['path']).stat().st_size==e['bytes']
dest=Path(plan['destination']);assert dest.name=='IALD-4.1-30.apk' and not dest.exists()
old=list(dest.parent.glob('*.apk'));assert len(old)==len(plan['preserve_existing_apks'])==15
assert {p.resolve() for p in old}=={Path(e['path']).resolve() for e in plan['preserve_existing_apks']}
result=json.loads(Path(plan['result']['path']).read_bytes());audit=json.loads(Path(plan['archive_audit']['path']).read_bytes())
assert result['build']['exit_code']==0 and result['protected_inputs_unchanged'] is True
assert audit['status']=='PASS' and all(v is True for v in audit['checks'].values())
signature=audit['signature_evidence']
def walk(x):
    if isinstance(x,dict):
        if 'path' in x and 'sha256' in x and Path(x['path']).is_file():
            assert sha(x['path'])==x['sha256']
            yield Path(x['path'])
        for v in x.values():yield from walk(v)
    elif isinstance(x,list):
        for v in x:yield from walk(v)
sigfiles=list(walk(signature));texts=[]
for f in sigfiles:
    if f.suffix in ('.log','.txt'):texts.append(f.read_text(encoding='utf-8'))
certs=set(re.findall(r'Signer #1 certificate SHA-256 digest:\s*([0-9a-fA-F]+)','\n'.join(texts)))
if certs:assert certs==set(plan['certificate_sha256'])
with zipfile.ZipFile(plan['source']['path']) as z:
    assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
    js=hashlib.sha256(z.read('assets/public/iald.js')).hexdigest()
server=Path(plan['endpoint_source']['pin']['path']);tree=ast.parse(server.read_bytes())
route=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='serve_download')
route.decorator_list=[]
from types import SimpleNamespace as NS
sent=[]
ns=dict(request=NS(),session={},load_users_estrito=lambda:{},iald_motores=NS(plano_de=lambda r:'free',GRATUITO='free'),RE_DOWNLOAD_GRATUITO=re.compile(plan['endpoint_source']['free_account_apk_pattern']),Response=lambda msg,status:(msg,status),os=NS(path=NS(join=lambda *a:'/mock/apk',isfile=lambda p:True)),DOWNLOADS_DIR='/mock',send_from_directory=lambda *a,**kw:sent.append(a) or 'APK_SENT')
exec(compile(ast.Module(body=[route],type_ignores=[]),'exact download route AST','exec'),ns)
assert ns['serve_download']('IALD-4.1-30.apk')[1]==403 and not sent
ns['session']={'username':'synthetic'};ns['load_users_estrito']=lambda:{'synthetic':{'plan':'free'}}
assert ns['serve_download']('IALD-4.1-30.apk')=='APK_SENT'
assert ns['serve_download']('../IALD-4.1-30.apk')[1]==403
primitive=Path(plan['reuse_primitive']['path']).read_text(encoding='utf-8')
assert "APK29_ADDITIVE_PUBLICATION_PLAN_R1.json" in primitive and 'downloads/IALD-4.1-29.apk' in primitive
assert "os.rename(staged, dest)" in primitive and "intent.open('xb')" in primitive
stale_endpoint=sha(server)!=plan['endpoint_source']['pin']['sha256'];assert stale_endpoint
report=dict(status='PASS_ARTIFACT_AND_ADDITIVE_SCOPE_EXECUTABLE_REVIEW_PENDING',technical_go=False,final_delivery='FINAL_DELIVERY_NOT_ACCEPTED',actor='codex-mimo-capacity-reviewer',reviewed_revision=current['receipt']['revision'],reference=str(W/'SESSION_REFERENCE.json'),plan=pin(P),relay=pin(H/'PLANCK_4CHECKS_RELAY.json'),source=pin(plan['source']['path']),source_bytes=Path(plan['source']['path']).stat().st_size,existing_apks_verified=15,destination_absent=True,embedded_js_sha256=js,
    four_checks=dict(artifact_result_audit_certificate_pins='PASS_DOCUMENTARY_PINNED_AUDIT_AND_SIGNATURE_EVIDENCE',single_target_additive_all_existing_apks_preserved='PASS_CURRENT_BYTES_AND_ABSENT_TARGET',authenticated_route_anonymous_zero_apk_bytes='PASS_OFFLINE_EXACT_ROUTE_AST; POST_PUBLICATION_HTTP_PENDING',fresh_owner_preflight_go_and_no_repeat_atomic_create='PENDING_ACTUAL_APK30_PUBLISHER_AND_FRESH_PREFLIGHT'),
    findings=[dict(severity='MEDIUM',id='APK30_EXECUTABLE_NOT_BOUND',evidence='Final plan explicitly states publisher adaptation required. Only pinned executable is old APK29 primitive with hard-coded29 target, old plan filename and old mission preflight import. No APK30 implementation is pinned.',minimal_fix='Producer supplies immutable APK30 publisher plus exact pin, own mission preflight/GO linkage, strict target absence, durable exclusive intent, reparse checks, fsync/hash and Windows atomic nonreplacement; retain old primitive. Review only this adaptation before execution.'),dict(severity='LOW',id='STALE_ENDPOINT_SOURCE_METADATA',actual_server=pin(server),declared=plan['endpoint_source']['pin'],minimal_fix='Correct endpoint_source pin and APK30 path in a new plan revision; current source_pins already contains actual server hash. Preserve FINAL_R2.')],
    limits=['No APK copy/publication, HTTP call, build, provider request, secret/env/key access or task acceptance by reviewer.','Anonymous login302 or loginHTML is permitted only with zero APK bytes; authenticated GET must match source SHA after actual publication. Existing APK29 HTTP evidence is historical only.','Technical publication phase may be approved independently of final delivery once executable and updated plan are reviewed; provider perception success is not fabricated or required by this bounded APK review.','iOS35 Cloud in progress is operator-reported here; no duplicate build, group availability or physical installation asserted.'])
out=W/'REVIEW_APK30_PUBLICATION_FINAL_R2.json';raw=json.dumps(report,ensure_ascii=False,indent=2).encode()
with out.open('xb') as f:f.write(raw)
assert out.read_bytes()==raw
print(json.dumps(dict(status=report['status'],technical_go=False,source_sha256=report['source']['sha256'],old_apks=15,report=str(out))))
