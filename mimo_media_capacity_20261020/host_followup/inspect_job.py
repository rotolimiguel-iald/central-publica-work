import sqlite3,json,hashlib,zlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
LIVE=Path('C:/IALD/projetos_pyhton/IALD')
JOB='cfe3165d-67b3-4e1e-bbb9-ac906080ec71'
CONV='c_mvh7ykird3r4'
def ro(p):
    c=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
out={}
with ro(LIVE/'.iald_runtime/chat_jobs/jobs.sqlite3') as db:
    r=db.execute('SELECT * FROM jobs WHERE id=? AND conversation_id=?',(JOB,CONV)).fetchone()
    assert r
    out['job']={k:r[k] for k in ('id','conversation_id','status','seq','error')}
with ro(LIVE/'.iald_runtime/private_media/media.sqlite3') as db:
    rows=db.execute('SELECT id,generation,metadata,status FROM media WHERE owner=? AND conversation=?',('luiz',CONV)).fetchall()
    assert rows
    out['media']=[dict(id=r['id'],metadata=json.loads(r['metadata']),status=r['status']) for r in rows]
    gen=rows[0]['generation']
ctx='app_'+hashlib.sha256((gen+':'+CONV).encode()).hexdigest()
with ro(Path('C:/IALD/MEMORIA_IALD/state/memory.sqlite3')) as db:
    row=db.execute('SELECT * FROM contexts WHERE context_id=? AND scope_json=?',(ctx,json.dumps({'house':'IALD_APP','principal':gen},sort_keys=True,separators=(',',':')))).fetchone()
    assert row,'exact context/scope absent'
    events=db.execute('SELECT revision,event_id,changes_json,state_json FROM events WHERE context_id=? ORDER BY revision',(ctx,)).fetchall()
    out['acom']={'context_id':ctx,'scope_verified':True,'events':[dict(revision=r['revision'],event_id=r['event_id']) for r in events]}
    # Retain only this explicitly authorized scope; no other context is read.
    (HERE/'SCOPED_ACOM_INPUT.json').write_text(json.dumps(dict(context_id=ctx,scope=json.loads(row['scope_json']),objective=zlib.decompress(row['objective_blob']).decode(),events=[dict(r) for r in events]),ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'SCOPED_JOB_METADATA.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
