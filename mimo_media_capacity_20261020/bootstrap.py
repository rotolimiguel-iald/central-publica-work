from pathlib import Path
import json,hashlib,subprocess,uuid
W=Path(__file__).resolve().parent;P=r'C:\Python314\python.exe'
source=W/'ORIGINAL.txt'
request={'operation':'init','objective_file':str(source),'objective_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'request_id':'bb3806ed-872e-47de-9f15-3a879ef029d5','scope':{'house':'IALD','principal':'luiz'},'actor':{'id':'codex-app-01a094df','kind':'agent'},'write_reference':str(W/'SESSION_REFERENCE.json'),'constraints':{'unit':'F9.MIMO_MEDIA_CAPACITY_20261020','preserve_science_accounts_wallet_consents':True,'no_retry_uncertain_requests':True}}
(W/'init_request.json').open('x',encoding='utf-8').write(json.dumps(request,ensure_ascii=False))
r=subprocess.run([P,'-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\session_memory.py'],input=json.dumps(request).encode(),capture_output=True)
assert r.returncode==0,r.stdout.decode()
(W/'init_receipt.json').open('xb').write(r.stdout)
old=Path(r'C:\IALD\Central de Patentes\work\mimo26_upgrade_20261020\task.py').read_text(encoding='utf-8')
(W/'task.py').open('x',encoding='utf-8').write(old.replace('F9.MIMO26_UPGRADE_20261020','F9.MIMO_MEDIA_CAPACITY_20261020'))
print(r.stdout.decode())
