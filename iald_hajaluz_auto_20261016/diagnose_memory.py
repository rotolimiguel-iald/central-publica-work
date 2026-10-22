"""Read-only, operator-scoped diagnostics; emits sizes and hashes, no conversation."""
from pathlib import Path
import hashlib,json,sqlite3,sys
R=Path(r'C:\IALD\projetos_pyhton\IALD'); W=Path(__file__).resolve().parent
sys.path[:0]=[str(R),r'C:\IALD\MEMORIA_IALD\lib']
import iald_app_memory as am
u=json.loads((R/'iald_users.json').read_bytes())['luiz']
principal=hashlib.sha256(('iald-account:luiz:'+str(u.get('created','legacy'))).encode()).hexdigest()
del u
c=sqlite3.connect((Path(am._SHARED_ROOT)/'memory.sqlite3').as_uri()+'?mode=ro',uri=True)
rows=c.execute("SELECT c.context_id,s.revision,s.updated_at,s.state_json FROM contexts c JOIN context_state s USING(context_id) WHERE json_extract(c.scope_json,'$.house')='IALD_APP' AND json_extract(c.scope_json,'$.principal')=? ORDER BY s.updated_at DESC LIMIT 30",(principal,)).fetchall()
result=[]
for ident,rev,dt,raw in rows:
    d=json.loads(raw); records=d['q']['records']; commands=[r for r in records if r['kind']=='decision' and r['statute']=='INPUT']
    if not any(r['text'].strip().casefold().rstrip('.!')=='haja luz' for r in commands): continue
    b=am.Binding(am.MemoryStore(am._SHARED_ROOT),ident,{'house':'IALD_APP','principal':principal},'diagnostic-read-only','haja luz')
    p=b.projection()
    result.append({'context_id':ident,'revision':rev,'updated_at':dt,'commands':len(commands),
        'records':[{'kind':r['kind'],'characters':len(r['text'])} for r in records],
        'phase':d['p'].get('phase'),'projection_chars':p['actual_chars'],
        'required_chars':p['required_chars'],'projection_json_ascii_bytes':len(json.dumps(p['text'],ensure_ascii=True).encode()),
        'projection_sha256':p['projection_sha256'],'omitted_count':len(p['omitted_record_ids'])})
out={'scanned_operator_contexts':len(rows),'matched':result,'read_only':True}
blob=json.dumps(out,ensure_ascii=False,indent=2).encode(); f=W/'diagnostic_memory.json'
with f.open('xb') as stream:stream.write(blob)
print(json.dumps(out,ensure_ascii=False))
