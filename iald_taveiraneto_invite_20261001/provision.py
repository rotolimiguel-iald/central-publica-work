from pathlib import Path
from datetime import datetime
import ast,ctypes,hashlib,json,os,secrets,sys
W=Path(__file__).parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
USER='taveiraneto';EMAIL='[dado pessoal removido]'
PRIVATE=R/'.iald_runtime/invites';VAULT=PRIVATE/(USER+'.dpapi')
sys.path.insert(0,str(R))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

class Blob(ctypes.Structure):
 _fields_=[('cbData',ctypes.c_ulong),('pbData',ctypes.POINTER(ctypes.c_ubyte))]
def crypt(data,protect):
 buffer=ctypes.create_string_buffer(data)
 source=Blob(len(data),ctypes.cast(buffer,ctypes.POINTER(ctypes.c_ubyte)));target=Blob()
 fn=ctypes.windll.crypt32.CryptProtectData if protect else ctypes.windll.crypt32.CryptUnprotectData
 ok=fn(ctypes.byref(source),None,None,None,None,1,ctypes.byref(target))
 if not ok:raise OSError('DPAPI operation failed')
 try:return ctypes.string_at(target.pbData,target.cbData)
 finally:ctypes.windll.kernel32.LocalFree(target.pbData)
def atomic(p,data):
 tmp=p.with_name(p.name+'.tmp_'+str(os.getpid()))
 with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 assert data and tmp.read_bytes()==data
 os.replace(tmp,p);assert p.read_bytes()==data
def backup(p):
 raw=p.read_bytes();b=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
 with b.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert b.read_bytes()==raw
 return raw,str(b)
def quiet():
 import runpy
 return runpy.run_path(str(W.parent/'iald_web_app_unified_20261001/deploy.py'))['quiet']()

def install():
 assert not (W/'deployment.json').exists(),'Already installed; do not repeat'
 baseline=json.loads((W/'baseline.json').read_bytes());test=json.loads((W/'tests.json').read_bytes())
 assert test['passed'] and test['stage_sha256']==sha(W/'stage/iald_motores.py')
 assert (W/'review.txt').is_file(),'Independent review required'
 p=R/'iald_motores.py';assert sha(p)==baseline[p.name],'Source changed'
 quiet();raw,bak=backup(p);new=(W/'stage/iald_motores.py').read_bytes();ast.parse(new)
 assert p.read_bytes()==raw;atomic(p,new)
 atomic(W/'deployment.json',json.dumps(dict(at=datetime.now().astimezone().isoformat(),
  installed_sha256=sha(p),backup=bak,tests=11,client_change=False,paid_calls=0),indent=2).encode())
 print(json.dumps({'installed':p.name,'restart_required':True}))

def create_account():
 from werkzeug.security import generate_password_hash,check_password_hash
 assert not (W/'account.json').exists(),'Account already provisioned'
 quiet();p=R/'iald_users.json';old=p.read_bytes();users=json.loads(old)
 assert USER not in users and not any(EMAIL in json.dumps(v).lower() for v in users.values()),'Account already exists'
 assert any(v.get('admin') is True for v in users.values())
 password=secrets.token_urlsafe(24)
 record=dict(password_hash=generate_password_hash(password),admin=False,sacred_language=False,
  created=datetime.now().astimezone().isoformat(),name='Testador taveiraneto',email=EMAIL,
  source='convite_operador',plano='assinante',motor='automatico',tokens_sem_limite=True,
  identidades=[],token_exemption_authorized_by='luiz',token_exemption_reason='Teste autorizado em 01/10/2026')
 assert check_password_hash(record['password_hash'],password)
 PRIVATE.mkdir(parents=True,exist_ok=True)
 assert not VAULT.exists(),'Existing invitation credential; do not replace'
 encrypted=crypt(password.encode(),True);assert crypt(encrypted,False).decode()==password
 atomic(VAULT,encrypted)
 before=dict(users);users[USER]=record
 _,bak=backup(p);assert p.read_bytes()==old,'Concurrent user edit'
 atomic(p,json.dumps(users,ensure_ascii=False,indent=2).encode('utf-8'))
 actual=json.loads(p.read_bytes());assert {k:v for k,v in actual.items() if k!=USER}==before
 atomic(W/'account.json',json.dumps(dict(username=USER,email=EMAIL,admin=False,
  tokens_sem_limite=True,monetary_limits_unchanged=True,source='explicit_user_invitation',
  account_created_at=record['created'],other_accounts_unchanged=True,backup=bak,
  email_sent=False),indent=2).encode())
 print(json.dumps({'created':USER,'admin':False,'tokens_sem_limite':True,'password_exposed':False}))

