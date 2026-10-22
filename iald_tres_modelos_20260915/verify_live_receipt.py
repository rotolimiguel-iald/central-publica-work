from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
expected = json.loads((WORK/'quota_values.json').read_text())
selected = {}
for line in (ROOT/'.env').read_text(encoding='utf-8-sig').splitlines():
    key, sep, value = line.partition('=')
    if sep and key.strip() in expected:
        selected[key.strip()] = value.strip().strip('"').strip("'")
assert selected == expected, 'Quota mismatch'
users = json.loads((ROOT/'iald_users.json').read_text(encoding='utf-8'))
owner = users.get('luiz', users.get('users', {}).get('luiz', {}))
assert owner.get('admin') and owner.get('somente_limite_global') is True
assert owner.get('motor') == 'openai', 'Restore model after test'
day = datetime.now(timezone.utc).date().isoformat()
dbpath = ROOT/'iald_uso_openai.json.reservas.sqlite3'
db = sqlite3.connect(dbpath.as_uri()+'?mode=ro', uri=True)
try:
    account_model = [dict(zip(('account','model','calls','usd_including_reservations'),row)) for row in db.execute(
        'SELECT user,model,COUNT(*),SUM(COALESCE(actual,cap)) FROM calls WHERE day=? GROUP BY user,model ORDER BY user,model', (day,))]
    per_model = [dict(zip(('model','calls','usd_including_reservations'),row)) for row in db.execute(
        'SELECT model,COUNT(*),SUM(COALESCE(actual,cap)) FROM calls WHERE day=? GROUP BY model ORDER BY model', (day,))]
finally:
    db.close()
files = ['iald_web_server.py','iald_motores.py','iald_orcamento.py','iald_memoria_canonica.py','app/iald.js','app/iald.css']
receipt = {'at':datetime.now().astimezone().isoformat(), 'status':'VERIFIED_READ_ONLY',
    'numeric_env':selected,'owner':{'username':'luiz','admin':True,'somente_limite_global':True,'motor':'openai'},
    'day_utc':day,'spending_by_account_and_model':account_model,'spending_by_model':per_model,
    'hashes':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
    'browser_verified': {'two_actual_responses':True,'labels_survived_reload':True,'switch_preserved_history':True,
        'usage_text':'Sem limite individual; uso global inclui reservas; US$3.00/dia'},
    'limitations':['Spending snapshot is local recorded cost including reservations, not provider credit balance.',
        'Native inference has no external API charge in this ledger.',
        'Free plan full-core compatibility remains OPEN and unchanged.']}
target = WORK/'runtime_verification.json'
assert not target.exists()
data=json.dumps(receipt,ensure_ascii=False,indent=2).encode()
temp=target.with_suffix('.tmp')
with temp.open('xb') as f: f.write(data)
assert temp.stat().st_size==len(data)
temp.replace(target)
print(json.dumps({'receipt':str(target),'quotas_match':True,'owner_global_only':True,'spending_models':per_model},ensure_ascii=False))
