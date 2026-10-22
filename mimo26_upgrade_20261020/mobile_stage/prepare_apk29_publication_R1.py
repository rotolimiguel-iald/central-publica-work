"""Prepare one additive authenticated APK download, never publish implicitly."""
from pathlib import Path
import ast, hashlib, json, re, types, urllib.parse

S=Path(__file__).resolve().parent
W=S.parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
P=S/'apk29_publication'
P.mkdir(exist_ok=True)
if any(P.iterdir()):raise RuntimeError('Existing publication preparation; use another revision')
def pin(path):return dict(path=str(path),sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest())
def new(path,value):
    raw=value if isinstance(value,bytes) else json.dumps(value,ensure_ascii=False,indent=2).encode()
    with path.open('xb') as f:f.write(raw)
    assert path.read_bytes()==raw
delivery=json.loads((S/'android29_R2/DELIVERY_EXECUTED_R1.json').read_bytes())
source=delivery['apk'];assert pin(source['path'])==source
audit=delivery['archive_audit'];assert pin(audit['path'])==audit
review=json.loads(Path(audit['path']).read_bytes());assert review['status']=='PASS' and all(review['checks'].values())
server=R/'iald_web_server.py';text=server.read_text(encoding='utf-8-sig');tree=ast.parse(text)
assignments={target.id:n.value for n in tree.body if isinstance(n,ast.Assign) for target in n.targets if isinstance(target,ast.Name)}
public=ast.literal_eval(assignments['PUBLIC_ROUTES']);assert 'serve_download' not in public
regex=ast.literal_eval(assignments['RE_DOWNLOAD_GRATUITO'].args[0])
filename='IALD-4.1-29.apk';assert re.fullmatch(regex,filename)
route=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='serve_download')
assert any(isinstance(d,ast.Call) and d.args and isinstance(d.args[0],ast.Constant) and d.args[0].value=='/downloads/<filename>' for d in route.decorator_list)
routecopy=ast.FunctionDef(name=route.name,args=route.args,body=route.body,decorator_list=[],returns=route.returns,type_comment=route.type_comment,type_params=route.type_params)
ast.fix_missing_locations(routecopy)
class Response:
    def __init__(self,text,status):self.status=status
registry={'fixture-free':{'plan':'free'},'fixture-paid':{'plan':'paid'}}
namespace=dict(Response=Response,load_users_estrito=lambda:registry,session={'username':'fixture-free'},
    iald_motores=types.SimpleNamespace(GRATUITO='free',plano_de=lambda row:row['plan']),
    RE_DOWNLOAD_GRATUITO=re.compile(regex),DOWNLOADS_DIR='SYNTHETIC_DOWNLOADS',
    os=types.SimpleNamespace(path=types.SimpleNamespace(join=lambda *p:'/'.join(p),isfile=lambda p:True)),
    send_from_directory=lambda folder,name,as_attachment:dict(status=200,filename=name,attachment=as_attachment))
exec(compile(ast.Module(body=[routecopy],type_ignores=[]),str(server),'exec'),namespace)
assert namespace['serve_download'](filename)['status']==200
assert namespace['serve_download']('../escape').status==403
assert namespace['serve_download']('unapproved.txt').status==403
namespace['session']={'username':'fixture-paid'};assert namespace['serve_download'](filename)['status']==200
old=Path(r'C:\IALD\Central de Patentes\work\iald_monthly_wallet_20261007\android_release.json')
olddata=json.loads(old.read_bytes())
def urls(value):
    if isinstance(value,str) and value.startswith('https://') and '/downloads/' in value and value.endswith('.apk'):yield value
    elif isinstance(value,dict):
        for child in value.values():yield from urls(child)
    elif isinstance(value,list):
        for child in value:yield from urls(child)