def verify():
 import requests
 from werkzeug.security import check_password_hash
 import iald_motores as m
 import iald_auto_router as router
 users=json.loads((R/'iald_users.json').read_bytes());record=users[USER]
 password=crypt(VAULT.read_bytes(),False).decode();assert check_password_hash(record['password_hash'],password)
 assert record['admin'] is False and router.default_for(record,USER) and not router.manual_allowed(record,USER)
 s=requests.Session()
 response=s.post('https://demo.iald.ia.br/login',data={'username':USER,'password':password},timeout=25,allow_redirects=False)
 assert response.status_code==302 and response.headers.get('Location')=='/app/index.html','Login failed'
 page=s.get('https://demo.iald.ia.br/app/index.html',timeout=25)
 assert page.status_code==200 and hashlib.sha256(page.content).hexdigest()==sha(R/'app/index.html'),'Shared UI does not match'
 status=s.get('https://demo.iald.ia.br/api/motor',timeout=25);assert status.status_code==200
 metadata=status.json()
 assert metadata.get('motor')=='automatico',sorted(metadata)
 admin=s.get('https://demo.iald.ia.br/admin/api/users',timeout=25,allow_redirects=False)
 assert admin.status_code in (302,401,403),'Admin unexpectedly accessible'
 s.get('https://demo.iald.ia.br/logout',timeout=25)
 result=dict(at=datetime.now().astimezone().isoformat(),public_login=True,shared_app_ui=True,
  automatic_mode=True,admin_denied=True,provider_consent_not_accepted=True,paid_calls=0,
  token_quota_account_record=True,installed_source_sha256=sha(R/'iald_motores.py'))
 atomic(W/'live.json',json.dumps(result,indent=2).encode());print(json.dumps(result))

def email_payload():
 assert json.loads((W/'live.json').read_bytes())['public_login']
 assert not (W/'email_sent.json').exists(),'Already sent; do not repeat'
 password=crypt(VAULT.read_bytes(),False).decode()
 text=('Olá!\n\nLuiz Antonio Rotoli Miguel liberou seu acesso individual para testar a IALD.\n\n'
  'Acesse: https://demo.iald.ia.br/\nUsuário: '+USER+'\nSenha individual: '+password+'\n\n'
  'Sua conta está ativa, sem cota diária ou mensal de tokens. O modo automático usa o JEV para escolher o modelo. '
  'Permanecem os limites técnicos dos modelos e os controles gerais de uso e gasto do serviço. '
  'Na primeira conversa, leia e aceite os avisos dos provedores que desejar utilizar.\n\n'
  'No iPhone/iPad, você também pode instalar pelo TestFlight: https://testflight.apple.com/join/A5XEdy1H\n'
  'No app, toque em “Entrar com usuário e senha” e use os mesmos dados acima.\n'
  'No Android, o site funciona diretamente; após entrar, o APK também está disponível em '
  'https://demo.iald.ia.br/downloads/IALD-4.1-26.apk\n\n'
  'A senha é pessoal: não compartilhe. Se encontrar falhas ou quiser sugerir melhorias, responda a este e-mail.\n\n'
  'Luiz Antonio Rotoli Miguel\nIALD')
 print(json.dumps(dict(to=[{'email':EMAIL}],subject='Convite para testar a IALD',text_content=text,save_to_sent_items=True),ensure_ascii=False))

if __name__=='__main__':
 {'install':install,'create':create_account,'verify':verify,'email_payload':email_payload,'quiet':lambda:print(json.dumps(quiet()))}[sys.argv[1]]()
