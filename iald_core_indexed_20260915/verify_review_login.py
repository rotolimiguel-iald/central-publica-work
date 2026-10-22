from datetime import datetime
import json
from pathlib import Path
import requests

WORK = Path(__file__).resolve().parent
credential = json.loads(Path(r'C:\Users\rotol\.iald_keys\apple-beta\review-account.json').read_bytes())
session = requests.Session()
session.trust_env = False
response = session.post('http://127.0.0.1:8082/api/entrar/senha',json={
    'usuario':credential['username'],'senha':credential['password']},timeout=20)
assert response.status_code == 200,'Review login failed'
login = response.json()
assert login['status'] == 'active' and login['plano'] == 'gratuito'
session.headers['Authorization'] = 'Bearer '+login['token']
info_response = session.get('http://127.0.0.1:8082/api/motor',timeout=30)
assert info_response.status_code == 200
info = info_response.json()
assert info['modelo'] == 'gpt-5.6-luna' and info['disponivel'] and not info['pode_escolher']
assert not info['consentimento']['dado']
tool_names = info['limites']['ferramentas']
assert {'search_tgl','fetch_tgl'} <= set(tool_names)
assert not any(name.startswith('iald_atlas_') for name in tool_names)
gate = session.post('http://127.0.0.1:8082/v1/chat/completions',json={
    'messages':[{'role':'user','content':'Teste da tela de consentimento.'}],'stream':True},timeout=20)
assert 'consentimento_ia' in gate.text,'Consent gate did not block request'
result = {'at':datetime.now().astimezone().isoformat(),'login_http':response.status_code,
          'motor_http':info_response.status_code,'model_available':info['disponivel'],
          'model':info['modelo'],'plano':info['plano'],'corpus_tools_available':True,
          'private_atlas_tools_absent':True,'consent_gate_verified':True,
          'api_inference_called':False,'credentials_printed':False}
with (WORK/'review_login_verified.json').open('x',encoding='utf-8') as handle:
    json.dump(result,handle,indent=2)
print(json.dumps(result))
