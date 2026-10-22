"""Synthetic retained event -> frozen staged ChatJobs.get -> real Flask JSON. No live imports."""
import sys,types,json,hashlib,tempfile,time,socket
from pathlib import Path
from unittest.mock import patch
from flask import Flask,jsonify
HERE=Path(__file__).resolve().parent
BACKEND=HERE.parent/'backend'
sys.path.insert(0,str(BACKEND))
sys.modules['iald_app_memory']=types.ModuleType('iald_app_memory')
import iald_chat_jobs as jobs
class SyntheticCipher:
    def seal(self,b): return b'SYNTHETIC_ONLY:'+b
    def open(self,b):
        assert b.startswith(b'SYNTHETIC_ONLY:')
        return b[len(b'SYNTHETIC_ONLY:'):]
app=Flask(__name__)
ID='12345678-1234-4234-8234-123456789abc'
with patch.object(socket.socket,'connect',side_effect=AssertionError('NETWORK_FORBIDDEN')), tempfile.TemporaryDirectory(dir=HERE) as tmp:
    store=jobs.ChatJobs(tmp,cipher=SyntheticCipher())
    with store.db() as db:
        db.execute('INSERT INTO jobs(id,owner,digest,conversation_id,status,created,updated) VALUES(?,?,?,?,?,?,?)',(ID,jobs.owner_key('synthetic'),'synthetic','conversation1','completed',time.time(),time.time()))
    event=json.dumps({'choices':[{'delta':{'content':'é'*6000000}}]},ensure_ascii=False,separators=(',',':'))
    store.append(ID,event)
    store.append(ID,'[DONE]')
    for after,name in [(0,'large_identity_page.json'),(1,'done_identity_page.json')]:
        page=store.get('synthetic',ID,after=after)
        with app.app_context(): raw=jsonify(page).get_data()
        (HERE/name).write_bytes(raw)
        if after==0: first=raw
    report={'statute':'REAL','stored_event_utf8_bytes':len(event.encode()),'page_bytes':len(first),'page_sha256':hashlib.sha256(first).hexdigest(),'event_sha256':hashlib.sha256(event.encode()).hexdigest(),'backend_source_sha256':hashlib.sha256((BACKEND/'iald_chat_jobs.py').read_bytes()).hexdigest(),'cipher':'synthetic prefix, no compression; not DPAPI validation','network_calls':0,'provider_calls':0}
    (HERE/'FIXTURE_RESULT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report))