prior=next(urls(olddata));parts=urllib.parse.urlsplit(prior)
url=urllib.parse.urlunsplit((parts.scheme,parts.netloc,parts.path.rsplit('/',1)[0]+'/'+urllib.parse.quote(filename), '', ''))
dest=R/'downloads'/filename
if dest.exists() and pin(dest)['sha256']!=source['sha256']:raise RuntimeError('Conflicting APK29 exists; no overwrite permitted')
preserve=[pin(p) for p in sorted((R/'downloads').glob('*.apk')) if p!=dest]
oldscript=Path(r'C:\IALD\Central de Patentes\work\memoria_organismo_20261016\mobile_build\publish_apk28_candidate.py')
script=oldscript.read_text(encoding='utf-8-sig')
script=script.replace("sys.path.insert(0, str(HERE.parent))\nfrom mission_io import pin, save\nfrom run_android28 import fresh_preflight, no_reparse", "sys.path.insert(0, str(HERE.parent / 'android29_R2'))\nfrom run_android29_R2 import pin, save, fresh_preflight, no_reparse")
script=script.replace('APK28','APK29').replace('apk28','apk29').replace('IALD-4.1-28.apk','IALD-4.1-29.apk').replace('root D','deploy')
script=script.replace("plan['preserve_apk27']", "plan['preserve_apk27']")
script=script.replace("for item in (plan['review'], plan['source'], plan['preserve_apk27'], plan['candidate']):", "for item in [plan['review'], plan['source'], plan['candidate'], plan['endpoint_source']['pin'], *plan['preserve_existing_apks']]:")
script=script.replace("if review['status'] != 'PASS_ARCHIVES_WITH_SCOPE'", "if review['status'] != 'PASS'")
script=script.replace("    if not args.publish:","    for item in plan['preserve_existing_apks']:\n        if pin(item['path']) != item: raise RuntimeError('Existing APK changed')\n    if not args.publish:",1)
script=script.replace("    if pin(dest)['sha256'] != plan['source']['sha256'] or pin(plan['preserve_apk27']['path']) != plan['preserve_apk27']:","    if pin(dest)['sha256'] != plan['source']['sha256'] or any(pin(item['path']) != item for item in plan['preserve_existing_apks']):")
# Durable single-publication intent fences crashes without replay.
script=script.replace("    save(receipt_dir / 'INTENT.json',", "    intent = HERE / 'PUBLICATION_INTENT_R1.json'\n    with intent.open('xb') as out:\n        out.write(json.dumps({'plan':pin(plan_path),'receipt_directory':str(receipt_dir),'no_repeat':True}).encode()); out.flush(); os.fsync(out.fileno())\n    save(receipt_dir / 'INTENT.json',",1)
ast.parse(script);candidate=P/'publish_apk29_candidate.py';new(candidate,script.encode())
plan=dict(status='PREPARED_ADDITIVE_DOWNLOAD_NOT_PUBLISHED',reference=pin(W/'SESSION_REFERENCE.json'),candidate=pin(candidate),
    source=source,review=audit,destination=str(dest),destination_exists_at_plan=dest.exists(),
    files=[dict(source=source['path'],destination=str(dest),sha256=source['sha256'],baseline=pin(dest)['sha256'] if dest.exists() else None)],
    preserve_apk27=next(x for x in preserve if Path(x['path']).name=='IALD-4.1-27.apk'),preserve_existing_apks=preserve,
    url_provenance=pin(old),authenticated_url=url,
    endpoint_source=dict(pin=pin(server),path='/downloads/'+filename,route_function='serve_download',
        route_lines=[route.lineno,route.end_lineno],public_route=False,free_account_apk_pattern=regex,
        requires_client_route_change=False,live_authenticated_http_verified=False),
    read_allowlist=[source,audit,pin(candidate),pin(server),pin(W/'SESSION_REFERENCE.json'),*preserve],
    write_allowlist=[str(dest)],backup=dict(policy='Create absent APK29 only; no existing bytes overwritten. APK14..27 hash-preserved. Identical target gives no-write; different target refuses.',target_baseline='ABSENT' if not dest.exists() else 'IDENTICAL',backup_required=False),
    atomicity='Stage on same C: volume inside W; fsync+SHA, os.rename to absent fixed filename; concurrent differing target refuses.',
    preconditions=['Main review prepared plan; current deploy preflight from own exact reference before --publish.','Source/archive audit/server guard pins unchanged; no route, account, client, restart, rebuild or push.'],
    after_copy=['Rehash APK29 and every previous APK.','Verify unauthenticated HTTP retains login/refusal; authenticated existing account GET must match APK SHA before calling live download verified.'],
    executed=dict(publication=False,http=False,build=False,push=False),command=['C:\\Python314\\python.exe','-B','-X','utf8',str(candidate),'--publish','--preflight','<fresh deploy check receipt>'])
new(P/'APK29_ADDITIVE_PUBLICATION_PLAN_R1.json',plan)
new(P/'STATIC_ROUTE_CHECKS_R1.json',dict(status='PASS',synthetic_tests=4,route_requires_login=True,free_and_paid_authenticated_accounts_allow_APK=True,path_traversal_refused=True,free_arbitrary_non_APK_refused=True,no_real_accounts_read=True,source=pin(server),live_http=False))
print(json.dumps(dict(plan=str(P/'APK29_ADDITIVE_PUBLICATION_PLAN_R1.json'),url=url,route_change_required=False,destination_exists=dest.exists(),preserved_apks=len(preserve),published=False)))
