"""Read-only prerequisite audit; never output environment values or credentials."""
from datetime import datetime
import hashlib
import importlib.metadata as md
import json
from pathlib import Path
import re
import requests

APP=Path(r'C:\IALD\projetos_pyhton\IALD')
WORK=Path(__file__).resolve().parent
expected={'iald_web_server.py':'f1056597c8ea89d0','iald_motores.py':'87fae82393f8adba',
    'iald_motor_claude.py':'fb70f041c55ceb7a','iald_orcamento.py':'0cd5513886827e69',
    'iald_sync_central.py':'6f55e7c0cd68acc0','app/iald.js':'77cd3ecc25a2ed96',
    'iald-app/www/iald.js':'77cd3ecc25a2ed96','app/index.html':'76a9eb82bf3af04e',
    'iald-app/www/index.html':'76a9eb82bf3af04e'}
files={name:{'sha256':hashlib.sha256((APP/name).read_bytes()).hexdigest(),
             'matches_order':hashlib.sha256((APP/name).read_bytes()).hexdigest().startswith(pin)}
       for name,pin in expected.items()}
raw=(APP/'.env').read_text(encoding='utf-8-sig')
presence={}
for name in ('IALD_CENTRAL_SYNC_SEGREDO','IALD_CENTRAL_SYNC_URL','IALD_CLAUDE_API_KEY'):
    match=re.search(r'(?m)^'+name+r'\s*=\s*(.*?)\r?$',raw)
    presence[name]=bool(match and match.group(1).strip().strip('"\''))
raw=None
packages={}
for name in ('anthropic','httpx','pydantic','anyio','requests','jiter','distro','typing_extensions','sniffio'):
    try:packages[name]=md.version(name)
    except md.PackageNotFoundError:packages[name]=None
http={}
session=requests.Session();session.trust_env=False
for url,method in [('http://127.0.0.1:8082/health','GET'),('https://demo.iald.ia.br/health','GET'),
                   ('https://central.iald.ia.br/api/iald-sync/puxar','POST')]:
    try:
        response=session.request(method,url,timeout=20)
        http[url]={'status':response.status_code}
    except requests.RequestException as error:http[url]={'error_type':type(error).__name__}
report={'at':datetime.now().astimezone().isoformat(),'files':files,'configured_presence_only':presence,
        'packages':packages,'http':http,'source_files_modified':False}
path=WORK/('initial_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.json')
with path.open('xb') as out:out.write(json.dumps(report,indent=2).encode())
assert json.loads(path.read_bytes())==report
print(json.dumps(report))
