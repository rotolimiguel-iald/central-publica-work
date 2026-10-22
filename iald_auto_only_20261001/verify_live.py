from pathlib import Path
from datetime import datetime
import ast,hashlib,json,sys,urllib.request
W=Path(__file__).parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0,str(R))
import iald_auto_router as router
import iald_app_providers as providers
import iald_motores as motors
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((W/'deployment.json').read_bytes())
assert all(sha(R/n)==h for n,h in d['files'].items())
assert all(sha(R/n)==h for n,h in d['scientific_unchanged'].items())
users=json.loads((R/'iald_users.json').read_bytes())
assert sha(R/'iald_users.json')==d['users_sha_before']
node=next(n for n in ast.parse((R/'iald_web_server.py').read_bytes()).body if isinstance(n,ast.FunctionDef) and n.name=='_motor_efetivo')
env=dict(app_router=router,app_providers=providers,iald_motores=motors)
exec(compile(ast.Module([node],type_ignores=[]),'deployed mode','exec'),env)
approved={u:r for u,r in users.items() if router.allowed(r,u)}
assert router.manual_allowed(users['luiz'],'luiz')
assert all(env['_motor_efetivo'](r,u)==router.AUTO and not router.manual_allowed(r,u) for u,r in approved.items() if u!='luiz')
family={u:dict(mode=env['_motor_efetivo'](users[u],u),manual=router.manual_allowed(users[u],u)) for u in ('luiz','alanacaroline','liana')}
with urllib.request.urlopen('http://127.0.0.1:8082/health',timeout=12) as response:assert response.status==200
record=dict(at=datetime.now().astimezone().isoformat(),health=200,installed_file_hashes_verified=True,remote_javascript_hash={'status':'NOT_VERIFIED','sha256':None,'reason':'Unauthenticated HTTP returned login HTML. It is not a JavaScript integrity check.'},approved_accounts=len(approved),automatic_non_operator=len(approved)-1,family=family,router_available=router.available(),users_untouched=True,scientific_files_unchanged=True,paid_calls=0,physical_devices_tested=False,scope='LOCAL_DEPLOYED_FILES_AND_ACCOUNT_POLICY_ONLY_NO_REMOTE_ASSET_INTEGRITY_CLAIM')
assert record['router_available']
(W/'live_verification.json').write_bytes(json.dumps(record,ensure_ascii=False,indent=2).encode())
print(json.dumps(record,ensure_ascii=False))
