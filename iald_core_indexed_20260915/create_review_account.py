"""Create only the explicitly approved Apple review account and private credential."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0,str(ROOT))
from werkzeug.security import generate_password_hash, check_password_hash
from iald_identidade import PedidosAcesso


def create(path,data):
    with path.open('xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    assert path.read_bytes() == data


if __name__ == '__main__':
    assert json.loads((WORK/'suite_gate.json').read_bytes())['passed']
    assert json.loads((WORK/'runtime_live.json').read_bytes())['public_health'] == 200
    target = ROOT/'iald_users.json'
    original = target.read_bytes()
    users = json.loads(original)
    name = 'iald_review_beta'
    assert name not in users
    assert name not in PedidosAcesso(str(ROOT/'iald_pedidos_acesso.json')).nomes_indisponiveis()
    folder = Path(r'C:\Users\rotol\.iald_keys\apple-beta')
    folder.mkdir(exist_ok=False)
    principal = os.environ['USERDOMAIN']+'\\'+os.environ['USERNAME']
    acl = subprocess.run(['icacls',str(folder),'/inheritance:r','/grant:r',principal+':(OI)(CI)F',
                           '*S-1-5-18:(OI)(CI)F'],capture_output=True,check=True)
    password = secrets.token_urlsafe(24)
    entry = {'password_hash':generate_password_hash(password),'admin':False,'sacred_language':False,
             'created':datetime.now().astimezone().isoformat(),'name':'Apple Beta Review',
             'source':'operator_approved_apple_beta_review','plano':'gratuito','motor':'openai',
             'acesso_nativa':False,'cota_chave':'apple-review-'+secrets.token_hex(16),'identidades':[]}
    assert check_password_hash(entry['password_hash'],password)
    credential = {'username':name,'password':password,'purpose':'Apple TestFlight beta review only',
                  'destination':'App Store Connect beta app review','created':entry['created']}
    credential_path = folder/'review-account.json'
    create(credential_path,json.dumps(credential,ensure_ascii=False,indent=2).encode())
    users[name] = entry
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    backup = target.with_name(target.name+'.bak_'+stamp)
    create(backup,original)
    data = (json.dumps(users,ensure_ascii=False,indent=2)+'\n').encode()
    temp = target.with_name(target.name+'.tmp_'+stamp)
    create(temp,data)
    assert target.read_bytes() == original,'Concurrent user account modification'
    temp.replace(target)
    restored = json.loads(target.read_bytes())
    assert restored.pop(name) == entry and restored == json.loads(original)
    receipt = {'at':entry['created'],'username':name,'admin':False,'native_access':False,
               'private_memory_access':False,'consent_record_created':False,
               'credentials_file':str(credential_path),'backup':str(backup),
               'users_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
    create(WORK/'review_account_created.json',json.dumps(receipt,ensure_ascii=False,indent=2).encode())
    print(json.dumps({key:value for key,value in receipt.items() if key not in ('users_sha256',)}))
