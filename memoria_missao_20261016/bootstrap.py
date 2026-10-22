"""Register the operator's memory priority using the existing ACOM adapter."""
from pathlib import Path
import hashlib, json, subprocess, uuid
P = Path(__file__).resolve().parent
source = P / 'OPERADOR_VERBATIM.txt'
request = P / 'INIT_REQUEST.json'
if not request.exists():
    payload = {'operation':'init','objective_file':str(source),
        'objective_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'request_id':str(uuid.uuid4()),'scope':{'house':'IALD','principal':'luiz-antonio-rotoli-miguel'},
        'actor':{'id':'codex-gerente-tgl','kind':'agent'},
        'write_reference':str(P/'ACOM_REFERENCE.json'),
        'constraints':{'unit':'F9.MEMORIA_MISSAO_20261016','science_waits_for_memory':True,
                       'no_scientific_production_or_gate_changes':True}}
    with request.open('x',encoding='utf-8') as f: json.dump(payload,f,ensure_ascii=False,indent=2)
payload=json.loads(request.read_bytes())
receipt=P/'INIT_RECEIPT.json'
if receipt.exists(): raise SystemExit('Already initialized; project the existing reference.')
r=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\session_memory.py'],input=json.dumps(payload,ensure_ascii=False),text=True,encoding='utf-8',capture_output=True)
with receipt.open('x',encoding='utf-8') as f: f.write(r.stdout)
if r.returncode: raise SystemExit(r.stdout+r.stderr)
j=json.loads(r.stdout)
print(json.dumps({'ok':j['ok'],'reference':str(P/'ACOM_REFERENCE.json'),'receipt':j['result']['snapshot']['receipt']},ensure_ascii=False))
