from pathlib import Path
from datetime import datetime
import ast,hashlib,json,sys,urllib.request,urllib.error
W=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0,str(R))
import iald_auto_router as router
import iald_app_providers as providers
import iald_motores as motors
deployment=json.loads((W/'deployment.json').read_bytes())
for name,digest in deployment['files'].items():
    assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest
users=json.loads((R/'iald_users.json').read_bytes())
node=next(n for n in ast.parse((R/'iald_web_server.py').read_bytes()).body
          if isinstance(n,ast.FunctionDef) and n.name=='_motor_efetivo')
env=dict(app_router=router,app_providers=providers,iald_motores=motors)
exec(compile(ast.Module([node],type_ignores=[]),'deployed effective mode','exec'),env)
family={u:dict(mode=env['_motor_efetivo'](users[u],u),approved=router.allowed(users[u],u))
        for u in ('luiz','alanacaroline','liana')}
assert all(r['mode']==router.AUTO and r['approved'] for r in family.values())
status={}
for url in ('http://127.0.0.1:8082/health',):
    with urllib.request.urlopen(url,timeout=12) as response:status[url]=response.status
assert set(status.values())=={200}
record=dict(checked_at=datetime.now().astimezone().isoformat(),family=family,
    approved_accounts=sum(router.allowed(r,u) for u,r in users.items()),
    automatic_defaults=sum(router.default_for(r,u) for u,r in users.items()),
    router_available=router.available(),http=status,
    public_browser='Application URL redirected to the normal IALD login screen, verified via CUA',
    public_automated_probe='Cloudflare HTTP403 code1010; no protection changed',
    users_untouched=hashlib.sha256((R/'iald_users.json').read_bytes()).hexdigest()==deployment['users_sha_before'],
    paid_calls=0,physical_devices_tested=False)
assert record['router_available']
(W/'live_verification.json').write_bytes(json.dumps(record,ensure_ascii=False,indent=2).encode())
print(json.dumps(record,ensure_ascii=False))
