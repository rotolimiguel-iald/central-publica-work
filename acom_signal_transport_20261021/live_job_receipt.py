"""Observe only job metadata in a bounded synthetic-test time window."""
from pathlib import Path
import json,sqlite3,time,sys
from task import W,new,check
dbpath=Path(r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\chat_jobs\jobs.sqlite3')
check('deployment')
if sys.argv[1]=='begin':
    new('LIVE_INTENT.json',{'started':time.time(),'synthetic_fixture':str(W/'LIVE_FIXTURE.json'),'no_repeat':True})
    print('Synthetic test window opened; no message sent by this script')
elif sys.argv[1]=='observe':
    start=json.loads((W/'LIVE_INTENT.json').read_bytes())['started']
    with sqlite3.connect(dbpath.as_uri()+'?mode=ro',uri=True) as db:
        db.row_factory=sqlite3.Row
        rows=[dict(r) for r in db.execute('SELECT id,status,created,updated,acknowledged,cancel_requested,seq,size,expired FROM jobs WHERE created>=? ORDER BY created',(start,))]
    if len(rows)!=1:raise RuntimeError('Expected exactly one test-window job; no attribution guessed')
    print(json.dumps(rows[0]))
    if rows[0]['status'] in ('completed','failed','cancelled','interrupted','expired'):
        new('LIVE_JOB_RESULT.json',{'job':rows[0],'scope':'Single new job in synthetic test window; no event content or credentials read','observed_at':time.time()})
else:raise ValueError('Explicit begin/observe required')
