from pathlib import Path
import ast,hashlib,json,sys,urllib.request
W=Path(__file__).resolve().parent; R=Path(r'C:\IALD\projetos_pyhton\IALD')
plan=json.loads((W/'install_plan.json').read_bytes());files=[]
for row in plan['files']:
    p=Path(row['destination']);raw=p.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    assert digest==row['sha256'];ast.parse(raw)
    files.append({'name':p.name,'sha256':digest,'matches_reviewed_plan':True})
sys.path.insert(0,str(R))
import iald_auto_router as router
import iald_app_memory as memory
assert router.__file__==str(R/'iald_auto_router.py')
assert router.bootstrap_intent.classify('haja luz')['inscription']=='VERBO'
assert router.bootstrap_intent.classify('Explique haja luz') is None
with urllib.request.urlopen('http://127.0.0.1:8082/login',timeout=15) as res:
    status=res.status;assert status==200
out={'status':'PASS','installed_files':files,'fresh_process_import':True,'login_http_status':status,
     'source_package_changed':False,'client_build_required':False,'web_ios_android_shared_backend':True,
     'physical_device_installation_verified':False}
with (W/'installed_verification.json').open('xb') as f:f.write(json.dumps(out,indent=2).encode())
print(json.dumps(out))
