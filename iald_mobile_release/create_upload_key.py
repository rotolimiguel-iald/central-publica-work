from pathlib import Path
import os
import subprocess
import secrets
import json

root=Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
keydir=Path.home()/'.iald_keys'
keydir.mkdir(exist_ok=True)
who=subprocess.check_output(['whoami'],text=True).strip()
subprocess.run(['icacls',str(keydir),'/inheritance:r','/grant:r',who+':(OI)(CI)F','*S-1-5-18:(OI)(CI)F'],check=True,capture_output=True)
store=keydir/'iald-upload.jks'
credentials=keydir/'iald-upload.properties'
if store.exists() or credentials.exists():
    assert store.exists() and credentials.exists(), 'Partial key setup: manual inspection required, nothing overwritten.'
else:
    password=secrets.token_urlsafe(36)
    env=os.environ.copy()
    env['IALD_KEYTOOL_PASSWORD']=password
    tool=Path(r'C:\Program Files\Android\Android Studio1\jbr\bin\keytool.exe')
    result=subprocess.run([str(tool),'-genkeypair','-noprompt','-keystore',str(store),'-storetype','JKS',
        '-alias','iald-upload','-keyalg','RSA','-keysize','4096','-validity','10000',
        '-dname','CN=IALD LTDA, O=IALD LTDA, C=BR',
        '-storepass:env','IALD_KEYTOOL_PASSWORD','-keypass:env','IALD_KEYTOOL_PASSWORD'],env=env,capture_output=True)
    assert result.returncode==0, 'keytool failed; key files retained for inspection'
    content=f'STORE_FILE={store.as_posix()}\nSTORE_PASSWORD={password}\nKEY_ALIAS=iald-upload\nKEY_PASSWORD={password}\n'
    tmp=credentials.with_suffix('.tmp')
    tmp.write_bytes(content.encode())
    assert tmp.stat().st_size>100
    tmp.replace(credentials)
    (keydir/'iald-upload.jks.backup').write_bytes(store.read_bytes())
    assert (keydir/'iald-upload.jks.backup').read_bytes()==store.read_bytes()
    subprocess.run([str(tool),'-exportcert','-rfc','-alias','iald-upload','-keystore',str(store),
        '-storepass:env','IALD_KEYTOOL_PASSWORD','-file',str(keydir/'iald-upload-certificate.pem')],env=env,check=True,capture_output=True)
target=root/'android/keystore.properties'
assert not target.exists(), 'Existing signing configuration retained; inspect before changing.'
target.write_bytes(credentials.read_bytes())
subprocess.run(['icacls',str(target),'/inheritance:r','/grant:r',who+':F','*S-1-5-18:F'],check=True,capture_output=True)
print('Upload key created with local backup; credentials protected; no secrets printed.')
