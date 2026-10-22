from pathlib import Path
import hashlib,json,difflib,subprocess,uuid,sys
W=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if sys.argv[1]=='init':
    src=W/'validation/independent_review_source.txt'
    request={'operation':'init','objective_file':str(src),'objective_sha256':sha(src),'request_id':'0e9391e6-df22-4b9b-badb-0c361d858015','scope':{'house':'IALD','principal':'luiz'},'actor':{'id':'codex-independent-review-hajaluz','kind':'agent'},'write_reference':str(W/'validation/REVIEW_SESSION_REFERENCE.json'),'constraints':{'review_only':True,'unit':'F9.APP_HAJALUZ_AUTO_20261016'}}
    p=subprocess.run([sys.executable,'-X','utf8',r'C:\IALD\MEMORIA_IALD\session_memory.py'],input=json.dumps(request),text=True,capture_output=True)
    print(p.stdout,p.stderr);sys.exit(p.returncode)
plan=json.loads((W/'install_plan.json').read_bytes())
for item in plan['files']:
    p=Path(item['source']);b=W/'baseline'/p.name;dest=Path(item['destination'])
    print(json.dumps({'name':p.name,'stage_match':sha(p)==item['sha256'],'baseline_match':sha(b)==item['baseline'] if b.exists() else item['baseline'] is None,'runtime_match':sha(dest)==item['baseline'] if dest.exists() else item['baseline'] is None}))
    print(''.join(difflib.unified_diff(b.read_text(encoding='utf-8').splitlines(True) if b.exists() else [],p.read_text(encoding='utf-8').splitlines(True),fromfile='baseline/'+p.name,tofile='staging/'+p.name)))
for name in ('transaction.py','maintenance.py','deploy_controlled.py'):
    p=W/name;old=W.parent/'iald_app_stack_20261014'/name
    print(json.dumps({'name':name,'sha256':sha(p),'reference':str(old),'byte_equal':old.exists() and p.read_bytes()==old.read_bytes()}))
