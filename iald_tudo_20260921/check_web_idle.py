from pathlib import Path
import json,sqlite3,urllib.request
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
counts={}
for name in ('iald_uso_claude.json.reservas.sqlite3','iald_uso_openai.json.reservas.sqlite3'):
    path=ROOT/name
    with sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)as db:
        counts[name]=db.execute("SELECT count(*) FROM calls WHERE status='reserved'").fetchone()[0]
with urllib.request.urlopen('http://127.0.0.1:8081/slots',timeout=5)as r:slots=json.load(r)
if not isinstance(slots,list):raise ValueError('Cannot check native slots')
active=sum(1 for s in slots if s.get('is_processing'))
print(json.dumps({'external_reserved':counts,'native_processing':active}))
if any(counts.values()) or active:raise SystemExit(2)
