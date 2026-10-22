from pathlib import Path
import sys,json,hashlib,ast
w=Path(__file__).resolve().parent
sys.path.insert(0,str(w))
from transaction import quiet,backup,atomic,write_evidence
plan_path=w/'memory_ceiling_fix_plan.json';plan=json.loads(plan_path.read_bytes())
review=json.loads((w/'validation/memory_ceiling_review.json').read_bytes())
assert review['status']=='PASS' and review['plan_sha256']==hashlib.sha256(plan_path.read_bytes()).hexdigest()
receipt=w/'memory_fix/deployment.json'
assert not receipt.exists()
assert len(plan['files'])==1
item=plan['files'][0];src=Path(item['source']);dst=Path(item['destination'])
assert src==w/'stage/iald_memoria_canonica.py' and dst==Path(r'C:\IALD\projetos_pyhton\IALD\iald_memoria_canonica.py')
old=dst.read_bytes();new=src.read_bytes();ast.parse(new)
assert hashlib.sha256(old).hexdigest()==item['baseline'] and hashlib.sha256(new).hexdigest()==item['sha256']
assert old.replace(b"metadata['context_tokens'] > 340000",b"metadata['context_tokens'] > 400000")==new
quiet();bk=backup(dst)
assert dst.read_bytes()==old
atomic(dst,new)
write_evidence(receipt,{'status':'INSTALLED_RESTART_REQUIRED','plan_sha256':review['plan_sha256'],'file':str(dst),'backup':bk,'sha256':item['sha256']})
print(json.dumps({'status':'INSTALLED_RESTART_REQUIRED','files':1}))
